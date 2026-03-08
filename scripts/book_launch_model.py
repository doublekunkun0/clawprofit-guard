#!/usr/bin/env python3
"""Generate scenario summaries for the AI practical book launch package."""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = ROOT / "docs" / "ai_book_business" / "financial_scenarios.json"
OUTPUT_DIR = ROOT / "output" / "book_launch"
JSON_OUTPUT = OUTPUT_DIR / "unit_economics_summary.json"
CSV_OUTPUT = OUTPUT_DIR / "unit_economics_summary.csv"


def load_config() -> dict:
    with CONFIG_PATH.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def fmt_money(value: float) -> str:
    return f"{value:.2f}"


def clean_number(value: float | int | None) -> float | int | None:
    if isinstance(value, float):
        return round(value, 2)
    return value


def summarize_direct_sales(scenario: dict) -> list[dict]:
    rows = []
    price = scenario["price"]
    variable_cost_rate = scenario["variable_cost_rate"]
    fixed_min = scenario["fixed_cost_min"]
    fixed_max = scenario["fixed_cost_max"]
    contribution = price * (1 - variable_cost_rate)
    break_even_min = math.ceil(fixed_min / contribution)
    break_even_max = math.ceil(fixed_max / contribution)

    for units in scenario["sales"]:
        gross_revenue = price * units
        net_before_fixed = gross_revenue * (1 - variable_cost_rate)
        profit_min = net_before_fixed - fixed_max
        profit_max = net_before_fixed - fixed_min
        rows.append(
            {
                "scenario_id": scenario["id"],
                "scenario_label": scenario["label"],
                "units": units,
                "gross_revenue_min": clean_number(gross_revenue),
                "gross_revenue_max": clean_number(gross_revenue),
                "profit_min": clean_number(profit_min),
                "profit_max": clean_number(profit_max),
                "break_even_units_min": break_even_min,
                "break_even_units_max": break_even_max,
            }
        )
    return rows


def summarize_royalty(scenario: dict) -> list[dict]:
    rows = []
    list_price = scenario["list_price"]
    royalty_min = scenario["royalty_rate_min"]
    royalty_max = scenario["royalty_rate_max"]

    for units in scenario["sales"]:
        income_min = list_price * royalty_min * units
        income_max = list_price * royalty_max * units
        rows.append(
            {
                "scenario_id": scenario["id"],
                "scenario_label": scenario["label"],
                "units": units,
                "gross_revenue_min": clean_number(income_min),
                "gross_revenue_max": clean_number(income_max),
                "profit_min": clean_number(income_min),
                "profit_max": clean_number(income_max),
                "break_even_units_min": 0,
                "break_even_units_max": 0,
            }
        )
    return rows


def summarize_unit_profit(scenario: dict) -> list[dict]:
    rows = []
    fixed_min = scenario["fixed_cost_min"]
    fixed_max = scenario["fixed_cost_max"]
    unit_profit_min = scenario["unit_profit_min"]
    unit_profit_max = scenario["unit_profit_max"]

    break_even_min = None if unit_profit_max <= 0 else math.ceil(fixed_min / unit_profit_max)
    break_even_max = None if unit_profit_min <= 0 else math.ceil(fixed_max / unit_profit_min)

    for units in scenario["sales"]:
        gross_profit_min = units * unit_profit_min
        gross_profit_max = units * unit_profit_max
        profit_min = gross_profit_min - fixed_max
        profit_max = gross_profit_max - fixed_min
        rows.append(
            {
                "scenario_id": scenario["id"],
                "scenario_label": scenario["label"],
                "units": units,
                "gross_revenue_min": clean_number(gross_profit_min),
                "gross_revenue_max": clean_number(gross_profit_max),
                "profit_min": clean_number(profit_min),
                "profit_max": clean_number(profit_max),
                "break_even_units_min": break_even_min,
                "break_even_units_max": break_even_max,
            }
        )
    return rows


def build_rows(config: dict) -> list[dict]:
    rows: list[dict] = []
    for scenario in config["scenarios"]:
        model = scenario["model"]
        if model == "direct_sales":
            rows.extend(summarize_direct_sales(scenario))
        elif model == "royalty":
            rows.extend(summarize_royalty(scenario))
        elif model == "unit_profit":
            rows.extend(summarize_unit_profit(scenario))
        else:
            raise ValueError(f"Unsupported model: {model}")
    return rows


def write_outputs(rows: list[dict]) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    with JSON_OUTPUT.open("w", encoding="utf-8") as handle:
        json.dump(rows, handle, ensure_ascii=False, indent=2)

    with CSV_OUTPUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "scenario_id",
                "scenario_label",
                "units",
                "gross_revenue_min",
                "gross_revenue_max",
                "profit_min",
                "profit_max",
                "break_even_units_min",
                "break_even_units_max",
            ],
        )
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    key: fmt_money(value) if isinstance(value, float) else value
                    for key, value in row.items()
                }
            )


def fmt_break_even(value: int | None) -> str:
    return "unbounded" if value is None else str(value)


def print_summary(rows: list[dict]) -> None:
    print("AI practical book launch scenarios")
    for row in rows:
        profit_range = f"{fmt_money(row['profit_min'])} to {fmt_money(row['profit_max'])}"
        revenue_range = (
            f"{fmt_money(row['gross_revenue_min'])} to {fmt_money(row['gross_revenue_max'])}"
        )
        print(
            f"- {row['scenario_label']} | units={row['units']} | "
            f"revenue_or_income={revenue_range} | profit={profit_range} | "
            f"break_even_units={fmt_break_even(row['break_even_units_min'])} "
            f"to {fmt_break_even(row['break_even_units_max'])}"
        )


def main() -> None:
    config = load_config()
    rows = build_rows(config)
    write_outputs(rows)
    print_summary(rows)


if __name__ == "__main__":
    main()
