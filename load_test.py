"""
Load-test the lambda function by sending {N_REQUESTS} requests in a very short space of time
"""

import concurrent.futures
import datetime
import json
import logging
import os
import random
import sys
from typing import Iterator
import uuid

import requests

from generate_random_datetime import generate_random_datetime

N_REQUESTS: int = int(sys.argv[1])

# set up python logger #
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def send_request(_):
    response = requests.post(
        url=os.environ["AWS_LAMBDA_URL"],
        json={
                "datetime": generate_random_datetime(
                    start=datetime.datetime(2024, 1, 1, 0, 0, 0),
                    end=datetime.datetime(2025, 1, 1, 0, 0, 0),
                    ).strftime("%Y-%m-%d %H:%M:%S"),
                "send_id": uuid.uuid4().hex,
                "event": random.choice(["delivered","hard bounce", "open", "click", "complaint"]) ,
        },
        timeout=60,
    )
    return (response.status_code, response.text)

response_hist = {}
response_text_hist = {}

if __name__ == "__main__":
    logger.info("started sending requests")
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results: Iterator = executor.map(
            send_request, range(N_REQUESTS) 
        )
    for result in results:
        if str(result) not in response_hist:
            response_hist[str(result)] = 0
        response_hist[str(result)] += 1
    logger.info("finished sending requests")
    logger.info(json.dumps(response_hist, indent=4))
