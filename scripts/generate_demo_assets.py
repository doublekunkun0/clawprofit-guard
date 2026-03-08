#!/usr/bin/env python3
"""Generate deterministic demo assets for the 60-second contest video."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.claw_profit_guard.engine import evaluate_trade
from src.claw_profit_guard.binance_demo import demo_order_test
from src.claw_profit_guard.models import EvaluationInput
from src.claw_profit_guard.risk_profile import recommend_profile

OUT_DIR = ROOT / "output" / "demo"


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=True, indent=2), encoding="utf-8")


def main() -> None:
    profile_payload: Dict[str, Any] = {
        "selected_profile": "aggressive",
        "quiz": {
            "experience_level": "intermediate",
            "risk_tolerance": "high",
            "leverage_preference": "high",
            "stop_loss_discipline": "sometimes",
            "revenge_tendency": "sometimes",
            "trading_frequency": "high",
            "max_drawdown_comfort_pct": 11,
        },
        "behavior": {
            "consecutive_losses": 3,
            "trades_last_24h": 17,
            "day_pnl_pct": -3.2,
        },
        "preferences": {
            "allow_symbols": ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT"],
        },
    }
    profile_result = recommend_profile(profile_payload).to_dict()
    _write_json(OUT_DIR / "01_profile_recommendation.json", profile_result)

    blocked_trade_payload: Dict[str, Any] = {
        "profile": profile_result["profile"],
        "trade": {
            "symbol": "BTCUSDT",
            "side": "LONG",
            "entry_price": 91300,
            "stop_loss_price": 90000,
            "take_profit_price": 92000,
            "leverage": 14,
            "position_notional_usdt": 3400,
            "account_equity_usdt": 2000,
        },
        "market": {
            "volatility_24h_pct": 6.2,
            "bid_ask_spread_bps": 7,
            "liquidity_depth_score": 78,
        },
        "behavior": {
            "consecutive_losses": 1,
            "trades_last_24h": 9,
            "day_pnl_pct": -1.4,
        },
    }

    blocked_result = evaluate_trade(EvaluationInput.from_dict(blocked_trade_payload)).to_dict()
    _write_json(OUT_DIR / "02_trade_blocked.json", blocked_result)

    suggestion = blocked_result["suggested_plan"]
    adjusted_trade_payload = json.loads(json.dumps(blocked_trade_payload))
    adjusted_trade_payload["trade"]["leverage"] = suggestion["leverage"]
    adjusted_trade_payload["trade"]["position_notional_usdt"] = suggestion[
        "position_notional_usdt"
    ]
    adjusted_trade_payload["trade"]["stop_loss_price"] = suggestion["stop_loss_price"]
    adjusted_trade_payload["trade"]["take_profit_price"] = suggestion["take_profit_price"]

    # Ensure adjusted plan also satisfies max risk-per-trade.
    guardrails = profile_result["guardrails"]
    entry = adjusted_trade_payload["trade"]["entry_price"]
    stop = adjusted_trade_payload["trade"]["stop_loss_price"]
    equity = adjusted_trade_payload["trade"]["account_equity_usdt"]
    if stop is not None and entry > 0:
        sl_distance_pct = abs(entry - stop) / entry * 100.0
        if sl_distance_pct > 0:
            max_notional_for_risk = (
                equity * guardrails["max_risk_per_trade_pct"] / sl_distance_pct
            )
            adjusted_trade_payload["trade"]["position_notional_usdt"] = round(
                min(
                    adjusted_trade_payload["trade"]["position_notional_usdt"],
                    max_notional_for_risk * 0.98,
                ),
                2,
            )

    adjusted_result = evaluate_trade(EvaluationInput.from_dict(adjusted_trade_payload)).to_dict()
    _write_json(OUT_DIR / "03_trade_adjusted.json", adjusted_result)
    order_preview = demo_order_test(adjusted_trade_payload["trade"])
    _write_json(OUT_DIR / "04_spot_order_preview.json", order_preview)

    summary = {
        "profile": profile_result["profile"],
        "blocked_decision": blocked_result["decision"],
        "blocked_score": blocked_result["risk_score"],
        "adjusted_decision": adjusted_result["decision"],
        "adjusted_score": adjusted_result["risk_score"],
        "suggestion_used": suggestion,
        "order_preview_status": order_preview["status"],
        "asset_files": [
            str(OUT_DIR / "01_profile_recommendation.json"),
            str(OUT_DIR / "02_trade_blocked.json"),
            str(OUT_DIR / "03_trade_adjusted.json"),
            str(OUT_DIR / "04_spot_order_preview.json"),
        ],
    }
    _write_json(OUT_DIR / "00_summary.json", summary)

    print("Demo assets generated:")
    for f in summary["asset_files"]:
        print(f"- {f}")
    print(f"- {OUT_DIR / '00_summary.json'}")
    print(
        f"Decision flow: {summary['blocked_decision']} ({summary['blocked_score']}) -> "
        f"{summary['adjusted_decision']} ({summary['adjusted_score']})"
    )


if __name__ == "__main__":
    main()
