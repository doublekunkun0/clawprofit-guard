#!/usr/bin/env python3
"""Entry point for ClawProfit Guard demo and HTTP service."""

from __future__ import annotations

import argparse
import json
import os
import sys
import threading
import time
from pathlib import Path
from typing import Dict

from src.claw_profit_guard.engine import evaluate_trade
from src.claw_profit_guard.models import EvaluationInput
from src.claw_profit_guard.risk_profile import recommend_profile
from src.claw_profit_guard.runtime import compute_backend_fingerprint, short_fingerprint
from src.claw_profit_guard.service import run_server


PRESETS: Dict[str, Dict] = {
    "safe": {
        "trade": {
            "symbol": "BTCUSDT",
            "side": "LONG",
            "entry_price": 91000,
            "stop_loss_price": 89200,
            "leverage": 3,
            "position_notional_usdt": 300,
            "account_equity_usdt": 3500,
        },
        "market": {
            "volatility_24h_pct": 2.1,
            "bid_ask_spread_bps": 2,
            "liquidity_depth_score": 92,
        },
        "behavior": {
            "consecutive_losses": 0,
            "trades_last_24h": 3,
            "day_pnl_pct": 1.2,
        },
    },
    "warning": {
        "trade": {
            "symbol": "ETHUSDT",
            "side": "LONG",
            "entry_price": 5200,
            "stop_loss_price": 5020,
            "leverage": 10,
            "position_notional_usdt": 1500,
            "account_equity_usdt": 2800,
        },
        "market": {
            "volatility_24h_pct": 5.4,
            "bid_ask_spread_bps": 7,
            "liquidity_depth_score": 74,
        },
        "behavior": {
            "consecutive_losses": 2,
            "trades_last_24h": 10,
            "day_pnl_pct": -2.9,
        },
    },
    "risky": {
        "trade": {
            "symbol": "1000PEPEUSDT",
            "side": "LONG",
            "entry_price": 0.021,
            "stop_loss_price": 0.0204,
            "leverage": 35,
            "position_notional_usdt": 2400,
            "account_equity_usdt": 1200,
        },
        "market": {
            "volatility_24h_pct": 16.2,
            "bid_ask_spread_bps": 30,
            "liquidity_depth_score": 40,
        },
        "behavior": {
            "consecutive_losses": 4,
            "trades_last_24h": 26,
            "day_pnl_pct": -9.1,
        },
    },
}

PROFILE_PRESETS: Dict[str, Dict] = {
    "conservative_candidate": {
        "quiz": {
            "experience_level": "beginner",
            "risk_tolerance": "low",
            "leverage_preference": "low",
            "stop_loss_discipline": "always",
            "revenge_tendency": "never",
            "trading_frequency": "low",
            "max_drawdown_comfort_pct": 3,
        },
        "behavior": {
            "consecutive_losses": 0,
            "trades_last_24h": 4,
            "day_pnl_pct": 0.5,
        },
    },
    "aggressive_downgraded": {
        "quiz": {
            "experience_level": "advanced",
            "risk_tolerance": "high",
            "leverage_preference": "high",
            "stop_loss_discipline": "rarely",
            "revenge_tendency": "often",
            "trading_frequency": "high",
            "max_drawdown_comfort_pct": 14,
        },
        "behavior": {
            "consecutive_losses": 5,
            "trades_last_24h": 22,
            "day_pnl_pct": -8.2,
        },
    },
}


def _load_workspace_env_files() -> None:
    workspace_root = Path(__file__).resolve().parent
    for filename in (".env.local", ".env"):
        env_path = workspace_root / filename
        if not env_path.exists() or not env_path.is_file():
            continue
        try:
            lines = env_path.read_text(encoding="utf-8").splitlines()
        except OSError:
            continue
        for raw_line in lines:
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            if not key or key in os.environ:
                continue
            value = value.strip().strip('"').strip("'")
            os.environ[key] = value


def _run_demo(preset: str) -> None:
    payload = PRESETS[preset]
    result = evaluate_trade(EvaluationInput.from_dict(payload))
    print(json.dumps(result.to_dict(), ensure_ascii=True, indent=2))


def _run_profile_demo(preset: str) -> None:
    payload = PROFILE_PRESETS[preset]
    result = recommend_profile(payload)
    print(json.dumps(result.to_dict(), ensure_ascii=True, indent=2))


def _start_reload_watcher(interval_seconds: float) -> None:
    baseline = compute_backend_fingerprint()

    def watch() -> None:
        while True:
            time.sleep(interval_seconds)
            current = compute_backend_fingerprint()
            if current == baseline:
                continue
            print(
                "Backend changes detected "
                f"({short_fingerprint(baseline)} -> {short_fingerprint(current)}), reloading...",
                flush=True,
            )
            os.execv(sys.executable, [sys.executable, *sys.argv])

    threading.Thread(target=watch, name="cpg-reload-watcher", daemon=True).start()


def main() -> None:
    _load_workspace_env_files()
    parser = argparse.ArgumentParser(description="ClawProfit Guard")
    parser.add_argument("--serve", action="store_true", help="Run HTTP server")
    parser.add_argument("--host", default="127.0.0.1", help="Server host")
    parser.add_argument("--port", type=int, default=8080, help="Server port")
    parser.add_argument(
        "--no-reload",
        action="store_true",
        help="Disable local backend auto-reload while serving",
    )
    parser.add_argument(
        "--reload-interval",
        type=float,
        default=0.75,
        help="Polling interval in seconds for local backend auto-reload",
    )
    parser.add_argument("--demo", action="store_true", help="Run local demo")
    parser.add_argument(
        "--profile-demo",
        action="store_true",
        help="Run profile recommendation demo",
    )
    parser.add_argument(
        "--preset",
        choices=sorted(PRESETS.keys()),
        default="warning",
        help="Demo preset scenario",
    )
    parser.add_argument(
        "--profile-preset",
        choices=sorted(PROFILE_PRESETS.keys()),
        default="conservative_candidate",
        help="Profile demo preset scenario",
    )
    args = parser.parse_args()

    if args.demo:
        _run_demo(args.preset)
        return

    if args.profile_demo:
        _run_profile_demo(args.profile_preset)
        return

    if args.serve:
        if not args.no_reload:
            _start_reload_watcher(max(args.reload_interval, 0.2))
        run_server(host=args.host, port=args.port)
        return

    parser.print_help()


if __name__ == "__main__":
    main()
