"""Helpers for Binance USD-M Futures market sync and order validation."""

from __future__ import annotations

import hashlib
import hmac
import json
import math
import os
import statistics
import time
from decimal import Decimal, ROUND_DOWN, ROUND_UP
from typing import Any, Dict, Iterable, List
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


DEFAULT_TIMEOUT_SECONDS = 4.0
DEFAULT_RECV_WINDOW_MS = 5000
TRACKED_ACCOUNT_SYMBOLS = ("BNBUSDT", "BTCUSDT", "ETHUSDT")
BENCHMARK_SYMBOLS = ("BTCUSDT", "BNBUSDT", "ETHUSDT")
DEFAULT_DEMO_API_BASE = "https://testnet.binancefuture.com"
DEFAULT_LIVE_API_BASE = "https://fapi.binance.com"
SYMBOL_TRADING_RULES_CACHE: Dict[str, Dict[str, str]] = {}
SAFE_LIVE_ORDER_MAX_NOTIONAL_USDT = Decimal("5")

DEFAULT_MARKET_FALLBACKS: Dict[str, Dict[str, float]] = {
    "BNBUSDT": {
        "entry_price": 640.0,
        "stop_loss_price": 626.0,
        "take_profit_price": 668.0,
        "volatility_24h_pct": 5.1,
        "bid_ask_spread_bps": 4.0,
        "liquidity_depth_score": 88.0,
    },
    "BTCUSDT": {
        "entry_price": 91300.0,
        "stop_loss_price": 90000.0,
        "take_profit_price": 93900.0,
        "volatility_24h_pct": 3.8,
        "bid_ask_spread_bps": 2.5,
        "liquidity_depth_score": 95.0,
    },
    "ETHUSDT": {
        "entry_price": 4700.0,
        "stop_loss_price": 4620.0,
        "take_profit_price": 4860.0,
        "volatility_24h_pct": 5.7,
        "bid_ask_spread_bps": 3.5,
        "liquidity_depth_score": 90.0,
    },
    "SOLUSDT": {
        "entry_price": 182.0,
        "stop_loss_price": 176.0,
        "take_profit_price": 193.0,
        "volatility_24h_pct": 6.4,
        "bid_ask_spread_bps": 5.2,
        "liquidity_depth_score": 86.0,
    },
    "XRPUSDT": {
        "entry_price": 2.34,
        "stop_loss_price": 2.27,
        "take_profit_price": 2.47,
        "volatility_24h_pct": 5.9,
        "bid_ask_spread_bps": 4.6,
        "liquidity_depth_score": 87.0,
    },
    "DOGEUSDT": {
        "entry_price": 0.31,
        "stop_loss_price": 0.298,
        "take_profit_price": 0.334,
        "volatility_24h_pct": 7.8,
        "bid_ask_spread_bps": 6.5,
        "liquidity_depth_score": 82.0,
    },
    "ADAUSDT": {
        "entry_price": 1.18,
        "stop_loss_price": 1.13,
        "take_profit_price": 1.28,
        "volatility_24h_pct": 6.1,
        "bid_ask_spread_bps": 5.4,
        "liquidity_depth_score": 84.0,
    },
}

DEFAULT_ACCOUNT_FALLBACKS: Dict[str, Dict[str, Any]] = {
    "BNBUSDT": {
        "estimated_equity_usdt": 2200.0,
        "available_usdt": 860.0,
        "locked_usdt": 90.0,
        "open_orders_count": 1,
        "nonzero_assets": [
            {"asset": "USDT", "free": 860.0, "locked": 90.0, "estimated_usdt": 950.0},
            {"asset": "BNB", "free": 1.95, "locked": 0.0, "estimated_usdt": 1248.0},
        ],
        "behavior": {
            "trades_last_24h": 12,
            "consecutive_losses": 2,
            "day_pnl_pct": -2.8,
            "realized_pnl_24h_usdt": -61.6,
        },
    },
    "BTCUSDT": {
        "estimated_equity_usdt": 4000.0,
        "available_usdt": 1650.0,
        "locked_usdt": 150.0,
        "open_orders_count": 2,
        "nonzero_assets": [
            {"asset": "USDT", "free": 1650.0, "locked": 150.0, "estimated_usdt": 1800.0},
            {"asset": "BTC", "free": 0.024, "locked": 0.0, "estimated_usdt": 2200.0},
        ],
        "behavior": {
            "trades_last_24h": 8,
            "consecutive_losses": 1,
            "day_pnl_pct": -1.4,
            "realized_pnl_24h_usdt": -56.0,
        },
    },
    "ETHUSDT": {
        "estimated_equity_usdt": 2500.0,
        "available_usdt": 980.0,
        "locked_usdt": 120.0,
        "open_orders_count": 1,
        "nonzero_assets": [
            {"asset": "USDT", "free": 980.0, "locked": 120.0, "estimated_usdt": 1100.0},
            {"asset": "ETH", "free": 0.3, "locked": 0.0, "estimated_usdt": 1400.0},
        ],
        "behavior": {
            "trades_last_24h": 10,
            "consecutive_losses": 2,
            "day_pnl_pct": -2.2,
            "realized_pnl_24h_usdt": -55.0,
        },
    },
    "SOLUSDT": {
        "estimated_equity_usdt": 2600.0,
        "available_usdt": 1120.0,
        "locked_usdt": 130.0,
        "open_orders_count": 2,
        "nonzero_assets": [
            {"asset": "USDT", "free": 1120.0, "locked": 130.0, "estimated_usdt": 1250.0},
            {"asset": "SOL", "free": 7.4, "locked": 0.0, "estimated_usdt": 1346.8},
        ],
        "behavior": {
            "trades_last_24h": 14,
            "consecutive_losses": 2,
            "day_pnl_pct": -2.6,
            "realized_pnl_24h_usdt": -67.6,
        },
    },
    "XRPUSDT": {
        "estimated_equity_usdt": 2400.0,
        "available_usdt": 980.0,
        "locked_usdt": 100.0,
        "open_orders_count": 1,
        "nonzero_assets": [
            {"asset": "USDT", "free": 980.0, "locked": 100.0, "estimated_usdt": 1080.0},
            {"asset": "XRP", "free": 564.0, "locked": 0.0, "estimated_usdt": 1319.76},
        ],
        "behavior": {
            "trades_last_24h": 11,
            "consecutive_losses": 1,
            "day_pnl_pct": -1.8,
            "realized_pnl_24h_usdt": -43.2,
        },
    },
    "DOGEUSDT": {
        "estimated_equity_usdt": 2200.0,
        "available_usdt": 890.0,
        "locked_usdt": 110.0,
        "open_orders_count": 2,
        "nonzero_assets": [
            {"asset": "USDT", "free": 890.0, "locked": 110.0, "estimated_usdt": 1000.0},
            {"asset": "DOGE", "free": 3800.0, "locked": 0.0, "estimated_usdt": 1178.0},
        ],
        "behavior": {
            "trades_last_24h": 18,
            "consecutive_losses": 3,
            "day_pnl_pct": -4.2,
            "realized_pnl_24h_usdt": -92.4,
        },
    },
    "ADAUSDT": {
        "estimated_equity_usdt": 2300.0,
        "available_usdt": 960.0,
        "locked_usdt": 120.0,
        "open_orders_count": 1,
        "nonzero_assets": [
            {"asset": "USDT", "free": 960.0, "locked": 120.0, "estimated_usdt": 1080.0},
            {"asset": "ADA", "free": 1035.0, "locked": 0.0, "estimated_usdt": 1221.3},
        ],
        "behavior": {
            "trades_last_24h": 13,
            "consecutive_losses": 2,
            "day_pnl_pct": -2.4,
            "realized_pnl_24h_usdt": -55.2,
        },
    },
}

PROFILE_REWARD_RISK = {
    "conservative": 2.0,
    "balanced": 1.8,
    "aggressive": 1.5,
}

PROFILE_POSITION_VS_EQUITY = {
    "conservative": 0.9,
    "balanced": 1.2,
    "aggressive": 1.5,
}

PROFILE_RISK_PER_TRADE = {
    "conservative": 0.8,
    "balanced": 1.5,
    "aggressive": 2.0,
}

PROFILE_STOP_DISTANCE = {
    "conservative": 0.85,
    "balanced": 1.15,
    "aggressive": 1.45,
}


def _clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def _exchange_context() -> Dict[str, str]:
    api_base = (
        os.getenv("BINANCE_FUTURES_API_BASE", "").strip()
        or os.getenv("BINANCE_SPOT_API_BASE", "").strip()
        or os.getenv("BINANCE_API_BASE", "").strip()
        or os.getenv("BINANCE_DEMO_API_BASE", "").strip()
    )
    configured_mode = (
        os.getenv("BINANCE_FUTURES_ENV", "").strip().lower()
        or os.getenv("BINANCE_SPOT_ENV", "").strip().lower()
    )
    inferred_mode = "demo" if "testnet" in api_base else "live"
    mode = configured_mode if configured_mode in {"demo", "live"} else inferred_mode
    resolved_base = api_base or (
        DEFAULT_DEMO_API_BASE if mode == "demo" else DEFAULT_LIVE_API_BASE
    )
    source_key = "binance_futures_demo" if mode == "demo" else "binance_futures_live"
    label = "Binance USD-M Futures Testnet" if mode == "demo" else "Binance USD-M Futures API"
    return {
        "venue": "binance",
        "mode": mode,
        "product": "usd_m_futures",
        "label": label,
        "source_key": source_key,
        "api_base": resolved_base,
    }


def _api_base() -> str:
    return str(_exchange_context()["api_base"])


def _exchange_label() -> str:
    return str(_exchange_context()["label"])


def _exchange_source_key() -> str:
    return str(_exchange_context()["source_key"])


def _credential_env_names() -> tuple[str, str]:
    configured_mode = (
        os.getenv("BINANCE_FUTURES_ENV", "").strip().lower()
        or os.getenv("BINANCE_SPOT_ENV", "").strip().lower()
    )
    if configured_mode == "live":
        return "BINANCE_API_KEY", "BINANCE_SECRET_KEY"
    if configured_mode == "demo":
        return "BINANCE_DEMO_API_KEY", "BINANCE_DEMO_SECRET_KEY"
    api_key = os.getenv("BINANCE_API_KEY", "").strip()
    secret_key = os.getenv("BINANCE_SECRET_KEY", "").strip()
    if api_key or secret_key:
        return "BINANCE_API_KEY", "BINANCE_SECRET_KEY"
    if _exchange_context()["mode"] == "live":
        return "BINANCE_API_KEY", "BINANCE_SECRET_KEY"
    return "BINANCE_DEMO_API_KEY", "BINANCE_DEMO_SECRET_KEY"


def _credentials_hint_text(target: str) -> str:
    api_name, secret_name = _credential_env_names()
    return f"Set {api_name} and {secret_name} to enable {target}."


def _configured_credentials() -> tuple[str, str]:
    api_key = os.getenv("BINANCE_API_KEY", "").strip()
    secret_key = os.getenv("BINANCE_SECRET_KEY", "").strip()
    if api_key and secret_key:
        return api_key, secret_key
    return (
        os.getenv("BINANCE_DEMO_API_KEY", "").strip(),
        os.getenv("BINANCE_DEMO_SECRET_KEY", "").strip(),
    )


def _is_demo_mode() -> bool:
    return str(_exchange_context()["mode"]) == "demo"


def _futures_dual_side_position(api_key: str, secret_key: str) -> bool:
    try:
        payload = _signed_json(
            "/fapi/v1/positionSide/dual",
            api_key=api_key,
            secret_key=secret_key,
            params={},
        )
    except Exception:
        return False
    value = payload.get("dualSidePosition")
    if isinstance(value, bool):
        return value
    return str(value).lower() == "true"


def _apply_position_side(
    preview: Dict[str, Any],
    *,
    dual_side_position: bool,
) -> Dict[str, Any]:
    if not dual_side_position:
        return dict(preview)
    enriched = dict(preview)
    enriched["positionSide"] = str(preview["intent_side"])
    return enriched


def _load_json_response(request: Request, *, timeout: float = DEFAULT_TIMEOUT_SECONDS) -> Any:
    try:
        with urlopen(request, timeout=timeout) as response:
            body = response.read().decode("utf-8")
            return json.loads(body) if body else {}
    except HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        try:
            payload = json.loads(detail)
        except json.JSONDecodeError:
            payload = {"msg": detail or exc.reason}
        raise RuntimeError(
            f"{_exchange_label()} HTTP {exc.code}: {payload.get('msg', detail or 'request failed')}"
        ) from exc
    except URLError as exc:
        raise RuntimeError(f"{_exchange_label()} network error: {exc.reason}") from exc


def _http_json(
    path: str,
    *,
    method: str = "GET",
    params: Dict[str, Any] | None = None,
    headers: Dict[str, str] | None = None,
    timeout: float = DEFAULT_TIMEOUT_SECONDS,
) -> Any:
    query = urlencode(params or {})
    url = f"{_api_base()}{path}"
    if query:
        url = f"{url}?{query}"
    request = Request(url, method=method, headers=headers or {})
    return _load_json_response(request, timeout=timeout)


def _close_prices_from_klines(klines: Iterable[List[Any]]) -> List[float]:
    closes: List[float] = []
    for row in klines:
        if len(row) > 4:
            try:
                closes.append(float(row[4]))
            except (TypeError, ValueError):
                continue
    return closes


def _realized_volatility_pct(klines: Iterable[List[Any]]) -> float:
    closes = _close_prices_from_klines(klines)
    if len(closes) < 2:
        return 0.0

    returns: List[float] = []
    for idx in range(1, len(closes)):
        prev_close = closes[idx - 1]
        current_close = closes[idx]
        if prev_close <= 0 or current_close <= 0:
            continue
        returns.append(math.log(current_close / prev_close))

    if len(returns) < 2:
        return 0.0
    return statistics.pstdev(returns) * math.sqrt(24.0) * 100.0


def _depth_score(depth_payload: Dict[str, Any]) -> float:
    total_quote = 0.0
    for side in ("bids", "asks"):
        for row in depth_payload.get(side, [])[:20]:
            if len(row) < 2:
                continue
            try:
                total_quote += float(row[0]) * float(row[1])
            except (TypeError, ValueError):
                continue

    if total_quote <= 0:
        return 25.0
    # Maps roughly from 10k quote depth -> 0 to 100m -> 100.
    return _clamp((math.log10(total_quote) - 4.0) * 25.0, 0.0, 100.0)


def _format_decimal(value: float, decimals: int) -> str:
    quant = Decimal("1").scaleb(-decimals)
    return format(Decimal(str(value)).quantize(quant, rounding=ROUND_DOWN), "f")


def _decimal_places(value_text: str) -> int:
    normalized = Decimal(str(value_text)).normalize()
    return max(0, -normalized.as_tuple().exponent)


def _format_by_increment(value: float, increment_text: str, fallback_decimals: int) -> str:
    try:
        increment = Decimal(str(increment_text))
    except Exception:
        return _format_decimal(value, fallback_decimals)
    if increment <= 0:
        return _format_decimal(value, fallback_decimals)

    value_decimal = Decimal(str(value))
    steps = (value_decimal / increment).to_integral_value(rounding=ROUND_DOWN)
    adjusted = steps * increment
    quant = Decimal("1").scaleb(-_decimal_places(str(increment)))
    return format(adjusted.quantize(quant, rounding=ROUND_DOWN), "f")


def _price_precision(price: float) -> int:
    if price >= 10000:
        return 2
    if price >= 100:
        return 2
    if price >= 1:
        return 3
    return 6


def _quantity_precision(price: float) -> int:
    if price >= 10000:
        return 5
    if price >= 100:
        return 4
    return 3


def _reward_risk_target(profile_name: str | None) -> float:
    return PROFILE_REWARD_RISK.get(str(profile_name or "").lower(), 1.8)


def _position_vs_equity_limit(profile_name: str | None) -> float:
    return PROFILE_POSITION_VS_EQUITY.get(str(profile_name or "").lower(), 1.2)


def _risk_per_trade_limit(profile_name: str | None) -> float:
    return PROFILE_RISK_PER_TRADE.get(str(profile_name or "").lower(), 1.5)


def _stop_distance_pct(profile_name: str | None, volatility_24h_pct: float) -> float:
    profile_base = PROFILE_STOP_DISTANCE.get(str(profile_name or "").lower(), 1.15)
    volatility_component = max(0.0, volatility_24h_pct) * 0.20
    return _clamp(max(profile_base, volatility_component), 0.6, 3.5)


def build_market_snapshot(
    *,
    symbol: str,
    side: str,
    profile_name: str | None,
    ticker_24h: Dict[str, Any],
    depth_payload: Dict[str, Any],
    klines_payload: List[List[Any]],
    chart_klines_payload: List[List[Any]] | None = None,
    benchmark_prices: Dict[str, float] | None = None,
    live: bool,
    warning: str | None = None,
) -> Dict[str, Any]:
    normalized_symbol = str(symbol).upper()
    normalized_side = str(side).upper() if side else "LONG"
    profile = str(profile_name or "balanced").lower()

    last_price = float(ticker_24h.get("lastPrice", 0.0) or 0.0)
    weighted_avg_price = float(ticker_24h.get("weightedAvgPrice", last_price) or last_price)
    bid_price = float(ticker_24h.get("bidPrice", last_price) or last_price)
    ask_price = float(ticker_24h.get("askPrice", last_price) or last_price)
    mid_price = (bid_price + ask_price) / 2.0 if bid_price > 0 and ask_price > 0 else last_price
    spread_bps = (
        ((ask_price - bid_price) / mid_price) * 10000.0
        if bid_price > 0 and ask_price > 0 and mid_price > 0
        else 0.0
    )
    realized_volatility = _realized_volatility_pct(klines_payload)
    fallback_volatility = abs(float(ticker_24h.get("priceChangePercent", 0.0) or 0.0))
    volatility_24h_pct = _clamp(
        realized_volatility if realized_volatility > 0 else fallback_volatility,
        0.0,
        25.0,
    )
    liquidity_depth_score = _depth_score(depth_payload)

    entry_price = ask_price if normalized_side == "LONG" else bid_price
    if entry_price <= 0:
        entry_price = last_price or weighted_avg_price

    stop_distance_pct = _stop_distance_pct(profile, volatility_24h_pct)
    reward_risk_target = _reward_risk_target(profile)
    if normalized_side == "LONG":
        stop_loss_price = entry_price * (1.0 - stop_distance_pct / 100.0)
        take_profit_price = entry_price * (
            1.0 + (stop_distance_pct * reward_risk_target) / 100.0
        )
    else:
        stop_loss_price = entry_price * (1.0 + stop_distance_pct / 100.0)
        take_profit_price = entry_price * (
            1.0 - (stop_distance_pct * reward_risk_target) / 100.0
        )

    precision = _price_precision(entry_price)
    chart_payload = chart_klines_payload if isinstance(chart_klines_payload, list) else klines_payload
    chart_candles: List[Dict[str, Any]] = []
    for row in chart_payload[-48:]:
        if not isinstance(row, list) or len(row) < 5:
            continue
        open_price = round(_safe_float(row[1]), precision)
        high_price = round(_safe_float(row[2]), precision)
        low_price = round(_safe_float(row[3]), precision)
        close_price = round(_safe_float(row[4]), precision)
        volume = round(_safe_float(row[5] if len(row) > 5 else 0.0), 2)
        chart_candles.append(
            {
                "open_time": int(row[0] or 0),
                "open": open_price,
                "high": high_price,
                "low": low_price,
                "close": close_price,
                "volume": volume,
            }
        )
    benchmark_source = benchmark_prices or {}
    benchmarks: List[Dict[str, Any]] = []
    for benchmark_symbol in BENCHMARK_SYMBOLS:
        raw_price = benchmark_source.get(benchmark_symbol)
        if raw_price is None:
            raw_price = DEFAULT_MARKET_FALLBACKS.get(benchmark_symbol, {}).get("entry_price")
        if raw_price is None:
            continue
        price = float(raw_price)
        benchmarks.append(
            {
                "symbol": benchmark_symbol,
                "last_price": round(price, _price_precision(price)),
            }
        )

    return {
        "symbol": normalized_symbol,
        "side": normalized_side,
        "profile": profile,
        "live": live,
        "source": _exchange_source_key() if live else "local_fallback",
        "exchange_context": _exchange_context(),
        "warning": warning,
        "market": {
            "last_price": round(last_price, precision),
            "weighted_avg_price": round(weighted_avg_price, precision),
            "bid_price": round(bid_price, precision),
            "ask_price": round(ask_price, precision),
            "volatility_24h_pct": round(volatility_24h_pct, 2),
            "bid_ask_spread_bps": round(spread_bps, 2),
            "liquidity_depth_score": round(liquidity_depth_score, 2),
        },
        "suggested_trade": {
            "entry_price": round(entry_price, precision),
            "stop_loss_price": round(stop_loss_price, precision),
            "take_profit_price": round(take_profit_price, precision),
            "target_reward_risk_ratio": round(reward_risk_target, 2),
        },
        "benchmarks": benchmarks,
        "chart": {
            "interval": "5m",
            "candles": chart_candles,
        },
    }


def fallback_market_snapshot(
    symbol: str,
    *,
    side: str = "LONG",
    profile_name: str | None = None,
    warning: str | None = None,
) -> Dict[str, Any]:
    normalized_symbol = str(symbol).upper()
    preset = DEFAULT_MARKET_FALLBACKS.get(normalized_symbol, DEFAULT_MARKET_FALLBACKS["BNBUSDT"])
    precision = _price_precision(preset["entry_price"])
    reward_risk_target = _reward_risk_target(profile_name)
    now_ms = int(time.time() * 1000)
    chart_candles: List[Dict[str, Any]] = []
    base_price = float(preset["entry_price"])
    for idx in range(48):
        wave = math.sin(idx / 4.8) * base_price * 0.006
        drift = (idx - 24) * base_price * 0.00045
        open_price = base_price + drift + wave
        close_price = open_price + math.cos(idx / 3.6) * base_price * 0.0028
        high_price = max(open_price, close_price) + base_price * 0.0019
        low_price = min(open_price, close_price) - base_price * 0.0017
        chart_candles.append(
            {
                "open_time": now_ms - ((47 - idx) * 5 * 60 * 1000),
                "open": round(open_price, precision),
                "high": round(high_price, precision),
                "low": round(low_price, precision),
                "close": round(close_price, precision),
                "volume": round(180 + (idx % 7) * 16.5, 2),
            }
        )
    benchmarks = [
        {
            "symbol": benchmark_symbol,
            "last_price": round(
                float(DEFAULT_MARKET_FALLBACKS[benchmark_symbol]["entry_price"]),
                _price_precision(float(DEFAULT_MARKET_FALLBACKS[benchmark_symbol]["entry_price"])),
            ),
        }
        for benchmark_symbol in BENCHMARK_SYMBOLS
        if benchmark_symbol in DEFAULT_MARKET_FALLBACKS
    ]
    return {
        "symbol": normalized_symbol,
        "side": str(side).upper() if side else "LONG",
        "profile": str(profile_name or "balanced").lower(),
        "live": False,
        "source": "local_fallback",
        "exchange_context": _exchange_context(),
        "warning": warning,
        "market": {
            "last_price": round(preset["entry_price"], precision),
            "weighted_avg_price": round(preset["entry_price"], precision),
            "bid_price": round(preset["entry_price"] * 0.999, precision),
            "ask_price": round(preset["entry_price"] * 1.001, precision),
            "volatility_24h_pct": round(preset["volatility_24h_pct"], 2),
            "bid_ask_spread_bps": round(preset["bid_ask_spread_bps"], 2),
            "liquidity_depth_score": round(preset["liquidity_depth_score"], 2),
        },
        "suggested_trade": {
            "entry_price": round(preset["entry_price"], precision),
            "stop_loss_price": round(preset["stop_loss_price"], precision),
            "take_profit_price": round(preset["take_profit_price"], precision),
            "target_reward_risk_ratio": round(reward_risk_target, 2),
        },
        "benchmarks": benchmarks,
        "chart": {
            "interval": "5m",
            "candles": chart_candles,
        },
    }


def get_market_snapshot(
    symbol: str,
    *,
    side: str = "LONG",
    profile_name: str | None = None,
) -> Dict[str, Any]:
    normalized_symbol = str(symbol).upper()
    try:
        benchmark_prices: Dict[str, float] = {}
        ticker_24h = _http_json("/fapi/v1/ticker/24hr", params={"symbol": normalized_symbol})
        depth_payload = _http_json(
            "/fapi/v1/depth", params={"symbol": normalized_symbol, "limit": 20}
        )
        klines_payload = _http_json(
            "/fapi/v1/klines", params={"symbol": normalized_symbol, "interval": "1h", "limit": 24}
        )
        chart_klines_payload = _http_json(
            "/fapi/v1/klines", params={"symbol": normalized_symbol, "interval": "5m", "limit": 48}
        )
        for benchmark_symbol in BENCHMARK_SYMBOLS:
            try:
                benchmark_payload = _http_json(
                    "/fapi/v1/ticker/price", params={"symbol": benchmark_symbol}
                )
                benchmark_prices[benchmark_symbol] = _safe_float(benchmark_payload.get("price"))
            except Exception:
                fallback_price = DEFAULT_MARKET_FALLBACKS.get(benchmark_symbol, {}).get("entry_price")
                if fallback_price is not None:
                    benchmark_prices[benchmark_symbol] = float(fallback_price)
        return build_market_snapshot(
            symbol=normalized_symbol,
            side=side,
            profile_name=profile_name,
            ticker_24h=ticker_24h,
            depth_payload=depth_payload,
            klines_payload=klines_payload,
            chart_klines_payload=chart_klines_payload if isinstance(chart_klines_payload, list) else [],
            benchmark_prices=benchmark_prices,
            live=True,
        )
    except Exception as exc:
        return fallback_market_snapshot(
            normalized_symbol,
            side=side,
            profile_name=profile_name,
            warning=str(exc),
        )


def _normalize_order_intent(side_value: Any) -> tuple[str, str]:
    normalized = str(side_value).upper()
    mapping = {
        "LONG": ("LONG", "BUY"),
        "SHORT": ("SHORT", "SELL"),
        "BUY": ("LONG", "BUY"),
        "SELL": ("SHORT", "SELL"),
    }
    if normalized not in mapping:
        raise ValueError(
            "trade.side must be LONG or SHORT for risk intent, or BUY or SELL for spot preview."
        )
    return mapping[normalized]


def _select_symbol_payload(symbol: str, exchange_info_payload: Dict[str, Any]) -> Dict[str, Any]:
    normalized_symbol = str(symbol).upper()
    symbols = exchange_info_payload.get("symbols", [])
    if not symbols:
        raise ValueError(f"No exchangeInfo returned for {normalized_symbol}.")

    for item in symbols:
        if str(item.get("symbol", "")).upper() == normalized_symbol:
            return item

    if len(symbols) == 1:
        return symbols[0]
    raise ValueError(f"{normalized_symbol} was not present in exchangeInfo response.")


def _extract_symbol_trading_rules(symbol: str, exchange_info_payload: Dict[str, Any]) -> Dict[str, str]:
    symbol_payload = _select_symbol_payload(symbol, exchange_info_payload)
    filters = {
        str(item.get("filterType", "")): item for item in symbol_payload.get("filters", [])
    }
    lot_size = filters.get("LOT_SIZE", {})
    price_filter = filters.get("PRICE_FILTER", {})
    notional_filter = filters.get("NOTIONAL") or filters.get("MIN_NOTIONAL") or {}
    return {
        "step_size": str(lot_size.get("stepSize", "0")),
        "min_qty": str(lot_size.get("minQty", "0")),
        "max_qty": str(lot_size.get("maxQty", "0")),
        "tick_size": str(price_filter.get("tickSize", "0")),
        "min_price": str(price_filter.get("minPrice", "0")),
        "max_price": str(price_filter.get("maxPrice", "0")),
        "min_notional": str(notional_filter.get("notional", notional_filter.get("minNotional", "0"))),
        "price_precision": str(symbol_payload.get("pricePrecision", "")),
        "quantity_precision": str(symbol_payload.get("quantityPrecision", "")),
    }


def _get_symbol_trading_rules(symbol: str) -> Dict[str, str]:
    normalized_symbol = str(symbol).upper()
    cached = SYMBOL_TRADING_RULES_CACHE.get(normalized_symbol)
    if cached is not None:
        return cached

    payload = _http_json("/fapi/v1/exchangeInfo", params={"symbol": normalized_symbol})
    rules = _extract_symbol_trading_rules(normalized_symbol, payload)
    SYMBOL_TRADING_RULES_CACHE[normalized_symbol] = rules
    return rules


def _preview_filter_issue(preview: Dict[str, Any], trading_rules: Dict[str, str]) -> str | None:
    quantity = Decimal(str(preview["quantity"]))
    market_reference = preview.get("market_reference") if isinstance(preview, dict) else None
    reference_price = ""
    if isinstance(market_reference, dict):
        reference_price = str(
            market_reference.get("execution_reference_price")
            or market_reference.get("ask_price")
            or market_reference.get("bid_price")
            or ""
        )
    price = Decimal(str(preview.get("price") or reference_price or "0"))
    min_qty = Decimal(str(trading_rules.get("min_qty", "0")))
    min_notional = Decimal(str(trading_rules.get("min_notional", "0")))
    requested_notional = Decimal(
        str(preview.get("requested_notional_usdt", f"{(quantity * price):f}"))
    )
    minimums = preview.get("exchange_minimums") if isinstance(preview, dict) else None
    minimum_qty_text = ""
    minimum_notional_text = ""
    if isinstance(minimums, dict):
        minimum_qty_text = str(minimums.get("minimum_executable_qty", ""))
        minimum_notional_text = str(minimums.get("minimum_executable_notional_usdt", ""))

    if min_qty > 0 and quantity < min_qty:
        return (
            f"Requested notional {requested_notional:f} is below Binance minimum executable "
            f"notional {minimum_notional_text or f'{(min_qty * price):f}'} USDT for "
            f"{preview['symbol']} at current price {price:f}; Binance LOT_SIZE minQty is "
            f"{minimum_qty_text or f'{min_qty:f}'}."
        )
    if min_notional > 0 and quantity * price < min_notional:
        return (
            f"Requested notional {requested_notional:f} is below Binance minimum executable "
            f"notional {minimum_notional_text or f'{min_notional:f}'} USDT for "
            f"{preview['symbol']} (MIN_NOTIONAL {min_notional:f}, minQty "
            f"{minimum_qty_text or f'{min_qty:f}'})."
        )
    return None


def _decimal_increment(value_text: str, *, minimum: str) -> Decimal:
    value = Decimal(str(value_text))
    floor = Decimal(str(minimum))
    return value if value > 0 else floor


def _floor_decimal_to_increment(value: Decimal, increment: Decimal) -> Decimal:
    if increment <= 0:
        return value
    steps = (value / increment).to_integral_value(rounding=ROUND_DOWN)
    return steps * increment


def _ceil_decimal_to_increment(value: Decimal, increment: Decimal) -> Decimal:
    if increment <= 0:
        return value
    steps = (value / increment).to_integral_value(rounding=ROUND_UP)
    return steps * increment


def _format_decimal_value(
    value: Decimal,
    increment: Decimal,
    fallback_decimals: int,
    *,
    precision_limit: int | None = None,
) -> str:
    decimals = _decimal_places(str(increment)) if increment > 0 else fallback_decimals
    if precision_limit is not None and precision_limit >= 0:
        decimals = min(decimals, precision_limit)
    quant = Decimal("1").scaleb(-decimals)
    return format(value.quantize(quant, rounding=ROUND_DOWN), "f")


def _format_signed_decimal_value(
    value: Decimal,
    increment: Decimal,
    fallback_decimals: int,
    *,
    precision_limit: int | None = None,
) -> str:
    sign = "+" if value > 0 else "-" if value < 0 else ""
    return f"{sign}{_format_decimal_value(abs(value), increment, fallback_decimals, precision_limit=precision_limit)}"


def _rule_precision(trading_rules: Dict[str, str], key: str) -> int | None:
    try:
        value = int(str(trading_rules.get(key, "")).strip())
    except (TypeError, ValueError):
        return None
    return value if value >= 0 else None


def _format_rule_aligned_decimal(
    value: Decimal,
    *,
    increment_text: str,
    minimum: str,
    fallback_decimals: int,
    precision_limit: int | None = None,
    round_up: bool = False,
) -> str:
    increment = _decimal_increment(increment_text, minimum=minimum)
    adjusted = (
        _ceil_decimal_to_increment(value, increment)
        if round_up
        else _floor_decimal_to_increment(value, increment)
    )
    return _format_decimal_value(
        adjusted,
        increment,
        fallback_decimals,
        precision_limit=precision_limit,
    )


def _safe_live_test_notional_usdt(
    requested_notional: float,
    trading_rules: Dict[str, str],
    reference_price: Decimal,
) -> Decimal:
    min_notional = _decimal_increment(trading_rules.get("min_notional", "0"), minimum="0")
    min_qty = _decimal_increment(trading_rules.get("min_qty", "0"), minimum="0")
    minimum_safe_notional = max(min_notional * Decimal("1.05"), min_qty * reference_price)
    requested = Decimal(str(max(requested_notional, 0.0)))
    capped = min(requested if requested > 0 else SAFE_LIVE_ORDER_MAX_NOTIONAL_USDT, SAFE_LIVE_ORDER_MAX_NOTIONAL_USDT)
    return max(capped, minimum_safe_notional)


def _required_initial_margin_usdt(
    *,
    estimated_execution_notional: Decimal,
    leverage: int,
) -> Decimal:
    normalized_leverage = max(int(leverage or 1), 1)
    return (estimated_execution_notional / Decimal(str(normalized_leverage))).quantize(
        Decimal("0.01")
    )


def _coerce_decimal(value: Any) -> Decimal:
    try:
        text = str(value or "").strip()
    except Exception:
        return Decimal("0")
    if not text:
        return Decimal("0")
    try:
        return Decimal(text)
    except Exception:
        return Decimal("0")


def _build_execution_summary(
    *,
    preview: Dict[str, Any],
    execution_payload: Dict[str, Any],
) -> Dict[str, str]:
    requested_notional = _coerce_decimal(preview.get("requested_notional_usdt"))
    actual_notional = _coerce_decimal(
        execution_payload.get("cumQuote")
        or execution_payload.get("cumQuoteQty")
        or execution_payload.get("quoteQty")
    )
    executed_qty = _coerce_decimal(
        execution_payload.get("executedQty") or execution_payload.get("cumQty")
    )
    average_fill_price = _coerce_decimal(execution_payload.get("avgPrice"))
    if actual_notional <= 0 and executed_qty > 0 and average_fill_price > 0:
        actual_notional = executed_qty * average_fill_price
    if actual_notional <= 0 and executed_qty > 0:
        market_reference = preview.get("market_reference") if isinstance(preview, dict) else {}
        if not isinstance(market_reference, dict):
            market_reference = {}
        reference_price = _coerce_decimal(
            market_reference.get("execution_reference_price")
            or market_reference.get("ask_price")
            or market_reference.get("bid_price")
            or preview.get("price")
        )
        if reference_price > 0:
            actual_notional = executed_qty * reference_price

    if requested_notional <= 0 and actual_notional <= 0:
        return {}

    requested_display = requested_notional.quantize(Decimal("0.01"), rounding=ROUND_DOWN)
    actual_display = actual_notional.quantize(Decimal("0.01"), rounding=ROUND_DOWN)
    summary: Dict[str, str] = {}
    if requested_display > 0:
        summary["requested_notional_usdt"] = _format_decimal_value(
            requested_display,
            Decimal("0.01"),
            2,
        )
    if actual_display > 0:
        summary["actual_execution_notional_usdt"] = _format_decimal_value(
            actual_display,
            Decimal("0.01"),
            2,
        )
    if requested_display > 0 and actual_display > 0:
        deviation = actual_display - requested_display
        deviation_pct = (deviation / requested_display) * Decimal("100")
        summary["execution_notional_delta_usdt"] = _format_signed_decimal_value(
            deviation,
            Decimal("0.01"),
            2,
        )
        summary["execution_notional_delta_pct"] = _format_signed_decimal_value(
            deviation_pct,
            Decimal("0.01"),
            2,
        )
    return summary


def _available_balance_usdt(api_key: str, secret_key: str) -> Decimal:
    account_payload = _signed_json(
        "/fapi/v3/account",
        api_key=api_key,
        secret_key=secret_key,
    )
    return Decimal(str(round(_safe_float(account_payload.get("availableBalance")), 2)))


def _preview_exchange_minimums(
    *,
    price: Decimal,
    trading_rules: Dict[str, str],
    fallback_price_decimals: int,
    fallback_quantity_decimals: int,
) -> Dict[str, str]:
    step_size = _decimal_increment(trading_rules.get("step_size", "0"), minimum="0")
    min_qty = _decimal_increment(trading_rules.get("min_qty", "0"), minimum="0")
    min_notional = _decimal_increment(trading_rules.get("min_notional", "0"), minimum="0")
    price_increment = _decimal_increment(trading_rules.get("tick_size", "0"), minimum="0")
    quantity_increment = (
        step_size if step_size > 0 else min_qty if min_qty > 0 else Decimal("0.00000001")
    )

    minimum_qty = max(min_qty, quantity_increment)
    if price > 0 and min_notional > 0 and minimum_qty * price < min_notional:
        minimum_qty = _ceil_decimal_to_increment(min_notional / price, quantity_increment)
        minimum_qty = max(minimum_qty, min_qty)
    minimum_notional = minimum_qty * price

    return {
        "minimum_executable_qty": _format_decimal_value(
            minimum_qty,
            quantity_increment,
            fallback_quantity_decimals,
            precision_limit=_rule_precision(trading_rules, "quantity_precision"),
        ),
        "minimum_executable_notional_usdt": _format_decimal_value(
            minimum_notional,
            Decimal("0.01"),
            2,
        ),
        "min_qty": _format_decimal_value(
            min_qty,
            quantity_increment,
            fallback_quantity_decimals,
            precision_limit=_rule_precision(trading_rules, "quantity_precision"),
        ),
        "min_notional": _format_decimal_value(min_notional, Decimal("0.01"), 2),
        "reference_price": _format_decimal_value(
            price,
            price_increment,
            fallback_price_decimals,
            precision_limit=_rule_precision(trading_rules, "price_precision"),
        ),
    }


def _safe_live_limit_price(
    intent_side: str,
    requested_price: float,
    book_ticker_payload: Dict[str, Any],
    trading_rules: Dict[str, str],
) -> Decimal:
    tick_size = _decimal_increment(trading_rules.get("tick_size", "0"), minimum="0.01")
    min_price = _decimal_increment(trading_rules.get("min_price", "0"), minimum="0.01")
    max_price = _decimal_increment(trading_rules.get("max_price", "0"), minimum="99999999")
    input_price = Decimal(str(requested_price))
    bid_price = Decimal(str(book_ticker_payload.get("bidPrice", 0) or 0))
    ask_price = Decimal(str(book_ticker_payload.get("askPrice", 0) or 0))

    candidates = [input_price]
    if str(intent_side).upper() == "LONG":
        if bid_price > 0:
            candidates.append(bid_price - (tick_size * 2))
        if ask_price > 0:
            candidates.append(ask_price - (tick_size * 3))
        positive_candidates = [candidate for candidate in candidates if candidate > 0]
        safe_price = min(positive_candidates) if positive_candidates else max(input_price, min_price)
        safe_price = max(safe_price, min_price)
        return _floor_decimal_to_increment(safe_price, tick_size)

    if ask_price > 0:
        candidates.append(ask_price + (tick_size * 2))
    if bid_price > 0:
        candidates.append(bid_price + (tick_size * 3))
    positive_candidates = [candidate for candidate in candidates if candidate > 0]
    safe_price = max(positive_candidates) if positive_candidates else max(input_price, min_price)
    safe_price = min(max(safe_price, min_price), max_price)
    return _ceil_decimal_to_increment(safe_price, tick_size)


def _safe_live_limit_quantity(
    target_notional_usdt: Decimal,
    price: Decimal,
    trading_rules: Dict[str, str],
) -> Decimal:
    step_size = _decimal_increment(trading_rules.get("step_size", "0"), minimum="0.001")
    min_qty = _decimal_increment(trading_rules.get("min_qty", "0"), minimum="0.001")
    min_notional = _decimal_increment(trading_rules.get("min_notional", "0"), minimum="0")
    safe_price = max(price, Decimal("0.00000001"))
    target_qty = target_notional_usdt / safe_price

    def normalized(candidate: Decimal) -> Decimal:
        next_qty = max(candidate, min_qty)
        if min_notional > 0 and next_qty * safe_price < min_notional:
            next_qty = _ceil_decimal_to_increment(min_notional / safe_price, step_size)
            next_qty = max(next_qty, min_qty)
        return next_qty

    floor_qty = normalized(_floor_decimal_to_increment(target_qty, step_size))
    ceil_qty = normalized(_ceil_decimal_to_increment(target_qty, step_size))

    floor_gap = abs((floor_qty * safe_price) - target_notional_usdt)
    ceil_gap = abs((ceil_qty * safe_price) - target_notional_usdt)
    if ceil_gap < floor_gap:
        return ceil_qty
    return floor_qty


def _live_market_reference_price(
    intent_side: str,
    requested_price: float,
    book_ticker_payload: Dict[str, Any],
) -> Decimal:
    bid_price = Decimal(str(book_ticker_payload.get("bidPrice", 0) or 0))
    ask_price = Decimal(str(book_ticker_payload.get("askPrice", 0) or 0))
    input_price = Decimal(str(requested_price))
    if str(intent_side).upper() == "LONG":
        return ask_price if ask_price > 0 else bid_price if bid_price > 0 else input_price
    return bid_price if bid_price > 0 else ask_price if ask_price > 0 else input_price


def build_demo_order_preview(trade_payload: Dict[str, Any]) -> Dict[str, Any]:
    symbol = str(trade_payload["symbol"]).upper()
    intent_side, order_side = _normalize_order_intent(trade_payload["side"])
    price = float(trade_payload["entry_price"])
    position_notional = float(trade_payload["position_notional_usdt"])
    if price <= 0:
        raise ValueError("trade.entry_price must be greater than zero for demo order test.")
    if position_notional <= 0:
        raise ValueError(
            "trade.position_notional_usdt must be greater than zero for demo order test."
        )
    quantity = position_notional / price
    if quantity <= 0:
        raise ValueError("Estimated order quantity must be greater than zero.")

    trading_rules: Dict[str, str] | None = None
    quantity_text = _format_decimal(quantity, _quantity_precision(price))
    price_text = _format_decimal(price, _price_precision(price))
    try:
        trading_rules = _get_symbol_trading_rules(symbol)
        quantity_text = _format_rule_aligned_decimal(
            Decimal(str(quantity)),
            increment_text=trading_rules.get("step_size", "0"),
            minimum="0",
            fallback_decimals=_quantity_precision(price),
            precision_limit=_rule_precision(trading_rules, "quantity_precision"),
        )
        price_text = _format_rule_aligned_decimal(
            Decimal(str(price)),
            increment_text=trading_rules.get("tick_size", "0"),
            minimum="0",
            fallback_decimals=_price_precision(price),
            precision_limit=_rule_precision(trading_rules, "price_precision"),
        )
    except Exception:
        trading_rules = None

    preview = {
        "symbol": symbol,
        "intent_side": intent_side,
        "side": order_side,
        "order_side": order_side,
        "type": "LIMIT",
        "timeInForce": "GTC",
        "quantity": quantity_text,
        "price": price_text,
        "requested_notional_usdt": _format_decimal_value(Decimal(str(position_notional)), Decimal("0.01"), 2),
        "recvWindow": str(DEFAULT_RECV_WINDOW_MS),
        "execution_mode": _exchange_source_key(),
        "validation_scope": "full",
    }
    if trading_rules:
        preview["exchange_rules"] = trading_rules
        preview["exchange_minimums"] = _preview_exchange_minimums(
            price=Decimal(price_text),
            trading_rules=trading_rules,
            fallback_price_decimals=_price_precision(price),
            fallback_quantity_decimals=_quantity_precision(price),
        )
    return preview


def build_live_order_preview(trade_payload: Dict[str, Any]) -> Dict[str, Any]:
    symbol = str(trade_payload["symbol"]).upper()
    intent_side, order_side = _normalize_order_intent(trade_payload["side"])
    requested_price = float(trade_payload["entry_price"])
    requested_notional = float(trade_payload["position_notional_usdt"])
    requested_leverage = _requested_exchange_leverage(trade_payload)
    requested_margin_type = _normalize_margin_type(trade_payload.get("margin_mode"))
    if requested_price <= 0:
        raise ValueError("trade.entry_price must be greater than zero for live execution.")
    if requested_notional <= 0:
        raise ValueError("trade.position_notional_usdt must be greater than zero for live execution.")

    trading_rules = _get_symbol_trading_rules(symbol)
    book_ticker_payload = _http_json("/fapi/v1/ticker/bookTicker", params={"symbol": symbol})
    live_price = _safe_live_limit_price(
        intent_side, requested_price, book_ticker_payload, trading_rules
    )
    target_notional_usdt = _safe_live_test_notional_usdt(
        requested_notional,
        trading_rules,
        live_price,
    )
    quantity = _safe_live_limit_quantity(target_notional_usdt, live_price, trading_rules)
    step_size = _decimal_increment(trading_rules.get("step_size", "0"), minimum="0.001")
    tick_size = _decimal_increment(trading_rules.get("tick_size", "0"), minimum="0.01")

    preview = {
        "symbol": symbol,
        "intent_side": intent_side,
        "side": order_side,
        "order_side": order_side,
        "type": "LIMIT",
        "requested_margin_type": requested_margin_type,
        "requested_leverage": str(requested_leverage),
        "timeInForce": "GTX",
        "price": _format_decimal_value(
            live_price,
            tick_size,
            _price_precision(requested_price),
            precision_limit=_rule_precision(trading_rules, "price_precision"),
        ),
        "quantity": _format_decimal_value(
            quantity,
            step_size,
            _quantity_precision(requested_price),
            precision_limit=_rule_precision(trading_rules, "quantity_precision"),
        ),
        "requested_notional_usdt": _format_decimal_value(
            Decimal(str(requested_notional)),
            Decimal("0.01"),
            2,
        ),
        "recvWindow": str(DEFAULT_RECV_WINDOW_MS),
        "execution_mode": _exchange_source_key(),
        "validation_scope": "live_limit_maker",
        "execution_policy": "place_and_cancel",
        "test_notional_usdt": _format_decimal_value(target_notional_usdt, Decimal("0.01"), 2),
        "exchange_rules": trading_rules,
        "exchange_minimums": _preview_exchange_minimums(
            price=live_price,
            trading_rules=trading_rules,
            fallback_price_decimals=_price_precision(requested_price),
            fallback_quantity_decimals=_quantity_precision(requested_price),
        ),
        "market_reference": {
            "bid_price": str(book_ticker_payload.get("bidPrice", "")),
            "ask_price": str(book_ticker_payload.get("askPrice", "")),
        },
    }
    return preview


def build_live_open_order_preview(trade_payload: Dict[str, Any]) -> Dict[str, Any]:
    symbol = str(trade_payload["symbol"]).upper()
    intent_side, order_side = _normalize_order_intent(trade_payload["side"])
    requested_price = float(trade_payload["entry_price"])
    requested_notional = float(trade_payload["position_notional_usdt"])
    requested_leverage = _requested_exchange_leverage(trade_payload)
    requested_margin_type = _normalize_margin_type(trade_payload.get("margin_mode"))
    if requested_price <= 0:
        raise ValueError("trade.entry_price must be greater than zero for live execution.")
    if requested_notional <= 0:
        raise ValueError("trade.position_notional_usdt must be greater than zero for live execution.")

    trading_rules = _get_symbol_trading_rules(symbol)
    book_ticker_payload = _http_json("/fapi/v1/ticker/bookTicker", params={"symbol": symbol})
    reference_price = _live_market_reference_price(
        intent_side,
        requested_price,
        book_ticker_payload,
    )
    quantity = _safe_live_limit_quantity(
        Decimal(str(requested_notional)),
        reference_price,
        trading_rules,
    )
    step_size = _decimal_increment(trading_rules.get("step_size", "0"), minimum="0.001")
    tick_size = _decimal_increment(trading_rules.get("tick_size", "0"), minimum="0.01")
    estimated_execution_notional = quantity * reference_price
    required_initial_margin = _required_initial_margin_usdt(
        estimated_execution_notional=estimated_execution_notional,
        leverage=requested_leverage,
    )

    preview = {
        "symbol": symbol,
        "intent_side": intent_side,
        "side": order_side,
        "order_side": order_side,
        "type": "MARKET",
        "requested_margin_type": requested_margin_type,
        "requested_leverage": str(requested_leverage),
        "requested_entry_price": _format_decimal_value(
            Decimal(str(requested_price)),
            tick_size,
            _price_precision(requested_price),
            precision_limit=_rule_precision(trading_rules, "price_precision"),
        ),
        "quantity": _format_decimal_value(
            quantity,
            step_size,
            _quantity_precision(requested_price),
            precision_limit=_rule_precision(trading_rules, "quantity_precision"),
        ),
        "requested_notional_usdt": _format_decimal_value(
            Decimal(str(requested_notional)),
            Decimal("0.01"),
            2,
        ),
        "estimated_execution_notional_usdt": _format_decimal_value(
            estimated_execution_notional,
            Decimal("0.01"),
            2,
        ),
        "required_initial_margin_usdt": _format_decimal_value(
            required_initial_margin,
            Decimal("0.01"),
            2,
        ),
        "recvWindow": str(DEFAULT_RECV_WINDOW_MS),
        "execution_mode": _exchange_source_key(),
        "validation_scope": "live_market_execution",
        "execution_policy": "place_and_keep",
        "exchange_rules": trading_rules,
        "exchange_minimums": _preview_exchange_minimums(
            price=reference_price,
            trading_rules=trading_rules,
            fallback_price_decimals=_price_precision(requested_price),
            fallback_quantity_decimals=_quantity_precision(requested_price),
        ),
        "market_reference": {
            "bid_price": str(book_ticker_payload.get("bidPrice", "")),
            "ask_price": str(book_ticker_payload.get("askPrice", "")),
            "execution_reference_price": _format_decimal_value(
                reference_price,
                tick_size,
                _price_precision(requested_price),
                precision_limit=_rule_precision(trading_rules, "price_precision"),
            ),
        },
        "newOrderRespType": "RESULT",
    }
    return preview


def get_demo_credentials_status() -> Dict[str, Any]:
    api_name, secret_name = _credential_env_names()
    api_key, secret = _configured_credentials()
    return {
        "configured": bool(api_key and secret),
        "has_api_key": bool(api_key),
        "has_secret_key": bool(secret),
        "api_key_env": api_name,
        "secret_key_env": secret_name,
    }


def _exchange_order_params(preview: Dict[str, Any]) -> Dict[str, Any]:
    params = {
        "symbol": str(preview["symbol"]),
        "side": str(preview["order_side"]),
        "type": str(preview["type"]),
        "recvWindow": str(preview["recvWindow"]),
    }
    if preview.get("quantity") is not None:
        params["quantity"] = str(preview["quantity"])
    if preview.get("price") is not None:
        params["price"] = str(preview["price"])
    if preview.get("timeInForce"):
        params["timeInForce"] = str(preview["timeInForce"])
    if preview.get("positionSide"):
        params["positionSide"] = str(preview["positionSide"])
    if preview.get("newOrderRespType"):
        params["newOrderRespType"] = str(preview["newOrderRespType"])
    return params


def _close_order_side(intent_side: str) -> str:
    return "SELL" if str(intent_side).upper() == "LONG" else "BUY"


def _requested_protective_targets(trade_payload: Dict[str, Any]) -> Dict[str, Any]:
    intent_side, _ = _normalize_order_intent(trade_payload.get("side"))
    entry_price = _safe_float(trade_payload.get("entry_price"))
    if entry_price <= 0:
        raise ValueError("trade.entry_price must be greater than zero for live execution.")

    stop_loss_raw = trade_payload.get("stop_loss_price")
    take_profit_raw = trade_payload.get("take_profit_price")
    if stop_loss_raw is None or take_profit_raw is None:
        raise ValueError(
            "Live open position requires both trade.stop_loss_price and trade.take_profit_price."
        )

    stop_loss_price = _safe_float(stop_loss_raw)
    take_profit_price = _safe_float(take_profit_raw)
    if stop_loss_price <= 0 or take_profit_price <= 0:
        raise ValueError(
            "trade.stop_loss_price and trade.take_profit_price must be greater than zero for live execution."
        )

    if intent_side == "LONG":
        if stop_loss_price >= entry_price:
            raise ValueError("For LONG, trade.stop_loss_price must be below trade.entry_price.")
        if take_profit_price <= entry_price:
            raise ValueError("For LONG, trade.take_profit_price must be above trade.entry_price.")
    else:
        if stop_loss_price <= entry_price:
            raise ValueError("For SHORT, trade.stop_loss_price must be above trade.entry_price.")
        if take_profit_price >= entry_price:
            raise ValueError("For SHORT, trade.take_profit_price must be below trade.entry_price.")

    return {
        "intent_side": intent_side,
        "entry_price": entry_price,
        "stop_loss_price": stop_loss_price,
        "take_profit_price": take_profit_price,
    }


def _aligned_protection_trigger_price(
    *,
    target_price: float,
    entry_price: float,
    intent_side: str,
    role: str,
    trading_rules: Dict[str, str],
) -> str:
    round_up = False
    if intent_side == "LONG":
        round_up = role == "stop_loss"
    else:
        round_up = role == "take_profit"

    price_text = _format_rule_aligned_decimal(
        Decimal(str(target_price)),
        increment_text=trading_rules.get("tick_size", "0"),
        minimum=trading_rules.get("min_price", "0"),
        fallback_decimals=_price_precision(entry_price),
        precision_limit=_rule_precision(trading_rules, "price_precision"),
        round_up=round_up,
    )
    aligned_price = Decimal(price_text)
    entry_decimal = Decimal(str(entry_price))
    if role == "stop_loss":
        if intent_side == "LONG" and not aligned_price < entry_decimal:
            raise ValueError(
                "Aligned stop-loss trigger is too close to entry for Binance tick size."
            )
        if intent_side == "SHORT" and not aligned_price > entry_decimal:
            raise ValueError(
                "Aligned stop-loss trigger is too close to entry for Binance tick size."
            )
    else:
        if intent_side == "LONG" and not aligned_price > entry_decimal:
            raise ValueError(
                "Aligned take-profit trigger is too close to entry for Binance tick size."
            )
        if intent_side == "SHORT" and not aligned_price < entry_decimal:
            raise ValueError(
                "Aligned take-profit trigger is too close to entry for Binance tick size."
            )
    return price_text


def _build_futures_protection_orders(
    *,
    trade_payload: Dict[str, Any],
    preview: Dict[str, Any],
) -> Dict[str, Dict[str, Any]]:
    requested_targets = _requested_protective_targets(trade_payload)
    intent_side = str(preview.get("intent_side") or requested_targets["intent_side"]).upper()
    symbol = str(preview["symbol"]).upper()
    trading_rules = preview.get("exchange_rules")
    if not isinstance(trading_rules, dict):
        trading_rules = _get_symbol_trading_rules(symbol)

    close_side = _close_order_side(intent_side)
    base_params: Dict[str, Any] = {
        "algoType": "CONDITIONAL",
        "symbol": symbol,
        "side": close_side,
        "recvWindow": str(DEFAULT_RECV_WINDOW_MS),
        "closePosition": "true",
        "workingType": "CONTRACT_PRICE",
    }
    if preview.get("positionSide"):
        base_params["positionSide"] = str(preview["positionSide"])

    stop_price = _aligned_protection_trigger_price(
        target_price=float(requested_targets["stop_loss_price"]),
        entry_price=float(requested_targets["entry_price"]),
        intent_side=intent_side,
        role="stop_loss",
        trading_rules=trading_rules,
    )
    take_profit_price = _aligned_protection_trigger_price(
        target_price=float(requested_targets["take_profit_price"]),
        entry_price=float(requested_targets["entry_price"]),
        intent_side=intent_side,
        role="take_profit",
        trading_rules=trading_rules,
    )

    return {
        "stop_loss": {
            **base_params,
            "type": "STOP_MARKET",
            "triggerPrice": stop_price,
            "stopPrice": stop_price,
        },
        "take_profit": {
            **base_params,
            "type": "TAKE_PROFIT_MARKET",
            "triggerPrice": take_profit_price,
            "stopPrice": take_profit_price,
        },
    }


def _place_named_futures_order(
    *,
    api_key: str,
    secret_key: str,
    params: Dict[str, Any],
    client_order_id: str,
) -> Dict[str, Any]:
    request_params = dict(params)
    request_params["newClientOrderId"] = client_order_id
    return _signed_json(
        "/fapi/v1/order",
        api_key=api_key,
        secret_key=secret_key,
        params=request_params,
        method="POST",
    )


def _place_named_futures_algo_order(
    *,
    api_key: str,
    secret_key: str,
    params: Dict[str, Any],
    client_algo_id: str,
) -> Dict[str, Any]:
    request_params = dict(params)
    request_params["clientAlgoId"] = client_algo_id
    return _signed_json(
        "/fapi/v1/algoOrder",
        api_key=api_key,
        secret_key=secret_key,
        params=request_params,
        method="POST",
    )


def _validate_futures_order_params(
    *,
    api_key: str,
    secret_key: str,
    params: Dict[str, Any],
) -> None:
    _signed_json(
        "/fapi/v1/order/test",
        api_key=api_key,
        secret_key=secret_key,
        params=params,
        method="POST",
    )


def _emergency_close_market_order(
    *,
    api_key: str,
    secret_key: str,
    preview: Dict[str, Any],
    execution_payload: Dict[str, Any],
) -> Dict[str, Any]:
    quantity = str(
        execution_payload.get("executedQty")
        or execution_payload.get("origQty")
        or preview.get("quantity")
        or ""
    ).strip()
    if not quantity or Decimal(quantity) <= 0:
        raise RuntimeError("Could not derive executed quantity for emergency close.")

    params: Dict[str, Any] = {
        "symbol": str(preview["symbol"]),
        "side": _close_order_side(str(preview["intent_side"])),
        "type": "MARKET",
        "quantity": quantity,
        "recvWindow": str(DEFAULT_RECV_WINDOW_MS),
        "newOrderRespType": "RESULT",
    }
    if preview.get("positionSide"):
        params["positionSide"] = str(preview["positionSide"])
    else:
        params["reduceOnly"] = "true"
    return _place_named_futures_order(
        api_key=api_key,
        secret_key=secret_key,
        params=params,
        client_order_id=f"cpgfailclose{int(time.time() * 1000)}",
    )


def _requested_exchange_leverage(trade_payload: Dict[str, Any]) -> int:
    leverage = _safe_float(trade_payload.get("leverage"))
    if leverage <= 0:
        raise ValueError("trade.leverage must be greater than zero for live execution.")
    rounded = round(leverage)
    if abs(leverage - rounded) > 1e-9:
        raise ValueError(
            "Binance USD-M Futures live execution leverage must be a whole number between 1 and 125."
        )
    leverage_int = int(rounded)
    if leverage_int < 1 or leverage_int > 125:
        raise ValueError(
            "Binance USD-M Futures live execution leverage must be between 1 and 125."
        )
    return leverage_int


def _normalize_margin_type(value: Any) -> str:
    normalized = str(value or "CROSSED").strip().upper()
    aliases = {
        "CROSS": "CROSSED",
        "CROSSED": "CROSSED",
        "ISOLATED": "ISOLATED",
        "ISOLATE": "ISOLATED",
        "全仓": "CROSSED",
        "逐仓": "ISOLATED",
    }
    margin_type = aliases.get(normalized)
    if not margin_type:
        raise ValueError("trade.margin_mode must be CROSSED or ISOLATED.")
    return margin_type


def _sync_futures_initial_leverage(
    *,
    symbol: str,
    leverage: int,
    api_key: str,
    secret_key: str,
) -> Dict[str, Any]:
    return _signed_json(
        "/fapi/v1/leverage",
        api_key=api_key,
        secret_key=secret_key,
        params={"symbol": symbol, "leverage": str(leverage)},
        method="POST",
    )


def _current_futures_margin_type(
    *,
    symbol: str,
    api_key: str,
    secret_key: str,
) -> str | None:
    try:
        payload = _signed_json(
            "/fapi/v2/positionRisk",
            api_key=api_key,
            secret_key=secret_key,
            params={"symbol": symbol},
        )
    except Exception:
        return None

    rows = payload if isinstance(payload, list) else []
    normalized_symbol = str(symbol).upper()
    for row in rows:
        if str(row.get("symbol", "")).upper() != normalized_symbol:
            continue
        raw_margin_type = str(row.get("marginType", "")).strip()
        if not raw_margin_type:
            continue
        try:
            return _normalize_margin_type(raw_margin_type)
        except ValueError:
            return raw_margin_type.upper()
    return None


def _sync_futures_margin_type(
    *,
    symbol: str,
    margin_type: str,
    api_key: str,
    secret_key: str,
) -> Dict[str, Any]:
    current_margin_type = _current_futures_margin_type(
        symbol=symbol,
        api_key=api_key,
        secret_key=secret_key,
    )
    if current_margin_type == margin_type:
        return {
            "symbol": symbol,
            "marginType": margin_type,
            "status": "matched",
            "message": "Margin type already matched the requested mode.",
        }

    try:
        payload = _signed_json(
            "/fapi/v1/marginType",
            api_key=api_key,
            secret_key=secret_key,
            params={"symbol": symbol, "marginType": margin_type},
            method="POST",
        )
        if isinstance(payload, dict):
            payload.setdefault("symbol", symbol)
            payload.setdefault("marginType", margin_type)
        return payload if isinstance(payload, dict) else {"symbol": symbol, "marginType": margin_type}
    except RuntimeError as exc:
        message = str(exc)
        if "No need to change margin type" in message:
            return {
                "symbol": symbol,
                "marginType": margin_type,
                "status": "no_change",
                "message": "Margin type already matched the requested mode.",
            }
        if "there exists open orders" in message.lower():
            current_margin_type = _current_futures_margin_type(
                symbol=symbol,
                api_key=api_key,
                secret_key=secret_key,
            )
            if current_margin_type == margin_type:
                return {
                    "symbol": symbol,
                    "marginType": margin_type,
                    "status": "matched_with_open_orders",
                    "message": "Margin type already matched the requested mode while open orders existed.",
                }
        raise


def _signed_query(params: Dict[str, Any], secret_key: str) -> str:
    payload = urlencode(params)
    signature = hmac.new(
        secret_key.encode("utf-8"),
        payload.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()
    return f"{payload}&signature={signature}"


def _signed_json(
    path: str,
    *,
    api_key: str,
    secret_key: str,
    params: Dict[str, Any] | None = None,
    method: str = "GET",
    timeout: float = DEFAULT_TIMEOUT_SECONDS,
) -> Any:
    signed_params = dict(params or {})
    signed_params.setdefault("recvWindow", DEFAULT_RECV_WINDOW_MS)
    signed_params["timestamp"] = int(time.time() * 1000)
    query = _signed_query(signed_params, secret_key)
    url = f"{_api_base()}{path}?{query}"
    request = Request(url, method=method, headers={"X-MBX-APIKEY": api_key})
    return _load_json_response(request, timeout=timeout)


def _base_asset_from_symbol(symbol: str) -> str:
    normalized = str(symbol).upper()
    if normalized.endswith("USDT"):
        return normalized[:-4]
    return normalized


def _fetch_price_map(symbols: List[str]) -> Dict[str, float]:
    price_map: Dict[str, float] = {}
    for symbol in symbols:
        normalized = str(symbol).upper()
        try:
            payload = _http_json("/fapi/v1/ticker/price", params={"symbol": normalized})
            price_map[normalized] = float(payload.get("price", 0.0) or 0.0)
        except Exception:
            continue
    return price_map


def _safe_float(value: Any) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def _estimate_balances(account_payload: Dict[str, Any], price_map: Dict[str, float]) -> List[Dict[str, Any]]:
    if account_payload.get("assets"):
        balances: List[Dict[str, Any]] = []
        for row in account_payload.get("assets", []):
            asset = str(row.get("asset", "")).upper()
            margin_balance = _safe_float(row.get("marginBalance"))
            available_balance = _safe_float(row.get("availableBalance"))
            open_order_margin = _safe_float(row.get("openOrderInitialMargin"))
            if margin_balance <= 0 and available_balance <= 0 and open_order_margin <= 0:
                continue
            balances.append(
                {
                    "asset": asset,
                    "free": round(available_balance, 8),
                    "locked": round(open_order_margin, 8),
                    "estimated_usdt": round(
                        margin_balance
                        if margin_balance > 0
                        else available_balance + open_order_margin,
                        2,
                    ),
                }
            )
        balances.sort(key=lambda item: item["estimated_usdt"], reverse=True)
        return balances

    balances: List[Dict[str, Any]] = []
    for row in account_payload.get("balances", []):
        asset = str(row.get("asset", "")).upper()
        free = _safe_float(row.get("free"))
        locked = _safe_float(row.get("locked"))
        total = free + locked
        if total <= 0:
            continue

        if asset == "USDT":
            estimated_usdt = total
        else:
            estimated_usdt = total * price_map.get(f"{asset}USDT", 0.0)
        balances.append(
            {
                "asset": asset,
                "free": round(free, 8),
                "locked": round(locked, 8),
                "estimated_usdt": round(estimated_usdt, 2),
            }
        )

    balances.sort(key=lambda item: item["estimated_usdt"], reverse=True)
    return balances


def _wallet_balance_usdt(account_payload: Dict[str, Any], balances: List[Dict[str, Any]]) -> float:
    total_wallet_balance = _safe_float(account_payload.get("totalWalletBalance"))
    if total_wallet_balance > 0:
        return round(total_wallet_balance, 2)

    for row in account_payload.get("assets", []):
        if str(row.get("asset", "")).upper() != "USDT":
            continue
        wallet_balance = _safe_float(row.get("walletBalance"))
        if wallet_balance > 0:
            return round(wallet_balance, 2)

    usdt_balance = next((item for item in balances if item.get("asset") == "USDT"), None)
    if usdt_balance:
        return round(_safe_float(usdt_balance.get("estimated_usdt")), 2)
    return 0.0


def _nonzero_quote_symbols(account_payload: Dict[str, Any]) -> List[str]:
    if account_payload.get("positions"):
        symbols = []
        for row in account_payload.get("positions", []):
            symbol = str(row.get("symbol", "")).upper()
            notional = abs(_safe_float(row.get("notional")))
            if notional <= 0 or not symbol:
                continue
            symbols.append(symbol)
        return sorted(set(symbols))
    symbols: List[str] = []
    for row in account_payload.get("balances", []):
        asset = str(row.get("asset", "")).upper()
        total = _safe_float(row.get("free")) + _safe_float(row.get("locked"))
        if total <= 0 or asset == "USDT":
            continue
        symbols.append(f"{asset}USDT")
    return sorted(set(symbols))


def _realized_trade_results(trades: List[Dict[str, Any]]) -> List[float]:
    if any("realizedPnl" in trade for trade in trades):
        results: List[float] = []
        for trade in sorted(trades, key=lambda item: int(item.get("time", 0))):
            realized_pnl = _safe_float(trade.get("realizedPnl"))
            commission = _safe_float(trade.get("commission"))
            net = realized_pnl + commission
            if abs(realized_pnl) <= 1e-12 and abs(net) <= 1e-12:
                continue
            results.append(net)
        return results

    inventory: List[List[float]] = []
    results: List[float] = []
    ordered_trades = sorted(trades, key=lambda item: int(item.get("time", 0)))

    for trade in ordered_trades:
        qty = _safe_float(trade.get("qty"))
        price = _safe_float(trade.get("price"))
        commission = _safe_float(trade.get("commission"))
        if qty <= 0 or price <= 0:
            continue

        if trade.get("isBuyer", False):
            inventory.append([qty, price])
            continue

        remaining = qty
        realized = 0.0
        while remaining > 1e-12 and inventory:
            lot_qty, lot_price = inventory[0]
            matched = min(remaining, lot_qty)
            realized += (price - lot_price) * matched
            lot_qty -= matched
            remaining -= matched
            if lot_qty <= 1e-12:
                inventory.pop(0)
            else:
                inventory[0][0] = lot_qty

        if qty > remaining:
            results.append(realized - commission)

    return results


def _normalize_futures_positions(position_risk_payload: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    positions: List[Dict[str, Any]] = []
    for row in position_risk_payload or []:
        quantity = _safe_float(row.get("positionAmt"))
        notional = _safe_float(row.get("notional"))
        if abs(quantity) <= 1e-12 and abs(notional) <= 1e-12:
            continue
        positions.append(
            {
                "symbol": str(row.get("symbol", "")).upper(),
                "position_side": str(row.get("positionSide", "BOTH")).upper(),
                "quantity": round(quantity, 8),
                "entry_price": round(_safe_float(row.get("entryPrice")), 6),
                "mark_price": round(_safe_float(row.get("markPrice")), 6),
                "notional_usdt": round(abs(notional), 2),
                "unrealized_pnl_usdt": round(_safe_float(row.get("unRealizedProfit")), 2),
                "liquidation_price": round(_safe_float(row.get("liquidationPrice")), 6),
                "initial_margin": round(_safe_float(row.get("initialMargin")), 2),
                "maint_margin": round(_safe_float(row.get("maintMargin")), 2),
            }
        )
    positions.sort(key=lambda item: item["notional_usdt"], reverse=True)
    return positions


def _normalize_futures_open_orders(open_orders_payload: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    orders: List[Dict[str, Any]] = []
    for row in open_orders_payload or []:
        symbol = str(row.get("symbol", "")).upper()
        if not symbol:
            continue
        orders.append(
            {
                "symbol": symbol,
                "side": str(row.get("side", "")).upper(),
                "position_side": str(row.get("positionSide", "BOTH")).upper(),
                "type": str(row.get("type", "")).upper(),
                "status": str(row.get("status", "")).upper(),
                "price": round(_safe_float(row.get("price")), 6),
                "stop_price": round(_safe_float(row.get("stopPrice")), 6),
                "orig_qty": round(_safe_float(row.get("origQty")), 8),
                "executed_qty": round(_safe_float(row.get("executedQty")), 8),
                "reduce_only": bool(row.get("reduceOnly", False)),
                "close_position": bool(row.get("closePosition", False)),
                "working_type": str(row.get("workingType", "")).upper(),
                "time": int(row.get("time", 0) or 0),
            }
        )
    orders.sort(key=lambda item: item["time"], reverse=True)
    return orders


def _normalize_futures_algo_orders(algo_orders_payload: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    orders: List[Dict[str, Any]] = []
    for row in algo_orders_payload or []:
        symbol = str(row.get("symbol", "")).upper()
        if not symbol:
            continue
        orders.append(
            {
                "symbol": symbol,
                "side": str(row.get("side", "")).upper(),
                "position_side": str(row.get("positionSide", "BOTH")).upper(),
                "type": str(
                    row.get("orderType")
                    or row.get("type")
                    or row.get("algoType")
                    or ""
                ).upper(),
                "status": str(row.get("status", row.get("algoStatus", ""))).upper(),
                "price": round(_safe_float(row.get("price")), 6),
                "stop_price": round(
                    _safe_float(row.get("triggerPrice") or row.get("stopPrice")), 6
                ),
                "orig_qty": round(
                    _safe_float(row.get("quantity") or row.get("origQty") or row.get("qty")), 8
                ),
                "executed_qty": round(_safe_float(row.get("executedQty")), 8),
                "reduce_only": bool(row.get("reduceOnly", False)),
                "close_position": bool(row.get("closePosition", False)),
                "working_type": str(
                    row.get("workingType") or row.get("triggerType") or row.get("priceProtect") or ""
                ).upper(),
                "algo_id": str(row.get("algoId", "")).strip(),
                "time": int(
                    row.get("time", row.get("createTime", row.get("createdTime", 0))) or 0
                ),
            }
        )
    orders.sort(key=lambda item: item["time"], reverse=True)
    return orders


def _closest_liquidation_gap_pct(positions: List[Dict[str, Any]]) -> float | None:
    gaps: List[float] = []
    for position in positions:
        quantity = float(position.get("quantity", 0.0))
        mark_price = float(position.get("mark_price", 0.0))
        liquidation_price = float(position.get("liquidation_price", 0.0))
        if abs(quantity) <= 1e-12 or mark_price <= 0 or liquidation_price <= 0:
            continue
        if quantity > 0:
            gap = ((mark_price - liquidation_price) / mark_price) * 100.0
        else:
            gap = ((liquidation_price - mark_price) / mark_price) * 100.0
        if gap >= 0:
            gaps.append(gap)
    if not gaps:
        return None
    return round(min(gaps), 2)


def _aggregate_behavior(
    trades_by_symbol: Dict[str, List[Dict[str, Any]]],
    equity_usdt: float,
) -> Dict[str, Any]:
    all_trades: List[Dict[str, Any]] = []
    realized_results: List[Dict[str, Any]] = []

    for trades in trades_by_symbol.values():
        all_trades.extend(trades)
        if any("realizedPnl" in trade for trade in trades):
            for trade in sorted(trades, key=lambda item: int(item.get("time", 0))):
                realized_pnl = _safe_float(trade.get("realizedPnl"))
                commission = _safe_float(trade.get("commission"))
                net = realized_pnl + commission
                realized_results.append({"time": int(trade.get("time", 0)), "pnl": net, "realized": realized_pnl})
            continue

        symbol_results = _realized_trade_results(trades)
        sells = [
            trade
            for trade in sorted(trades, key=lambda item: int(item.get("time", 0)))
            if not trade.get("isBuyer", False)
        ]
        for idx, pnl in enumerate(symbol_results):
            trade_time = int(sells[idx].get("time", 0)) if idx < len(sells) else 0
            realized_results.append({"time": trade_time, "pnl": pnl, "realized": pnl})

    realized_results.sort(key=lambda item: item["time"])
    consecutive_losses = 0
    for item in reversed(realized_results):
        if abs(float(item.get("realized", 0.0))) <= 1e-12:
            continue
        if item["pnl"] < 0:
            consecutive_losses += 1
        else:
            break

    realized_pnl_usdt = sum(item["pnl"] for item in realized_results)
    day_pnl_pct = (realized_pnl_usdt / max(equity_usdt, 1e-6)) * 100.0
    return {
        "trades_last_24h": len(all_trades),
        "consecutive_losses": consecutive_losses,
        "day_pnl_pct": round(day_pnl_pct, 2),
        "realized_pnl_24h_usdt": round(realized_pnl_usdt, 2),
    }


def _behavior_status(behavior: Dict[str, Any]) -> str:
    trades = int(behavior.get("trades_last_24h", 0))
    losses = int(behavior.get("consecutive_losses", 0))
    pnl = float(behavior.get("day_pnl_pct", 0.0))
    if losses >= 3 or pnl <= -5 or trades >= 18:
        return "high_alert"
    if losses >= 1 or pnl < 0 or trades >= 8:
        return "elevated"
    return "stable"


def _build_account_briefing(
    *,
    live: bool,
    profile_name: str,
    estimated_equity_usdt: float,
    available_usdt: float,
    behavior: Dict[str, Any],
    suggested_position_cap_usdt: float,
    risk_budget_usdt: float,
    active_positions_count: int = 0,
    closest_liq_gap_pct: float | None = None,
) -> List[str]:
    source_text = (
        f"Connected to {_exchange_label()} account context."
        if live
        else "Using local fallback account context."
    )
    return [
        source_text,
        (
            f"Estimated equity {estimated_equity_usdt:.2f} USDT, available USDT "
            f"{available_usdt:.2f}."
        ),
        (
            f"Recent activity: {int(behavior.get('trades_last_24h', 0))} trades in 24h, "
            f"realized PnL {float(behavior.get('day_pnl_pct', 0.0)):.2f}%, trailing loss "
            f"streak {int(behavior.get('consecutive_losses', 0))}."
        ),
        (
            f"Active futures positions: {active_positions_count}."
            + (
                f" Closest estimated liquidation gap is {closest_liq_gap_pct:.2f}%."
                if closest_liq_gap_pct is not None
                else ""
            )
        ),
        (
            f"Under {profile_name} profile, suggested max notional is "
            f"{suggested_position_cap_usdt:.2f} USDT and per-trade risk budget is "
            f"{risk_budget_usdt:.2f} USDT."
        ),
    ]


def build_account_snapshot(
    *,
    symbol: str,
    profile_name: str | None,
    account_payload: Dict[str, Any],
    open_orders_payload: List[Dict[str, Any]],
    algo_open_orders_payload: List[Dict[str, Any]],
    trades_by_symbol: Dict[str, List[Dict[str, Any]]],
    position_risk_payload: List[Dict[str, Any]] | None = None,
    price_map: Dict[str, float] | None = None,
    live: bool,
    warning: str | None = None,
) -> Dict[str, Any]:
    profile = str(profile_name or "balanced").lower()
    normalized_symbol = str(symbol).upper()
    balances = _estimate_balances(account_payload, price_map or {})
    positions = _normalize_futures_positions(position_risk_payload or [])
    open_orders = _normalize_futures_open_orders(open_orders_payload or [])
    algo_open_orders = _normalize_futures_algo_orders(algo_open_orders_payload or [])
    estimated_equity_usdt = round(
        _safe_float(account_payload.get("totalMarginBalance"))
        or sum(item["estimated_usdt"] for item in balances),
        2,
    )
    wallet_balance_usdt = _wallet_balance_usdt(account_payload, balances)
    available_usdt = round(
        _safe_float(account_payload.get("availableBalance"))
        or next((item["free"] for item in balances if item["asset"] == "USDT"), 0.0),
        2,
    )
    locked_usdt = round(
        _safe_float(account_payload.get("totalOpenOrderInitialMargin"))
        or next((item["locked"] for item in balances if item["asset"] == "USDT"), 0.0),
        2,
    )
    behavior = _aggregate_behavior(trades_by_symbol, estimated_equity_usdt)
    suggested_position_cap_usdt = round(
        estimated_equity_usdt * _position_vs_equity_limit(profile), 2
    )
    risk_budget_usdt = round(estimated_equity_usdt * _risk_per_trade_limit(profile) / 100.0, 2)
    tracked_symbols = sorted(set(trades_by_symbol.keys()) | {item["symbol"] for item in positions if item.get("symbol")})
    closest_liq_gap_pct = _closest_liquidation_gap_pct(positions)

    return {
        "symbol": normalized_symbol,
        "profile": profile,
        "live": live,
        "connected": True,
        "source": _exchange_source_key() if live else "local_fallback",
        "exchange_context": _exchange_context(),
        "warning": warning,
        "credentials": get_demo_credentials_status(),
        "account": {
            "estimated_equity_usdt": estimated_equity_usdt,
            "wallet_balance_usdt": wallet_balance_usdt,
            "available_usdt": available_usdt,
            "locked_usdt": locked_usdt,
            "open_orders_count": len(open_orders_payload or []),
            "open_orders": open_orders[:12],
            "algo_open_orders_count": len(algo_open_orders_payload or []),
            "algo_open_orders": algo_open_orders[:12],
            "nonzero_assets": balances[:5],
            "tracked_symbols": tracked_symbols,
            "open_positions": positions[:5],
        },
        "behavior": behavior,
        "auto_fill": {
            "account_equity_usdt": wallet_balance_usdt or estimated_equity_usdt,
            "trades_last_24h": int(behavior["trades_last_24h"]),
            "consecutive_losses": int(behavior["consecutive_losses"]),
            "day_pnl_pct": float(behavior["day_pnl_pct"]),
        },
        "agent_context": {
            "behavior_status": _behavior_status(behavior),
            "suggested_position_cap_usdt": suggested_position_cap_usdt,
            "risk_budget_usdt": risk_budget_usdt,
            "active_positions_count": len(positions),
            "closest_liquidation_gap_pct": closest_liq_gap_pct,
        },
        "briefing": _build_account_briefing(
            live=live,
            profile_name=profile,
            estimated_equity_usdt=estimated_equity_usdt,
            available_usdt=available_usdt,
            behavior=behavior,
            suggested_position_cap_usdt=suggested_position_cap_usdt,
            risk_budget_usdt=risk_budget_usdt,
            active_positions_count=len(positions),
            closest_liq_gap_pct=closest_liq_gap_pct,
        ),
    }


def fallback_account_snapshot(
    symbol: str,
    *,
    profile_name: str | None = None,
    warning: str | None = None,
) -> Dict[str, Any]:
    normalized_symbol = str(symbol).upper()
    profile = str(profile_name or "balanced").lower()
    preset = DEFAULT_ACCOUNT_FALLBACKS.get(
        normalized_symbol, DEFAULT_ACCOUNT_FALLBACKS["BNBUSDT"]
    )
    estimated_equity_usdt = float(preset["estimated_equity_usdt"])
    available_usdt = float(preset["available_usdt"])
    wallet_balance_usdt = float(
        next((item.get("estimated_usdt", 0.0) for item in preset["nonzero_assets"] if item.get("asset") == "USDT"), available_usdt)
    )
    behavior = dict(preset["behavior"])
    suggested_position_cap_usdt = round(
        estimated_equity_usdt * _position_vs_equity_limit(profile), 2
    )
    risk_budget_usdt = round(estimated_equity_usdt * _risk_per_trade_limit(profile) / 100.0, 2)

    return {
        "symbol": normalized_symbol,
        "profile": profile,
        "live": False,
        "connected": False,
        "source": "local_fallback",
        "exchange_context": _exchange_context(),
        "warning": warning,
        "credentials": get_demo_credentials_status(),
        "account": {
            "estimated_equity_usdt": round(estimated_equity_usdt, 2),
            "wallet_balance_usdt": round(wallet_balance_usdt, 2),
            "available_usdt": round(available_usdt, 2),
            "locked_usdt": round(float(preset["locked_usdt"]), 2),
            "open_orders_count": int(preset["open_orders_count"]),
            "open_orders": [],
            "algo_open_orders_count": 0,
            "algo_open_orders": [],
            "nonzero_assets": list(preset["nonzero_assets"]),
            "tracked_symbols": sorted(set(TRACKED_ACCOUNT_SYMBOLS + (normalized_symbol,))),
            "open_positions": [],
        },
        "behavior": behavior,
        "auto_fill": {
            "account_equity_usdt": round(wallet_balance_usdt or estimated_equity_usdt, 2),
            "trades_last_24h": int(behavior["trades_last_24h"]),
            "consecutive_losses": int(behavior["consecutive_losses"]),
            "day_pnl_pct": float(behavior["day_pnl_pct"]),
        },
        "agent_context": {
            "behavior_status": _behavior_status(behavior),
            "suggested_position_cap_usdt": suggested_position_cap_usdt,
            "risk_budget_usdt": risk_budget_usdt,
            "active_positions_count": 0,
            "closest_liquidation_gap_pct": None,
        },
        "briefing": _build_account_briefing(
            live=False,
            profile_name=profile,
            estimated_equity_usdt=estimated_equity_usdt,
            available_usdt=available_usdt,
            behavior=behavior,
            suggested_position_cap_usdt=suggested_position_cap_usdt,
            risk_budget_usdt=risk_budget_usdt,
        ),
    }


def get_account_snapshot(
    symbol: str,
    *,
    profile_name: str | None = None,
) -> Dict[str, Any]:
    normalized_symbol = str(symbol).upper()
    creds = get_demo_credentials_status()
    if not creds["configured"]:
        return fallback_account_snapshot(
            normalized_symbol,
            profile_name=profile_name,
            warning=_credentials_hint_text(f"{_exchange_label()} account sync"),
        )

    api_key, secret_key = _configured_credentials()
    start_time_ms = int((time.time() - 24 * 60 * 60) * 1000)
    try:
        snapshot_warning: str | None = None
        account_payload = _signed_json(
            "/fapi/v3/account",
            api_key=api_key,
            secret_key=secret_key,
        )
        tracked_symbols = sorted(
            set(TRACKED_ACCOUNT_SYMBOLS + (normalized_symbol,) + tuple(_nonzero_quote_symbols(account_payload)))
        )
        open_orders_payload = _signed_json(
            "/fapi/v1/openOrders", api_key=api_key, secret_key=secret_key
        )
        try:
            algo_open_orders_payload = _signed_json(
                "/fapi/v1/openAlgoOrders",
                api_key=api_key,
                secret_key=secret_key,
                params={"symbol": normalized_symbol},
            )
        except Exception as exc:
            algo_open_orders_payload = []
            snapshot_warning = str(exc)
        position_risk_payload = _signed_json(
            "/fapi/v2/positionRisk", api_key=api_key, secret_key=secret_key
        )
        trades_by_symbol: Dict[str, List[Dict[str, Any]]] = {}
        for trade_symbol in tracked_symbols:
            trades_by_symbol[trade_symbol] = _signed_json(
                "/fapi/v1/userTrades",
                api_key=api_key,
                secret_key=secret_key,
                params={
                    "symbol": trade_symbol,
                    "limit": 50,
                    "startTime": start_time_ms,
                },
            )
        return build_account_snapshot(
            symbol=normalized_symbol,
            profile_name=profile_name,
            account_payload=account_payload,
            open_orders_payload=open_orders_payload if isinstance(open_orders_payload, list) else [],
            algo_open_orders_payload=(
                algo_open_orders_payload if isinstance(algo_open_orders_payload, list) else []
            ),
            trades_by_symbol=trades_by_symbol,
            position_risk_payload=position_risk_payload if isinstance(position_risk_payload, list) else [],
            live=True,
            warning=snapshot_warning,
        )
    except Exception as exc:
        return fallback_account_snapshot(
            normalized_symbol,
            profile_name=profile_name,
            warning=str(exc),
        )


def cancel_current_symbol_orders(symbol: str) -> Dict[str, Any]:
    normalized_symbol = str(symbol).upper()
    creds = get_demo_credentials_status()
    if not creds["configured"]:
        return {
            "ok": False,
            "status": "not_configured",
            "mode": "preview_only",
            "message": _credentials_hint_text(f"{_exchange_label()} order cancellation"),
            "symbol": normalized_symbol,
            "credentials": creds,
            "exchange_context": _exchange_context(),
        }

    api_key, secret_key = _configured_credentials()
    try:
        open_orders_payload = _signed_json(
            "/fapi/v1/openOrders",
            api_key=api_key,
            secret_key=secret_key,
            params={"symbol": normalized_symbol},
        )
        algo_open_orders_payload = _signed_json(
            "/fapi/v1/openAlgoOrders",
            api_key=api_key,
            secret_key=secret_key,
            params={"symbol": normalized_symbol},
        )
    except Exception as exc:
        return {
            "ok": False,
            "status": "exchange_rejected",
            "mode": _exchange_source_key(),
            "message": str(exc),
            "symbol": normalized_symbol,
            "credentials": creds,
            "exchange_context": _exchange_context(),
        }

    open_orders = open_orders_payload if isinstance(open_orders_payload, list) else []
    algo_open_orders = algo_open_orders_payload if isinstance(algo_open_orders_payload, list) else []
    open_order_count = len(open_orders)
    algo_order_count = len(algo_open_orders)

    if open_order_count == 0 and algo_order_count == 0:
        return {
            "ok": True,
            "status": "nothing_to_cancel",
            "mode": _exchange_source_key(),
            "message": f"No open orders were found for {normalized_symbol}.",
            "symbol": normalized_symbol,
            "canceled_open_orders": 0,
            "canceled_algo_orders": 0,
            "credentials": creds,
            "exchange_context": _exchange_context(),
        }

    open_cancel_result: Dict[str, Any] | None = None
    algo_cancel_result: Dict[str, Any] | None = None
    open_cancel_error: str | None = None
    algo_cancel_error: str | None = None

    if open_order_count > 0:
        try:
            open_cancel_result = _signed_json(
                "/fapi/v1/allOpenOrders",
                api_key=api_key,
                secret_key=secret_key,
                params={"symbol": normalized_symbol},
                method="DELETE",
            )
        except Exception as exc:
            open_cancel_error = str(exc)

    if algo_order_count > 0:
        try:
            algo_cancel_result = _signed_json(
                "/fapi/v1/algoOpenOrders",
                api_key=api_key,
                secret_key=secret_key,
                params={"symbol": normalized_symbol},
                method="DELETE",
            )
        except Exception as exc:
            algo_cancel_error = str(exc)

    ok = not open_cancel_error and not algo_cancel_error
    if ok:
        message = (
            f"Canceled {open_order_count} open orders and {algo_order_count} algo orders "
            f"for {normalized_symbol}."
        )
        status = "canceled"
    else:
        status = "cancel_partial" if (open_cancel_result or algo_cancel_result) else "cancel_failed"
        issues = [item for item in [open_cancel_error, algo_cancel_error] if item]
        message = "; ".join(issues) if issues else "Order cancellation did not complete."

    return {
        "ok": ok,
        "status": status,
        "mode": _exchange_source_key(),
        "message": message,
        "symbol": normalized_symbol,
        "canceled_open_orders": open_order_count if open_cancel_result is not None else 0,
        "canceled_algo_orders": algo_order_count if algo_cancel_result is not None else 0,
        "open_cancel": open_cancel_result,
        "algo_cancel": algo_cancel_result,
        "credentials": creds,
        "exchange_context": _exchange_context(),
    }


def close_current_symbol_position(symbol: str) -> Dict[str, Any]:
    normalized_symbol = str(symbol).upper()
    creds = get_demo_credentials_status()
    if not creds["configured"]:
        return {
            "ok": False,
            "status": "not_configured",
            "mode": "preview_only",
            "message": _credentials_hint_text(f"{_exchange_label()} position close"),
            "symbol": normalized_symbol,
            "credentials": creds,
            "exchange_context": _exchange_context(),
        }

    api_key, secret_key = _configured_credentials()
    try:
        position_risk_payload = _signed_json(
            "/fapi/v2/positionRisk",
            api_key=api_key,
            secret_key=secret_key,
            params={"symbol": normalized_symbol},
        )
    except Exception as exc:
        return {
            "ok": False,
            "status": "exchange_rejected",
            "mode": _exchange_source_key(),
            "message": str(exc),
            "symbol": normalized_symbol,
            "credentials": creds,
            "exchange_context": _exchange_context(),
        }

    raw_positions = position_risk_payload if isinstance(position_risk_payload, list) else []
    close_orders: List[Dict[str, Any]] = []
    for row in raw_positions:
        row_symbol = str(row.get("symbol", "")).upper()
        if row_symbol != normalized_symbol:
            continue
        quantity_text = str(row.get("positionAmt", "")).strip()
        quantity_decimal = _coerce_decimal(quantity_text)
        if quantity_decimal == 0:
            continue
        position_side = str(row.get("positionSide", "BOTH")).upper()
        if position_side == "LONG":
            side = "SELL"
        elif position_side == "SHORT":
            side = "BUY"
        else:
            side = "SELL" if quantity_decimal > 0 else "BUY"

        params: Dict[str, Any] = {
            "symbol": normalized_symbol,
            "side": side,
            "type": "MARKET",
            "quantity": _format_decimal_value(abs(quantity_decimal), Decimal("0.00000001"), 8),
            "recvWindow": str(DEFAULT_RECV_WINDOW_MS),
            "newOrderRespType": "RESULT",
        }
        if position_side in {"LONG", "SHORT"}:
            params["positionSide"] = position_side
        else:
            params["reduceOnly"] = "true"
        close_orders.append(params)

    if not close_orders:
        return {
            "ok": True,
            "status": "nothing_to_close",
            "mode": _exchange_source_key(),
            "message": f"No active position was found for {normalized_symbol}.",
            "symbol": normalized_symbol,
            "closed_positions": [],
            "credentials": creds,
            "exchange_context": _exchange_context(),
        }

    executions: List[Dict[str, Any]] = []
    try:
        for params in close_orders:
            executions.append(
                _place_named_futures_order(
                    api_key=api_key,
                    secret_key=secret_key,
                    params=params,
                    client_order_id=f"cpgclose{int(time.time() * 1000)}{len(executions)}",
                )
            )
    except Exception as exc:
        return {
            "ok": False,
            "status": "exchange_rejected",
            "mode": _exchange_source_key(),
            "message": str(exc),
            "symbol": normalized_symbol,
            "closed_positions": executions,
            "credentials": creds,
            "exchange_context": _exchange_context(),
        }

    return {
        "ok": True,
        "status": "closed",
        "mode": _exchange_source_key(),
        "message": f"Submitted {len(executions)} market close orders for {normalized_symbol}.",
        "symbol": normalized_symbol,
        "closed_positions": executions,
        "credentials": creds,
        "exchange_context": _exchange_context(),
    }


def demo_order_test(trade_payload: Dict[str, Any]) -> Dict[str, Any]:
    preview = build_demo_order_preview(trade_payload)
    creds = get_demo_credentials_status()
    if not creds["configured"]:
        return {
            "ok": False,
            "status": "not_configured",
            "mode": "preview_only",
            "message": _credentials_hint_text(f"{_exchange_label()} order validation"),
            "preview": preview,
            "credentials": creds,
            "exchange_context": _exchange_context(),
        }

    api_key, secret_key = _configured_credentials()
    preview = _apply_position_side(
        preview,
        dual_side_position=_futures_dual_side_position(api_key, secret_key),
    )
    requested_margin_type = str(preview.get("requested_margin_type", "CROSSED"))
    requested_leverage = int(preview.get("requested_leverage", 0) or 0)
    base_response = {
        "preview": preview,
        "credentials": creds,
        "exchange_context": _exchange_context(),
    }

    trading_rules = preview.get("exchange_rules")
    if isinstance(trading_rules, dict):
        filter_issue = _preview_filter_issue(preview, trading_rules)
        if filter_issue:
            return {
                "ok": False,
                "status": "preview_invalid",
                "mode": "preview_only",
                "message": filter_issue,
                **base_response,
            }

    params = _exchange_order_params(preview)
    params["timestamp"] = int(time.time() * 1000)
    query = _signed_query(params, secret_key)
    url = f"{_api_base()}/fapi/v1/order/test?{query}"
    request = Request(url, method="POST", headers={"X-MBX-APIKEY": api_key})

    try:
        with urlopen(request, timeout=DEFAULT_TIMEOUT_SECONDS) as response:
            body = response.read().decode("utf-8")
            payload = json.loads(body) if body else {}
        return {
            "ok": True,
            "status": "validated",
            "mode": _exchange_source_key(),
            "message": f"{_exchange_label()} accepted the test order.",
            "response": payload,
            **base_response,
        }
    except HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        try:
            payload = json.loads(detail)
        except json.JSONDecodeError:
            payload = {"msg": detail or exc.reason}
        return {
            "ok": False,
            "status": "exchange_rejected",
            "mode": _exchange_source_key(),
            "message": payload.get("msg", detail or "Binance rejected the test order."),
            "response": payload,
            **base_response,
        }
    except URLError as exc:
        return {
            "ok": False,
            "status": "network_unavailable",
            "mode": "preview_only",
            "message": f"Could not reach {_exchange_label()}: {exc.reason}",
            **base_response,
        }


def live_order_place_and_cancel(
    trade_payload: Dict[str, Any],
    *,
    confirm_live_execution: bool = False,
) -> Dict[str, Any]:
    if not confirm_live_execution:
        return {
            "ok": False,
            "status": "confirmation_required",
            "mode": "preview_only",
            "message": "Live execution requires explicit confirmation.",
            "credentials": get_demo_credentials_status(),
            "exchange_context": _exchange_context(),
        }

    try:
        preview = build_live_order_preview(trade_payload)
    except Exception as exc:
        return {
            "ok": False,
            "status": "preview_invalid",
            "mode": "preview_only",
            "message": str(exc),
            "credentials": get_demo_credentials_status(),
            "exchange_context": _exchange_context(),
        }

    creds = get_demo_credentials_status()
    if not creds["configured"]:
        return {
            "ok": False,
            "status": "not_configured",
            "mode": "preview_only",
            "message": _credentials_hint_text(f"{_exchange_label()} live order execution"),
            "preview": preview,
            "credentials": creds,
            "exchange_context": _exchange_context(),
        }

    api_key, secret_key = _configured_credentials()
    preview = _apply_position_side(
        preview,
        dual_side_position=_futures_dual_side_position(api_key, secret_key),
    )
    requested_margin_type = str(preview.get("requested_margin_type", "CROSSED"))
    requested_leverage = int(preview.get("requested_leverage", 0) or 0)
    base_response = {
        "preview": preview,
        "credentials": creds,
        "exchange_context": _exchange_context(),
    }

    trading_rules = preview.get("exchange_rules")
    if isinstance(trading_rules, dict):
        filter_issue = _preview_filter_issue(preview, trading_rules)
        if filter_issue:
            return {
                "ok": False,
                "status": "preview_invalid",
                "mode": "preview_only",
                "message": filter_issue,
                **base_response,
            }

    try:
        margin_sync = _sync_futures_margin_type(
            symbol=str(preview["symbol"]),
            margin_type=requested_margin_type,
            api_key=api_key,
            secret_key=secret_key,
        )
    except Exception as exc:
        return {
            "ok": False,
            "status": "exchange_rejected",
            "mode": _exchange_source_key(),
            "message": f"Margin mode sync failed: {exc}",
            **base_response,
        }

    try:
        leverage_sync = _sync_futures_initial_leverage(
            symbol=str(preview["symbol"]),
            leverage=requested_leverage,
            api_key=api_key,
            secret_key=secret_key,
        )
    except Exception as exc:
        return {
            "ok": False,
            "status": "exchange_rejected",
            "mode": _exchange_source_key(),
            "message": f"Leverage sync failed: {exc}",
            **base_response,
        }

    client_order_id = f"cpglive{int(time.time() * 1000)}"
    create_params = _exchange_order_params(preview)
    create_params["newClientOrderId"] = client_order_id

    try:
        execution_payload = _signed_json(
            "/fapi/v1/order",
            api_key=api_key,
            secret_key=secret_key,
            params=create_params,
            method="POST",
        )
    except Exception as exc:
        return {
            "ok": False,
            "status": "exchange_rejected",
            "mode": _exchange_source_key(),
            "message": str(exc),
            **base_response,
        }

    order_id = execution_payload.get("orderId")
    try:
        cancel_payload = _signed_json(
            "/fapi/v1/order",
            api_key=api_key,
            secret_key=secret_key,
            params={"symbol": str(preview["symbol"]), "orderId": order_id},
            method="DELETE",
        )
    except Exception as exc:
        error_text = str(exc)
        if "Unknown order sent" in error_text:
            return {
                "ok": True,
                "status": "placed_then_canceled",
                "mode": _exchange_source_key(),
                "message": (
                    f"Placed a live {_exchange_label()} limit order and it was already gone by the time cancel was attempted."
                ),
                "margin_sync": margin_sync,
                "leverage_sync": leverage_sync,
                "execution": execution_payload,
                "cancel": {
                    "symbol": str(preview["symbol"]),
                    "orderId": order_id,
                    "status": "ALREADY_GONE",
                    "message": error_text,
                },
                **base_response,
            }
        return {
            "ok": False,
            "status": "cancel_failed",
            "mode": _exchange_source_key(),
            "message": f"Live order was placed but cancel failed: {exc}",
            "execution": execution_payload,
            **base_response,
        }

    return {
        "ok": True,
        "status": "placed_then_canceled",
        "mode": _exchange_source_key(),
        "message": (
            f"Placed a live {_exchange_label()} limit order and canceled it immediately."
        ),
        "margin_sync": margin_sync,
        "leverage_sync": leverage_sync,
        "execution": execution_payload,
        "cancel": cancel_payload,
        **base_response,
    }


def live_order_open_position(
    trade_payload: Dict[str, Any],
    *,
    confirm_live_execution: bool = False,
) -> Dict[str, Any]:
    if not confirm_live_execution:
        return {
            "ok": False,
            "status": "confirmation_required",
            "mode": "preview_only",
            "message": "Live execution requires explicit confirmation.",
            "credentials": get_demo_credentials_status(),
            "exchange_context": _exchange_context(),
        }

    try:
        _requested_protective_targets(trade_payload)
        preview = build_live_open_order_preview(trade_payload)
    except Exception as exc:
        return {
            "ok": False,
            "status": "preview_invalid",
            "mode": "preview_only",
            "message": str(exc),
            "credentials": get_demo_credentials_status(),
            "exchange_context": _exchange_context(),
        }

    creds = get_demo_credentials_status()
    if not creds["configured"]:
        return {
            "ok": False,
            "status": "not_configured",
            "mode": "preview_only",
            "message": _credentials_hint_text(f"{_exchange_label()} live order execution"),
            "preview": preview,
            "credentials": creds,
            "exchange_context": _exchange_context(),
        }

    api_key, secret_key = _configured_credentials()
    preview = _apply_position_side(
        preview,
        dual_side_position=_futures_dual_side_position(api_key, secret_key),
    )
    requested_margin_type = str(preview.get("requested_margin_type", "CROSSED"))
    requested_leverage = int(preview.get("requested_leverage", 0) or 0)
    try:
        protection_orders_preview = _build_futures_protection_orders(
            trade_payload=trade_payload,
            preview=preview,
        )
    except Exception as exc:
        return {
            "ok": False,
            "status": "preview_invalid",
            "mode": "preview_only",
            "message": str(exc),
            "preview": preview,
            "credentials": creds,
            "exchange_context": _exchange_context(),
        }
    base_response = {
        "preview": preview,
        "protection_preview": protection_orders_preview,
        "credentials": creds,
        "exchange_context": _exchange_context(),
    }

    trading_rules = preview.get("exchange_rules")
    if isinstance(trading_rules, dict):
        filter_issue = _preview_filter_issue(preview, trading_rules)
        if filter_issue:
            return {
                "ok": False,
                "status": "preview_invalid",
                "mode": "preview_only",
                "message": filter_issue,
                **base_response,
            }

    try:
        margin_sync = _sync_futures_margin_type(
            symbol=str(preview["symbol"]),
            margin_type=requested_margin_type,
            api_key=api_key,
            secret_key=secret_key,
        )
    except Exception as exc:
        return {
            "ok": False,
            "status": "exchange_rejected",
            "mode": _exchange_source_key(),
            "message": f"Margin mode sync failed: {exc}",
            **base_response,
        }

    try:
        leverage_sync = _sync_futures_initial_leverage(
            symbol=str(preview["symbol"]),
            leverage=requested_leverage,
            api_key=api_key,
            secret_key=secret_key,
        )
    except Exception as exc:
        return {
            "ok": False,
            "status": "exchange_rejected",
            "mode": _exchange_source_key(),
            "message": f"Leverage sync failed: {exc}",
            **base_response,
        }

    required_initial_margin = Decimal(str(preview.get("required_initial_margin_usdt", "0") or "0"))
    try:
        available_balance = _available_balance_usdt(api_key, secret_key)
    except Exception as exc:
        return {
            "ok": False,
            "status": "exchange_rejected",
            "mode": _exchange_source_key(),
            "message": f"Account balance precheck failed: {exc}",
            **base_response,
        }
    if required_initial_margin > 0 and required_initial_margin > available_balance:
        return {
            "ok": False,
            "status": "exchange_rejected",
            "mode": _exchange_source_key(),
            "message": (
                "Insufficient available USDT for requested execution. "
                f"Required initial margin {required_initial_margin:.2f} USDT, "
                f"available {available_balance:.2f} USDT."
            ),
            "available_balance_usdt": _format_decimal_value(available_balance, Decimal("0.01"), 2),
            **base_response,
        }

    create_params = _exchange_order_params(preview)
    try:
        _validate_futures_order_params(
            api_key=api_key,
            secret_key=secret_key,
            params=create_params,
        )
    except Exception as exc:
        return {
            "ok": False,
            "status": "exchange_rejected",
            "mode": _exchange_source_key(),
            "message": str(exc),
            **base_response,
        }
    create_params["newClientOrderId"] = f"cpgopen{int(time.time() * 1000)}"

    try:
        execution_payload = _signed_json(
            "/fapi/v1/order",
            api_key=api_key,
            secret_key=secret_key,
            params=create_params,
            method="POST",
        )
    except Exception as exc:
        return {
            "ok": False,
            "status": "exchange_rejected",
            "mode": _exchange_source_key(),
            "message": str(exc),
            **base_response,
        }
    execution_summary = _build_execution_summary(
        preview=preview,
        execution_payload=execution_payload if isinstance(execution_payload, dict) else {},
    )

    stop_loss_payload: Dict[str, Any] | None = None
    try:
        stop_loss_payload = _place_named_futures_algo_order(
            api_key=api_key,
            secret_key=secret_key,
            params=protection_orders_preview["stop_loss"],
            client_algo_id=f"cpgsl{int(time.time() * 1000)}",
        )
    except Exception as exc:
        try:
            emergency_close = _emergency_close_market_order(
                api_key=api_key,
                secret_key=secret_key,
                preview=preview,
                execution_payload=execution_payload if isinstance(execution_payload, dict) else {},
            )
        except Exception as close_exc:
            return {
                "ok": False,
                "status": "protection_failed",
                "mode": _exchange_source_key(),
                "message": (
                    "Position opened, but stop-loss protection failed and emergency close also failed: "
                    f"{close_exc}"
                ),
                "execution": execution_payload,
                "execution_summary": execution_summary,
                "protection_orders": {},
                **base_response,
            }
        return {
            "ok": False,
            "status": "protection_failed",
            "mode": _exchange_source_key(),
            "message": (
                "Position opened, but stop-loss protection failed. An emergency close order was submitted."
            ),
            "execution": execution_payload,
            "execution_summary": execution_summary,
            "emergency_close": emergency_close,
            "protection_orders": {},
            **base_response,
        }

    take_profit_payload: Dict[str, Any] | None = None
    try:
        take_profit_payload = _place_named_futures_algo_order(
            api_key=api_key,
            secret_key=secret_key,
            params=protection_orders_preview["take_profit"],
            client_algo_id=f"cpgtp{int(time.time() * 1000)}",
        )
    except Exception as exc:
        return {
            "ok": False,
            "status": "protection_partial",
            "mode": _exchange_source_key(),
            "message": (
                "Position opened and stop-loss protection is active, but take-profit order placement failed: "
                f"{exc}"
            ),
            "execution": execution_payload,
            "execution_summary": execution_summary,
            "protection_orders": {
                "stop_loss": stop_loss_payload,
            },
            **base_response,
        }

    return {
        "ok": True,
        "status": "opened",
        "mode": _exchange_source_key(),
        "message": (
            f"Placed a live {_exchange_label()} market order and posted stop-loss and take-profit protection orders."
        ),
        "margin_sync": margin_sync,
        "leverage_sync": leverage_sync,
        "execution": execution_payload,
        "execution_summary": execution_summary,
        "protection_orders": {
            "stop_loss": stop_loss_payload,
            "take_profit": take_profit_payload,
        },
        **base_response,
    }
