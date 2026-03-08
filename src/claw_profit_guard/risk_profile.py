"""Risk profile recommendation and dynamic guardrail mapping."""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

from .models import BehaviorContext, GuardrailConfig, ProfileRecommendation


PROFILE_ORDER = ["conservative", "balanced", "aggressive"]
SYMBOL_ORDER = ["BNBUSDT", "BTCUSDT", "ETHUSDT"]
SYMBOL_LABELS: Dict[str, str] = {
    "BNBUSDT": "BNB",
    "BTCUSDT": "BTC",
    "ETHUSDT": "ETH",
}

PROFILE_PRESETS: Dict[str, Dict[str, Any]] = {
    "conservative": {
        "max_leverage": 5,
        "max_position_vs_equity": 0.9,
        "max_daily_loss_pct": 3,
        "max_consecutive_losses": 3,
        "require_stop_loss": True,
        "max_risk_per_trade_pct": 0.8,
        "min_reward_risk_ratio": 2.0,
        "allow_symbols": ["BTCUSDT", "ETHUSDT", "BNBUSDT"],
    },
    "balanced": {
        "max_leverage": 10,
        "max_position_vs_equity": 1.2,
        "max_daily_loss_pct": 5,
        "max_consecutive_losses": 4,
        "require_stop_loss": True,
        "max_risk_per_trade_pct": 1.5,
        "min_reward_risk_ratio": 1.8,
        "allow_symbols": ["BTCUSDT", "ETHUSDT", "BNBUSDT"],
    },
    "aggressive": {
        "max_leverage": 15,
        "max_position_vs_equity": 1.5,
        "max_daily_loss_pct": 8,
        "max_consecutive_losses": 5,
        "require_stop_loss": True,
        "max_risk_per_trade_pct": 2.0,
        "min_reward_risk_ratio": 1.5,
        "allow_symbols": [
            "BTCUSDT",
            "ETHUSDT",
            "BNBUSDT",
        ],
    },
}

SYSTEM_HARD_LIMITS: Dict[str, Any] = {
    "max_leverage": 15.0,
    "max_position_vs_equity": 1.8,
    "max_daily_loss_pct": 8.0,
    "max_consecutive_losses": 5,
    "max_risk_per_trade_pct": 2.0,
}


def _clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def _normalize_profile_name(name: str) -> str:
    value = str(name).strip().lower()
    if value not in PROFILE_PRESETS:
        raise ValueError(
            f"Unsupported profile '{name}'. Use one of: {', '.join(PROFILE_ORDER)}."
        )
    return value


def _profile_index(name: str) -> int:
    return PROFILE_ORDER.index(name)


def _stricter_profile(left: str, right: str) -> str:
    # Lower index means stricter risk profile.
    return PROFILE_ORDER[min(_profile_index(left), _profile_index(right))]


def _score_quiz(quiz: Dict[str, Any]) -> float:
    def pick(mapping: Dict[str, float], key: str, fallback: float = 50.0) -> float:
        value = str(quiz.get(key, "")).strip().lower()
        return mapping.get(value, fallback)

    experience = pick({"beginner": 30, "intermediate": 55, "advanced": 75}, "experience_level")
    tolerance = pick({"low": 25, "medium": 55, "high": 85}, "risk_tolerance")
    leverage_pref = pick({"low": 20, "medium": 55, "high": 85}, "leverage_preference")
    stop_loss = pick({"always": 25, "sometimes": 55, "rarely": 85}, "stop_loss_discipline")
    revenge = pick({"never": 20, "sometimes": 60, "often": 90}, "revenge_tendency")
    frequency = pick({"low": 25, "medium": 55, "high": 80}, "trading_frequency")

    drawdown_value = quiz.get("max_drawdown_comfort_pct", 6)
    try:
        drawdown_pct = float(drawdown_value)
    except (TypeError, ValueError):
        drawdown_pct = 6.0
    drawdown_score = _clamp((drawdown_pct / 15.0) * 100.0, 0.0, 100.0)

    return (
        experience
        + tolerance
        + leverage_pref
        + stop_loss
        + revenge
        + frequency
        + drawdown_score
    ) / 7.0


def build_symbol_catalog() -> List[Dict[str, Any]]:
    profiles_by_symbol: Dict[str, List[str]] = {}
    for profile_name, preset in PROFILE_PRESETS.items():
        for raw_symbol in preset.get("allow_symbols", []):
            symbol = str(raw_symbol).upper()
            profiles_by_symbol.setdefault(symbol, []).append(profile_name)

    ordered_symbols = [symbol for symbol in SYMBOL_ORDER if symbol in profiles_by_symbol]
    ordered_symbols.extend(
        sorted(symbol for symbol in profiles_by_symbol if symbol not in set(ordered_symbols))
    )

    catalog: List[Dict[str, Any]] = []
    for symbol in ordered_symbols:
        catalog.append(
            {
                "symbol": symbol,
                "label": SYMBOL_LABELS.get(symbol, symbol.removesuffix("USDT")),
                "profiles": profiles_by_symbol[symbol],
            }
        )
    return catalog


def _behavior_adjustment(behavior: BehaviorContext) -> Tuple[float, float]:
    penalty = 0.0
    bonus = 0.0

    penalty += _clamp(behavior.consecutive_losses * 5.0, 0.0, 25.0)
    penalty += _clamp(max(0.0, behavior.trades_last_24h - 6.0) * 1.2, 0.0, 20.0)
    penalty += _clamp(max(0.0, -behavior.day_pnl_pct) * 3.0, 0.0, 30.0)

    if behavior.consecutive_losses == 0:
        bonus += 3.0
    if behavior.trades_last_24h <= 5:
        bonus += 3.0
    if behavior.day_pnl_pct >= 0:
        bonus += 2.0

    return penalty, bonus


def _profile_from_score(score: float) -> str:
    if score <= 38:
        return "conservative"
    if score <= 68:
        return "balanced"
    return "aggressive"


def _auto_downgrade(profile: str, behavior: BehaviorContext) -> Tuple[str, List[str]]:
    adjustments: List[str] = []
    current = profile

    if behavior.day_pnl_pct <= -12 or behavior.consecutive_losses >= 6:
        if current != "conservative":
            current = "conservative"
            adjustments.append("Severe drawdown detected, forced to conservative profile.")
        return current, adjustments

    if behavior.day_pnl_pct <= -8 or behavior.consecutive_losses >= 4:
        stricter = _stricter_profile(current, "balanced")
        if stricter != current:
            current = stricter
            adjustments.append("Cooling mode activated due to losses, profile tightened by one level.")

    if behavior.trades_last_24h >= 30 and behavior.day_pnl_pct < 0:
        stricter = _stricter_profile(current, "balanced")
        if stricter != current:
            current = stricter
            adjustments.append("Overtrading under negative PnL detected, profile tightened.")

    return current, adjustments


def _enforce_hard_limits(cfg: GuardrailConfig) -> GuardrailConfig:
    cfg.max_leverage = min(cfg.max_leverage, SYSTEM_HARD_LIMITS["max_leverage"])
    cfg.max_position_vs_equity = min(
        cfg.max_position_vs_equity, SYSTEM_HARD_LIMITS["max_position_vs_equity"]
    )
    cfg.max_daily_loss_pct = min(cfg.max_daily_loss_pct, SYSTEM_HARD_LIMITS["max_daily_loss_pct"])
    cfg.max_consecutive_losses = min(
        cfg.max_consecutive_losses, SYSTEM_HARD_LIMITS["max_consecutive_losses"]
    )
    cfg.max_risk_per_trade_pct = min(
        cfg.max_risk_per_trade_pct, SYSTEM_HARD_LIMITS["max_risk_per_trade_pct"]
    )
    cfg.max_leverage = max(1.0, cfg.max_leverage)
    cfg.max_position_vs_equity = max(0.3, cfg.max_position_vs_equity)
    cfg.max_daily_loss_pct = max(1.0, cfg.max_daily_loss_pct)
    cfg.max_consecutive_losses = max(1, cfg.max_consecutive_losses)
    cfg.max_risk_per_trade_pct = max(0.2, cfg.max_risk_per_trade_pct)
    cfg.min_reward_risk_ratio = _clamp(cfg.min_reward_risk_ratio, 1.0, 4.0)
    return cfg


def enforce_system_guardrail_limits(cfg: GuardrailConfig) -> GuardrailConfig:
    """Public wrapper used when guardrails are provided directly by caller."""
    return _enforce_hard_limits(cfg)


def _guardrails_for_profile(profile: str, allow_symbols: List[str] | None = None) -> GuardrailConfig:
    cfg = GuardrailConfig.from_dict(PROFILE_PRESETS[profile])
    if allow_symbols:
        cfg.allow_symbols = [str(s).upper() for s in allow_symbols]
    return _enforce_hard_limits(cfg)


def _apply_overrides(cfg: GuardrailConfig, overrides: Dict[str, Any]) -> GuardrailConfig:
    if not overrides:
        return cfg
    merged = cfg.to_dict()
    merged.update(overrides)
    return _enforce_hard_limits(GuardrailConfig.from_dict(merged))


def _build_strengths(quiz: Dict[str, Any], behavior: BehaviorContext) -> List[str]:
    strengths: List[str] = []
    if str(quiz.get("stop_loss_discipline", "")).strip().lower() == "always":
        strengths.append("Strong stop-loss discipline.")
    if behavior.consecutive_losses == 0:
        strengths.append("No recent loss streak detected.")
    if behavior.trades_last_24h <= 5:
        strengths.append("Trading frequency is controlled.")
    if behavior.day_pnl_pct >= 0:
        strengths.append("Recent daily PnL is stable or positive.")
    if not strengths:
        strengths.append("You are actively engaging with risk controls.")
    return strengths


def _build_issues(quiz: Dict[str, Any], behavior: BehaviorContext) -> List[str]:
    issues: List[str] = []
    if str(quiz.get("revenge_tendency", "")).strip().lower() == "often":
        issues.append("Revenge-trading tendency is high.")
    if str(quiz.get("stop_loss_discipline", "")).strip().lower() in {"rarely", "sometimes"}:
        issues.append("Stop-loss execution discipline is inconsistent.")
    if behavior.consecutive_losses >= 3:
        issues.append("Loss streak risk is elevated.")
    if behavior.trades_last_24h >= 18:
        issues.append("Overtrading pattern detected in last 24h.")
    if behavior.day_pnl_pct <= -5:
        issues.append("Current daily drawdown is significant.")
    if not issues:
        issues.append("No critical behavior risk found.")
    return issues


def _build_coaching(issues: List[str]) -> List[str]:
    coaching: List[str] = []
    for issue in issues:
        if "Revenge-trading" in issue:
            coaching.append("After two losses, enforce a 30-minute cooldown before new entries.")
        elif "Stop-loss execution" in issue:
            coaching.append("Convert every entry into a bracket order with mandatory stop-loss.")
        elif "Loss streak" in issue:
            coaching.append("Cut position size by 50% until one green day is recovered.")
        elif "Overtrading" in issue:
            coaching.append("Set a hard cap on intraday trades and disable entries after cap is hit.")
        elif "drawdown" in issue:
            coaching.append("Switch to capital protection mode and only take A-grade setups.")
    if not coaching:
        coaching.append("Continue using the current guardrails and review weekly performance.")
    return coaching[:4]


def recommend_profile(payload: Dict[str, Any]) -> ProfileRecommendation:
    """Recommend profile from questionnaire + behavior calibration."""
    quiz_raw = payload.get("quiz", {})
    quiz = quiz_raw if isinstance(quiz_raw, dict) else {}
    behavior = BehaviorContext.from_dict(payload.get("behavior", {}))
    preferences = payload.get("preferences", {}) if isinstance(payload.get("preferences"), dict) else {}
    allow_symbols = preferences.get("allow_symbols")
    selected_profile_raw = payload.get("selected_profile")
    selected_profile = (
        _normalize_profile_name(selected_profile_raw)
        if selected_profile_raw is not None
        else None
    )

    baseline_subjective = {
        "conservative": 25.0,
        "balanced": 55.0,
        "aggressive": 82.0,
    }
    if quiz:
        subjective_score = _score_quiz(quiz)
    elif selected_profile:
        subjective_score = baseline_subjective[selected_profile]
    else:
        subjective_score = 50.0

    behavior_penalty, behavior_bonus = _behavior_adjustment(behavior)
    raw_score = _clamp(subjective_score - behavior_penalty + behavior_bonus, 0.0, 100.0)

    if quiz:
        computed_profile = _profile_from_score(raw_score)
    elif selected_profile:
        computed_profile = selected_profile
    else:
        computed_profile = _profile_from_score(raw_score)
    computed_profile, auto_adjustments = _auto_downgrade(computed_profile, behavior)

    final_profile = computed_profile
    if selected_profile and quiz:
        stricter = _stricter_profile(selected_profile, computed_profile)
        final_profile = stricter
        if stricter != selected_profile:
            auto_adjustments.append(
                f"Selected profile '{selected_profile}' tightened to '{stricter}' by risk checks."
            )
        else:
            auto_adjustments.append(f"Selected profile '{selected_profile}' accepted.")

    guardrails = _guardrails_for_profile(final_profile, allow_symbols=allow_symbols)
    guardrails = _apply_overrides(guardrails, payload.get("guardrail_overrides", {}))

    strengths = _build_strengths(quiz, behavior)
    issues = _build_issues(quiz, behavior)
    coaching = _build_coaching(issues)

    return ProfileRecommendation(
        profile=final_profile,
        profile_score=raw_score,
        subjective_score=subjective_score,
        behavior_penalty=behavior_penalty,
        behavior_bonus=behavior_bonus,
        strengths=strengths,
        issues=issues,
        coaching=coaching,
        auto_adjustments=auto_adjustments,
        guardrails=guardrails,
    )


def derive_guardrails_from_payload(
    payload: Dict[str, Any], behavior: BehaviorContext
) -> Tuple[GuardrailConfig, Dict[str, Any]]:
    """Derive guardrails from profile/quiz payload when explicit guardrails are absent."""
    profile_field = payload.get("profile")
    root_quiz = payload.get("quiz", {})
    selected_profile: str | None = None
    quiz: Dict[str, Any] = root_quiz if isinstance(root_quiz, dict) else {}
    preferences = payload.get("preferences", {}) if isinstance(payload.get("preferences"), dict) else {}
    guardrail_overrides = (
        payload.get("guardrail_overrides", {})
        if isinstance(payload.get("guardrail_overrides"), dict)
        else {}
    )

    if isinstance(profile_field, str):
        selected_profile = _normalize_profile_name(profile_field)
    elif isinstance(profile_field, dict):
        if isinstance(profile_field.get("name"), str):
            selected_profile = _normalize_profile_name(profile_field["name"])
        if not quiz and isinstance(profile_field.get("quiz"), dict):
            quiz = profile_field["quiz"]
        if not preferences and isinstance(profile_field.get("preferences"), dict):
            preferences = profile_field.get("preferences", {})
        if isinstance(profile_field.get("guardrail_overrides"), dict):
            merged = dict(profile_field.get("guardrail_overrides", {}))
            merged.update(guardrail_overrides)
            guardrail_overrides = merged

    if selected_profile is None and not quiz:
        return _enforce_hard_limits(GuardrailConfig.from_dict({})), {}

    recommendation = recommend_profile(
        {
            "quiz": quiz,
            "behavior": behavior.__dict__,
            "preferences": preferences,
            "selected_profile": selected_profile,
            "guardrail_overrides": guardrail_overrides,
        }
    )
    context = {
        "mode": "profile_assisted",
        "profile": recommendation.profile,
        "profile_score": round(recommendation.profile_score, 2),
        "auto_adjustments": recommendation.auto_adjustments,
    }
    return recommendation.guardrails, context
