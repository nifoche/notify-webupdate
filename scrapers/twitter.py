#!/usr/bin/env python3
"""
Twitter/X Scraper - Twitterの投稿を取得するスクレイパー
"""

import logging
from typing import List, Dict
from playwright.async_api import Page
from urllib.parse import urlparse

from .base import BaseScraper

logger = logging.getLogger(__name__)


class TwitterScraper(BaseScraper):
    """Twitter/Xのスクレイパー"""

    def get_site_name(self) -> str:
        return "Twitter/X"

    async def fetch_posts(self, page: Page) -> List[Dict[str, str]]:
        """
        Twitterのページから投稿を取得

        注意: Twitterはログイン要件が厳しいため、実際にはAPIの使用を推奨
        この実装は公開アカウント向けのサンプルです
        """
        await self.setup_page(page)

        try:
            await page.goto(self.url, wait_until='networkidle', timeout=30000)

            # Twitterの投稿セレクタ（変更される可能性があります）
            posts = []

            # 投稿要素を取得
            tweet_elements = await page.query_selector_all('article[data-testid="tweet"]')

            for element in tweet_elements[:10]:  # 最新10件
                try:
                    # 投稿IDを取得
                    tweet_id = await element.get_attribute('aria-labelledby')

                    # 投稿内容を取得
                    content_elem = await element.query_selector('div[lang]')
                    if content_elem:
                        content = await content_elem.inner_text()
                    else:
                        content = "Content not available"

                    # 投稿URLを構築
                    tweet_url = await self._extract_tweet_url(element, self.url)

                    posts.append({
                        'id': tweet_id or f"unknown_{hash(content)}",
                        'content': content[:500],  # 500文字に制限
                        'url': tweet_url
                    })

                except Exception as e:
                    logger.warning(f"Failed to parse tweet: {e}")
                    continue

            logger.info(f"Fetched {len(posts)} posts from Twitter")
            return posts

        except Exception as e:
            logger.error(f"Failed to fetch Twitter posts: {e}")
            return []

    async def _extract_tweet_url(self, element, base_url: str) -> str:
        """ツイートのURLを抽出"""
        try:
            link_elem = await element.query_selector('a[href*="/status/"]')
            if link_elem:
                href = await link_elem.get_attribute('href')
                if href and href.startswith('/'):
                    return f"https://x.com{href}"
                return href
        except:
            pass
        return base_url
