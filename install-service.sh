#!/bin/bash
# systemd Service Installation Script

set -e

if [ "$EUID" -ne 0 ]; then
    echo "Error: Please run as root (sudo)"
    exit 1
fi

echo "========================================="
echo "SNS Monitor Service Installation"
echo "========================================="
echo ""

# プロジェクトパスの取得
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_PATH="$SCRIPT_DIR"
VENV_PATH="$PROJECT_PATH/venv"

# ユーザー名の取得
SERVICE_USER=${SUDO_USER:-$USER}

echo "Project path: $PROJECT_PATH"
echo "Service user: $SERVICE_USER"
echo ""

# サービスファイルの作成
cat > /etc/systemd/system/sns-monitor.service <<EOF
[Unit]
Description=SNS Update Monitor Service
After=network.target

[Service]
Type=simple
User=$SERVICE_USER
WorkingDirectory=$PROJECT_PATH
Environment="PATH=$VENV_PATH/bin"
ExecStart=$VENV_PATH/bin/python $PROJECT_PATH/main.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

echo "✓ Service file created"

# systemdのリロード
systemctl daemon-reload
echo "✓ systemd reloaded"

# サービスの有効化
systemctl enable sns-monitor
echo "✓ Service enabled"

echo ""
echo "========================================="
echo "Installation completed!"
echo "========================================="
echo ""
echo "Commands:"
echo "  Start:   sudo systemctl start sns-monitor"
echo "  Stop:    sudo systemctl stop sns-monitor"
echo "  Status:  sudo systemctl status sns-monitor"
echo "  Logs:    sudo journalctl -u sns-monitor -f"
echo ""
echo "To start the service now, run:"
echo "  sudo systemctl start sns-monitor"
echo ""
