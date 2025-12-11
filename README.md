
NoSQLNoEscape
==============

SQL クイズを出題するフロントエンド (Vite + React + TypeScript) と、クイズデータを返す FastAPI バックエンドのセットです。

構成
----
- backend: FastAPI サーバー。クイズ API とデータ生成スクリプトを含む。
- frontend: React (Vite) クライアント。API からクイズを取得して四択表示。

前提
---
- Python 3.11+
- Node.js 18+（推奨）

バックエンドセットアップ
------------------
1) ディレクトリ移動: `cd backend`
2) 依存インストール: `pip install -r requirements.txt`
3) 開発サーバー起動: `uvicorn main:app --reload --host 0.0.0.0 --port 8000`
- API 詳細は [backend/README.md](backend/README.md) を参照。
- クイズデータは [backend/quiz_data.json](backend/quiz_data.json)。不足分生成は `python generate_quiz_data.py`。

フロントエンドセットアップ
--------------------
1) ディレクトリ移動: `cd frontend`
2) 依存インストール: `npm install`
3) ローカル開発: `npm run dev`
- バックエンドが異なるホストの場合、`.env` で `VITE_API_BASE` を設定（例: `VITE_API_BASE=http://localhost:8000`）。

主な操作
------
- GET `/quizzes?level=basic&count=10&shuffle=true` でクイズ一覧取得。
- GET `/quiz/{question_id}` で個別問題取得。
- フロントは起動時に選択レベルのクイズを取得し、回答後に正解・解説を表示します。

