import plotly.express as px
from dash import Input, Output

from dashboard import data


def register(app) -> None:
    @app.callback(
        Output("kaq3-rate", "figure"),
        Output("kaq3-volume", "figure"),
        Input("kaq3-date", "start_date"),
        Input("kaq3-date", "end_date"),
    )
    def update_kaq3(start: str, end: str):
        filtered = data.filter_date(data.kaq3, "signup_month", start, end)
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
