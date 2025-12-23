from dash import dcc, html

from dashboard import data
from dashboard.ui import datatable_from_df


def build_tab() -> dcc.Tab:
    return dcc.Tab(
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
                                min_date_allowed=data.KAQ3_DATE_MIN,
                                max_date_allowed=data.KAQ3_DATE_MAX,
                                start_date=data.KAQ3_DATE_MIN,
                                end_date=data.KAQ3_DATE_MAX,
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
                    datatable_from_df(data.kaq3, "kaq3-table"),
                ],
            ),
        ],
    )
