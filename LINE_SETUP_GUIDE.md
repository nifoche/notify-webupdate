# LINE Messaging API 設定完全ガイド

notify-webupdateでLINE通知を使用するための詳細な手順書です。

**所要時間**: 10〜15分

---

## 📋 目次

1. [LINE Developersアカウント作成](#1-line-developersアカウント作成)
2. [プロバイダー作成](#2プロバイダー作成)
3. [Messaging APIチャンネル作成](#3-messaging-apiチャンネル作成)
4. [チャネルアクセストークンの取得](#4チャネルアクセストークンの取得)
5. [ユーザーIDの取得](#5ユーザーidの取得)
6. [環境変数への設定](#6環境変数への設定)
7. [通知テスト](#7通知テスト)
8. [トラブルシューティング](#トラブルシューティング)

---

## 1. LINE Developersアカウント作成

### ステップ1: LINE Developersにアクセス

ブラウザで [LINE Developers](https://developers.line.biz/) にアクセス

### ステップ2: ログイン

1. 「**Log in**」ボタンをクリック
2. LINEアカウントでログイン
   - スマホのLINEアプリでQRコード扫描
   - またはメールアドレスとパスワードでログイン

### ステップ3: 初回ログイン時の設定

初めてログインする場合、以下の情報を入力：

- **メールアドレス**
- **パスワード**
- **氏名**
- **所属組織**（個人利用の場合は「個人」または「Personal」でOK）

---

## 2. プロバイダー作成

**プロバイダー**とは、チャンネルをグループ化するためのものです。

### ステップ1: プロバイダー作成

1. [LINE Developersコンソール](https://developers.line.biz/console/) にアクセス
2. 「**Create new provider**」ボタンをクリック

### ステップ2: プロバイダー情報入力

以下の情報を入力：

| 項目 | 入力例 | 説明 |
|------|--------|------|
| **Provider name** | `notify-webupdate` | プロバイダー名（英数字） |
| **Provider name (for display)** | `SNS Update Monitor` | 表示名（日本語OK） |
| **Email address** | `your-email@example.com` | 連絡先メールアドレス |
| **Website** | `https://github.com/nifoche/notify-webupdate` | ウェブサイトURL（GitHubでOK） |
| **Description** | `Webサイト更新をLINEで通知するシステム` | 説明 |

### ステップ3: 作成完了

「**Create**」ボタンをクリックするとプロバイダーが作成されます。

---

## 3. Messaging APIチャンネル作成

Messaging API機能を使用するためのチャンネルを作成します。

### ステップ1: チャンネル作成

1. 作成したプロバイダーのページを開く
2. 「**Create a new channel**」ボタンをクリック

### ステップ2: チャンネルタイプ選択

「**Messaging API**」を選択して「**Next**」をクリック

### ステップ3: チャンネル情報入力

以下の情報を入力：

| 項目 | 入力例 | 説明 |
|------|--------|------|
| **Channel name** | `notify-monitor` | チャンネル名（英数字、小文字推奨） |
| **Channel description** | `SNS更新通知チャンネル` | チャンネルの説明 |
| **Channel icon** | （任意） | チャンネルのアイコン画像 |
| **Category** | `Application` | カテゴリ（Applicationを選択） |
| **Sub-category** | `Tools, utilities` | サブカテゴリ |

### ステップ4: 利用規約に同意

- 「**I agree to the LINE Messaging API Terms of Use and Privacy Policy**」にチェック
- 「**Create**」ボタンをクリック

---

## 4. チャネルアクセストークンの取得

チャネルアクセストークンは、LINE APIを呼び出すためのパスワードのようなものです。

### ステップ1: チャンネル設定画面を開く

1. 作成したチャンネルのページを開く
2. 「**Messaging API**」タブをクリック

### ステップ2: チャネルアクセストークンを発行

1. 「**Channel access token**」セクションを探す
2. 「**Issue**」ボタンをクリック

### ステップ3: トークンをコピー

発行されたトークンをコピーしてください。

**重要**:
- ⚠️ **このトークンは再表示できません！**
- ⚠️ **必ず安全な場所に保存してください**
- ⚠️ **他人に絶対に教えないでください**

**トークンの例**:
```
eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI6MSIsIm5hbWUiOiJUb255IFN0YXJrIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
```

---

## 5. ユーザーIDの取得

ユーザーIDは、通知を送る相手（あなた）のLINEアカウントのIDです。

### 方法A: LINE公式アプリから確認（推奨・最も簡単）

**スマホのLINEアプリで確認**:

1. LINEアプリを開く
2. 右上の「**...（その他）**」をタップ
3. 「**設定**」をタップ
4. 「**アカウント**」をタップ
5. 「**ユーザーID**」欄にIDが表示されます（例: `U1234567890abcdef1234567890abcdef`）

### 方法B: テストメッセージで確認

**LINE Developersコンソールで確認**:

1. チャネルの「**Messaging API**」タブを開く
2. 「**Messages**」セクションを探す
3. 「**Send test message**」をクリック
4. 送信先ユーザーを選択
5. メッセージを送信
6. あなたのLINEアプリでメッセージを受信

**ユーザーIDの確認方法**:
- テストメッセージのURLから確認:
  ```
  https://api.line.me/v2/bot/message/U1234567890abcdef1234567890abcdef/reply
                                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                        これがユーザーID
  ```

---

## 6. 環境変数への設定

取得したチャネルアクセストークンとユーザーIDを`.env`ファイルに設定します。

### ステップ1: VPSにログイン

```bash
ssh root@163.44.116.182
```

### ステップ2: .envファイルを編集

```bash
cd /opt/notify-webupdate
nano .env
```

### ステップ3: LINE設定を入力

以下の項目を編集：

```bash
# LINE Messaging API設定
LINE_CHANNEL_ACCESS_TOKEN=ここにチャンネルアクセストークンを貼り付け
LINE_USER_ID=ここにユーザーIDを貼り付け
```

**入力例**:
```bash
LINE_CHANNEL_ACCESS_TOKEN=eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI6MSIsIm5hbWUiOiJUb255IFN0YXJrIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
LINE_USER_ID=U1234567890abcdef1234567890abcdef
```

### ステップ4: 保存と終了

- `Ctrl + O` → `Enter` → 保存
- `Ctrl + X` → 終了

---

## 7. 通知テスト

設定が正しいか確認するためのテストを実行します。

### ステップ1: 通知テストスクリプトを実行

```bash
cd /opt/notify-webupdate
docker-compose exec monitor python test-notifications.py
```

### ステップ2: LINEアプリで確認

以下のようなメッセージが届けば成功：

```
【テスト通知】

 notify-webupdate からのテスト通知です。

 時刻: 2025-03-09 12:34:56

 もしこのメッセージが届いていれば、LINE通知は正常に動作しています！✅
```

---

## トラブルシューティング

### ❌ 問題1: 通知が届かない

#### 原因1: チャネルアクセストークンが間違っている

**確認方法**:
```bash
# .envファイルを確認
cat /opt/notify-webupdate/.env | grep LINE_CHANNEL_ACCESS_TOKEN
```

**対処法**:
- トークンに余分なスペースがないか確認
- トークン全体がコピーされているか確認
- トークンを再発行して再設定

---

#### 原因2: ユーザーIDが間違っている

**確認方法**:
```bash
# .envファイルを確認
cat /opt/notify-webupdate/.env | grep LINE_USER_ID
```

**対処法**:
- ユーザーIDの形式を確認（`U`で始まる33文字）
- LINEアプリで再度ユーザーIDを確認

---

#### 原因3: LINE Messaging APIが有効化されていない

**確認方法**:
- LINE Developersコンソールでチャンネルを確認
- 「**Messaging API**」タブ → ステータスが「**Enabled**」になっているか

**対処法**:
- チャンネルが「**Pending**」の場合、承認待ち
- 1〜2時間待ってから再試行

---

### ❌ 問題2: 「401 Unauthorized」エラー

**原因**: チャネルアクセストークンが無効

**対処法**:
1. チャネルアクセストークンを再発行
2. `.env`ファイルのトークンを更新
3. Dockerコンテナを再起動

```bash
cd /opt/notify-webupdate
docker-compose restart
```

---

### ❌ 問題3: 「400 Bad Request」エラー

**原因**: リクエスト形式の問題

**対処法**:
- ユーザーIDの形式を確認（`U` + 33文字の英数字）
- 通知メッセージの長さを確認（長すぎないか）

---

## 📊 LINE APIの制限

### 無料枠

| プラン | 月間送信数 | 料金 |
|--------|-----------|------|
| **Free** | 1,000通 | 無料 |
| **Basic** | 10,000通 | 無料 |
| **Pro** | 100,000通 | 無料 |

**更新監視の場合**: Freeプランで十分（1日あたり最大33通）

---

## 🎯 完了チェックリスト

設定完了後、以下を確認してください：

- [ ] LINE Developersアカウントを作成した
- [ ] プロバイダーを作成した
- [ ] Messaging APIチャンネルを作成した
- [ ] チャネルアクセストークンを取得した
- [ ] ユーザーIDを取得した
- [ ] .envファイルに設定した
- [ ] 通知テストに成功した

---

## 🔗 参考リンク

- [LINE Developers](https://developers.line.biz/)
- [LINE Developers Console](https://developers.line.biz/console/)
- [Messaging APIドキュメント](https://developers.line.biz/en/docs/messaging-api/)

---

**最終更新**: 2025年3月9日
