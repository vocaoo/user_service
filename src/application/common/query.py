from abc import ABC

from didiator import QueryHandler as DQueryHandler, Query as DQuery


class Query[QRes](DQuery, ABC):
    pass


class QueryHandler[Q, QRes](DQueryHandler, ABC):
    pass
