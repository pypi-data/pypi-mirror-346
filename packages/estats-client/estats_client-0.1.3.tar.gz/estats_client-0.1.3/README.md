# estats-client

[![PyPI version](https://badge.fury.io/py/estats-client.svg)](https://badge.fury.io/py/estats-client)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Versions](https://img.shields.io/pypi/pyversions/estats-client.svg)](https://pypi.org/project/estats-client/)
[![Build Status](https://github.com/RAKUDEJI/estats-client/actions/workflows/build-artifacts.yml/badge.svg)](https://github.com/RAKUDEJI/estats-client/actions/workflows/build-artifacts.yml)
[![Test and Publish Status](https://github.com/RAKUDEJI/estats-client/actions/workflows/publish-to-pypi.yml/badge.svg)](https://github.com/RAKUDEJI/estats-client/actions/workflows/publish-to-pypi.yml)

`estats-client` は、日本の[政府統計の総合窓口 (e-Stat)](https://www.e-stat.go.jp/) の公式APIを利用するための、使いやすいPythonクライアントライブラリです。
このライブラリを使用することで、e-Statが提供する豊富な統計データへ簡単にアクセスし、取得したデータを型安全なPydanticモデルとして扱うことができます。これにより、データ分析やアプリケーション開発における統計データの取り扱いが大幅に簡素化されます。

## 目次
- [主な機能](#主な機能)
- [インストール](#インストール)
- [必要なもの](#必要なもの)
- [基本的な使い方](#基本的な使い方)
  - [アプリケーションIDの設定](#アプリケーションidの設定)
  - [クライアントの初期化](#クライアントの初期化)
  - [統計表情報リストの取得 (`get_stats_list`)](#統計表情報リストの取得-get_stats_list)
  - [統計データの取得 (`get_stats_data`)](#統計データの取得-get_stats_data)
  - [エラーハンドリング](#エラーハンドリング)
- [Pydanticモデルについて](#pydanticモデルについて)
- [開発](#開発)
  - [セットアップ](#セットアップ)
  - [テスト](#テスト)
- [ライセンス](#ライセンス)
- [コントリビューション](#コントリビューション)

## 主な機能

-   **統計表情報リスト取得**: キーワードや調査年などで統計表を検索し、メタ情報をリストで取得します (`get_stats_list` APIに対応)。
-   **統計データ取得**: 指定した統計表IDに基づいて、実際の統計データを取得します (`get_stats_data` APIに対応)。
-   **Pydanticによる型安全なレスポンス**: APIレスポンスはPydanticモデルにパースされるため、データの構造が明確になり、型ヒントによる開発支援や実行時のデータバリデーションの恩恵を受けられます。
-   **シンプルなAPIインターフェース**: 直感的に利用できるメソッドを提供します。
-   **再試行メカニズム**: ネットワークエラーなど一時的な問題に対応するため、一部の処理（カタログ取得など）にはリトライ機能が組み込まれています。

## インストール

PyPIから最新バージョンをインストールできます:
```bash
pip install estats-client
```

## 必要なもの

-   **e-Stat API アプリケーションID (appId)**:
    e-Stat APIを利用するには、まず[e-StatのAPI利用者登録ページ](https://www.e-stat.go.jp/api/api-dev/)で利用者登録を行い、アプリケーションIDを取得する必要があります。このIDはAPIリクエスト時に必須となります。

## 基本的な使い方

### アプリケーションIDの設定
取得したアプリケーションIDは、環境変数 `ESTATS_APP_ID` に設定することを推奨します。ライブラリは自動的にこの環境変数を参照します。
または、クライアント初期化時に `app_id`引数として直接渡すことも可能です。

ローカル環境で開発を行う場合など、プロジェクトルートに `.env` ファイルを作成してアプリケーションIDを管理することも可能です。
```env
ESTATS_APP_ID="YOUR_APP_ID_HERE"
```
この場合、`python-dotenv` ライブラリを利用して環境変数を読み込むことができます。
ただし、ライブラリの利用者としては、環境変数 `ESTATS_APP_ID` を直接設定するか、クライアント初期化時に `app_id` 引数で明示的に指定する方法が一般的です。

### クライアントの初期化
```python
import os
# from dotenv import load_dotenv # .envファイルを使用する場合にコメントを解除
from estats_client import (
    EstatsAPIClient,
    # StatsListParam, # get_stats_list の例で使用
    # StatsDataParam, # get_stats_data の例で使用
    # GetDataCatalogResponse, # get_stats_list の例で使用
    # GetStatsDataResponse, # get_stats_data の例で使用
    # 必要に応じて他のモデルもインポート
)

# .env ファイルを利用して環境変数を読み込む場合は、python-dotenv をインストールし、
# 以下の行のコメントを解除してください。
# load_dotenv()

# 環境変数からAPP_IDを取得 (推奨)
app_id = os.getenv("ESTATS_APP_ID")

if not app_id:
    # app_id = "YOUR_APP_ID_FALLBACK" # またはここで直接指定
    raise ValueError("環境変数 ESTATS_APP_ID が設定されていません。クライアント初期化時に app_id を指定してください。")

client = EstatsAPIClient(app_id=app_id)
```

### 統計表情報リストの取得 (`get_stats_list`)
```python
from estats_client import StatsListParam, GetDataCatalogResponse # トップレベルからインポート

# client は前のセクションで初期化済みとします
# from estats_client import EstatsAPIClient
# import os
# APP_ID = os.getenv("ESTATS_APP_ID")
# client = EstatsAPIClient(app_id=APP_ID)


try:
    params = StatsListParam(
        searchWord="国勢調査",
        statsField="02000000", # 例: 人口・世帯
        limit=2
    )
    # クライアントメソッドが直接Pydanticモデルを返す
    stats_list_response: GetDataCatalogResponse = client.get_stats_list(params=params)

    if stats_list_response.get_data_catalog.result.status == 0:
        print("統計表情報リスト取得 成功:")
        for catalog in stats_list_response.get_data_catalog.data_catalog_list_inf.data_catalog_inf:
            print(f"  ID: {catalog.id}")
            print(f"  統計名: {catalog.dataset.stat_name.value}")
            print(f"  表題: {catalog.dataset.title.name}")
            print("-" * 20)
    else:
        print(f"エラー: {stats_list_response.get_data_catalog.result.error_msg}")

except Exception as e: # requests.exceptions.HTTPError など、より具体的な例外を補足することも可能
    print(f"APIリクエスト中にエラーが発生しました: {e}")
```

### 統計データの取得 (`get_stats_data`)
```python
from estats_client import StatsDataParam, GetStatsDataResponse # トップレベルからインポート

# client は前のセクションで初期化済みとします

# 上記で取得した統計表IDなどを利用
stats_data_id_example = "0003410379" # 例: 令和２年国勢調査 人口等基本集計

try:
    params = StatsDataParam(statsDataId=stats_data_id_example, limit=5)
    # クライアントメソッドが直接Pydanticモデルを返す
    stats_data_response: GetStatsDataResponse = client.get_stats_data(params=params)

    if stats_data_response.get_stats_data.result.status == 0:
        print(f"\\n統計データ取得 成功: {stats_data_response.get_stats_data.statistical_data.table_inf.title.value}")
        for value_info in stats_data_response.get_stats_data.statistical_data.data_inf.value:
            # 各種カテゴリ名を取得するには、CLASS_INFを参照する必要があります
            # ここでは簡略化のため、時間と値のみ表示
            print(f"  時間: {value_info.time}, 値: {value_info.value} ({value_info.unit})")
    else:
        print(f"エラー: {stats_data_response.get_stats_data.result.error_msg}")

except Exception as e:
    print(f"APIリクエスト中にエラーが発生しました: {e}")
```

### エラーハンドリング
`_make_request` メソッド内で `response.raise_for_status()` が呼ばれるため、APIがエラーレスポンス (4xx, 5xx) を返した場合、`requests.exceptions.HTTPError` が発生します。
また、e-Stat API自体が正常レスポンス (200 OK) 内にエラーステータスを含める場合があるため、レスポンス内の `RESULT.STATUS` も確認することが重要です。

```python
import requests

try:
    # ... API呼び出し ...
    pass
except requests.exceptions.HTTPError as http_err:
    print(f"HTTPエラーが発生しました: {http_err}")
    print(f"レスポンスボディ: {http_err.response.text}")
except requests.exceptions.RequestException as req_err:
    print(f"リクエスト関連のエラーが発生しました: {req_err}")
except Exception as e:
    print(f"予期せぬエラーが発生しました: {e}")
```

## Pydanticモデルについて
このライブラリは、e-Stat APIからのJSONレスポンスをPydanticモデルに変換します。これにより以下のメリットがあります。
-   **データ構造の明確化**: APIレスポンスの複雑な構造が、Pythonのクラスとして明確に定義されます。
-   **型安全性**: エディタやIDEによる型ヒントの補完が効き、開発効率が向上します。また、実行時に期待しないデータ型が渡された場合にエラーを発生させ、バグの早期発見に繋がります。
-   **データバリデーション**: Pydanticが自動的にデータの型や制約（必須項目など）を検証します。

各APIレスポンスに対応するPydanticモデルは `estats_client` パッケージから直接インポートできます (例: `from estats_client import GetStatsDataResponse`)。
内部的には `estats_client.models.result` および `estats_client.models.result_get_catalog` モジュールで定義されています。

## 開発 (コントリビューター向け)

### セットアップ
このライブラリの開発に貢献したい場合は、以下の手順で開発環境をセットアップできます。
このリポジトリをクローンし、[Rye](https://rye-up.com/) を使って開発環境をセットアップします。
```bash
git clone https://github.com/RAKUDEJI/estats-client.git
cd estats-client
rye sync
```

### テスト
テストは `pytest` を使用して実行します。
```bash
rye run pytest
```
テストを実行する前に、プロジェクトルートに `.env` ファイルを作成し、テスト用のアプリケーションIDを `ESTATS_APP_ID_FOR_TESTS` という名前の環境変数として設定してください。
```env
ESTATS_APP_ID_FOR_TESTS="YOUR_TEST_APP_ID_HERE"
```
この環境変数は、CI環境ではGitHubリポジトリのSecretsから設定されます。

## リリース手順

このライブラリを新しいバージョンとしてPyPIに公開するには、以下の手順を実行します。
リリースはGitHub Actions経由で自動的に行われます。

1.  **バージョン番号の更新**:
    *   `src/estats_client/__init__.py` ファイル内の `__version__` 変数を新しいバージョン番号（例: `0.1.3`）に更新します。
    *   `pyproject.toml` ファイル内の `version` フィールドを同じ新しいバージョン番号に更新します。

2.  **変更のコミットとプッシュ**:
    *   すべての変更（機能追加、バグ修正、バージョン番号の更新など）をGitリポジトリにコミットします。
    *   変更をリモートリポジトリ（例: `origin main`）にプッシュします。
        ```bash
        git add .
        git commit -m "Release v0.1.3" # コミットメッセージは適宜変更
        git push origin main
        ```

3.  **Gitタグの作成とプッシュ**:
    *   新しいバージョンに対応するGitタグを作成します。タグ名は `v` + バージョン番号（例: `v0.1.3`）とします。
    *   作成したタグをリモートリポジトリにプッシュします。これにより、GitHub Actionsの公開ワークフローがトリガーされます。
        ```bash
        git tag v0.1.3 # バージョン番号を適宜変更
        git push origin v0.1.3 # バージョン番号を適宜変更
        ```

4.  **GitHub Actionsの確認**:
    *   GitHubリポジトリのActionsタブで、`Publish Python Package to PyPI` ワークフローが開始され、正常に完了することを確認します。

**手動でのワークフロー実行**:
何らかの理由でタグのプッシュによる自動実行ができない場合や、再実行が必要な場合は、GitHubリポジトリのActionsタブから `Publish Python Package to PyPI` ワークフローを選択し、「Run workflow」ボタンから手動で実行することも可能です。
## ライセンス
このプロジェクトはMITライセンスのもとで公開されています。詳細は `pyproject.toml` の `license` フィールドをご覧ください。

## コントリビューション
バグ報告、機能改善の提案、プルリクエストなどを歓迎します。
-   何か問題を見つけた場合や改善提案がある場合は、お気軽にGitHub Issuesに報告してください。
-   コードの変更を提案する場合は、フォークしてブランチを作成し、変更内容を記述したプルリクエストを送ってください。プルリクエストには、変更の目的や内容を明確に記述するようお願いします。
