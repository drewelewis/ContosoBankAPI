import logging
from elasticsearch import RequestsHttpConnection
from cmreslogging.handlers import CMRESHandler
from app.config import config


class Logger:
    
    def __init__(self):
        self.es_host=config.ELASTICSEARCH_HOST
        self.es_port=config.ELASTICSEARCH_PORT
        self.es_index=config.ELASTICSEARCH_INDEX
        self.log_level=config.ELASTICSEARCH_LOG_LEVEL
        self.logger = logging.getLogger("contosobank-logs")
        self.logger.setLevel(logging.DEBUG)


        # Avoid adding handlers multiple times
        if not self.logger.handlers:
            # Elasticsearch handler
            es_handler = CMRESHandler(
                hosts=[{'host': self.es_host, 'port': self.es_port}],
                auth_type=CMRESHandler.AuthType.NO_AUTH,
                es_index_name=self.es_index
            )
            self.logger.addHandler(es_handler)

            # Console handler
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.DEBUG)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

logger=Logger().logger


