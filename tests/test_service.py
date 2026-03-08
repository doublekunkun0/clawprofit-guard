from __future__ import annotations

import io
import json
import unittest
from unittest.mock import patch

from src.claw_profit_guard.service import _RequestHandler


class _DummyHandler:
    def __init__(self, method: str, path: str, payload: dict | None = None) -> None:
        raw = json.dumps(payload or {}).encode("utf-8")
        self.command = method
        self.path = path
        self.headers = {"Content-Length": str(len(raw))}
        self.rfile = io.BytesIO(raw)
        self.wfile = io.BytesIO()
        self.response_code: int | None = None
        self.response_headers: list[tuple[str, str]] = []

    def send_response(self, status: int) -> None:
        self.response_code = status

    def send_header(self, key: str, value: str) -> None:
        self.response_headers.append((key, value))

    def end_headers(self) -> None:
        return

    def json_body(self) -> dict:
        return json.loads(self.wfile.getvalue().decode("utf-8"))


class ServiceHandlerTests(unittest.TestCase):
    def run_get(self, path: str) -> _DummyHandler:
        handler = _DummyHandler("GET", path)
        _RequestHandler.do_GET(handler)  # type: ignore[arg-type]
        return handler

    def run_post(self, path: str, payload: dict | None = None) -> _DummyHandler:
        handler = _DummyHandler("POST", path, payload)
        _RequestHandler.do_POST(handler)  # type: ignore[arg-type]
        return handler

    def test_health_endpoint(self) -> None:
        handler = self.run_get("/health")
        self.assertEqual(handler.response_code, 200)
        payload = handler.json_body()
        self.assertEqual(payload["status"], "ok")
        self.assertIn("server_runtime_version", payload)
        self.assertIn("workspace_version", payload)
        self.assertIn("runtime_in_sync", payload)
        self.assertIn("asset_version", payload)

    @patch("src.claw_profit_guard.service.build_symbol_catalog")
    def test_symbol_catalog_endpoint(self, mock_symbol_catalog) -> None:
        mock_symbol_catalog.return_value = [
            {"symbol": "BNBUSDT", "label": "BNB", "profiles": ["conservative", "balanced"]}
        ]
        handler = self.run_get("/v1/catalog/symbols")
        self.assertEqual(handler.response_code, 200)
        self.assertEqual(handler.json_body()["symbols"][0]["symbol"], "BNBUSDT")
        mock_symbol_catalog.assert_called_once_with()

    @patch("src.claw_profit_guard.service.get_market_snapshot")
    def test_market_snapshot_endpoint(self, mock_market_snapshot) -> None:
        mock_market_snapshot.return_value = {
            "symbol": "BNBUSDT",
            "side": "LONG",
            "profile": "balanced",
            "live": False,
            "source": "local_fallback",
            "warning": "offline",
            "market": {"last_price": 640},
            "suggested_trade": {"entry_price": 640, "stop_loss_price": 626, "take_profit_price": 668},
        }
        handler = self.run_get(
            "/v1/binance/market-snapshot?symbol=BNBUSDT&side=LONG&profile=balanced"
        )
        self.assertEqual(handler.response_code, 200)
        self.assertEqual(handler.json_body()["symbol"], "BNBUSDT")
        mock_market_snapshot.assert_called_once_with(
            "BNBUSDT",
            side="LONG",
            profile_name="balanced",
        )

    @patch("src.claw_profit_guard.service.get_account_snapshot")
    def test_account_snapshot_endpoint(self, mock_account_snapshot) -> None:
        mock_account_snapshot.return_value = {
            "symbol": "BNBUSDT",
            "profile": "balanced",
            "live": False,
            "connected": False,
            "source": "local_fallback",
            "warning": "demo",
            "account": {"estimated_equity_usdt": 2200},
            "behavior": {"trades_last_24h": 12},
            "auto_fill": {"account_equity_usdt": 2200},
            "agent_context": {"behavior_status": "elevated"},
            "briefing": ["demo"],
        }
        handler = self.run_get(
            "/v1/binance/account-snapshot?symbol=BNBUSDT&profile=balanced"
        )
        self.assertEqual(handler.response_code, 200)
        self.assertEqual(handler.json_body()["symbol"], "BNBUSDT")
        mock_account_snapshot.assert_called_once_with(
            "BNBUSDT",
            profile_name="balanced",
        )

    @patch("src.claw_profit_guard.service.demo_order_test")
    def test_demo_order_test_endpoint(self, mock_demo_order_test) -> None:
        mock_demo_order_test.return_value = {
            "ok": False,
            "status": "not_configured",
            "mode": "preview_only",
            "message": "preview only",
            "preview": {"symbol": "BNBUSDT"},
            "credentials": {"configured": False},
        }
        handler = self.run_post(
            "/v1/binance/demo-order-test",
            {
                "trade": {
                    "symbol": "BNBUSDT",
                    "side": "LONG",
                    "entry_price": 640,
                    "position_notional_usdt": 640,
                }
            },
        )
        self.assertEqual(handler.response_code, 200)
        self.assertEqual(handler.json_body()["status"], "not_configured")
        mock_demo_order_test.assert_called_once()

    @patch("src.claw_profit_guard.service.live_order_place_and_cancel")
    def test_live_order_endpoint(self, mock_live_order_place_and_cancel) -> None:
        mock_live_order_place_and_cancel.return_value = {
            "ok": True,
            "status": "placed_then_canceled",
            "mode": "binance_spot_live",
            "message": "placed and canceled",
            "preview": {"symbol": "BNBUSDT"},
            "credentials": {"configured": True},
        }
        handler = self.run_post(
            "/v1/binance/live-order",
            {
                "confirm_live_execution": True,
                "trade": {
                    "symbol": "BNBUSDT",
                    "side": "LONG",
                    "entry_price": 640,
                    "position_notional_usdt": 640,
                },
            },
        )
        self.assertEqual(handler.response_code, 200)
        self.assertEqual(handler.json_body()["status"], "placed_then_canceled")
        mock_live_order_place_and_cancel.assert_called_once_with(
            {
                "symbol": "BNBUSDT",
                "side": "LONG",
                "entry_price": 640,
                "position_notional_usdt": 640,
            },
            confirm_live_execution=True,
        )

    @patch("src.claw_profit_guard.service.live_order_open_position")
    def test_live_open_order_endpoint(self, mock_live_order_open_position) -> None:
        mock_live_order_open_position.return_value = {
            "ok": True,
            "status": "opened",
            "mode": "binance_futures_live",
            "message": "opened",
            "preview": {"symbol": "BNBUSDT", "type": "MARKET"},
            "credentials": {"configured": True},
        }
        handler = self.run_post(
            "/v1/binance/live-open-order",
            {
                "confirm_live_execution": True,
                "trade": {
                    "symbol": "BNBUSDT",
                    "side": "LONG",
                    "entry_price": 640,
                    "position_notional_usdt": 8.4,
                },
            },
        )
        self.assertEqual(handler.response_code, 200)
        self.assertEqual(handler.json_body()["status"], "opened")
        mock_live_order_open_position.assert_called_once_with(
            {
                "symbol": "BNBUSDT",
                "side": "LONG",
                "entry_price": 640,
                "position_notional_usdt": 8.4,
            },
            confirm_live_execution=True,
        )

    @patch("src.claw_profit_guard.service.cancel_current_symbol_orders")
    def test_cancel_current_orders_endpoint(self, mock_cancel_current_symbol_orders) -> None:
        mock_cancel_current_symbol_orders.return_value = {
            "ok": True,
            "status": "canceled",
            "mode": "binance_futures_live",
            "message": "canceled",
            "symbol": "BNBUSDT",
        }
        handler = self.run_post(
            "/v1/binance/cancel-current-orders",
            {"symbol": "BNBUSDT"},
        )
        self.assertEqual(handler.response_code, 200)
        self.assertEqual(handler.json_body()["status"], "canceled")
        mock_cancel_current_symbol_orders.assert_called_once_with("BNBUSDT")

    @patch("src.claw_profit_guard.service.close_current_symbol_position")
    def test_close_current_position_endpoint(self, mock_close_current_symbol_position) -> None:
        mock_close_current_symbol_position.return_value = {
            "ok": True,
            "status": "closed",
            "mode": "binance_futures_live",
            "message": "closed",
            "symbol": "BNBUSDT",
        }
        handler = self.run_post(
            "/v1/binance/close-current-position",
            {"symbol": "BNBUSDT"},
        )
        self.assertEqual(handler.response_code, 200)
        self.assertEqual(handler.json_body()["status"], "closed")
        mock_close_current_symbol_position.assert_called_once_with("BNBUSDT")

    def test_demo_order_test_requires_trade_object(self) -> None:
        handler = self.run_post("/v1/binance/demo-order-test", {})
        self.assertEqual(handler.response_code, 400)
        self.assertIn("trade object is required", handler.json_body()["error"])


if __name__ == "__main__":
    unittest.main()
