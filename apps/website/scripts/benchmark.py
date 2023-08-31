import asyncio
import random
import re
from time import time

import aiohttp
from django.conf import settings

TEXT_ROW_RE = re.compile(r"[A-Za-z]")

URL = "http://localhost:8000/share"

SHARES_PER_SECOND = 100
# STT_PER_SECONDS = 10
LOOP_DURATION = 10


headers = {"Referer": URL}


async def dummy_send_share(session, share, *args, **kwargs):
    print(share[:10], ...)


async def send_share(
    session: aiohttp.ClientSession,
    share: str,
    latitude: float = 0.0,
    longitude: float = 0.0,
    token: str = None,
    sleep: float = None,
    index: int = None,
    t_start: float = 0,
):
    data = {
        "message": share,
        "latitude": latitude if latitude else random.gauss(44.64, 1),
        "longitude": longitude if longitude else random.gauss(10.92, 1),
        "csrfmiddlewaretoken": token,
    }

    if sleep:
        await asyncio.sleep(sleep)

    t0 = time()
    async with session.post(URL, data=data, headers=headers) as response:
        assert response.status == 200
        print(
            f"{index:<5d}",
            f"{sleep:7.3f}",
            f"{(t1 := time()) - t_start:7.3f}",
            f"{(dt := (t1 - t0)):7.3f}",
            f"POST response ({response.status})",
            sep=" | ",
        )
        return dt


async def get_csrf_token(session: aiohttp.ClientSession) -> str:
    async with session.get(URL) as response:
        return response.cookies["csrftoken"].value


async def loop(shares: list[str]):
    async with aiohttp.ClientSession() as session:
        token = await get_csrf_token(session)

        t_start = time()
        tasks = []
        async with asyncio.TaskGroup() as group:
            for it in range(SHARES_PER_SECOND * LOOP_DURATION):
                share = random.choice(shares)
                sleep = random.uniform(0, LOOP_DURATION)
                task = group.create_task(
                    send_share(
                        session,
                        share=share,
                        token=token,
                        sleep=sleep,
                        t_start=t_start,
                        index=it,
                    )
                )
                tasks.append(task)

        times = [t.result() for t in tasks]
        print(
            f"max: {max(times):.3f}",
            f"min: {min(times):.3f}",
            f"mean: {sum(times) / len(times):.3f}",
            sep=" | ",
        )


def run():
    with open(settings.DEMO_SHARES_PATH, "rt") as fp:
        shares = [line for line in fp.readlines() if TEXT_ROW_RE.match(line)]

    asyncio.run(loop(shares))
