from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

import pandas as pd

from src.marketcheck_client import MarketCheckClient, normalize_listings
from src.reporting import (
    TargetConfig,
    load_targets_config,
    summarize_listings,
)


def _safe_token(value: str) -> str:
    return value.replace(" ", "-")


def _generate_markdown(
    target: TargetConfig,
    summary: Dict[str, Any],
    histogram: List[Dict[str, Any]],
    lowest: List[Dict[str, Any]],
    report_date: str,
) -> str:
    header = f"# Competitor Report — {target.year} {target.make} {target.model}"
    overview_lines = [
        f"- Total listings: **{summary['count']}**",
        f"- Average price: **${summary['price_avg']:,.2f}**" if summary["price_avg"] else "- Average price: N/A",
        f"- Lowest price: **${summary['price_min']:,.2f}**" if summary["price_min"] else "- Lowest price: N/A",
        f"- Highest price: **${summary['price_max']:,.2f}**" if summary["price_max"] else "- Highest price: N/A",
        f"- Report run: {report_date}",
    ]

    dealer_lines = ["| Dealer | City | State | Listings |", "| --- | --- | --- | --- |"]
    for dealer in summary["dealer_counts"]:
        dealer_lines.append(
            f"| {dealer['dealer_name']} | {dealer.get('city') or ''} | "
            f"{dealer.get('state') or ''} | {dealer['count']} |"
        )

    lowest_lines = ["| Dealer | City | State | Miles | Price | VDP |", "| --- | --- | --- | --- | --- | --- |"]
    for row in lowest:
        price = row.get("price")
        price_text = f"${price:,.0f}" if price else "N/A"
        lowest_lines.append(
            f"| {row['dealer_name']} | {row.get('city') or ''} | {row.get('state') or ''} | "
            f"{row.get('miles') or ''} | "
            f"{price_text} | {row.get('vdp_url') or ''} |"
        )

    hist_lines = ["| Price Bucket | Listings |", "| --- | --- |"]
    for bucket in histogram:
        hist_lines.append(f"| {bucket['bucket']} | {bucket['count']} |")

    sections = [
        header,
        "",
        "## Inventory Summary",
        "",
        *overview_lines,
        "",
        "## Dealer Distribution",
        "",
        *(dealer_lines or ["No dealer data available."]),
        "",
        "## Top 10 Lowest Prices",
        "",
        *(lowest_lines or ["No price data available."]),
        "",
        "## Price Histogram",
        "",
        *(hist_lines or ["No price histogram available."]),
        "",
    ]
    return "\n".join(sections)


def _write_outputs(
    target: TargetConfig,
    listings: List[Dict[str, Any]],
    summary: Dict[str, Any],
    report_date: datetime,
) -> None:
    reports_dir = Path("reports")
    data_dir = reports_dir / "data"
    reports_dir.mkdir(parents=True, exist_ok=True)
    data_dir.mkdir(parents=True, exist_ok=True)

    date_stamp = report_date.strftime("%Y%m%d")
    make_token = _safe_token(target.make)
    model_token = _safe_token(target.model)

    csv_path = data_dir / f"{make_token}_{model_token}_{target.year}_{date_stamp}.csv"
    markdown_path = (
        reports_dir / f"competitors_{make_token}_{model_token}_{target.year}_{date_stamp}.md"
    )

    pd.DataFrame(listings).to_csv(csv_path, index=False)

    markdown = _generate_markdown(
        target,
        summary,
        summary["price_histogram"],
        summary["top_lowest"],
        report_date.strftime("%Y-%m-%d"),
    )
    markdown_path.write_text(markdown, encoding="utf-8")


def _run_target(target: TargetConfig, client: MarketCheckClient) -> None:
    params = {
        "year": target.year,
        "make": target.make,
        "model": target.model,
        "trim": target.trim,
        "zip": target.zip,
        "radius": target.radius,
        "rows": target.rows,
        "price_min": target.price_min,
        "price_max": target.price_max,
    }
    response = client.search_active(**params)
    listings = normalize_listings(response.get("listings", []))
    summary = summarize_listings(listings)
    report_date = datetime.utcnow()

    _write_outputs(target, listings, summary, report_date)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate MarketCheck competitor reports.")
    parser.add_argument("--year", type=int)
    parser.add_argument("--make")
    parser.add_argument("--model")
    parser.add_argument("--trim")
    parser.add_argument("--zip")
    parser.add_argument("--radius", type=int, default=100)
    parser.add_argument("--rows", type=int, default=200)
    parser.add_argument("--price-min", type=float)
    parser.add_argument("--price-max", type=float)
    parser.add_argument("--config", type=str, help="Path to YAML config for batch runs.")
    return parser.parse_args()


def main() -> None:
    args = _parse_args()

    client = MarketCheckClient()

    targets: Iterable[TargetConfig]
    if args.config:
        targets = load_targets_config(args.config)
    else:
        missing = [field for field in ("year", "make", "model", "zip") if getattr(args, field) is None]
        if missing:
            raise SystemExit(f"Missing required arguments: {', '.join(missing)}")
        target_dict = {
            "year": args.year,
            "make": args.make,
            "model": args.model,
            "trim": args.trim,
            "zip": args.zip,
            "radius": args.radius,
            "rows": args.rows,
            "price_min": args.price_min,
            "price_max": args.price_max,
        }
        targets = [TargetConfig.from_dict(target_dict)]

    for target in targets:
        _run_target(target, client)


if __name__ == "__main__":
    main()
