from dash import dcc, html

from dashboard.components import (
    activation,
    additional_queries,
    collaboration,
    content_types,
    device_impact,
    engagement_tier,
    overview,
)


def build_layout() -> html.Div:
    return html.Div(
        className="page",
        children=[
            dcc.Tabs(
                className="tabs",
                children=[
                    overview.build_tab(),
                    engagement_tier.build_tab(),
                    content_types.build_tab(),
                    activation.build_tab(),
                    device_impact.build_tab(),
                    collaboration.build_tab(),
                    additional_queries.build_tab(),
                ],
            ),
        ],
    )
