from prometheus_client import start_http_server, Summary
import random
import time
from prometheus_client.core import GaugeMetricFamily, CounterMetricFamily, REGISTRY
import mysql.connector
from mysql.connector import Error

connection = mysql.connector.connect(host='localhost',
                                         database='demo',
                                         user='root',
                                         password='V@ibhav02')
sql_select_Query = "select count from billing where Region = 'US' and CAT_CODE = 1"
cursor = connection.cursor()
cursor.execute(sql_select_Query)
records = cursor.fetchall()

# Create a metric to track time spent and requests made.
REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')

# Decorate function with metric.
@REQUEST_TIME.time()
def process_request(t):
    """A dummy function that takes some time."""
    time.sleep(t)

class CustomCollector(object):
    def collect(self):
        c = CounterMetricFamily('usa_success_day01', 'Successful billings in US on day 0')
        c.add_metric(['us_success_day01'], records[0][0])
        yield c

REGISTRY.register(CustomCollector())

if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(8000)
    # Generate some requests.
    while True:
        process_request(random.random())
