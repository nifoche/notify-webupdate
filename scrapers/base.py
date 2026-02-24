#!/usr/bin/env python3
"""
Base Scraper - スクレイパーの基底クラス
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from playwright.async_api import Page


class BaseScraper(ABC):
    """スクレイパーの基底クラス"""

    def __init__(self, url: str):
        self.url = url

    @abstractmethod
    async def fetch_posts(self, page: Page) -> List[Dict[str, str]]:
        """
        ページから投稿を取得する

        Args:
            page: PlaywrightのPageオブジェクト

        Returns:
            投稿データのリスト [{'id': str, 'content': str, 'url': str}, ...]
        """
        pass

    @abstractmethod
    def get_site_name(self) -> str:
        """サイト名を返す"""
        pass

    async def setup_page(self, page: Page):
        """
        ページの初期設定（画像・フォント読み込みのブロック）
        """
        await page.route("**/*.{png,jpg,jpeg,gif,webp,svg,ico,woff,woff2,ttf}",
                        lambda route: route.abort())
