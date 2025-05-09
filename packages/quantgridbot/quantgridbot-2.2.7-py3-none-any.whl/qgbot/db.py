# src/qgbot/db.py

import sqlite3
import threading
import logging
import time
import random
from datetime import datetime
from pathlib import Path

DB_SCHEMA = """
CREATE TABLE IF NOT EXISTS trades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    action TEXT NOT NULL,
    tx_hash TEXT UNIQUE NOT NULL,
    eth_price REAL NOT NULL,
    eth_amount REAL NOT NULL
);
"""

class TradeDatabase:
    def __init__(self, db_path: str = "trades.db"):
        self.db_path = db_path
        self._lock = threading.RLock()
        self._connect()

    def _connect(self):
        try:
            Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
            self.conn = sqlite3.connect(self.db_path, timeout=10, check_same_thread=False)
            self.conn.execute("PRAGMA journal_mode=WAL;")
            self.conn.execute("PRAGMA foreign_keys = ON;")
            self.conn.execute(DB_SCHEMA)
            self.conn.commit()
            logging.info(f"[DB] Connected and initialized: {self.db_path}")
        except Exception as e:
            logging.critical(f"[DB INIT ERROR] {e}")
            raise SystemExit(1)

    def log_trade(self, action: str, tx_hash: str, eth_price: float, eth_amount: float, timestamp: str = None):
        """Log a trade with retry and lock safety."""
        timestamp = timestamp or datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        retries = 3
        delay = 1.5

        for attempt in range(1, retries + 1):
            try:
                with self._lock:
                    self.conn.execute(
                        """
                        INSERT OR IGNORE INTO trades (timestamp, action, tx_hash, eth_price, eth_amount)
                        VALUES (?, ?, ?, ?, ?)
                        """,
                        (timestamp, action.lower(), tx_hash, float(eth_price), float(eth_amount))
                    )
                    self.conn.commit()
                    logging.info(f"[✓ DB] {action.upper()} {eth_amount:.6f} ETH @ ${eth_price:.2f}")
                    return
            except sqlite3.OperationalError as e:
                logging.warning(f"[DB LOCKED] Attempt {attempt}: {e}")
                time.sleep(delay + random.uniform(0, 1))
                delay *= 2
            except Exception as e:
                logging.error(f"[DB ERROR] Logging failed: {e}")
                break
        logging.critical("[DB] Max retries reached. Trade not logged.")

    def fetch_all_trades(self):
        """Return full trade history (most recent first)."""
        try:
            with self._lock:
                cur = self.conn.cursor()
                cur.execute("SELECT * FROM trades ORDER BY id DESC")
                rows = cur.fetchall()
                logging.debug(f"[DB] Retrieved {len(rows)} trades.")
                return rows
        except Exception as e:
            logging.error(f"[DB READ ERROR] {e}")
            return []

    def backup_db(self, backup_path: str = None):
        """Create a database backup."""
        backup_path = backup_path or f"trades_backup_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.db"
        try:
            with self._lock:
                dest = sqlite3.connect(backup_path)
                self.conn.backup(dest)
                dest.close()
                logging.info(f"[DB] Backup completed: {backup_path}")
        except Exception as e:
            logging.error(f"[DB BACKUP ERROR] {e}")

    def close(self):
        """Safely close the DB connection."""
        try:
            with self._lock:
                self.conn.close()
                logging.info("[DB] Connection closed.")
        except Exception as e:
            logging.error(f"[DB CLOSE ERROR] {e}")


# === Global Singleton ===
trade_db = TradeDatabase()

def log_trade(action, tx_hash, eth_price, eth_amount, timestamp=None):
    """Legacy compatibility shim."""
    trade_db.log_trade(action, tx_hash, eth_price, eth_amount, timestamp)