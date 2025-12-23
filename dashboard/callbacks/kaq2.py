import pandas as pd
import plotly.express as px
from dash import Input, Output

from dashboard import data
from dashboard.constants import MONTH_LABELS


def register(app) -> None:
    @app.callback(
        Output("kaq2-trend", "figure"),
        Output("kaq2-seasonality", "figure"),
        Output("kaq2-yearly", "figure"),
        Input("kaq2-metric", "value"),
        Input("kaq2-types", "value"),
        Input("kaq2-date", "start_date"),
        Input("kaq2-date", "end_date"),
        Input("kaq2-overall", "value"),
    )
    def update_kaq2(metric: str, types: list[str], start: str, end: str, overall_flags: list[str]):
        types = types or []
        filtered = data.filter_date(data.kaq2_monthly_type, "year_month", start, end)
        if types:
            filtered = filtered[filtered["content_type"].isin(types)]

        plot_df = filtered.copy()
        if "overall" in (overall_flags or []):
            overall_df = data.filter_date(data.kaq2_monthly_overall, "year_month", start, end).copy()
            overall_df["content_type"] = "all"
            plot_df = pd.concat([plot_df, overall_df], ignore_index=True)

        trend = px.line(
            plot_df,
            x="year_month",
            y=metric,
            color="content_type",
            markers=True,
            title="Monthly engagement by content type",
            labels={"year_month": "Time", "content_type": "Content Type", metric: "Value"},
        )
        trend.update_layout(
            legend_title_text="Content type",
            margin=dict(l=20, r=20, t=50, b=20),
            xaxis_title="Time",
            yaxis_title=metric.replace("_", " ").title(),
        )

        seasonality_df = data.kaq2_monthly_type.copy()
        seasonality_df = seasonality_df[seasonality_df["content_type"].isin(types)] if types else seasonality_df
        seasonality_df = seasonality_df.groupby(["month", "content_type"], as_index=False)[metric].mean()
        seasonality_df["month_label"] = seasonality_df["month"].map(MONTH_LABELS)
        seasonality = px.line(
            seasonality_df,
            x="month_label",
            y=metric,
            color="content_type",
            markers=True,
            title="Seasonality (monthly average across years)",
            labels={"month_label": "Month", "content_type": "Content Type", metric: "Value"},
        )
        seasonality.update_layout(
            legend_title_text="Content type",
            margin=dict(l=20, r=20, t=50, b=20),
            xaxis_title="Month",
            yaxis_title=metric.replace("_", " ").title(),
        )

        yearly_df = data.kaq2_yearly[data.kaq2_yearly["content_type"].notna()].copy()
        if types:
            yearly_df = yearly_df[yearly_df["content_type"].isin(types)]
        yearly = px.bar(
            yearly_df,
            x="content_type",
            y=metric,
            color="year",
            barmode="group",
            title="Yearly totals by content type",
            labels={"content_type": "Content Type", "year": "Year", metric: "Value"},
        )
        yearly.update_layout(
            legend_title_text="Year",
            margin=dict(l=20, r=20, t=50, b=20),
            xaxis_title="Content Type",
            yaxis_title=metric.replace("_", " ").title(),
        )

        return trend, seasonality, yearly
