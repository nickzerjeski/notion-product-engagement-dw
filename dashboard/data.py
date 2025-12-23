from __future__ import annotations

from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
RESULTS_DIR = BASE_DIR / "results"


def load_csv(name: str) -> pd.DataFrame:
    return pd.read_csv(RESULTS_DIR / f"{name}.csv")


def add_year_month(df: pd.DataFrame, year_col: str = "year", month_col: str = "month") -> pd.DataFrame:
    df = df.copy()
    df[year_col] = pd.to_numeric(df[year_col], errors="coerce")
    df[month_col] = pd.to_numeric(df[month_col], errors="coerce")
    df["year_month"] = pd.to_datetime(
        dict(year=df[year_col], month=df[month_col], day=1), errors="coerce"
    )
    return df


def filter_date(df: pd.DataFrame, date_col: str, start: str | None, end: str | None) -> pd.DataFrame:
    filtered = df
    if start:
        filtered = filtered[filtered[date_col] >= pd.to_datetime(start)]
    if end:
        filtered = filtered[filtered[date_col] <= pd.to_datetime(end)]
    return filtered


kaq1 = add_year_month(load_csv("kaq1"))
kaq2 = add_year_month(load_csv("kaq2"))
kaq3 = load_csv("kaq3")
kaq3["signup_month"] = pd.to_datetime(kaq3["signup_month"], errors="coerce")
kaq4 = add_year_month(load_csv("kaq4"))
kaq5 = add_year_month(load_csv("kaq5"))
aq1 = load_csv("aq1")
aq2 = load_csv("aq2")
aq2["month_start"] = pd.to_datetime(aq2["month_start"], errors="coerce")

kaq1_monthly = kaq1[kaq1["year_month"].notna()].copy()
kaq1_monthly_tier = kaq1_monthly[kaq1_monthly["subscription_tier"].notna()].copy()
kaq1_monthly_overall = kaq1_monthly[kaq1_monthly["subscription_tier"].isna()].copy()
kaq1_totals = kaq1[kaq1["year"].isna() & kaq1["month"].isna()].copy()

kaq2_monthly = kaq2[kaq2["year_month"].notna()].copy()
kaq2_monthly_type = kaq2_monthly[kaq2_monthly["content_type"].notna()].copy()
kaq2_monthly_overall = kaq2_monthly[kaq2_monthly["content_type"].isna()].copy()
kaq2_yearly = kaq2[kaq2["year"].notna() & kaq2["month"].isna()].copy()
kaq2_totals = kaq2[kaq2["year"].isna() & kaq2["month"].isna()].copy()

kaq4_monthly = kaq4[kaq4["year_month"].notna()].copy()
kaq4_monthly_platform = kaq4_monthly[kaq4_monthly["platform"].notna()].copy()
kaq4_monthly_overall = kaq4_monthly[kaq4_monthly["platform"].isna()].copy()
kaq4_totals = kaq4[kaq4["year"].isna() & kaq4["month"].isna()].copy()

kaq5["work_mode"] = kaq5["work_mode"].astype(str)

KAQ1_DATE_MIN = kaq1_monthly["year_month"].min()
KAQ1_DATE_MAX = kaq1_monthly["year_month"].max()
KAQ2_DATE_MIN = kaq2_monthly["year_month"].min()
KAQ2_DATE_MAX = kaq2_monthly["year_month"].max()
KAQ3_DATE_MIN = kaq3["signup_month"].min()
KAQ3_DATE_MAX = kaq3["signup_month"].max()
KAQ4_DATE_MIN = kaq4_monthly["year_month"].min()
KAQ4_DATE_MAX = kaq4_monthly["year_month"].max()
KAQ5_DATE_MIN = kaq5["year_month"].min()
KAQ5_DATE_MAX = kaq5["year_month"].max()
