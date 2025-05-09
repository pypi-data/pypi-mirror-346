# src/qgbot/wallet.py

import logging
import time
import random
from decimal import Decimal, InvalidOperation
from typing import Dict, Any, Optional

from .utils import get_eth_balance, now_price, safe_rpc


class DynamicWallet:
    def __init__(self, config: Dict[str, Any]) -> None:
        self.config = config
        self.address = config.get("wallet_address", "")
        if not self.address:
            logging.critical("[WALLET INIT ERROR] Wallet address not specified in config.")
            raise SystemExit(1)
        logging.info(f"[WALLET] Address initialized: {self.address}")

    def fetch_live_tokens(self) -> Dict[str, Dict[str, Decimal]]:
        """Return current ETH + tracked token balances with USD equivalents."""
        try:
            eth_balance = self._retry(self._get_eth_balance)
            eth_price = self._retry(self._get_now_price)
            eth_usd = eth_balance * eth_price

            result = {
                "ETH": {
                    "balance": eth_balance,
                    "usd_value": eth_usd
                }
            }

            if self.config.get("track_tokens"):
                for token in self.config.get("token_contracts", []):
                    entry = self._fetch_token_entry(token)
                    if entry:
                        result.update(entry)
            return result
        except Exception as e:
            logging.error(f"[WALLET ERROR] {e}")
            return self._empty_portfolio()

    def _retry(self, func, retries: int = 3, delay: int = 2) -> Decimal:
        for attempt in range(1, retries + 1):
            try:
                value = func()
                if isinstance(value, Decimal) and value >= 0:
                    return value
                raise ValueError("Invalid numeric result")
            except (Exception, InvalidOperation) as e:
                logging.warning(f"[RETRY {attempt}] {func.__name__}: {e}")
                time.sleep(delay + random.uniform(0, 1))
                delay *= 2
        logging.critical(f"[FAILURE] {func.__name__} max retries exceeded.")
        return Decimal("0")

    def _get_eth_balance(self) -> Decimal:
        return get_eth_balance(self.address)

    def _get_now_price(self) -> Decimal:
        return now_price()

    def _fetch_token_entry(self, token: Dict[str, Any]) -> Optional[Dict[str, Dict[str, Decimal]]]:
        try:
            contract = token.get("address")
            decimals = token.get("decimals", 18)
            symbol = token.get("symbol", "???")

            if not contract:
                logging.warning(f"[TOKEN MISSING] No contract address for symbol: {symbol}")
                return None

            method = "0x70a08231" + self.address.lower().replace("0x", "").rjust(64, "0")
            data = safe_rpc("eth_call", [{"to": contract, "data": method}, "latest"])

            if not data:
                logging.warning(f"[NO RESPONSE] {symbol} balance unavailable.")
                return None

            raw = int(data, 16)
            balance = Decimal(raw) / Decimal(10) ** decimals
            if balance <= 0:
                return None

            # Placeholder: same pricing method as ETH (or extend with oracle support)
            token_price = self._retry(self._get_now_price)
            usd_value = balance * token_price

            return {
                symbol: {
                    "balance": balance,
                    "usd_value": usd_value
                }
            }
        except Exception as e:
            logging.error(f"[TOKEN FETCH ERROR] {token.get('symbol', '???')}: {e}")
            return None

    def _empty_portfolio(self) -> Dict[str, Dict[str, Decimal]]:
        return {
            "ETH": {
                "balance": Decimal("0"),
                "usd_value": Decimal("0")
            }
        }