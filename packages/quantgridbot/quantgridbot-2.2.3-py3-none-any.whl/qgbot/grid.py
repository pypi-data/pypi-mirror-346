# src/qgbot/grid.py

import time
import logging
import random
import numpy as np
from decimal import Decimal, InvalidOperation
from collections import deque
from threading import Event, Lock

from .utils import now_price


class GridBot:
    def __init__(self, wallet, executor, config):
        self.wallet = wallet
        self.executor = executor
        self.config = config

        self.grid_size = config['grid_size']
        self.refresh_interval = config['refresh_interval']
        self.cooldown = config['trade_cooldown']
        self.recenter_interval = config.get('recenter_interval', 180)
        self.slippage_threshold = Decimal(str(config.get('slippage_pct', '0.005')))
        self.grid_pct = Decimal(str(config.get('grid_lower_pct', '0.02'))) / Decimal('2')

        self.price_history = deque(maxlen=150)
        self._stop_event = Event()
        self._lock = Lock()

        self.mode = "single"
        self.primary_grid = []
        self.secondary_grid = []
        self.primary_center = Decimal('0')
        self.secondary_center = Decimal('0')
        self.last_trade_time = 0
        self.last_recenter_time = 0
        self.last_price = Decimal('0')

    def stop(self):
        self._stop_event.set()

    def safe_now_price(self) -> Decimal:
        """Get price with retry safety and validation."""
        retries, delay = 3, 2
        for attempt in range(retries):
            if self._stop_event.is_set():
                return Decimal('0')
            try:
                price = Decimal(now_price())
                if price <= 0:
                    raise ValueError("Zero or negative price.")
                return price
            except (Exception, InvalidOperation) as e:
                logging.error(f"[PRICE ERROR] Attempt {attempt + 1}: {e}")
                time.sleep(delay + random.uniform(0, 1))
                delay *= 2
        return Decimal('0')

    def setup_grid(self, center_price: Decimal, dual=False, center2: Decimal = None):
        try:
            lower = Decimal('1') - self.grid_pct
            upper = Decimal('1') + self.grid_pct
            points = self.grid_size + 1

            if dual and center2:
                self.mode = "dual"
                self.primary_grid = [center_price * Decimal(x) for x in np.linspace(float(lower), float(upper), points)]
                self.secondary_grid = [center2 * Decimal(x) for x in np.linspace(float(lower), float(upper), points)]
                self.primary_center = center_price
                self.secondary_center = center2
                logging.info(f"[DUAL GRID] Centers: ${center_price:.2f} & ${center2:.2f}")
            else:
                self.mode = "single"
                self.primary_grid = [center_price * Decimal(x) for x in np.linspace(float(lower), float(upper), points)]
                self.secondary_grid = []
                self.primary_center = center_price
                logging.info(f"[SINGLE GRID] Centered @ ${center_price:.2f} | {len(self.primary_grid)} levels")

            self.last_recenter_time = time.monotonic()
        except Exception as e:
            logging.error(f"[GRID SETUP ERROR] {e}")

    def detect_clusters(self):
        """Detect dominant price clusters via histogram."""
        try:
            if len(self.price_history) < 40:
                return None

            prices = np.array(self.price_history)
            hist, bins = np.histogram(prices, bins=6)
            peaks = np.argsort(hist)[-2:]

            clusters = []
            for i in sorted(peaks):
                low = Decimal(str(bins[i]))
                high = Decimal(str(bins[i + 1]))
                center = (low + high) / 2
                clusters.append(center)

            if len(clusters) == 2:
                spread = abs(clusters[0] - clusters[1]) / min(clusters)
                if spread > Decimal('0.015'):
                    logging.info(f"[CLUSTERS DETECTED] {clusters[0]:.2f} | {clusters[1]:.2f} (spread: {spread:.4f})")
                    return sorted(clusters)
            return None
        except Exception as e:
            logging.error(f"[CLUSTER ERROR] {e}")
            return None

    def recenter_grids(self, price: Decimal):
        """Rebuild grid(s) based on new center price or detected clusters."""
        if self._stop_event.is_set():
            return
        try:
            clusters = self.detect_clusters()
            if clusters:
                self.setup_grid(clusters[0], dual=True, center2=clusters[1])
            else:
                self.setup_grid(price)
        except Exception as e:
            logging.error(f"[RECENTER ERROR] {e}")

    def check_grids(self, price: Decimal):
        """Evaluate current price vs grid levels."""
        now_ts = time.monotonic()
        self.price_history.append(price)

        if now_ts - self.last_recenter_time > self.recenter_interval or not self.primary_grid:
            self.recenter_grids(price)

        if now_ts - self.last_trade_time < self.cooldown:
            return

        grids = self.primary_grid + (self.secondary_grid if self.mode == "dual" else [])
        centers = [self.primary_center] + ([self.secondary_center] if self.mode == "dual" else [])

        for center, grid in zip(centers, [self.primary_grid, self.secondary_grid] if self.mode == "dual" else [self.primary_grid]):
            for level in grid:
                spread = abs(price - level) / center
                if spread <= self.slippage_threshold:
                    logging.info(f"[GRID HIT] {price:.2f} matched level {level:.2f} | Δ={spread:.5f}")
                    self.executor.execute_trade(adaptive_volume=Decimal('1.0'))
                    self.last_trade_time = now_ts
                    return

    def run(self):
        logging.info("[GRIDBOT] Starting execution...")
        while not self._stop_event.is_set():
            try:
                price = self.safe_now_price()
                if price > 0:
                    self.last_price = price
                    self.check_grids(price)
                else:
                    logging.warning("[INVALID PRICE] Skipping tick.")
                time.sleep(self.refresh_interval)
            except Exception as e:
                logging.error(f"[GRIDBOT ERROR] {e}")
                time.sleep(5)
        logging.info("[GRIDBOT] Stopped.")