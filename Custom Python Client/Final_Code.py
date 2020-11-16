import cx_Oracle as co
from prometheus_client import start_http_server, Summary
import random
import time
from prometheus_client.core import GaugeMetricFamily, REGISTRY


# Oracle
conn = co.connect('hr/hr@localhost:1521/orcl')
curr = conn.cursor()
query = "select success from invoice_delivery_monitor where region = 'US' and billing_date = '01-JUL-20' and day=1"
curr.execute(query)
result = curr.fetchall()


#CustomCollector
REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')


@REQUEST_TIME.time()
def process_request(t):
    """A dummy function that takes some time."""
    time.sleep(t)

class CustomCollector(object):
    def collect(self):
        c = GaugeMetricFamily('usa_failure_burndown', 'Successful billings in US on 1st July')
        c.add_metric(['us_failure_burndown'],0)
        yield c

REGISTRY.register(CustomCollector())

if __name__ == '__main__':
    start_http_server(8000)
    while True:
        process_request(random.random())
