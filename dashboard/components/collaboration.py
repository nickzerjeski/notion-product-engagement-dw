from dash import dcc, html

from dashboard import data
from dashboard.ui import datatable_from_df


def build_tab() -> dcc.Tab:
    return dcc.Tab(
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
                                min_date_allowed=data.KAQ5_DATE_MIN,
                                max_date_allowed=data.KAQ5_DATE_MAX,
                                start_date=data.KAQ5_DATE_MIN,
                                end_date=data.KAQ5_DATE_MAX,
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
                    datatable_from_df(data.kaq5, "kaq5-table"),
                ],
            ),
        ],
    )
