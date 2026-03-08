# ConoHa VPS デプロイ完全ガイド

このガイドでは、ConoHa VPSにnotify-webupdateをデプロイするための手順を、初心者向けに詳細に説明します。

**所要時間: 約30分〜1時間**

---

## 📋 目次

1. [事前準備](#事前準備)
2. [ConoHaアカウント作成](#1-conohaアカウント作成)
3. [VPSサーバー作成](#2-vpsサーバー作成)
4. [SSH接続設定](#3-ssh接続設定)
5. [Dockerインストール](#4-dockerインストール)
6. [プロジェクトデプロイ](#5-プロジェクトデプロイ)
7. [サービス起動と確認](#6-サービス起動と確認)
8. [トラブルシューティング](#トラブルシューティング)

---

## 事前準備

### 必要なもの

- ✅ クレジットカードまたはPayPalアカウント
- ✅ メールアドレス
- ✅ ターミナルアプリ（Mac: ターミナル.app、Windows: PowerShell or Git Bash）
- ✅ テキストエディタ（メモ帳など）

### 費用の目安

| 項目 | 初期費用 | 月額費用 |
|------|---------|---------|
| VPSサーバー（1GB） | ¥0 | ¥1,135 |
| ドメイン（任意） | ¥1,000〜 | ¥1,000〜/年 |
| **合計** | **¥0** | **¥1,135/月〜** |

---

## 1. ConoHaアカウント作成

### ステップ1: ConoHaにアクセス

1. ブラウザで [ConoHa VPS](https://www.conoha.jp/vps/) を開く
2. 右上の「**会員登録**」ボタンをクリック

### ステップ2: 会員登録フォーム

**必要情報**:
- メールアドレス
- パスワード（8文字以上、英数字記号を混ぜること）

**入力例**:
```
メールアドレス: your-email@example.com
パスワード: Abc12345!  （←この強度を目安に）
```

### ステップ3: メール認証

1. 入力したメールアドレスに確認メールが届く
2. メール内の「**本登録**」リンクをクリック
3. ブラウザで登録完了画面が表示される

### ステップ4: お客様情報入力

**必要情報**:
- 氏名（フリガナ）
- 電話番号
- 住所
- 支払い方法（クレジットカード or PayPal）

**注意点**:
- 氏名はローマ字でも漢字でもOK
- 電話番号は携帯電話でOK
- 住所は日本国内であればどこでもOK

### ステップ5: 支払い情報登録

**クレジットカードの場合**:
- カード番号
- 有効期限
- セキュリティコード（裏面の3桁）
- カード名義人

**PayPalの場合**:
- PayPalアカウントでログイン
- 連携を承認

**⚠️ 重要**: 
- 初回は**¥0**（試用期間あり）
- **¥1,135**はVPS作成後の翌月から課金
- いつでも解約可能

---

## 2. VPSサーバー作成

### ステップ1: ConoHaコントロールパネルにログイン

1. [ConoHaコントロールパネル](https://manage.conoha.jp/) にアクセス
2. 登録したメールアドレスとパスワードでログイン

### ステップ2: VPS追加ボタンをクリック

1. 左側のメニューから「**VPS**」をクリック
2. 右上の「**VPS追加**」ボタンをクリック

### ステップ3: サーバー設定

以下の通り設定します：

#### ① プラン選択

| プラン | メモリ | SSD | 月額 | 推奨度 |
|--------|--------|-----|------|--------|
| 512MB | 512MB | 50GB SSD | ¥685 | ❌ Playwrightには不足 |
| **1GB** | **1GB** | **50GB SSD** | **¥1,135** | ✅ **推奨** |
| 2GB | 2GB | 50GB SSD | ¥1,715 | △ 余裕があるならOK |
| 4GB | 4GB | 100GB SSD | ¥3,198 | △ 過剰 |

**選択**: 「**1GB / 50GB SSD / 1コア**」

#### ② イメージ選択

**✅ 推奨: 「Ubuntu 24.04 LTS」を選択**

**理由**:
- LTS（Long Term Support）で2027年までサポート
- Python 3.12がプリインストール
- 情報が豊富でトラブルシューティングが容易
- **Dockerインストールは5分で完了**（コマンド1つ）

**「Docker」イメージについて**:
- ConoHaが提供するDockerプリインストールイメージを選ぶことも可能
- ただし、以下の点に注意が必要です：
  - ⚠️ ベースOSが不明確な場合がある
  - ⚠️ Dockerバージョンが古い可能性がある
  - ⚠️ トラブル時の情報が少ない
- **初心者には「Ubuntu 24.04 LTS」を選んで自分でDockerをインストールする方を推奨**

**選択肢の比較**:
| イメージ | 推奨度 | 理由 |
|---------|--------|------|
| **Ubuntu 24.04 LTS** | ✅ **推奨** | 最新・情報豊富・Dockerインストール簡単 |
| Ubuntu 22.04 LTS | △ | 古い（2027年4月までサポート） |
| Docker（ConoHa提供） | △ | 環境が不明確・バージョン古いかも |
| CentOS / AlmaLinux | ❌ | 設定が異なる場合あり |
| Debian | △ | 情報がUbuntuより少ない |

#### ③ rootパスワード設定

**重要**: 強力なパスワードを設定してください！

**パスワードの要件**:
- 8文字以上
- 英大文字・小文字・数字・記号を混ぜる

**良い例**:
```
Xy9#mP2$vL5
Kj8@nQ4%zW1
```

**悪い例**:
```
password123  （←簡単すぎる）
root  （←短すぎる）
abcd1234  （←パターンが単純）
```

**⚠️ 注意**:
- このパスワードはサーバーの管理者権限です
- **絶対に忘れないでください！**
- メモアプリに保存推奨

#### ④ ネームタグ設定（任意）

サーバーを識別するための名前です。

**例**:
- `notify-monitor`
- `sns-update-watcher`
- `31sumai-checker`

**設定**: `notify-monitor` と入力

#### ⑤ SSH鍵設定

**今回はスキップします**（後で設定可能）

- 「**SSH鍵**」: 未選択のまま
- パスワード認証で接続します

#### ⑥ パケットフィルター設定（ファイアウォール）

**設定**: 「**ssh-only**」または「**全て許可**」を選択

**推奨**: 「**全て許可**」を選択（後でSSH設定後、ポート22のみ開放に変更）

### ステップ4: 確認と追加

1. 設定内容を確認
2. 「**追加**」ボタンをクリック
3. 1〜2分でサーバーが起動

### ステップ5: IPアドレスをメモ

**重要**: サーバー起動後に表示されるIPアドレスをメモしてください！

**例**:
```
IPアドレス: XXX.XXX.XXX.XXX
```

**このIPアドレスは以下で使います**:
- SSH接続
- ブラウザでのアクセス（Web管理画面がある場合）

---

## 3. SSH接続設定

### ステップ1: ターミナルを開く

**Macの場合**:
1. 「**Spotlight検索**」を開く（`Cmd + Space`）
2. 「**ターミナル**」と入力
3. `Enter`キーで起動

**Windowsの場合**:
1. 「**スタートメニュー**」をクリック
2. 「**PowerShell**」または「**Git Bash**」を検索
3. 起動

### ステップ2: SSH接続コマンド入力

ターミナルで以下のコマンドを入力：

```bash
ssh root@XXX.XXX.XXX.XXX
```

**`XXX.XXX.XXX.XXX`** は、さっきメモしたIPアドレスに置き換えてください。

**例**:
```bash
ssh root@153.126.123.45
```

### ステップ3: 初回接続時の警告

初めて接続する場合、以下のメッセージが表示されます：

```
The authenticity of host 'XXX.XXX.XXX.XXX (XXX.XXX.XXX.XXX)' can't be established.
ED25519 key fingerprint is SHA256:xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx.
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])?
```

**対処**: `yes` と入力して`Enter`キー

### ステップ4: パスワード入力

```
root@XXX.XXX.XXX.XXX's password:
```

**対処**: さっき設定したrootパスワードを入力

**注意点**:
- 入力中は**何も表示されません**（セキュリティのため）
- 間違えてもBackSpaceで修正可能
- 入力完了したら`Enter`キー

### ステップ5: 接続成功

以下のようなメッセージが表示されれば接続成功：

```
Welcome to Ubuntu 24.04 LTS (GNU/Linux 6.8.0-1015-gcp x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

  System information as of Mon Jan XX XX:XX:XX UTC 2025

  System load:  0.01
  Usage of /:   12.5% of 19.52GB
  Memory usage: 18%
  Swap usage:   0%
  Processes:    102
  Users logged in: 0
  IPv4 address for eth0: XXX.XXX.XXX.XXX


Last login: Mon Jan XX XX:XX:XX 2025 from XXX.XXX.XXX.XXX
```

プロンプトが `root@vps-xxx-xxx-xxx:~#` に変わります。

### ステップ6: 接続を切る方法

```bash
exit
```

と入力すると接続が切れます。

---

## 4. Dockerインストール

### ステップ1: パッケージ更新

まず、パッケージリストを更新します。

```bash
apt update && apt upgrade -y
```

**説明**:
- `apt update`: 利用可能なパッケージのリストを更新
- `apt upgrade -y`: インストール済みパッケージをアップグレード
- `-y`: すべての確認プロンプトに自動で「はい」と答える

**所要時間**: 2〜5分

### ステップ2: タイムゾーン設定

**重要**: タイムゾーンを日本に設定しないと、ログの時刻が9時間ずれます！

```bash
timedatectl set-timezone Asia/Tokyo
```

**確認**:
```bash
date
```

**出力例**:
```
2025年  1月 XX日 月曜日 XX:XX:XX JST
```

**`JST`**と表示されればOK！

### ステップ3: 必要なパッケージインストール

Dockerインストールに必要なパッケージをインストールします。

```bash
apt install -y curl git
```

**説明**:
- `curl`: Webからファイルをダウンロードするツール
- `git`: バージョン管理システム（GitHubからクローンするため）

### ステップ4: Docker公式インストールスクリプト実行

**最も簡単な方法**: Docker公式のインストールスクリプトを使用します。

```bash
curl -fsSL https://get.docker.com | sh
```

**説明**:
- `curl`: ファイルをダウンロード
- `-fsSL`: エラー時に表示せず、 silentlyに従う
- `| sh`: ダウンロードしたスクリプトを実行

**所要時間**: 2〜5分

### ステップ5: Dockerバージョン確認

```bash
docker --version
```

**出力例**:
```
Docker version 27.3.1, build ce12230
```

バージョンが表示されれば成功！

### ステップ6: Dockerサービス起動・自動起動設定

```bash
# Dockerサービス起動
systemctl start docker

# 自動起動有効化（サーバー再起動時もDockerが自動起動）
systemctl enable docker

# 確認
systemctl is-enabled docker
```

**出力**:
```
enabled
```

`enabled`と表示されればOK！

### ステップ7: Docker Composeインストール

```bash
# 最新版のDocker Composeをダウンロード
curl -SL https://github.com/docker/compose/releases/download/v2.30.3/docker-compose-linux-x86_64 -o /usr/local/bin/docker-compose

# 実行権限付与
chmod +x /usr/local/bin/docker-compose

# 確認
docker-compose --version
```

**出力例**:
```
Docker Compose version v2.30.3
```

### ステップ8: 動作テスト

```bash
docker run hello-world
```

**出力例**:
```
Unable to find image 'hello-world:latest' locally
latest: Pulling from library/hello-world
...
Hello from Docker!
This message shows that your installation appears to be working correctly.
```

**`Hello from Docker!`**と表示されれば成功！

---

## 5. プロジェクトデプロイ

### ステップ1: プロジェクト用ディレクトリ作成

```bash
mkdir -p /opt/notify-webupdate
cd /opt/notify-webupdate
```

**説明**:
- `/opt`: サードパーティーソフトウェア用ディレクトリ（Linux標準）
- `notify-webupdate`: プロジェクト名

### ステップ2: プロジェクト転送

**方法A: GitHubからクローン（推奨）**

```bash
git clone https://github.com/nifoche/notify-webupdate.git .
```

**方法B: ローカルからrsyncで転送**

**ローカルPCのターミナルで実行**:

```bash
cd /Users/sales/genki-denki/dev/tools/notify-webupdate

rsync -avz --progress \
    --exclude 'venv' \
    --exclude '__pycache__' \
    --exclude '.git' \
    --exclude 'node_modules' \
    --exclude '*.db' \
    --exclude '.env' \
    ./ root@XXX.XXX.XXX.XXX:/opt/notify-webupdate/
```

**説明**:
- `-a`: アーカイブモード（パーミッション・タイムスタンプ保持）
- `-v`: 詳細表示
- `-z`: 転送中に圧縮
- `--progress`: 進捗表示
- `--exclude`: 除外するファイル・ディレクトリ

### ステップ3: 環境変数設定

```bash
# .envファイル作成
cp .env.example .env

# 編集
nano .env
```

**nanoエディタの基本操作**:
- `Ctrl + O`: 保存（「Write File」と表示されるので`Enter`）
- `Ctrl + X`: 終了

**設定内容**:
```bash
# 監視対象URL
TARGET_URLS=https://www.31sumai.com/attend/X2571/

# 監視間隔（秒）
CHECK_INTERVAL=60

# LINE Messaging API
LINE_CHANNEL_ACCESS_TOKEN=your_channel_access_token_here
LINE_USER_ID=your_user_id_here

# Gmail SMTP
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password_here
FROM_EMAIL=your_email@gmail.com
TO_EMAIL=your_email@gmail.com
```

---

## 6. サービス起動と確認

### ステップ1: Dockerイメージビルド

```bash
cd /opt/notify-webupdate

# Dockerイメージビルド
docker-compose build
```

**所要時間**: 5〜10分（初回のみ）

### ステップ2: Dockerコンテナ起動

```bash
# バックグラウンドで起動
docker-compose up -d
```

**出力例**:
```
Creating network "notify-webupdate_default" with the default driver
Creating notify-webupdate_monitor_1 ... done
```

### ステップ3: コンテナ状態確認

```bash
docker ps
```

**出力例**:
```
CONTAINER ID   IMAGE                    COMMAND             CREATED        STATUS        PORTS     NAMES
abc123def456   notify-webupdate_monitor   "python main.py"   5 seconds ago Up 4 seconds             notify-webupdate_monitor_1
```

**`STATUS`**が`Up XXX seconds`と表示されれば稼働中！

### ステップ4: ログ確認

```bash
# リアルタイムログ監視
docker-compose logs -f

# ログ監視終了（Ctrl + C）
```

**出力例**:
```
monitor_1  | 2025-01-XX XX:XX:XX - __main__ - INFO - SNS Monitor initialized with 1 URLs
monitor_1  | 2025-01-XX XX:XX:XX - __main__ - INFO - Starting monitor...
monitor_1  | 2025-01-XX XX:XX:XX - __main__ - INFO - Monitor cycle completed. Next check in 60s
```

### ステップ5: 手動通知テスト

```bash
# コンテナ内で通知テスト実行
docker-compose exec monitor python test-notifications.py
```

**LINEとメール両方に通知が届けば成功！**

### ステップ6: 自動再起動設定確認

Docker Composeには既に`restart: always`設定が含まれています。

**確認**:
```bash
docker inspect notify-webupdate_monitor_1 | grep -A 5 RestartPolicy
```

**出力**:
```
"RestartPolicy": {
    "Name": "always",
    "MaximumRetryCount": 0
},
```

---

## トラブルシューティング

### ❌ 問題1: SSH接続できない

**症状**:
```
ssh: connect to host XXX.XXX.XXX.XXX port 22: Connection refused
```

**原因**:
- サーバーが起動していない
- ファイアウォールでSSHポートがブロックされている

**対処法**:
1. ConoHaコントロールパネルでサーバーの状態を確認
2. サーバーが「**停止**」なら「**起動**」ボタンをクリック
3. 2〜3分待ってから再度SSH接続

---

### ❌ 問題2: Dockerがインストールできない

**症状**:
```
E: Unable to locate package curl
```

**対処法**:
```bash
apt update
apt install -y curl
```

---

### ❌ 問題3: Dockerコマンドが見つからない

**症状**:
```
bash: docker: command not found
```

**対処法**:
```bash
# Dockerがインストールされているか確認
which docker

# なければ再インストール
curl -fsSL https://get.docker.com | sh
```

---

### ❌ 問題4: docker-compose up -d が失敗

**症状**:
```
ERROR: Couldn't connect to Docker daemon
```

**対処法**:
```bash
# Dockerサービス起動
systemctl start docker

# 確認
systemctl status docker
```

---

### ❌ 問題5: 通知が来ない

**対処法**:

1. **ログ確認**:
```bash
docker-compose logs -f
```

2. **環境変数確認**:
```bash
docker-compose exec monitor env | grep LINE
docker-compose exec monitor env | grep SMTP
```

3. **通知テスト実行**:
```bash
docker-compose exec monitor python test-notifications.py
```

4. **設定再確認**:
- LINE: チャネルアクセストークンとユーザーIDが正しいか
- Gmail: アプリパスワードが正しいか

---

### ❌ 問題6: コンテナがすぐに終了する

**症状**:
```bash
docker ps
# 何も表示されない
```

**対処法**:

1. **終了したコンテナを確認**:
```bash
docker ps -a
```

2. **ログ確認**:
```bash
docker-compose logs
```

3. **再起動**:
```bash
docker-compose up -d
```

---

## 📊 運用管理

### サービス管理コマンド

| コマンド | 説明 |
|----------|------|
| `docker-compose ps` | コンテナ状態確認 |
| `docker-compose logs -f` | ログ監視 |
| `docker-compose restart` | サービス再起動 |
| `docker-compose stop` | サービス停止 |
| `docker-compose start` | サービス起動 |
| `docker-compose down` | コンテナ削除 |

### 定期メンテナンス

**1ヶ月に1回実行推奨**:

```bash
# Dockerイメージ更新
docker-compose pull
docker-compose up -d

# 古いDockerイメージ削除
docker image prune -a

# ディスク容量確認
df -h
```

---

## 📝 まとめ

### デプロイ完了後のチェックリスト

- [ ] SSH接続できる
- [ ] Dockerがインストールされている
- [ ] Docker Composeがインストールされている
- [ ] プロジェクトが転送されている
- [ ] .envファイルが設定されている
- [ ] Dockerコンテナが稼働している
- [ ] ログにエラーがない
- [ ] LINE通知が届く
- [ ] メール通知が届く

### 次のステップ

1. ✅ **デプロイ完了** - 24時間監視開始
2. 📊 **通知確認** - 更新時に通知が届くか
3. 🔧 **微調整** - 監視間隔などの調整
4. 📈 **運用開始** - 本格的なサイト監視

---

## 💡 コスト削減のヒント

### VPSプランの選び方

| 監視サイト数 | 推奨プラン | 月額 |
|------------|-----------|------|
| 1〜5サイト | 1GB | ¥1,135 |
| 5〜10サイト | 2GB | ¥1,715 |
| 10〜20サイト | 4GB | ¥3,198 |

### 監視間隔の調整

| 間隔 | 精度 | 負荷 | 推奨用途 |
|------|------|------|----------|
| 30秒 | 高 | 高 | 重要なサイトのみ |
| 60秒 | 中 | 中 | **推奨** |
| 120秒 | 低 | 低 | 複数サイト監視時 |

---

## 🆘 サポート

### ConoHa公式サポート

- [ConoHa VPS ドキュメント](https://support.conoha.jp/)
- [ConoHa サポートフォーム](https://www.conoha.jp/contact/)

### プロジェクト関連

- [GitHub Issues](https://github.com/nifoche/notify-webupdate/issues)

---

**最終更新**: 2025年1月
