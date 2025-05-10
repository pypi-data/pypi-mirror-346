# estats-client

[![PyPI version](https://badge.fury.io/py/estats-client.svg)](https://badge.fury.io/py/estats-client)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Versions](https://img.shields.io/pypi/pyversions/estats-client.svg)](https://pypi.org/project/estats-client/)
[![Build Status](https://github.com/RAKUDEJI/estats-client/actions/workflows/build-artifacts.yml/badge.svg)](https://github.com/RAKUDEJI/estats-client/actions/workflows/build-artifacts.yml)

`estats-client` は、日本の[政府統計の総合窓口 (e-Stat)](https://www.e-stat.go.jp/) APIを利用するためのPythonクライアントライブラリです。
e-Stat APIから統計データを簡単に取得し、Pydanticモデルとして利用することができます。

## 主な機能

-   統計表情報取得 (`getStatsList`)
-   統計データ取得 (`getStatsData`)
-   レスポンスデータをPydanticモデルにパース
-   シンプルなAPIインターフェース

## インストール

PyPIからインストールできます（公開後）:
```bash
pip install estats-client
```

## 必要なもの

-   **e-Stat API アプリケーションID (appId)**:
    e-Stat APIを利用するには、[e-Statのウェブサイト](https://www.e-stat.go.jp/api/api-dev/)で利用者登録を行い、アプリケーションIDを取得する必要があります。

##基本的な使い方

### 環境変数の設定
取得したアプリケーションIDは、環境変数 `ESTATS_APP_ID` に設定するか、クライアント初期化時に直接渡すことができます。
プロジェクトルートに `.env` ファイルを作成して管理することも可能です（ライブラリ利用時は環境変数推奨）。
```
ESTATS_APP_ID="YOUR_APP_ID_HERE"
```

### クライアントの初期化とデータ取得

```python
import os
from dotenv import load_dotenv
from estats_client.models.client import EstatsAPIClient, StatsDataParam, StatsListParam
from estats_client.models.result import GetStatsDataResponse
from estats_client.models.result_get_catalog import GetDataCatalogResponse

# .envファイルから環境変数を読み込む (ローカル開発用)
load_dotenv()

APP_ID = os.getenv("ESTATS_APP_ID")

if not APP_ID:
    raise ValueError("環境変数 ESTATS_APP_ID が設定されていません。")

# クライアントの初期化
client = EstatsAPIClient(app_id=APP_ID)

# --- 統計表情報取得 (getStatsList) の例 ---
try:
    list_params = StatsListParam(searchWord="経済センサス", limit=1)
    response_json_list = client.get_stats_list(params=list_params)
    stats_list_response = GetDataCatalogResponse(**response_json_list)

    if stats_list_response.get_data_catalog.result.status == 0:
        print("統計表情報取得 成功:")
        for catalog_info in stats_list_response.get_data_catalog.data_catalog_list_inf.data_catalog_inf:
            print(f"  ID: {catalog_info.id}")
            print(f"  統計名: {catalog_info.dataset.stat_name.value}")
            print(f"  表題: {catalog_info.dataset.title.name}")
            # 必要に応じて他の情報も表示
    else:
        print(f"統計表情報取得 エラー: {stats_list_response.get_data_catalog.result.error_msg}")

except Exception as e:
    print(f"統計表情報取得中にエラーが発生しました: {e}")


# --- 統計データ取得 (getStatsData) の例 ---
try:
    data_params = StatsDataParam(statsDataId="0003173901") # 例: 航空輸送統計調査
    response_json_data = client.get_stats_data(params=data_params)
    stats_data_response = GetStatsDataResponse(**response_json_data)

    if stats_data_response.get_stats_data.result.status == 0:
        print("\\n統計データ取得 成功:")
        print(f"  統計名: {stats_data_response.get_stats_data.statistical_data.table_inf.statistics_name}")
        print(f"  取得データ件数: {len(stats_data_response.get_stats_data.statistical_data.data_inf.value)}")
        # 最初のいくつかのデータを表示
        for i, value_data in enumerate(stats_data_response.get_stats_data.statistical_data.data_inf.value[:3]):
            print(f"    データ{i+1}: Time={value_data.time}, Value={value_data.value}")
    else:
        print(f"統計データ取得 エラー: {stats_data_response.get_stats_data.result.error_msg}")

except Exception as e:
    print(f"統計データ取得中にエラーが発生しました: {e}")

```

## 開発

### セットアップ
このリポジトリをクローンし、[Rye](https://rye-up.com/) を使って開発環境をセットアップします。
```bash
git clone https://github.com/RAKUDEJI/estats-client.git
cd estats-client
rye sync
```

### テスト
テストはpytestを使用して実行します。
```bash
rye run pytest
```
テストを実行する前に、プロジェクトルートに `.env` ファイルを作成し、`APP_ID="YOUR_TEST_APP_ID"` のようにテスト用のアプリケーションIDを設定してください。

## ライセンス
このプロジェクトはMITライセンスのもとで公開されています。詳細は `LICENSE` ファイル（もしあれば）または `pyproject.toml` をご覧ください。

## コントリビューション
バグ報告、機能リクエスト、プルリクエストを歓迎します。Issueを作成するか、プルリクエストを送ってください。
