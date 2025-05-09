# src/qgbot/app.py

import logging
import time
import signal
import sys
from typing import Optional

from .core import MasterController
from .db import TradeDatabase

try:
    from rich.logging import RichHandler
    USE_RICH = True
except ImportError:
    USE_RICH = False


class AppRunner:
    def __init__(self, config_path: str = "config.json") -> None:
        self.config_path = config_path
        self.master: Optional[MasterController] = None
        self.db: Optional[TradeDatabase] = None
        self._running = False

    def start(self) -> None:
        self._configure_logging()
        logging.info("[APP] Starting Quant-GridBot...")

        try:
            self.db = TradeDatabase()
            self.master = MasterController(self.config_path)

            self._running = True
            self._attach_signals()

            self.master.start_all()
            self._run_forever()
        except Exception as e:
            logging.critical(f"[APP INIT ERROR] {e}")
            self.shutdown(exit_code=1)

    def _configure_logging(self):
        try:
            handlers = [RichHandler()] if USE_RICH else [logging.StreamHandler(sys.stdout)]
            logging.basicConfig(
                level=logging.INFO,
                format="%(message)s" if USE_RICH else "%(asctime)s [%(levelname)s] %(message)s",
                handlers=handlers
            )
        except Exception as e:
            print(f"[LOGGING INIT FAILURE] {e}", file=sys.stderr)

    def _attach_signals(self):
        try:
            signal.signal(signal.SIGINT, self.handle_signal)
            signal.signal(signal.SIGTERM, self.handle_signal)
        except Exception as e:
            logging.warning(f"[SIGNAL INIT ERROR] {e}")

    def _run_forever(self):
        try:
            while self._running:
                time.sleep(1)
        except KeyboardInterrupt:
            logging.warning("[APP] CTRL+C received.")
            self.shutdown(0)
        except Exception as e:
            logging.error(f"[APP LOOP ERROR] {e}")
            self.shutdown(1)

    def handle_signal(self, sig: int, frame: Optional[object]):
        logging.warning(f"[SIGNAL] Received signal {sig}.")
        self.shutdown(0)

    def shutdown(self, exit_code: int = 0):
        if not self._running:
            return
        self._running = False
        logging.info("[APP] Initiating shutdown...")
        try:
            if self.master:
                self.master.stop_all()
            if self.db:
                self.db.close()
        except Exception as e:
            logging.error(f"[SHUTDOWN ERROR] {e}")
        logging.info("[APP] Shutdown complete.")
        sys.exit(exit_code)


def main():
    AppRunner().start()