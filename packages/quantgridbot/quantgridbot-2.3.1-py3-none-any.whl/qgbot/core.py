# src/qgbot/core.py

import time
import threading
import logging
from dataclasses import dataclass
from decimal import Decimal
from rich.live import Live
from rich.console import Console
from rich.table import Table
from rich import box

from .wallet import DynamicWallet
from .executor import TradeExecutor
from .grid import GridBot
from .rebalance import RebalanceBot
from .config_loader import load_config


@dataclass
class ThreadMeta:
    thread: threading.Thread
    restart_count: int = 0
    last_restart_time: str = "-"
    cpu: str = "-"
    mem: str = "-"
    def status_summary(self):
        return {
            "alive": self.thread.is_alive(),
            "cpu": self.cpu,
            "mem": self.mem
        }


class MasterController:
    def __init__(self, config_path: str = "config.json") -> None:
        self._threads_meta = {}
        self._running = threading.Event()
        self._boot_time = time.time()
        self.config = load_config(config_path)
        self.wallet = DynamicWallet(self.config)
        self.executor = TradeExecutor(self.wallet, self.config)
        self.gridbot = GridBot(self.wallet, self.executor, self.config)
        self.rebalancer = RebalanceBot(self.wallet, self.executor, self.config)
        self.console = Console()

    def _launch_thread(self, name: str, target_fn):
        thread = threading.Thread(target=target_fn, name=name, daemon=True)
        thread.start()
        self._threads_meta[name] = ThreadMeta(thread=thread)
        logging.info(f"[THREAD] {name} started.")

    def _start_components(self):
        self._launch_thread("GridBot", self.gridbot.run)
        self._launch_thread("RebalanceBot", self.rebalancer.run)
        logging.info("[CORE] All components started.")

    def start_all(self):
        if self._running.is_set():
            logging.warning("[CORE] Already running.")
            return
        self._running.set()
        self._threads_meta.clear()
        self._start_components()

    def stop_all(self):
        if not self._running.is_set():
            logging.warning("[CORE] Already stopped.")
            return
        logging.info("[CORE] Shutdown initiated.")
        self._running.clear()

        try:
            self.gridbot.stop()
            self.rebalancer.stop()

            for name, meta in self._threads_meta.items():
                if meta.thread.is_alive():
                    meta.thread.join(timeout=10)
                    if meta.thread.is_alive():
                        logging.warning(f"[CORE] {name} did not shut down cleanly.")
        except Exception as e:
            logging.error(f"[CORE STOP ERROR] {e}")

        logging.info("[CORE] Shutdown complete.")

    def _heartbeat_check(self):
        for name, meta in self._threads_meta.items():
            if not meta.thread.is_alive():
                logging.warning(f"[HEARTBEAT] {name} died. Restarting...")
                restart_target = self.gridbot.run if "Grid" in name else self.rebalancer.run
                if meta.restart_count > 3:
                    time.sleep(min(30, 5 * meta.restart_count))  # backoff
                self._launch_thread(name, restart_target)
                meta.restart_count += 1
                meta.last_restart_time = time.strftime("%H:%M:%S")

    def _render_status(self) -> Table:
        from datetime import datetime
        up_secs = int(time.time() - self._boot_time)
        up_str = f"Uptime: {up_secs // 60}m {up_secs % 60}s"
        logging.debug(up_str)

        table = Table(title="System Threads", box=box.ROUNDED)
        table.add_column("Name", justify="center", style="cyan")
        table.add_column("Alive", justify="center", style="green")
        table.add_column("Restarts", justify="center", style="magenta")
        table.add_column("Last Restart", justify="center", style="yellow")
        table.add_column("CPU %", justify="center", style="bright_green")
        table.add_column("Mem %", justify="center", style="bright_blue")

        for name, meta in self._threads_meta.items():
            status = meta.status_summary()
            alive = "✓" if status["alive"] else "✗"
            table.add_row(
                name, alive, str(meta.restart_count),
                meta.last_restart_time, status["cpu"], status["mem"]
            )
        return table

    def show_portfolio(self):
        try:
            data = self.wallet.fetch_live_tokens()
            total = Decimal("0")
            table = Table(title="Portfolio Overview", box=box.SIMPLE_HEAVY)
            table.add_column("Token", style="cyan")
            table.add_column("Balance", justify="right", style="yellow")
            table.add_column("USD Value", justify="right", style="green")

            for symbol, d in data.items():
                total += d["usd_value"]
                table.add_row(symbol, f"{d['balance']:.6f}", f"${d['usd_value']:.2f}")

            table.add_row("—", "—", "—")
            table.add_row("Total", "", f"[bold green]${total:.2f}[/bold green]")
            self.console.print(table)
        except Exception as e:
            logging.error(f"[PORTFOLIO ERROR] {e}")

    def run_forever(self):
        try:
            self.start_all()
            logging.info("[CORE] Entering main loop. CTRL+C to exit.")

            last_portfolio = time.time()
            last_monitor = time.time()

            with Live(self._render_status(), refresh_per_second=1, console=self.console) as live:
                while self._running.is_set():
                    time.sleep(1)

                    if time.time() - last_monitor >= 5:
                        self._heartbeat_check()
                        live.update(self._render_status())
                        last_monitor = time.time()

                    if time.time() - last_portfolio >= 300:
                        self.show_portfolio()
                        last_portfolio = time.time()

        except KeyboardInterrupt:
            logging.warning("[CORE] Keyboard interrupt received.")
            self.stop_all()
        except Exception as e:
            logging.error(f"[CORE LOOP ERROR] {e}")
            self.stop_all()
