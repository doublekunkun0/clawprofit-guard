(function () {
  "use strict";

  const CLIENT_ASSET_VERSION = String(window.__cpgAssetVersion || "");

  const I18N = {
    en: {
      "meta.title": "ClawProfit Guard | Binance Futures AI Risk Agent",
      "hero.title": "Binance Futures Pre-Trade AI Risk Agent",
      "hero.subtitle":
        "Adaptive risk profiling, live futures account and market sync, execution readiness checks, and bracket protection orders in one guided workflow.",
      "hero.feature_profile": "Adaptive risk profiling",
      "hero.feature_context": "Live futures context sync",
      "hero.feature_bracket": "Bracket protection orders",
      "hero.feature_controls": "One-click cancel / close",
      "hero.proof_venue_label": "Venue",
      "hero.proof_venue_value": "Binance USD-M Futures",
      "hero.proof_flow_label": "Workflow",
      "hero.proof_flow_value": "Profile -> Evaluate -> Check -> Execute",
      "hero.proof_value_label": "Core value",
      "hero.proof_value_value": "Protect downside before chasing upside",
      "section.profile_setup": "1. Risk Profile Setup",
      "section.profile_note":
        "Use an adaptive, account-aware question bank to locate the user's trading style first, then score it with measurable ranges.",
      "section.profile_flow":
        "The agent asks 4-7 questions based on your answers and recent account behavior. Finish the path and confirm the suggested profile.",
      "section.trade_eval": "2. Trade Evaluation",
      "section.trade_note": "Market data syncs automatically. Confirm profile first, then evaluate trade.",
      "section.trade_hint":
        "BNB / BTC / ETH market values auto-sync. Current profile guardrails may still block some pairs.",
      "agent.kicker": "Agent Console",
      "agent.title": "ClawProfit Agent",
      "agent.note": "Live account, live market, daily summary, and next action in one screen.",
      "agent.status_booting": "Agent booting",
      "agent.status_profile": "Profiling",
      "agent.status_ready": "Ready to evaluate",
      "agent.status_repair": "Repair required",
      "agent.status_execution": "Execution ready",
      "agent.status_preview": "Preview ready",
      "agent.status_syncing": "Syncing context",
      "agent.status_desynced": "Runtime desynced",
      "field.experience_level": "Experience",
      "field.risk_tolerance": "Risk Tolerance",
      "field.leverage_preference": "Leverage Preference",
      "field.stop_loss_discipline": "Stop-loss Discipline",
      "field.revenge_tendency": "Revenge Tendency",
      "field.trading_frequency": "Trading Frequency",
      "field.max_drawdown_comfort_pct": "Max Drawdown Comfort (%)",
      "field.selected_profile": "Selected Profile (optional)",
      "field.consecutive_losses": "Consecutive Losses",
      "field.trades_last_24h": "Trades Last 24h",
      "field.day_pnl_pct": "Day PnL (%)",
      "field.symbol": "Symbol",
      "field.side": "Side",
      "field.entry_price": "Entry Price",
      "field.stop_loss_price": "Stop-loss Price",
      "field.take_profit_price": "Take-profit Price",
      "field.stop_loss_rate": "Stop-loss %",
      "field.take_profit_rate": "Take-profit %",
      "field.leverage": "Leverage",
      "field.margin_mode": "Margin Mode",
      "field.position_notional_usdt": "Position Size (USDT)",
      "field.position_margin_usdt": "Margin Used (USDT)",
      "field.position_ratio": "Wallet Balance Ratio",
      "field.account_equity_usdt": "Futures Wallet Balance (USDT)",
      "field.volatility_24h_pct": "Volatility 24h (%)",
      "field.bid_ask_spread_bps": "Spread (bps)",
      "field.liquidity_depth_score": "Liquidity Depth Score",
      "result.liquidity_band_low": "Thin",
      "result.liquidity_band_mid": "Balanced",
      "result.liquidity_band_high": "Deep",
      "opt.beginner": "Beginner",
      "opt.intermediate": "Intermediate",
      "opt.advanced": "Advanced",
      "opt.low": "Low",
      "opt.medium": "Medium",
      "opt.high": "High",
      "opt.always": "Always",
      "opt.sometimes": "Sometimes",
      "opt.rarely": "Rarely",
      "opt.never": "Never",
      "opt.often": "Often",
      "opt.auto": "Auto",
      "opt.long": "LONG",
      "opt.short": "SHORT",
      "opt.crossed": "CROSSED",
      "opt.isolated": "ISOLATED",
      "opt.dd_5": "5% (capital protection)",
      "opt.dd_8": "8% (balanced)",
      "opt.dd_12": "12% (high-risk)",
      "token.bnb": "BNB",
      "token.btc": "BTC",
      "token.eth": "ETH",
      "token.sol": "SOL",
      "token.xrp": "XRP",
      "token.doge": "DOGE",
      "token.ada": "ADA",
      "profile.conservative": "Conservative",
      "profile.balanced": "Balanced",
      "profile.aggressive": "Aggressive",
      "btn.evaluate_trade": "Evaluate Trade",
      "btn.order_test": "Futures Order Check",
      "btn.live_order": "Live Trial (Cancel)",
      "btn.live_open_order": "Live Open Position",
      "btn.view_current_exposure": "View Current Position / Orders",
      "btn.cancel_current_orders": "Cancel Current Orders",
      "btn.close_current_position": "Close Position",
      "btn.apply_plan": "Apply Suggested Plan",
      "btn.refresh_agent_briefing": "Refresh Briefing",
      "btn.prev_question": "Previous",
      "btn.retake": "Retake",
      "btn.confirm_profile": "Confirm Profile",
      "wizard.progress": "Question {current}/{total}",
      "wizard.log_empty":
        "Start with the core prompts. The agent will decide whether leverage and loss-response follow-ups are needed.",
      "wizard.answered": "{done}/{total} answered",
      "wizard.complete": "Current question path completed. Profile is being generated automatically.",
      "wizard.q.experience": "Which range is closest to your real live-trading experience?",
      "wizard.q.trading_frequency": "In a normal trading day, how many completed trades do you usually make?",
      "wizard.q.risk_tolerance": "Which per-trade-risk and daily-loss range is closest to your real behavior?",
      "wizard.q.leverage_preference": "What leverage range do you actually use most often?",
      "wizard.q.stop_loss_discipline": "In your last 20 trades, how many times did you follow your stop-loss plan?",
      "wizard.q.revenge_tendency": "After two losses in a row, what do you usually do next?",
      "wizard.q.max_drawdown": "At what one-day loss level would you usually stop trading?",
      "wizard.opt.experience.beginner": "< 1 year live trading or < 200 closed trades",
      "wizard.opt.experience.intermediate":
        "1-3 years live trading and about 200-2000 closed trades",
      "wizard.opt.experience.advanced": "> 3 years live trading and > 2000 closed trades",
      "wizard.opt.risk.low": "Per-trade risk <=1%, daily max loss <=3%",
      "wizard.opt.risk.medium": "Per-trade risk 1%-2%, daily max loss 3%-6%",
      "wizard.opt.risk.high": "Per-trade risk >2%, daily max loss >6%",
      "wizard.opt.leverage.low": "Typical leverage 1x-3x",
      "wizard.opt.leverage.medium": "Typical leverage 4x-10x",
      "wizard.opt.leverage.high": "Typical leverage 11x-20x",
      "wizard.opt.stop.always": "Stop-loss execution >=90% in last 20 trades",
      "wizard.opt.stop.sometimes": "Stop-loss execution 60%-90% in last 20 trades",
      "wizard.opt.stop.rarely": "Stop-loss execution <60% in last 20 trades",
      "wizard.opt.revenge.never": "After losses, I enforce >=30 min cooldown",
      "wizard.opt.revenge.sometimes": "Occasional chase orders (<=2 times/week)",
      "wizard.opt.revenge.often": "Frequent chase orders (>2 times/week)",
      "wizard.opt.frequency.low": "Average 1-3 trades/day",
      "wizard.opt.frequency.medium": "Average 4-10 trades/day",
      "wizard.opt.frequency.high": "Average >10 trades/day",
      "wizard.note.experience": "The agent uses this to decide whether it needs to ask deeper execution questions.",
      "wizard.note.frequency": "Trading frequency is the first filter for overtrading and whether more follow-ups are needed.",
      "wizard.note.frequency_account":
        "Recent 24h trade count is already available from account context, so the agent skips self-reported frequency.",
      "wizard.note.risk": "This sets the base guardrail range for leverage, size, and daily loss.",
      "wizard.note.risk_account":
        "Recent account behavior is used as a calibration layer, so this answer is not scored in isolation.",
      "wizard.note.leverage": "Your earlier answers suggest leverage meaningfully affects your score, so the agent asks it directly.",
      "wizard.note.leverage_risk": "High risk tolerance was detected, so the agent needs your real leverage habit instead of assuming it.",
      "wizard.note.leverage_activity": "Your trading activity is elevated, so leverage is now a required follow-up.",
      "wizard.note.stop": "Execution discipline determines whether the agent needs to inspect loss-response behavior.",
      "wizard.note.revenge_discipline": "Your stop-loss discipline adds uncertainty, so the agent is checking your behavior after losses.",
      "wizard.note.revenge_risk": "Because your risk/activity level is elevated, the agent needs one more behavior check.",
      "wizard.note.revenge_account":
        "Loss streak or negative PnL was detected in account context, so a loss-response follow-up is required.",
      "wizard.note.drawdown": "This final answer determines the daily stop-trading threshold and profile tightening rules.",
      "wizard.note.drawdown_account":
        "Recent account losses make this stop-trading threshold more important for final scoring.",
      "wizard.account_signal":
        "Account context: {trades} trades/24h, PnL {pnl}%, loss streak {losses}.",
      "status.await_profile": "Awaiting profile generation",
      "status.loading_profile": "Generating profile suggestion...",
      "status.preview_profile": "Preview: {profile} (score {score}). Keep answering to refine it.",
      "status.pending_confirmation":
        "Suggested: {profile} (score {score}). Confirm or modify your answers.",
      "status.confirmed_profile": "Confirmed: {profile}. Trade evaluation is unlocked.",
      "status.profile_dirty": "Inputs changed. Regenerate and reconfirm profile.",
      "result.profile_result": "Profile Result",
      "result.trade_result": "Trade Result",
      "result.trade_signal": "Trade Signal",
      "placeholder.profile_result": "Complete the questions to see the suggested profile.",
      "profile.tech_kicker": "Risk Mesh",
      "profile.score_caption": "Risk Score",
      "profile.guardrail_caption": "Execution Envelope",
      "profile.confirmed_tag": "Confirmed",
      "profile.preview_tag": "Live Preview",
      "profile.pending_tag": "Pending Confirm",
      "profile.sync_caption": "Account-aware calibration",
      "profile.bnb_caption": "",
      "profile.bias_shield": "Shield Bias",
      "profile.bias_balanced": "Balanced Bias",
      "profile.bias_velocity": "Velocity Bias",
      "profile.caption_stop": "Stop Envelope",
      "profile.caption_reward": "Reward Filter",
      "profile.caption_density": "Capital Density",
      "placeholder.trade_result":
        "Confirm profile first, then evaluate a trade to see decision, reasons, and suggested plan.",
      "placeholder.market_sync":
        "Market data will sync automatically to load demo prices and suggested stop/take-profit.",
      "placeholder.order_test":
        "Run futures order check to validate the USD-M Futures payload before execution.",
      "placeholder.current_exposure":
        "Click to view the current symbol's live position and active orders.",
      "status.current_exposure_loading": "Loading current symbol position and open orders...",
      "status.cancel_orders_loading": "Canceling current symbol open orders and protection orders...",
      "status.close_position_loading": "Closing the current symbol position with a market order...",
      "placeholder.account_sync":
        "Account sync waits for Binance USD-M Futures credentials; until then the agent uses safe fallback context.",
      "placeholder.agent_briefing":
        "Agent briefing will summarize the current profile, account context, and next action.",
      "placeholder.agent_steps":
        "Profile, account sync, market sync, evaluation, and order check will appear here.",
      "result.label_profile": "Profile",
      "result.label_score": "score",
      "result.guardrails": "Guardrails",
      "result.max_leverage": "max leverage",
      "result.max_daily_loss": "max daily loss",
      "result.max_risk_trade": "max risk/trade",
      "result.max_position_equity": "max position/equity",
      "result.max_reward_risk": "min reward/risk",
      "result.strengths": "Strengths",
      "result.issues": "Issues",
      "result.coaching": "Coaching",
      "result.auto_adjustments": "Auto Adjustments",
      "result.decision": "Decision",
      "result.risk_score": "Risk score",
      "result.await_evaluation": "Await",
      "result.suggested_plan": "Suggested Plan",
      "result.plan_leverage": "leverage",
      "result.plan_notional": "position_size_usdt",
      "result.plan_stop_loss": "stop_loss_price",
      "result.plan_take_profit": "take_profit_price",
      "result.plan_note": "note",
      "result.reasons": "Reasons",
      "result.blockers": "Blockers",
      "result.metrics": "Metrics",
      "result.profile_context": "Profile Context",
      "result.position_tracker": "Position Tracker",
      "result.current_exposure": "Current Position / Orders",
      "result.current_position_summary": "Current Position",
      "result.current_open_orders": "Current Open Orders",
      "result.current_protection_orders": "Current Protection Orders",
      "result.current_action": "Latest Action",
      "result.order_side": "Order Side",
      "result.order_type": "Order Type",
      "result.order_price": "Order Price",
      "result.order_stop_price": "Trigger Price",
      "result.order_qty": "Order Qty",
      "result.position_waiting": "Waiting for exchange position update...",
      "result.position_missing": "No active position detected for the current symbol yet.",
      "result.position_side": "Position Side",
      "result.position_qty": "Position Qty",
      "result.position_notional": "Position Notional",
      "result.position_entry_price": "Entry Price",
      "result.position_mark_price": "Mark Price",
      "result.position_unrealized_pnl": "Unrealized PnL",
      "result.live_refreshing": "Live syncing",
      "result.position_liq_price": "Liquidation Price",
      "result.position_initial_margin": "Initial Margin",
      "result.position_roe": "ROE",
      "result.market_sync": "Market Sync",
      "result.market_source": "Data Source",
      "result.market_chart": "Live K-Line",
      "result.market_chart_empty": "Chart data is loading...",
      "result.market_chart_range": "Range",
      "result.market_chart_change": "Move",
      "result.market_chart_live": "Live 5m",
      "result.market_warning": "Warning",
      "result.market_prices": "Last / Bid / Ask",
      "result.market_stats": "Vol / Spread / Depth",
      "result.market_suggested_trade": "Suggested Entry / SL / TP",
      "result.next_step": "Next",
      "result.order_check": "Futures Order Check",
      "result.order_status": "Status",
      "result.order_mode": "Mode",
      "result.order_message": "Message",
      "result.order_opened_compact": "Position opened successfully.",
      "result.order_opened_compact_hint":
        "Position, protection orders, and current order state have been synced to Current Position / Orders.",
      "result.order_preview": "Order Preview",
      "result.preview_qty": "Preview Qty",
      "result.order_credentials": "API Credentials",
      "result.exchange_minimums": "Exchange Minimums",
      "result.min_executable_qty": "Min executable qty",
      "result.min_executable_notional": "Min executable notional",
      "result.live_test_notional": "Live Test Notional",
      "result.live_order": "Live Order",
      "result.cancel_result": "Cancel Result",
      "result.execution_policy": "Execution Policy",
      "result.requested_margin_mode": "Requested Margin Mode",
      "result.requested_leverage": "Requested Leverage",
      "result.requested_entry_price": "Requested Entry Price",
      "result.requested_notional": "Requested Position Size",
      "result.requested_margin": "Requested Margin",
      "result.actual_execution_notional": "Actual Filled Notional",
      "result.execution_notional_delta": "Notional Deviation",
      "result.execution_notional_delta_pct": "Deviation Ratio",
      "result.execution_deviation_alert": "Execution Deviation Alert",
      "result.execution_deviation_warn":
        "Actual fill deviated materially from the requested order size. Consider adjusting size or checking contract step size before the next order.",
      "result.execution_deviation_block":
        "Actual fill deviated sharply from the requested order size. Review the requested amount before opening the next position.",
      "result.estimated_execution_notional": "Estimated Execution Notional",
      "result.required_initial_margin": "Required Initial Margin",
      "result.execution_reference_price": "Execution Reference Price",
      "result.execution_details": "Execution Details",
      "result.protection_orders": "Protection Orders",
      "result.stop_loss_order": "Stop-loss Order",
      "result.take_profit_order": "Take-profit Order",
      "result.trigger_price": "Trigger Price",
      "result.working_type": "Working Type",
      "result.close_all": "Close All",
      "result.emergency_close": "Emergency Close",
      "result.executed_qty": "Executed Qty",
      "result.avg_fill_price": "Avg Fill Price",
      "result.exchange_leverage": "Exchange Leverage",
      "result.exchange_margin_mode": "Exchange Margin Mode",
      "result.account_sync": "Account Sync",
      "result.account_source": "Account Source",
      "result.account_connection": "Connection",
      "result.account_equity": "Futures Account Equity",
      "result.account_wallet": "Futures Wallet Balance",
      "result.account_available": "Available USDT",
      "result.account_locked": "Locked USDT",
      "result.account_open_orders": "Open Orders",
      "result.account_behavior": "Behavior Snapshot",
      "result.account_assets": "Top Assets",
      "result.account_position_cap": "Suggested Max Notional",
      "result.account_risk_budget": "Risk Budget",
      "result.agent_briefing": "Agent Briefing",
      "result.agent_steps": "Agent Steps",
      "metric.risk_per_trade_pct": "Risk at stop",
      "metric.reward_risk_ratio": "Reward/risk",
      "metric.target_reward_risk_ratio": "Required reward/risk",
      "metric.liquidation_buffer_pct": "Est. liquidation buffer",
      "metric.leverage_risk": "Leverage risk",
      "metric.volatility_risk": "Volatility risk",
      "metric.concentration_risk": "Concentration risk",
      "metric.liquidity_risk": "Liquidity risk",
      "metric.behavior_risk": "Behavior risk",
      "decision.ALLOW": "ALLOW",
      "decision.WARN": "WARN",
      "decision.BLOCK": "BLOCK",
      "alert.profile_failed": "Profile request failed",
      "alert.account_sync_failed": "Account sync failed",
      "alert.market_sync_failed": "Market sync failed",
      "alert.evaluate_failed": "Evaluate request failed",
      "alert.order_test_failed": "Futures order check failed",
      "alert.live_order_failed": "Live order trial failed",
      "alert.live_open_order_failed": "Live open-position order failed",
      "alert.cancel_current_orders_failed": "Cancel current orders failed",
      "alert.close_current_position_failed": "Close current position failed",
      "alert.runtime_mismatch":
        "Frontend/backend versions are not aligned. Waiting for backend reload before trading actions.",
      "alert.asset_mismatch": "A newer demo page is available. Reloading the page now.",
      "alert.execution_requires_profile": "Confirm the risk profile before any live execution.",
      "alert.execution_requires_evaluation": "Evaluate the trade before any live execution.",
      "alert.execution_blocked": "Current trade is blocked by guardrails. Apply fixes before live execution.",
      "alert.wizard_incomplete": "Please complete all profile prompts first.",
      "alert.confirm_profile_first": "Please generate and confirm profile before evaluating trade.",
      "alert.no_profile_to_confirm": "Generate profile first, then confirm.",
      "status.runtime_check": "Checking runtime sync...",
      "status.market_loading": "Syncing Binance market snapshot...",
      "status.order_loading": "Checking Binance USD-M Futures order preview...",
      "status.live_order_loading": "Placing a live USD-M Futures limit order and canceling it immediately...",
      "status.live_open_order_loading": "Placing a live USD-M Futures market order and posting stop-loss / take-profit protection orders...",
      "hint.next_profile": "Next: finish the profile questions.",
      "hint.next_confirm_profile": "Next: confirm the suggested profile to unlock trade evaluation.",
      "hint.next_evaluate": "Next: review the auto-synced market values and click Evaluate Trade.",
      "hint.next_apply_fix": "Next: apply the suggested plan, then re-evaluate.",
      "hint.next_order_test": "Next: run Futures Order Check to show execution readiness.",
      "hint.next_live_order": "Next: run Live Order Trial or Live Open Position, depending on whether you want to keep the position.",
      "step.profile": "Risk profile",
      "step.account": "Account context",
      "step.market": "Market context",
      "step.evaluate": "Trade decision",
      "step.order": "Execution check",
      "step.briefing": "Agent briefing",
      "step.profile.pending": "Finish the adaptive question path and confirm the suggested profile.",
      "step.profile.done": "Profile confirmed and ready.",
      "step.account.pending": "Waiting for account sync or fallback context.",
      "step.account.done": "Account context is available.",
      "step.market.pending": "Waiting for live or fallback market snapshot.",
      "step.market.done": "Market snapshot is synced.",
      "step.evaluate.pending": "Evaluate the current trade plan.",
      "step.evaluate.done": "Trade decision is available.",
      "step.order.pending": "Order check unlocks after a non-blocked decision.",
      "step.order.done": "Order preview or validation is available.",
      "step.briefing.pending": "Refresh the latest agent briefing when you want a fresh daily summary.",
      "step.briefing.done": "Agent briefing was refreshed with the latest context.",
      "source.binance_spot_demo": "Binance Spot Demo Mode",
      "source.binance_spot_live": "Binance Spot API",
      "source.binance_futures_demo": "Binance USD-M Futures Testnet",
      "source.binance_futures_live": "Binance USD-M Futures API",
      "source.local_fallback": "Local Fallback (not live futures account)",
      "mode.binance_spot_demo": "Binance Spot Demo Mode",
      "mode.binance_spot_live": "Binance Spot API",
      "mode.binance_futures_demo": "Binance USD-M Futures Testnet",
      "mode.binance_futures_live": "Binance USD-M Futures API",
      "mode.preview_only": "Preview Only",
      "order_status.validated": "Validated",
      "order_status.placed_then_canceled": "Placed then canceled",
      "order_status.opened": "Opened",
      "order_status.protection_partial": "Protection partial",
      "order_status.protection_failed": "Protection failed",
      "order_status.cancel_failed": "Cancel failed",
      "order_status.preview_invalid": "Preview invalid",
      "order_status.confirmation_required": "Confirmation required",
      "order_status.intent_preview_only": "Preview only for SHORT intent",
      "order_status.not_configured": "Preview only",
      "order_status.network_unavailable": "Network unavailable",
      "order_status.exchange_rejected": "Exchange rejected",
      "confirm.live_order":
        "This will place a real Binance USD-M Futures limit order and cancel it immediately. Continue?",
      "confirm.live_open_order":
        "This will place a real Binance USD-M Futures market order and immediately post stop-loss / take-profit protection orders. Continue?",
      "confirm.cancel_current_orders":
        "This will cancel the current symbol's open orders and protection orders. Continue?",
      "confirm.close_current_position":
        "This will submit a market order to close the current symbol position. Continue?",
      "misc.configured": "Configured",
      "misc.missing": "Missing",
      "misc.na": "N/A",
      "misc.live_connected": "Live connected",
      "misc.demo_only": "Disconnected, showing local demo values",
    },
    zh: {
      "meta.title": "ClawProfit Guard｜龙虾合约风控官",
      "hero.title": "币安合约交易前 AI 风控官",
      "hero.subtitle":
        "动态问答建档、实盘合约账户与市场联动、预下单校验、开仓即挂止盈止损，一屏完成完整交易闭环。",
      "hero.feature_profile": "动态问答建档",
      "hero.feature_context": "Binance 合约实时联动",
      "hero.feature_bracket": "开仓即挂止盈止损",
      "hero.feature_controls": "一键撤单 / 一键平仓",
      "hero.proof_venue_label": "交易场景",
      "hero.proof_venue_value": "Binance USD-M Futures",
      "hero.proof_flow_label": "闭环流程",
      "hero.proof_flow_value": "建档 -> 评估 -> 校验 -> 执行",
      "hero.proof_value_label": "核心定位",
      "hero.proof_value_value": "先防可避免亏损，再追求收益",
      "section.profile_setup": "1. 风险档位设置",
      "section.profile_note":
        "先用接入账户行为的动态问答库定位用户交易风格，再用可量化选项完成评分和分档。",
      "section.profile_flow":
        "Agent 会根据你的回答和近24小时账户行为动态追问 4-7 题。完成当前路径后，系统会自动生成档位。",
      "section.trade_eval": "2. 交易评估",
      "section.trade_note": "市场参数会自动同步。先确认档位，再做交易评估。",
      "section.trade_hint":
        "BNB / BTC / ETH 会自动同步演示市场参数，但仍受当前档位白名单约束。",
      "agent.kicker": "Agent 控制台",
      "agent.title": "ClawProfit Agent",
      "agent.note": "已连接账户、实时市场、日内简报和下一步操作，一屏看清。",
      "agent.status_booting": "Agent 启动中",
      "agent.status_profile": "正在建档",
      "agent.status_ready": "可开始评估",
      "agent.status_repair": "需要修正",
      "agent.status_execution": "可执行",
      "agent.status_preview": "可预览校验",
      "agent.status_syncing": "正在同步上下文",
      "agent.status_desynced": "前后端未同步",
      "field.experience_level": "交易经验",
      "field.risk_tolerance": "风险偏好",
      "field.leverage_preference": "杠杆偏好",
      "field.stop_loss_discipline": "止损纪律",
      "field.revenge_tendency": "报复性交易倾向",
      "field.trading_frequency": "交易频率",
      "field.max_drawdown_comfort_pct": "可接受最大回撤（%）",
      "field.selected_profile": "手动档位（可选）",
      "field.consecutive_losses": "连续亏损次数",
      "field.trades_last_24h": "近24小时交易次数",
      "field.day_pnl_pct": "当日盈亏（%）",
      "field.symbol": "交易对",
      "field.side": "方向",
      "field.entry_price": "开仓价",
      "field.stop_loss_price": "止损价",
      "field.take_profit_price": "止盈价",
      "field.stop_loss_rate": "止损率",
      "field.take_profit_rate": "止盈率",
      "field.leverage": "杠杆",
      "field.margin_mode": "保证金模式",
      "field.position_notional_usdt": "持仓数量（USDT）",
      "field.position_margin_usdt": "保证金（USDT）",
      "field.position_ratio": "钱包余额占比",
      "field.account_equity_usdt": "合约钱包余额（USDT）",
      "field.volatility_24h_pct": "24h波动率（%）",
      "field.bid_ask_spread_bps": "买卖价差（bps）",
      "field.liquidity_depth_score": "流动性深度评分",
      "result.liquidity_band_low": "偏薄",
      "result.liquidity_band_mid": "均衡",
      "result.liquidity_band_high": "充足",
      "opt.beginner": "新手",
      "opt.intermediate": "中级",
      "opt.advanced": "高级",
      "opt.low": "低",
      "opt.medium": "中",
      "opt.high": "高",
      "opt.always": "总是",
      "opt.sometimes": "有时",
      "opt.rarely": "很少",
      "opt.never": "从不",
      "opt.often": "经常",
      "opt.auto": "自动",
      "opt.long": "做多",
      "opt.short": "做空",
      "opt.crossed": "全仓",
      "opt.isolated": "逐仓",
      "opt.dd_5": "5%（保护资金）",
      "opt.dd_8": "8%（平衡）",
      "opt.dd_12": "12%（高风险）",
      "token.bnb": "BNB",
      "token.btc": "BTC",
      "token.eth": "ETH",
      "token.sol": "SOL",
      "token.xrp": "XRP",
      "token.doge": "DOGE",
      "token.ada": "ADA",
      "profile.conservative": "保守型",
      "profile.balanced": "平衡型",
      "profile.aggressive": "进取型",
      "btn.evaluate_trade": "评估交易",
      "btn.order_test": "合约预下单校验",
      "btn.live_order": "真实挂单试跑（撤单）",
      "btn.live_open_order": "真实开仓执行（保留仓位）",
      "btn.view_current_exposure": "查看当前仓位/委托",
      "btn.cancel_current_orders": "撤销当前委托",
      "btn.close_current_position": "一键平仓",
      "btn.apply_plan": "应用建议并复评估",
      "btn.refresh_agent_briefing": "更新简报",
      "btn.prev_question": "上一题",
      "btn.retake": "重做问答",
      "btn.confirm_profile": "确认档位",
      "wizard.progress": "问题 {current}/{total}",
      "wizard.log_empty": "先回答基础问题，Agent 会判断是否继续追问杠杆和亏损后的行为。",
      "wizard.answered": "已回答 {done}/{total}",
      "wizard.complete": "当前问答路径已完成，系统正在自动生成档位。",
      "wizard.q.experience": "哪一段最接近你的真实实盘经历？",
      "wizard.q.trading_frequency": "正常交易日里，你通常会完成多少笔交易？",
      "wizard.q.risk_tolerance": "哪组单笔风险和单日亏损范围最接近你平时的做法？",
      "wizard.q.leverage_preference": "你实际最常用的杠杆区间是？",
      "wizard.q.stop_loss_discipline": "最近 20 笔里，你有多少次按计划执行了止损？",
      "wizard.q.revenge_tendency": "如果连续亏损 2 笔，你下一步通常会怎么做？",
      "wizard.q.max_drawdown": "单日亏到什么程度，你通常会主动停手？",
      "wizard.opt.experience.beginner": "<1年实盘 或 累计平仓<200笔",
      "wizard.opt.experience.intermediate": "1-3年实盘 且 累计平仓约200-2000笔",
      "wizard.opt.experience.advanced": ">3年实盘 且 累计平仓>2000笔",
      "wizard.opt.risk.low": "单笔风险<=1%，单日最大亏损<=3%",
      "wizard.opt.risk.medium": "单笔风险1%-2%，单日最大亏损3%-6%",
      "wizard.opt.risk.high": "单笔风险>2%，单日最大亏损>6%",
      "wizard.opt.leverage.low": "常用杠杆 1x-3x",
      "wizard.opt.leverage.medium": "常用杠杆 4x-10x",
      "wizard.opt.leverage.high": "常用杠杆 11x-20x",
      "wizard.opt.stop.always": "近20笔止损执行率 >=90%",
      "wizard.opt.stop.sometimes": "近20笔止损执行率 60%-90%",
      "wizard.opt.stop.rarely": "近20笔止损执行率 <60%",
      "wizard.opt.revenge.never": "亏损后会强制冷静>=30分钟",
      "wizard.opt.revenge.sometimes": "偶发追单（每周<=2次）",
      "wizard.opt.revenge.often": "频繁追单（每周>2次）",
      "wizard.opt.frequency.low": "日均 1-3 笔",
      "wizard.opt.frequency.medium": "日均 4-10 笔",
      "wizard.opt.frequency.high": "日均 >10 笔",
      "wizard.note.experience": "Agent 先用这题判断你属于新手、进阶还是高经验用户，决定后续要不要深问。",
      "wizard.note.frequency": "交易频率是识别过度交易和是否继续追问执行细节的第一层筛选。",
      "wizard.note.frequency_account": "系统已经从账户上下文读取到近24小时交易次数，因此会跳过主观频率自评。",
      "wizard.note.risk": "这题用于设定基础风控护栏，决定仓位、杠杆和日亏限制。",
      "wizard.note.risk_account": "系统会结合最近账户行为一起校准这题，不会只按主观自评打分。",
      "wizard.note.leverage": "前面的回答说明杠杆会显著影响你的评分，所以 Agent 需要直接确认。",
      "wizard.note.leverage_risk": "系统检测到你的风险偏好偏高，不能靠默认值推断杠杆习惯。",
      "wizard.note.leverage_activity": "你的交易活跃度偏高，杠杆使用会显著影响风控结果。",
      "wizard.note.stop": "执行纪律会决定 Agent 是否继续追问你在亏损后的真实反应。",
      "wizard.note.revenge_discipline": "你的止损执行存在不确定性，Agent 需要补问亏损后的行为。",
      "wizard.note.revenge_risk": "你的风险偏好或交易活跃度偏高，所以需要再做一次行为确认。",
      "wizard.note.revenge_account": "账户上下文里已经出现连亏或负收益信号，所以必须补问一次亏损后的反应。",
      "wizard.note.drawdown": "最后这题用来确定你该在什么日亏阈值下停手，以及是否触发收紧档位。",
      "wizard.note.drawdown_account": "由于账户最近已经出现亏损，这个停手阈值会更直接影响最终评分和档位收紧。",
      "wizard.account_signal": "账户上下文：近24小时 {trades} 笔，盈亏 {pnl}%，连续亏损 {losses} 次。",
      "status.await_profile": "等待生成档位",
      "status.loading_profile": "正在生成档位建议...",
      "status.preview_profile": "临时档位：{profile}（评分 {score}）。继续答题，系统会实时修正。",
      "status.pending_confirmation": "建议档位：{profile}（评分 {score}）。请确认或修改问答。",
      "status.confirmed_profile": "已确认档位：{profile}。可开始交易评估。",
      "status.profile_dirty": "输入已变更，请重新生成并确认档位。",
      "result.profile_result": "档位结果",
      "result.trade_result": "交易结果",
      "result.trade_signal": "交易信号",
      "placeholder.profile_result": "完成问答后，这里会显示系统建议档位。",
      "profile.tech_kicker": "风险矩阵",
      "profile.score_caption": "风险评分",
      "profile.guardrail_caption": "执行边界",
      "profile.confirmed_tag": "已确认",
      "profile.preview_tag": "实时预估",
      "profile.pending_tag": "待确认",
      "profile.sync_caption": "已结合账户行为做动态校准",
      "profile.bnb_caption": "",
      "profile.bias_shield": "防守偏置",
      "profile.bias_balanced": "平衡偏置",
      "profile.bias_velocity": "进攻偏置",
      "profile.caption_stop": "止损边界",
      "profile.caption_reward": "收益筛选",
      "profile.caption_density": "资金密度",
      "placeholder.trade_result": "先确认档位，再点击“评估交易”查看决策、原因与修正建议。",
      "placeholder.market_sync": "市场数据会自动同步，并带入演示价格、止损和止盈。",
      "placeholder.order_test": "点击合约预下单校验，验证 USD-M Futures 订单参数。",
      "placeholder.current_exposure": "点击查看当前交易对的实盘仓位和当前委托。",
      "status.current_exposure_loading": "正在读取当前交易对的仓位和委托...",
      "status.cancel_orders_loading": "正在撤销当前交易对的普通委托和保护单...",
      "status.close_position_loading": "正在用市价单平掉当前交易对仓位...",
      "placeholder.account_sync":
        "账户同步等待 Binance USD-M Futures 凭证；在此之前 Agent 会使用安全的本地回退上下文。",
      "placeholder.agent_briefing":
        "Agent 简报会总结当前档位、账户状态和下一步动作。",
      "placeholder.agent_steps":
        "风险档位、账户同步、市场同步、交易评估、订单校验，会按步骤显示在这里。",
      "result.label_profile": "档位",
      "result.label_score": "评分",
      "result.guardrails": "风控护栏",
      "result.max_leverage": "最大杠杆",
      "result.max_daily_loss": "日亏上限",
      "result.max_risk_trade": "单笔风险上限",
      "result.max_position_equity": "仓位/权益上限",
      "result.max_reward_risk": "最低盈亏比",
      "result.strengths": "优势",
      "result.issues": "风险问题",
      "result.coaching": "优化建议",
      "result.auto_adjustments": "自动调整",
      "result.decision": "决策",
      "result.risk_score": "风险分",
      "result.await_evaluation": "待评估",
      "result.suggested_plan": "建议方案",
      "result.plan_leverage": "杠杆",
      "result.plan_notional": "持仓数量",
      "result.plan_stop_loss": "止损价",
      "result.plan_take_profit": "止盈价",
      "result.plan_note": "说明",
      "result.reasons": "原因",
      "result.blockers": "拦截项",
      "result.metrics": "指标明细",
      "result.profile_context": "档位上下文",
      "result.position_tracker": "仓位跟踪",
      "result.current_exposure": "当前仓位/委托",
      "result.current_position_summary": "当前仓位",
      "result.current_open_orders": "当前委托",
      "result.current_protection_orders": "当前保护单",
      "result.current_action": "最近动作",
      "result.order_side": "委托方向",
      "result.order_type": "委托类型",
      "result.order_price": "委托价格",
      "result.order_stop_price": "触发价格",
      "result.order_qty": "委托数量",
      "result.position_waiting": "正在等待交易所返回最新持仓...",
      "result.position_missing": "当前交易对暂未检测到活跃持仓。",
      "result.position_side": "仓位方向",
      "result.position_qty": "持仓数量",
      "result.position_notional": "仓位名义价值",
      "result.position_entry_price": "开仓均价",
      "result.position_mark_price": "标记价格",
      "result.position_unrealized_pnl": "未实现盈亏",
      "result.live_refreshing": "实时同步中",
      "result.position_liq_price": "强平价格",
      "result.position_initial_margin": "占用保证金",
      "result.position_roe": "收益率",
      "result.market_sync": "市场同步",
      "result.market_source": "数据来源",
      "result.market_chart": "实时 K 线",
      "result.market_chart_empty": "图表数据加载中...",
      "result.market_chart_range": "区间",
      "result.market_chart_change": "波段",
      "result.market_chart_live": "实时 5m",
      "result.market_warning": "提示",
      "result.market_prices": "最新 / 买一 / 卖一",
      "result.market_stats": "波动 / 价差 / 深度",
      "result.market_suggested_trade": "建议开仓 / 止损 / 止盈",
      "result.next_step": "下一步",
      "result.order_check": "合约预下单校验",
      "result.order_status": "状态",
      "result.order_mode": "模式",
      "result.order_message": "说明",
      "result.order_opened_compact": "已开仓成功。",
      "result.order_opened_compact_hint": "仓位、保护单和当前委托状态已同步到当前仓位/委托。",
      "result.order_preview": "订单预览",
      "result.preview_qty": "预估数量",
      "result.order_credentials": "API 凭证",
      "result.exchange_minimums": "交易所最小值",
      "result.min_executable_qty": "最小可执行数量",
      "result.min_executable_notional": "最小可执行名义价值",
      "result.live_test_notional": "试跑名义金额",
      "result.live_order": "真实挂单",
      "result.cancel_result": "撤单结果",
      "result.execution_policy": "执行策略",
      "result.requested_margin_mode": "请求保证金模式",
      "result.requested_leverage": "请求杠杆",
      "result.requested_entry_price": "请求开仓价",
      "result.requested_notional": "请求持仓数量",
      "result.requested_margin": "请求保证金",
      "result.actual_execution_notional": "实际开单金额",
      "result.execution_notional_delta": "金额偏差",
      "result.execution_notional_delta_pct": "偏差比例",
      "result.execution_deviation_alert": "成交偏差预警",
      "result.execution_deviation_warn":
        "这次实际开单金额与目标金额存在明显偏差。下次开仓前建议检查开单金额或合约步进。",
      "result.execution_deviation_block":
        "这次实际开单金额与目标金额偏差过大。请先复核开单金额后再开下一单。",
      "result.estimated_execution_notional": "预计执行名义价值",
      "result.required_initial_margin": "所需初始保证金",
      "result.execution_reference_price": "执行参考价",
      "result.execution_details": "执行结果",
      "result.protection_orders": "保护单",
      "result.stop_loss_order": "止损保护单",
      "result.take_profit_order": "止盈保护单",
      "result.trigger_price": "触发价",
      "result.working_type": "触发基准",
      "result.close_all": "全平",
      "result.emergency_close": "应急平仓",
      "result.executed_qty": "实际成交数量",
      "result.avg_fill_price": "平均成交价",
      "result.exchange_leverage": "交易所杠杆",
      "result.exchange_margin_mode": "交易所保证金模式",
      "result.account_sync": "账户同步",
      "result.account_source": "账户来源",
      "result.account_connection": "连接状态",
      "result.account_equity": "合约总权益",
      "result.account_wallet": "合约钱包余额",
      "result.account_available": "可用 USDT",
      "result.account_locked": "冻结 USDT",
      "result.account_open_orders": "未成交订单",
      "result.account_behavior": "行为快照",
      "result.account_assets": "主要资产",
      "result.account_position_cap": "建议最大名义仓位",
      "result.account_risk_budget": "单笔风险预算",
      "result.agent_briefing": "Agent 简报",
      "result.agent_steps": "Agent 步骤",
      "metric.risk_per_trade_pct": "单笔止损风险",
      "metric.reward_risk_ratio": "实际盈亏比",
      "metric.target_reward_risk_ratio": "要求盈亏比",
      "metric.liquidation_buffer_pct": "预估清算缓冲",
      "metric.leverage_risk": "杠杆风险",
      "metric.volatility_risk": "波动风险",
      "metric.concentration_risk": "仓位集中风险",
      "metric.liquidity_risk": "流动性风险",
      "metric.behavior_risk": "行为风险",
      "decision.ALLOW": "放行",
      "decision.WARN": "预警",
      "decision.BLOCK": "拦截",
      "alert.profile_failed": "档位请求失败",
      "alert.account_sync_failed": "账户同步失败",
      "alert.market_sync_failed": "市场同步失败",
      "alert.evaluate_failed": "评估请求失败",
      "alert.order_test_failed": "合约预下单校验失败",
      "alert.live_order_failed": "真实下单试跑失败",
      "alert.live_open_order_failed": "真实开仓执行失败",
      "alert.cancel_current_orders_failed": "撤销当前委托失败",
      "alert.close_current_position_failed": "一键平仓失败",
      "alert.runtime_mismatch": "前后端版本未同步，交易相关操作已暂停，等待服务自动重载。",
      "alert.asset_mismatch": "检测到更新的演示页面，正在自动刷新。",
      "alert.execution_requires_profile": "请先确认风险档位，再进行真实执行。",
      "alert.execution_requires_evaluation": "请先完成交易评估，再进行真实执行。",
      "alert.execution_blocked": "当前交易已被风控拦截，请先修正参数再执行。",
      "alert.wizard_incomplete": "请先完成全部风险问答。",
      "alert.confirm_profile_first": "请先生成并确认档位，再进行交易评估。",
      "alert.no_profile_to_confirm": "请先生成档位，再点击确认。",
      "status.runtime_check": "正在检查运行时同步状态...",
      "status.market_loading": "正在同步 Binance 市场快照...",
      "status.order_loading": "正在校验 Binance USD-M Futures 订单预览...",
      "status.live_order_loading": "正在提交真实 USD-M Futures 限价单并立即撤单...",
      "status.live_open_order_loading": "正在提交真实 USD-M Futures 市价单，并挂出止损 / 止盈保护单...",
      "hint.next_profile": "下一步：先完成风险问答。",
      "hint.next_confirm_profile": "下一步：确认系统建议档位，解锁交易评估。",
      "hint.next_evaluate": "下一步：查看自动同步后的市场参数，然后点击“评估交易”。",
      "hint.next_apply_fix": "下一步：应用建议方案，再重新评估。",
      "hint.next_order_test": "下一步：点击合约预下单校验，展示执行准备情况。",
      "hint.next_live_order": "下一步：根据需要选择“真实挂单试跑（撤单）”或“真实开仓执行（保留仓位）”。",
      "step.profile": "风险档位",
      "step.account": "账户上下文",
      "step.market": "市场上下文",
      "step.evaluate": "交易决策",
      "step.order": "执行校验",
      "step.briefing": "Agent 简报",
      "step.profile.pending": "先完成 Agent 动态问答并确认系统建议档位。",
      "step.profile.done": "风险档位已确认。",
      "step.account.pending": "等待账户同步或本地回退上下文。",
      "step.account.done": "账户上下文已就绪。",
      "step.market.pending": "等待实时或本地市场快照。",
      "step.market.done": "市场快照已同步。",
      "step.evaluate.pending": "请先评估当前交易计划。",
      "step.evaluate.done": "交易决策已生成。",
      "step.order.pending": "交易不是拦截后，才能做订单校验。",
      "step.order.done": "订单预览或校验结果已生成。",
      "step.briefing.pending": "需要时点击更新，生成最新的日内开仓总结。",
      "step.briefing.done": "Agent 简报已更新到最新上下文。",
      "source.binance_spot_demo": "Binance Spot Demo Mode",
      "source.binance_spot_live": "Binance Spot API",
      "source.binance_futures_demo": "Binance USD-M Futures Testnet",
      "source.binance_futures_live": "Binance USD-M Futures API",
      "source.local_fallback": "本地回退数据（非实盘合约账户）",
      "mode.binance_spot_demo": "Binance Spot Demo Mode",
      "mode.binance_spot_live": "Binance Spot API",
      "mode.binance_futures_demo": "Binance USD-M Futures Testnet",
      "mode.binance_futures_live": "Binance USD-M Futures API",
      "mode.preview_only": "仅预览模式",
      "order_status.validated": "已通过校验",
      "order_status.placed_then_canceled": "已挂单并撤单",
      "order_status.opened": "已开仓",
      "order_status.protection_partial": "保护单部分成功",
      "order_status.protection_failed": "保护单失败",
      "order_status.cancel_failed": "撤单失败",
      "order_status.preview_invalid": "预览参数无效",
      "order_status.confirmation_required": "需要确认",
      "order_status.intent_preview_only": "做空意图仅预览",
      "order_status.not_configured": "仅预览",
      "order_status.network_unavailable": "网络不可用",
      "order_status.exchange_rejected": "被交易所拒绝",
      "confirm.live_order": "这会提交一笔真实 Binance USD-M Futures 限价单并立即撤单，是否继续？",
      "confirm.live_open_order": "这会提交一笔真实 Binance USD-M Futures 市价单，并立即挂出止损 / 止盈保护单，是否继续？",
      "confirm.cancel_current_orders": "这会撤销当前交易对的普通委托和保护单，是否继续？",
      "confirm.close_current_position": "这会用市价单平掉当前交易对仓位，是否继续？",
      "misc.configured": "已配置",
      "misc.missing": "未配置",
      "misc.na": "无",
      "misc.live_connected": "已连接实盘",
      "misc.demo_only": "未连接实盘，当前展示的是本地演示值",
    },
  };

  const SERVER_TEXT_EXACT_ZH = {
    "Risk profile is within acceptable range.": "风险状态处于可接受范围。",
    "Leverage risk is elevated for current guardrail profile.": "当前杠杆风险偏高。",
    "Market volatility is high; entry timing risk is elevated.": "市场波动较大，入场时机风险升高。",
    "Position concentration is high relative to account equity.": "仓位集中度相对账户权益偏高。",
    "Spread/depth conditions imply material slippage risk.":
      "价差与深度条件提示存在明显滑点风险。",
    "Behavior pattern suggests tilt/overtrading risk.": "行为模式显示有情绪化或过度交易风险。",
    "Stop-loss distance implies meaningful single-trade downside.":
      "止损距离意味着单笔潜在回撤较大。",
    "Liquidation buffer is narrow under current leverage.": "当前杠杆下清算缓冲较窄。",
    "Hard guardrail triggered. Apply suggested sizing before any execution.":
      "触发硬性风控护栏，请按建议缩仓后再执行。",
    "Trade blocked by model risk. Reduce leverage/size and retry.":
      "模型风险判定为拦截，请降低杠杆和仓位后重试。",
    "Trade allowed with warning. Use smaller sizing and tighter risk controls.":
      "可执行但预警，建议降低仓位并加强风险控制。",
    "Trade condition is acceptable under current guardrails.":
      "当前交易条件符合风控护栏。",
    "Strong stop-loss discipline.": "止损纪律较强。",
    "No recent loss streak detected.": "近期未出现连续亏损。",
    "Trading frequency is controlled.": "交易频率控制良好。",
    "Recent daily PnL is stable or positive.": "近期当日盈亏稳定或为正。",
    "You are actively engaging with risk controls.": "你正在积极使用风险控制。",
    "Revenge-trading tendency is high.": "报复性交易倾向偏高。",
    "Stop-loss execution discipline is inconsistent.": "止损执行纪律不稳定。",
    "Loss streak risk is elevated.": "连续亏损风险偏高。",
    "Overtrading pattern detected in last 24h.": "近24小时检测到过度交易模式。",
    "Current daily drawdown is significant.": "当前日内回撤较大。",
    "No critical behavior risk found.": "未发现关键行为风险。",
    "After two losses, enforce a 30-minute cooldown before new entries.":
      "连续两次亏损后，建议强制冷静30分钟再开新仓。",
    "Convert every entry into a bracket order with mandatory stop-loss.":
      "每次开仓都使用括号单并强制设置止损。",
    "Cut position size by 50% until one green day is recovered.":
      "在恢复一个盈利日之前，仓位先下调50%。",
    "Set a hard cap on intraday trades and disable entries after cap is hit.":
      "设定日内交易次数硬上限，达到后停止开仓。",
    "Switch to capital protection mode and only take A-grade setups.":
      "切换到资金保护模式，只做A类机会。",
    "Continue using the current guardrails and review weekly performance.":
      "继续使用当前护栏，并进行每周复盘。",
    "Severe drawdown detected, forced to conservative profile.":
      "检测到严重回撤，已强制切换为保守档位。",
    "Cooling mode activated due to losses, profile tightened by one level.":
      "因亏损触发冷静模式，档位已收紧一级。",
    "Overtrading under negative PnL detected, profile tightened.":
      "亏损状态下出现过度交易，档位已收紧。",
    "Binance Spot Demo Mode accepted the test order.":
      "Binance Spot Demo Mode 已接受该测试订单。",
    "Binance Spot API accepted the test order.": "Binance Spot API 已接受该测试订单。",
    "Binance USD-M Futures Testnet accepted the test order.":
      "Binance USD-M Futures Testnet 已接受该测试订单。",
    "Binance USD-M Futures API accepted the test order.":
      "Binance USD-M Futures API 已接受该测试订单。",
    "Set BINANCE_DEMO_API_KEY and BINANCE_DEMO_SECRET_KEY to enable Binance Spot Demo Mode order validation.":
      "请设置 BINANCE_DEMO_API_KEY 和 BINANCE_DEMO_SECRET_KEY，以启用 Binance Spot Demo Mode 订单校验。",
    "Set BINANCE_API_KEY and BINANCE_SECRET_KEY to enable Binance Spot API order validation.":
      "请设置 BINANCE_API_KEY 和 BINANCE_SECRET_KEY，以启用 Binance Spot API 订单校验。",
    "Set BINANCE_DEMO_API_KEY and BINANCE_DEMO_SECRET_KEY to enable Binance USD-M Futures Testnet order validation.":
      "请设置 BINANCE_DEMO_API_KEY 和 BINANCE_DEMO_SECRET_KEY，以启用 Binance USD-M Futures Testnet 订单校验。",
    "Set BINANCE_API_KEY and BINANCE_SECRET_KEY to enable Binance USD-M Futures API order validation.":
      "请设置 BINANCE_API_KEY 和 BINANCE_SECRET_KEY，以启用 Binance USD-M Futures API 订单校验。",
    "Connected to Binance Spot Demo Mode account context.":
      "已接入 Binance Spot Demo Mode 账户上下文。",
    "Connected to Binance Spot API account context.":
      "已接入 Binance Spot API 账户上下文。",
    "Connected to Binance USD-M Futures Testnet account context.":
      "已接入 Binance USD-M Futures Testnet 账户上下文。",
    "Connected to Binance USD-M Futures API account context.":
      "已接入 Binance USD-M Futures API 账户上下文。",
    "Using local fallback account context until spot demo credentials are configured.":
      "当前使用本地回退账户上下文，直到配置 Spot Demo 凭证为止。",
    "Using local fallback account context.": "当前使用本地回退账户上下文。",
    "Set BINANCE_DEMO_API_KEY and BINANCE_DEMO_SECRET_KEY to enable Binance Spot Demo Mode account sync.":
      "请设置 BINANCE_DEMO_API_KEY 和 BINANCE_DEMO_SECRET_KEY，以启用 Binance Spot Demo Mode 账户同步。",
    "Set BINANCE_API_KEY and BINANCE_SECRET_KEY to enable Binance Spot API account sync.":
      "请设置 BINANCE_API_KEY 和 BINANCE_SECRET_KEY，以启用 Binance Spot API 账户同步。",
    "Set BINANCE_DEMO_API_KEY and BINANCE_DEMO_SECRET_KEY to enable Binance USD-M Futures Testnet account sync.":
      "请设置 BINANCE_DEMO_API_KEY 和 BINANCE_DEMO_SECRET_KEY，以启用 Binance USD-M Futures Testnet 账户同步。",
    "Set BINANCE_API_KEY and BINANCE_SECRET_KEY to enable Binance USD-M Futures API account sync.":
      "请设置 BINANCE_API_KEY 和 BINANCE_SECRET_KEY，以启用 Binance USD-M Futures API 账户同步。",
    "Live execution requires explicit confirmation.": "真实下单需要显式确认。",
    "Placed a live Binance Spot API LIMIT_MAKER order and canceled it immediately.":
      "已在 Binance Spot API 提交一笔真实 LIMIT_MAKER 挂单，并已立即撤单。",
    "Placed a live Binance USD-M Futures API limit order and canceled it immediately.":
      "已在 Binance USD-M Futures API 提交一笔真实限价单，并已立即撤单。",
    "Placed a live Binance USD-M Futures Testnet limit order and canceled it immediately.":
      "已在 Binance USD-M Futures Testnet 提交一笔真实限价单，并已立即撤单。",
    "Placed a live Binance USD-M Futures API market order and kept the position open.":
      "已在 Binance USD-M Futures API 提交一笔真实市价单，并保留仓位。",
    "Placed a live Binance USD-M Futures Testnet market order and kept the position open.":
      "已在 Binance USD-M Futures Testnet 提交一笔真实市价单，并保留仓位。",
    "Placed a live Binance USD-M Futures API market order and posted stop-loss and take-profit protection orders.":
      "已在 Binance USD-M Futures API 提交真实市价单，并挂出止损和止盈保护单。",
    "Placed a live Binance USD-M Futures Testnet market order and posted stop-loss and take-profit protection orders.":
      "已在 Binance USD-M Futures Testnet 提交真实市价单，并挂出止损和止盈保护单。",
    "Position opened, but stop-loss protection failed. An emergency close order was submitted.":
      "仓位已开出，但止损保护单挂单失败，系统已提交应急平仓单。",
  };

  const state = {
    lang: "en",
    symbolCatalog: null,
    profileResult: null,
    tradeResult: null,
    marketSnapshot: null,
    accountSnapshot: null,
    orderTestResult: null,
    profileConfirmed: false,
    positionRatio: null,
    profileStatusMode: "await",
    profileStatusProfile: null,
    profileStatusScore: null,
    wizardStep: 0,
    wizardAnswers: {},
    initialWizardAnswers: {},
    marketSyncRequestId: 0,
    accountSyncRequestId: 0,
    profileRefreshTimer: null,
    profileRefreshRequestId: 0,
    profileIsProvisional: false,
    currentExposureActionResult: null,
    currentExposureActionPending: false,
    currentExposurePanelPinnedUntil: 0,
    orderActionPending: false,
    orderPanelPinnedUntil: 0,
    positionTrackerTimer: null,
    positionTrackerTarget: null,
    profileScoreDisplay: null,
    profileScoreAnimationFrame: null,
    positionNotionalMode: "preset",
    runtimeHealthReady: false,
    runtimeMismatch: false,
    runtimeServerVersion: "",
    runtimeWorkspaceVersion: "",
    runtimeAssetVersion: "",
    runtimeCheckedAt: 0,
    runtimeHealthTimer: null,
    agentBriefingManualRefreshAt: 0,
    agentBriefingRefreshing: false,
    agentBriefingError: "",
  };

  const ids = [
    "experience_level",
    "risk_tolerance",
    "leverage_preference",
    "stop_loss_discipline",
    "revenge_tendency",
    "trading_frequency",
    "max_drawdown_comfort_pct",
    "selected_profile",
    "consecutive_losses",
    "trades_last_24h",
    "day_pnl_pct",
    "symbol",
    "side",
    "entry_price",
    "stop_loss_price",
    "take_profit_price",
    "leverage",
    "margin_mode",
    "position_notional_usdt",
    "account_equity_usdt",
    "volatility_24h_pct",
    "bid_ask_spread_bps",
    "liquidity_depth_score",
  ];
  const profileInputIds = [
    "experience_level",
    "risk_tolerance",
    "leverage_preference",
    "stop_loss_discipline",
    "revenge_tendency",
    "trading_frequency",
    "max_drawdown_comfort_pct",
    "selected_profile",
    "consecutive_losses",
    "trades_last_24h",
    "day_pnl_pct",
  ];
  const tradeInputIds = [
    "symbol",
    "side",
    "entry_price",
    "stop_loss_price",
    "take_profit_price",
    "leverage",
    "margin_mode",
    "position_notional_usdt",
    "account_equity_usdt",
    "volatility_24h_pct",
    "bid_ask_spread_bps",
    "liquidity_depth_score",
    "consecutive_losses",
    "trades_last_24h",
    "day_pnl_pct",
  ];
  const uiIds = [
    "btn-prev-step",
    "btn-reset-wizard",
    "btn-confirm-profile",
    "btn-evaluate",
    "btn-order-test",
    "btn-live-order",
    "btn-live-open-order",
    "btn-view-current-exposure",
    "btn-apply-fix",
    "position-ratio-group",
    "profile-confirm-status",
    "wizard-progress",
    "wizard-log",
    "wizard-question",
    "wizard-context",
    "wizard-options",
    "lang-zh",
    "lang-en",
    "market-sync-status",
    "order-test-result",
    "current-exposure-status",
    "account-sync-status",
    "agent-status-chip",
    "agent-stepper",
    "agent-briefing",
  ];
  const SYMBOL_LABEL_KEYS = {
    BNBUSDT: "token.bnb",
    BTCUSDT: "token.btc",
    ETHUSDT: "token.eth",
  };
  const TOKEN_PRESETS = {
    BNBUSDT: {
      entry_price: 640,
      stop_loss_price: 626,
      take_profit_price: 668,
      leverage: 9,
      margin_mode: "CROSSED",
      position_notional_usdt: 1100,
      account_equity_usdt: 2200,
      volatility_24h_pct: 5.1,
      bid_ask_spread_bps: 4,
      liquidity_depth_score: 88,
    },
    BTCUSDT: {
      entry_price: 91300,
      stop_loss_price: 90000,
      take_profit_price: 93900,
      leverage: 8,
      margin_mode: "CROSSED",
      position_notional_usdt: 2400,
      account_equity_usdt: 4000,
      volatility_24h_pct: 3.8,
      bid_ask_spread_bps: 2.5,
      liquidity_depth_score: 95,
    },
    ETHUSDT: {
      entry_price: 4700,
      stop_loss_price: 4620,
      take_profit_price: 4860,
      leverage: 10,
      margin_mode: "CROSSED",
      position_notional_usdt: 1600,
      account_equity_usdt: 2500,
      volatility_24h_pct: 5.7,
      bid_ask_spread_bps: 3.5,
      liquidity_depth_score: 90,
    },
  };

  const POSITION_RATIO_OPTIONS = [0.1, 0.3, 0.5, 0.7, 1];

  function defaultSymbolCatalog() {
    return Object.keys(TOKEN_PRESETS).map((symbol) => ({
      symbol,
      label: symbol.replace(/USDT$/, ""),
      profiles: [],
    }));
  }

  function frequencyBucketFromTrades(trades) {
    const n = Number(trades);
    if (!Number.isFinite(n)) {
      return "";
    }
    if (n <= 3) {
      return "low";
    }
    if (n <= 10) {
      return "medium";
    }
    return "high";
  }

  function hasLiveAccountSnapshot(snapshot = state.accountSnapshot) {
    return Boolean(snapshot && snapshot.connected && snapshot.live && snapshot.source !== "local_fallback");
  }

  function runtimeMismatchText() {
    const server = state.runtimeServerVersion || t("misc.na");
    const workspace = state.runtimeWorkspaceVersion || t("misc.na");
    return `${t("alert.runtime_mismatch")} (${server} -> ${workspace})`;
  }

  function orderTickerMessageText(message) {
    return String(message || "")
      .replace(/\s+/g, " ")
      .trim();
  }

  function orderTickerDuration(message) {
    const text = orderTickerMessageText(message);
    const units = Array.from(text).length;
    const seconds = Math.max(16, Math.min(34, Math.round(units * 0.24)));
    return `${seconds}s`;
  }

  function renderOrderTicker(message, statusClass = "warn") {
    const box = byId("order-test-result");
    const text = orderTickerMessageText(message) || t("placeholder.order_test");
    box.classList.remove("muted");
    box.classList.remove("ticker-ok", "ticker-warn", "ticker-block");
    box.classList.add("order-ticker-shell", `ticker-${statusClass}`);
    box.innerHTML = `
      <div class="order-ticker-lane" style="--ticker-duration:${escapeHtml(orderTickerDuration(text))}">
        <div class="order-ticker-track">
          <span class="order-ticker-copy">${escapeHtml(text)}</span>
          <span class="order-ticker-sep" aria-hidden="true">◆</span>
          <span class="order-ticker-copy" aria-hidden="true">${escapeHtml(text)}</span>
        </div>
      </div>
    `;
  }

  function setOrderTestStatus(message, statusClass = "warn") {
    renderOrderTicker(message, statusClass);
  }

  function pinOrderPanel(ms = 0) {
    const duration = Number(ms);
    if (!Number.isFinite(duration) || duration <= 0) {
      return;
    }
    state.orderPanelPinnedUntil = Math.max(
      Number(state.orderPanelPinnedUntil || 0),
      Date.now() + duration
    );
  }

  function shouldPreserveOrderPanel() {
    return state.orderActionPending || Date.now() < Number(state.orderPanelPinnedUntil || 0);
  }

  function pinCurrentExposurePanel(ms = 0) {
    const duration = Number(ms);
    if (!Number.isFinite(duration) || duration <= 0) {
      return;
    }
    state.currentExposurePanelPinnedUntil = Math.max(
      Number(state.currentExposurePanelPinnedUntil || 0),
      Date.now() + duration
    );
  }

  function shouldPreserveCurrentExposurePanel() {
    return (
      state.currentExposureActionPending ||
      Date.now() < Number(state.currentExposurePanelPinnedUntil || 0)
    );
  }

  function setCurrentExposurePending(message, statusClass = "warn") {
    state.currentExposureActionPending = true;
    pinCurrentExposurePanel(10000);
    const box = byId("current-exposure-status");
    box.classList.remove("muted");
    box.innerHTML = `
      <div class="status-head ${statusClass}">
        ${escapeHtml(t("result.current_exposure"))}
      </div>
      <div class="card">${escapeHtml(message)}</div>
    `;
  }

  function clearCurrentExposurePending({ keepPinnedMs = 3500 } = {}) {
    state.currentExposureActionPending = false;
    pinCurrentExposurePanel(keepPinnedMs);
  }

  function accountBehaviorSignals() {
    const autoFill = hasLiveAccountSnapshot() ? state.accountSnapshot.auto_fill || {} : {};
    const agentContext = hasLiveAccountSnapshot() ? state.accountSnapshot.agent_context || {} : {};
    const trades = Number(autoFill.trades_last_24h);
    const losses = Number(autoFill.consecutive_losses);
    const pnl = Number(autoFill.day_pnl_pct);
    const ready = Number.isFinite(trades) && Number.isFinite(losses) && Number.isFinite(pnl);
    const behaviorStatus = String(agentContext.behavior_status || "");
    const frequencyBucket = ready ? frequencyBucketFromTrades(trades) : "";
    const highAlert =
      ready &&
      (behaviorStatus === "high_alert" || losses >= 3 || pnl <= -5 || trades >= 18);
    const elevated =
      ready &&
      (highAlert || behaviorStatus === "elevated" || losses >= 1 || pnl < 0 || trades >= 8);
    const stable =
      ready &&
      !elevated &&
      (behaviorStatus === "stable" || (losses === 0 && pnl >= 0 && trades <= 5));
    return {
      ready,
      trades,
      losses,
      pnl,
      behaviorStatus,
      frequencyBucket,
      highAlert,
      elevated,
      stable,
    };
  }

  function resolvedTradingFrequency(answers) {
    const explicit = String(answers.trading_frequency || "");
    if (explicit) {
      return explicit;
    }
    return accountBehaviorSignals().frequencyBucket || "";
  }

  function shouldAskTradingFrequency() {
    return !accountBehaviorSignals().ready;
  }

  function deriveTradingFrequency() {
    return accountBehaviorSignals().frequencyBucket || "medium";
  }

  function shouldAskLeverage(answers) {
    const experience = String(answers.experience_level || "");
    const risk = String(answers.risk_tolerance || "");
    const frequency = resolvedTradingFrequency(answers);
    return (
      experience === "intermediate" ||
      experience === "advanced" ||
      risk === "medium" ||
      risk === "high" ||
      frequency === "medium" ||
      frequency === "high"
    );
  }

  function deriveLeveragePreference(answers) {
    const experience = String(answers.experience_level || "");
    const risk = String(answers.risk_tolerance || "");
    const frequency = resolvedTradingFrequency(answers);
    if (risk === "high") {
      return "high";
    }
    if (risk === "medium" || frequency === "high" || experience === "advanced") {
      return "medium";
    }
    return "low";
  }

  function shouldAskRevengeTendency(answers) {
    const signals = accountBehaviorSignals();
    const risk = String(answers.risk_tolerance || "");
    const frequency = resolvedTradingFrequency(answers);
    const stopLoss = String(answers.stop_loss_discipline || "");
    return (
      stopLoss === "sometimes" ||
      stopLoss === "rarely" ||
      risk === "high" ||
      frequency === "high" ||
      signals.highAlert ||
      (signals.elevated && risk !== "low")
    );
  }

  function deriveRevengeTendency(answers) {
    const signals = accountBehaviorSignals();
    const experience = String(answers.experience_level || "");
    const risk = String(answers.risk_tolerance || "");
    const frequency = resolvedTradingFrequency(answers);
    const stopLoss = String(answers.stop_loss_discipline || "");
    if (signals.highAlert && stopLoss !== "always") {
      return "often";
    }
    if (signals.elevated && (stopLoss === "sometimes" || stopLoss === "rarely")) {
      return "often";
    }
    if (signals.elevated) {
      return "sometimes";
    }
    if (signals.stable && stopLoss === "always" && risk === "low") {
      return "never";
    }
    if (stopLoss === "always" && risk === "low" && frequency === "low") {
      return "never";
    }
    if (
      stopLoss === "always" &&
      (risk === "medium" || frequency === "medium" || experience === "advanced")
    ) {
      return "sometimes";
    }
    if (stopLoss === "rarely" && (risk === "high" || frequency === "high")) {
      return "often";
    }
    return "sometimes";
  }

  const QUESTION_BANK = [
    {
      id: "experience_level",
      questionKey: "wizard.q.experience",
      labelKey: "field.experience_level",
      options: [
        { value: "beginner", labelKey: "wizard.opt.experience.beginner" },
        { value: "intermediate", labelKey: "wizard.opt.experience.intermediate" },
        { value: "advanced", labelKey: "wizard.opt.experience.advanced" },
      ],
    },
    {
      id: "trading_frequency",
      questionKey: "wizard.q.trading_frequency",
      labelKey: "field.trading_frequency",
      includeWhen: shouldAskTradingFrequency,
      deriveValue: deriveTradingFrequency,
      options: [
        { value: "low", labelKey: "wizard.opt.frequency.low" },
        { value: "medium", labelKey: "wizard.opt.frequency.medium" },
        { value: "high", labelKey: "wizard.opt.frequency.high" },
      ],
    },
    {
      id: "risk_tolerance",
      questionKey: "wizard.q.risk_tolerance",
      labelKey: "field.risk_tolerance",
      options: [
        { value: "low", labelKey: "wizard.opt.risk.low" },
        { value: "medium", labelKey: "wizard.opt.risk.medium" },
        { value: "high", labelKey: "wizard.opt.risk.high" },
      ],
    },
    {
      id: "leverage_preference",
      questionKey: "wizard.q.leverage_preference",
      labelKey: "field.leverage_preference",
      includeWhen: shouldAskLeverage,
      deriveValue: deriveLeveragePreference,
      options: [
        { value: "low", labelKey: "wizard.opt.leverage.low" },
        { value: "medium", labelKey: "wizard.opt.leverage.medium" },
        { value: "high", labelKey: "wizard.opt.leverage.high" },
      ],
    },
    {
      id: "stop_loss_discipline",
      questionKey: "wizard.q.stop_loss_discipline",
      labelKey: "field.stop_loss_discipline",
      options: [
        { value: "always", labelKey: "wizard.opt.stop.always" },
        { value: "sometimes", labelKey: "wizard.opt.stop.sometimes" },
        { value: "rarely", labelKey: "wizard.opt.stop.rarely" },
      ],
    },
    {
      id: "revenge_tendency",
      questionKey: "wizard.q.revenge_tendency",
      labelKey: "field.revenge_tendency",
      includeWhen: shouldAskRevengeTendency,
      deriveValue: deriveRevengeTendency,
      options: [
        { value: "never", labelKey: "wizard.opt.revenge.never" },
        { value: "sometimes", labelKey: "wizard.opt.revenge.sometimes" },
        { value: "often", labelKey: "wizard.opt.revenge.often" },
      ],
    },
    {
      id: "max_drawdown_comfort_pct",
      questionKey: "wizard.q.max_drawdown",
      labelKey: "field.max_drawdown_comfort_pct",
      options: [
        { value: "5", labelKey: "opt.dd_5" },
        { value: "8", labelKey: "opt.dd_8" },
        { value: "12", labelKey: "opt.dd_12" },
      ],
    },
  ];

  function byId(id) {
    return document.getElementById(id);
  }

  function t(key) {
    return I18N[state.lang][key] || I18N.en[key] || key;
  }

  function escapeHtml(value) {
    return String(value)
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;")
      .replaceAll("'", "&#39;");
  }

  function toNumber(id) {
    return Number(byId(id).value);
  }

  function toOptionalNumber(id) {
    const raw = String(byId(id).value ?? "").trim();
    return raw === "" ? null : Number(raw);
  }

  function normalizeLeverageInput() {
    const input = byId("leverage");
    if (!input) {
      return 1;
    }
    const raw = String(input.value ?? "").trim();
    let nextValue = Number(raw);
    if (!Number.isFinite(nextValue)) {
      nextValue = 1;
    }
    nextValue = Math.round(nextValue);
    nextValue = Math.min(125, Math.max(1, nextValue));
    input.value = String(nextValue);
    updatePositionMarginField();
    return nextValue;
  }

  function leverageInputValue({ normalize = false } = {}) {
    if (normalize) {
      return normalizeLeverageInput();
    }
    const raw = String(byId("leverage").value ?? "").trim();
    const value = Number(raw);
    return Number.isFinite(value) && value > 0 ? value : Number.NaN;
  }

  function computePositionMarginValue() {
    const notional = toOptionalNumber("position_notional_usdt");
    const leverage = leverageInputValue();
    if (!Number.isFinite(notional) || !Number.isFinite(leverage) || leverage <= 0) {
      return null;
    }
    return Number(notional) / Number(leverage);
  }

  function updatePositionMarginField() {
    const input = byId("position_margin_usdt");
    if (!input) {
      return;
    }
    const margin = computePositionMarginValue();
    input.value = Number.isFinite(margin) ? formatEditableNotional(margin) : "";
  }

  function updateDecisionSignalPanel() {
    const card = byId("decision-signal-card");
    const valueEl = byId("decision-signal-display");
    const badgeEl = byId("decision-signal-badge");
    const metaEl = byId("decision-signal-meta");
    const fillEl = byId("decision-signal-fill");
    if (!card || !valueEl || !badgeEl || !metaEl || !fillEl) {
      return;
    }
    const result = state.tradeResult;
    if (!result) {
      card.classList.remove("allow", "warn", "block");
      card.classList.add("pending");
      valueEl.textContent = "--";
      badgeEl.textContent = t("result.await_evaluation");
      metaEl.textContent = `${t("result.decision")}: ${t("result.await_evaluation")} | ${t(
        "result.risk_score"
      )}: --`;
      fillEl.style.width = "0%";
      return;
    }
    const score = Number(result.risk_score);
    const tone = decisionClass(result.decision);
    card.classList.remove("pending", "allow", "warn", "block");
    card.classList.add(tone);
    valueEl.textContent = Number.isFinite(score) ? formatScore(score) : t("misc.na");
    badgeEl.textContent = translateDecision(result.decision);
    metaEl.textContent = `${t("result.decision")}: ${translateDecision(result.decision)} | ${t(
      "result.risk_score"
    )}: ${Number.isFinite(score) ? formatScore(score) : t("misc.na")}`;
    fillEl.style.width = `${Math.max(0, Math.min(Number.isFinite(score) ? score : 0, 100))}%`;
  }

  function setValue(id, value) {
    byId(id).value = value === null || value === undefined ? "" : String(value);
    if (id === "position_notional_usdt" || id === "leverage") {
      updatePositionMarginField();
    }
  }

  function formatMetric(value, suffix = "") {
    const n = Number(value);
    if (Number.isNaN(n)) {
      return t("misc.na");
    }
    if (suffix === "x") {
      return `${n.toFixed(2)}x`;
    }
    if (suffix === "%") {
      return `${n.toFixed(2)}%`;
    }
    return n.toFixed(2);
  }

  function translateProfileName(name) {
    if (!name) return t("misc.na");
    const key = `profile.${String(name).toLowerCase()}`;
    return t(key);
  }

  function translateDecision(decision) {
    return t(`decision.${decision}`) || decision;
  }

  function formatTemplate(key, vars = {}) {
    let value = t(key);
    Object.entries(vars).forEach(([name, content]) => {
      value = value.replaceAll(`{${name}}`, String(content));
    });
    return value;
  }

  function formatScore(value) {
    const n = Number(value);
    if (Number.isNaN(n)) {
      return t("misc.na");
    }
    return n.toFixed(1);
  }

  function formatCurrency(value) {
    const n = Number(value);
    if (Number.isNaN(n)) {
      return t("misc.na");
    }
    return `${n.toFixed(2)} USDT`;
  }

  function buildLiveOpenOrderConfirmText() {
    const trade = evaluatePayload().trade;
    const preview = (state.orderTestResult && state.orderTestResult.preview) || {};
    const lines = [t("confirm.live_open_order")];
    lines.push(`${t("field.symbol")}: ${trade.symbol}`);
    lines.push(`${t("field.side")}: ${trade.side}`);
    lines.push(`${t("result.requested_margin_mode")}: ${marginModeLabel(trade.margin_mode)}`);
    lines.push(`${t("result.requested_leverage")}: ${formatMetric(trade.leverage, "x")}`);
    lines.push(`${t("result.requested_notional")}: ${formatCurrency(trade.position_notional_usdt)}`);
    if (preview.quantity) {
      lines.push(`${t("result.preview_qty")}: ${preview.quantity}`);
    }
    if (preview.price) {
      lines.push(`${t("field.entry_price")}: ${preview.price}`);
    }
    return lines.join("\n");
  }

  function symbolCatalog() {
    return Array.isArray(state.symbolCatalog) && state.symbolCatalog.length
      ? state.symbolCatalog
      : defaultSymbolCatalog();
  }

  function symbolOptionLabel(item) {
    const symbol = String(item.symbol || "").toUpperCase();
    const labelKey = SYMBOL_LABEL_KEYS[symbol];
    if (labelKey) {
      return t(labelKey);
    }
    return item.label || symbol.replace(/USDT$/, "") || symbol;
  }

  function renderSymbolSelect() {
    const select = byId("symbol");
    if (!select) {
      return;
    }
    const currentValue = String(select.value || "BNBUSDT").toUpperCase();
    const options = symbolCatalog();
    const nextValue = options.some((item) => item.symbol === currentValue)
      ? currentValue
      : String(options[0]?.symbol || "BNBUSDT").toUpperCase();

    select.innerHTML = options
      .map((item) => {
        const symbol = String(item.symbol || "").toUpperCase();
        const profiles = Array.isArray(item.profiles) ? item.profiles.join(",") : "";
        const title = profiles ? ` title="${escapeHtml(profiles)}"` : "";
        return `<option value="${escapeHtml(symbol)}"${title}>${escapeHtml(
          symbolOptionLabel(item)
        )}</option>`;
      })
      .join("");
    select.value = nextValue;
  }

  async function loadSymbolCatalog() {
    try {
      const data = await getJSON("/v1/catalog/symbols");
      if (Array.isArray(data.symbols) && data.symbols.length > 0) {
        state.symbolCatalog = data.symbols
          .map((item) => ({
            symbol: String(item.symbol || "").toUpperCase(),
            label: String(item.label || ""),
            profiles: Array.isArray(item.profiles)
              ? item.profiles.map((profile) => String(profile))
              : [],
          }))
          .filter((item) => item.symbol);
      } else {
        state.symbolCatalog = null;
      }
    } catch (err) {
      state.symbolCatalog = null;
    }
    renderSymbolSelect();
  }

  function activeWizardSteps(answers = state.wizardAnswers) {
    return QUESTION_BANK.filter(
      (step) => typeof step.includeWhen !== "function" || step.includeWhen(answers)
    );
  }

  function restoreInitialWizardFormValues() {
    QUESTION_BANK.forEach((step) => {
      setValue(step.id, state.initialWizardAnswers[step.id]);
    });
  }

  function syncWizardFormValues() {
    const activeIds = new Set(activeWizardSteps().map((step) => step.id));
    QUESTION_BANK.forEach((step) => {
      const answer = String(state.wizardAnswers[step.id] || "").trim();
      let nextValue = answer;
      if (!answer && !activeIds.has(step.id) && typeof step.deriveValue === "function") {
        nextValue = step.deriveValue(state.wizardAnswers);
      }
      if (!nextValue) {
        nextValue = state.initialWizardAnswers[step.id] || String(step.options[0].value);
      }
      setValue(step.id, nextValue);
    });
    setValue("selected_profile", "");
  }

  function syncWizardPathState() {
    const activeIds = new Set(activeWizardSteps().map((step) => step.id));
    QUESTION_BANK.forEach((step) => {
      if (!activeIds.has(step.id)) {
        state.wizardAnswers[step.id] = "";
      }
    });
    syncWizardFormValues();
    const total = activeWizardSteps().length;
    state.wizardStep = total === 0 ? 0 : Math.min(Math.max(state.wizardStep, 0), total - 1);
  }

  function currentFlowHintKey() {
    if (!allWizardAnswered()) {
      return "hint.next_profile";
    }
    if (!state.profileConfirmed) {
      return state.profileResult ? "hint.next_confirm_profile" : "status.loading_profile";
    }
    if (!state.tradeResult) {
      return "hint.next_evaluate";
    }
    if (state.tradeResult.decision === "BLOCK" && state.tradeResult.suggested_plan) {
      return "hint.next_apply_fix";
    }
    if (state.orderTestResult && state.orderTestResult.ok && state.orderTestResult.status === "validated") {
      return "hint.next_live_order";
    }
    return "hint.next_order_test";
  }

  function updateActionState() {
    const runtimeBlocked = !state.runtimeHealthReady || state.runtimeMismatch;
    const orderBusy = Boolean(state.orderActionPending);
    const canConfirm = Boolean(
      state.profileResult && !state.profileConfirmed && !state.profileIsProvisional && allWizardAnswered()
    );
    const canEvaluate = Boolean(state.profileConfirmed && state.profileResult);
    const canApplyFix = Boolean(state.tradeResult && state.tradeResult.suggested_plan);
    const canOrderTest = Boolean(state.profileConfirmed && state.profileResult);
    const canLiveExecution = Boolean(state.profileConfirmed && state.profileResult);

    byId("btn-confirm-profile").disabled = runtimeBlocked || orderBusy || !canConfirm;
    byId("btn-evaluate").disabled = runtimeBlocked || orderBusy || !canEvaluate;
    byId("btn-apply-fix").disabled = runtimeBlocked || orderBusy || !canApplyFix;
    byId("btn-order-test").disabled = runtimeBlocked || orderBusy || !canOrderTest;
    byId("btn-live-order").disabled = runtimeBlocked || orderBusy || !canLiveExecution;
    byId("btn-live-open-order").disabled = runtimeBlocked || orderBusy || !canLiveExecution;
    byId("btn-view-current-exposure").disabled = runtimeBlocked || orderBusy;
  }

  function setOrderActionPending(message, statusClass = "warn") {
    state.orderActionPending = true;
    pinOrderPanel(10000);
    renderOrderTicker(message, statusClass);
    updateActionState();
  }

  function clearOrderActionPending({ keepPinnedMs = 4500 } = {}) {
    state.orderActionPending = false;
    pinOrderPanel(keepPinnedMs);
    updateActionState();
  }

  function agentStatusKey() {
    if (state.runtimeMismatch) {
      return "agent.status_desynced";
    }
    if (!state.runtimeHealthReady) {
      return "agent.status_booting";
    }
    if (!state.profileConfirmed) {
      return state.profileResult ? "agent.status_profile" : "agent.status_syncing";
    }
    if (state.tradeResult && state.tradeResult.decision === "BLOCK") {
      return "agent.status_repair";
    }
    if (state.orderTestResult) {
      return state.orderTestResult.ok ? "agent.status_execution" : "agent.status_preview";
    }
    if (state.tradeResult) {
      return "agent.status_ready";
    }
    return "agent.status_ready";
  }

  function renderAgentStatusChip() {
    const chip = byId("agent-status-chip");
    chip.classList.remove("muted", "warn", "ok");
    const key = agentStatusKey();
    const isOk =
      key === "agent.status_execution" || key === "agent.status_ready";
    const isWarn =
      key === "agent.status_desynced" ||
      key === "agent.status_profile" ||
      key === "agent.status_preview" ||
      key === "agent.status_syncing";
    chip.classList.add(isOk ? "ok" : isWarn ? "warn" : "muted");
    chip.textContent = t(key);
  }

  function agentStepsData() {
    return [
      {
        key: "step.profile",
        done: Boolean(state.profileConfirmed),
        active: !state.profileConfirmed,
        noteKey: state.profileConfirmed ? "step.profile.done" : "step.profile.pending",
      },
      {
        key: "step.account",
        done: Boolean(state.accountSnapshot),
        active: Boolean(!state.accountSnapshot && state.profileConfirmed),
        noteKey: state.accountSnapshot ? "step.account.done" : "step.account.pending",
      },
      {
        key: "step.market",
        done: Boolean(state.marketSnapshot),
        active: Boolean(!state.marketSnapshot && state.profileConfirmed),
        noteKey: state.marketSnapshot ? "step.market.done" : "step.market.pending",
      },
      {
        key: "step.evaluate",
        done: Boolean(state.tradeResult),
        active: Boolean(state.profileConfirmed && !state.tradeResult),
        noteKey: state.tradeResult ? "step.evaluate.done" : "step.evaluate.pending",
      },
      {
        key: "step.order",
        done: Boolean(state.orderTestResult),
        active: Boolean(state.tradeResult && !state.orderTestResult),
        noteKey: state.orderTestResult ? "step.order.done" : "step.order.pending",
      },
      {
        key: "step.briefing",
        done: Boolean(state.agentBriefingManualRefreshAt),
        active: Boolean(
          !state.agentBriefingManualRefreshAt &&
            (state.accountSnapshot || state.tradeResult || state.orderTestResult)
        ),
        noteKey: state.agentBriefingManualRefreshAt
          ? "step.briefing.done"
          : "step.briefing.pending",
      },
    ];
  }

  function renderAgentSteps() {
    const box = byId("agent-stepper");
    box.classList.remove("muted");
    const items = agentStepsData()
      .map(
        (item, index) => `
          <div class="agent-step${item.done ? " done" : ""}${item.active ? " active" : ""}">
            <span class="agent-step-num">${index + 1}</span>
            <div class="agent-step-copy">
              <span class="agent-step-title">${escapeHtml(t(item.key))}</span>
              <span class="agent-step-note">${escapeHtml(t(item.noteKey))}</span>
            </div>
          </div>
        `
      )
      .join("");
    box.innerHTML = `
      <h3>${escapeHtml(t("result.agent_steps"))}</h3>
      <div class="agent-steps">${items}</div>
    `;
  }

  function livePositionSummaryLine(snapshot) {
    const account = snapshot?.account || {};
    const positions = Array.isArray(account.open_positions) ? account.open_positions : [];
    if (!positions.length) {
      return null;
    }
    const summarized = positions
      .slice(0, 2)
      .map((item) => {
        const symbol = String(item.symbol || "");
        const side = trackedPositionSideLabel(item);
        const notional = formatCurrency(item.notional_usdt);
        return `${symbol} ${side} ${notional}`;
      })
      .join(" | ");
    return state.lang === "zh"
      ? `当前活跃仓位 ${positions.length} 个：${summarized}`
      : `${positions.length} active positions: ${summarized}`;
  }

  function agentBriefingLines() {
    const lines = [];
    if (state.runtimeMismatch) {
      lines.push(runtimeMismatchText());
      return lines;
    }
    if (!state.runtimeHealthReady) {
      lines.push(t("status.runtime_check"));
      return lines;
    }

    if (state.accountSnapshot && !hasLiveAccountSnapshot(state.accountSnapshot)) {
      lines.push(t("misc.demo_only"));
      lines.push(
        translateServerText(String(state.accountSnapshot.warning || "")) || t("placeholder.account_sync")
      );
    } else if (state.accountSnapshot) {
      const account = state.accountSnapshot.account || {};
      const behavior = state.accountSnapshot.behavior || {};
      const trades = behavior.trades_last_24h ?? t("misc.na");
      const pnl = formatMetric(behavior.day_pnl_pct, "%");
      const losses = behavior.consecutive_losses ?? t("misc.na");
      const wallet = formatCurrency(account.wallet_balance_usdt);
      const available = formatCurrency(account.available_usdt);
      const openOrders = account.open_orders_count ?? t("misc.na");
      lines.push(
        state.lang === "zh"
          ? `日内开仓概况：近24小时 ${trades} 笔，当日盈亏 ${pnl}，连续亏损 ${losses} 次。`
          : `Daily summary: ${trades} trades in the last 24h, day PnL ${pnl}, loss streak ${losses}.`
      );
      lines.push(
        state.lang === "zh"
          ? `账户可用情况：合约钱包余额 ${wallet}，可用保证金 ${available}，未成交委托 ${openOrders} 个。`
          : `Account context: futures wallet ${wallet}, available balance ${available}, ${openOrders} open orders.`
      );
      const positionLine = livePositionSummaryLine(state.accountSnapshot);
      if (positionLine) {
        lines.push(positionLine);
      }
    } else {
      lines.push(t(currentFlowHintKey()));
    }

    if (state.marketSnapshot?.market) {
      const market = state.marketSnapshot.market;
      const symbol = byId("symbol").value.toUpperCase();
      lines.push(
        state.lang === "zh"
          ? `${symbol} 最新价 ${formatMetric(market.last_price)}，24h 波动 ${formatMetric(
              market.volatility_24h_pct,
              "%"
            )}。`
          : `${symbol} last price ${formatMetric(market.last_price)}, 24h volatility ${formatMetric(
              market.volatility_24h_pct,
              "%"
            )}.`
      );
    }

    if (state.tradeResult) {
      lines.push(
        state.lang === "zh"
          ? `当前交易评估：${translateDecision(state.tradeResult.decision)}，风险分 ${state.tradeResult.risk_score}。`
          : `Trade decision: ${translateDecision(state.tradeResult.decision)}, risk score ${state.tradeResult.risk_score}.`
      );
    }

    if (state.orderTestResult) {
      lines.push(
        state.lang === "zh"
          ? `执行准备：${orderStatusLabel(state.orderTestResult.status)}。`
          : `Execution readiness: ${orderStatusLabel(state.orderTestResult.status)}.`
      );
    }

    if (state.agentBriefingError) {
      lines.unshift(state.agentBriefingError);
    }

    return lines;
  }

  function currentProfileName() {
    if (state.profileResult && state.profileResult.profile) {
      return state.profileResult.profile;
    }
    return "balanced";
  }

  function marketSourceLabel(source) {
    return t(`source.${source}`) || source || t("misc.na");
  }

  function benchmarkSymbolLabel(symbol) {
    const normalized = String(symbol || "").toUpperCase();
    const labelKey = SYMBOL_LABEL_KEYS[normalized];
    if (labelKey) {
      return t(labelKey);
    }
    return normalized.replace(/USDT$/, "") || normalized || t("misc.na");
  }

  function marketSwitchSymbols(data) {
    const market = data.market || {};
    const benchmarks = Array.isArray(data.benchmarks) ? data.benchmarks : [];
    const priceMap = new Map();
    priceMap.set(String(data.symbol || "").toUpperCase(), Number(market.last_price || 0));
    benchmarks.forEach((item) => {
      const symbol = String(item.symbol || "").toUpperCase();
      if (symbol) {
        priceMap.set(symbol, Number(item.last_price || 0));
      }
    });
    return ["BTCUSDT", "BNBUSDT", "ETHUSDT"]
      .filter((symbol) => priceMap.has(symbol))
      .map((symbol) => ({
        symbol,
        lastPrice: priceMap.get(symbol),
      }));
  }

  function orderStatusLabel(status) {
    return t(`order_status.${status}`) || status || t("misc.na");
  }

  function orderModeLabel(mode) {
    return t(`mode.${mode}`) || mode || t("misc.na");
  }

  function marginModeLabel(mode) {
    const normalized = String(mode || "").toLowerCase();
    if (normalized === "crossed") {
      return t("opt.crossed");
    }
    if (normalized === "isolated") {
      return t("opt.isolated");
    }
    return mode || t("misc.na");
  }

  function formatEditableNotional(value) {
    const n = Number(value);
    if (!Number.isFinite(n)) {
      return "";
    }
    return String(Math.round(n * 100) / 100);
  }

  function renderPositionRatioButtons() {
    const group = byId("position-ratio-group");
    if (!group) {
      return;
    }
    const equity = toOptionalNumber("account_equity_usdt");
    const canUse = Number.isFinite(equity) && Number(equity) > 0;
    group.querySelectorAll("[data-ratio]").forEach((button) => {
      const ratio = Number(button.dataset.ratio || "");
      const active = Number.isFinite(ratio) && state.positionRatio === ratio;
      button.disabled = !canUse;
      button.classList.toggle("active", active);
    });
  }

  function syncPositionRatioFromForm() {
    const equity = toOptionalNumber("account_equity_usdt");
    const margin = computePositionMarginValue();
    if (!Number.isFinite(equity) || Number(equity) <= 0 || !Number.isFinite(margin)) {
      state.positionRatio = null;
      renderPositionRatioButtons();
      return;
    }
    const ratio = Number(margin) / Number(equity);
    const matched = POSITION_RATIO_OPTIONS.find((candidate) => Math.abs(candidate - ratio) < 0.005);
    state.positionRatio = matched ?? null;
    renderPositionRatioButtons();
  }

  function applyPositionRatio(ratio, { reset = true } = {}) {
    const equity = toOptionalNumber("account_equity_usdt");
    const leverage = leverageInputValue({ normalize: true });
    if (!Number.isFinite(equity) || Number(equity) <= 0) {
      state.positionRatio = null;
      renderPositionRatioButtons();
      return;
    }
    state.positionRatio = ratio;
    state.positionNotionalMode = "ratio";
    const margin = Number(equity) * ratio;
    const notional = margin * Math.max(Number(leverage), 1);
    setValue("position_notional_usdt", formatEditableNotional(notional));
    updatePositionMarginField();
    renderPositionRatioButtons();
    if (reset) {
      resetTradeStateIfEdited();
    }
  }

  function applySymbolPreset(symbol) {
    const preset = TOKEN_PRESETS[String(symbol || "").toUpperCase()];
    if (!preset) {
      return;
    }
    Object.entries(preset).forEach(([id, value]) => setValue(id, value));
    state.positionNotionalMode = "preset";
    syncPositionRatioFromForm();
    resetTradeStateIfEdited();
  }

  function wizardStepById(stepId) {
    return QUESTION_BANK.find((step) => step.id === stepId) || null;
  }

  function wizardOptionLabel(step, rawValue) {
    const value = String(rawValue);
    const option = step.options.find((item) => String(item.value) === value);
    if (!option) {
      return value;
    }
    return t(option.labelKey);
  }

  function firstMissingWizardIndex() {
    return activeWizardSteps().findIndex((step) => !state.wizardAnswers[step.id]);
  }

  function answeredWizardCount() {
    return activeWizardSteps().filter((step) => Boolean(state.wizardAnswers[step.id])).length;
  }

  function allWizardAnswered() {
    return firstMissingWizardIndex() === -1;
  }

  function setProfileStatus(mode, profile = null, score = null) {
    state.profileStatusMode = mode;
    state.profileStatusProfile = profile;
    state.profileStatusScore = score;
    renderProfileConfirmStatus();
    updateActionState();
  }

  function renderProfileConfirmStatus() {
    const chip = byId("profile-confirm-status");
    if (!chip) {
      return;
    }

    chip.classList.remove("muted", "warn", "ok");
    if (state.profileStatusMode === "loading") {
      chip.classList.add("warn");
      chip.textContent = t("status.loading_profile");
      return;
    }

    if (state.profileStatusMode === "preview") {
      chip.classList.add("warn");
      chip.textContent = formatTemplate("status.preview_profile", {
        profile: translateProfileName(state.profileStatusProfile),
        score: formatScore(state.profileStatusScore),
      });
      return;
    }

    if (state.profileStatusMode === "pending") {
      chip.classList.add("warn");
      chip.textContent = formatTemplate("status.pending_confirmation", {
        profile: translateProfileName(state.profileStatusProfile),
        score: formatScore(state.profileStatusScore),
      });
      return;
    }

    if (state.profileStatusMode === "confirmed") {
      chip.classList.add("ok");
      chip.textContent = formatTemplate("status.confirmed_profile", {
        profile: translateProfileName(state.profileStatusProfile),
      });
      return;
    }

    if (state.profileStatusMode === "dirty") {
      chip.classList.add("warn");
      chip.textContent = t("status.profile_dirty");
      return;
    }

    chip.classList.add("muted");
    chip.textContent = t("status.await_profile");
  }

  function renderWizardLog() {
    const box = byId("wizard-log");
    if (!box) {
      return;
    }
    box.classList.remove("muted");
    box.textContent = "";
  }

  function wizardContextText(step) {
    if (!step) {
      return "";
    }
    const signals = accountBehaviorSignals();
    const notes = [];
    if (step.id === "leverage_preference") {
      if (state.wizardAnswers.risk_tolerance === "high") {
        notes.push(t("wizard.note.leverage_risk"));
      } else if (resolvedTradingFrequency(state.wizardAnswers) === "high") {
        notes.push(t("wizard.note.leverage_activity"));
      } else {
        notes.push(t("wizard.note.leverage"));
      }
      return notes.join(" ");
    }
    if (step.id === "revenge_tendency") {
      if (
        state.wizardAnswers.stop_loss_discipline === "sometimes" ||
        state.wizardAnswers.stop_loss_discipline === "rarely"
      ) {
        notes.push(t("wizard.note.revenge_discipline"));
      } else {
        notes.push(t("wizard.note.revenge_risk"));
      }
      if (signals.elevated || signals.highAlert) {
        notes.push(t("wizard.note.revenge_account"));
      }
      return notes.join(" ");
    }
    const baseKey = {
      experience_level: "wizard.note.experience",
      trading_frequency: "wizard.note.frequency",
      risk_tolerance: "wizard.note.risk",
      stop_loss_discipline: "wizard.note.stop",
      max_drawdown_comfort_pct: "wizard.note.drawdown",
    }[step.id] || "";
    if (baseKey) {
      notes.push(t(baseKey));
    }
    if (step.id === "risk_tolerance" && signals.ready) {
      notes.push(t("wizard.note.risk_account"));
      if (!shouldAskTradingFrequency()) {
        notes.push(t("wizard.note.frequency_account"));
      }
    }
    if (step.id === "max_drawdown_comfort_pct" && (signals.elevated || signals.highAlert)) {
      notes.push(t("wizard.note.drawdown_account"));
    }
    return notes.join(" ");
  }

  function renderWizard() {
    const steps = activeWizardSteps();
    const total = steps.length;
    if (total === 0) {
      return;
    }
    state.wizardStep = Math.min(Math.max(state.wizardStep, 0), total - 1);
    const step = steps[state.wizardStep];
    const contextText = wizardContextText(step);

    byId("wizard-progress").textContent = formatTemplate("wizard.progress", {
      current: state.wizardStep + 1,
      total,
    });
    byId("wizard-question").textContent = t(step.questionKey);
    if (byId("wizard-context")) {
      byId("wizard-context").textContent = "";
    }
    byId("btn-prev-step").disabled = state.wizardStep === 0;

    byId("wizard-options").innerHTML = step.options
      .map((option) => {
        const value = String(option.value);
        const active = state.wizardAnswers[step.id] === value ? " active" : "";
        return `<button type="button" class="wizard-option${active}" data-step="${escapeHtml(
          step.id
        )}" data-value="${escapeHtml(value)}">${escapeHtml(t(option.labelKey))}</button>`;
      })
      .join("");

    byId("wizard-options")
      .querySelectorAll("button")
      .forEach((el) => el.addEventListener("click", onWizardOptionClick));

    renderWizardLog();
  }

  async function requestProfileRefresh(requestId, provisional) {
    try {
      await ensureRuntimeReady();
      const data = await postJSON("/v1/profile/recommend", profilePayload({ provisional }));
      if (requestId !== state.profileRefreshRequestId) {
        return;
      }
      state.profileResult = data;
      state.profileConfirmed = false;
      state.profileIsProvisional = provisional;
      renderProfile(data);
      setProfileStatus(provisional ? "preview" : "pending", data.profile, data.profile_score);
    } catch (err) {
      if (requestId !== state.profileRefreshRequestId) {
        return;
      }
      state.profileIsProvisional = false;
      setProfileStatus("await");
      alert(`${t("alert.profile_failed")}: ${err.message}`);
    }
  }

  function scheduleProfileRefresh() {
    if (answeredWizardCount() === 0) {
      return;
    }
    if (state.profileRefreshTimer) {
      clearTimeout(state.profileRefreshTimer);
    }
    const provisional = !allWizardAnswered();
    const requestId = ++state.profileRefreshRequestId;
    state.profileResult = null;
    state.profileConfirmed = false;
    state.profileIsProvisional = provisional;
    setProfileStatus("loading");
    state.profileRefreshTimer = setTimeout(() => {
      state.profileRefreshTimer = null;
      requestProfileRefresh(requestId, provisional);
    }, 180);
  }

  function setWizardAnswer(stepId, value) {
    const step = wizardStepById(stepId);
    if (!step) {
      return false;
    }
    const normalized = String(value);
    const isValid = step.options.some((option) => String(option.value) === normalized);
    if (!isValid) {
      return false;
    }
    state.wizardAnswers[step.id] = normalized;
    syncWizardPathState();
    return true;
  }

  function loadWizardDefaults() {
    state.initialWizardAnswers = {};
    state.wizardAnswers = {};
    QUESTION_BANK.forEach((step) => {
      const source = String(byId(step.id).value || "").trim();
      const fallback = String(step.options[0].value);
      const allowed = step.options.map((option) => String(option.value));
      const normalized = allowed.includes(source) ? source : fallback;
      state.initialWizardAnswers[step.id] = normalized;
      state.wizardAnswers[step.id] = "";
    });
    restoreInitialWizardFormValues();
  }

  function onWizardOptionClick(evt) {
    const stepId = evt.currentTarget.getAttribute("data-step");
    const value = evt.currentTarget.getAttribute("data-value");
    if (!setWizardAnswer(stepId, value)) {
      return;
    }
    resetProfileStateIfEdited({ preserveRenderedProfile: true });
    if (state.wizardStep < activeWizardSteps().length - 1) {
      state.wizardStep += 1;
    }
    renderWizard();
    if (answeredWizardCount() > 0) {
      scheduleProfileRefresh();
    }
  }

  function onPrevWizardStep() {
    state.wizardStep = Math.max(0, state.wizardStep - 1);
    renderWizard();
  }

  function onResetWizard() {
    QUESTION_BANK.forEach((step) => {
      state.wizardAnswers[step.id] = "";
    });
    state.wizardStep = 0;
    restoreInitialWizardFormValues();
    syncWizardPathState();
    resetProfileStateIfEdited();
    renderWizard();
  }

  function translateServerText(text) {
    if (state.lang === "en" || !text) {
      return text;
    }
    if (SERVER_TEXT_EXACT_ZH[text]) {
      return SERVER_TEXT_EXACT_ZH[text];
    }
    const patterns = [
      {
        re: /^Symbol (.+) is outside allowlist\.$/,
        fn: (m) => `交易对 ${m[1]} 不在白名单中。`,
      },
      {
        re: /^Leverage ([\d.]+) exceeds max ([\d.]+)\.$/,
        fn: (m) => `杠杆 ${m[1]} 超过上限 ${m[2]}。`,
      },
      {
        re: /^Daily loss (-?[\d.]+)% breached limit -([\d.]+)%\.$/,
        fn: (m) => `当日亏损 ${m[1]}% 已突破 -${m[2]}% 限额。`,
      },
      {
        re: /^Consecutive losses (\d+) reached cooldown threshold\.$/,
        fn: (m) => `连续亏损 ${m[1]} 次，已触发冷静阈值。`,
      },
      {
        re: /^Estimated loss at stop \(([\d.]+)%\) exceeds max risk per trade ([\d.]+)%\.$/,
        fn: (m) => `止损预计亏损 ${m[1]}% 超过单笔风险上限 ${m[2]}%。`,
      },
      {
        re: /^Reward\/risk ratio ([\d.]+)x is below required ([\d.]+)x\.$/,
        fn: (m) => `当前盈亏比 ${m[1]}x 低于要求的 ${m[2]}x。`,
      },
      {
        re: /^Selected profile '([^']+)' tightened to '([^']+)' by risk checks\.$/,
        fn: (m) => `手动档位“${translateProfileName(m[1])}”被风控收紧为“${translateProfileName(m[2])}”。`,
      },
      {
        re: /^Selected profile '([^']+)' accepted\.$/,
        fn: (m) => `手动档位“${translateProfileName(m[1])}”已采用。`,
      },
      {
        re: /^Entry price must be greater than zero\.$/,
        fn: () => "开仓价必须大于0。",
      },
      {
        re: /^Account equity must be greater than zero\.$/,
        fn: () => "账户权益必须大于0。",
      },
      {
        re: /^Position notional must be greater than zero\.$/,
        fn: () => "仓位名义价值必须大于0。",
      },
      {
        re: /^Position size is too large versus account equity\.$/,
        fn: () => "仓位相对账户权益过大。",
      },
      {
        re: /^Stop-loss is required by guardrail but missing\.$/,
        fn: () => "当前风控要求必须设置止损。",
      },
      {
        re: /^For LONG, stop-loss must be below entry price\.$/,
        fn: () => "做多时，止损价必须低于开仓价。",
      },
      {
        re: /^For SHORT, stop-loss must be above entry price\.$/,
        fn: () => "做空时，止损价必须高于开仓价。",
      },
      {
        re: /^For LONG, take-profit must be above entry price\.$/,
        fn: () => "做多时，止盈价必须高于开仓价。",
      },
      {
        re: /^For SHORT, take-profit must be below entry price\.$/,
        fn: () => "做空时，止盈价必须低于开仓价。",
      },
      {
        re: /^No take-profit is set; payoff quality is undefined\.$/,
        fn: () => "当前未设置止盈，收益质量无法评估。",
      },
      {
        re: /^Reward\/risk ratio is below the current profile requirement\.$/,
        fn: () => "当前盈亏比低于档位要求。",
      },
      {
        re: /^Binance (?:Spot|USD-M Futures) (?:Demo Mode|Testnet|API) network error: (.+)$/,
        fn: (m) => `Binance 网络错误：${m[1]}。`,
      },
      {
        re: /^Binance (?:Spot|USD-M Futures) (?:Demo Mode|Testnet|API) HTTP (\d+): (.+)$/,
        fn: (m) => `Binance 返回 HTTP ${m[1]}：${m[2]}。`,
      },
      {
        re: /^Could not reach Binance (?:Spot|USD-M Futures) (?:Demo Mode|Testnet|API): (.+)$/,
        fn: (m) => `无法连接 Binance：${m[1]}。`,
      },
      {
        re: /^Estimated equity ([\d.]+) USDT, available USDT ([\d.]+)\.$/,
        fn: (m) => `估算权益 ${m[1]} USDT，可用 USDT ${m[2]}。`,
      },
      {
        re: /^Recent activity: (\d+) trades in 24h, realized PnL (-?[\d.]+)%, trailing loss streak (\d+)\.$/,
        fn: (m) => `近24小时交易 ${m[1]} 笔，已实现盈亏 ${m[2]}%，当前连续亏损 ${m[3]} 次。`,
      },
      {
        re: /^Active futures positions: (\d+)\.(?: Closest estimated liquidation gap is ([\d.]+)%\.)?$/,
        fn: (m) =>
          m[2]
            ? `当前合约持仓 ${m[1]} 个，最近的预估爆仓缓冲为 ${m[2]}%。`
            : `当前合约持仓 ${m[1]} 个。`,
      },
      {
        re: /^Under ([a-z]+) profile, suggested max notional is ([\d.]+) USDT and per-trade risk budget is ([\d.]+) USDT\.$/,
        fn: (m) =>
          `在${translateProfileName(m[1])}档位下，建议最大名义仓位 ${m[2]} USDT，单笔风险预算 ${m[3]} USDT。`,
      },
      {
        re: /^Requested notional ([\d.]+) is below Binance minimum executable notional ([\d.]+) USDT for ([A-Z0-9]+) at current price ([\d.]+); Binance LOT_SIZE minQty is ([\d.]+)\.$/,
        fn: (m) =>
          `当前请求名义价值 ${m[1]} USDT 低于 ${m[3]} 在现价 ${m[4]} 下的最小可执行名义价值 ${m[2]} USDT；Binance LOT_SIZE 最小数量为 ${m[5]}。`,
      },
      {
        re: /^Requested notional ([\d.]+) is below Binance minimum executable notional ([\d.]+) USDT for ([A-Z0-9]+) \(MIN_NOTIONAL ([\d.]+), minQty ([\d.]+)\)\.$/,
        fn: (m) =>
          `当前请求名义价值 ${m[1]} USDT 低于 ${m[3]} 的最小可执行名义价值 ${m[2]} USDT（MIN_NOTIONAL ${m[4]}，最小数量 ${m[5]}）。`,
      },
    ];

    for (const item of patterns) {
      const m = text.match(item.re);
      if (m) {
        return item.fn(m);
      }
    }
    return text;
  }

  function setLangButtonState() {
    byId("lang-zh").classList.toggle("active", state.lang === "zh");
    byId("lang-en").classList.toggle("active", state.lang === "en");
  }

  function applyI18n() {
    document.documentElement.lang = state.lang === "zh" ? "zh-CN" : "en";
    document.title = t("meta.title");
    document.querySelectorAll("[data-i18n]").forEach((el) => {
      const key = el.getAttribute("data-i18n");
      el.textContent = t(key);
    });
    setLangButtonState();
    renderSymbolSelect();
    renderWizard();
    renderProfileConfirmStatus();
    renderAgentSteps();
    renderAgentStatusChip();
    updatePositionMarginField();
    updateDecisionSignalPanel();
  }

  function profileQuizPayload({ provisional = false } = {}) {
    const activeIds = new Set(activeWizardSteps().map((step) => step.id));
    const quiz = {};
    QUESTION_BANK.forEach((step) => {
      const answer = String(state.wizardAnswers[step.id] || "").trim();
      let nextValue = answer;
      if (!answer && !activeIds.has(step.id) && typeof step.deriveValue === "function") {
        nextValue = String(step.deriveValue(state.wizardAnswers) || "").trim();
      }
      if (!nextValue && provisional) {
        return;
      }
      if (!nextValue) {
        return;
      }
      quiz[step.id] =
        step.id === "max_drawdown_comfort_pct" ? Number(nextValue) : nextValue;
    });
    return quiz;
  }

  function profilePayload({ provisional = false } = {}) {
    const selected = byId("selected_profile").value;
    const payload = {
      quiz: profileQuizPayload({ provisional }),
      behavior: {
        consecutive_losses: toNumber("consecutive_losses"),
        trades_last_24h: toNumber("trades_last_24h"),
        day_pnl_pct: toNumber("day_pnl_pct"),
      },
    };
    if (selected) {
      payload.selected_profile = selected;
    }
    return payload;
  }

  function evaluatePayload() {
    const normalizedLeverage = normalizeLeverageInput();
    return {
      profile: state.profileResult ? state.profileResult.profile : undefined,
      quiz: state.profileResult ? undefined : profilePayload().quiz,
      trade: {
        symbol: byId("symbol").value.toUpperCase(),
        side: byId("side").value,
        entry_price: toNumber("entry_price"),
        stop_loss_price: toOptionalNumber("stop_loss_price"),
        take_profit_price: toOptionalNumber("take_profit_price"),
        leverage: normalizedLeverage,
        margin_mode: byId("margin_mode").value,
        position_notional_usdt: toNumber("position_notional_usdt"),
        account_equity_usdt: toNumber("account_equity_usdt"),
      },
      market: {
        volatility_24h_pct: toNumber("volatility_24h_pct"),
        bid_ask_spread_bps: toNumber("bid_ask_spread_bps"),
        liquidity_depth_score: toNumber("liquidity_depth_score"),
      },
      behavior: {
        consecutive_losses: toNumber("consecutive_losses"),
        trades_last_24h: toNumber("trades_last_24h"),
        day_pnl_pct: toNumber("day_pnl_pct"),
      },
    };
  }

  async function postJSON(url, payload) {
    const res = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    const data = await res.json().catch(() => ({}));
    if (!res.ok) {
      throw new Error(data.error || `Request failed: ${res.status}`);
    }
    return data;
  }

  async function getJSON(url) {
    const res = await fetch(url);
    const data = await res.json().catch(() => ({}));
    if (!res.ok) {
      throw new Error(data.error || `Request failed: ${res.status}`);
    }
    return data;
  }

  async function syncRuntimeHealth({ allowRecoverySync = false } = {}) {
    const hadMismatch = state.runtimeMismatch;
    try {
      const data = await getJSON("/health");
      state.runtimeHealthReady = true;
      state.runtimeServerVersion = String(data.server_runtime_version || "");
      state.runtimeWorkspaceVersion = String(data.workspace_version || "");
      state.runtimeAssetVersion = String(data.asset_version || "");
      state.runtimeMismatch = Boolean(data.runtime_in_sync === false);
      state.runtimeCheckedAt = Date.now();
      if (
        CLIENT_ASSET_VERSION &&
        state.runtimeAssetVersion &&
        state.runtimeAssetVersion !== CLIENT_ASSET_VERSION
      ) {
        window.setTimeout(() => window.location.reload(), 120);
        throw new Error(t("alert.asset_mismatch"));
      }
    } catch (err) {
      state.runtimeHealthReady = true;
      state.runtimeServerVersion = "";
      state.runtimeWorkspaceVersion = "";
      state.runtimeAssetVersion = "";
      state.runtimeMismatch = true;
      state.runtimeCheckedAt = Date.now();
    }
    updateActionState();
    renderAgentBriefing();
    if (allowRecoverySync && hadMismatch && !state.runtimeMismatch) {
      loadSymbolCatalog();
      syncAccountSnapshot();
      syncMarketSnapshot();
      if (answeredWizardCount() > 0) {
        scheduleProfileRefresh();
      }
    }
    return !state.runtimeMismatch;
  }

  async function ensureRuntimeReady() {
    const checkAgeMs = Date.now() - state.runtimeCheckedAt;
    if (!state.runtimeHealthReady || state.runtimeMismatch || checkAgeMs > 2500) {
      await syncRuntimeHealth({ allowRecoverySync: true });
    }
    if (state.runtimeMismatch) {
      throw new Error(runtimeMismatchText());
    }
  }

  function mapList(items) {
    return (items || [])
      .map((x) => `<li>${escapeHtml(translateServerText(String(x)))}</li>`)
      .join("");
  }

  function profileClass(profile) {
    const normalized = String(profile || "").toLowerCase();
    if (normalized === "conservative" || normalized === "balanced" || normalized === "aggressive") {
      return normalized;
    }
    return "balanced";
  }

  function clamp01(value) {
    const n = Number(value);
    if (!Number.isFinite(n)) {
      return 0;
    }
    return Math.max(0, Math.min(1, n));
  }

  function riskHueFromScore(score) {
    const ratio = clamp01(score / 100);
    return Math.round(150 - ratio * 150);
  }

  function easeOutCubic(t) {
    return 1 - (1 - t) ** 3;
  }

  function applyRiskBubbleVisual(field, valueEl, value) {
    const safeValue = Number.isFinite(value) ? value : 0;
    const ratio = clamp01(safeValue / 100);
    const hue = riskHueFromScore(safeValue);
    field.style.setProperty("--risk-hue", String(hue));
    field.style.setProperty("--risk-ratio", ratio.toFixed(3));
    field.style.setProperty("--score-ink", `hsl(${hue} 62% 26%)`);
    valueEl.textContent = safeValue.toFixed(2);
  }

  function animateProfileScore(targetScore) {
    const field = byId("profile-score-bubble");
    const valueEl = byId("profile-score-value");
    if (!field || !valueEl || !Number.isFinite(targetScore)) {
      state.profileScoreDisplay = Number.isFinite(targetScore) ? targetScore : null;
      return;
    }

    if (state.profileScoreAnimationFrame) {
      cancelAnimationFrame(state.profileScoreAnimationFrame);
      state.profileScoreAnimationFrame = null;
    }

    const startValue = Number.isFinite(state.profileScoreDisplay)
      ? Number(state.profileScoreDisplay)
      : Number(targetScore);
    const endValue = Number(targetScore);
    const delta = endValue - startValue;
    const duration = Math.min(1100, 520 + Math.abs(delta) * 10);

    if (Math.abs(delta) < 0.01) {
      applyRiskBubbleVisual(field, valueEl, endValue);
      state.profileScoreDisplay = endValue;
      return;
    }

    const startedAt = performance.now();
    const tick = (now) => {
      const progress = Math.min(1, (now - startedAt) / duration);
      const nextValue = startValue + delta * easeOutCubic(progress);
      applyRiskBubbleVisual(field, valueEl, nextValue);
      state.profileScoreDisplay = nextValue;
      if (progress < 1) {
        state.profileScoreAnimationFrame = requestAnimationFrame(tick);
        return;
      }
      state.profileScoreDisplay = endValue;
      state.profileScoreAnimationFrame = null;
    };

    applyRiskBubbleVisual(field, valueEl, startValue);
    state.profileScoreAnimationFrame = requestAnimationFrame(tick);
  }

  function profileThemeMeta(profile) {
    const normalized = profileClass(profile);
    if (normalized === "conservative") {
      return {
        toneClass: "theme-conservative",
        accentLabel: t("profile.bias_shield"),
      };
    }
    if (normalized === "aggressive") {
      return {
        toneClass: "theme-aggressive",
        accentLabel: t("profile.bias_velocity"),
      };
    }
    return {
      toneClass: "theme-balanced",
      accentLabel: t("profile.bias_balanced"),
    };
  }

  function renderInsightList(items) {
    if (!items || items.length === 0) {
      return `<li class="tech-list-item"><span class="tech-list-dot"></span><span>${escapeHtml(
        t("misc.na")
      )}</span></li>`;
    }
    return (items || [])
      .map(
        (item) => `<li class="tech-list-item"><span class="tech-list-dot"></span><span>${escapeHtml(
          translateServerText(String(item))
        )}</span></li>`
      )
      .join("");
  }

  function renderGuardrailTile({ label, value, caption, ratio, tone = "amber" }) {
    return `
      <div class="guardrail-tile ${tone}">
        <span class="guardrail-label">${escapeHtml(label)}</span>
        <strong class="guardrail-value">${escapeHtml(value)}</strong>
        <div class="guardrail-track">
          <span class="guardrail-fill" style="--fill:${Math.round(clamp01(ratio) * 100)}%"></span>
        </div>
        <span class="guardrail-caption">${escapeHtml(caption)}</span>
      </div>
    `;
  }

  function renderProfile(data) {
    const summaryBox = byId("profile-result-inline");
    const detailBox = byId("profile-result");
    summaryBox.classList.remove("muted");
    detailBox.classList.remove("muted");
    const profileName = escapeHtml(translateProfileName(data.profile));
    const profileScoreRaw = Number(data.profile_score);
    const initialProfileScore = Number.isFinite(state.profileScoreDisplay)
      ? Number(state.profileScoreDisplay).toFixed(2)
      : Number.isFinite(profileScoreRaw)
        ? profileScoreRaw.toFixed(2)
        : t("misc.na");
    const scoreRatio = clamp01(profileScoreRaw / 100);
    const riskHue = riskHueFromScore(profileScoreRaw);
    const bubbleStyle = `--risk-hue:${riskHue}; --risk-ratio:${scoreRatio.toFixed(3)}; --score-ink:hsl(${riskHue} 62% 26%);`;
    const theme = profileThemeMeta(data.profile);
    const maxLeverageRaw = Number(data.guardrails.max_leverage);
    const maxDailyLossRaw = Number(data.guardrails.max_daily_loss_pct);
    const maxRiskPerTradeRaw = Number(data.guardrails.max_risk_per_trade_pct);
    const minRewardRiskRaw = Number(data.guardrails.min_reward_risk_ratio);
    const maxPositionVsEquityRaw = Number(data.guardrails.max_position_vs_equity);
    const maxLeverage = Number.isFinite(maxLeverageRaw)
      ? formatMetric(maxLeverageRaw, "x")
      : t("misc.na");
    const maxDailyLoss = Number.isFinite(maxDailyLossRaw)
      ? `-${formatMetric(maxDailyLossRaw, "%")}`
      : t("misc.na");
    const maxRiskPerTrade = Number.isFinite(maxRiskPerTradeRaw)
      ? formatMetric(maxRiskPerTradeRaw, "%")
      : t("misc.na");
    const minRewardRisk = Number.isFinite(minRewardRiskRaw)
      ? formatMetric(minRewardRiskRaw, "x")
      : t("misc.na");
    const maxPositionVsEquity = Number.isFinite(maxPositionVsEquityRaw)
      ? formatMetric(maxPositionVsEquityRaw, "x")
      : t("misc.na");
    const strengths = renderInsightList(data.strengths);
    const issues = renderInsightList(data.issues);
    const coaching = renderInsightList(data.coaching);
    const adjustmentsItems = data.auto_adjustments || [];
    const adjustments = renderInsightList(adjustmentsItems);
    const profileChipLabel = state.profileConfirmed
      ? t("profile.confirmed_tag")
      : state.profileIsProvisional
        ? t("profile.preview_tag")
        : t("profile.pending_tag");
    const guardrailTiles = [
      renderGuardrailTile({
        label: t("result.max_leverage"),
        value: maxLeverage,
        caption: theme.accentLabel,
        ratio: Number.isFinite(maxLeverageRaw) ? maxLeverageRaw / 20 : 0,
        tone: "amber",
      }),
      renderGuardrailTile({
        label: t("result.max_daily_loss"),
        value: maxDailyLoss,
        caption: t("profile.sync_caption"),
        ratio: Number.isFinite(maxDailyLossRaw) ? maxDailyLossRaw / 12 : 0,
        tone: "red",
      }),
      renderGuardrailTile({
        label: t("result.max_risk_trade"),
        value: maxRiskPerTrade,
        caption: t("profile.caption_stop"),
        ratio: Number.isFinite(maxRiskPerTradeRaw) ? maxRiskPerTradeRaw / 3 : 0,
        tone: "amber",
      }),
      renderGuardrailTile({
        label: t("result.max_reward_risk"),
        value: minRewardRisk,
        caption: t("profile.caption_reward"),
        ratio: Number.isFinite(minRewardRiskRaw) ? minRewardRiskRaw / 3 : 0,
        tone: "green",
      }),
      renderGuardrailTile({
        label: t("result.max_position_equity"),
        value: maxPositionVsEquity,
        caption: t("profile.caption_density"),
        ratio: Number.isFinite(maxPositionVsEquityRaw) ? maxPositionVsEquityRaw / 1.5 : 0,
        tone: "amber",
      }),
    ].join("");
    const summaryMarkup = `
      <div class="profile-dashboard ${theme.toneClass}">
        <div class="profile-hero-card">
          <div class="profile-hero-copy">
            <div class="profile-tech-kicker">${escapeHtml(t("profile.tech_kicker"))}</div>
            <div class="profile-title-row">
              <div>
                <div class="profile-title">${profileName}</div>
                <div class="profile-subtitle">${escapeHtml(t("profile.sync_caption"))}</div>
              </div>
              <div class="profile-chip-row">
                <span class="profile-chip">${escapeHtml(profileChipLabel)}</span>
                <span class="profile-chip subtle">${escapeHtml(
                  `${t("result.label_profile")} AI`
                )}</span>
              </div>
            </div>
            <div class="profile-signal-strip">
              <span class="signal-pill">${escapeHtml(t("result.max_leverage"))}: ${escapeHtml(
                maxLeverage
              )}</span>
              <span class="signal-pill">${escapeHtml(
                t("result.max_risk_trade")
              )}: ${escapeHtml(maxRiskPerTrade)}</span>
              <span class="signal-pill">${escapeHtml(
                t("result.max_reward_risk")
              )}: ${escapeHtml(minRewardRisk)}</span>
            </div>
          </div>
          <div class="profile-hero-visual">
            <div class="score-bubble-field" style="${escapeHtml(bubbleStyle)}">
              <span class="score-bubble bubble-back"></span>
              <span class="score-bubble bubble-side side-left"></span>
              <span class="score-bubble bubble-side side-right"></span>
              <div class="score-bubble-main" id="profile-score-bubble">
                <span class="score-caption">${escapeHtml(t("profile.score_caption"))}</span>
                <strong id="profile-score-value">${escapeHtml(initialProfileScore)}</strong>
              </div>
            </div>
          </div>
        </div>
      </div>
    `;
    const detailMarkup = `
      <div class="profile-dashboard ${theme.toneClass}">
        <div class="profile-sections-grid">
          <section class="profile-section-card span-wide">
            <div class="profile-section-head">
              <div>
                <h3 class="profile-section-title">${escapeHtml(t("result.guardrails"))}</h3>
              </div>
            </div>
            <div class="guardrail-grid-tech">
              ${guardrailTiles}
            </div>
          </section>
          <section class="profile-section-card">
            <div class="profile-section-head">
              <h3 class="profile-section-title">${escapeHtml(t("result.strengths"))}</h3>
            </div>
            <ul class="tech-list">${strengths}</ul>
          </section>
          <section class="profile-section-card">
            <div class="profile-section-head">
              <h3 class="profile-section-title">${escapeHtml(t("result.issues"))}</h3>
            </div>
            <ul class="tech-list">${issues}</ul>
          </section>
          <section class="profile-section-card">
            <div class="profile-section-head">
              <h3 class="profile-section-title">${escapeHtml(t("result.coaching"))}</h3>
            </div>
            <ul class="tech-list">${coaching}</ul>
          </section>
          ${
            adjustmentsItems.length > 0
              ? `<section class="profile-section-card">
                  <div class="profile-section-head">
                    <h3 class="profile-section-title">${escapeHtml(
                      t("result.auto_adjustments")
                    )}</h3>
                  </div>
                  <ul class="tech-list">${adjustments}</ul>
                </section>`
              : ""
          }
        </div>
      </div>
    `;
    summaryBox.innerHTML = summaryMarkup;
    detailBox.innerHTML = detailMarkup;
    animateProfileScore(profileScoreRaw);
    renderAgentSteps();
    renderAgentBriefing();
  }

  function decisionClass(decision) {
    if (decision === "ALLOW") return "allow";
    if (decision === "WARN") return "warn";
    return "block";
  }

  function renderMetrics(metrics) {
    const items = [
      ["metric.risk_per_trade_pct", metrics.risk_per_trade_pct, "%"],
      ["metric.reward_risk_ratio", metrics.reward_risk_ratio, "x"],
      ["metric.target_reward_risk_ratio", metrics.target_reward_risk_ratio, "x"],
      ["metric.liquidation_buffer_pct", metrics.liquidation_buffer_pct, "%"],
      ["metric.leverage_risk", metrics.leverage_risk, "%"],
      ["metric.volatility_risk", metrics.volatility_risk, "%"],
      ["metric.concentration_risk", metrics.concentration_risk, "%"],
      ["metric.liquidity_risk", metrics.liquidity_risk, "%"],
      ["metric.behavior_risk", metrics.behavior_risk, "%"],
    ];

    return items
      .map(
        ([labelKey, value, suffix]) => `
          <div class="metric-card">
            <span class="metric-label">${escapeHtml(t(labelKey))}</span>
            <strong class="metric-value">${escapeHtml(formatMetric(value, suffix))}</strong>
          </div>
        `
      )
      .join("");
  }

  function renderTrade(data) {
    const box = byId("trade-result");
    box.classList.remove("muted");
    updateDecisionSignalPanel();
    const blockersItems = data.blockers || [];
    const reasons = mapList(data.reasons || []);
    const blockers = mapList(blockersItems);
    const plan = data.suggested_plan || {};
    const planLeverage = escapeHtml(plan.leverage ?? t("misc.na"));
    const planNotional = escapeHtml(plan.position_notional_usdt ?? t("misc.na"));
    const planStopLoss = escapeHtml(plan.stop_loss_price ?? t("misc.na"));
    const planTakeProfit = escapeHtml(plan.take_profit_price ?? t("misc.na"));
    const planNote = escapeHtml(translateServerText(plan.note || t("misc.na")));
    const metricsHtml = renderMetrics(data.metric_breakdown || {});
    const reasonsSpanClass = blockersItems.length > 0 ? "" : " trade-section-span";
    box.innerHTML = `
      <div class="trade-result-shell">
        <section class="trade-section-card trade-plan-card">
          <div class="trade-section-head">
            <h3 class="trade-section-title">${escapeHtml(t("result.suggested_plan"))}</h3>
          </div>
          <div class="trade-plan-grid">
            <div class="trade-plan-tile">
              <span class="trade-plan-label">${escapeHtml(t("result.plan_leverage"))}</span>
              <strong class="trade-plan-value">${planLeverage}</strong>
            </div>
            <div class="trade-plan-tile">
              <span class="trade-plan-label">${escapeHtml(t("result.plan_notional"))}</span>
              <strong class="trade-plan-value">${planNotional}</strong>
            </div>
            <div class="trade-plan-tile">
              <span class="trade-plan-label">${escapeHtml(t("result.plan_stop_loss"))}</span>
              <strong class="trade-plan-value">${planStopLoss}</strong>
            </div>
            <div class="trade-plan-tile">
              <span class="trade-plan-label">${escapeHtml(t("result.plan_take_profit"))}</span>
              <strong class="trade-plan-value">${planTakeProfit}</strong>
            </div>
          </div>
          <div class="trade-plan-note">${escapeHtml(t("result.plan_note"))}: ${planNote}</div>
        </section>
        <div class="trade-result-grid">
          <section class="trade-section-card${reasonsSpanClass}">
            <div class="trade-section-head">
              <h3 class="trade-section-title">${escapeHtml(t("result.reasons"))}</h3>
            </div>
            <ul class="tech-list compact">${reasons}</ul>
          </section>
          ${
            blockersItems.length > 0
              ? `<section class="trade-section-card">
                  <div class="trade-section-head">
                    <h3 class="trade-section-title">${escapeHtml(t("result.blockers"))}</h3>
                  </div>
                  <ul class="tech-list compact">${blockers}</ul>
                </section>`
              : ""
          }
          <section class="trade-section-card trade-section-span">
            <div class="trade-section-head">
              <h3 class="trade-section-title">${escapeHtml(t("result.metrics"))}</h3>
            </div>
            <div class="metric-grid trade-metric-grid">${metricsHtml}</div>
          </section>
        </div>
      </div>
    `;
    renderAgentSteps();
    renderAgentBriefing();
  }

  function resetMarketSyncState() {
    state.marketSnapshot = null;
    const box = byId("market-sync-status");
    box.classList.add("muted");
    box.classList.remove("market-box");
    box.textContent = `${t("placeholder.market_sync")} ${t(currentFlowHintKey())}`;
    renderAgentSteps();
    renderAgentStatusChip();
  }

  function resetAccountSyncState() {
    state.accountSnapshot = null;
    state.currentExposureActionResult = null;
    if (!state.profileConfirmed) {
      syncWizardPathState();
      renderWizard();
    }
    const box = byId("account-sync-status");
    box.classList.add("muted");
    box.textContent = `${t("placeholder.account_sync")} ${t(currentFlowHintKey())}`;
    const exposureBox = byId("current-exposure-status");
    exposureBox.classList.add("muted");
    exposureBox.textContent = t("placeholder.current_exposure");
    renderAgentSteps();
    renderAgentStatusChip();
  }

  function resetOrderTestState() {
    state.orderTestResult = null;
    renderOrderTicker(`${t("placeholder.order_test")} ${t(currentFlowHintKey())}`, "warn");
    renderAgentSteps();
    renderAgentStatusChip();
    updateActionState();
  }

  function renderAccountSync(data) {
    const box = byId("account-sync-status");
    const account = data.account || {};
    const behavior = data.behavior || {};
    const agent = data.agent_context || {};
    const liveConnected = hasLiveAccountSnapshot(data);
    const displayCurrency = (value) =>
      liveConnected ? formatCurrency(value) : t("misc.na");
    const displayMetric = (value, suffix = "") =>
      liveConnected ? formatMetric(value, suffix) : t("misc.na");
    const displayCount = (value) => (liveConnected ? value ?? t("misc.na") : t("misc.na"));
    const assets = (account.nonzero_assets || [])
      .slice(0, 4)
      .map(
        (item) =>
          `<li>${escapeHtml(item.asset)}: ${escapeHtml(formatCurrency(item.estimated_usdt))}</li>`
      )
      .join("");
    const warningLine =
      !liveConnected && data.warning
        ? `<br/><strong>${escapeHtml(t("result.market_warning"))}</strong>: ${escapeHtml(
            translateServerText(String(data.warning))
          )}`
        : "";

    box.classList.remove("muted");
    box.innerHTML = `
      <h3>${escapeHtml(t("result.account_sync"))}</h3>
      <div class="card">
        <strong>${escapeHtml(t("result.account_source"))}</strong>: ${escapeHtml(
          marketSourceLabel(data.source)
        )}<br/>
        <strong>${escapeHtml(t("result.account_connection"))}</strong>: ${escapeHtml(
          liveConnected ? t("misc.live_connected") : t("misc.demo_only")
        )}${warningLine}<br/>
        <strong>${escapeHtml(t("result.account_equity"))}</strong>: ${escapeHtml(
          displayCurrency(account.estimated_equity_usdt)
        )}<br/>
        <strong>${escapeHtml(t("result.account_wallet"))}</strong>: ${escapeHtml(
          displayCurrency(account.wallet_balance_usdt)
        )}<br/>
        <strong>${escapeHtml(t("result.account_available"))}</strong>: ${escapeHtml(
          displayCurrency(account.available_usdt)
        )}<br/>
        <strong>${escapeHtml(t("result.account_locked"))}</strong>: ${escapeHtml(
          displayCurrency(account.locked_usdt)
        )}<br/>
        <strong>${escapeHtml(t("result.account_open_orders"))}</strong>: ${escapeHtml(
          displayCount(account.open_orders_count)
        )}
      </div>
      <div class="card">
        <strong>${escapeHtml(t("result.account_behavior"))}</strong>: ${escapeHtml(
          displayCount(behavior.trades_last_24h)
        )} trades / ${escapeHtml(displayMetric(behavior.day_pnl_pct, "%"))} / ${escapeHtml(
          displayCount(behavior.consecutive_losses)
        )} streak<br/>
        <strong>${escapeHtml(t("result.account_position_cap"))}</strong>: ${escapeHtml(
          displayCurrency(agent.suggested_position_cap_usdt)
        )}<br/>
        <strong>${escapeHtml(t("result.account_risk_budget"))}</strong>: ${escapeHtml(
          displayCurrency(agent.risk_budget_usdt)
        )}
      </div>
      <div class="card">
        <strong>${escapeHtml(t("result.account_assets"))}</strong>
        <ul class="agent-list">${
          liveConnected ? assets || `<li>${escapeHtml(t("misc.na"))}</li>` : `<li>${escapeHtml(t("misc.na"))}</li>`
        }</ul>
      </div>
    `;
    renderAgentSteps();
    renderAgentStatusChip();
  }

  function renderAgentBriefing() {
    const box = byId("agent-briefing");
    const lines = agentBriefingLines();
    box.classList.remove("muted");
    box.innerHTML = `
      <div class="agent-briefing-head">
        <h3>${escapeHtml(t("result.agent_briefing"))}</h3>
        <button
          id="btn-refresh-agent-briefing"
          class="btn ghost tiny"
          type="button"
          ${state.agentBriefingRefreshing ? "disabled" : ""}
        >${escapeHtml(
          state.agentBriefingRefreshing ? t("agent.status_syncing") : t("btn.refresh_agent_briefing")
        )}</button>
      </div>
      <ul class="agent-list">${lines
        .map((line) => `<li>${escapeHtml(line)}</li>`)
        .join("")}</ul>
    `;
    const refreshButton = byId("btn-refresh-agent-briefing");
    if (refreshButton) {
      refreshButton.addEventListener("click", onRefreshAgentBriefing);
    }
    renderAgentStatusChip();
  }

  async function onRefreshAgentBriefing() {
    if (state.agentBriefingRefreshing) {
      return;
    }
    state.agentBriefingRefreshing = true;
    state.agentBriefingError = "";
    renderAgentBriefing();
    try {
      await ensureRuntimeReady();
      await Promise.allSettled([
        syncAccountSnapshot({ applyForm: false }),
        syncMarketSnapshot({ applyForm: false }),
      ]);
      state.agentBriefingManualRefreshAt = Date.now();
    } catch (err) {
      state.agentBriefingError =
        state.lang === "zh"
          ? `更新 Agent 简报失败：${err.message}`
          : `Failed to refresh Agent briefing: ${err.message}`;
    } finally {
      state.agentBriefingRefreshing = false;
      renderAgentSteps();
      renderAgentBriefing();
    }
  }

  function trackedPositionFromSnapshot() {
    const target = state.positionTrackerTarget;
    const snapshot = state.accountSnapshot;
    if (!target || !snapshot || !snapshot.account || !Array.isArray(snapshot.account.open_positions)) {
      return null;
    }
    const positions = snapshot.account.open_positions;
    const symbol = String(target.symbol || "").toUpperCase();
    const intentSide = String(target.intentSide || "").toUpperCase();
    const targetPositionSide = String(target.positionSide || "").toUpperCase();

    const bySymbol = positions.filter((item) => String(item.symbol || "").toUpperCase() === symbol);
    if (!bySymbol.length) {
      return null;
    }
    if (targetPositionSide) {
      const exact = bySymbol.find(
        (item) => String(item.position_side || "").toUpperCase() === targetPositionSide
      );
      if (exact) {
        return exact;
      }
    }
    if (intentSide === "LONG") {
      return (
        bySymbol.find((item) => Number(item.quantity) > 0) ||
        bySymbol[0]
      );
    }
    if (intentSide === "SHORT") {
      return (
        bySymbol.find((item) => Number(item.quantity) < 0) ||
        bySymbol[0]
      );
    }
    return bySymbol[0];
  }

  function trackedPositionSideLabel(position) {
    const explicit = String(position?.position_side || "").toUpperCase();
    if (explicit === "LONG") {
      return `${t("opt.long")} / LONG`;
    }
    if (explicit === "SHORT") {
      return `${t("opt.short")} / SHORT`;
    }
    const quantity = Number(position?.quantity || 0);
    if (quantity > 0) {
      return `${t("opt.long")} / LONG`;
    }
    if (quantity < 0) {
      return `${t("opt.short")} / SHORT`;
    }
    return explicit || t("misc.na");
  }

  function protectionSideLabel(order) {
    const side = String(order?.side || "").toUpperCase();
    const positionSide = String(order?.position_side || "").toUpperCase();
    if (side === "SELL" && positionSide === "LONG") {
      return state.lang === "zh" ? "平多保护" : "Protect LONG";
    }
    if (side === "BUY" && positionSide === "SHORT") {
      return state.lang === "zh" ? "平空保护" : "Protect SHORT";
    }
    return `${side || t("misc.na")} / ${positionSide || "BOTH"}`;
  }

  function trackedPositionCardHtml() {
    const target = state.positionTrackerTarget;
    if (!target) {
      return "";
    }
    const position = trackedPositionFromSnapshot();
    if (!position) {
      const startedAt = Number(target.startedAt || 0);
      const waitingWindow = Date.now() - startedAt < 12000;
      const waitingText =
        !state.accountSnapshot || waitingWindow
          ? t("result.position_waiting")
          : t("result.position_missing");
      return `<div class="card"><strong>${escapeHtml(t("result.position_tracker"))}</strong><br/>${escapeHtml(
        waitingText
      )}</div>`;
    }
    const initialMargin = Number(position.initial_margin || 0);
    const unrealizedPnl = Number(position.unrealized_pnl_usdt || 0);
    const roe = initialMargin > 0 ? (unrealizedPnl / initialMargin) * 100 : null;
    return `<div class="card"><strong>${escapeHtml(t("result.position_tracker"))}</strong><br/>
      ${escapeHtml(t("field.symbol"))}: ${escapeHtml(position.symbol || t("misc.na"))}<br/>
      ${escapeHtml(t("result.position_side"))}: ${escapeHtml(trackedPositionSideLabel(position))}<br/>
      ${escapeHtml(t("result.position_qty"))}: ${escapeHtml(formatMetric(position.quantity))}<br/>
      ${escapeHtml(t("result.position_notional"))}: ${escapeHtml(formatCurrency(position.notional_usdt))}<br/>
      ${escapeHtml(t("result.position_entry_price"))}: ${escapeHtml(formatMetric(position.entry_price))}<br/>
      ${escapeHtml(t("result.position_mark_price"))}: ${escapeHtml(formatMetric(position.mark_price))}<br/>
      ${escapeHtml(t("result.position_unrealized_pnl"))}: ${escapeHtml(
        formatCurrency(position.unrealized_pnl_usdt)
      )}<br/>
      ${escapeHtml(t("result.position_initial_margin"))}: ${escapeHtml(
        formatCurrency(position.initial_margin)
      )}<br/>
      ${escapeHtml(t("result.position_roe"))}: ${escapeHtml(
        roe === null ? t("misc.na") : formatMetric(roe, "%")
      )}<br/>
      ${escapeHtml(t("result.position_liq_price"))}: ${escapeHtml(
        formatMetric(position.liquidation_price)
      )}
    </div>`;
  }

  function currentExposureFromSnapshot(snapshot = state.accountSnapshot) {
    const symbol = String(byId("symbol")?.value || "").toUpperCase();
    if (!snapshot || !snapshot.account) {
      return {
        symbol,
        liveConnected: false,
        positions: [],
        openOrders: [],
        warning: "",
      };
    }
    const account = snapshot.account || {};
    const positions = Array.isArray(account.open_positions)
      ? account.open_positions.filter((item) => String(item.symbol || "").toUpperCase() === symbol)
      : [];
    const openOrders = Array.isArray(account.open_orders)
      ? account.open_orders.filter((item) => String(item.symbol || "").toUpperCase() === symbol)
      : [];
    const algoOrders = Array.isArray(account.algo_open_orders)
      ? account.algo_open_orders.filter((item) => String(item.symbol || "").toUpperCase() === symbol)
      : [];
    return {
      symbol,
      liveConnected: hasLiveAccountSnapshot(snapshot),
      positions,
      openOrders,
      algoOrders,
      warning: snapshot.warning || "",
    };
  }

  function currentExposurePnlStats(exposure) {
    const positions = Array.isArray(exposure?.positions) ? exposure.positions : [];
    const totalUnrealized = positions.reduce(
      (sum, item) => sum + Number(item?.unrealized_pnl_usdt || 0),
      0
    );
    const totalInitialMargin = positions.reduce(
      (sum, item) => sum + Number(item?.initial_margin || 0),
      0
    );
    const totalNotional = positions.reduce(
      (sum, item) => sum + Math.abs(Number(item?.notional_usdt || 0)),
      0
    );
    const roe =
      totalInitialMargin > 0 ? (totalUnrealized / totalInitialMargin) * 100 : null;
    const latestMarkPrice =
      positions.length === 1 ? Number(positions[0]?.mark_price || 0) : Number.NaN;
    return {
      totalUnrealized,
      totalInitialMargin,
      totalNotional,
      roe,
      latestMarkPrice,
      hasPosition: positions.length > 0,
    };
  }

  function renderCurrentExposure(snapshot = state.accountSnapshot) {
    const box = byId("current-exposure-status");
    const exposure = currentExposureFromSnapshot(snapshot);
    if (!snapshot) {
      box.classList.add("muted");
      box.textContent = t("placeholder.current_exposure");
      return;
    }
    if (!exposure.liveConnected) {
      box.classList.remove("muted");
      box.innerHTML = `
        <div class="status-head warn">${escapeHtml(t("result.current_exposure"))}</div>
        <div class="card">
          ${escapeHtml(t("misc.demo_only"))}
          ${
            exposure.warning
              ? `<br/><strong>${escapeHtml(t("result.market_warning"))}</strong>: ${escapeHtml(
                  translateServerText(String(exposure.warning))
                )}`
              : ""
          }
        </div>
      `;
      return;
    }

    const positionsHtml = exposure.positions.length
      ? exposure.positions
          .map(
            (position) => `<li>
              <strong class="exposure-position-side">${escapeHtml(
                trackedPositionSideLabel(position)
              )}</strong>
              <div class="exposure-stat-grid">
                <span class="exposure-stat-row">
                  <span>${escapeHtml(t("result.position_qty"))}</span>
                  <em>${escapeHtml(formatMetric(position.quantity))}</em>
                </span>
                <span class="exposure-stat-row">
                  <span>${escapeHtml(t("result.position_entry_price"))}</span>
                  <em>${escapeHtml(formatMetric(position.entry_price))}</em>
                </span>
                <span class="exposure-stat-row">
                  <span>${escapeHtml(t("result.position_notional"))}</span>
                  <em>${escapeHtml(formatCurrency(position.notional_usdt))}</em>
                </span>
                <span class="exposure-stat-row">
                  <span>${escapeHtml(t("result.position_unrealized_pnl"))}</span>
                  <em>${escapeHtml(formatCurrency(position.unrealized_pnl_usdt))}</em>
                </span>
              </div>
            </li>`
          )
          .join("")
      : `<li class="exposure-empty">${escapeHtml(t("result.position_missing"))}</li>`;

    const openOrdersHtml = exposure.openOrders
      .map(
        (order) => `<li>
          <strong>${escapeHtml(
            `${t("result.order_type")}: ${order.type || t("misc.na")}`
          )}</strong><br/>
          ${escapeHtml(t("result.order_side"))}: ${escapeHtml(
            `${order.side || t("misc.na")} / ${order.position_side || "BOTH"}`
          )}<br/>
          ${escapeHtml(t("result.order_price"))}: ${escapeHtml(
            Number(order.price || 0) > 0 ? formatMetric(order.price) : t("misc.na")
          )}<br/>
          ${escapeHtml(t("result.order_stop_price"))}: ${escapeHtml(
            Number(order.stop_price || 0) > 0 ? formatMetric(order.stop_price) : t("misc.na")
          )}<br/>
          ${escapeHtml(t("result.order_qty"))}: ${escapeHtml(
            Number(order.orig_qty || 0) > 0 ? formatMetric(order.orig_qty) : t("misc.na")
          )}<br/>
          ${escapeHtml(t("result.order_status"))}: ${escapeHtml(order.status || t("misc.na"))}
        </li>`
      )
      .join("");

    const action = state.currentExposureActionResult;
    const pnl = currentExposurePnlStats(exposure);
    const pnlToneClass =
      pnl.totalUnrealized > 0 ? "pnl-positive" : pnl.totalUnrealized < 0 ? "pnl-negative" : "pnl-neutral";
    const pnlCardHtml = pnl.hasPosition
      ? `<div class="card exposure-pnl-card ${pnlToneClass}">
          <strong>${escapeHtml(t("result.position_unrealized_pnl"))}</strong>
          <div class="exposure-pnl-value">${escapeHtml(formatCurrency(pnl.totalUnrealized))}</div>
          <div class="exposure-pnl-meta">
            <span class="exposure-stat-row">
              <span>${escapeHtml(t("result.position_initial_margin"))}</span>
              <em>${escapeHtml(formatCurrency(pnl.totalInitialMargin))}</em>
            </span>
            <span class="exposure-stat-row">
              <span>${escapeHtml(t("result.position_notional"))}</span>
              <em>${escapeHtml(formatCurrency(pnl.totalNotional))}</em>
            </span>
            <span class="exposure-stat-row">
              <span>${escapeHtml(t("result.position_roe"))}</span>
              <em>${escapeHtml(
                pnl.roe === null ? t("misc.na") : formatMetric(pnl.roe, "%")
              )}</em>
            </span>
            <span class="exposure-stat-row">
              <span>${escapeHtml(t("result.position_mark_price"))}</span>
              <em>${escapeHtml(
                Number.isFinite(pnl.latestMarkPrice) && pnl.latestMarkPrice > 0
                  ? formatMetric(pnl.latestMarkPrice)
                  : t("misc.na")
              )}</em>
            </span>
          </div>
          <div class="exposure-pnl-live">${escapeHtml(t("result.live_refreshing"))}</div>
        </div>`
      : `<div class="card exposure-pnl-card pnl-neutral">
          <strong>${escapeHtml(t("result.position_unrealized_pnl"))}</strong>
          <div class="exposure-pnl-value">${escapeHtml(formatCurrency(0))}</div>
          <div class="exposure-pnl-meta">
            <span class="exposure-empty">${escapeHtml(t("result.position_missing"))}</span>
          </div>
        </div>`;

    box.classList.remove("muted");
    box.innerHTML = `
      <div class="exposure-topbar">
        <div class="exposure-head-stack">
          <div class="status-head ok">${escapeHtml(t("result.current_exposure"))}</div>
          <div class="exposure-summary-inline">
            <span class="exposure-connection-pill">${escapeHtml(t("misc.live_connected"))}</span>
          </div>
        </div>
        <div class="inline-action-row">
          <button id="btn-close-current-position-inline" class="btn danger tiny" type="button">${escapeHtml(
            t("btn.close_current_position")
          )}</button>
          <button id="btn-cancel-current-orders-inline" class="btn warning tiny" type="button">${escapeHtml(
            t("btn.cancel_current_orders")
          )}</button>
        </div>
      </div>
      ${
        action
          ? `<div class="card${
              action.ok ? "" : " block-card"
            }"><strong>${escapeHtml(t("result.current_action"))}</strong><br/>
              ${escapeHtml(translateServerText(action.message || t("misc.na")))}
            </div>`
          : ""
      }
      <div class="exposure-grid">
        <div class="card exposure-position-card">
          <strong>${escapeHtml(t("result.current_position_summary"))}</strong>
          <ul class="agent-list">${positionsHtml}</ul>
        </div>
        ${pnlCardHtml}
        ${
          exposure.openOrders.length
            ? `<div class="card exposure-orders-card">
                <strong>${escapeHtml(t("result.current_open_orders"))}</strong>
                <ul class="agent-list">${openOrdersHtml}</ul>
              </div>`
            : ""
        }
      </div>
    `;
    const cancelButton = byId("btn-cancel-current-orders-inline");
    if (cancelButton) {
      cancelButton.addEventListener("pointerdown", () => {
        pinCurrentExposurePanel(10000);
      });
      cancelButton.addEventListener("click", onCancelCurrentOrders);
    }
    const closeButton = byId("btn-close-current-position-inline");
    if (closeButton) {
      closeButton.addEventListener("pointerdown", () => {
        pinCurrentExposurePanel(10000);
      });
      closeButton.addEventListener("click", onCloseCurrentPosition);
    }
  }

  function stopPositionTracker({ clearTarget = false } = {}) {
    if (state.positionTrackerTimer) {
      clearInterval(state.positionTrackerTimer);
      state.positionTrackerTimer = null;
    }
    if (clearTarget) {
      state.positionTrackerTarget = null;
    }
  }

  function startPositionTracker(target) {
    state.positionTrackerTarget = {
      symbol: String(target.symbol || "").toUpperCase(),
      intentSide: String(target.intentSide || "").toUpperCase(),
      positionSide: String(target.positionSide || "").toUpperCase(),
      startedAt: Date.now(),
    };
    stopPositionTracker();
    syncAccountSnapshot({ applyForm: false });
    state.positionTrackerTimer = setInterval(() => {
      syncAccountSnapshot({ applyForm: false });
    }, 3000);
  }

  function renderMarketSync(data) {
    const box = byId("market-sync-status");
    const market = data.market || {};
    const trade = data.suggested_trade || {};
    const side = String(byId("side")?.value || "LONG").toUpperCase();
    const sideLabel = side === "SHORT" ? t("opt.short") : t("opt.long");
    const hasWarning = Boolean(data.warning);
    const statusClass = data.live ? "ok" : "warn";
    const symbol = String(data.symbol || "BNBUSDT").toUpperCase();
    const entry = Number(trade.entry_price || 0);
    const stop = Number(trade.stop_loss_price || 0);
    const takeProfit = Number(trade.take_profit_price || 0);
    const riskPctRaw =
      entry > 0
        ? side === "SHORT"
          ? ((stop - entry) / entry) * 100
          : ((entry - stop) / entry) * 100
        : NaN;
    const rewardPctRaw =
      entry > 0
        ? side === "SHORT"
          ? ((entry - takeProfit) / entry) * 100
          : ((takeProfit - entry) / entry) * 100
        : NaN;
    const riskPct = Number.isFinite(riskPctRaw) ? Math.max(riskPctRaw, 0) : NaN;
    const rewardPct = Number.isFinite(rewardPctRaw) ? Math.max(rewardPctRaw, 0) : NaN;
    const rewardRisk =
      Number.isFinite(riskPct) && riskPct > 0 && Number.isFinite(rewardPct)
        ? rewardPct / riskPct
        : NaN;
    const switchButtonsHtml = marketSwitchSymbols(data).length
      ? `<div class="market-switch-row">${marketSwitchSymbols(data)
          .map(
            (item) => `<button class="market-switch-chip${
              item.symbol === symbol ? " active" : ""
            }" type="button" data-market-symbol="${escapeHtml(item.symbol)}">
                <span class="market-switch-symbol">${escapeHtml(item.symbol)}</span>
                <strong>${escapeHtml(formatMetric(item.lastPrice))}</strong>
              </button>`
          )
          .join("")}</div>`
      : "";

    box.classList.remove("muted");
    box.classList.add("market-box");
    box.innerHTML = `
      <div class="market-header-row">
        <div class="status-head ${statusClass}">
          ${escapeHtml(t("result.market_sync"))}
        </div>
        ${switchButtonsHtml}
      </div>
      <div class="market-hero-grid">
        <div class="market-price-panel">
          <div class="market-panel-head">
            <div class="market-chip-row">
              <span class="market-direction-chip ${side === "SHORT" ? "short" : "long"}">${escapeHtml(
                sideLabel
              )}</span>
            </div>
            <div class="market-volatility-pill">
              <span class="market-stat-label">24H</span>
              <strong>${escapeHtml(formatMetric(market.volatility_24h_pct, "%"))}</strong>
            </div>
          </div>
          <div class="market-primary-price">${escapeHtml(formatMetric(market.last_price))}</div>
          <div class="market-price-rail">
            <div class="market-price-mini">
              <span>最新</span>
              <strong>${escapeHtml(formatMetric(market.last_price))}</strong>
            </div>
            <div class="market-price-mini">
              <span>买一</span>
              <strong>${escapeHtml(formatMetric(market.bid_price))}</strong>
            </div>
            <div class="market-price-mini">
              <span>卖一</span>
              <strong>${escapeHtml(formatMetric(market.ask_price))}</strong>
            </div>
          </div>
        </div>
      </div>
      <div class="market-plan-grid">
        <div class="market-plan-metric">
          <span>${escapeHtml(t("field.entry_price"))}</span>
          <strong>${escapeHtml(formatMetric(trade.entry_price))}</strong>
        </div>
        <div class="market-plan-metric">
          <span>${escapeHtml(t("field.stop_loss_price"))}</span>
          <strong>${escapeHtml(formatMetric(trade.stop_loss_price))}</strong>
        </div>
        <div class="market-plan-metric">
          <span>${escapeHtml(t("field.take_profit_price"))}</span>
          <strong>${escapeHtml(formatMetric(trade.take_profit_price))}</strong>
        </div>
      </div>
      <div class="market-signal-grid">
        <div class="market-signal-card">
          <span class="market-signal-label">${escapeHtml(t("field.stop_loss_rate"))}</span>
          <strong>${escapeHtml(Number.isFinite(riskPct) ? formatMetric(riskPct, "%") : t("misc.na"))}</strong>
        </div>
        <div class="market-signal-card">
          <span class="market-signal-label">${escapeHtml(t("field.take_profit_rate"))}</span>
          <strong>${escapeHtml(Number.isFinite(rewardPct) ? formatMetric(rewardPct, "%") : t("misc.na"))}</strong>
        </div>
        <div class="market-signal-card">
          <span class="market-signal-label">${escapeHtml(t("metric.reward_risk_ratio"))}</span>
          <strong>${escapeHtml(Number.isFinite(rewardRisk) ? formatMetric(rewardRisk, "x") : t("misc.na"))}</strong>
        </div>
      </div>
      ${
        hasWarning
          ? `<div class="card"><strong>${escapeHtml(t(
              "result.market_warning"
            ))}</strong>: ${escapeHtml(translateServerText(data.warning))}</div>`
          : ""
      }
    `;
    box.querySelectorAll("[data-market-symbol]").forEach((button) => {
      button.addEventListener("click", () => {
        const nextSymbol = String(button.getAttribute("data-market-symbol") || "").toUpperCase();
        if (!nextSymbol || nextSymbol === String(byId("symbol").value || "").toUpperCase()) {
          return;
        }
        byId("symbol").value = nextSymbol;
        onSymbolChange();
      });
    });
  }

  function renderOrderTest(data) {
    const preview = data.preview || {};
    const execution = data.execution || {};
    const cancel = data.cancel || {};
    const compactOpenedState =
      data.ok &&
      String(data.status) === "opened" &&
      execution.orderId &&
      !data.emergency_close?.orderId;
    const statusClass = data.ok
      ? "ok"
      : ["exchange_rejected", "protection_failed"].includes(String(data.status))
        ? "block"
        : "warn";
    const compactPreviewText = (() => {
      const parts = [
        preview.symbol,
        preview.intent_side
          ? `${preview.intent_side}->${preview.order_side || preview.side}`
          : preview.side,
        preview.type,
        preview.quantity,
      ].filter(Boolean);
      if (preview.price) {
        parts.push("@", preview.price);
      }
      return parts.join(" ");
    })();

    const compactTickerParts = [
      `${t("result.order_status")}: ${orderStatusLabel(data.status)}`,
      data.mode ? `${t("result.order_mode")}: ${orderModeLabel(data.mode)}` : "",
      translateServerText(
        data.message || (compactOpenedState ? t("result.order_opened_compact") : t("misc.na"))
      ),
      compactPreviewText ? `${t("result.order_preview")}: ${compactPreviewText}` : "",
      preview.requested_notional_usdt
        ? `${t("result.requested_notional")}: ${formatCurrency(preview.requested_notional_usdt)}`
        : "",
      execution.orderId
        ? `${t(String(data.status) === "opened" ? "result.live_open_order" : "result.live_order")}: orderId=${execution.orderId}`
        : "",
      cancel.orderId
        ? `${t("result.cancel_result")}: ${cancel.status || "CANCELED"}`
        : "",
    ].filter(Boolean);

    renderOrderTicker(compactTickerParts.join(" · "), statusClass);
    renderAgentSteps();
    renderAgentBriefing();
    updateActionState();
  }

  function applyMarketSnapshotToForm(data) {
    const market = data.market || {};
    const trade = data.suggested_trade || {};

    if (trade.entry_price !== undefined) setValue("entry_price", trade.entry_price);
    if (trade.stop_loss_price !== undefined) setValue("stop_loss_price", trade.stop_loss_price);
    if (trade.take_profit_price !== undefined) {
      setValue("take_profit_price", trade.take_profit_price);
    }
    if (market.volatility_24h_pct !== undefined) {
      setValue("volatility_24h_pct", market.volatility_24h_pct);
    }
    if (market.bid_ask_spread_bps !== undefined) {
      setValue("bid_ask_spread_bps", market.bid_ask_spread_bps);
    }
    if (market.liquidity_depth_score !== undefined) {
      setValue("liquidity_depth_score", market.liquidity_depth_score);
    }
    if (!shouldPreserveOrderPanel()) {
      resetTradeStateIfEdited();
    } else {
      updatePositionMarginField();
      updateActionState();
    }
  }

  function applyAccountSnapshotToForm(data) {
    if (!hasLiveAccountSnapshot(data)) {
      if (!shouldPreserveOrderPanel()) {
        resetTradeStateIfEdited();
      } else {
        updateActionState();
      }
      return;
    }
    const autoFill = data.auto_fill || {};
    if (autoFill.account_equity_usdt !== undefined) {
      setValue("account_equity_usdt", autoFill.account_equity_usdt);
      if (state.positionRatio !== null) {
        applyPositionRatio(state.positionRatio, { reset: false });
      } else if (state.positionNotionalMode !== "manual") {
        applyPositionRatio(0.1, { reset: false });
      } else {
        syncPositionRatioFromForm();
      }
    }
    if (!state.profileConfirmed) {
      if (autoFill.trades_last_24h !== undefined) {
        setValue("trades_last_24h", autoFill.trades_last_24h);
      }
      if (autoFill.consecutive_losses !== undefined) {
        setValue("consecutive_losses", autoFill.consecutive_losses);
      }
      if (autoFill.day_pnl_pct !== undefined) {
        setValue("day_pnl_pct", autoFill.day_pnl_pct);
      }
      syncWizardPathState();
      renderWizard();
      if (allWizardAnswered()) {
        scheduleProfileRefresh();
      }
    }
    if (!shouldPreserveOrderPanel()) {
      resetTradeStateIfEdited();
    } else {
      updatePositionMarginField();
      updateActionState();
    }
  }

  async function syncAccountSnapshot({ applyForm = true } = {}) {
    try {
      await ensureRuntimeReady();
    } catch (err) {
      resetAccountSyncState();
      byId("account-sync-status").textContent = err.message;
      renderAgentBriefing();
      return;
    }
    const requestId = ++state.accountSyncRequestId;
    const box = byId("account-sync-status");
    box.classList.add("muted");
    box.textContent = t("agent.status_syncing");
    try {
      const params = new URLSearchParams({
        symbol: byId("symbol").value.toUpperCase(),
        profile: currentProfileName(),
      });
      const data = await getJSON(`/v1/binance/account-snapshot?${params.toString()}`);
      if (requestId !== state.accountSyncRequestId) {
        return;
      }
      state.accountSnapshot = data;
      if (applyForm) {
        applyAccountSnapshotToForm(data);
      }
      renderAccountSync(data);
      if (!shouldPreserveCurrentExposurePanel()) {
        renderCurrentExposure(data);
      }
      if (state.orderTestResult && !state.orderActionPending) {
        renderOrderTest(state.orderTestResult);
      }
      renderAgentBriefing();
    } catch (err) {
      if (requestId !== state.accountSyncRequestId) {
        return;
      }
      resetAccountSyncState();
      byId("account-sync-status").textContent = `${t("alert.account_sync_failed")}: ${err.message}`;
      renderAgentBriefing();
    }
  }

  async function syncMarketSnapshot({ applyForm = true } = {}) {
    try {
      await ensureRuntimeReady();
    } catch (err) {
      resetMarketSyncState();
      byId("market-sync-status").textContent = err.message;
      renderAgentBriefing();
      return;
    }
    const requestId = ++state.marketSyncRequestId;
    const box = byId("market-sync-status");
    box.classList.add("muted");
    box.textContent = t("status.market_loading");
    try {
      const params = new URLSearchParams({
        symbol: byId("symbol").value.toUpperCase(),
        side: byId("side").value,
        profile: currentProfileName(),
      });
      const data = await getJSON(`/v1/binance/market-snapshot?${params.toString()}`);
      if (requestId !== state.marketSyncRequestId) {
        return;
      }
      state.marketSnapshot = data;
      if (applyForm) {
        applyMarketSnapshotToForm(data);
      }
      renderMarketSync(data);
      renderAgentBriefing();
    } catch (err) {
      if (requestId !== state.marketSyncRequestId) {
        return;
      }
      resetMarketSyncState();
      byId("market-sync-status").textContent = `${t("alert.market_sync_failed")}: ${err.message}`;
      renderAgentBriefing();
    }
  }

  function applySuggestedPlanToForm() {
    if (!state.tradeResult || !state.tradeResult.suggested_plan) {
      return;
    }
    const p = state.tradeResult.suggested_plan;
    byId("leverage").value = p.leverage;
    normalizeLeverageInput();
    setValue("position_notional_usdt", p.position_notional_usdt);
    if (p.stop_loss_price !== null && p.stop_loss_price !== undefined) {
      byId("stop_loss_price").value = p.stop_loss_price;
    }
    if (p.take_profit_price !== null && p.take_profit_price !== undefined) {
      byId("take_profit_price").value = p.take_profit_price;
    }
    syncPositionRatioFromForm();
    resetOrderTestState();
    updateActionState();
  }

  function resetTradeStateIfEdited() {
    if (shouldPreserveOrderPanel()) {
      updatePositionMarginField();
      updateActionState();
      return;
    }
    const hadTradeResult = Boolean(state.tradeResult);
    state.tradeResult = null;
    stopPositionTracker({ clearTarget: true });
    resetOrderTestState();
    if (!hadTradeResult) {
      updateActionState();
      return;
    }
    const box = byId("trade-result");
    box.classList.add("muted");
    box.textContent = t("placeholder.trade_result");
    updateDecisionSignalPanel();
    updateActionState();
    renderAgentBriefing();
  }

  function resetProfileStateIfEdited({ preserveRenderedProfile = false } = {}) {
    if (state.profileRefreshTimer) {
      clearTimeout(state.profileRefreshTimer);
      state.profileRefreshTimer = null;
    }
    state.profileRefreshRequestId += 1;
    const summaryBox = byId("profile-result-inline");
    const detailBox = byId("profile-result");
    const hadProfile = Boolean(state.profileResult);
    const hadRenderedProfile = Boolean(
      summaryBox && detailBox && (!summaryBox.classList.contains("muted") || !detailBox.classList.contains("muted"))
    );
    const wasConfirmed = state.profileConfirmed;
    state.profileResult = null;
    state.profileConfirmed = false;
    state.profileIsProvisional = false;
    state.profileStatusProfile = null;
    state.profileStatusScore = null;
    byId("selected_profile").value = "";
    stopPositionTracker({ clearTarget: true });
    resetTradeStateIfEdited();

    if (hadProfile || hadRenderedProfile || wasConfirmed) {
      if (preserveRenderedProfile) {
        setProfileStatus("loading");
        renderAgentBriefing();
        return;
      }
      summaryBox.classList.add("muted");
      summaryBox.textContent = t("placeholder.profile_result");
      detailBox.classList.add("muted");
      detailBox.textContent = t("placeholder.profile_result");
      setProfileStatus("dirty");
      renderAgentBriefing();
      return;
    }
    setProfileStatus("await");
    renderAgentBriefing();
  }

  function onConfirmProfile() {
    if (!state.profileResult) {
      alert(t("alert.no_profile_to_confirm"));
      return;
    }
    if (state.profileIsProvisional || !allWizardAnswered()) {
      alert(t("alert.wizard_incomplete"));
      return;
    }
    state.profileConfirmed = true;
    state.profileIsProvisional = false;
    setProfileStatus(
      "confirmed",
      state.profileResult.profile,
      state.profileResult.profile_score
    );
    syncAccountSnapshot();
    syncMarketSnapshot();
  }

  function onProfileInputsChanged() {
    const shouldKeepPreview = answeredWizardCount() > 0;
    resetProfileStateIfEdited({ preserveRenderedProfile: shouldKeepPreview });
    if (shouldKeepPreview) {
      scheduleProfileRefresh();
    }
  }

  async function onEvaluateTrade() {
    if (!state.profileConfirmed || !state.profileResult) {
      alert(t("alert.confirm_profile_first"));
      return;
    }
    try {
      await ensureRuntimeReady();
      const data = await postJSON("/v1/evaluate", evaluatePayload());
      state.tradeResult = data;
      renderTrade(data);
      updateActionState();
    } catch (err) {
      alert(`${t("alert.evaluate_failed")}: ${err.message}`);
    }
  }

  async function runTradeEvaluation() {
    await ensureRuntimeReady();
    const data = await postJSON("/v1/evaluate", evaluatePayload());
    state.tradeResult = data;
    renderTrade(data);
    updateActionState();
    return data;
  }

  async function runDemoOrderTest() {
    const data = await postJSON("/v1/binance/demo-order-test", {
      trade: evaluatePayload().trade,
    });
    state.orderTestResult = data;
    if (!state.orderActionPending) {
      renderOrderTest(data);
    }
    updateActionState();
    return data;
  }

  async function ensureExecutionReady() {
    if (!state.profileConfirmed || !state.profileResult) {
      setOrderTestStatus(t("alert.execution_requires_profile"), "warn");
      throw new Error(t("alert.execution_requires_profile"));
    }
    if (!state.tradeResult) {
      setOrderTestStatus(t("status.market_loading"), "warn");
      await runTradeEvaluation();
    }
    if (!state.tradeResult) {
      setOrderTestStatus(t("alert.execution_requires_evaluation"), "warn");
      throw new Error(t("alert.execution_requires_evaluation"));
    }
    if (state.tradeResult.decision === "BLOCK") {
      setOrderTestStatus(t("alert.execution_blocked"), "block");
      throw new Error(t("alert.execution_blocked"));
    }
    if (!state.orderTestResult || !state.orderTestResult.ok || state.orderTestResult.status !== "validated") {
      setOrderTestStatus(t("status.order_loading"), "warn");
      const data = await runDemoOrderTest();
      if (!data.ok || data.status !== "validated") {
        throw new Error(data.message || t("hint.next_order_test"));
      }
    }
  }

  async function onDemoOrderTest() {
    setOrderTestStatus(t("status.order_loading"), "warn");
    try {
      await ensureRuntimeReady();
      await runDemoOrderTest();
    } catch (err) {
      clearOrderActionPending({ keepPinnedMs: 3000 });
      setOrderTestStatus(`${t("alert.order_test_failed")}: ${err.message}`, "block");
    }
  }

  async function onLiveOrderTrial() {
    document.activeElement?.blur?.();
    pinOrderPanel(15000);
    setOrderActionPending(t("status.live_order_loading"));
    try {
      await ensureExecutionReady();
      setOrderActionPending(t("status.live_order_loading"));
      const data = await postJSON("/v1/binance/live-order", {
        confirm_live_execution: true,
        trade: evaluatePayload().trade,
      });
      stopPositionTracker({ clearTarget: true });
      state.orderTestResult = data;
      clearOrderActionPending();
      renderOrderTest(data);
      updateActionState();
    } catch (err) {
      clearOrderActionPending({ keepPinnedMs: 5000 });
      setOrderTestStatus(`${t("alert.live_order_failed")}: ${err.message}`, "block");
    }
  }

  async function onLiveOpenOrder() {
    document.activeElement?.blur?.();
    pinOrderPanel(15000);
    setOrderActionPending(t("status.live_open_order_loading"));
    try {
      await ensureExecutionReady();
      setOrderActionPending(t("status.live_open_order_loading"));
      const data = await postJSON("/v1/binance/live-open-order", {
        confirm_live_execution: true,
        trade: evaluatePayload().trade,
      });
      state.currentExposureActionResult = null;
      state.orderTestResult = data;
      if (data.execution && data.preview) {
        startPositionTracker({
          symbol: data.preview.symbol,
          intentSide: data.preview.intent_side,
          positionSide: data.preview.positionSide,
        });
      } else {
        stopPositionTracker({ clearTarget: true });
      }
      clearOrderActionPending();
      renderOrderTest(data);
      updateActionState();
    } catch (err) {
      clearOrderActionPending({ keepPinnedMs: 5000 });
      setOrderTestStatus(`${t("alert.live_open_order_failed")}: ${err.message}`, "block");
    }
  }

  async function onViewCurrentExposure() {
    state.currentExposureActionResult = null;
    const box = byId("current-exposure-status");
    box.classList.remove("muted");
    box.innerHTML = `<div class="status-head warn">${escapeHtml(t(
      "result.current_exposure"
    ))}</div><div class="card">${escapeHtml(t("status.current_exposure_loading"))}</div>`;
    try {
      await ensureRuntimeReady();
      await syncAccountSnapshot({ applyForm: false });
      const exposure = currentExposureFromSnapshot();
      if (exposure.liveConnected && exposure.positions.length) {
        startPositionTracker({
          symbol: exposure.symbol,
          intentSide: "",
          positionSide: "",
        });
      }
    } catch (err) {
      box.classList.remove("muted");
      box.innerHTML = `<div class="status-head warn">${escapeHtml(t(
        "result.current_exposure"
      ))}</div><div class="card">${escapeHtml(err.message)}</div>`;
    }
  }

  async function onCancelCurrentOrders() {
    document.activeElement?.blur?.();
    pinCurrentExposurePanel(15000);
    setCurrentExposurePending(t("status.cancel_orders_loading"));
    try {
      await ensureRuntimeReady();
      const data = await postJSON("/v1/binance/cancel-current-orders", {
        symbol: byId("symbol").value.toUpperCase(),
      });
      state.currentExposureActionResult = data;
      clearCurrentExposurePending();
      await syncAccountSnapshot({ applyForm: false });
      renderCurrentExposure(state.accountSnapshot);
    } catch (err) {
      clearCurrentExposurePending({ keepPinnedMs: 5000 });
      state.currentExposureActionResult = {
        ok: false,
        message: `${t("alert.cancel_current_orders_failed")}: ${err.message}`,
      };
      renderCurrentExposure();
    }
  }

  async function onCloseCurrentPosition() {
    document.activeElement?.blur?.();
    pinCurrentExposurePanel(15000);
    setCurrentExposurePending(t("status.close_position_loading"));
    try {
      await ensureRuntimeReady();
      const data = await postJSON("/v1/binance/close-current-position", {
        symbol: byId("symbol").value.toUpperCase(),
      });
      state.currentExposureActionResult = data;
      stopPositionTracker({ clearTarget: true });
      clearCurrentExposurePending();
      await syncAccountSnapshot({ applyForm: false });
      renderCurrentExposure(state.accountSnapshot);
    } catch (err) {
      clearCurrentExposurePending({ keepPinnedMs: 5000 });
      state.currentExposureActionResult = {
        ok: false,
        message: `${t("alert.close_current_position_failed")}: ${err.message}`,
      };
      renderCurrentExposure();
    }
  }

  async function onApplyFixAndRecheck() {
    applySuggestedPlanToForm();
    await onEvaluateTrade();
  }

  function onSymbolChange() {
    stopPositionTracker({ clearTarget: true });
    state.currentExposureActionResult = null;
    applySymbolPreset(byId("symbol").value);
    syncAccountSnapshot();
    syncMarketSnapshot();
  }

  function onSideChange() {
    stopPositionTracker({ clearTarget: true });
    resetTradeStateIfEdited();
    syncMarketSnapshot();
  }

  function onPositionNotionalEdited() {
    state.positionNotionalMode = "manual";
    syncPositionRatioFromForm();
    updatePositionMarginField();
    resetTradeStateIfEdited();
  }

  function onLeverageEdited() {
    if (state.positionRatio !== null) {
      applyPositionRatio(state.positionRatio);
      return;
    }
    updatePositionMarginField();
    resetTradeStateIfEdited();
  }

  function onAccountEquityEdited() {
    if (state.positionRatio !== null) {
      applyPositionRatio(state.positionRatio);
      return;
    }
    syncPositionRatioFromForm();
    resetTradeStateIfEdited();
  }

  function setLanguage(lang) {
    if (!I18N[lang]) {
      return;
    }
    state.lang = lang;
    localStorage.setItem("cpg_demo_lang", lang);
    applyI18n();
    if (state.profileResult) {
      renderProfile(state.profileResult);
    }
    if (state.tradeResult) {
      renderTrade(state.tradeResult);
    }
    if (state.marketSnapshot) {
      renderMarketSync(state.marketSnapshot);
    } else {
      resetMarketSyncState();
    }
    if (state.accountSnapshot) {
      renderAccountSync(state.accountSnapshot);
      renderCurrentExposure(state.accountSnapshot);
    } else {
      resetAccountSyncState();
    }
    if (state.orderTestResult && !state.orderActionPending) {
      renderOrderTest(state.orderTestResult);
    } else if (!state.orderActionPending) {
      resetOrderTestState();
    }
    renderAgentBriefing();
  }

  function detectInitialLanguage() {
    const saved = localStorage.getItem("cpg_demo_lang");
    if (saved && I18N[saved]) {
      return saved;
    }
    return navigator.language && navigator.language.toLowerCase().startsWith("zh")
      ? "zh"
      : "en";
  }

  function init() {
    ids.forEach((id) => {
      if (!byId(id)) {
        throw new Error(`Missing required field: ${id}`);
      }
    });
    uiIds.forEach((id) => {
      if (!byId(id)) {
        throw new Error(`Missing required ui element: ${id}`);
      }
    });

    loadWizardDefaults();
    renderSymbolSelect();
    setProfileStatus("await");
    resetAccountSyncState();
    resetMarketSyncState();
    resetOrderTestState();
    renderWizard();
    renderAgentSteps();
    renderAgentBriefing();
    applySymbolPreset(byId("symbol").value);
    renderPositionRatioButtons();

    byId("btn-confirm-profile").addEventListener("click", onConfirmProfile);
    byId("btn-prev-step").addEventListener("click", onPrevWizardStep);
    byId("btn-reset-wizard").addEventListener("click", onResetWizard);
    byId("btn-evaluate").addEventListener("click", onEvaluateTrade);
    byId("btn-order-test").addEventListener("click", onDemoOrderTest);
    byId("btn-live-order").addEventListener("click", onLiveOrderTrial);
    byId("btn-live-open-order").addEventListener("click", onLiveOpenOrder);
    byId("btn-view-current-exposure").addEventListener("click", onViewCurrentExposure);
    byId("btn-apply-fix").addEventListener("click", onApplyFixAndRecheck);
    ["btn-evaluate", "btn-order-test", "btn-live-order", "btn-live-open-order"].forEach((id) => {
      const button = byId(id);
      if (!button) {
        return;
      }
      button.addEventListener("pointerdown", () => {
        pinOrderPanel(10000);
      });
    });
    byId("lang-zh").addEventListener("click", () => setLanguage("zh"));
    byId("lang-en").addEventListener("click", () => setLanguage("en"));
    byId("symbol").addEventListener("change", onSymbolChange);
    byId("side").addEventListener("change", onSideChange);
    byId("position-ratio-group")
      .querySelectorAll("[data-ratio]")
      .forEach((button) =>
        button.addEventListener("click", () =>
          applyPositionRatio(Number(button.dataset.ratio || ""))
        )
      );
    profileInputIds.forEach((id) => {
      byId(id).addEventListener("input", onProfileInputsChanged);
      byId(id).addEventListener("change", onProfileInputsChanged);
    });
    tradeInputIds.forEach((id) => {
      const handler =
        id === "position_notional_usdt"
          ? onPositionNotionalEdited
          : id === "leverage"
            ? onLeverageEdited
          : id === "account_equity_usdt"
            ? onAccountEquityEdited
            : resetTradeStateIfEdited;
      byId(id).addEventListener("input", handler);
      byId(id).addEventListener("change", handler);
    });
    byId("leverage").addEventListener("blur", normalizeLeverageInput);

    setLanguage(detectInitialLanguage());
    updatePositionMarginField();
    updateDecisionSignalPanel();
    loadSymbolCatalog();
    syncRuntimeHealth().then(() => {
      if (!state.runtimeMismatch) {
        syncAccountSnapshot();
        syncMarketSnapshot();
      }
    });
    state.runtimeHealthTimer = window.setInterval(() => {
      syncRuntimeHealth({ allowRecoverySync: true });
    }, 4000);
  }

  init();
})();
