import json
from pathlib import Path

from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from estats_client.client import EstatsAPIClient, StatsListParam
from estats_client.models.result_get_catalog import (
    GetDataCatalogResponse,
)


@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=1, min=4, max=60),
    retry=retry_if_exception_type((ValueError, Exception)),
)
def get_stats_list_with_retry(client: EstatsAPIClient, params: StatsListParam):
    return client.get_stats_list(params)


def get_all_catalog(
    client: EstatsAPIClient, file: Path, start_position=0
) -> int | None:
    try:
        response_model: GetDataCatalogResponse = get_stats_list_with_retry(
            client, StatsListParam(limit=100, startPosition=start_position)
        )

        if response_model.get_data_catalog.result.status == 0:
            data = (
                response_model.get_data_catalog.data_catalog_list_inf.data_catalog_inf
            )

            with file.open("a", encoding="utf-8") as fi:
                for d_item in data:
                    json_string = json.dumps(d_item.model_dump(), ensure_ascii=False)
                    fi.write(json_string)
                    fi.write("\n")

            if (
                response_model.get_data_catalog.data_catalog_list_inf.result_inf.next_key
                is None
            ):
                return None

            next_key = response_model.get_data_catalog.data_catalog_list_inf.result_inf.next_key
            return int(next_key)
        else:
            raise ValueError(response_model.get_data_catalog.result.error_msg)
    except Exception as e:
        print(f"An error occurred: {str(e)}. Retrying...")
        raise
