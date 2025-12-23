import pandas as pd
import plotly.express as px
from dash import Input, Output

from dashboard import data


def register(app) -> None:
    @app.callback(
        Output("kaq4-activity", "figure"),
        Output("kaq4-duration", "figure"),
        Input("kaq4-platforms", "value"),
        Input("kaq4-date", "start_date"),
        Input("kaq4-date", "end_date"),
        Input("kaq4-overall", "value"),
    )
    def update_kaq4(platforms: list[str], start: str, end: str, overall_flags: list[str]):
        platforms = platforms or []
        filtered = data.filter_date(data.kaq4_monthly_platform, "year_month", start, end)
        if platforms:
            filtered = filtered[filtered["platform"].isin(platforms)]

        plot_df = filtered.copy()
        if "overall" in (overall_flags or []):
            overall_df = data.filter_date(data.kaq4_monthly_overall, "year_month", start, end).copy()
            overall_df["platform"] = "overall"
            plot_df = pd.concat([plot_df, overall_df], ignore_index=True)

        activity_fig = px.line(
            plot_df,
            x="year_month",
            y="dau",
            color="platform",
            markers=True,
            title="Monthly active users by platform",
            labels={"year_month": "Time", "platform": "Platform", "dau": "Daily Active Users"},
        )
        activity_fig.update_layout(
            legend_title_text="Platform",
            margin=dict(l=20, r=20, t=50, b=20),
            xaxis_title="Time",
            yaxis_title="Daily Active Users",
        )

        duration_fig = px.line(
            plot_df,
            x="year_month",
            y="avg_session_duration_sec",
            color="platform",
            markers=True,
            title="Average session duration (seconds)",
            labels={
                "year_month": "Time",
                "platform": "Platform",
                "avg_session_duration_sec": "Avg Session Duration (sec)",
            },
        )
        duration_fig.update_layout(
            legend_title_text="Platform",
            margin=dict(l=20, r=20, t=50, b=20),
            xaxis_title="Time",
            yaxis_title="Avg Session Duration (sec)",
        )

        return activity_fig, duration_fig
