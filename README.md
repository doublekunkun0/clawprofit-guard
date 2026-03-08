# ClawProfit Guard | 龙虾合约风控官

Language:

- English: `README.md`
- 中文版: [README.zh-CN.md](./README.zh-CN.md)

中文速览：

- 这是一个面向 `Binance USD-M Futures` 的交易前 AI 风控 Agent
- 核心闭环：`建档 -> 评估 -> 校验 -> 执行 -> 保护 -> 跟踪`
- 核心价值：`先防可避免亏损，再追求收益`
- 本地演示入口：[http://127.0.0.1:8080/demo](http://127.0.0.1:8080/demo)
- 正式部署入口：[Render Blueprint](https://dashboard.render.com/blueprint/new?repo=https://github.com/doublekunkun0/clawprofit-guard)

ClawProfit Guard is a Binance-focused pre-trade AI risk agent for USD-M Futures.
It helps users do one thing well:

1. Build a risk profile from adaptive questions plus recent account behavior.
2. Evaluate a planned trade before execution.
3. Check exchange readiness.
4. Open a position only after guardrails pass, then place stop-loss and take-profit protection orders.

This repo is designed for contest-style demos: one screen shows the full loop from `profile -> evaluate -> check -> execute -> track -> close`.

## What Makes It Competitive

- Adaptive risk-profile wizard with real account behavior calibration
- Binance USD-M Futures market sync with safe local fallback
- Binance USD-M Futures account sync with safe local fallback
- Pre-trade decision engine returning `ALLOW`, `WARN`, or `BLOCK`
- Auto-repair plan for leverage, size, stop-loss, and take-profit
- Futures order-readiness check before execution
- Live limit-order trial with immediate cancel
- Live market-order open with bracket protection orders
- Current position / open-order view, one-click cancel, one-click close
- Agent panel with step-by-step reasoning and refreshable daily briefing
- BNB / BTC / ETH contest-ready presets
- Lightweight backend: Python standard library only

## Product Positioning

This is not a signal bot.
This is not an autopilot trader.

It is a pre-trade safety layer for Binance users and AI agents:

- block avoidable losses before execution
- force bracket discipline
- make trading explainable
- keep the user in control

## Quick Start

```bash
cd /Users/kb/Desktop/AI自媒体视频
python3 run.py --serve --host 127.0.0.1 --port 8080
```

Open the demo:

- [http://127.0.0.1:8080/demo](http://127.0.0.1:8080/demo)

## Stable Public Deployment

This repo includes a Render Blueprint for a long-lived public demo:

- Deploy link: [Render Blueprint](https://dashboard.render.com/blueprint/new?repo=https://github.com/doublekunkun0/clawprofit-guard)
- Config file: [render.yaml](./render.yaml)
- Container entrypoint: [Dockerfile](./Dockerfile)

Deployment notes:

- The public deployment is intentionally configured as a safe demo.
- `BINANCE_API_KEY` and `BINANCE_SECRET_KEY` are left blank in Render so public visitors cannot access live trading.
- The app still exposes the full product flow, but account-level live execution should remain local-only.

Health check:

```bash
curl -s http://127.0.0.1:8080/health
```

Language switch:

- Use the top-right `中文 / EN` buttons in the demo UI.

## Core Demo Flow

1. Complete the adaptive risk questions.
2. Confirm the suggested profile.
3. Let the app auto-sync futures account and market context.
4. Click `评估交易`.
5. Click `合约预下单校验`.
6. Choose either:
   - `真实挂单试跑（撤单）`
   - `真实开仓执行（保留仓位）`
7. View current position / orders, cancel orders, or close position.

## Key API Endpoints

### Risk profile

```bash
curl -s http://127.0.0.1:8080/v1/profile/recommend \
  -H 'Content-Type: application/json' \
  -d '{
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
    }
  }'
```

### Market snapshot

```bash
curl -s 'http://127.0.0.1:8080/v1/binance/market-snapshot?symbol=BNBUSDT&side=LONG&profile=balanced'
```

### Account snapshot

```bash
curl -s 'http://127.0.0.1:8080/v1/binance/account-snapshot?symbol=BNBUSDT&profile=balanced'
```

### Trade evaluation

```bash
curl -s http://127.0.0.1:8080/v1/evaluate \
  -H 'Content-Type: application/json' \
  -d '{
    "profile": "balanced",
    "trade": {
      "symbol": "BNBUSDT",
      "side": "LONG",
      "entry_price": 620,
      "stop_loss_price": 610,
      "take_profit_price": 635,
      "leverage": 3,
      "position_notional_usdt": 180,
      "account_equity_usdt": 240
    },
    "market": {
      "volatility_24h_pct": 1.5,
      "bid_ask_spread_bps": 0.2,
      "liquidity_depth_score": 40
    },
    "behavior": {
      "consecutive_losses": 1,
      "trades_last_24h": 6,
      "day_pnl_pct": -0.8
    }
  }'
```

### Futures order-readiness check

Note:
- The endpoint name is still `/v1/binance/demo-order-test` for backward compatibility.
- Its current behavior is USD-M Futures order preview + readiness validation.

```bash
curl -s -X POST http://127.0.0.1:8080/v1/binance/demo-order-test \
  -H 'Content-Type: application/json' \
  -d '{
    "trade": {
      "symbol": "BNBUSDT",
      "side": "LONG",
      "entry_price": 620,
      "stop_loss_price": 610,
      "take_profit_price": 635,
      "leverage": 3,
      "position_notional_usdt": 180
    }
  }'
```

### Live limit-order trial and cancel

```bash
curl -s -X POST http://127.0.0.1:8080/v1/binance/live-order \
  -H 'Content-Type: application/json' \
  -d '{
    "trade": {
      "symbol": "BNBUSDT",
      "side": "LONG",
      "entry_price": 620,
      "stop_loss_price": 610,
      "take_profit_price": 635,
      "leverage": 3,
      "position_notional_usdt": 60,
      "margin_mode": "CROSSED"
    }
  }'
```

### Live open position with protection orders

```bash
curl -s -X POST http://127.0.0.1:8080/v1/binance/live-open-order \
  -H 'Content-Type: application/json' \
  -d '{
    "trade": {
      "symbol": "BNBUSDT",
      "side": "LONG",
      "entry_price": 620,
      "stop_loss_price": 610,
      "take_profit_price": 635,
      "leverage": 3,
      "position_notional_usdt": 180,
      "margin_mode": "CROSSED"
    }
  }'
```

## Contest Assets

Generate demo assets:

```bash
python3 scripts/generate_demo_assets.py
```

Generated files include:

- `output/demo/00_summary.json`
- `output/demo/01_profile_recommendation.json`
- `output/demo/02_trade_blocked.json`
- `output/demo/03_trade_adjusted.json`
- `output/demo/04_spot_order_preview.json`

Note:
- `04_spot_order_preview.json` is a legacy filename.
- The current product flow is futures-oriented.

Related contest docs:

- [docs/PRD_v1.md](./docs/PRD_v1.md)
- [docs/DEMO_VIDEO_60S.md](./docs/DEMO_VIDEO_60S.md)
- [docs/CONTEST_SUBMISSION_CHECKLIST.md](./docs/CONTEST_SUBMISSION_CHECKLIST.md)
- [docs/FIRST_PRIZE_SUBMISSION.md](./docs/FIRST_PRIZE_SUBMISSION.md)
- [openclaw/README.md](./openclaw/README.md)

## Run Tests

```bash
python3 -m unittest discover -s tests -p "test_*.py" -v
```

## Safety Note

This tool is a risk assistant, not investment advice and not a profit guarantee.

- Keep API permissions minimal.
- Prefer isolated demo keys or low-risk keys when recording.
- Do not expose seed phrases or private keys.
- Real execution should always remain explicitly user-triggered.
