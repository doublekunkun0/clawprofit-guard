from __future__ import annotations

import unittest

from src.claw_profit_guard.engine import evaluate_trade
from src.claw_profit_guard.models import EvaluationInput
from src.claw_profit_guard.risk_profile import build_symbol_catalog, recommend_profile


class ProfileTests(unittest.TestCase):
    def test_profile_recommendation_outputs_guardrails(self) -> None:
        payload = {
            "quiz": {
                "experience_level": "intermediate",
                "risk_tolerance": "medium",
                "leverage_preference": "medium",
                "stop_loss_discipline": "always",
                "revenge_tendency": "sometimes",
                "trading_frequency": "medium",
                "max_drawdown_comfort_pct": 6,
            },
            "behavior": {
                "consecutive_losses": 1,
                "trades_last_24h": 8,
                "day_pnl_pct": -1.0,
            },
        }
        result = recommend_profile(payload)
        self.assertIn(result.profile, {"conservative", "balanced", "aggressive"})
        self.assertGreater(result.guardrails.max_leverage, 0)
        self.assertGreaterEqual(result.guardrails.min_reward_risk_ratio, 1.0)
        self.assertTrue(result.strengths)
        self.assertTrue(result.coaching)

    def test_symbol_catalog_is_limited_to_bnb_btc_eth(self) -> None:
        catalog = build_symbol_catalog()
        self.assertEqual([item["symbol"] for item in catalog], ["BNBUSDT", "BTCUSDT", "ETHUSDT"])

    def test_aggressive_selection_is_tightened_on_bad_behavior(self) -> None:
        payload = {
            "selected_profile": "aggressive",
            "quiz": {
                "experience_level": "advanced",
                "risk_tolerance": "high",
                "leverage_preference": "high",
                "stop_loss_discipline": "rarely",
                "revenge_tendency": "often",
                "trading_frequency": "high",
                "max_drawdown_comfort_pct": 15,
            },
            "behavior": {
                "consecutive_losses": 5,
                "trades_last_24h": 25,
                "day_pnl_pct": -9.0,
            },
        }
        result = recommend_profile(payload)
        self.assertIn(result.profile, {"conservative", "balanced"})
        self.assertTrue(result.auto_adjustments)

    def test_evaluation_accepts_profile_string(self) -> None:
        payload = {
            "trade": {
                "symbol": "BTCUSDT",
                "side": "LONG",
                "entry_price": 91000,
                "stop_loss_price": 90000,
                "leverage": 9,
                "position_notional_usdt": 1000,
                "account_equity_usdt": 2500,
            },
            "market": {
                "volatility_24h_pct": 3.5,
                "bid_ask_spread_bps": 3,
                "liquidity_depth_score": 85,
            },
            "behavior": {
                "consecutive_losses": 0,
                "trades_last_24h": 4,
                "day_pnl_pct": 0.4,
            },
            "profile": "balanced",
        }
        data = EvaluationInput.from_dict(payload)
        self.assertEqual(data.guardrails.max_leverage, 10.0)
        result = evaluate_trade(data)
        self.assertIn("profile_context", result.to_dict())

    def test_evaluation_accepts_quiz_profile(self) -> None:
        payload = {
            "trade": {
                "symbol": "ETHUSDT",
                "side": "LONG",
                "entry_price": 5200,
                "stop_loss_price": 5100,
                "leverage": 14,
                "position_notional_usdt": 1800,
                "account_equity_usdt": 1800,
            },
            "market": {
                "volatility_24h_pct": 9.0,
                "bid_ask_spread_bps": 8,
                "liquidity_depth_score": 72,
            },
            "behavior": {
                "consecutive_losses": 3,
                "trades_last_24h": 19,
                "day_pnl_pct": -4.5,
            },
            "quiz": {
                "experience_level": "intermediate",
                "risk_tolerance": "high",
                "leverage_preference": "high",
                "stop_loss_discipline": "sometimes",
                "revenge_tendency": "sometimes",
                "trading_frequency": "high",
                "max_drawdown_comfort_pct": 10,
            },
        }
        data = EvaluationInput.from_dict(payload)
        self.assertLessEqual(data.guardrails.max_leverage, 15.0)
        self.assertIn(data.profile_context.get("profile"), {"conservative", "balanced", "aggressive"})

    def test_default_path_applies_system_hard_limits(self) -> None:
        payload = {
            "trade": {
                "symbol": "BTCUSDT",
                "side": "LONG",
                "entry_price": 90000,
                "stop_loss_price": 89000,
                "leverage": 14,
                "position_notional_usdt": 1200,
                "account_equity_usdt": 3000,
            },
            "market": {},
            "behavior": {},
        }
        data = EvaluationInput.from_dict(payload)
        self.assertEqual(data.guardrails.max_leverage, 15.0)

    def test_require_stop_loss_string_false_is_parsed_and_enforced_correctly(self) -> None:
        payload = {
            "trade": {
                "symbol": "BTCUSDT",
                "side": "LONG",
                "entry_price": 90000,
                "stop_loss_price": None,
                "leverage": 3,
                "position_notional_usdt": 300,
                "account_equity_usdt": 3000,
            },
            "market": {
                "volatility_24h_pct": 2.5,
                "bid_ask_spread_bps": 3,
                "liquidity_depth_score": 90,
            },
            "behavior": {
                "consecutive_losses": 0,
                "trades_last_24h": 2,
                "day_pnl_pct": 0.2,
            },
            "guardrails": {
                "require_stop_loss": "false",
                "max_leverage": 10,
                "max_position_vs_equity": 1.5,
                "max_daily_loss_pct": 8,
                "max_consecutive_losses": 5,
                "max_risk_per_trade_pct": 1.0,
                "allow_symbols": ["BTCUSDT"],
            },
        }
        data = EvaluationInput.from_dict(payload)
        self.assertFalse(data.guardrails.require_stop_loss)
        result = evaluate_trade(data)
        blocker_text = " | ".join(result.blockers)
        self.assertNotIn("Stop-loss is required by guardrail but missing.", blocker_text)
        self.assertNotIn("Estimated loss at stop", blocker_text)


if __name__ == "__main__":
    unittest.main()
