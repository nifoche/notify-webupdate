#!/usr/bin/env python3
"""
Database Module - SQLiteによる投稿ID管理
"""

import logging
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


class Database:
    """SQLiteデータベース操作クラス"""

    def __init__(self, db_path: str = 'posts.db'):
        self.db_path = db_path
        self.conn = self._get_connection()
        self._create_table()

    def _get_connection(self) -> sqlite3.Connection:
        """データベース接続を取得"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            return conn
        except sqlite3.Error as e:
            logger.error(f"Failed to connect to database: {e}")
            raise

    def _create_table(self):
        """投稿テーブルを作成"""
        sql = '''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            post_id TEXT UNIQUE NOT NULL,
            content TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        '''
        try:
            self.conn.execute(sql)
            self.conn.commit()
            logger.info("Database table ready")
        except sqlite3.Error as e:
            logger.error(f"Failed to create table: {e}")
            raise

    def exists(self, post_id: str) -> bool:
        """投稿IDが存在するかチェック"""
        sql = 'SELECT 1 FROM posts WHERE post_id = ? LIMIT 1'
        try:
            cursor = self.conn.execute(sql, (post_id,))
            return cursor.fetchone() is not None
        except sqlite3.Error as e:
            logger.error(f"Failed to check post existence: {e}")
            return False

    def save_post(self, post_id: str, content: str):
        """新規投稿を保存"""
        sql = 'INSERT INTO posts (post_id, content) VALUES (?, ?)'
        try:
            self.conn.execute(sql, (post_id, content))
            self.conn.commit()
        except sqlite3.IntegrityError:
            logger.warning(f"Post {post_id} already exists (duplicate)")
        except sqlite3.Error as e:
            logger.error(f"Failed to save post: {e}")
            raise

    def get_all_posts(self) -> list:
        """全投稿を取得"""
        sql = 'SELECT * FROM posts ORDER BY created_at DESC'
        try:
            cursor = self.conn.execute(sql)
            return cursor.fetchall()
        except sqlite3.Error as e:
            logger.error(f"Failed to get posts: {e}")
            return []

    def cleanup_old_posts(self, days: int = 30):
        """古い投稿を削除"""
        sql = f'DELETE FROM posts WHERE created_at < datetime("now", "-{days} days")'
        try:
            cursor = self.conn.execute(sql)
            deleted = cursor.rowcount
            self.conn.commit()
            logger.info(f"Deleted {deleted} old posts (older than {days} days)")
            return deleted
        except sqlite3.Error as e:
            logger.error(f"Failed to cleanup old posts: {e}")
            return 0

    def close(self):
        """データベース接続を閉じる"""
        if self.conn:
            self.conn.close()
            logger.info("Database connection closed")
