# ClawProfit Guard PRD v1

## 1) Product Positioning

ClawProfit Guard is a Binance-focused pre-trade AI risk agent for USD-M Futures.
Its job is not to predict the market.
Its job is to stop users from making avoidable execution mistakes before they place risk.

一句话定位：

- `先防可避免亏损，再追求收益。`

## 2) Problem

Most user losses are caused by execution and behavior failure, not only wrong direction:

- over-leverage
- oversized positions
- no stop-loss
- weak reward/risk setup
- revenge trading after losses
- poor liquidity conditions
- opening positions without bracket protection

## 3) Goal

Primary goal:

- Reduce avoidable drawdowns before a futures order is sent.

Secondary goals:

- Turn emotional execution into rule-based execution.
- Force bracket discipline at the point of order entry.
- Give explainable, actionable trade repair suggestions instead of generic warnings.

## 4) Target Users

- Binance USD-M Futures users with repeated manual entry decisions
- Users who want stricter pre-trade guardrails than the exchange UI provides
- AI-agent users who want execution gated by explicit risk rules

## 5) Core User Flow

1. User answers an adaptive risk-profile questionnaire.
2. Agent calibrates the profile with recent account behavior.
3. System syncs futures account and market context.
4. User submits a trade plan.
5. Engine returns `ALLOW`, `WARN`, or `BLOCK`.
6. If needed, the engine returns a safer plan.
7. User runs order-readiness validation.
8. User can:
   - trial a live limit order and cancel it immediately
   - open a real market position and automatically post stop-loss / take-profit protection orders
9. User monitors current position, cancel orders, or closes position in one screen.

## 6) MVP Scope

- Trade risk scoring engine (0-100)
- Hard guardrails for leverage, size, daily loss, stop-loss, reward/risk
- Adaptive questionnaire + behavior calibration
- Suggested safer plan for leverage, position size, stop-loss, take-profit
- Binance USD-M Futures account + market sync with safe local fallback
- Futures order-readiness validation before execution
- Live limit-order trial with immediate cancel
- Live market-order open with stop-loss / take-profit protection orders
- Current position / order / unrealized PnL monitoring
- One-click cancel current orders
- One-click close current position
- OpenClaw integration kit for agent handoff

## 7) Non-Goals (v1)

- Fully autonomous trading without user trigger
- Alpha generation or signal prediction
- Portfolio management across many exchanges
- Custody or account hosting
- Profit guarantees

## 8) Decision Policy

Risk score formula:

`Risk = 0.30*Leverage + 0.25*Volatility + 0.20*Concentration + 0.15*Liquidity + 0.10*Behavior`

Policy:

- Any hard guardrail breach => `BLOCK`
- Score > 70 => `BLOCK`
- 31-70 => `WARN`
- <= 30 => `ALLOW`

## 9) Safety Principles

- Minimum permissions
- Human-in-the-loop execution
- Daily loss cap
- Forced stop-loss requirement
- Symbol allowlist
- If readiness validation fails, do not allow execution CTA to proceed silently
- If protection orders fail after opening, surface the failure explicitly and prefer emergency protection logic

## 10) Demo Value

This product is especially strong for contest demo because it shows a full and credible loop:

- risk profile
- live futures account context
- live market context
- trade decision
- exchange readiness check
- real execution path
- real position tracking

That makes it feel closer to a product than a concept slide.
