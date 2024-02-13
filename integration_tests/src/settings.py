from db_contractor.db_connect import DBConnect
from log.app import Logger

logger = Logger(service_name='integration-tests-db-lib', log_level='debug')
logger.log_to_logstash(host="0.0.0.0", port=6004, logstash_network='udp')

processing_connect = DBConnect(host="0.0.0.0", port="5432", db_name="name",
                               username="generatorfortests", password="123", logger=logger)

