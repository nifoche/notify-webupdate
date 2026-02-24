# SNS Update Monitor

SNSページの更新を監視し、新着投稿をLINEとメールで通知するシステム。

## 機能

- 複数SNSの更新を数秒〜数分間隔で監視
- PlaywrightによるJSレンダリング対応
- SQLiteによる重複チェック
- LINE Messaging API で即時通知
- SMTPメールによる通知
- 軽量動作（画像読み込みブロック）

## システム要件

- Python 3.10+
- Linux VPS (Ubuntu 24.04 推奨)
- メモリ 1GB以上

## インストール

```bash
# 依存関係のインストール
sudo apt update
sudo apt install -y python3 python3-pip python3-venv

# 仮想環境の作成
python3 -m venv venv
source venv/bin/activate

# パッケージのインストール
pip install -r requirements.txt
```

## 設定

1. `.env.example` を `.env` にコピー
2. 環境変数を設定

```bash
cp .env.example .env
nano .env
```

### LINE Messaging API の設定

1. [LINE Developers](https://developers.line.biz/) でプロバイダー・チャンネル作成
2. Messaging API を有効化
3. チャネルアクセストークン・ユーザーIDを取得
4. `.env` に設定

### Gmail SMTP の設定

1. Googleアカウントで2段階認証を有効化
2. アプリパスワードを発行
3. `.env` に設定

## 実行

### 手動実行

```bash
source venv/bin/activate
python main.py
```

### サービス登録（24時間稼働）

```bash
# サービスファイルのコピー
sudo cp sns-monitor.service /etc/systemd/system/

# サービスの有効化・起動
sudo systemctl daemon-reload
sudo systemctl enable sns-monitor
sudo systemctl start sns-monitor

# ステータス確認
sudo systemctl status sns-monitor

# ログ確認
sudo journalctl -u sns-monitor -f
```

## 運用コスト

| 項目 | コスト |
|------|--------|
| VPS | 月額 500〜1,000円 |
| LINE API | 0円（月200通まで） |
| メール | 0円（Gmail SMTP） |

## ライセンス

MIT
