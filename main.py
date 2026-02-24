#!/usr/bin/env python3
"""
SNS Update Monitor - Main Script
SNSの更新を監視し、新着投稿をLINEとメールで通知する
"""

import asyncio
import logging
import os
import random
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional

from dotenv import load_dotenv
from playwright.async_api import async_playwright, Browser, Page

from database import Database
from notifier import send_line_notification, send_email_notification

# 環境変数の読み込み
load_dotenv()

# ログ設定
LOG_PATH = os.getenv('LOG_PATH', 'monitor.log')
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_PATH, encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class SNSMonitor:
    """SNS更新監視クラス"""

    def __init__(self):
        self.target_urls = self._parse_urls()
        self.check_interval = int(os.getenv('CHECK_INTERVAL', '120'))
        self.db = Database(os.getenv('DATABASE_PATH', 'posts.db'))
        logger.info(f"SNS Monitor initialized with {len(self.target_urls)} URLs")

    def _parse_urls(self) -> List[str]:
        """環境変数からURLをパース"""
        urls_str = os.getenv('TARGET_URLS', '')
        return [url.strip() for url in urls_str.split(',') if url.strip()]

    async def fetch_posts(self, page: Page, url: str) -> List[Dict[str, str]]:
        """
        SNSページから投稿を取得する（汎用実装）

        注意: 実際にはSNSごとにスクレイピングロジックを実装する必要があります
        これはサンプル実装です
        """
        try:
            await page.goto(url, wait_until='networkidle', timeout=30000)

            # サンプル: ページタイトルを取得（実際には投稿データを取得）
            # 実装例: Twitter/X, Facebook等のセレクタを指定
            posts = []

            # TODO: SNSごとのセレクタを実装
            # 例: Twitterの場合
            # post_elements = await page.query_selector_all('article[data-testid="tweet"]')
            # for element in post_elements:
            #     post_id = await element.get_attribute('aria-labelledby')
            #     content = await element.inner_text()
            #     posts.append({'id': post_id, 'content': content})

            # サンプルデータ（開発用）
            sample_id = f"sample_{datetime.now().isoformat()}"
            posts.append({
                'id': sample_id,
                'content': f'Sample post from {url}',
                'url': url
            })

            return posts

        except Exception as e:
            logger.error(f"Failed to fetch posts from {url}: {e}")
            return []

    async def monitor(self):
        """監視メインループ"""
        logger.info("Starting monitor...")

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)

            for url in self.target_urls:
                try:
                    # 軽量ページを作成（画像・フォント読み込み無効）
                    page = await browser.new_page()

                    await page.route("**/*.{png,jpg,jpeg,gif,webp,svg,ico,woff,woff2,ttf}",
                                    lambda route: route.abort())

                    # 投稿取得
                    posts = await self.fetch_posts(page, url)

                    if not posts:
                        logger.info(f"No posts found for {url}")
                        await page.close()
                        continue

                    # 差分チェック
                    for post in posts:
                        post_id = post['id']
                        content = post['content']
                        post_url = post.get('url', url)

                        if not self.db.exists(post_id):
                            logger.info(f"New post detected: {post_id}")

                            # 通知送信
                            await self._send_notifications(post_id, content, post_url, url)

                            # データベースに保存
                            self.db.save_post(post_id, content)
                            logger.info(f"Saved post {post_id} to database")
                        else:
                            logger.debug(f"Post {post_id} already exists")

                    await page.close()

                except Exception as e:
                    logger.error(f"Error monitoring {url}: {e}", exc_info=True)

            await browser.close()

        logger.info(f"Monitor cycle completed. Next check in {self.check_interval}s")

    async def _send_notifications(self, post_id: str, content: str, post_url: str, site_url: str):
        """LINEとメールで通知を送信"""
        site_name = self._extract_site_name(site_url)

        # LINE通知
        try:
            message = f"【SNS更新通知】\n\nサイト: {site_name}\n\n{content}\n\n{post_url}"
            await send_line_notification(message)
            logger.info(f"LINE notification sent for post {post_id}")
        except Exception as e:
            logger.error(f"Failed to send LINE notification: {e}")

        # メール通知
        try:
            subject = f"【SNS更新通知】{site_name}"
            body = f"""サイト: {site_name}
投稿内容: {content}
URL: {post_url}
取得時刻: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
            send_email_notification(subject, body)
            logger.info(f"Email notification sent for post {post_id}")
        except Exception as e:
            logger.error(f"Failed to send email notification: {e}")

    def _extract_site_name(self, url: str) -> str:
        """URLからサイト名を抽出"""
        from urllib.parse import urlparse
        parsed = urlparse(url)
        return parsed.netloc.replace('www.', '')

    def _add_random_delay(self):
        """アンチブロックのためのランダム待機"""
        base_delay = self.check_interval
        variation = base_delay * 0.2  # ±20%
        delay = base_delay + random.uniform(-variation, variation)
        logger.debug(f"Sleeping for {delay:.2f}s")
        return delay

    async def run(self):
        """継続実行ループ"""
        logger.info("Monitor started. Press Ctrl+C to stop.")

        try:
            while True:
                await self.monitor()
                delay = self._add_random_delay()
                await asyncio.sleep(delay)

        except KeyboardInterrupt:
            logger.info("Monitor stopped by user")
        except Exception as e:
            logger.error(f"Monitor crashed: {e}", exc_info=True)
            raise


async def main():
    """メイン関数"""
    monitor = SNSMonitor()
    await monitor.run()


if __name__ == '__main__':
    asyncio.run(main())
