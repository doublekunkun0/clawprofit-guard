# ClawProfit Guard API Contract v1

Base URL (local demo):

`http://127.0.0.1:8080`

## GET /health

Response `200`:

```json
{
  "status": "ok",
  "service": "claw-profit-guard"
}
```

## POST /v1/evaluate

Purpose:

- Evaluate a planned trade before execution.
- Supports three modes:
  - explicit `guardrails`
  - direct `profile` (`conservative|balanced|aggressive`)
  - questionnaire (`quiz`) + behavior auto-calibration

Request:

```json
{
  "trade": {
    "symbol": "BTCUSDT",
    "side": "LONG",
    "entry_price": 91500,
    "stop_loss_price": 90000,
    "take_profit_price": 94500,
    "leverage": 20,
    "position_notional_usdt": 2500,
    "account_equity_usdt": 1800
  },
  "market": {
    "volatility_24h_pct": 8.6,
    "bid_ask_spread_bps": 11,
    "liquidity_depth_score": 62
  },
  "behavior": {
    "consecutive_losses": 3,
    "trades_last_24h": 18,
    "day_pnl_pct": -6.8
  },
  "guardrails": {
    "max_leverage": 20,
    "max_position_vs_equity": 1.5,
    "max_daily_loss_pct": 8,
    "max_consecutive_losses": 4,
    "require_stop_loss": true,
    "max_risk_per_trade_pct": 2.0,
    "min_reward_risk_ratio": 1.8,
    "allow_symbols": [
      "BTCUSDT",
      "ETHUSDT",
      "BNBUSDT"
    ]
  }
}
```

Profile-based request (no manual guardrails):

```json
{
  "profile": "balanced",
  "trade": {
    "symbol": "BTCUSDT",
    "side": "LONG",
    "entry_price": 91500,
    "stop_loss_price": 90000,
    "leverage": 12,
    "position_notional_usdt": 2500,
    "account_equity_usdt": 1800
  },
  "market": {
    "volatility_24h_pct": 8.6,
    "bid_ask_spread_bps": 11,
    "liquidity_depth_score": 62
  },
  "behavior": {
    "consecutive_losses": 3,
    "trades_last_24h": 18,
    "day_pnl_pct": -6.8
  }
}
```

Response `200`:

```json
{
  "decision": "WARN",
  "risk_score": 57.43,
  "reasons": [
    "Leverage risk is elevated for current guardrail profile.",
    "Position concentration is high relative to account equity."
  ],
  "blockers": [],
  "metric_breakdown": {
    "leverage_risk": 82.2,
    "volatility_risk": 71.67,
    "concentration_risk": 69.44,
    "liquidity_risk": 41.4,
    "behavior_risk": 48.0,
    "risk_per_trade_pct": 1.82,
    "reward_risk_ratio": 1.24,
    "target_reward_risk_ratio": 1.8,
    "liquidation_buffer_pct": 4.25
  },
  "suggested_plan": {
    "leverage": 11.0,
    "position_notional_usdt": 2160.0,
    "stop_loss_price": 90000.0,
    "take_profit_price": 94500.0,
    "note": "Trade allowed with warning. Use smaller sizing and tighter risk controls."
  },
  "profile_context": {
    "mode": "profile_assisted",
    "profile": "balanced",
    "profile_score": 56.2,
    "auto_adjustments": []
  }
}
```

Validation errors:

- `400` with `{"error": "..."}` for malformed JSON or missing fields.

## POST /v1/profile/recommend

Purpose:

- Recommend risk profile and dynamic guardrails based on questionnaire and behavior.

Request:

```json
{
  "quiz": {
    "experience_level": "intermediate",
    "risk_tolerance": "medium",
    "leverage_preference": "medium",
    "stop_loss_discipline": "always",
    "revenge_tendency": "sometimes",
    "trading_frequency": "medium",
    "max_drawdown_comfort_pct": 6
  },
  "behavior": {
    "consecutive_losses": 1,
    "trades_last_24h": 8,
    "day_pnl_pct": -1.0
  },
  "selected_profile": "balanced",
  "preferences": {
    "allow_symbols": [
      "BTCUSDT",
      "ETHUSDT",
      "BNBUSDT"
    ]
  }
}
```

Response `200`:

```json
{
  "profile": "balanced",
  "profile_score": 53.4,
  "subjective_score": 58.2,
  "behavior_penalty": 12.8,
  "behavior_bonus": 8.0,
  "strengths": [
    "Strong stop-loss discipline."
  ],
  "issues": [
    "Stop-loss execution discipline is inconsistent."
  ],
  "coaching": [
    "Convert every entry into a bracket order with mandatory stop-loss."
  ],
  "auto_adjustments": [],
  "guardrails": {
    "max_leverage": 10.0,
    "max_position_vs_equity": 1.2,
    "max_daily_loss_pct": 5.0,
    "max_consecutive_losses": 4,
    "require_stop_loss": true,
    "max_risk_per_trade_pct": 1.5,
    "min_reward_risk_ratio": 1.8,
    "allow_symbols": [
      "BTCUSDT",
      "ETHUSDT",
      "BNBUSDT"
    ]
  }
}
```

## Field Notes

- `liquidity_depth_score` range recommendation: `0-100`.
- `day_pnl_pct` uses signed percent, e.g. `-3.5` for daily drawdown.
- `guardrails` is optional; defaults are applied if omitted.
- Even with direct `guardrails`, system hard limits are enforced (max leverage 15, max daily loss 8%, max risk per trade 2%).

## GET /v1/binance/market-snapshot

Purpose:

- Pull Binance USD-M Futures market data for `BNB/BTC/ETH` style contest walkthroughs.
- Returns a live futures snapshot when network is available.
- Falls back to local presets if Binance Futures data is unavailable.

Example response:

```json
{
  "symbol": "BNBUSDT",
  "side": "LONG",
  "profile": "balanced",
  "live": true,
  "source": "binance_futures_live",
  "exchange_context": {
    "venue": "binance",
    "mode": "live",
    "product": "usd_m_futures"
  },
  "warning": null,
  "market": {
    "last_price": 618.8,
    "weighted_avg_price": 620.11,
    "bid_price": 618.79,
    "ask_price": 618.8,
    "volatility_24h_pct": 1.32,
    "bid_ask_spread_bps": 0.0,
    "liquidity_depth_score": 38.4
  },
  "suggested_trade": {
    "entry_price": 618.8,
    "stop_loss_price": 611.68,
    "take_profit_price": 631.61,
    "target_reward_risk_ratio": 1.8
  }
}
```

## GET /v1/binance/account-snapshot

Purpose:

- Pull Binance USD-M Futures wallet balances, open positions, open orders, and recent tracked behavior.
- Derive account-level behavior context for the risk agent.
- Falls back to local demo context when credentials are missing or the network is unavailable.

Example response:

```json
{
  "symbol": "BNBUSDT",
  "profile": "balanced",
  "live": true,
  "connected": true,
  "source": "binance_futures_live",
  "exchange_context": {
    "venue": "binance",
    "mode": "live",
    "product": "usd_m_futures"
  },
  "warning": null,
  "account": {
    "estimated_equity_usdt": 250.4,
    "wallet_balance_usdt": 241.76,
    "available_usdt": 191.57,
    "locked_usdt": 0.0,
    "open_orders_count": 1,
    "open_positions": [
      {
        "symbol": "BNBUSDT",
        "position_side": "LONG",
        "quantity": 0.28,
        "entry_price": 614.07,
        "mark_price": 616.98,
        "notional_usdt": 172.75,
        "initial_margin": 57.32,
        "unrealized_pnl_usdt": 0.81
      }
    ],
    "tracked_symbols": ["BNBUSDT", "BTCUSDT", "ETHUSDT"]
  },
  "behavior": {
    "trades_last_24h": 14,
    "consecutive_losses": 0,
    "day_pnl_pct": 0.42,
    "realized_pnl_24h_usdt": 1.06
  },
  "auto_fill": {
    "account_equity_usdt": 241.76,
    "trades_last_24h": 14,
    "consecutive_losses": 0,
    "day_pnl_pct": 0.42
  },
  "agent_context": {
    "behavior_status": "stable",
    "suggested_position_cap_usdt": 217.58,
    "risk_budget_usdt": 3.63
  },
  "briefing": [
    "Connected to Binance USD-M Futures live account context.",
    "Wallet balance 241.76 USDT, available 191.57 USDT.",
    "Recent activity: 14 trades in 24h, day PnL 0.42%, no current loss streak.",
    "Under balanced profile, suggested max notional is 217.58 USDT and per-trade risk budget is 3.63 USDT."
  ]
}
```

## POST /v1/binance/demo-order-test

Purpose:

- Build a Binance USD-M Futures order preview from current trade inputs.
- Validate execution readiness before the user sends a real order.
- Return exchange-aligned quantity, minimums, required initial margin, and protection-order preview.
- The endpoint name remains `/v1/binance/demo-order-test` for backward compatibility.

Example response:

```json
{
  "ok": true,
  "status": "validated",
  "mode": "binance_futures_live",
  "message": "Binance USD-M Futures API accepted the test order.",
  "preview": {
    "symbol": "BNBUSDT",
    "intent_side": "LONG",
    "side": "BUY",
    "order_side": "BUY",
    "type": "MARKET",
    "quantity": "0.28",
    "requested_entry_price": "614.28",
    "requested_notional_usdt": "173.83",
    "requested_margin_type": "CROSSED",
    "requested_leverage": 3,
    "required_initial_margin_usdt": "57.94",
    "estimated_execution_notional_usdt": "171.94",
    "exchange_minimums": {
      "minimum_executable_qty": "0.01",
      "minimum_executable_notional_usdt": "6.14"
    }
  },
  "exchange_context": {
    "venue": "binance",
    "mode": "live",
    "product": "usd_m_futures"
  },
  "credentials": {
    "configured": true,
    "has_api_key": true,
    "has_secret_key": true
  }
}
```
