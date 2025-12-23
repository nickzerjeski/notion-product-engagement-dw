import plotly.graph_objects as go
from dash import Input, Output

from dashboard import data


def register(app) -> None:
    @app.callback(
        Output("overview-growth", "figure"),
        Input("aq1-table", "data"),
    )
    def update_overview_growth(_):
        growth_df = data.kaq3.sort_values("signup_month").copy()
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
