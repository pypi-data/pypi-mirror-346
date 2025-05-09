import logging
import time
import signal
import sys
import threading
from datetime import datetime
from typing import Optional

from .core import MasterController
from .db import TradeDatabase

try:
    from rich.logging import RichHandler
    from rich.console import Console
    from rich.panel import Panel
    from rich.text import Text
    USE_RICH = True
    console = Console()
except ImportError:
    USE_RICH = False
    console = None


class AppRunner:
    def __init__(self, config_path: str = "config.json") -> None:
        self.config_path = config_path
        self.master: Optional[MasterController] = None
        self.db: Optional[TradeDatabase] = None
        self._running: bool = False
        self._boot_time = datetime.utcnow()
        self._loop_count = 0
        self._last_heartbeat = time.time()

    def start(self) -> None:
        self._configure_logging()
        self._show_banner("QGBOT", "Quant-Grade ETH Grid Trading Engine")
        self._log_boot_steps()

        try:
            self.db = TradeDatabase()
            self.master = MasterController(self.config_path)

            self._running = True
            self._attach_signals()

            self.master.start_all()
            self._run_forever()

        except Exception as e:
            logging.critical(f"[APP INIT ERROR] {e}", exc_info=True)
            self.shutdown(exit_code=1)

    def _configure_logging(self):
        handlers = [RichHandler()] if USE_RICH else [logging.StreamHandler(sys.stdout)]
        logging.basicConfig(
            level=logging.INFO,
            format="%(message)s" if USE_RICH else "%(asctime)s [%(levelname)s] %(message)s",
            handlers=handlers
        )
        logging.info("[LOGGING] Initialized RichHandler" if USE_RICH else "[LOGGING] Fallback logger active")

    def _attach_signals(self):
        try:
            signal.signal(signal.SIGINT, self.handle_signal)
            signal.signal(signal.SIGTERM, self.handle_signal)
        except Exception as e:
            logging.warning(f"[SIGNAL INIT ERROR] {e}")

    def _run_forever(self):
        try:
            while self._running:
                start = time.time()
                time.sleep(1)
                self._loop_count += 1

                if self._loop_count % 60 == 0:  # Every minute
                    uptime = datetime.utcnow() - self._boot_time
                    lag = time.time() - start
                    logging.info(f"[STATUS] Uptime: {str(uptime).split('.')[0]} | Loop lag: {lag:.3f}s")

        except KeyboardInterrupt:
            logging.warning("[APP] CTRL+C received.")
            self.shutdown(0)
        except Exception as e:
            logging.error(f"[APP LOOP ERROR] {e}", exc_info=True)
            self.shutdown(1)

    def _log_boot_steps(self):
        if USE_RICH:
            panel = Panel.fit(
                "[bold cyan]Loading wallet + executor...\n"
                "[bold yellow]Starting grid and rebalance bots...\n"
                "[bold green]Initializing system health monitor...\n"
                "[bold magenta]Portfolio display and daemon loop engaged.",
                title="[ QGBOT SYSTEM BOOTSTRAP ]", border_style="bright_magenta"
            )
            console.print(panel)
        else:
            logging.info("[BOOT] Wallet + executor init")
            logging.info("[BOOT] Grid + rebalance bots starting")
            logging.info("[BOOT] System monitor active")
            logging.info("[BOOT] Portfolio tracking started")

    def _show_banner(self, title: str, subtitle: str):
        if USE_RICH and console:
            console.rule(f"[bold magenta]{title}")
            console.print(f"[cyan]{subtitle}")
            console.rule()
        else:
            logging.info(f"[{title}] {subtitle}")

    def handle_signal(self, sig: int, frame: Optional[object]):
        logging.warning(f"[SIGNAL] Received signal {sig}.")
        self.shutdown(0)

    def shutdown(self, exit_code: int = 0):
        if not self._running:
            return
        self._running = False
        logging.info("[APP] Initiating shutdown sequence...")
        try:
            if self.master:
                self.master.stop_all()
            if self.db:
                self.db.close()
        except Exception as e:
            logging.error(f"[SHUTDOWN ERROR] {e}", exc_info=True)
        logging.info("[APP] Shutdown complete.")
        sys.exit(exit_code)


def main():
    AppRunner().start()
