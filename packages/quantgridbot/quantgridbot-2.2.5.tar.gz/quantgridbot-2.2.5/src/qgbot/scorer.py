# src/qgbot/scorer.py

import logging
import time
import random
from decimal import Decimal, InvalidOperation
from collections import deque
from typing import List, Tuple, Optional

from .utils import now_price, fetch_token_price_via_uniswap


class TokenScorer:
    def __init__(
        self,
        tokens: List[str],
        min_volatility_threshold: Decimal = Decimal("0.001"),
        rolling_window: int = 1
    ):
        """
        Volatility-based token signal detector.
        Args:
            tokens: list of token contract addresses
            min_volatility_threshold: ignore tokens that move less than this percent
            rolling_window: use last N prices for smoothing
        """
        self.tokens = tokens
        self.min_volatility_threshold = min_volatility_threshold
        self.rolling_window = rolling_window
        self.last_prices = {t: deque(maxlen=rolling_window) for t in tokens}

    def safe_fetch_price(self, token: str) -> Decimal:
        """Robust price fetch with retry across primary + fallback sources."""
        retries, delay = 3, 2
        for attempt in range(retries):
            try:
                price = fetch_token_price_via_uniswap(token)
                if price > 0:
                    return price

                price = now_price(token)
                if price > 0:
                    return price

                raise ValueError("Invalid price from all sources.")
            except (Exception, InvalidOperation) as e:
                logging.warning(f"[PRICE FETCH] {token} | Attempt {attempt+1}: {e}")
                time.sleep(delay + random.uniform(0, 1))
                delay *= 2
        logging.error(f"[FETCH FAILURE] {token} — final fallback to 0")
        return Decimal("0")

    def score_tokens(self) -> List[Tuple[str, Decimal]]:
        """Score tokens by recent price volatility (Δ%) over rolling window."""
        scored = []
        for token in self.tokens:
            try:
                current = self.safe_fetch_price(token)
                if current <= 0:
                    logging.debug(f"[SKIP TOKEN] {token} | price={current}")
                    continue

                history = self.last_prices[token]
                if history:
                    previous = history[-1]
                    if previous > 0:
                        delta = abs(current - previous) / previous
                        if delta >= self.min_volatility_threshold:
                            scored.append((token, delta))
                            logging.info(f"[SCORE] {token} Δ={delta:.5f}")
                history.append(current)
            except Exception as e:
                logging.error(f"[SCORING ERROR] {token}: {e}")
        return sorted(scored, key=lambda x: x[1], reverse=True)

    def best_token(self) -> Optional[str]:
        """Return most volatile token, or fallback to first."""
        try:
            ranked = self.score_tokens()
            if ranked:
                top = ranked[0]
                logging.info(f"[BEST TOKEN] {top[0]} | Δ={top[1]:.5f}")
                return top[0]
        except Exception as e:
            logging.error(f"[BEST TOKEN ERROR] {e}")
        return self.tokens[0] if self.tokens else None

    def top_n_tokens(self, n: int = 3) -> List[str]:
        """Return top-N most volatile tokens by recent delta."""
        try:
            ranked = self.score_tokens()
            top = [t for t, _ in ranked[:n]]
            logging.info(f"[TOP {n}] {top}")
            return top
        except Exception as e:
            logging.error(f"[TOP N ERROR] {e}")
            return []