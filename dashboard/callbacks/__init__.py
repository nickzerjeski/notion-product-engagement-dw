
from dashboard.callbacks import (
    additional_queries,
    kaq1,
    kaq2,
    kaq3,
    kaq4,
    kaq5,
    overview,
)


def register_all(app) -> None:
    overview.register(app)
    kaq1.register(app)
    kaq2.register(app)
    kaq3.register(app)
    kaq4.register(app)
    kaq5.register(app)
    additional_queries.register(app)
