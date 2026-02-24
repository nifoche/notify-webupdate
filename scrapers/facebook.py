#!/usr/bin/env python3
"""
Facebook Scraper - Facebookの投稿を取得するスクレイパー
"""

import logging
from typing import List, Dict
from playwright.async_api import Page

from .base import BaseScraper

logger = logging.getLogger(__name__)


class FacebookScraper(BaseScraper):
    """Facebookページのスクレイパー"""

    def get_site_name(self) -> str:
        return "Facebook"

    async def fetch_posts(self, page: Page) -> List[Dict[str, str]]:
        """
        Facebookのページから投稿を取得

        注意: Facebookはログイン要件があるため、実際にはAPIの使用を推奨
        この実装は公開ページ向けのサンプルです
        """
        await self.setup_page(page)

        try:
            await page.goto(self.url, wait_until='networkidle', timeout=30000)

            posts = []

            # Facebookの投稿セレクタ（変更される可能性があります）
            post_elements = await page.query_selector_all('[role="article"]')

            for element in post_elements[:10]:  # 最新10件
                try:
                    # 投稿IDを取得（FBではデータ-testid等を使用）
                    post_id = await element.get_attribute('data-testid') or f"fb_{hash(str(element))}"

                    # 投稿内容を取得
                    content_elem = await element.query_selector('[data-text]')
                    if content_elem:
                        content = await content_elem.inner_text()
                    else:
                        # フォールバック: 全体のテキストを取得
                        content = await element.inner_text()
                        content = content.split('\n')[0]  # 最初の行のみ

                    posts.append({
                        'id': post_id,
                        'content': content[:500],  # 500文字に制限
                        'url': self.url
                    })

                except Exception as e:
                    logger.warning(f"Failed to parse Facebook post: {e}")
                    continue

            logger.info(f"Fetched {len(posts)} posts from Facebook")
            return posts

        except Exception as e:
            logger.error(f"Failed to fetch Facebook posts: {e}")
            return []
