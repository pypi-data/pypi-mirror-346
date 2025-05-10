import os
from pathlib import Path
from estats_client.models.client import EstatsAPIClient, StatsListParam
from estats_client.models.result_get_catalog import DataCatalogInf, GetDataCatalogResponse
import pandas as pd
import json
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=1, min=4, max=60),
    retry=retry_if_exception_type((ValueError, Exception))
)
def get_stats_list_with_retry(client: EstatsAPIClient, params: StatsListParam):
    return client.get_stats_list(params)

def get_all_catalog(client: EstatsAPIClient, file: Path, start_position=0) -> int | None:
    try:
        j = get_stats_list_with_retry(client, StatsListParam(limit=100, startPosition=start_position))
        if j['GET_DATA_CATALOG']['RESULT']['STATUS'] == 0:
            data = j['GET_DATA_CATALOG']['DATA_CATALOG_LIST_INF']['DATA_CATALOG_INF']

            with file.open("a", encoding="utf-8") as fi:
                for d in data:
                    json.dump(d, fi, ensure_ascii=False)
                    fi.write("\n")
            
            if 'NEXT_KEY' not in j['GET_DATA_CATALOG']['DATA_CATALOG_LIST_INF']['RESULT_INF']:
                return None
            
            next_key = j['GET_DATA_CATALOG']['DATA_CATALOG_LIST_INF']['RESULT_INF']['NEXT_KEY']
            return int(next_key)
        else:
            raise ValueError(j['GET_DATA_CATALOG']['RESULT']['ERROR_MSG'])
    except Exception as e:
        print(f"An error occurred: {str(e)}. Retrying...")
        raise