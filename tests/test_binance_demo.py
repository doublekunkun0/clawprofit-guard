from __future__ import annotations

import json
import unittest
from unittest.mock import patch

from src.claw_profit_guard import binance_demo


class _FakeResponse:
    def __init__(self, payload: dict) -> None:
        self._payload = payload

    def read(self) -> bytes:
        return json.dumps(self._payload).encode("utf-8")

    def __enter__(self) -> "_FakeResponse":
        return self

    def __exit__(self, exc_type, exc, tb) -> bool:
        return False


class BinanceDemoTests(unittest.TestCase):
    def setUp(self) -> None:
        binance_demo.SYMBOL_TRADING_RULES_CACHE.clear()

    def test_build_market_snapshot_for_long_trade(self) -> None:
        with patch.dict("os.environ", {"BINANCE_FUTURES_ENV": "demo"}, clear=False):
            snapshot = binance_demo.build_market_snapshot(
                symbol="BNBUSDT",
                side="LONG",
                profile_name="balanced",
                ticker_24h={
                    "lastPrice": "640.5",
                    "weightedAvgPrice": "638.1",
                    "bidPrice": "640.0",
                    "askPrice": "641.0",
                    "priceChangePercent": "4.2",
                },
                depth_payload={
                    "bids": [["640.0", "25"], ["639.8", "12"]],
                    "asks": [["641.0", "24"], ["641.2", "16"]],
                },
                klines_payload=[
                    [0, "630", "643", "628", "632"],
                    [0, "632", "645", "631", "638"],
                    [0, "638", "644", "636", "641"],
                ],
                live=True,
            )
        self.assertTrue(snapshot["live"])
        self.assertEqual(snapshot["source"], "binance_futures_demo")
        self.assertGreater(snapshot["market"]["volatility_24h_pct"], 0.0)
        self.assertGreater(snapshot["suggested_trade"]["take_profit_price"], snapshot["suggested_trade"]["entry_price"])
        self.assertLess(snapshot["suggested_trade"]["stop_loss_price"], snapshot["suggested_trade"]["entry_price"])
        self.assertEqual(
            [item["symbol"] for item in snapshot["benchmarks"]],
            ["BTCUSDT", "BNBUSDT", "ETHUSDT"],
        )
        self.assertEqual(snapshot["chart"]["interval"], "5m")
        self.assertEqual(len(snapshot["chart"]["candles"]), 3)
        self.assertIn("close", snapshot["chart"]["candles"][0])

    @patch("src.claw_profit_guard.binance_demo._http_json", side_effect=RuntimeError("offline"))
    def test_get_market_snapshot_falls_back(self, _mock_http_json) -> None:
        snapshot = binance_demo.get_market_snapshot("ETHUSDT", side="SHORT", profile_name="aggressive")
        self.assertFalse(snapshot["live"])
        self.assertEqual(snapshot["source"], "local_fallback")
        self.assertEqual(snapshot["symbol"], "ETHUSDT")
        self.assertEqual(snapshot["side"], "SHORT")
        self.assertEqual(snapshot["warning"], "offline")
        self.assertEqual(
            [item["symbol"] for item in snapshot["benchmarks"]],
            ["BTCUSDT", "BNBUSDT", "ETHUSDT"],
        )

    def test_build_demo_order_preview_uses_limit_order_shape(self) -> None:
        with patch.dict("os.environ", {"BINANCE_FUTURES_ENV": "demo"}, clear=False):
            preview = binance_demo.build_demo_order_preview(
                {
                    "symbol": "BTCUSDT",
                    "side": "LONG",
                    "entry_price": 91000,
                    "position_notional_usdt": 1820,
                }
            )
        self.assertEqual(preview["symbol"], "BTCUSDT")
        self.assertEqual(preview["intent_side"], "LONG")
        self.assertEqual(preview["side"], "BUY")
        self.assertEqual(preview["order_side"], "BUY")
        self.assertEqual(preview["type"], "LIMIT")
        self.assertEqual(preview["timeInForce"], "GTC")
        self.assertEqual(preview["price"], "91000.00")
        self.assertEqual(preview["quantity"], "0.02000")
        self.assertEqual(preview["execution_mode"], "binance_futures_demo")
        self.assertEqual(preview["validation_scope"], "full")

    def test_build_demo_order_preview_supports_short_for_futures(self) -> None:
        preview = binance_demo.build_demo_order_preview(
            {
                "symbol": "ETHUSDT",
                "side": "SHORT",
                "entry_price": 4700,
                "position_notional_usdt": 940,
            }
        )
        self.assertEqual(preview["intent_side"], "SHORT")
        self.assertEqual(preview["side"], "SELL")
        self.assertEqual(preview["validation_scope"], "full")

    @patch("src.claw_profit_guard.binance_demo._http_json")
    def test_build_demo_order_preview_aligns_quantity_to_lot_size(self, mock_http_json) -> None:
        mock_http_json.return_value = {
            "symbols": [
                {
                    "symbol": "BTCUSDT",
                    "pricePrecision": 2,
                    "quantityPrecision": 3,
                    "filters": [
                        {
                            "filterType": "PRICE_FILTER",
                            "minPrice": "556.80",
                            "maxPrice": "4529764",
                            "tickSize": "0.10",
                        },
                        {
                            "filterType": "LOT_SIZE",
                            "minQty": "0.001",
                            "maxQty": "1000",
                            "stepSize": "0.001",
                        },
                        {
                            "filterType": "MIN_NOTIONAL",
                            "notional": "100",
                        },
                    ],
                },
                {
                    "symbol": "BNBUSDT",
                    "pricePrecision": 3,
                    "quantityPrecision": 2,
                    "filters": [
                        {
                            "filterType": "PRICE_FILTER",
                            "minPrice": "6.60000000",
                            "maxPrice": "1000000.00000000",
                            "tickSize": "0.01000000",
                        },
                        {
                            "filterType": "LOT_SIZE",
                            "minQty": "0.01000000",
                            "maxQty": "100000.00000000",
                            "stepSize": "0.01000000",
                        },
                        {
                            "filterType": "MIN_NOTIONAL",
                            "minNotional": "5.00000000",
                        },
                    ],
                },
            ]
        }
        preview = binance_demo.build_demo_order_preview(
            {
                "symbol": "BNBUSDT",
                "side": "LONG",
                "entry_price": 624.58,
                "position_notional_usdt": 120.0,
            }
        )
        self.assertEqual(preview["quantity"], "0.19")
        self.assertEqual(preview["price"], "624.58")
        self.assertEqual(preview["exchange_rules"]["step_size"], "0.01000000")
        self.assertEqual(preview["exchange_rules"]["price_precision"], "3")
        self.assertEqual(preview["exchange_rules"]["quantity_precision"], "2")
        self.assertEqual(
            preview["exchange_minimums"]["minimum_executable_notional_usdt"], "6.24"
        )

    def test_build_account_snapshot_contains_auto_fill_and_briefing(self) -> None:
        snapshot = binance_demo.build_account_snapshot(
            symbol="BNBUSDT",
            profile_name="balanced",
            account_payload={
                "balances": [
                    {"asset": "USDT", "free": "1000", "locked": "100"},
                    {"asset": "BNB", "free": "2", "locked": "0"},
                ]
            },
            open_orders_payload=[
                {
                    "symbol": "BNBUSDT",
                    "side": "SELL",
                    "positionSide": "LONG",
                    "type": "LIMIT",
                    "status": "NEW",
                    "price": "660",
                    "stopPrice": "0",
                    "origQty": "0.10",
                    "executedQty": "0",
                    "workingType": "CONTRACT_PRICE",
                    "time": 123,
                }
            ],
            algo_open_orders_payload=[
                {
                    "symbol": "BNBUSDT",
                    "side": "SELL",
                    "positionSide": "LONG",
                    "type": "STOP_MARKET",
                    "algoStatus": "NEW",
                    "triggerPrice": "615.10",
                    "quantity": "0.03",
                    "workingType": "CONTRACT_PRICE",
                    "algoId": "algo-1",
                    "createdTime": 124,
                }
            ],
            trades_by_symbol={
                "BNBUSDT": [
                    {
                        "price": "600",
                        "qty": "1",
                        "commission": "0",
                        "isBuyer": True,
                        "time": 1,
                    },
                    {
                        "price": "590",
                        "qty": "1",
                        "commission": "0",
                        "isBuyer": False,
                        "time": 2,
                    },
                ]
            },
            price_map={"BNBUSDT": 640.0},
            live=True,
        )
        self.assertTrue(snapshot["live"])
        self.assertEqual(snapshot["account"]["open_orders_count"], 1)
        self.assertEqual(snapshot["account"]["open_orders"][0]["type"], "LIMIT")
        self.assertEqual(snapshot["account"]["open_orders"][0]["position_side"], "LONG")
        self.assertEqual(snapshot["account"]["algo_open_orders_count"], 1)
        self.assertEqual(snapshot["account"]["algo_open_orders"][0]["type"], "STOP_MARKET")
        self.assertEqual(snapshot["account"]["wallet_balance_usdt"], 1100.0)
        self.assertEqual(snapshot["auto_fill"]["account_equity_usdt"], 1100.0)
        self.assertEqual(snapshot["behavior"]["consecutive_losses"], 1)
        self.assertTrue(snapshot["briefing"])

    @patch.dict("os.environ", {}, clear=False)
    def test_demo_order_test_without_credentials_is_preview_only(self) -> None:
        with patch.dict(
            "os.environ",
            {
                "BINANCE_API_KEY": "",
                "BINANCE_SECRET_KEY": "",
                "BINANCE_DEMO_API_KEY": "",
                "BINANCE_DEMO_SECRET_KEY": "",
                "BINANCE_FUTURES_ENV": "live",
            },
            clear=False,
        ):
            result = binance_demo.demo_order_test(
                {
                    "symbol": "BNBUSDT",
                    "side": "LONG",
                    "entry_price": 640,
                    "position_notional_usdt": 640,
                }
            )
        self.assertFalse(result["ok"])
        self.assertEqual(result["status"], "not_configured")
        self.assertEqual(result["mode"], "preview_only")
        self.assertEqual(result["preview"]["side"], "BUY")
        self.assertEqual(result["credentials"]["api_key_env"], "BINANCE_API_KEY")
        self.assertIn("preview", result)

    @patch("src.claw_profit_guard.binance_demo._futures_dual_side_position", return_value=True)
    @patch("src.claw_profit_guard.binance_demo._get_symbol_trading_rules", return_value={})
    @patch("src.claw_profit_guard.binance_demo.urlopen", return_value=_FakeResponse({}))
    def test_demo_order_test_short_validates_with_mocked_exchange(
        self, _mock_urlopen, _mock_get_symbol_trading_rules, _mock_position_mode
    ) -> None:
        with patch.dict(
            "os.environ",
            {
                "BINANCE_API_KEY": "live-key",
                "BINANCE_SECRET_KEY": "live-secret",
                "BINANCE_FUTURES_ENV": "live",
            },
            clear=False,
        ):
            result = binance_demo.demo_order_test(
                {
                    "symbol": "BNBUSDT",
                    "side": "SHORT",
                    "entry_price": 640,
                    "position_notional_usdt": 640,
                }
            )
        self.assertTrue(result["ok"])
        self.assertEqual(result["status"], "validated")
        self.assertEqual(result["mode"], "binance_futures_live")
        self.assertEqual(result["preview"]["side"], "SELL")
        self.assertEqual(result["preview"]["positionSide"], "SHORT")

    @patch("src.claw_profit_guard.binance_demo._futures_dual_side_position", return_value=False)
    @patch("src.claw_profit_guard.binance_demo.urlopen", return_value=_FakeResponse({}))
    def test_demo_order_test_validates_with_mocked_exchange(self, _mock_urlopen, _mock_position_mode) -> None:
        with patch.dict(
            "os.environ",
            {
                "BINANCE_API_KEY": "live-key",
                "BINANCE_SECRET_KEY": "live-secret",
                "BINANCE_FUTURES_ENV": "live",
            },
            clear=False,
        ):
            result = binance_demo.demo_order_test(
                {
                    "symbol": "BNBUSDT",
                    "side": "LONG",
                    "entry_price": 640,
                    "position_notional_usdt": 640,
                }
        )
        self.assertTrue(result["ok"])
        self.assertEqual(result["status"], "validated")
        self.assertEqual(result["mode"], "binance_futures_live")
        self.assertEqual(result["preview"]["side"], "BUY")

    def test_live_order_requires_confirmation(self) -> None:
        result = binance_demo.live_order_place_and_cancel(
            {
                "symbol": "BNBUSDT",
                "side": "LONG",
                "entry_price": 640,
                "position_notional_usdt": 20,
            }
        )
        self.assertFalse(result["ok"])
        self.assertEqual(result["status"], "confirmation_required")

    def test_live_open_order_requires_confirmation(self) -> None:
        result = binance_demo.live_order_open_position(
            {
                "symbol": "BNBUSDT",
                "side": "LONG",
                "entry_price": 640,
                "stop_loss_price": 626,
                "take_profit_price": 668,
                "leverage": 9,
                "position_notional_usdt": 20,
            }
        )
        self.assertFalse(result["ok"])
        self.assertEqual(result["status"], "confirmation_required")

    def test_live_open_order_requires_stop_loss_and_take_profit(self) -> None:
        result = binance_demo.live_order_open_position(
            {
                "symbol": "BNBUSDT",
                "side": "LONG",
                "entry_price": 640,
                "leverage": 9,
                "position_notional_usdt": 20,
            },
            confirm_live_execution=True,
        )
        self.assertFalse(result["ok"])
        self.assertEqual(result["status"], "preview_invalid")
        self.assertIn("stop_loss_price", result["message"])

    def test_live_open_order_rejects_non_integer_leverage(self) -> None:
        with patch.dict(
            "os.environ",
            {
                "BINANCE_API_KEY": "live-key",
                "BINANCE_SECRET_KEY": "live-secret",
                "BINANCE_FUTURES_ENV": "live",
            },
            clear=False,
        ):
            result = binance_demo.live_order_open_position(
                {
                    "symbol": "BNBUSDT",
                    "side": "LONG",
                    "entry_price": 624.00,
                    "stop_loss_price": 616.71,
                    "take_profit_price": 636.79,
                    "leverage": 8.5,
                    "position_notional_usdt": 8.4,
                },
                confirm_live_execution=True,
            )
        self.assertFalse(result["ok"])
        self.assertEqual(result["status"], "preview_invalid")
        self.assertIn("whole number", result["message"])

    @patch("src.claw_profit_guard.binance_demo._http_json")
    def test_build_live_open_order_preview_uses_nearest_executable_quantity(self, mock_http_json) -> None:
        def fake_http_json(path: str, **kwargs):
            if path == "/fapi/v1/exchangeInfo":
                return {
                    "symbols": [
                        {
                            "symbol": "BNBUSDT",
                            "pricePrecision": 2,
                            "quantityPrecision": 2,
                            "filters": [
                                {"filterType": "PRICE_FILTER", "minPrice": "0.01", "maxPrice": "100000", "tickSize": "0.01"},
                                {"filterType": "LOT_SIZE", "minQty": "0.01", "maxQty": "100000", "stepSize": "0.01"},
                                {"filterType": "MIN_NOTIONAL", "notional": "5"},
                            ],
                        }
                    ]
                }
            if path == "/fapi/v1/ticker/bookTicker":
                return {"bidPrice": "620.30", "askPrice": "620.40"}
            raise AssertionError(f"Unexpected path: {path}")

        mock_http_json.side_effect = fake_http_json
        preview = binance_demo.build_live_open_order_preview(
            {
                "symbol": "BNBUSDT",
                "side": "LONG",
                "entry_price": 620.40,
                "leverage": 3,
                "margin_mode": "CROSSED",
                "position_notional_usdt": 24.21,
            }
        )
        self.assertEqual(preview["quantity"], "0.04")
        self.assertEqual(preview["estimated_execution_notional_usdt"], "24.81")
        self.assertEqual(preview["required_initial_margin_usdt"], "8.27")

    @patch("src.claw_profit_guard.binance_demo._futures_dual_side_position", return_value=False)
    @patch("src.claw_profit_guard.binance_demo._signed_json")
    @patch("src.claw_profit_guard.binance_demo._http_json")
    def test_live_order_places_and_cancels_with_mocked_exchange(
        self, mock_http_json, mock_signed_json, _mock_position_mode
    ) -> None:
        def fake_http_json(path: str, **kwargs):
            if path == "/fapi/v1/exchangeInfo":
                return {
                    "symbols": [
                        {
                            "symbol": "BNBUSDT",
                            "pricePrecision": 3,
                            "quantityPrecision": 3,
                            "filters": [
                                {
                                    "filterType": "PRICE_FILTER",
                                    "minPrice": "0.01000000",
                                    "maxPrice": "1000000.00000000",
                                    "tickSize": "0.01000000",
                                },
                                {
                                    "filterType": "LOT_SIZE",
                                    "minQty": "0.00100000",
                                    "maxQty": "100000.00000000",
                                    "stepSize": "0.00100000",
                                },
                                {
                                    "filterType": "MIN_NOTIONAL",
                                    "notional": "5.00000000",
                                },
                            ]
                        }
                    ]
                }
            if path == "/fapi/v1/ticker/bookTicker":
                return {"bidPrice": "624.74", "askPrice": "624.75"}
            raise AssertionError(f"Unexpected path: {path}")

        def fake_signed_json(path: str, **kwargs):
            if path == "/fapi/v2/positionRisk":
                return [{"symbol": "BNBUSDT", "marginType": "ISOLATED"}]
            if path == "/fapi/v1/order" and kwargs.get("method") == "POST":
                return {"symbol": "BNBUSDT", "orderId": 123456, "status": "NEW"}
            if path == "/fapi/v1/order" and kwargs.get("method") == "DELETE":
                return {"symbol": "BNBUSDT", "orderId": 123456, "status": "CANCELED"}
            if path == "/fapi/v1/marginType" and kwargs.get("method") == "POST":
                return {"code": 200, "msg": "success", "symbol": "BNBUSDT", "marginType": "CROSSED"}
            if path == "/fapi/v1/leverage" and kwargs.get("method") == "POST":
                return {"symbol": "BNBUSDT", "leverage": 9, "maxNotionalValue": "1000000"}
            raise AssertionError(f"Unexpected signed path: {path} / {kwargs.get('method')}")

        mock_http_json.side_effect = fake_http_json
        mock_signed_json.side_effect = fake_signed_json
        with patch.dict(
            "os.environ",
            {
                "BINANCE_API_KEY": "live-key",
                "BINANCE_SECRET_KEY": "live-secret",
                "BINANCE_FUTURES_ENV": "live",
            },
            clear=False,
        ):
            result = binance_demo.live_order_place_and_cancel(
                {
                    "symbol": "BNBUSDT",
                    "side": "LONG",
                    "entry_price": 624.80,
                    "leverage": 9,
                    "margin_mode": "CROSSED",
                    "position_notional_usdt": 28,
                },
                confirm_live_execution=True,
            )
        self.assertTrue(result["ok"])
        self.assertEqual(result["status"], "placed_then_canceled")
        self.assertEqual(result["preview"]["type"], "LIMIT")
        self.assertEqual(result["preview"]["requested_margin_type"], "CROSSED")
        self.assertEqual(result["preview"]["requested_leverage"], "9")
        self.assertEqual(result["preview"]["quantity"], "0.009")
        self.assertEqual(result["preview"]["price"], "624.72")
        self.assertEqual(result["preview"]["timeInForce"], "GTX")
        self.assertEqual(result["margin_sync"]["marginType"], "CROSSED")
        self.assertEqual(result["leverage_sync"]["leverage"], 9)
        self.assertEqual(result["cancel"]["status"], "CANCELED")

    @patch("src.claw_profit_guard.binance_demo._futures_dual_side_position", return_value=False)
    @patch("src.claw_profit_guard.binance_demo._signed_json")
    @patch("src.claw_profit_guard.binance_demo._http_json")
    def test_live_order_treats_unknown_order_cancel_as_already_gone(
        self, mock_http_json, mock_signed_json, _mock_position_mode
    ) -> None:
        def fake_http_json(path: str, **kwargs):
            if path == "/fapi/v1/exchangeInfo":
                return {
                    "symbols": [
                        {
                            "symbol": "BNBUSDT",
                            "pricePrecision": 3,
                            "quantityPrecision": 3,
                            "filters": [
                                {
                                    "filterType": "PRICE_FILTER",
                                    "minPrice": "0.01000000",
                                    "maxPrice": "1000000.00000000",
                                    "tickSize": "0.01000000",
                                },
                                {
                                    "filterType": "LOT_SIZE",
                                    "minQty": "0.00100000",
                                    "maxQty": "100000.00000000",
                                    "stepSize": "0.00100000",
                                },
                                {
                                    "filterType": "MIN_NOTIONAL",
                                    "notional": "5.00000000",
                                },
                            ],
                        }
                    ]
                }
            if path == "/fapi/v1/ticker/bookTicker":
                return {"bidPrice": "624.74", "askPrice": "624.75"}
            raise AssertionError(f"Unexpected path: {path}")

        def fake_signed_json(path: str, **kwargs):
            if path == "/fapi/v2/positionRisk":
                return [{"symbol": "BNBUSDT", "marginType": "ISOLATED"}]
            if path == "/fapi/v1/order" and kwargs.get("method") == "POST":
                return {"symbol": "BNBUSDT", "orderId": 999001, "status": "NEW"}
            if path == "/fapi/v1/order" and kwargs.get("method") == "DELETE":
                raise RuntimeError("Binance USD-M Futures API HTTP 400: Unknown order sent.")
            if path == "/fapi/v1/marginType" and kwargs.get("method") == "POST":
                return {"code": 200, "msg": "success", "symbol": "BNBUSDT", "marginType": "CROSSED"}
            if path == "/fapi/v1/leverage" and kwargs.get("method") == "POST":
                return {"symbol": "BNBUSDT", "leverage": 9, "maxNotionalValue": "1000000"}
            raise AssertionError(f"Unexpected signed path: {path} / {kwargs.get('method')}")

        mock_http_json.side_effect = fake_http_json
        mock_signed_json.side_effect = fake_signed_json
        with patch.dict(
            "os.environ",
            {
                "BINANCE_API_KEY": "live-key",
                "BINANCE_SECRET_KEY": "live-secret",
                "BINANCE_FUTURES_ENV": "live",
            },
            clear=False,
        ):
            result = binance_demo.live_order_place_and_cancel(
                {
                    "symbol": "BNBUSDT",
                    "side": "LONG",
                    "entry_price": 624.80,
                    "leverage": 9,
                    "margin_mode": "CROSSED",
                    "position_notional_usdt": 28,
                },
                confirm_live_execution=True,
            )

        self.assertTrue(result["ok"])
        self.assertEqual(result["status"], "placed_then_canceled")
        self.assertEqual(result["cancel"]["status"], "ALREADY_GONE")

    @patch("src.claw_profit_guard.binance_demo._futures_dual_side_position", return_value=True)
    @patch("src.claw_profit_guard.binance_demo._signed_json")
    @patch("src.claw_profit_guard.binance_demo._http_json")
    def test_live_open_order_keeps_position_with_mocked_exchange(
        self, mock_http_json, mock_signed_json, _mock_position_mode
    ) -> None:
        def fake_http_json(path: str, **kwargs):
            if path == "/fapi/v1/exchangeInfo":
                return {
                    "symbols": [
                        {
                            "symbol": "BNBUSDT",
                            "pricePrecision": 3,
                            "quantityPrecision": 2,
                            "filters": [
                                {
                                    "filterType": "PRICE_FILTER",
                                    "minPrice": "6.600",
                                    "maxPrice": "100000",
                                    "tickSize": "0.010",
                                },
                                {
                                    "filterType": "LOT_SIZE",
                                    "minQty": "0.01",
                                    "maxQty": "100000",
                                    "stepSize": "0.01",
                                },
                                {
                                    "filterType": "MIN_NOTIONAL",
                                    "notional": "5",
                                },
                            ],
                        }
                    ]
                }
            if path == "/fapi/v1/ticker/bookTicker":
                return {"bidPrice": "624.00", "askPrice": "624.05"}
            raise AssertionError(f"Unexpected path: {path}")

        def fake_signed_json(path: str, **kwargs):
            if path == "/fapi/v2/positionRisk":
                return [{"symbol": "BNBUSDT", "marginType": "CROSSED"}]
            if path == "/fapi/v3/account":
                return {"availableBalance": "50"}
            if path == "/fapi/v1/marginType" and kwargs.get("method") == "POST":
                return {"code": 200, "msg": "success", "symbol": "BNBUSDT", "marginType": "ISOLATED"}
            if path == "/fapi/v1/order/test" and kwargs.get("method") == "POST":
                return {}
            if path == "/fapi/v1/leverage" and kwargs.get("method") == "POST":
                return {"symbol": "BNBUSDT", "leverage": 9, "maxNotionalValue": "1000000"}
            if path == "/fapi/v1/algoOrder" and kwargs.get("method") == "POST":
                params = kwargs.get("params") or {}
                order_type = params.get("type")
                if order_type == "STOP_MARKET":
                    return {
                        "symbol": "BNBUSDT",
                        "algoId": 888889,
                        "algoStatus": "NEW",
                        "type": "STOP_MARKET",
                        "side": "SELL",
                        "triggerPrice": params.get("triggerPrice"),
                    }
                if order_type == "TAKE_PROFIT_MARKET":
                    return {
                        "symbol": "BNBUSDT",
                        "algoId": 888890,
                        "algoStatus": "NEW",
                        "type": "TAKE_PROFIT_MARKET",
                        "side": "SELL",
                        "triggerPrice": params.get("triggerPrice"),
                    }
            if path == "/fapi/v1/order" and kwargs.get("method") == "POST":
                return {
                    "symbol": "BNBUSDT",
                    "orderId": 888888,
                    "status": "FILLED",
                    "type": "MARKET",
                    "executedQty": "0.01",
                    "avgPrice": "624.05",
                }
            raise AssertionError(f"Unexpected signed path: {path} / {kwargs.get('method')}")

        mock_http_json.side_effect = fake_http_json
        mock_signed_json.side_effect = fake_signed_json
        with patch.dict(
            "os.environ",
            {
                "BINANCE_API_KEY": "live-key",
                "BINANCE_SECRET_KEY": "live-secret",
                "BINANCE_FUTURES_ENV": "live",
            },
            clear=False,
        ):
            result = binance_demo.live_order_open_position(
                {
                    "symbol": "BNBUSDT",
                    "side": "LONG",
                    "entry_price": 624.00,
                    "stop_loss_price": 616.71,
                    "take_profit_price": 636.79,
                    "leverage": 9,
                    "margin_mode": "ISOLATED",
                    "position_notional_usdt": 8.4,
                },
                confirm_live_execution=True,
            )
        self.assertTrue(result["ok"])
        self.assertEqual(result["status"], "opened")
        self.assertEqual(result["preview"]["type"], "MARKET")
        self.assertEqual(result["preview"]["requested_margin_type"], "ISOLATED")
        self.assertEqual(result["preview"]["requested_leverage"], "9")
        self.assertEqual(result["preview"]["quantity"], "0.01")
        self.assertEqual(result["preview"]["positionSide"], "LONG")
        self.assertEqual(result["preview"]["required_initial_margin_usdt"], "0.69")
        self.assertEqual(result["margin_sync"]["marginType"], "ISOLATED")
        self.assertEqual(result["leverage_sync"]["leverage"], 9)
        self.assertEqual(result["execution"]["status"], "FILLED")
        self.assertEqual(result["execution_summary"]["requested_notional_usdt"], "8.40")
        self.assertEqual(result["execution_summary"]["actual_execution_notional_usdt"], "6.24")
        self.assertEqual(result["execution_summary"]["execution_notional_delta_usdt"], "-2.16")
        self.assertEqual(result["execution_summary"]["execution_notional_delta_pct"], "-25.71")
        self.assertEqual(result["protection_orders"]["stop_loss"]["type"], "STOP_MARKET")
        self.assertEqual(result["protection_orders"]["stop_loss"]["triggerPrice"], "616.71")
        self.assertEqual(result["protection_orders"]["take_profit"]["type"], "TAKE_PROFIT_MARKET")
        self.assertEqual(result["protection_orders"]["take_profit"]["triggerPrice"], "636.79")
        self.assertEqual(
            [call.args[0] for call in mock_signed_json.call_args_list],
            [
                "/fapi/v2/positionRisk",
                "/fapi/v1/marginType",
                "/fapi/v1/leverage",
                "/fapi/v3/account",
                "/fapi/v1/order/test",
                "/fapi/v1/order",
                "/fapi/v1/algoOrder",
                "/fapi/v1/algoOrder",
            ],
        )

    @patch("src.claw_profit_guard.binance_demo._futures_dual_side_position", return_value=True)
    @patch("src.claw_profit_guard.binance_demo._signed_json")
    @patch("src.claw_profit_guard.binance_demo._http_json")
    def test_live_open_order_rejects_when_available_balance_is_insufficient(
        self, mock_http_json, mock_signed_json, _mock_position_mode
    ) -> None:
        def fake_http_json(path: str, **kwargs):
            if path == "/fapi/v1/exchangeInfo":
                return {
                    "symbols": [
                        {
                            "symbol": "BNBUSDT",
                            "pricePrecision": 3,
                            "quantityPrecision": 2,
                            "filters": [
                                {"filterType": "PRICE_FILTER", "minPrice": "6.600", "maxPrice": "100000", "tickSize": "0.010"},
                                {"filterType": "LOT_SIZE", "minQty": "0.01", "maxQty": "100000", "stepSize": "0.01"},
                                {"filterType": "MIN_NOTIONAL", "notional": "5"},
                            ],
                        }
                    ]
                }
            if path == "/fapi/v1/ticker/bookTicker":
                return {"bidPrice": "624.00", "askPrice": "624.05"}
            raise AssertionError(f"Unexpected path: {path}")

        def fake_signed_json(path: str, **kwargs):
            if path == "/fapi/v2/positionRisk":
                return [{"symbol": "BNBUSDT", "marginType": "CROSSED"}]
            if path == "/fapi/v1/marginType" and kwargs.get("method") == "POST":
                return {"code": 200, "msg": "success", "symbol": "BNBUSDT", "marginType": "ISOLATED"}
            if path == "/fapi/v1/leverage" and kwargs.get("method") == "POST":
                return {"symbol": "BNBUSDT", "leverage": 9, "maxNotionalValue": "1000000"}
            if path == "/fapi/v3/account":
                return {"availableBalance": "0.40"}
            raise AssertionError(f"Unexpected signed path: {path} / {kwargs.get('method')}")

        mock_http_json.side_effect = fake_http_json
        mock_signed_json.side_effect = fake_signed_json
        with patch.dict(
            "os.environ",
            {
                "BINANCE_API_KEY": "live-key",
                "BINANCE_SECRET_KEY": "live-secret",
                "BINANCE_FUTURES_ENV": "live",
            },
            clear=False,
        ):
            result = binance_demo.live_order_open_position(
                {
                    "symbol": "BNBUSDT",
                    "side": "LONG",
                    "entry_price": 624.00,
                    "stop_loss_price": 616.71,
                    "take_profit_price": 636.79,
                    "leverage": 9,
                    "margin_mode": "ISOLATED",
                    "position_notional_usdt": 8.4,
                },
                confirm_live_execution=True,
            )
        self.assertFalse(result["ok"])
        self.assertEqual(result["status"], "exchange_rejected")
        self.assertIn("Insufficient available USDT", result["message"])
        self.assertEqual(result["available_balance_usdt"], "0.40")

    @patch("src.claw_profit_guard.binance_demo._signed_json")
    def test_sync_futures_margin_type_skips_post_when_requested_mode_matches(
        self, mock_signed_json
    ) -> None:
        def fake_signed_json(path: str, **kwargs):
            if path == "/fapi/v2/positionRisk":
                return [{"symbol": "BNBUSDT", "marginType": "ISOLATED"}]
            if path == "/fapi/v1/marginType":
                raise AssertionError("marginType POST should be skipped when the current mode already matches")
            raise AssertionError(f"Unexpected signed path: {path}")

        mock_signed_json.side_effect = fake_signed_json
        result = binance_demo._sync_futures_margin_type(
            symbol="BNBUSDT",
            margin_type="ISOLATED",
            api_key="live-key",
            secret_key="live-secret",
        )
        self.assertEqual(result["symbol"], "BNBUSDT")
        self.assertEqual(result["marginType"], "ISOLATED")
        self.assertEqual(result["status"], "matched")

    @patch("src.claw_profit_guard.binance_demo._signed_json")
    def test_cancel_current_symbol_orders_cancels_open_and_algo_orders(
        self, mock_signed_json
    ) -> None:
        def fake_signed_json(path: str, **kwargs):
            method = kwargs.get("method", "GET")
            params = kwargs.get("params") or {}
            if path == "/fapi/v1/openOrders" and method == "GET":
                self.assertEqual(params.get("symbol"), "BNBUSDT")
                return [{"symbol": "BNBUSDT", "orderId": 1}]
            if path == "/fapi/v1/openAlgoOrders" and method == "GET":
                self.assertEqual(params.get("symbol"), "BNBUSDT")
                return [{"symbol": "BNBUSDT", "algoId": 2}]
            if path == "/fapi/v1/allOpenOrders" and method == "DELETE":
                return {"code": 200, "msg": "done"}
            if path == "/fapi/v1/algoOpenOrders" and method == "DELETE":
                return {"code": 200, "msg": "done"}
            raise AssertionError(f"Unexpected signed path: {path} / {method}")

        mock_signed_json.side_effect = fake_signed_json
        with patch.dict(
            "os.environ",
            {
                "BINANCE_API_KEY": "live-key",
                "BINANCE_SECRET_KEY": "live-secret",
                "BINANCE_FUTURES_ENV": "live",
            },
            clear=False,
        ):
            result = binance_demo.cancel_current_symbol_orders("BNBUSDT")
        self.assertTrue(result["ok"])
        self.assertEqual(result["status"], "canceled")
        self.assertEqual(result["canceled_open_orders"], 1)
        self.assertEqual(result["canceled_algo_orders"], 1)

    @patch("src.claw_profit_guard.binance_demo._signed_json")
    def test_close_current_symbol_position_submits_market_close_order(
        self, mock_signed_json
    ) -> None:
        def fake_signed_json(path: str, **kwargs):
            method = kwargs.get("method", "GET")
            params = kwargs.get("params") or {}
            if path == "/fapi/v2/positionRisk" and method == "GET":
                self.assertEqual(params.get("symbol"), "BNBUSDT")
                return [
                    {
                        "symbol": "BNBUSDT",
                        "positionAmt": "0.03",
                        "positionSide": "LONG",
                    }
                ]
            if path == "/fapi/v1/order" and method == "POST":
                self.assertEqual(params.get("side"), "SELL")
                self.assertEqual(params.get("positionSide"), "LONG")
                self.assertEqual(params.get("type"), "MARKET")
                self.assertEqual(params.get("quantity"), "0.03000000")
                return {"orderId": 3, "status": "FILLED", "executedQty": "0.03"}
            raise AssertionError(f"Unexpected signed path: {path} / {method}")

        mock_signed_json.side_effect = fake_signed_json
        with patch.dict(
            "os.environ",
            {
                "BINANCE_API_KEY": "live-key",
                "BINANCE_SECRET_KEY": "live-secret",
                "BINANCE_FUTURES_ENV": "live",
            },
            clear=False,
        ):
            result = binance_demo.close_current_symbol_position("BNBUSDT")
        self.assertTrue(result["ok"])
        self.assertEqual(result["status"], "closed")
        self.assertEqual(len(result["closed_positions"]), 1)

    @patch("src.claw_profit_guard.binance_demo._http_json")
    def test_demo_order_test_rejects_preview_below_min_notional(self, mock_http_json) -> None:
        mock_http_json.return_value = {
            "symbols": [
                {
                    "symbol": "BNBUSDT",
                    "pricePrecision": 3,
                    "quantityPrecision": 3,
                    "filters": [
                        {
                            "filterType": "PRICE_FILTER",
                            "minPrice": "0.01000000",
                            "maxPrice": "1000000.00000000",
                            "tickSize": "0.01000000",
                        },
                        {
                            "filterType": "LOT_SIZE",
                            "minQty": "0.00100000",
                            "maxQty": "100000.00000000",
                            "stepSize": "0.00100000",
                        },
                        {
                            "filterType": "MIN_NOTIONAL",
                            "minNotional": "10.00000000",
                        },
                    ]
                }
            ]
        }
        with patch.dict(
            "os.environ",
            {
                "BINANCE_API_KEY": "live-key",
                "BINANCE_SECRET_KEY": "live-secret",
                "BINANCE_FUTURES_ENV": "live",
            },
            clear=False,
        ):
            result = binance_demo.demo_order_test(
                {
                    "symbol": "BNBUSDT",
                    "side": "LONG",
                    "entry_price": 624.58,
                    "position_notional_usdt": 5.0,
                }
            )
        self.assertFalse(result["ok"])
        self.assertEqual(result["status"], "preview_invalid")
        self.assertIn("MIN_NOTIONAL", result["message"])

    @patch("src.claw_profit_guard.binance_demo._http_json")
    def test_demo_order_test_reports_minimum_executable_notional_for_small_bnb_trade(
        self, mock_http_json
    ) -> None:
        mock_http_json.return_value = {
            "symbols": [
                {
                    "symbol": "BNBUSDT",
                    "pricePrecision": 3,
                    "quantityPrecision": 2,
                    "filters": [
                        {
                            "filterType": "PRICE_FILTER",
                            "minPrice": "6.600",
                            "maxPrice": "100000",
                            "tickSize": "0.010",
                        },
                        {
                            "filterType": "LOT_SIZE",
                            "minQty": "0.01",
                            "maxQty": "100000",
                            "stepSize": "0.01",
                        },
                        {
                            "filterType": "MIN_NOTIONAL",
                            "notional": "5",
                        },
                    ],
                }
            ]
        }
        with patch.dict(
            "os.environ",
            {
                "BINANCE_API_KEY": "live-key",
                "BINANCE_SECRET_KEY": "live-secret",
                "BINANCE_FUTURES_ENV": "live",
            },
            clear=False,
        ):
            result = binance_demo.demo_order_test(
                {
                    "symbol": "BNBUSDT",
                    "side": "LONG",
                    "entry_price": 623.88,
                    "position_notional_usdt": 4.8,
                }
            )
        self.assertFalse(result["ok"])
        self.assertEqual(result["status"], "preview_invalid")
        self.assertEqual(
            result["preview"]["exchange_minimums"]["minimum_executable_notional_usdt"], "6.23"
        )
        self.assertIn("Requested notional 4.80", result["message"])
        self.assertIn("minimum executable notional 6.23", result["message"])

    def test_get_account_snapshot_without_credentials_uses_fallback(self) -> None:
        with patch.dict(
            "os.environ",
            {
                "BINANCE_API_KEY": "",
                "BINANCE_SECRET_KEY": "",
                "BINANCE_DEMO_API_KEY": "",
                "BINANCE_DEMO_SECRET_KEY": "",
            },
            clear=False,
        ):
            snapshot = binance_demo.get_account_snapshot("BNBUSDT", profile_name="balanced")
        self.assertFalse(snapshot["live"])
        self.assertFalse(snapshot["connected"])
        self.assertEqual(snapshot["source"], "local_fallback")
        self.assertEqual(snapshot["credentials"]["api_key_env"], "BINANCE_API_KEY")
        self.assertIn("auto_fill", snapshot)

    @patch("src.claw_profit_guard.binance_demo._signed_json")
    def test_get_account_snapshot_with_mocked_signed_calls(self, mock_signed_json) -> None:
        def fake_signed_json(path: str, **kwargs):
            if path == "/fapi/v3/account":
                return {
                    "totalMarginBalance": "1640",
                    "totalWalletBalance": "1000",
                    "availableBalance": "1000",
                    "totalOpenOrderInitialMargin": "0",
                    "assets": [
                        {
                            "asset": "USDT",
                            "walletBalance": "1000",
                            "marginBalance": "1640",
                            "availableBalance": "1000",
                            "openOrderInitialMargin": "0",
                        }
                    ],
                    "positions": [
                        {"symbol": "BNBUSDT", "notional": "640"},
                    ],
                }
            if path == "/fapi/v1/openOrders":
                return []
            if path == "/fapi/v2/positionRisk":
                return [
                    {
                        "symbol": "BNBUSDT",
                        "positionAmt": "1",
                        "entryPrice": "640",
                        "markPrice": "641",
                        "notional": "641",
                        "unRealizedProfit": "1",
                        "liquidationPrice": "500",
                        "initialMargin": "64.1",
                        "maintMargin": "2.56",
                        "positionSide": "BOTH",
                    }
                ]
            if path == "/fapi/v1/userTrades":
                return []
            raise AssertionError(f"Unexpected path: {path}")

        mock_signed_json.side_effect = fake_signed_json
        with patch.dict(
            "os.environ",
            {
                "BINANCE_API_KEY": "live-key",
                "BINANCE_SECRET_KEY": "live-secret",
                "BINANCE_FUTURES_ENV": "live",
            },
            clear=False,
        ):
            snapshot = binance_demo.get_account_snapshot("BNBUSDT", profile_name="balanced")
        self.assertTrue(snapshot["live"])
        self.assertTrue(snapshot["connected"])
        self.assertEqual(snapshot["account"]["estimated_equity_usdt"], 1640.0)
        self.assertEqual(snapshot["account"]["wallet_balance_usdt"], 1000.0)
        self.assertEqual(snapshot["auto_fill"]["account_equity_usdt"], 1000.0)
        self.assertEqual(snapshot["source"], "binance_futures_live")
        self.assertEqual(snapshot["account"]["open_positions"][0]["symbol"], "BNBUSDT")


if __name__ == "__main__":
    unittest.main()
