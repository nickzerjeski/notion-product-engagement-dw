from __future__ import annotations

from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
from dash import Dash, Input, Output, dcc, html, dash_table

BASE_DIR = Path(__file__).resolve().parent.parent
RESULTS_DIR = BASE_DIR / "results"

pio.templates.default = "plotly_white"

MONTH_LABELS = {
    1: "Jan",
    2: "Feb",
    3: "Mar",
    4: "Apr",
    5: "May",
    6: "Jun",
    7: "Jul",
    8: "Aug",
    9: "Sep",
    10: "Oct",
    11: "Nov",
    12: "Dec",
}


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


def datatable_from_df(df: pd.DataFrame, table_id: str) -> dash_table.DataTable:
    return dash_table.DataTable(
        id=table_id,
        columns=[{"name": col, "id": col} for col in df.columns],
        data=df.to_dict("records"),
        page_size=12,
        style_table={"overflowX": "auto"},
        style_cell={
            "padding": "6px",
            "fontFamily": "var(--font-body)",
            "fontSize": "13px",
            "whiteSpace": "normal",
        },
        style_header={"fontWeight": "600", "backgroundColor": "#f2f2f2"},
    )


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


def make_kpi(label: str, value: str, hint: str | None = None) -> html.Div:
    return html.Div(
        [
            html.Div(label, className="kpi-label"),
            html.Div(value, className="kpi-value"),
            html.Div(hint or "", className="kpi-hint"),
        ],
        className="kpi-card",
    )


app = Dash(__name__, title="Notion Engagement Dashboard")
server = app.server

kaq1_date_min = kaq1_monthly["year_month"].min()
kaq1_date_max = kaq1_monthly["year_month"].max()
kaq2_date_min = kaq2_monthly["year_month"].min()
kaq2_date_max = kaq2_monthly["year_month"].max()
kaq3_date_min = kaq3["signup_month"].min()
kaq3_date_max = kaq3["signup_month"].max()
kaq4_date_min = kaq4_monthly["year_month"].min()
kaq4_date_max = kaq4_monthly["year_month"].max()
kaq5_date_min = kaq5["year_month"].min()
kaq5_date_max = kaq5["year_month"].max()


app.layout = html.Div(
    className="page",
    children=[
        dcc.Tabs(
            className="tabs",
            children=[
                dcc.Tab(
                    label="Overview",
                    className="tab",
                    selected_className="tab-selected",
                    children=[
                        html.Div(
                            className="grid-3",
                            children=[
                                make_kpi(
                                    "Total active users",
                                    f"{int(kaq1_totals[kaq1_totals['subscription_tier'].isna()]['dau'].iloc[0]):,}",
                                    "Across all months and tiers",
                                ),
                                make_kpi(
                                    "Total events",
                                    f"{int(kaq1_totals[kaq1_totals['subscription_tier'].isna()]['events'].iloc[0]):,}",
                                    "Across all months and tiers",
                                ),
                                make_kpi(
                                    "Latest activation rate",
                                    f"{kaq3.sort_values('signup_month')['activation_rate'].iloc[-1]:.0%}",
                                    "Most recent cohort",
                                ),
                                make_kpi(
                                    "Latest MoM DAU change",
                                    f"{aq2.sort_values('month_start')['rel_change'].dropna().iloc[-1]:.0%}",
                                    "Relative change vs previous month",
                                ),
                            ],
                        ),
                        html.Div(
                            className="panel",
                            children=[
                                html.H3("User growth overview"),
                                dcc.Graph(id="overview-growth"),
                            ],
                        ),
                    ],
                ),
                dcc.Tab(
                    label="Engagement by Tier",
                    className="tab",
                    selected_className="tab-selected",
                    children=[
                        html.Div(
                            className="controls",
                            children=[
                                html.Div(
                                    [
                                        html.Label("Metric"),
                                        dcc.Dropdown(
                                            id="kaq1-metric",
                                            options=[
                                                {"label": "Daily Active Users", "value": "dau"},
                                                {"label": "Events", "value": "events"},
                                                {
                                                    "label": "Events per Active User",
                                                    "value": "events_per_active_user",
                                                },
                                            ],
                                            value="dau",
                                            clearable=False,
                                        ),
                                    ],
                                    className="control",
                                ),
                                html.Div(
                                    [
                                        html.Label("Subscription tiers"),
                                        dcc.Dropdown(
                                            id="kaq1-tiers",
                                            options=[
                                                {"label": tier, "value": tier}
                                                for tier in sorted(kaq1_monthly_tier["subscription_tier"].unique())
                                            ],
                                            value=sorted(kaq1_monthly_tier["subscription_tier"].unique()),
                                            multi=True,
                                        ),
                                    ],
                                    className="control",
                                ),
                                html.Div(
                                    [
                                        html.Label("Date range"),
                                        dcc.DatePickerRange(
                                            id="kaq1-date",
                                            min_date_allowed=kaq1_date_min,
                                            max_date_allowed=kaq1_date_max,
                                            start_date=kaq1_date_min,
                                            end_date=kaq1_date_max,
                                        ),
                                    ],
                                    className="control",
                                ),
                                html.Div(
                                    [
                                        html.Label("Include overall line"),
                                        dcc.Checklist(
                                            id="kaq1-overall",
                                            options=[{"label": "Overall", "value": "overall"}],
                                            value=["overall"],
                                        ),
                                    ],
                                    className="control checklist",
                                ),
                            ],
                        ),
                        html.Div(
                            className="grid-2",
                            children=[
                                dcc.Graph(id="kaq1-trend"),
                                dcc.Graph(id="kaq1-total"),
                            ],
                        ),
                        html.Details(
                            className="data-details",
                            children=[
                                html.Summary("View KAQ1 raw data"),
                                datatable_from_df(kaq1, "kaq1-table"),
                            ],
                        ),
                    ],
                ),
                dcc.Tab(
                    label="Content Types",
                    className="tab",
                    selected_className="tab-selected",
                    children=[
                        html.Div(
                            className="controls",
                            children=[
                                html.Div(
                                    [
                                        html.Label("Metric"),
                                        dcc.Dropdown(
                                            id="kaq2-metric",
                                            options=[
                                                {"label": "Daily Active Users", "value": "dau"},
                                                {"label": "Events", "value": "events"},
                                                {
                                                    "label": "Events per Active User",
                                                    "value": "events_per_active_user",
                                                },
                                            ],
                                            value="dau",
                                            clearable=False,
                                        ),
                                    ],
                                    className="control",
                                ),
                                html.Div(
                                    [
                                        html.Label("Content types"),
                                        dcc.Dropdown(
                                            id="kaq2-types",
                                            options=[
                                                {"label": t.replace("_", " ").title(), "value": t}
                                                for t in sorted(kaq2_monthly_type["content_type"].unique())
                                            ],
                                            value=sorted(kaq2_monthly_type["content_type"].unique()),
                                            multi=True,
                                        ),
                                    ],
                                    className="control",
                                ),
                                html.Div(
                                    [
                                        html.Label("Date range"),
                                        dcc.DatePickerRange(
                                            id="kaq2-date",
                                            min_date_allowed=kaq2_date_min,
                                            max_date_allowed=kaq2_date_max,
                                            start_date=kaq2_date_min,
                                            end_date=kaq2_date_max,
                                        ),
                                    ],
                                    className="control",
                                ),
                                html.Div(
                                    [
                                        html.Label("Include overall line"),
                                        dcc.Checklist(
                                            id="kaq2-overall",
                                            options=[{"label": "Overall", "value": "overall"}],
                                            value=["overall"],
                                        ),
                                    ],
                                    className="control checklist",
                                ),
                            ],
                        ),
                        html.Div(
                            className="grid-2",
                            children=[
                                dcc.Graph(id="kaq2-trend"),
                                dcc.Graph(id="kaq2-seasonality"),
                            ],
                        ),
                        html.Div(
                            className="panel",
                            children=[
                                html.H3("Yearly totals"),
                                dcc.Graph(id="kaq2-yearly"),
                            ],
                        ),
                        html.Details(
                            className="data-details",
                            children=[
                                html.Summary("View KAQ2 raw data"),
                                datatable_from_df(kaq2, "kaq2-table"),
                            ],
                        ),
                    ],
                ),
                dcc.Tab(
                    label="Activation",
                    className="tab",
                    selected_className="tab-selected",
                    children=[
                        html.Div(
                            className="controls",
                            children=[
                                html.Div(
                                    [
                                        html.Label("Signup month range"),
                                        dcc.DatePickerRange(
                                            id="kaq3-date",
                                            min_date_allowed=kaq3_date_min,
                                            max_date_allowed=kaq3_date_max,
                                            start_date=kaq3_date_min,
                                            end_date=kaq3_date_max,
                                        ),
                                    ],
                                    className="control",
                                ),
                            ],
                        ),
                        html.Div(
                            className="grid-2",
                            children=[
                                dcc.Graph(id="kaq3-rate"),
                                dcc.Graph(id="kaq3-volume"),
                            ],
                        ),
                        html.Details(
                            className="data-details",
                            children=[
                                html.Summary("View KAQ3 raw data"),
                                datatable_from_df(kaq3, "kaq3-table"),
                            ],
                        ),
                    ],
                ),
                dcc.Tab(
                    label="Device Impact",
                    className="tab",
                    selected_className="tab-selected",
                    children=[
                        html.Div(
                            className="controls",
                            children=[
                                html.Div(
                                    [
                                        html.Label("Platforms"),
                                        dcc.Dropdown(
                                            id="kaq4-platforms",
                                            options=[
                                                {"label": p.title(), "value": p}
                                                for p in sorted(kaq4_monthly_platform["platform"].unique())
                                            ],
                                            value=sorted(kaq4_monthly_platform["platform"].unique()),
                                            multi=True,
                                        ),
                                    ],
                                    className="control",
                                ),
                                html.Div(
                                    [
                                        html.Label("Date range"),
                                        dcc.DatePickerRange(
                                            id="kaq4-date",
                                            min_date_allowed=kaq4_date_min,
                                            max_date_allowed=kaq4_date_max,
                                            start_date=kaq4_date_min,
                                            end_date=kaq4_date_max,
                                        ),
                                    ],
                                    className="control",
                                ),
                                html.Div(
                                    [
                                        html.Label("Include overall line"),
                                        dcc.Checklist(
                                            id="kaq4-overall",
                                            options=[{"label": "Overall", "value": "overall"}],
                                            value=["overall"],
                                        ),
                                    ],
                                    className="control checklist",
                                ),
                            ],
                        ),
                        html.Div(
                            className="grid-2",
                            children=[
                                dcc.Graph(id="kaq4-activity"),
                                dcc.Graph(id="kaq4-duration"),
                            ],
                        ),
                        html.Details(
                            className="data-details",
                            children=[
                                html.Summary("View KAQ4 raw data"),
                                datatable_from_df(kaq4, "kaq4-table"),
                            ],
                        ),
                    ],
                ),
                dcc.Tab(
                    label="Collaboration",
                    className="tab",
                    selected_className="tab-selected",
                    children=[
                        html.Div(
                            className="controls",
                            children=[
                                html.Div(
                                    [
                                        html.Label("Date range"),
                                        dcc.DatePickerRange(
                                            id="kaq5-date",
                                            min_date_allowed=kaq5_date_min,
                                            max_date_allowed=kaq5_date_max,
                                            start_date=kaq5_date_min,
                                            end_date=kaq5_date_max,
                                        ),
                                    ],
                                    className="control",
                                ),
                            ],
                        ),
                        html.Div(
                            className="grid-2",
                            children=[
                                dcc.Graph(id="kaq5-proportion"),
                                dcc.Graph(id="kaq5-events"),
                            ],
                        ),
                        html.Details(
                            className="data-details",
                            children=[
                                html.Summary("View KAQ5 raw data"),
                                datatable_from_df(kaq5, "kaq5-table"),
                            ],
                        ),
                    ],
                ),
                dcc.Tab(
                    label="Additional Queries",
                    className="tab",
                    selected_className="tab-selected",
                    children=[
                        html.Div(
                            className="grid-2",
                            children=[
                                dcc.Graph(id="aq1-events"),
                                dcc.Graph(id="aq2-dau"),
                            ],
                        ),
                        html.Div(
                            className="panel",
                            children=[
                                dcc.Graph(id="aq2-change"),
                            ],
                        ),
                        html.Details(
                            className="data-details",
                            children=[
                                html.Summary("View AQ1 raw data"),
                                datatable_from_df(aq1, "aq1-table"),
                            ],
                        ),
                        html.Details(
                            className="data-details",
                            children=[
                                html.Summary("View AQ2 raw data"),
                                datatable_from_df(aq2, "aq2-table"),
                            ],
                        ),
                    ],
                ),
            ],
        ),
    ],
)

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
    filtered = filter_date(kaq1_monthly_tier, "year_month", start, end)
    if tiers:
        filtered = filtered[filtered["subscription_tier"].isin(tiers)]
    plot_df = filtered.copy()
    if "overall" in (overall_flags or []):
        overall_df = filter_date(kaq1_monthly_overall, "year_month", start, end).copy()
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

    totals = kaq1_totals[kaq1_totals["subscription_tier"].notna()].copy()
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
    filtered = filter_date(kaq2_monthly_type, "year_month", start, end)
    if types:
        filtered = filtered[filtered["content_type"].isin(types)]

    plot_df = filtered.copy()
    if "overall" in (overall_flags or []):
        overall_df = filter_date(kaq2_monthly_overall, "year_month", start, end).copy()
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

    seasonality_df = kaq2_monthly_type.copy()
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

    yearly_df = kaq2_yearly[kaq2_yearly["content_type"].notna()].copy()
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


@app.callback(
    Output("kaq3-rate", "figure"),
    Output("kaq3-volume", "figure"),
    Input("kaq3-date", "start_date"),
    Input("kaq3-date", "end_date"),
)
def update_kaq3(start: str, end: str):
    filtered = filter_date(kaq3, "signup_month", start, end)
    rate_fig = px.line(
        filtered,
        x="signup_month",
        y="activation_rate",
        markers=True,
        title="Activation rate within first 7 days",
        labels={"signup_month": "Signup Month", "activation_rate": "Activation Rate"},
    )
    rate_fig.update_layout(
        yaxis_tickformat=".0%",
        margin=dict(l=20, r=20, t=50, b=20),
        xaxis_title="Signup Month",
        yaxis_title="Activation Rate",
    )

    volume_fig = px.bar(
        filtered,
        x="signup_month",
        y=["new_users", "activated_users"],
        barmode="group",
        title="New users vs activated users",
        labels={"signup_month": "Signup Month", "value": "Users", "variable": "User Type"},
    )
    volume_fig.update_layout(
        margin=dict(l=20, r=20, t=50, b=20),
        xaxis_title="Signup Month",
        yaxis_title="Users",
        legend_title_text="User Type",
    )

    return rate_fig, volume_fig


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
    filtered = filter_date(kaq4_monthly_platform, "year_month", start, end)
    if platforms:
        filtered = filtered[filtered["platform"].isin(platforms)]

    plot_df = filtered.copy()
    if "overall" in (overall_flags or []):
        overall_df = filter_date(kaq4_monthly_overall, "year_month", start, end).copy()
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


@app.callback(
    Output("kaq5-proportion", "figure"),
    Output("kaq5-events", "figure"),
    Input("kaq5-date", "start_date"),
    Input("kaq5-date", "end_date"),
)
def update_kaq5(start: str, end: str):
    filtered = filter_date(kaq5, "year_month", start, end)
    prop_fig = px.area(
        filtered,
        x="year_month",
        y="proportion",
        color="work_mode",
        title="Share of activity by work mode",
        groupnorm="fraction",
        labels={"year_month": "Time", "work_mode": "Work Mode", "proportion": "Share"},
    )
    prop_fig.update_layout(
        legend_title_text="Work mode",
        margin=dict(l=20, r=20, t=50, b=20),
        xaxis_title="Time",
        yaxis_title="Share of Activity",
    )

    events_fig = px.bar(
        filtered,
        x="year_month",
        y="events",
        color="work_mode",
        barmode="group",
        title="Event volume by work mode",
        labels={"year_month": "Time", "work_mode": "Work Mode", "events": "Events"},
    )
    events_fig.update_layout(
        legend_title_text="Work mode",
        margin=dict(l=20, r=20, t=50, b=20),
        xaxis_title="Time",
        yaxis_title="Events",
    )

    return prop_fig, events_fig


@app.callback(
    Output("aq1-events", "figure"),
    Output("aq2-dau", "figure"),
    Output("aq2-change", "figure"),
    Input("aq1-table", "data"),
)
def update_aq1_aq2(_):
    aq1_sorted = aq1.sort_values("content_type_rank")
    aq1_fig = px.bar(
        aq1_sorted,
        x="content_type",
        y="events",
        text="content_type_rank",
        title="Total events by content type (ranked)",
        labels={"content_type": "Content Type", "events": "Events"},
    )
    aq1_fig.update_traces(textposition="outside")
    aq1_fig.update_layout(
        margin=dict(l=20, r=20, t=50, b=20),
        xaxis_title="Content Type",
        yaxis_title="Events",
    )

    dau_fig = go.Figure()
    dau_fig.add_trace(
        go.Scatter(
            x=aq2["month_start"],
            y=aq2["dau_current_month"],
            mode="lines+markers",
            name="Current month DAU",
        )
    )
    dau_fig.add_trace(
        go.Scatter(
            x=aq2["month_start"],
            y=aq2["dau_previous_month"],
            mode="lines+markers",
            name="Previous month DAU",
        )
    )
    dau_fig.update_layout(
        title="Month-over-month DAU",
        margin=dict(l=20, r=20, t=50, b=20),
        xaxis_title="Time",
        yaxis_title="Daily Active Users",
    )

    change_fig = go.Figure()
    change_fig.add_trace(
        go.Bar(x=aq2["month_start"], y=aq2["abs_change"], name="Absolute change")
    )
    change_fig.add_trace(
        go.Scatter(
            x=aq2["month_start"],
            y=aq2["rel_change"],
            mode="lines+markers",
            name="Relative change",
            yaxis="y2",
        )
    )
    change_fig.update_layout(
        title="DAU change magnitude",
        yaxis=dict(title="Absolute change"),
        yaxis2=dict(title="Relative change", overlaying="y", side="right", tickformat=".0%"),
        margin=dict(l=20, r=20, t=50, b=20),
        xaxis_title="Time",
    )

    return aq1_fig, dau_fig, change_fig


@app.callback(
    Output("overview-growth", "figure"),
    Input("aq1-table", "data"),
)
def update_overview_growth(_):
    growth_df = kaq3.sort_values("signup_month").copy()
    growth_df["cumulative_new_users"] = growth_df["new_users"].cumsum()
    growth_fig = go.Figure()
    growth_fig.add_trace(
        go.Scatter(
            x=growth_df["signup_month"],
            y=growth_df["cumulative_new_users"],
            mode="lines+markers",
            name="Cumulative new users",
        )
    )
    growth_fig.update_layout(
        title="Cumulative new users",
        margin=dict(l=20, r=20, t=50, b=20),
        xaxis_title="Time",
        yaxis_title="Cumulative New Users",
    )
    return growth_fig


if __name__ == "__main__":
    app.run(debug=False)
