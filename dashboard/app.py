from __future__ import annotations

import sys
from pathlib import Path

import plotly.io as pio
from dash import Dash

if __package__ in (None, ""):
    sys.path.append(str(Path(__file__).resolve().parent.parent))

from dashboard.callbacks import register_all
from dashboard.layout import build_layout

pio.templates.default = "plotly_white"

app = Dash(__name__, title="Notion Engagement Dashboard")
server = app.server

app.layout = build_layout()
register_all(app)


if __name__ == "__main__":
    app.run(debug=False)
