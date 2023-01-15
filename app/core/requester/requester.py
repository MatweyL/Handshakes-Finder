import asyncio
import logging

import aiohttp
from aiohttp import ClientSession

from app.core.requester.data import GetFriendsQuery
from app.core.requester.errors import rebuild_queries
from app.core.requester.validator import validate
from app.utils.base import get_access_token


async def _a_get_batch(qp: GetFriendsQuery, session: ClientSession, timeout):
    requested_url = qp.get_query()
    await asyncio.sleep(timeout)
    async with session.get(requested_url) as response:
        response_json = await response.json()
        return response_json, qp


async def _a_get(qp: GetFriendsQuery):
    tasks = []
    timeout = 0
    async with aiohttp.ClientSession() as session:
        for qp_batch in qp.get_queries_params_batch():
            timeout += qp.timeout_step
            tasks.append(asyncio.create_task(_a_get_batch(qp_batch, session, timeout)))
        logging.info(f"generated: {len(tasks)} tasks; approximate time: {timeout} s")
        return await asyncio.gather(*tasks)


async def a_get(qp: GetFriendsQuery, current_retry=0, max_retries=1):
    verbose_responses = await _a_get(qp)
    valid_data, errors = validate(verbose_responses)
    current_retry += 1
    if current_retry <= max_retries:
        rebuilt_qps = rebuild_queries(errors)
        if rebuilt_qps:
            for rebuilt_qp in rebuilt_qps:
                valid_data.extend(await a_get(rebuilt_qp, current_retry, max_retries))
    return valid_data


if __name__ == "__main__":
    qp = GetFriendsQuery(
        identifiers=[288649843],
        access_token=get_access_token()
    )
    print(asyncio.run(a_get(qp)))
