from __future__ import annotations

import unittest

from src.claw_profit_guard.engine import evaluate_trade
from src.claw_profit_guard.models import EvaluationInput


class EngineTests(unittest.TestCase):
    def test_allow_for_low_risk_trade(self) -> None:
        payload = {
            "trade": {
                "symbol": "BTCUSDT",
                "side": "LONG",
                "entry_price": 90000,
                "stop_loss_price": 89100,
                "leverage": 3,
                "position_notional_usdt": 450,
                "account_equity_usdt": 5000,
            },
            "market": {
                "volatility_24h_pct": 2.0,
                "bid_ask_spread_bps": 2,
                "liquidity_depth_score": 94,
            },
            "behavior": {
                "consecutive_losses": 0,
                "trades_last_24h": 2,
                "day_pnl_pct": 0.8,
            },
        }
        result = evaluate_trade(EvaluationInput.from_dict(payload))
        self.assertEqual(result.decision, "ALLOW")
        self.assertLessEqual(result.risk_score, 30.0)

    def test_warn_for_medium_risk_trade(self) -> None:
        payload = {
            "trade": {
                "symbol": "ETHUSDT",
                "side": "SHORT",
                "entry_price": 5200,
                "stop_loss_price": 5330,
                "leverage": 11,
                "position_notional_usdt": 1400,
                "account_equity_usdt": 2600,
            },
            "market": {
                "volatility_24h_pct": 6.1,
                "bid_ask_spread_bps": 9,
                "liquidity_depth_score": 70,
            },
            "behavior": {
                "consecutive_losses": 1,
                "trades_last_24h": 12,
                "day_pnl_pct": -2.5,
            },
        }
        result = evaluate_trade(EvaluationInput.from_dict(payload))
        self.assertEqual(result.decision, "WARN")
        self.assertGreaterEqual(result.risk_score, 31.0)
        self.assertLessEqual(result.risk_score, 70.0)

    def test_block_on_guardrail(self) -> None:
        payload = {
            "trade": {
                "symbol": "1000PEPEUSDT",
                "side": "LONG",
                "entry_price": 0.021,
                "stop_loss_price": 0.0208,
                "leverage": 40,
                "position_notional_usdt": 2500,
                "account_equity_usdt": 1200,
            },
            "market": {
                "volatility_24h_pct": 16.0,
                "bid_ask_spread_bps": 28,
                "liquidity_depth_score": 35,
            },
            "behavior": {
                "consecutive_losses": 4,
                "trades_last_24h": 24,
                "day_pnl_pct": -10.4,
            },
        }
        result = evaluate_trade(EvaluationInput.from_dict(payload))
        self.assertEqual(result.decision, "BLOCK")
        self.assertTrue(result.blockers)

    def test_apply_suggested_plan_removes_risk_per_trade_blocker(self) -> None:
        payload = {
            "trade": {
                "symbol": "BTCUSDT",
                "side": "LONG",
                "entry_price": 90000,
                "stop_loss_price": 89100,
                "leverage": 8,
                "position_notional_usdt": 1200,
                "account_equity_usdt": 1000,
            },
            "market": {
                "volatility_24h_pct": 4.0,
                "bid_ask_spread_bps": 5,
                "liquidity_depth_score": 80,
            },
            "behavior": {
                "consecutive_losses": 1,
                "trades_last_24h": 8,
                "day_pnl_pct": -1.5,
            },
            "guardrails": {
                "max_leverage": 10,
                "max_position_vs_equity": 2.0,
                "max_daily_loss_pct": 8.0,
                "max_consecutive_losses": 5,
                "require_stop_loss": True,
                "max_risk_per_trade_pct": 0.8,
                "allow_symbols": ["BTCUSDT"],
            },
        }
        first = evaluate_trade(EvaluationInput.from_dict(payload))
        self.assertTrue(
            any("Estimated loss at stop" in b for b in first.blockers),
            "Initial trade should violate max_risk_per_trade.",
        )

        payload["trade"]["leverage"] = first.suggested_plan.leverage
        payload["trade"]["position_notional_usdt"] = first.suggested_plan.position_notional_usdt
        payload["trade"]["stop_loss_price"] = first.suggested_plan.stop_loss_price
        second = evaluate_trade(EvaluationInput.from_dict(payload))
        self.assertFalse(
            any("Estimated loss at stop" in b for b in second.blockers),
            "Suggested plan should resolve risk-per-trade blocker.",
        )

    def test_low_reward_risk_ratio_is_blocked_and_suggestion_repairs_it(self) -> None:
        payload = {
            "trade": {
                "symbol": "BNBUSDT",
                "side": "LONG",
                "entry_price": 640,
                "stop_loss_price": 630,
                "take_profit_price": 650,
                "leverage": 5,
                "position_notional_usdt": 500,
                "account_equity_usdt": 2000,
            },
            "market": {
                "volatility_24h_pct": 4.2,
                "bid_ask_spread_bps": 4,
                "liquidity_depth_score": 86,
            },
            "behavior": {
                "consecutive_losses": 0,
                "trades_last_24h": 4,
                "day_pnl_pct": 0.5,
            },
            "guardrails": {
                "max_leverage": 10,
                "max_position_vs_equity": 1.5,
                "max_daily_loss_pct": 8.0,
                "max_consecutive_losses": 5,
                "require_stop_loss": True,
                "max_risk_per_trade_pct": 2.0,
                "min_reward_risk_ratio": 1.8,
                "allow_symbols": ["BNBUSDT"],
            },
        }
        first = evaluate_trade(EvaluationInput.from_dict(payload))
        self.assertTrue(
            any("Reward/risk ratio" in b for b in first.blockers),
            "Initial trade should violate minimum reward/risk ratio.",
        )

        payload["trade"]["take_profit_price"] = first.suggested_plan.take_profit_price
        second = evaluate_trade(EvaluationInput.from_dict(payload))
        self.assertFalse(
            any("Reward/risk ratio" in b for b in second.blockers),
            "Suggested take-profit should repair reward/risk blocker.",
        )

    def test_reward_risk_equal_to_threshold_is_not_blocked_by_float_precision(self) -> None:
        payload = {
            "profile": "conservative",
            "trade": {
                "symbol": "ETHUSDT",
                "side": "LONG",
                "entry_price": 1980.13,
                "stop_loss_price": 1963.3,
                "take_profit_price": 2013.79,
                "leverage": 1,
                "position_notional_usdt": 62.42,
                "account_equity_usdt": 86.69,
            },
            "market": {
                "volatility_24h_pct": 1.44,
                "bid_ask_spread_bps": 0.05,
                "liquidity_depth_score": 33.31,
            },
            "behavior": {
                "consecutive_losses": 0,
                "trades_last_24h": 0,
                "day_pnl_pct": 0.0,
            },
        }
        result = evaluate_trade(EvaluationInput.from_dict(payload))
        self.assertEqual(result.decision, "ALLOW")
        self.assertFalse(
            any("Reward/risk ratio" in b for b in result.blockers),
            "Exact threshold should pass even if float math produces 1.9999999999.",
        )


if __name__ == "__main__":
    unittest.main()
