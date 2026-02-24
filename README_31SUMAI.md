# 三井のすまい(31sumai) 予約監視セットアップガイド

## 概要

三井のすまいモデルルーム予約ページが「予約開始」状態に変わった際に、LINEとメールで通知するシステムです。

## 監視対象

- **URL**: https://www.31sumai.com/attend/X2571/
- **物件名**: パークコート麻布十番東京
- **監視間隔**: 60秒推奨（可変）

## 動作仕組み

### 状態判定

| 状態 | 検知キーワード | 通知 |
|------|---------------|------|
| **予約開始** | 「予約フォーム」「ご予約」「予約する」「申込」 | ✅ 通知 |
| **予約不可** | 「予約を受け付けておりません」「予約期間は終了」 | - 通知なし |

### 通知内容

**LINE通知**:
```
【更新通知】

サイト: 三井のすまい (X2571)

【予約開始】モデルルームの予約が開始されました！

https://www.31sumai.com/attend/X2571/
```

**メール通知**:
```
件名: 【更新通知】三井のすまい (X2571)

サイト: 三井のすまい (X2571)
内容: 【予約開始】モデルルームの予約が開始されました！
URL: https://www.31sumai.com/attend/X2571/
取得時刻: 2026-02-24 12:34:56
```

## セットアップ手順

### 1. プロジェクトのクローン

```bash
cd ~/projects
git clone https://github.com/nifoche/notify-webupdate.git
cd notify-webupdate
```

### 2. インストール

```bash
# インストールスクリプト実行
./setup.sh
```

### 3. 環境変数の設定

```bash
# 31sumai専用設定をコピー
cp .env.sumai.example .env

# 編集
nano .env
```

**必須設定項目**:
```bash
# ターゲットURL
TARGET_URLS=https://www.31sumai.com/attend/X2571/

# 監視間隔（秒）
CHECK_INTERVAL=60

# LINE Messaging API
LINE_CHANNEL_ACCESS_TOKEN=your_token_here
LINE_USER_ID=your_user_id_here

# SMTP (Gmail)
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password
TO_EMAIL=your_email@gmail.com
```

### 4. LINE APIの設定

1. [LINE Developers](https://developers.line.biz/) にアクセス
2. プロバイダーとチャンネルを作成
3. Messaging API を有効化
4. チャネルアクセストークンを取得
5. ユーザーIDを確認（テスト送信等で）
6. `.env` に設定

### 5. Gmail SMTPの設定

1. Googleアカウントで[2段階認証](https://myaccount.google.com/security)を有効化
2. [アプリパスワード](https://myaccount.google.com/apppasswords)を発行
3. `.env` に設定

### 6. テスト実行

```bash
# 仮想環境を有効化
source venv/bin/activate

# 手動実行（ログをリアルタイム表示）
python main.py
```

**期待される出力**:
```
2026-02-24 12:34:56 - __main__ - INFO - SNS Monitor initialized with 1 URLs
2026-02-24 12:34:57 - __main__ - INFO - Starting monitor...
2026-02-24 12:35:00 - __main__ - INFO - Status: not_available, Content: 【予約不可】現在予約を受け付けておりません
2026-02-24 12:35:00 - __main__ - INFO - Monitor cycle completed. Next check in 60s
```

初回実行時に現在の状態がデータベースに保存されます。**予約開始に変わったタイミングで通知が送信されます。**

### 7. サービス登録（24時間稼働）

```bash
# サービスをインストール
sudo ./install-service.sh

# サービスを起動
sudo systemctl start sns-monitor

# ステータス確認
sudo systemctl status sns-monitor

# ログ確認
sudo journalctl -u sns-monitor -f
```

## 複数URLの監視

複数の31sumaiページを監視する場合：

```bash
# .env
TARGET_URLS=https://www.31sumai.com/attend/X2571/,https://www.31sumai.com/attend/X9999/
```

## トラブルシューティング

### 通知が来ない場合

1. **データベースを確認**:
   ```bash
   sqlite3 posts.db "SELECT * FROM posts ORDER BY created_at DESC LIMIT 5;"
   ```

2. **ログを確認**:
   ```bash
   tail -f monitor.log
   ```

3. **LINEトークンの検証**:
   ```bash
   curl -v -X POST https://api.line.me/v2/bot/message/push \
     -H 'Authorization: Bearer YOUR_TOKEN' \
     -H 'Content-Type: application/json' \
     -d '{"to":"YOUR_USER_ID","messages":[{"type":"text","text":"Test"}]}'
   ```

### 状態が正しく検知されない場合

ページの構成が変更されている可能性があります。実際のページテキストを確認：

```bash
curl -s https://www.31sumai.com/attend/X2571/ | grep -i "予約"
```

キーワードを変更する場合は `scrapers/sumai.py` を編集してください。

## 関連ファイル

- `scrapers/sumai.py` - 31sumaiスクレイパー実装
- `main.py` - メイン監視ループ
- `.env.sumai.example` - 設定テンプレート

## ライセンス

MIT
