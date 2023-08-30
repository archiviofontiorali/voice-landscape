import random
import re
from time import time

import requests
from django.conf import settings

TEXT_ROW_RE = re.compile(r"[A-Za-z]")


N_SAMPLES = 10
SHARES_PER_ITER = 10


def run():
    with open(settings.DEMO_SHARES_PATH, "rt") as fp:
        shares = [line for line in fp.readlines() if TEXT_ROW_RE.match(line)]

    url = "http://localhost:8000/share"

    client = requests.session()
    client.get(url)
    token = client.cookies.get("csrftoken")
    headers = {"Referer": url}

    for it in range(N_SAMPLES):
        t_total = 0.0
        w_total = 0

        for share in random.choices(shares, k=SHARES_PER_ITER):
            t_start = time()
            response = client.post(
                url,
                {
                    "message": share,
                    "latitude": "0.",
                    "longitude": "0.",
                    "csrfmiddlewaretoken": token,
                },
                headers=headers,
            )
            t_total += time() - t_start
            w_total += len(share)

            if response.status_code != 200:
                raise Exception(response.status_code)

        print(f"{it:5d}", f"time: {t_total:7.03f}", f"chars: {w_total}", sep=" | ")
