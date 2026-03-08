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

---

## 🔔 通知設定の手順

### ステップ1: .envファイルの作成

```bash
# テンプレートをコピー
cp .env.example .env

# 編集
nano .env
```

### ステップ2: 通知テスト

```bash
# 仮想環境を有効化
source venv/bin/activate

# 通知テスト実行
python test-notifications.py
```

---

## 📱 LINE Messaging API の詳細設定

### 手順1: LINE Developersでプロバイダー・チャンネル作成

1. [LINE Developers](https://developers.line.biz/) にアクセス
2. 「**Log in**」でLINEアカウントでログイン
3. 「**Start free**」または「**Create new provider**」をクリック
4. プロバイダー名を入力（例: `notify-webupdate`）
5. 「**Messaging API**」チャンネルを作成
6. チャンネル名を入力（例: `SNS Monitor`）
7. チャンネル説明を入力（例: `Webサイト更新通知`）
8. 「**Agree**」にチェックして「**Create**」

### 手順2: Messaging APIの設定

1. 作成したチャンネルの「**Messaging API**」タブを開く
2. 「**Channel access token**」の「**Issue**」をクリック
3. 表示されたトークンをコピー（**再表示不可なので注意！**）
4. `.env`の`LINE_CHANNEL_ACCESS_TOKEN`に貼り付け

### 手順3: ユーザーIDの取得

**方法A: LINE公式アプリから確認（推奨）**

1. スマホのLINEアプリを開く
2. 「**ホーム**」タブ → 「**設定**」（歯車アイコン）
3. 「**プロフィール**」
4. 「**自分のユーザーID**」をコピー

**方法B: テストメッセージ送信で確認**

1. LINE Developersコンソールの「**Messaging API**」タブ
2. 「**Messages**」セクション
3. 「**Send test message**」をクリック
4. 自分のLINEアカウントを選択してメッセージ送信
5. `https://api.line.me/v2/bot/message/{userId}/...` の`userId`部分がユーザーID

### 手順4: .envに設定

```bash
LINE_CHANNEL_ACCESS_TOKEN=ここにチャンネルアクセストークンを貼り付け
LINE_USER_ID=ここにユーザーIDを貼り付け
```

### 🎯 LINE APIの制限

- **無料枠**: 月200通まで
- **超過後**: 1通あたり約¥1〜2
- **更新監視なら200通で十分**

---

## 📧 Gmail SMTP の詳細設定

### 手順1: 2段階認証の有効化

1. [Googleアカウントセキュリティ](https://myaccount.google.com/security) にアクセス
2. 「**2段階認証プロセス**」がオフの場合はオンにする
3. スマホにGoogle認証アプリをインストール（推奨）
4. 2段階認証を設定

### 手順2: アプリパスワードの発行

**重要**: Gmailのパスワードではなく、**アプリパスワード**が必要です！

1. [Googleアカウントセキュリティ](https://myaccount.google.com/security) にアクセス
2. 「**2段階認証プロセス**」の設定画面に移動
3. 下にスクロールして「**アプリパスワード**」をクリック
4. Googleパスワードを入力
5. 以下の通り設定:
   - **アプリ**: 「**メール**」を選択
   - **デバイス**: 「**その他（名前を入力）**」→「`notify-webupdate`」と入力
6. 「**生成**」をクリック
7. 表示された16文字のパスワードをコピー（例: `abcd efgh ijkl mnop`）
8. **このパスワードは再表示されないので注意！**

### 手順3: .envに設定

```bash
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=abcd efgh ijkl mnop  # スペース込みでそのまま貼り付け
FROM_EMAIL=your_email@gmail.com
TO_EMAIL=your_email@gmail.com
```

### 🎯 Gmail SMTPの制限

- **1日あたり**: 最大500通
- **更新監視なら500通で十分**
- **無料**: Gmail SMTPは無料

### ⚠️ よくあるエラー

| エラー | 原因 | 対処法 |
|--------|------|--------|
| `Authentication failed` | アプリパスワードが間違っている | 再発行して正しくコピペ |
| `Less secure app access` | 2段階認証が無効 | 2段階認証を有効化 |
| `Invalid login` | 通常のパスワードを使用 | アプリパスワードを使用 |

---

## ✅ 通知テストの実行

### テスト手順

```bash
# 1. .envファイルを作成
cp .env.example .env
nano .env  # LINEとGmailの情報を入力

# 2. 仮想環境を有効化
source venv/bin/activate

# 3. 依存関係インストール（まだの場合）
pip install -r requirements.txt

# 4. 通知テスト実行
python test-notifications.py
```

### テスト結果の確認

**成功の場合**:
```
✅ LINE通知の送信に成功しました！
   LINEアプリでメッセージを確認してください

✅ メール通知の送信に成功しました！
   メールボックスを確認してください
```

**失敗の場合**:
```
❌ LINE通知の送信に失敗しました
   - CHANNEL_ACCESS_TOKEN が正しいか
   - USER_ID が正しいか

❌ メール通知の送信に失敗しました
   - SMTP_USERNAME（Gmailアドレス）が正しいか
   - SMTP_PASSWORD（アプリパスワード）が正しいか
```

---

## 🔧 .envファイルのセキュリティ

### ⚠️ 重要: .envファイルは絶対にGitHubに上げない

```bash
# .gitignore に含まれていることを確認
cat .gitignore | grep .env
```

### セキュリティベストプラクティス

1. **.envファイルはローカルのみで保持**
2. **VPSにアップロード時はscpやrsyncで安全に転送**
3. **ファイル権限を制限**: `chmod 600 .env`

---

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
