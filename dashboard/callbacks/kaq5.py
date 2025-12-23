import plotly.express as px
from dash import Input, Output

from dashboard import data


def register(app) -> None:
    @app.callback(
        Output("kaq5-proportion", "figure"),
        Output("kaq5-events", "figure"),
        Input("kaq5-date", "start_date"),
        Input("kaq5-date", "end_date"),
    )
    def update_kaq5(start: str, end: str):
        filtered = data.filter_date(data.kaq5, "year_month", start, end)
        prop_fig = px.area(
            filtered,
            x="year_month",
            y="proportion",
            color="work_mode",
            title="Share of activity by work mode",
            groupnorm="fraction",
            labels={"year_month": "Time", "work_mode": "Work Mode", "proportion": "Share"},
        )
        prop_fig.update_layout(
            legend_title_text="Work mode",
            margin=dict(l=20, r=20, t=50, b=20),
            xaxis_title="Time",
            yaxis_title="Share of Activity",
        )

        events_fig = px.bar(
            filtered,
            x="year_month",
            y="events",
            color="work_mode",
            barmode="group",
            title="Event volume by work mode",
            labels={"year_month": "Time", "work_mode": "Work Mode", "events": "Events"},
        )
        events_fig.update_layout(
            legend_title_text="Work mode",
            margin=dict(l=20, r=20, t=50, b=20),
            xaxis_title="Time",
            yaxis_title="Events",
        )

        return prop_fig, events_fig
