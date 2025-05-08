from abc import ABC

from fianchetto_tradebot.common.brokerage.connector import Connector


class ApiService(ABC):
    def __init__(self, connector: Connector):
        self.connector = connector