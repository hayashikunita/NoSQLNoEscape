NoSQLNoEscape Backend
======================

FastAPI で実装されたクイズ配信 API。ローカルの `quiz_data.json` を読み込み、難易度別クイズを返します。

動作環境
--------
- Python 3.11+
- pip または uv

セットアップ
-----------
1. 仮想環境を作成・有効化（任意）。
2. 依存関係をインストール:
	 - pip の場合: `pip install -r requirements.txt`
	 - uv の場合: `uv pip install -r requirements.txt`

起動方法
------
開発サーバーをポート 8000 で起動します。

```
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

主要エンドポイント
----------------
- GET `/health`: ヘルスチェック。
- GET `/quizzes`: クイズ一覧を取得。
	- クエリ: `level` (`basic`|`standard`|`hard`, 既定 `basic`), `count` (取得数, 既定 10), `shuffle` (シャッフル有無, 既定 true)。
	- レスポンス: `total` (該当難易度の総数), `count` (返却件数), `level`, `items` (クイズ配列)。
- GET `/quiz/{question_id}`: 個別クイズを取得 (`basic-001` などの ID 指定)。

クイズデータ
----------
- データは [quiz_data.json](quiz_data.json) に保存。
- 雛形生成スクリプト: [generate_quiz_data.py](generate_quiz_data.py)
	- 既存の `quiz_data.json` をベースに、目標件数（basic:100, standard:50, hard:50）まで自動生成。
	- 実行例: `python generate_quiz_data.py`

開発メモ
------
- CORS は全許可で設定済み（フロントエンド開発用）。
- スキーマは Pydantic の `QuizQuestion` / `QuizResponse` を使用しています。
