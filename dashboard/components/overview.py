from dash import dcc, html

from dashboard import data
from dashboard.ui import make_kpi


def build_tab() -> dcc.Tab:
    return dcc.Tab(
        label="Overview",
        className="tab",
        selected_className="tab-selected",
        children=[
            html.Div(
                className="grid-3",
                children=[
                    make_kpi(
                        "Total active users",
                        f"{int(data.kaq1_totals[data.kaq1_totals['subscription_tier'].isna()]['dau'].iloc[0]):,}",
                        "Across all months and tiers",
                    ),
                    make_kpi(
                        "Total events",
                        f"{int(data.kaq1_totals[data.kaq1_totals['subscription_tier'].isna()]['events'].iloc[0]):,}",
                        "Across all months and tiers",
                    ),
                    make_kpi(
                        "Latest activation rate",
                        f"{data.kaq3.sort_values('signup_month')['activation_rate'].iloc[-1]:.0%}",
                        "Most recent cohort",
                    ),
                    make_kpi(
                        "Latest MoM DAU change",
                        f"{data.aq2.sort_values('month_start')['rel_change'].dropna().iloc[-1]:.0%}",
                        "Relative change vs previous month",
                    ),
                ],
            ),
            html.Div(
                className="panel",
                children=[
                    html.H3("User growth overview"),
                    dcc.Graph(id="overview-growth"),
                ],
            ),
        ],
    )
