from dash import dcc, html

from dashboard import data
from dashboard.ui import datatable_from_df


def build_tab() -> dcc.Tab:
    return dcc.Tab(
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
                                    for tier in sorted(data.kaq1_monthly_tier["subscription_tier"].unique())
                                ],
                                value=sorted(data.kaq1_monthly_tier["subscription_tier"].unique()),
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
                                min_date_allowed=data.KAQ1_DATE_MIN,
                                max_date_allowed=data.KAQ1_DATE_MAX,
                                start_date=data.KAQ1_DATE_MIN,
                                end_date=data.KAQ1_DATE_MAX,
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
                    datatable_from_df(data.kaq1, "kaq1-table"),
                ],
            ),
        ],
    )
