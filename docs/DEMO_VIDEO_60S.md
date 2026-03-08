# ClawProfit Guard 60s Demo Script

## Recording Goal

Show one complete and credible futures loop:

1. User gets a risk profile.
2. Agent loads Binance USD-M Futures account and market context.
3. High-risk trade is blocked or warned.
4. System returns a safer plan.
5. User validates order readiness.
6. User opens a real position and the system places stop-loss / take-profit protection orders.
7. User views current position and can close it if needed.

## Pre-Recording Commands

```bash
cd /Users/kb/Desktop/AI自媒体视频
python3 scripts/generate_demo_assets.py
python3 run.py --serve --host 127.0.0.1 --port 8080
```

Open:

- `http://127.0.0.1:8080/demo`

Generated assets:

- `/Users/kb/Desktop/AI自媒体视频/output/demo/00_summary.json`
- `/Users/kb/Desktop/AI自媒体视频/output/demo/01_profile_recommendation.json`
- `/Users/kb/Desktop/AI自媒体视频/output/demo/02_trade_blocked.json`
- `/Users/kb/Desktop/AI自媒体视频/output/demo/03_trade_adjusted.json`
- `/Users/kb/Desktop/AI自媒体视频/output/demo/04_spot_order_preview.json`

Note:

- `04_spot_order_preview.json` is a legacy filename.
- The current demo flow is futures-oriented.

## 60-Second Timeline

### 0s-6s (Hook)

Screen:

- Show the demo home screen.
- Highlight the title and the one-line value proposition.

Voice:

- `I built ClawProfit Guard, a Binance Futures pre-trade AI risk agent that blocks avoidable losses before execution.`

### 6s-14s (Profile)

Screen:

- Answer 2-3 adaptive profile questions.
- Show the generated profile card and risk score bubble.

Voice:

- `It starts with adaptive profiling, using both questionnaire answers and real account behavior to set personalized guardrails.`

### 14s-22s (Live Context)

Screen:

- Show `Agent 控制台`.
- Highlight `账户同步`, `市场同步`, and `Agent 简报`.

Voice:

- `Then it syncs Binance USD-M Futures account and market context, so the next trade uses real balance, behavior, price, spread, volatility, and liquidity.`

### 22s-34s (Evaluation)

Screen:

- Enter a trade.
- Click `评估交易`.
- Highlight the suggested plan and metrics.

Voice:

- `Before any order is sent, it evaluates the trade, returns ALLOW, WARN, or BLOCK, and explains the risk in plain language.`

### 34s-42s (Repair)

Screen:

- Click `应用建议并复评估`.
- Show the decision improves.

Voice:

- `If the setup is too aggressive, it doesn't just say no. It repairs the trade by resizing position, adjusting leverage, and rebuilding stop-loss and take-profit.`

### 42s-49s (Readiness Check)

Screen:

- Click `合约预下单校验`.
- Show the ticker-style readiness message.

Voice:

- `Next it validates execution readiness against Binance Futures rules, so the order is checked before real capital is placed.`

### 49s-57s (Live Execution)

Screen:

- Click `真实开仓执行（保留仓位）`.
- Show the marquee success message.
- Highlight `当前仓位/委托`.

Voice:

- `If the user chooses to execute, it opens the position and immediately places stop-loss and take-profit protection orders.`

### 57s-60s (Close)

Screen:

- Show current position card and one-click controls.

Voice:

- `This turns Binance Futures execution into a safer, explainable, bracket-protected workflow.`

## Judge Talk Track

- `This is not a signal bot.`
- `It is a pre-trade safety layer for Binance Futures users.`
- `The key innovation is that risk profiling, live context, exchange validation, and protected execution are connected in one loop.`
- `It ships with an OpenClaw handoff package, so the same workflow can be plugged into an AI agent.`
