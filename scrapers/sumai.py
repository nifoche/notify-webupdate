#!/usr/bin/env python3
"""
31sumai (三井のすまい) Scraper - モデルルーム予約ページ監視
"""

import logging
from typing import List, Dict
from playwright.async_api import Page
from urllib.parse import urlparse

from .base import BaseScraper

logger = logging.getLogger(__name__)


class SumaiScraper(BaseScraper):
    """三井のすまい予約ページのスクレイパー"""

    # 予約不可状態を示すキーワード
    NOT_AVAILABLE_KEYWORDS = [
        "予約を受け付けておりません",
        "ただいま予約を受け付けておりません",
        "予約は終了いたしました",
        "予約期間は終了いたしました"
    ]

    # 予約可能状態を示すキーワード
    AVAILABLE_KEYWORDS = [
        "予約フォーム",
        "ご予約",
        "予約する",
        "申込"
    ]

    def get_site_name(self) -> str:
        parsed = urlparse(self.url)
        path_parts = parsed.path.split('/')
        event_code = path_parts[-2] if len(path_parts) > 2 else "Unknown"
        return f"三井のすまい ({event_code})"

    async def fetch_posts(self, page: Page) -> List[Dict[str, str]]:
        """
        予約ページの状態を取得

        Returns:
            [{'id': '状態を示すID', 'content': '状態を示すテキスト', 'url': 'ページURL'}]
        """
        await self.setup_page(page)

        try:
            await page.goto(self.url, wait_until='networkidle', timeout=30000)

            # ページ全体のテキストを取得
            page_text = await page.inner_text('body')

            # 状態判定
            status = self._determine_status(page_text)
            content = self._get_status_content(page_text, status)

            # ステータスをIDとして使用（変更検出用）
            status_id = f"sumai_status_{status}"

            post = {
                'id': status_id,
                'content': content,
                'url': self.url,
                'status': status  # 追加情報
            }

            logger.info(f"Status: {status}, Content: {content[:100]}")
            return [post]

        except Exception as e:
            logger.error(f"Failed to fetch 31sumai page: {e}")
            return []

    def _determine_status(self, page_text: str) -> str:
        """
        ページのテキストから状態を判定

        Returns:
            'available' (予約可能) | 'not_available' (予約不可) | 'unknown' (不明)
        """
        page_lower = page_text.lower()

        # 予約不可キーワードのチェック
        for keyword in self.NOT_AVAILABLE_KEYWORDS:
            if keyword in page_text:
                return 'not_available'

        # 予約可能キーワードのチェック
        for keyword in self.AVAILABLE_KEYWORDS:
            if keyword in page_text:
                return 'available'

        return 'unknown'

    def _get_status_content(self, page_text: str, status: str) -> str:
        """状態に応じた通知メッセージを生成"""
        if status == 'available':
            return "【予約開始】モデルルームの予約が開始されました！"
        elif status == 'not_available':
            return "【予約不可】現在予約を受け付けておりません"
        else:
            return f"【状態不明】ページの状態を特定できませんでした"
