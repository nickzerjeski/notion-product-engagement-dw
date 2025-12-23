from dash import dcc, html

from dashboard import data
from dashboard.ui import datatable_from_df


def build_tab() -> dcc.Tab:
    return dcc.Tab(
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
                                    for p in sorted(data.kaq4_monthly_platform["platform"].unique())
                                ],
                                value=sorted(data.kaq4_monthly_platform["platform"].unique()),
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
                                min_date_allowed=data.KAQ4_DATE_MIN,
                                max_date_allowed=data.KAQ4_DATE_MAX,
                                start_date=data.KAQ4_DATE_MIN,
                                end_date=data.KAQ4_DATE_MAX,
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
                    datatable_from_df(data.kaq4, "kaq4-table"),
                ],
            ),
        ],
    )
