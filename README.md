# SNS/Web Update Monitor

SNSページやWebサイトの更新を監視し、新着投稿をLINEとメールで通知するシステム。

## 機能

- 複数SNS/Webサイトの更新を数秒〜数分間隔で監視
- PlaywrightによるJSレンダリング対応
- SQLiteによる重複チェック
- LINE Messaging API で即時通知
- SMTPメールによる通知
- 軽量動作（画像読み込みブロック）

## 対応サイト

| サイト | スクレイパー | 用途 |
|--------|------------|------|
| **三井のすまい (31sumai)** | `SumaiScraper` | モデルルーム予約監視 |
| Twitter/X | `TwitterScraper` | ツイート監視 |
| Facebook | `FacebookScraper` | 投稿監視 |
| その他 | `GenericScraper` | 汎用ページ監視 |

---

## 🏢 三井のすまい(31sumai) 予約監視

モデルルーム予約ページが「予約開始」状態に変わった際に通知します。

### セットアップ（クイック）

```bash
# 1. プロジェクトをクローン
git clone https://github.com/nifoche/notify-webupdate.git
cd notify-webupdate

# 2. インストール
./setup.sh

# 3. 31sumai用設定を作成
cp .env.sumai.example .env
nano .env
```

### `.env`設定

```bash
# 監視対象URL
TARGET_URLS=https://www.31sumai.com/attend/X2571/

# 監視間隔（秒）- 60秒推奨
CHECK_INTERVAL=60

# LINE Messaging API
LINE_CHANNEL_ACCESS_TOKEN=your_channel_access_token
LINE_USER_ID=your_user_id

# Gmail SMTP
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password
TO_EMAIL=your_email@gmail.com
```

### 動作仕組み

| 現在の状態 | 次の状態 | 通知 |
|-----------|---------|------|
| 予約不可 | 予約開始 | ✅ 通知送信 |
| 予約開始 | 予約開始 | - 送信済みなので通知なし |
| 予約開始 | 予約不可 | ✅ 状態変更を通知 |

**検出キーワード**:
- 予約開始: 「予約フォーム」「ご予約」「予約する」「申込」
- 予約不可: 「予約を受け付けておりません」「予約期間は終了」

### 実行

```bash
# 手動実行（テスト）
source venv/bin/activate
python main.py

# サービス登録（24時間稼働）
sudo ./install-service.sh
sudo systemctl start sns-monitor
```

---

## システム要件

- Python 3.10+
- Linux VPS (Ubuntu 24.04 推奨)
- メモリ 1GB以上

## 全体的なインストール手順

### 依存関係のインストール

```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv
```

### 仮想環境の作成

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 環境変数の設定

```bash
# デフォルト設定
cp .env.example .env

# または31sumai用設定
cp .env.sumai.example .env

nano .env
```

---

## LINE Messaging API の設定

1. [LINE Developers](https://developers.line.biz/) でプロバイダー・チャンネル作成
2. Messaging API を有効化
3. チャネルアクセストークン・ユーザーIDを取得
4. `.env` に設定

## Gmail SMTP の設定

1. Googleアカウントで2段階認証を有効化
2. アプリパスワードを発行
3. `.env` に設定

---

## 運用コスト

| 項目 | コスト |
|------|--------|
| VPS | 月額 500〜1,000円 |
| LINE API | 0円（月200通まで） |
| メール | 0円（Gmail SMTP） |

---

## トラブルシューティング

### 通知が来ない場合

1. データベースを確認:
   ```bash
   sqlite3 posts.db "SELECT * FROM posts ORDER BY created_at DESC LIMIT 5;"
   ```

2. ログを確認:
   ```bash
   tail -f monitor.log
   ```

### サービス管理

```bash
# ステータス確認
sudo systemctl status sns-monitor

# ログ確認
sudo journalctl -u sns-monitor -f

# 再起動
sudo systemctl restart sns-monitor

# 停止
sudo systemctl stop sns-monitor
```

---

## ライセンス

MIT
