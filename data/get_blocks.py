from datetime import timedelta
import json
from ratelimit import limits, sleep_and_retry
from opnieuw import retry, RetryException
from secret_tokens.etherscan import api_token
from pathlib import Path
from requests.exceptions import ConnectionError, HTTPError
import requests
from tqdm import tqdm
from typing import Dict


@retry(retry_on_exceptions=(ConnectionError, HTTPError, RetryException),
       retry_window_after_first_call_in_seconds=600)
@sleep_and_retry
@limits(calls=4, period=timedelta(seconds=1).total_seconds())
def query_block(block_number: int) -> Dict:
    base_url = 'https://api.etherscan.io/api'
    params = {'module': 'proxy',
              'action': 'eth_getBlockByNumber',
              'boolean': 'false',
              'apikey': api_token,
              'tag': hex(block_number)}
    response = requests.get(base_url, params=params)
    response.raise_for_status()
    result = response.json()['result']
    if not isinstance(result, dict):
        raise RetryException
    return result


def write_block(block_number: int, fp: Path):
    block = query_block(block_number)
    with fp.joinpath(f'block_{block_number}.json').open('w') as f:
        json.dump(block, f)


def get_block_range(from_block: int, to_block: int, write_to: Path) -> None:
    for i in tqdm(range(from_block, to_block)):
        write_block(i, write_to)


merge_block = 15537393
post_merge_block = 15599189
pre_merge_block = 2 * merge_block - post_merge_block

get_block_range(pre_merge_block, post_merge_block, write_to=Path('../static/block_data'))

