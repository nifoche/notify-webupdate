# Playwright公式Pythonイメージを使用
FROM mcr.microsoft.com/playwright/python:v1.48.0-noble

# 作業ディレクトリ設定
WORKDIR /app

# Python依存関係インストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Playwrightブラウザインストール
RUN playwright install --with-deps chromium

# プロジェクトファイルコピー
COPY . .

# データディレクトリ作成
RUN mkdir -p /app/data

# 環境変数設定
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# ヘルスチェック（Dockerが動いているか確認用）
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)" || exit 1

# コマンド実行
CMD ["python", "main.py"]
