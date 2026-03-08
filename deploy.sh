#!/bin/bash
# notify-webupdate 一括デプロイスクリプト
# ConoHa Webコンソールで実行してください

set -e  # エラー時は停止

echo "========================================="
echo "notify-webupdate デプロイ開始"
echo "========================================="
echo ""

# ===== ステップ1: Dockerインストール =====
echo "ステップ1: Dockerインストール"
echo "================================="

# Dockerインストール
if ! command -v docker &> /dev/null; then
    echo "Dockerをインストール中..."
    curl -fsSL https://get.docker.com | sh
    systemctl start docker
    systemctl enable docker
    echo "✓ Dockerインストール完了"
else
    echo "✓ Dockerは既にインストールされています"
fi

# Docker Composeインストール
if ! command -v docker-compose &> /dev/null; then
    echo "Docker Composeをインストール中..."
    curl -SL https://github.com/docker/compose/releases/download/v2.30.3/docker-compose-linux-x86_64 -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
    echo "✓ Docker Composeインストール完了"
else
    echo "✓ Docker Composeは既にインストールされています"
fi

echo ""
echo "バージョン確認:"
docker --version
docker-compose --version
echo ""

# ===== ステップ2: プロジェクトデプロイ =====
echo "ステップ2: プロジェクトデプロイ"
echo "================================="

# プロジェクトディレクトリ作成
mkdir -p /opt/notify-webupdate
cd /opt/notify-webupdate

# プロジェクトクローン
if [ -d "/opt/notify-webupdate/.git" ]; then
    echo "✓ プロジェクトは既にクローンされています"
    git pull
else
    echo "GitHubからプロジェクトをクローン中..."
    git clone https://github.com/nifoche/notify-webupdate.git .
    echo "✓ プロジェクトクローン完了"
fi

echo ""

# ===== ステップ3: 環境変数設定 =====
echo "ステップ3: 環境変数設定"
echo "================================="

if [ ! -f "/opt/notify-webupdate/.env" ]; then
    echo ".envファイルを作成します"
    cp /opt/notify-webupdate/.env.example /opt/notify-webupdate/.env
    echo "✓ .envファイル作成完了"
    echo ""
    echo "⚠️  以下の手順で.envファイルを編集してください:"
    echo "   nano /opt/notify-webupdate/.env"
    echo ""
    echo "   設定項目:"
    echo "   - TARGET_URLS: 監視対象URL"
    echo "   - LINE_CHANNEL_ACCESS_TOKEN: LINEトークン"
    echo "   - LINE_USER_ID: LINEユーザーID"
    echo "   - SMTP_USERNAME: Gmailアドレス"
    echo "   - SMTP_PASSWORD: Gmailアプリパスワード"
    echo ""
    echo "   編集完了後、以下のコマンドでデプロイを続行してください:"
    echo "   cd /opt/notify-webupdate"
    echo "   docker-compose up -d"
    echo ""
    exit 0
else
    echo "✓ .envファイルは既に存在します"
fi

echo ""

# ===== ステップ4: データディレクトリ作成 =====
echo "ステップ4: データディレクトリ作成"
echo "================================="

mkdir -p /opt/notify-webupdate/data
echo "✓ データディレクトリ作成完了"

echo ""

# ===== ステップ5: Dockerイメージビルド =====
echo "ステップ5: Dockerイメージビルド"
echo "================================="

echo "Dockerイメージをビルド中（5〜10分かかります）..."
docker-compose build
echo "✓ Dockerイメージビルド完了"

echo ""

# ===== ステップ6: Dockerコンテナ起動 =====
echo "ステップ6: Dockerコンテナ起動"
echo "================================="

docker-compose up -d
echo "✓ Dockerコンテナ起動完了"

echo ""

# ===== ステップ7: 動作確認 =====
echo "ステップ7: 動作確認"
echo "================================="

echo "コンテナ状態:"
docker ps | grep notify-webupdate

echo ""
echo "ログ（最新10行）:"
docker-compose logs --tail=10

echo ""
echo "========================================="
echo "デプロイ完了！"
echo "========================================="
echo ""
echo "監視開始しました！"
echo ""
echo "管理コマンド:"
echo "  ログ確認: docker-compose logs -f"
echo "  コンテナ停止: docker-compose stop"
echo "  コンテナ起動: docker-compose start"
echo "  コンテナ再起動: docker-compose restart"
echo "  コンテナ削除: docker-compose down"
echo ""
