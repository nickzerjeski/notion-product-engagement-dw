from dash import dcc, html

from dashboard import data
from dashboard.ui import datatable_from_df


def build_tab() -> dcc.Tab:
    return dcc.Tab(
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
                                    for t in sorted(data.kaq2_monthly_type["content_type"].unique())
                                ],
                                value=sorted(data.kaq2_monthly_type["content_type"].unique()),
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
                                min_date_allowed=data.KAQ2_DATE_MIN,
                                max_date_allowed=data.KAQ2_DATE_MAX,
                                start_date=data.KAQ2_DATE_MIN,
                                end_date=data.KAQ2_DATE_MAX,
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
                    datatable_from_df(data.kaq2, "kaq2-table"),
                ],
            ),
        ],
    )
