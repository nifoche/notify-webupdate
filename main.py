#!/usr/bin/env python3
"""
SNS Update Monitor - Main Script
SNS/Webページの更新を監視し、新着投稿をLINEとメールで通知する
"""

import asyncio
import logging
import os
import random
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
from urllib.parse import urlparse

from dotenv import load_dotenv
from playwright.async_api import async_playwright, Browser, Page

from database import Database
from notifier import send_line_notification, send_email_notification
from scrapers import SumaiScraper, TwitterScraper, FacebookScraper

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
    """SNS/Webページ更新監視クラス"""

    def __init__(self):
        self.target_urls = self._parse_urls()
        self.check_interval = int(os.getenv('CHECK_INTERVAL', '120'))
        self.db = Database(os.getenv('DATABASE_PATH', 'posts.db'))
        logger.info(f"SNS Monitor initialized with {len(self.target_urls)} URLs")

    def _parse_urls(self) -> List[str]:
        """環境変数からURLをパース"""
        urls_str = os.getenv('TARGET_URLS', '')
        return [url.strip() for url in urls_str.split(',') if url.strip()]

    def _create_scraper(self, url: str):
        """
        URLに応じたスクレイパーを作成

        Args:
            url: ターゲットURL

        Returns:
            スクレーパーインスタンス
        """
        parsed = urlparse(url)
        domain = parsed.netloc.lower()

        # 31sumai
        if '31sumai.com' in domain:
            return SumaiScraper(url)
        # Twitter/X
        elif 'twitter.com' in domain or 'x.com' in domain:
            return TwitterScraper(url)
        # Facebook
        elif 'facebook.com' in domain:
            return FacebookScraper(url)
        # デフォルト（汎用）
        else:
            logger.warning(f"No specific scraper for {domain}, using generic scraper")
            return GenericScraper(url)

    async def monitor(self):
        """監視メインループ"""
        logger.info("Starting monitor...")

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)

            for url in self.target_urls:
                try:
                    # スクレイパーを取得
                    scraper = self._create_scraper(url)

                    # 軽量ページを作成（画像・フォント読み込み無効）
                    page = await browser.new_page()

                    # ページ設定
                    if hasattr(scraper, 'setup_page'):
                        await scraper.setup_page(page)
                    else:
                        await self._setup_page_generic(page)

                    # 投稿取得
                    posts = await scraper.fetch_posts(page)

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
                            await self._send_notifications(
                                post_id,
                                content,
                                post_url,
                                url,
                                scraper.get_site_name()
                            )

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

    async def _setup_page_generic(self, page: Page):
        """汎用ページ設定（画像・フォント読み込み無効）"""
        await page.route("**/*.{png,jpg,jpeg,gif,webp,svg,ico,woff,woff2,ttf}",
                        lambda route: route.abort())

    async def _send_notifications(self, post_id: str, content: str, post_url: str,
                                  site_url: str, site_name: str):
        """LINEとメールで通知を送信"""
        # LINE通知
        try:
            message = f"【更新通知】\n\nサイト: {site_name}\n\n{content}\n\n{post_url}"
            await send_line_notification(message)
            logger.info(f"LINE notification sent for post {post_id}")
        except Exception as e:
            logger.error(f"Failed to send LINE notification: {e}")

        # メール通知
        try:
            subject = f"【更新通知】{site_name}"
            body = f"""サイト: {site_name}
内容: {content}
URL: {post_url}
取得時刻: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
            send_email_notification(subject, body)
            logger.info(f"Email notification sent for post {post_id}")
        except Exception as e:
            logger.error(f"Failed to send email notification: {e}")

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


class GenericScraper:
    """汎用スクレイパー（フォールバック用）"""

    def __init__(self, url: str):
        self.url = url

    def get_site_name(self) -> str:
        from urllib.parse import urlparse
        parsed = urlparse(self.url)
        return parsed.netloc.replace('www.', '')

    async def fetch_posts(self, page: Page) -> List[Dict[str, str]]:
        """ページのタイトルを取得（汎用実装）"""
        await page.goto(self.url, wait_until='networkidle', timeout=30000)

        # ページタイトルを取得
        title = await page.title()
        timestamp = datetime.now().isoformat()

        return [{
            'id': f"generic_{timestamp}",
            'content': f"ページ更新: {title}",
            'url': self.url
        }]

    async def setup_page(self, page: Page):
        """画像・フォント読み込み無効"""
        await page.route("**/*.{png,jpg,jpeg,gif,webp,svg,ico,woff,woff2,ttf}",
                        lambda route: route.abort())


async def main():
    """メイン関数"""
    monitor = SNSMonitor()
    await monitor.run()


if __name__ == '__main__':
    asyncio.run(main())
