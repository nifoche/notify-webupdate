#!/usr/bin/env python3
"""
通知テストスクリプト
LINEとメールの設定が正しいかを確認するためのテストツール
"""

import os
import sys
from datetime import datetime

from dotenv import load_dotenv

# カレントディレクトリの.envを読み込み
load_dotenv()

# メインモジュールから通知関数をインポート
sys.path.insert(0, os.path.dirname(__file__))
from notifier import send_line_notification, send_email_notification


def test_line_notification():
    """LINE通知テスト"""
    print("=" * 50)
    print("LINE通知テスト")
    print("=" * 50)

    line_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
    line_user_id = os.getenv('LINE_USER_ID')

    if not line_token or line_token == 'your_channel_access_token_here':
        print("❌ LINE_CHANNEL_ACCESS_TOKEN が設定されていません")
        print("   .envファイルで設定してください")
        return False

    if not line_user_id or line_user_id == 'your_user_id_here':
        print("❌ LINE_USER_ID が設定されていません")
        print("   .envファイルで設定してください")
        return False

    message = f"""【テスト通知】
 notify-webupdate からのテスト通知です。

 時刻: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

 もしこのメッセージが届いていれば、LINE通知は正常に動作しています！✅
"""

    print(f"メッセージ送信中...")
    print(f"トークン: {line_token[:20]}...")
    print(f"ユーザーID: {line_user_id}")
    print()

    success = send_line_notification(message)

    if success:
        print("✅ LINE通知の送信に成功しました！")
        print("   LINEアプリでメッセージを確認してください")
    else:
        print("❌ LINE通知の送信に失敗しました")
        print("   以下を確認してください:")
        print("   - CHANNEL_ACCESS_TOKEN が正しいか")
        print("   - USER_ID が正しいか")
        print("   - インターネット接続が正常か")

    print()
    return success


def test_email_notification():
    """メール通知テスト"""
    print("=" * 50)
    print("メール通知テスト")
    print("=" * 50)

    smtp_host = os.getenv('SMTP_HOST')
    smtp_username = os.getenv('SMTP_USERNAME')
    smtp_password = os.getenv('SMTP_PASSWORD')
    from_email = os.getenv('FROM_EMAIL')
    to_email = os.getenv('TO_EMAIL')

    # 必須項目チェック
    missing = []
    if not smtp_host:
        missing.append('SMTP_HOST')
    if not smtp_username or smtp_username == 'your_email@gmail.com':
        missing.append('SMTP_USERNAME')
    if not smtp_password or smtp_password == 'your_app_password_here':
        missing.append('SMTP_PASSWORD')
    if not from_email or from_email == 'your_email@gmail.com':
        missing.append('FROM_EMAIL')
    if not to_email or to_email == 'your_email@gmail.com':
        missing.append('TO_EMAIL')

    if missing:
        print("❌ 以下の項目が設定されていません:")
        for item in missing:
            print(f"   - {item}")
        print("   .envファイルで設定してください")
        return False

    subject = "【テスト】notify-webupdate からの通知"
    body = f"""notify-webupdate からのテストメールです。

時刻: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

もしこのメールが届いていれば、メール通知は正常に動作しています！✅
"""

    print(f"メール送信中...")
    print(f"SMTPサーバー: {smtp_host}")
    print(f"送信元: {from_email}")
    print(f"送信先: {to_email}")
    print()

    success = send_email_notification(subject, body)

    if success:
        print("✅ メール通知の送信に成功しました！")
        print("   メールボックスを確認してください")
    else:
        print("❌ メール通知の送信に失敗しました")
        print("   以下を確認してください:")
        print("   - SMTP_USERNAME（Gmailアドレス）が正しいか")
        print("   - SMTP_PASSWORD（アプリパスワード）が正しいか")
        print("   - Gmailで2段階認証が有効になっているか")
        print("   - アプリパスワードが発行されているか")

    print()
    return success


def main():
    """メイン関数"""
    print()
    print("🚀 notify-webupdate 通知テストツール")
    print()

    # .envファイル存在チェック
    if not os.path.exists('.env'):
        print("❌ .envファイルが見つかりません")
        print("   以下の手順で作成してください:")
        print("   1. cp .env.example .env")
        print("   2. nano .env")
        print("   3. 必要な情報を入力して保存")
        print()
        return

    # LINEテスト
    line_ok = test_line_notification()

    # メールテスト
    email_ok = test_email_notification()

    # 結果サマリー
    print("=" * 50)
    print("テスト結果サマリー")
    print("=" * 50)
    print(f"LINE通知:  {'✅ 成功' if line_ok else '❌ 失敗'}")
    print(f"メール通知: {'✅ 成功' if email_ok else '❌ 失敗'}")
    print()

    if line_ok and email_ok:
        print("🎉 すべての通知テストに成功しました！")
        print("   これでVPSにデプロイする準備ができました")
    else:
        print("⚠️  一部のテストに失敗しました")
        print("   上記の指示に従って設定を確認してください")

    print()


if __name__ == '__main__':
    main()
