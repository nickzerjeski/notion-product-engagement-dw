from __future__ import annotations

from dash import dash_table, html

import pandas as pd


def datatable_from_df(df: pd.DataFrame, table_id: str) -> dash_table.DataTable:
    return dash_table.DataTable(
        id=table_id,
        columns=[{"name": col, "id": col} for col in df.columns],
        data=df.to_dict("records"),
        page_size=12,
        style_table={"overflowX": "auto"},
        style_cell={
            "padding": "6px",
            "fontFamily": "var(--font-body)",
            "fontSize": "13px",
            "whiteSpace": "normal",
        },
        style_header={"fontWeight": "600", "backgroundColor": "#f2f2f2"},
    )


def make_kpi(label: str, value: str, hint: str | None = None) -> html.Div:
    return html.Div(
        [
            html.Div(label, className="kpi-label"),
            html.Div(value, className="kpi-value"),
            html.Div(hint or "", className="kpi-hint"),
        ],
        className="kpi-card",
    )
