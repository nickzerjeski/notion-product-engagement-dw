import plotly.express as px
import plotly.graph_objects as go
from dash import Input, Output

from dashboard import data


def register(app) -> None:
    @app.callback(
        Output("aq1-events", "figure"),
        Output("aq2-dau", "figure"),
        Output("aq2-change", "figure"),
        Input("aq1-table", "data"),
    )
    def update_aq1_aq2(_):
        aq1_sorted = data.aq1.sort_values("content_type_rank")
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
                x=data.aq2["month_start"],
                y=data.aq2["dau_current_month"],
                mode="lines+markers",
                name="Current month DAU",
            )
        )
        dau_fig.add_trace(
            go.Scatter(
                x=data.aq2["month_start"],
                y=data.aq2["dau_previous_month"],
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
            go.Bar(x=data.aq2["month_start"], y=data.aq2["abs_change"], name="Absolute change")
        )
        change_fig.add_trace(
            go.Scatter(
                x=data.aq2["month_start"],
                y=data.aq2["rel_change"],
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
