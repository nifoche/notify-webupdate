#!/usr/bin/env python3
"""
Notification Module - LINEとメールによる通知送信
"""

import logging
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import requests

logger = logging.getLogger(__name__)


def send_line_notification(message: str) -> bool:
    """
    LINE Messaging APIで通知を送信

    Args:
        message: 送信するメッセージ

    Returns:
        成功時True、失敗時False
    """
    line_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
    line_user_id = os.getenv('LINE_USER_ID')

    if not line_token or not line_user_id:
        logger.error("LINE credentials not configured")
        return False

    url = 'https://api.line.me/v2/bot/message/push'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {line_token}'
    }
    data = {
        'to': line_user_id,
        'messages': [
            {
                'type': 'text',
                'text': message
            }
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=data, timeout=10)
        response.raise_for_status()
        logger.info("LINE notification sent successfully")
        return True
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to send LINE notification: {e}")
        return False


def send_email_notification(subject: str, body: str) -> bool:
    """
    SMTPメールで通知を送信

    Args:
        subject: メール件名
        body: メール本文

    Returns:
        成功時True、失敗時False
    """
    smtp_host = os.getenv('SMTP_HOST')
    smtp_port = int(os.getenv('SMTP_PORT', '587'))
    smtp_username = os.getenv('SMTP_USERNAME')
    smtp_password = os.getenv('SMTP_PASSWORD')
    from_email = os.getenv('FROM_EMAIL')
    to_email = os.getenv('TO_EMAIL')

    if not all([smtp_host, smtp_username, smtp_password, from_email, to_email]):
        logger.error("SMTP credentials not configured")
        return False

    try:
        # メール作成
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain', 'utf-8'))

        # SMTP接続・送信
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.send_message(msg)

        logger.info("Email notification sent successfully")
        return True

    except Exception as e:
        logger.error(f"Failed to send email notification: {e}")
        return False
