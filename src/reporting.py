from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

import pandas as pd


DATE_STAMP_FORMAT = "%Y%m%d"
PRICE_BUCKET = 2500


@dataclass
class TargetConfig:
    year: int
    make: str
    model: str
    trim: Optional[str] = None
    zip: Optional[str] = None
    radius: Optional[int] = None
    rows: Optional[int] = None
    price_min: Optional[float] = None
    price_max: Optional[float] = None
    context_file: Optional[str] = None

    @classmethod
    def from_dict(cls, payload: Dict[str, Any]) -> "TargetConfig":
        return cls(
            year=int(payload["year"]),
            make=str(payload["make"]),
            model=str(payload["model"]),
            trim=payload.get("trim"),
            zip=payload.get("zip"),
            radius=payload.get("radius"),
            rows=payload.get("rows"),
            price_min=payload.get("price_min"),
            price_max=payload.get("price_max"),
            context_file=payload.get("context") or payload.get("context_file"),
        )

    @property
    def date_stamp(self) -> str:
        return datetime.utcnow().strftime(DATE_STAMP_FORMAT)

    def safe_stub(self) -> str:
        return "_".join(
            [
                self.make.replace(" ", "").lower(),
                self.model.replace(" ", "").lower(),
                str(self.year),
            ]
        )


def _parse_scalar(value: str) -> Any:
    value = value.strip()
    if not value:
        return None
    if (value.startswith('"') and value.endswith('"')) or (
        value.startswith("'") and value.endswith("'")
    ):
        return value[1:-1]
    if value.isdigit():
        return int(value)
    try:
        return float(value)
    except ValueError:
        pass
    if value.lower() in {"true", "false"}:
        return value.lower() == "true"
    return value


def _naive_yaml_loader(text: str) -> List[Dict[str, Any]]:
    """Parse a very small subset of YAML (list of dictionaries)."""
    items: List[Dict[str, Any]] = []
    current: Optional[Dict[str, Any]] = None
    current_indent = 0

    for raw_line in text.splitlines():
        if not raw_line.strip() or raw_line.strip().startswith("#"):
            continue

        indent = len(raw_line) - len(raw_line.lstrip(" "))
        line = raw_line.strip()

        if line.startswith("-"):
            if current:
                items.append(current)
            current = {}
            current_indent = indent + 2
            remainder = line[1:].strip()
            if remainder:
                key, _, val = remainder.partition(":")
                current[key.strip()] = _parse_scalar(val)
            continue

        if current is None:
            raise ValueError("YAML format must begin with a list item ('-').")

        if indent < current_indent:
            # new top-level entry
            items.append(current)
            current = {}
            current_indent = indent

        key, _, val = line.partition(":")
        current[key.strip()] = _parse_scalar(val)

    if current:
        items.append(current)
    return items


def load_targets_config(path: str | Path) -> List[TargetConfig]:
    path = Path(path)
    text = path.read_text(encoding="utf-8")
    try:
        import yaml  # type: ignore

        raw_items = yaml.safe_load(text)  # type: ignore[attr-defined]
        if not isinstance(raw_items, list):
            raise ValueError("Config must be a list of target dictionaries.")
    except ModuleNotFoundError:
        raw_items = _naive_yaml_loader(text)

    return [TargetConfig.from_dict(item) for item in raw_items]


def summarize_listings(records: Iterable[Dict[str, Any]]) -> Dict[str, Any]:
    frame = pd.DataFrame(records)
    if frame.empty:
        return {
            "count": 0,
            "price_avg": None,
            "price_min": None,
            "price_max": None,
            "dealer_counts": [],
            "top_lowest": [],
            "price_histogram": [],
        }

    price_series = pd.to_numeric(frame["price"], errors="coerce")
    frame["price"] = price_series
    frame["dealer_name"] = frame["dealer_name"].fillna("Unknown Dealer")

    summary = {
        "count": int(frame.shape[0]),
        "price_avg": round(float(price_series.mean()), 2) if price_series.notna().any() else None,
        "price_min": round(float(price_series.min()), 2) if price_series.notna().any() else None,
        "price_max": round(float(price_series.max()), 2) if price_series.notna().any() else None,
    }

    dealer_counts = (
        frame.groupby(["dealer_name", "city", "state"])["vin"]
        .count()
        .reset_index()
        .rename(columns={"vin": "count"})
        .sort_values(by="count", ascending=False)
    )
    summary["dealer_counts"] = dealer_counts.to_dict(orient="records")

    lowest = (
        frame.dropna(subset=["price"])
        .sort_values("price", ascending=True)
        .head(10)
        .loc[:, ["dealer_name", "city", "state", "price", "miles", "vdp_url"]]
    )
    summary["top_lowest"] = lowest.to_dict(orient="records")

    if price_series.notna().any():
        buckets = defaultdict(int)
        for price in price_series.dropna():
            bucket_floor = int(price // PRICE_BUCKET) * PRICE_BUCKET
            bucket_label = f"${bucket_floor:,.0f} - ${bucket_floor + PRICE_BUCKET - 1:,.0f}"
            buckets[bucket_label] += 1
        summary["price_histogram"] = [
            {"bucket": key, "count": buckets[key]} for key in sorted(buckets.keys())
        ]
    else:
        summary["price_histogram"] = []

    return summary


def resolve_latest_csv(target: TargetConfig, csv_root: Path) -> Optional[Path]:
    pattern = f"{target.make}_{target.model}_{target.year}_*.csv"
    candidates = sorted(csv_root.glob(pattern))
    return candidates[-1] if candidates else None
