import time
import logging
import random
from decimal import Decimal, InvalidOperation
from threading import Event
from .utils import now_price, safe_rpc

class RebalanceBot:
    def __init__(self, wallet, executor, config):
        self.wallet = wallet
        self.executor = executor
        self.config = config
        self.interval = config.get('refresh_interval', 180)
        self.fallback_sleep = config.get('fallback_sleep', 10)
        self.rebalance_threshold = Decimal(str(config.get('rebalance_threshold', 0.1)))
        self.target_eth_ratio = Decimal(str(config.get('target_eth_ratio', 0.5)))
        self._stop_event = Event()

    def stop(self):
        self._stop_event.set()

    def safe_now_price(self):
        retries = 3
        delay = 2
        for attempt in range(retries):
            if self._stop_event.is_set():
                return Decimal('0')
            try:
                price = Decimal(now_price())
                if price <= 0:
                    raise ValueError("Zero or negative price fetched.")
                return price
            except (Exception, InvalidOperation) as e:
                logging.error(f"[SAFE NOW PRICE RETRY {attempt+1}] {e}")
                time.sleep(delay + random.uniform(0, 1))
                delay *= 2
        logging.error("[SAFE NOW PRICE ERROR] Max retries exceeded.")
        return Decimal('0')

    def run(self):
        logging.info("[REBALANCER] Running...")
        while not self._stop_event.is_set():
            try:
                eth_price = self.safe_now_price()
                if eth_price <= 0:
                    logging.warning("[REBALANCER WARNING] ETH price invalid, skipping cycle...")
                    time.sleep(self.fallback_sleep)
                    continue

                portfolio = self.wallet.fetch_live_tokens()
                eth_value = Decimal(portfolio.get('ETH', {}).get('usd_value', 0))
                total_value = sum(Decimal(asset.get('usd_value', 0)) for asset in portfolio.values())

                if eth_value <= 0 or total_value <= 0:
                    logging.warning("[REBALANCER WARNING] Invalid ETH or portfolio total detected.")
                    time.sleep(self.fallback_sleep)
                    continue

                eth_ratio = eth_value / total_value
                deviation = abs(eth_ratio - self.target_eth_ratio)

                logging.info(f"[REBALANCE STATUS] ETH ${eth_value:.2f} / Total ${total_value:.2f} | ETH Ratio {eth_ratio:.2%} | Deviation {deviation:.2%}")

                if deviation > self.rebalance_threshold:
                    self._rebalance(eth_value, total_value, eth_ratio, eth_price)
                else:
                    logging.info("[REBALANCER] Portfolio within balance threshold. No action needed.")

                time.sleep(self.interval)

            except Exception as e:
                logging.error(f"[REBALANCE LOOP ERROR] {e}")
                time.sleep(self.fallback_sleep)

        logging.info("[REBALANCER] Stop signal received. Rebalancer halted cleanly.")

    def _rebalance(self, eth_value, total_value, eth_ratio, eth_price):
        if self._stop_event.is_set():
            return

        try:
            target_eth_value = total_value * self.target_eth_ratio
            delta_value = target_eth_value - eth_value

            logging.info(f"[REBALANCE ACTION] Δ Target: ${delta_value:.2f}")

            if delta_value > 0:
                amount_needed = delta_value
                best_token = self._find_best_token_to_sell()
                if best_token:
                    logging.info(f"[REBALANCER] Swapping {best_token} → ETH (${amount_needed:.2f})...")
                    self.executor.swap_to_eth(best_token, amount_needed)
                else:
                    logging.warning("[REBALANCER WARNING] No token available to swap into ETH.")
            else:
                amount_to_sell = abs(delta_value)
                logging.info(f"[REBALANCER] Selling ETH → stablecoin (${amount_to_sell:.2f})...")
                self.executor.swap_eth_to_stable(amount_to_sell)

        except Exception as e:
            logging.error(f"[REBALANCE EXECUTION ERROR] {e}")

    def _find_best_token_to_sell(self):
        """Safely find the largest non-ETH token."""
        try:
            portfolio = self.wallet.fetch_live_tokens()
            candidates = {
                token: Decimal(asset.get('usd_value', 0))
                for token, asset in portfolio.items()
                if token != 'ETH' and Decimal(asset.get('usd_value', 0)) > 0
            }

            if not candidates:
                logging.warning("[REBALANCER WARNING] No non-ETH tokens available for rebalance.")
                return None

            best_token = max(candidates, key=candidates.get)
            logging.info(f"[BEST TOKEN SELECTED] {best_token} with USD value ${candidates[best_token]:.2f}")
            return best_token

        except Exception as e:
            logging.error(f"[BEST TOKEN SELECTION ERROR] {e}")
            return None