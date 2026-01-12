import logging
import json
from datetime import datetime
from elasticsearch import Elasticsearch
from app.config import config


class ElasticsearchHandler(logging.Handler):
    def __init__(self, hosts, index_name):
        super().__init__()
        self.es = Elasticsearch(hosts)
        self.index_name = index_name

    def emit(self, record):
        try:
            doc = {
                '@timestamp': datetime.utcnow().isoformat(),
                'level': record.levelname,
                'logger': record.name,
                'message': record.getMessage(),
                'module': record.module,
                'function': record.funcName,
                'line': record.lineno
            }
            
            # Add extra fields if they exist
            if hasattr(record, 'extra_data'):
                doc['extra_data'] = record.extra_data
                
            self.es.index(index=self.index_name, body=doc)
        except Exception as e:
            # Fallback to prevent logging errors from breaking the app
            print(f"Failed to log to Elasticsearch: {e}")


class Logger:
    def __init__(self):
        self.es_host = config.ELASTICSEARCH_HOST or 'localhost'
        self.es_port = config.ELASTICSEARCH_PORT or 9200
        self.es_index = config.ELASTICSEARCH_INDEX or 'contosobank-logs'
        self.log_level = config.ELASTICSEARCH_LOG_LEVEL or 'INFO'
        self.logger = logging.getLogger("contosobank-logs")
        self.logger.setLevel(logging.DEBUG)

        # Avoid adding handlers multiple times
        if not self.logger.handlers:
            try:
                # Elasticsearch handler
                es_handler = ElasticsearchHandler(
                    hosts=[f"http://{self.es_host}:{self.es_port}"],
                    index_name=self.es_index
                )
                es_handler.setLevel(getattr(logging, self.log_level.split('.')[-1]))
                self.logger.addHandler(es_handler)
            except Exception as e:
                print(f"Failed to connect to Elasticsearch: {e}")

            # Console handler
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.DEBUG)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)


logger = Logger().logger


