# SNSスクレイパーの使用方法

## 概要

各SNSごとのスクレイピングロジックを`scrapers/`モジュールで管理しています。

## 対応SNS

- Twitter/X (`scrapers/twitter.py`)
- Facebook (`scrapers/facebook.py`)

## 新しいSNSの追加方法

1. `scrapers/`ディレクトリに新しいファイルを作成（例: `instagram.py`）
2. `BaseScraper`を継承したクラスを実装

```python
from scrapers.base import BaseScraper
from playwright.async_api import Page
from typing import List, Dict

class InstagramScraper(BaseScraper):
    def get_site_name(self) -> str:
        return "Instagram"

    async def fetch_posts(self, page: Page) -> List[Dict[str, str]]:
        await self.setup_page(page)
        await page.goto(self.url, wait_until='networkidle')

        # Instagram固有のセレクタで投稿を取得
        posts = []
        # ... 実装 ...

        return posts
```

3. `scrapers/__init__.py`にエクスポートを追加

4. `main.py`で使用

```python
from scrapers import InstagramScraper

scraper = InstagramScraper(url)
posts = await scraper.fetch_posts(page)
```

## 注意点

- **Twitter/X**: ログイン要件があるため、実際にはAPI使用を推奨
- **Facebook**: 公開ページのみ対応、ログインが必要なページはAPI使用を推奨
- セレクタはサイトの更新で変わる可能性があるため、定期的なメンテナンスが必要

## API使用推奨

安定した運用には、各SNSの公式APIを使用することを推奨します：

- Twitter API v2
- Facebook Graph API
- Instagram Basic Display API
