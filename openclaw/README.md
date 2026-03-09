# OpenClaw Integration Kit

This folder packages ClawProfit Guard into a judge-friendly OpenClaw handoff.
It shows how the product can be mounted as an agent workflow without claiming an unpublished manifest format.

## Included Files

- `tool_schemas.json`: tool names, endpoint paths, inputs, and outputs
- `sample_runbook.md`: recommended judge/demo flow
- `../docs/OPENCLAW_SYSTEM_PROMPT.md`: system prompt aligned to the current backend behavior

## Local Wiring

1. Start the local API server:

```bash
cd clawprofit-guard
python3 run.py --serve --host 127.0.0.1 --port 8080
```

2. Register the tools from `tool_schemas.json` against `http://127.0.0.1:8080`.
3. Use the system prompt from `docs/OPENCLAW_SYSTEM_PROMPT.md`.
4. Run the demo flow from `sample_runbook.md`.

## Scope Notes

- Account sync, market sync, and order-readiness checks are wired to Binance USD-M Futures with local fallback when unavailable.
- The workflow supports live position opening, stop-loss / take-profit protection orders, current position viewing, cancel orders, and close position.
- The product should be described as a pre-trade safety layer, not a signal bot.
