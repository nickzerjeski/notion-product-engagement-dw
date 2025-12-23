import pandas as pd
import plotly.express as px
from dash import Input, Output

from dashboard import data


def register(app) -> None:
    @app.callback(
        Output("kaq1-trend", "figure"),
        Output("kaq1-total", "figure"),
        Input("kaq1-metric", "value"),
        Input("kaq1-tiers", "value"),
        Input("kaq1-date", "start_date"),
        Input("kaq1-date", "end_date"),
        Input("kaq1-overall", "value"),
    )
    def update_kaq1(metric: str, tiers: list[str], start: str, end: str, overall_flags: list[str]):
        tiers = tiers or []
        filtered = data.filter_date(data.kaq1_monthly_tier, "year_month", start, end)
        if tiers:
            filtered = filtered[filtered["subscription_tier"].isin(tiers)]
        plot_df = filtered.copy()
        if "overall" in (overall_flags or []):
            overall_df = data.filter_date(data.kaq1_monthly_overall, "year_month", start, end).copy()
            overall_df["subscription_tier"] = "All tiers"
            plot_df = pd.concat([plot_df, overall_df], ignore_index=True)

        trend = px.line(
            plot_df,
            x="year_month",
            y=metric,
            color="subscription_tier",
            markers=True,
            title="Monthly engagement by subscription tier",
            labels={"year_month": "Time", "subscription_tier": "Subscription Tier", metric: "Value"},
        )
        trend.update_layout(
            legend_title_text="Tier",
            margin=dict(l=20, r=20, t=50, b=20),
            xaxis_title="Time",
            yaxis_title=metric.replace("_", " ").title(),
        )

        totals = data.kaq1_totals[data.kaq1_totals["subscription_tier"].notna()].copy()
        if tiers:
            totals = totals[totals["subscription_tier"].isin(tiers)]
        total_bar = px.bar(
            totals,
            x="subscription_tier",
            y=metric,
            text_auto=True,
            title="Total engagement across the full period",
            labels={"subscription_tier": "Subscription Tier", metric: "Value"},
        )
        total_bar.update_layout(
            margin=dict(l=20, r=20, t=50, b=20),
            xaxis_title="Subscription Tier",
            yaxis_title=metric.replace("_", " ").title(),
        )

        return trend, total_bar
