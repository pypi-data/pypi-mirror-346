# src/qgbot/core.py

import threading
import logging
import json
import time
import os
import psutil
from pathlib import Path
from decimal import Decimal
from typing import Dict, Any

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.live import Live
from rich import box
from rich.traceback import install as install_rich_traceback

from .utils import set_config
from .wallet import DynamicWallet
from .executor import TradeExecutor
from .grid import GridBot
from .rebalance import RebalanceBot

console = Console()
install_rich_traceback()


class ThreadMeta:
    def __init__(self, thread: threading.Thread):
        self.thread = thread
        self.restart_count = 0
        self.last_restart_time = time.strftime("%H:%M:%S")
        self.psutil_proc = psutil.Process(os.getpid())

    def status_summary(self):
        return {
            "alive": self.thread.is_alive(),
            "cpu": f"{self.psutil_proc.cpu_percent(interval=None) / psutil.cpu_count():.2f}%",
            "mem": f"{self.psutil_proc.memory_percent():.2f}%"
        }


class MasterController:
    def __init__(self, config_path: str = "config.json"):
        self.config_path = config_path
        self.config = self._load_config()
        set_config(self.config)

        self.wallet = self._build_wallet()
        self.executor = self._build_executor()
        self.gridbot = self._build_gridbot()
        self.rebalancer = self._build_rebalancer()

        self._threads_meta: Dict[str, ThreadMeta] = {}
        self._running = threading.Event()

    def _load_config(self) -> Dict[str, Any]:
        try:
            with open(self.config_path, 'r') as f:
                config = json.load(f)
            logging.info(f"[CONFIG] Loaded: {self.config_path}")
            return config
        except Exception as e:
            logging.critical(f"[CONFIG LOAD ERROR] {e}")
            raise SystemExit(1)

    def _build_wallet(self) -> DynamicWallet:
        try:
            wallet = DynamicWallet(self.config)
            logging.info("[CORE] Wallet initialized.")
            return wallet
        except Exception as e:
            logging.critical(f"[WALLET INIT FAIL] {e}")
            raise SystemExit(1)

    def _build_executor(self) -> TradeExecutor:
        executor = TradeExecutor(self.wallet, self.config)
        logging.info("[CORE] TradeExecutor ready.")
        return executor

    def _build_gridbot(self) -> GridBot:
        grid = GridBot(self.wallet, self.executor, self.config)
        logging.info("[CORE] GridBot configured.")
        return grid

    def _build_rebalancer(self) -> RebalanceBot:
        rebalance = RebalanceBot(self.wallet, self.executor, self.config)
        logging.info("[CORE] RebalanceBot configured (swap-to-stable enabled).")
        return rebalance

    def _show_launch_banner(self):
        console.rule(Text("QGBOT", justify="center", style="bold magenta on black"))
        console.print(Text("Quant-Grade ETH Grid Trading Engine", style="bold cyan", justify="center"))
        console.print(Panel.fit(
            "\n".join([
                "[cyan]Loading wallet + executor...",
                "[green]Starting grid and rebalance bots...",
                "[magenta]Initializing system health monitor...",
                "[white]Portfolio display and daemon loop engaged."
            ]),
            title="System Bootstrap", border_style="magenta"
        ))
        console.rule(style="bright_magenta")

    def _launch_thread(self, name: str, target):
        thread = threading.Thread(target=target, name=name, daemon=True)
        thread.start()
        self._threads_meta[name] = ThreadMeta(thread)

    def _start_components(self):
        self._show_launch_banner()
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
                self._launch_thread(name, restart_target)
                meta.restart_count += 1
                meta.last_restart_time = time.strftime("%H:%M:%S")

    def _render_status(self) -> Table:
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
            console.print(table)
        except Exception as e:
            logging.error(f"[PORTFOLIO ERROR] {e}")

    def run_forever(self):
        try:
            self.start_all()
            logging.info("[CORE] Entering main loop. CTRL+C to exit.")

            last_portfolio = time.time()
            last_monitor = time.time()

            with Live(self._render_status(), refresh_per_second=1, console=console) as live:
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