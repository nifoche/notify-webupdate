#!/bin/bash
# SNS Update Monitor Setup Script

set -e

echo "========================================="
echo "SNS Update Monitor Setup"
echo "========================================="
echo ""

# Pythonのチェック
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | awk '{print $2}')
echo "✓ Python version: $PYTHON_VERSION"

# 仮想環境の作成
if [ ! -d "venv" ]; then
    echo ""
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

# 仮想環境を有効化
source venv/bin/activate

# パッケージのインストール
echo ""
echo "Installing Python packages..."
pip install --upgrade pip
pip install -r requirements.txt

# Playwrightブラウザのインストール
echo ""
echo "Installing Playwright browsers..."
playwright install chromium

# 環境変数ファイルのコピー
if [ ! -f ".env" ]; then
    echo ""
    echo "Creating .env file..."
    cp .env.example .env
    echo "✓ .env file created"
    echo ""
    echo "⚠️  Please edit .env file and configure your settings:"
    echo "   - TARGET_URLS"
    echo "   - LINE_CHANNEL_ACCESS_TOKEN"
    echo "   - LINE_USER_ID"
    echo "   - SMTP settings"
else
    echo "✓ .env file already exists"
fi

# データベース初期化
echo ""
echo "Initializing database..."
python3 -c "from database import Database; Database()"

# 実行権限の付与
chmod +x main.py
chmod +x setup.sh

echo ""
echo "========================================="
echo "Setup completed!"
echo "========================================="
echo ""
echo "Next steps:"
echo "1. Edit .env file with your settings"
echo "2. Run manually: source venv/bin/activate && python main.py"
echo "3. Or install as service: sudo ./install-service.sh"
echo ""
