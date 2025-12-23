from dash import dcc, html

from dashboard import data
from dashboard.ui import datatable_from_df


def build_tab() -> dcc.Tab:
    return dcc.Tab(
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
                    datatable_from_df(data.aq1, "aq1-table"),
                ],
            ),
            html.Details(
                className="data-details",
                children=[
                    html.Summary("View AQ2 raw data"),
                    datatable_from_df(data.aq2, "aq2-table"),
                ],
            ),
        ],
    )
