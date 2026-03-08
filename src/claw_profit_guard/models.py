"""Data models for ClawProfit Guard."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


Decision = str  # ALLOW | WARN | BLOCK


def _to_float(value: Any, field_name: str) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        raise ValueError(f"{field_name} must be a number.")


def _to_int(value: Any, field_name: str) -> int:
    try:
        ivalue = int(value)
    except (TypeError, ValueError):
        raise ValueError(f"{field_name} must be an integer.")
    return ivalue


def _to_bool_strict(value: Any, field_name: str) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        normalized = value.strip().lower()
        if normalized in {"true", "1", "yes", "y", "on"}:
            return True
        if normalized in {"false", "0", "no", "n", "off"}:
            return False
    raise ValueError(
        f"{field_name} must be a boolean (true/false), got {value!r}."
    )


@dataclass
class TradeIntent:
    symbol: str
    side: str
    entry_price: float
    stop_loss_price: Optional[float]
    take_profit_price: Optional[float]
    leverage: float
    position_notional_usdt: float
    account_equity_usdt: float

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "TradeIntent":
        stop_loss = data.get("stop_loss_price")
        take_profit = data.get("take_profit_price")
        side = str(data["side"]).upper()
        if side not in {"LONG", "SHORT"}:
            raise ValueError("trade.side must be LONG or SHORT.")
        entry_price = _to_float(data["entry_price"], "trade.entry_price")
        leverage = _to_float(data["leverage"], "trade.leverage")
        position_notional = _to_float(
            data["position_notional_usdt"], "trade.position_notional_usdt"
        )
        account_equity = _to_float(
            data["account_equity_usdt"], "trade.account_equity_usdt"
        )
        if entry_price <= 0:
            raise ValueError("trade.entry_price must be greater than zero.")
        if leverage <= 0:
            raise ValueError("trade.leverage must be greater than zero.")
        if position_notional <= 0:
            raise ValueError("trade.position_notional_usdt must be greater than zero.")
        if account_equity <= 0:
            raise ValueError("trade.account_equity_usdt must be greater than zero.")
        stop_loss_value = (
            _to_float(stop_loss, "trade.stop_loss_price")
            if stop_loss is not None
            else None
        )
        take_profit_value = (
            _to_float(take_profit, "trade.take_profit_price")
            if take_profit is not None
            else None
        )
        if stop_loss_value is not None and stop_loss_value <= 0:
            raise ValueError("trade.stop_loss_price must be greater than zero.")
        if take_profit_value is not None and take_profit_value <= 0:
            raise ValueError("trade.take_profit_price must be greater than zero.")
        return TradeIntent(
            symbol=str(data["symbol"]).upper(),
            side=side,
            entry_price=entry_price,
            stop_loss_price=stop_loss_value,
            take_profit_price=take_profit_value,
            leverage=leverage,
            position_notional_usdt=position_notional,
            account_equity_usdt=account_equity,
        )


@dataclass
class MarketContext:
    volatility_24h_pct: float
    bid_ask_spread_bps: float
    liquidity_depth_score: float

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "MarketContext":
        volatility = _to_float(data.get("volatility_24h_pct", 0.0), "market.volatility_24h_pct")
        spread = _to_float(data.get("bid_ask_spread_bps", 0.0), "market.bid_ask_spread_bps")
        depth = _to_float(data.get("liquidity_depth_score", 50.0), "market.liquidity_depth_score")
        if depth < 0 or depth > 100:
            raise ValueError("market.liquidity_depth_score must be in range 0-100.")
        return MarketContext(
            volatility_24h_pct=volatility,
            bid_ask_spread_bps=spread,
            liquidity_depth_score=depth,
        )


@dataclass
class BehaviorContext:
    consecutive_losses: int = 0
    trades_last_24h: int = 0
    day_pnl_pct: float = 0.0

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "BehaviorContext":
        losses = _to_int(data.get("consecutive_losses", 0), "behavior.consecutive_losses")
        trades = _to_int(data.get("trades_last_24h", 0), "behavior.trades_last_24h")
        day_pnl = _to_float(data.get("day_pnl_pct", 0.0), "behavior.day_pnl_pct")
        if losses < 0:
            raise ValueError("behavior.consecutive_losses must be >= 0.")
        if trades < 0:
            raise ValueError("behavior.trades_last_24h must be >= 0.")
        return BehaviorContext(
            consecutive_losses=losses,
            trades_last_24h=trades,
            day_pnl_pct=day_pnl,
        )


@dataclass
class GuardrailConfig:
    max_leverage: float = 20.0
    max_position_vs_equity: float = 1.5
    max_daily_loss_pct: float = 8.0
    max_consecutive_losses: int = 4
    require_stop_loss: bool = True
    max_risk_per_trade_pct: float = 2.0
    min_reward_risk_ratio: float = 1.5
    allow_symbols: List[str] = field(
        default_factory=lambda: [
            "BTCUSDT",
            "ETHUSDT",
            "BNBUSDT",
        ]
    )

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "GuardrailConfig":
        cfg = GuardrailConfig()
        if not data:
            return cfg
        if "max_leverage" in data:
            cfg.max_leverage = _to_float(data["max_leverage"], "guardrails.max_leverage")
        if "max_position_vs_equity" in data:
            cfg.max_position_vs_equity = _to_float(
                data["max_position_vs_equity"], "guardrails.max_position_vs_equity"
            )
        if "max_daily_loss_pct" in data:
            cfg.max_daily_loss_pct = _to_float(
                data["max_daily_loss_pct"], "guardrails.max_daily_loss_pct"
            )
        if "max_consecutive_losses" in data:
            cfg.max_consecutive_losses = _to_int(
                data["max_consecutive_losses"], "guardrails.max_consecutive_losses"
            )
        if "require_stop_loss" in data:
            cfg.require_stop_loss = _to_bool_strict(
                data["require_stop_loss"], "guardrails.require_stop_loss"
            )
        if "max_risk_per_trade_pct" in data:
            cfg.max_risk_per_trade_pct = _to_float(
                data["max_risk_per_trade_pct"], "guardrails.max_risk_per_trade_pct"
            )
        if "min_reward_risk_ratio" in data:
            cfg.min_reward_risk_ratio = _to_float(
                data["min_reward_risk_ratio"], "guardrails.min_reward_risk_ratio"
            )
        if "allow_symbols" in data and isinstance(data["allow_symbols"], list):
            cfg.allow_symbols = [str(x).upper() for x in data["allow_symbols"]]
        if cfg.max_leverage <= 0:
            raise ValueError("guardrails.max_leverage must be greater than zero.")
        if cfg.max_position_vs_equity <= 0:
            raise ValueError("guardrails.max_position_vs_equity must be greater than zero.")
        if cfg.max_daily_loss_pct <= 0:
            raise ValueError("guardrails.max_daily_loss_pct must be greater than zero.")
        if cfg.max_consecutive_losses <= 0:
            raise ValueError("guardrails.max_consecutive_losses must be greater than zero.")
        if cfg.max_risk_per_trade_pct <= 0:
            raise ValueError("guardrails.max_risk_per_trade_pct must be greater than zero.")
        if cfg.min_reward_risk_ratio <= 0:
            raise ValueError("guardrails.min_reward_risk_ratio must be greater than zero.")
        return cfg

    def to_dict(self) -> Dict[str, Any]:
        return {
            "max_leverage": float(self.max_leverage),
            "max_position_vs_equity": float(self.max_position_vs_equity),
            "max_daily_loss_pct": float(self.max_daily_loss_pct),
            "max_consecutive_losses": int(self.max_consecutive_losses),
            "require_stop_loss": bool(self.require_stop_loss),
            "max_risk_per_trade_pct": float(self.max_risk_per_trade_pct),
            "min_reward_risk_ratio": float(self.min_reward_risk_ratio),
            "allow_symbols": list(self.allow_symbols),
        }


@dataclass
class EvaluationInput:
    trade: TradeIntent
    market: MarketContext
    behavior: BehaviorContext
    guardrails: GuardrailConfig
    profile_context: Dict[str, Any] = field(default_factory=dict)

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "EvaluationInput":
        behavior = BehaviorContext.from_dict(data.get("behavior", {}))
        profile_context: Dict[str, Any] = {}

        guardrails_data = data.get("guardrails", {})
        if guardrails_data:
            from .risk_profile import enforce_system_guardrail_limits

            guardrails = enforce_system_guardrail_limits(
                GuardrailConfig.from_dict(guardrails_data)
            )
        else:
            # Lazy import avoids circular dependency at module load time.
            from .risk_profile import derive_guardrails_from_payload

            guardrails, profile_context = derive_guardrails_from_payload(
                payload=data, behavior=behavior
            )

        return EvaluationInput(
            trade=TradeIntent.from_dict(data["trade"]),
            market=MarketContext.from_dict(data.get("market", {})),
            behavior=behavior,
            guardrails=guardrails,
            profile_context=profile_context,
        )


@dataclass
class ProfileRecommendation:
    profile: str
    profile_score: float
    subjective_score: float
    behavior_penalty: float
    behavior_bonus: float
    strengths: List[str]
    issues: List[str]
    coaching: List[str]
    auto_adjustments: List[str]
    guardrails: GuardrailConfig

    def to_dict(self) -> Dict[str, Any]:
        return {
            "profile": self.profile,
            "profile_score": round(self.profile_score, 2),
            "subjective_score": round(self.subjective_score, 2),
            "behavior_penalty": round(self.behavior_penalty, 2),
            "behavior_bonus": round(self.behavior_bonus, 2),
            "strengths": self.strengths,
            "issues": self.issues,
            "coaching": self.coaching,
            "auto_adjustments": self.auto_adjustments,
            "guardrails": self.guardrails.to_dict(),
        }


@dataclass
class SuggestedPlan:
    leverage: float
    position_notional_usdt: float
    stop_loss_price: Optional[float]
    take_profit_price: Optional[float]
    note: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "leverage": round(self.leverage, 2),
            "position_notional_usdt": round(self.position_notional_usdt, 2),
            "stop_loss_price": (
                None if self.stop_loss_price is None else round(self.stop_loss_price, 8)
            ),
            "take_profit_price": (
                None if self.take_profit_price is None else round(self.take_profit_price, 8)
            ),
            "note": self.note,
        }


@dataclass
class EvaluationResult:
    decision: Decision
    risk_score: float
    reasons: List[str]
    blockers: List[str]
    metric_breakdown: Dict[str, float]
    suggested_plan: SuggestedPlan
    profile_context: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        data = {
            "decision": self.decision,
            "risk_score": round(self.risk_score, 2),
            "reasons": self.reasons,
            "blockers": self.blockers,
            "metric_breakdown": {
                k: round(v, 2) for k, v in self.metric_breakdown.items()
            },
            "suggested_plan": self.suggested_plan.to_dict(),
        }
        if self.profile_context:
            data["profile_context"] = self.profile_context
        return data
