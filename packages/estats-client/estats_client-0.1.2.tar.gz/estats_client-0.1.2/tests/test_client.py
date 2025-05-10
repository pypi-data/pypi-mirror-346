import pytest
import json
import os
from dotenv import load_dotenv
from estats_client import ( # トップレベルからインポート
    EstatsAPIClient,
    StatsDataParam,
    GetStatsDataResponse,
)

# .envファイルから環境変数を読み込む
load_dotenv()

# 環境変数からAPP_IDを取得
APP_ID = os.getenv("APP_ID")

# APP_IDが設定されていない場合はエラーとする
if APP_ID is None:
    raise ValueError("環境変数 APP_ID が設定されていません。.envファイルを確認してください。")


def test_get_stats_data_success():
    """
    get_stats_data APIを呼び出し、正常なレスポンスが返ることを確認するテスト。
    """
    client = EstatsAPIClient(app_id=APP_ID)
    params = StatsDataParam(statsDataId="0003173901")

    try:
        # クライアントメソッドが直接Pydanticモデルを返すようになった
        response_model: GetStatsDataResponse = client.get_stats_data(params=params)

        # APIの仕様に基づき、RESULT.STATUSが0であることを確認
        assert response_model.get_stats_data.result.status == 0, \
            f"API Error: {response_model.get_stats_data.result.error_msg}"

        # データが取得できていることを確認（例: VALUEのリストが空でないこと）
        assert len(response_model.get_stats_data.statistical_data.data_inf.value) > 0, \
            "No data values returned"

        print("API Response:")
        # model_dump()で辞書に変換し、json.dumpsでensure_ascii=Falseを指定してJSON文字列に変換
        print(json.dumps(response_model.model_dump(), indent=2, ensure_ascii=False))

    except Exception as e:
        pytest.fail(f"API request failed: {e}")