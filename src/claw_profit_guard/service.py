"""Minimal HTTP service for ClawProfit Guard."""

from __future__ import annotations

import json
from pathlib import Path
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Dict, Tuple
from urllib.parse import parse_qs, urlsplit

from .binance_demo import (
    cancel_current_symbol_orders,
    close_current_symbol_position,
    demo_order_test,
    get_account_snapshot,
    get_market_snapshot,
    live_order_open_position,
    live_order_place_and_cancel,
)
from .engine import evaluate_trade
from .models import EvaluationInput
from .risk_profile import build_symbol_catalog, recommend_profile
from .runtime import (
    compute_backend_fingerprint,
    compute_demo_asset_fingerprint,
    short_fingerprint,
)

ROOT_DIR = Path(__file__).resolve().parents[2]
DEMO_DIR = ROOT_DIR / "web" / "demo"
SERVER_RUNTIME_VERSION = short_fingerprint(compute_backend_fingerprint())


def _health_payload() -> Dict[str, object]:
    workspace_version = short_fingerprint(compute_backend_fingerprint())
    return {
        "status": "ok",
        "service": "claw-profit-guard",
        "server_runtime_version": SERVER_RUNTIME_VERSION,
        "workspace_version": workspace_version,
        "runtime_in_sync": SERVER_RUNTIME_VERSION == workspace_version,
        "asset_version": short_fingerprint(compute_demo_asset_fingerprint()),
    }


def _json_response(handler: BaseHTTPRequestHandler, status: int, payload: Dict) -> None:
    body = json.dumps(payload, ensure_ascii=True).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Content-Length", str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)


def _parse_json(handler: BaseHTTPRequestHandler) -> Tuple[Dict, str]:
    try:
        content_length = int(handler.headers.get("Content-Length", "0"))
    except ValueError:
        return {}, "Invalid Content-Length header."
    try:
        raw = handler.rfile.read(content_length) if content_length else b"{}"
        data = json.loads(raw.decode("utf-8"))
        if not isinstance(data, dict):
            return {}, "JSON body must be an object."
        return data, ""
    except json.JSONDecodeError as exc:
        return {}, f"Invalid JSON: {exc.msg}"


def _file_response(handler: BaseHTTPRequestHandler, path: Path, content_type: str) -> None:
    if not path.exists() or not path.is_file():
        _json_response(handler, HTTPStatus.NOT_FOUND, {"error": "Not found"})
        return
    body = path.read_bytes()
    handler.send_response(HTTPStatus.OK)
    handler.send_header("Content-Type", content_type)
    handler.send_header("Content-Length", str(len(body)))
    handler.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
    handler.send_header("Pragma", "no-cache")
    handler.send_header("Expires", "0")
    handler.end_headers()
    handler.wfile.write(body)


def _template_response(
    handler: BaseHTTPRequestHandler,
    path: Path,
    *,
    content_type: str,
    replacements: Dict[str, str],
) -> None:
    if not path.exists() or not path.is_file():
        _json_response(handler, HTTPStatus.NOT_FOUND, {"error": "Not found"})
        return
    body_text = path.read_text(encoding="utf-8")
    for old, new in replacements.items():
        body_text = body_text.replace(old, new)
    body = body_text.encode("utf-8")
    handler.send_response(HTTPStatus.OK)
    handler.send_header("Content-Type", content_type)
    handler.send_header("Content-Length", str(len(body)))
    handler.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
    handler.send_header("Pragma", "no-cache")
    handler.send_header("Expires", "0")
    handler.end_headers()
    handler.wfile.write(body)


def _query_params(handler: BaseHTTPRequestHandler) -> Dict[str, str]:
    parsed = urlsplit(handler.path)
    query = parse_qs(parsed.query, keep_blank_values=True)
    return {key: values[-1] for key, values in query.items() if values}


class _RequestHandler(BaseHTTPRequestHandler):
    server_version = "ClawProfitGuardHTTP/1.0"

    def do_GET(self) -> None:  # noqa: N802
        path = self.path.split("?", 1)[0]
        if path in {"/demo", "/demo/"}:
            _template_response(
                self,
                DEMO_DIR / "index.html",
                content_type="text/html; charset=utf-8",
                replacements={"__CPG_ASSET_VERSION__": short_fingerprint(compute_demo_asset_fingerprint())},
            )
            return
        if path == "/demo/app.js":
            _file_response(self, DEMO_DIR / "app.js", "application/javascript; charset=utf-8")
            return
        if path == "/demo/styles.css":
            _file_response(self, DEMO_DIR / "styles.css", "text/css; charset=utf-8")
            return
        if path == "/health":
            _json_response(self, HTTPStatus.OK, _health_payload())
            return
        if path == "/v1/catalog/symbols":
            _json_response(
                self,
                HTTPStatus.OK,
                {"symbols": build_symbol_catalog()},
            )
            return
        if path == "/v1/binance/market-snapshot":
            params = _query_params(self)
            symbol = str(params.get("symbol", "BNBUSDT")).upper()
            side = str(params.get("side", "LONG")).upper()
            profile_name = params.get("profile") or None
            try:
                snapshot = get_market_snapshot(
                    symbol,
                    side=side,
                    profile_name=profile_name,
                )
            except Exception as exc:  # broad on purpose for strict API errors
                _json_response(
                    self,
                    HTTPStatus.BAD_REQUEST,
                    {"error": f"Market sync failed: {exc}"},
                )
                return
            _json_response(self, HTTPStatus.OK, snapshot)
            return
        if path == "/v1/binance/account-snapshot":
            params = _query_params(self)
            symbol = str(params.get("symbol", "BNBUSDT")).upper()
            profile_name = params.get("profile") or None
            try:
                snapshot = get_account_snapshot(
                    symbol,
                    profile_name=profile_name,
                )
            except Exception as exc:  # broad on purpose for strict API errors
                _json_response(
                    self,
                    HTTPStatus.BAD_REQUEST,
                    {"error": f"Account sync failed: {exc}"},
                )
                return
            _json_response(self, HTTPStatus.OK, snapshot)
            return
        _json_response(self, HTTPStatus.NOT_FOUND, {"error": "Not found"})

    def do_POST(self) -> None:  # noqa: N802
        path = self.path.split("?", 1)[0]
        if path not in {
            "/v1/evaluate",
            "/v1/profile/recommend",
            "/v1/binance/demo-order-test",
            "/v1/binance/live-order",
            "/v1/binance/live-open-order",
            "/v1/binance/cancel-current-orders",
            "/v1/binance/close-current-position",
        }:
            _json_response(self, HTTPStatus.NOT_FOUND, {"error": "Not found"})
            return

        payload, err = _parse_json(self)
        if err:
            _json_response(self, HTTPStatus.BAD_REQUEST, {"error": err})
            return

        if path == "/v1/profile/recommend":
            try:
                result = recommend_profile(payload)
            except Exception as exc:  # broad on purpose for strict API errors
                _json_response(
                    self,
                    HTTPStatus.BAD_REQUEST,
                    {"error": f"Invalid payload: {exc}"},
                )
                return
            _json_response(self, HTTPStatus.OK, result.to_dict())
            return

        if path == "/v1/binance/demo-order-test":
            trade_payload = payload.get("trade")
            if not isinstance(trade_payload, dict):
                _json_response(
                    self,
                    HTTPStatus.BAD_REQUEST,
                    {"error": "Invalid payload: trade object is required."},
                )
                return
            try:
                result = demo_order_test(trade_payload)
            except Exception as exc:  # broad on purpose for strict API errors
                _json_response(
                    self,
                    HTTPStatus.BAD_REQUEST,
                    {"error": f"Invalid payload: {exc}"},
                )
                return
            _json_response(self, HTTPStatus.OK, result)
            return

        if path == "/v1/binance/live-order":
            trade_payload = payload.get("trade")
            if not isinstance(trade_payload, dict):
                _json_response(
                    self,
                    HTTPStatus.BAD_REQUEST,
                    {"error": "Invalid payload: trade object is required."},
                )
                return
            try:
                result = live_order_place_and_cancel(
                    trade_payload,
                    confirm_live_execution=bool(payload.get("confirm_live_execution")),
                )
            except Exception as exc:  # broad on purpose for strict API errors
                _json_response(
                    self,
                    HTTPStatus.BAD_REQUEST,
                    {"error": f"Invalid payload: {exc}"},
                )
                return
            _json_response(self, HTTPStatus.OK, result)
            return

        if path == "/v1/binance/live-open-order":
            trade_payload = payload.get("trade")
            if not isinstance(trade_payload, dict):
                _json_response(
                    self,
                    HTTPStatus.BAD_REQUEST,
                    {"error": "Invalid payload: trade object is required."},
                )
                return
            try:
                result = live_order_open_position(
                    trade_payload,
                    confirm_live_execution=bool(payload.get("confirm_live_execution")),
                )
            except Exception as exc:  # broad on purpose for strict API errors
                _json_response(
                    self,
                    HTTPStatus.BAD_REQUEST,
                    {"error": f"Invalid payload: {exc}"},
                )
                return
            _json_response(self, HTTPStatus.OK, result)
            return

        if path == "/v1/binance/cancel-current-orders":
            symbol = str(payload.get("symbol", "BNBUSDT")).upper()
            try:
                result = cancel_current_symbol_orders(symbol)
            except Exception as exc:  # broad on purpose for strict API errors
                _json_response(
                    self,
                    HTTPStatus.BAD_REQUEST,
                    {"error": f"Cancel current orders failed: {exc}"},
                )
                return
            _json_response(self, HTTPStatus.OK, result)
            return

        if path == "/v1/binance/close-current-position":
            symbol = str(payload.get("symbol", "BNBUSDT")).upper()
            try:
                result = close_current_symbol_position(symbol)
            except Exception as exc:  # broad on purpose for strict API errors
                _json_response(
                    self,
                    HTTPStatus.BAD_REQUEST,
                    {"error": f"Close current position failed: {exc}"},
                )
                return
            _json_response(self, HTTPStatus.OK, result)
            return

        try:
            data = EvaluationInput.from_dict(payload)
            result = evaluate_trade(data)
        except Exception as exc:  # broad on purpose for strict API errors
            _json_response(
                self,
                HTTPStatus.BAD_REQUEST,
                {"error": f"Invalid payload: {exc}"},
            )
            return

        _json_response(self, HTTPStatus.OK, result.to_dict())

    def log_message(self, format: str, *args) -> None:  # noqa: A003
        # Silence noisy default logs during demo.
        return


def run_server(host: str = "127.0.0.1", port: int = 8080) -> None:
    server = ThreadingHTTPServer((host, port), _RequestHandler)
    print(f"ClawProfit Guard listening on http://{host}:{port}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
