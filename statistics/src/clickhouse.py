from clickhouse_driver import Client
from config import settings


ch_client = Client(settings.ch_host)
