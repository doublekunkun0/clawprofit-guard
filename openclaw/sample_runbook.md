# Sample Runbook

Use this order during the contest demo:

1. `recommend_risk_profile`
2. `sync_account_snapshot`
3. `sync_market_snapshot`
4. `evaluate_trade_plan`
5. If result is `BLOCK`, apply `suggested_plan` and call `evaluate_trade_plan` again
6. `check_futures_order_readiness`
7. Depending on the demo path:
   - `trial_live_limit_order`
   - or `open_futures_position`
8. `sync_current_exposure`

## Narration Notes

- Call the product a `pre-trade safety layer`, not a signal bot.
- Say `Binance USD-M Futures` explicitly when talking about context sync or execution.
- Emphasize that the strongest value is the full loop:
  - profile
  - evaluate
  - validate
  - execute
  - protect
  - monitor
