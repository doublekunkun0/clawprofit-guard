"""Risk evaluation engine for ClawProfit Guard."""

from __future__ import annotations

from typing import Dict, List, Tuple

from .models import EvaluationInput, EvaluationResult, SuggestedPlan


COMPARISON_EPS = 1e-9


def _clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def _is_meaningfully_below(value: float, target: float, eps: float = COMPARISON_EPS) -> bool:
    return value + eps < target


def _score_leverage(leverage: float, max_leverage: float) -> float:
    ratio = leverage / max(max_leverage, 1e-6)
    return _clamp((ratio**1.15) * 100.0, 0.0, 100.0)


def _score_volatility(volatility_24h_pct: float) -> float:
    return _clamp((volatility_24h_pct / 12.0) * 100.0, 0.0, 100.0)


def _score_concentration(position_notional: float, equity: float) -> float:
    ratio = position_notional / max(equity, 1e-6)
    return _clamp((ratio / 2.0) * 100.0, 0.0, 100.0)


def _score_liquidity(spread_bps: float, depth_score: float) -> float:
    spread_part = _clamp((spread_bps / 25.0) * 70.0, 0.0, 70.0)
    depth_penalty = _clamp((100.0 - depth_score) * 0.3, 0.0, 30.0)
    return _clamp(spread_part + depth_penalty, 0.0, 100.0)


def _score_behavior(consecutive_losses: int, trades_last_24h: int, day_pnl_pct: float) -> float:
    losses_score = _clamp((consecutive_losses / 5.0) * 45.0, 0.0, 45.0)
    overtrading_score = _clamp((trades_last_24h / 30.0) * 30.0, 0.0, 30.0)
    drawdown_score = _clamp((max(0.0, -day_pnl_pct) / 10.0) * 25.0, 0.0, 25.0)
    return _clamp(losses_score + overtrading_score + drawdown_score, 0.0, 100.0)


def _risk_per_trade_pct(intent: EvaluationInput) -> float:
    trade = intent.trade
    if trade.stop_loss_price is None or trade.entry_price <= 0:
        return 100.0
    sl_distance_pct = abs(trade.entry_price - trade.stop_loss_price) / trade.entry_price * 100.0
    used_margin = trade.position_notional_usdt / max(trade.leverage, 1e-6)
    loss_usdt = used_margin * (sl_distance_pct / 100.0) * trade.leverage
    return (loss_usdt / max(trade.account_equity_usdt, 1e-6)) * 100.0


def _reward_risk_ratio(intent: EvaluationInput) -> float:
    trade = intent.trade
    if trade.stop_loss_price is None or trade.take_profit_price is None:
        return 0.0

    if trade.side == "LONG":
        risk_distance = trade.entry_price - trade.stop_loss_price
        reward_distance = trade.take_profit_price - trade.entry_price
    else:
        risk_distance = trade.stop_loss_price - trade.entry_price
        reward_distance = trade.entry_price - trade.take_profit_price

    if risk_distance <= 0 or reward_distance <= 0:
        return 0.0
    return reward_distance / risk_distance


def _liquidation_buffer_pct(leverage: float) -> float:
    # Coarse approximation for demo purposes.
    return _clamp((100.0 / max(leverage, 1e-6)) * 0.85, 0.5, 60.0)


def _build_suggestions(intent: EvaluationInput, blockers: List[str], risk_score: float) -> SuggestedPlan:
    trade = intent.trade
    guardrails = intent.guardrails

    leverage_target = min(trade.leverage, guardrails.max_leverage)
    if risk_score >= 71:
        leverage_target = min(leverage_target, max(2.0, guardrails.max_leverage * 0.35))
    elif risk_score >= 31:
        leverage_target = min(leverage_target, max(3.0, guardrails.max_leverage * 0.55))

    max_notional_by_equity = trade.account_equity_usdt * guardrails.max_position_vs_equity
    if risk_score >= 71:
        max_notional_by_equity *= 0.6
    elif risk_score >= 31:
        max_notional_by_equity *= 0.8

    if trade.stop_loss_price is None:
        if trade.side == "LONG":
            stop_loss_target = trade.entry_price * 0.985
        else:
            stop_loss_target = trade.entry_price * 1.015
    else:
        stop_loss_target = trade.stop_loss_price
        if trade.side == "LONG" and stop_loss_target >= trade.entry_price:
            stop_loss_target = trade.entry_price * 0.985
        if trade.side == "SHORT" and stop_loss_target <= trade.entry_price:
            stop_loss_target = trade.entry_price * 1.015

    sl_distance_pct = 0.0
    if trade.entry_price > 0 and stop_loss_target is not None:
        sl_distance_pct = abs(trade.entry_price - stop_loss_target) / trade.entry_price * 100.0

    if sl_distance_pct > 0:
        max_notional_by_risk = (
            trade.account_equity_usdt * guardrails.max_risk_per_trade_pct / sl_distance_pct
        )
        max_notional_by_risk *= 0.98
    else:
        max_notional_by_risk = trade.position_notional_usdt

    max_notional = min(max_notional_by_equity, max_notional_by_risk)
    position_target = min(trade.position_notional_usdt, max_notional)
    take_profit_target = trade.take_profit_price
    stop_distance_abs = abs(trade.entry_price - stop_loss_target)
    target_reward_risk = guardrails.min_reward_risk_ratio
    current_rr = _reward_risk_ratio(intent)

    if stop_distance_abs > 0:
        if _is_meaningfully_below(current_rr, target_reward_risk) or take_profit_target is None:
            if trade.side == "LONG":
                take_profit_target = trade.entry_price + (stop_distance_abs * target_reward_risk)
            else:
                take_profit_target = trade.entry_price - (stop_distance_abs * target_reward_risk)

    if blockers:
        note = "Hard guardrail triggered. Apply suggested sizing before any execution."
    elif risk_score >= 71:
        note = "Trade blocked by model risk. Reduce leverage/size and retry."
    elif risk_score >= 31:
        note = "Trade allowed with warning. Use smaller sizing and tighter risk controls."
    else:
        note = "Trade condition is acceptable under current guardrails."

    return SuggestedPlan(
        leverage=leverage_target,
        position_notional_usdt=position_target,
        stop_loss_price=stop_loss_target,
        take_profit_price=take_profit_target,
        note=note,
    )


def _check_blockers(
    intent: EvaluationInput, risk_per_trade_pct: float, reward_risk_ratio: float
) -> List[str]:
    trade = intent.trade
    behavior = intent.behavior
    guardrails = intent.guardrails
    blockers: List[str] = []

    if trade.entry_price <= 0:
        blockers.append("Entry price must be greater than zero.")
    if trade.account_equity_usdt <= 0:
        blockers.append("Account equity must be greater than zero.")
    if trade.position_notional_usdt <= 0:
        blockers.append("Position notional must be greater than zero.")

    if trade.symbol not in guardrails.allow_symbols:
        blockers.append(f"Symbol {trade.symbol} is outside allowlist.")
    if trade.leverage > guardrails.max_leverage:
        blockers.append(
            f"Leverage {trade.leverage:.2f} exceeds max {guardrails.max_leverage:.2f}."
        )
    if trade.position_notional_usdt / max(trade.account_equity_usdt, 1e-6) > guardrails.max_position_vs_equity:
        blockers.append("Position size is too large versus account equity.")
    if guardrails.require_stop_loss and trade.stop_loss_price is None:
        blockers.append("Stop-loss is required by guardrail but missing.")
    if trade.stop_loss_price is not None:
        if trade.side == "LONG" and trade.stop_loss_price >= trade.entry_price:
            blockers.append("For LONG, stop-loss must be below entry price.")
        if trade.side == "SHORT" and trade.stop_loss_price <= trade.entry_price:
            blockers.append("For SHORT, stop-loss must be above entry price.")
    if trade.take_profit_price is not None:
        if trade.side == "LONG" and trade.take_profit_price <= trade.entry_price:
            blockers.append("For LONG, take-profit must be above entry price.")
        if trade.side == "SHORT" and trade.take_profit_price >= trade.entry_price:
            blockers.append("For SHORT, take-profit must be below entry price.")
    if behavior.day_pnl_pct <= -guardrails.max_daily_loss_pct:
        blockers.append(
            f"Daily loss {behavior.day_pnl_pct:.2f}% breached limit -{guardrails.max_daily_loss_pct:.2f}%."
        )
    if behavior.consecutive_losses >= guardrails.max_consecutive_losses:
        blockers.append(
            f"Consecutive losses {behavior.consecutive_losses} reached cooldown threshold."
        )
    if trade.stop_loss_price is not None and risk_per_trade_pct > guardrails.max_risk_per_trade_pct:
        blockers.append(
            f"Estimated loss at stop ({risk_per_trade_pct:.2f}%) exceeds max risk per trade "
            f"{guardrails.max_risk_per_trade_pct:.2f}%."
        )
    if (
        trade.stop_loss_price is not None
        and trade.take_profit_price is not None
        and _is_meaningfully_below(reward_risk_ratio, guardrails.min_reward_risk_ratio)
    ):
        blockers.append(
            f"Reward/risk ratio {reward_risk_ratio:.2f}x is below required "
            f"{guardrails.min_reward_risk_ratio:.2f}x."
        )
    return blockers


def _to_reasons(
    metrics: Dict[str, float],
    blockers: List[str],
    risk_per_trade: float,
    reward_risk: float,
    liq_buffer: float,
    has_stop_loss: bool,
    has_take_profit: bool,
    min_reward_risk_ratio: float,
) -> List[str]:
    reasons: List[str] = []
    if blockers:
        reasons.extend(blockers)
    if metrics["leverage_risk"] >= 65:
        reasons.append("Leverage risk is elevated for current guardrail profile.")
    if metrics["volatility_risk"] >= 60:
        reasons.append("Market volatility is high; entry timing risk is elevated.")
    if metrics["concentration_risk"] >= 55:
        reasons.append("Position concentration is high relative to account equity.")
    if metrics["liquidity_risk"] >= 55:
        reasons.append("Spread/depth conditions imply material slippage risk.")
    if metrics["behavior_risk"] >= 55:
        reasons.append("Behavior pattern suggests tilt/overtrading risk.")
    if has_stop_loss and risk_per_trade >= 1.5:
        reasons.append("Stop-loss distance implies meaningful single-trade downside.")
    if not has_take_profit:
        reasons.append("No take-profit is set; payoff quality is undefined.")
    elif reward_risk > 0 and _is_meaningfully_below(reward_risk, min_reward_risk_ratio):
        reasons.append("Reward/risk ratio is below the current profile requirement.")
    if liq_buffer <= 3.5:
        reasons.append("Liquidation buffer is narrow under current leverage.")

    if not reasons:
        reasons.append("Risk profile is within acceptable range.")
    return reasons


def _weighted_score(metrics: Dict[str, float]) -> float:
    return (
        metrics["leverage_risk"] * 0.30
        + metrics["volatility_risk"] * 0.25
        + metrics["concentration_risk"] * 0.20
        + metrics["liquidity_risk"] * 0.15
        + metrics["behavior_risk"] * 0.10
    )


def _decide(risk_score: float, blockers: List[str]) -> str:
    if blockers:
        return "BLOCK"
    if risk_score > 70:
        return "BLOCK"
    if risk_score >= 31:
        return "WARN"
    return "ALLOW"


def evaluate_trade(intent: EvaluationInput) -> EvaluationResult:
    """Evaluate a trade plan and return policy decision plus suggestions."""
    metrics = {
        "leverage_risk": _score_leverage(intent.trade.leverage, intent.guardrails.max_leverage),
        "volatility_risk": _score_volatility(intent.market.volatility_24h_pct),
        "concentration_risk": _score_concentration(
            intent.trade.position_notional_usdt, intent.trade.account_equity_usdt
        ),
        "liquidity_risk": _score_liquidity(
            intent.market.bid_ask_spread_bps, intent.market.liquidity_depth_score
        ),
        "behavior_risk": _score_behavior(
            intent.behavior.consecutive_losses,
            intent.behavior.trades_last_24h,
            intent.behavior.day_pnl_pct,
        ),
    }

    risk_per_trade = _risk_per_trade_pct(intent)
    reward_risk = _reward_risk_ratio(intent)
    liq_buffer = _liquidation_buffer_pct(intent.trade.leverage)
    blockers = _check_blockers(intent, risk_per_trade, reward_risk)

    risk_score = _weighted_score(metrics)
    decision = _decide(risk_score, blockers)
    has_stop_loss = intent.trade.stop_loss_price is not None
    has_take_profit = intent.trade.take_profit_price is not None
    reasons = _to_reasons(
        metrics,
        blockers,
        risk_per_trade,
        reward_risk,
        liq_buffer,
        has_stop_loss,
        has_take_profit,
        intent.guardrails.min_reward_risk_ratio,
    )
    suggested_plan = _build_suggestions(intent, blockers, risk_score)

    metrics_enriched = dict(metrics)
    metrics_enriched["risk_per_trade_pct"] = (
        _clamp(risk_per_trade, 0.0, 100.0) if has_stop_loss else 0.0
    )
    metrics_enriched["reward_risk_ratio"] = reward_risk if has_take_profit else 0.0
    metrics_enriched["target_reward_risk_ratio"] = intent.guardrails.min_reward_risk_ratio
    metrics_enriched["liquidation_buffer_pct"] = liq_buffer

    return EvaluationResult(
        decision=decision,
        risk_score=risk_score,
        reasons=reasons,
        blockers=blockers,
        metric_breakdown=metrics_enriched,
        suggested_plan=suggested_plan,
        profile_context=intent.profile_context,
    )
