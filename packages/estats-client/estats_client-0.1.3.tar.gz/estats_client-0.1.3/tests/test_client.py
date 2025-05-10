import json
import os

import pytest
from dotenv import load_dotenv

from estats_client import (
    EstatsAPIClient,
    GetStatsDataResponse,
    StatsDataParam,
)

load_dotenv()

APP_ID = os.getenv("APP_ID")

if APP_ID is None:
    raise ValueError(
        "環境変数 APP_ID が設定されていません。.envファイルを確認してください。"
    )


def test_get_stats_data_success():
    """get_stats_data APIを呼び出し、正常なレスポンスが返ることを確認するテスト。
    """
    client = EstatsAPIClient(app_id=APP_ID)
    params = StatsDataParam(statsDataId="0003173901")

    try:
        response_model: GetStatsDataResponse = client.get_stats_data(params=params)

        assert response_model.get_stats_data.result.status == 0, (
            f"API Error: {response_model.get_stats_data.result.error_msg}"
        )

        assert len(response_model.get_stats_data.statistical_data.data_inf.value) > 0, (
            "No data values returned"
        )

        print("API Response:")
        print(json.dumps(response_model.model_dump(), indent=2, ensure_ascii=False))

    except Exception as e:
        pytest.fail(f"API request failed: {e}")
