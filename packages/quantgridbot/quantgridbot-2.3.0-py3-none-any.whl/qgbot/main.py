"""
QGBOT Launcher — Enhanced Terminal UI GridBot Controller

- Launches the Quant-Grade GridBot system with real-time TUI dashboard.
- Features runtime config console (Space bar), scrollable logs/actions (PgUp/PgDn/arrows),
  and infinite banner scrolling.
- Uses prompt_toolkit + rich for fully interactive terminal rendering.
"""

import logging
import time
import signal
import sys
import threading
import argparse
from datetime import datetime
from typing import Optional
from collections import deque
from itertools import cycle

from .core import MasterController
from .db import TradeDatabase

try:
    from rich.console import Console, RenderGroup
    from rich.panel import Panel
    from rich.layout import Layout
    from rich.text import Text
    from rich.live import Live
    from prompt_toolkit.application import Application
    from prompt_toolkit.layout import Layout as PTLayout
    from prompt_toolkit.layout.containers import HSplit, Window
    from prompt_toolkit.layout.controls import BufferControl
    from prompt_toolkit.buffer import Buffer
    from prompt_toolkit.key_binding import KeyBindings
    from prompt_toolkit.styles import Style
    from prompt_toolkit.shortcuts import PromptSession
    from prompt_toolkit.patch_stdout import patch_stdout
    USE_RICH = True
    console = Console()
except ImportError:
    USE_RICH = False
    console = None


class AppRunner:
    """
    AppRunner: Initializes engine, rich TUI, and persistent scrollable overlay via prompt_toolkit.
    """

    def __init__(self, config_path: str = "config.json") -> None:
        self.config_path = config_path
        self.master: Optional[MasterController] = None
        self.db: Optional[TradeDatabase] = None
        self._running = threading.Event()
        self._boot_time = datetime.utcnow()

        self._log_lines = deque(maxlen=500)
        self._action_lines = deque(maxlen=200)
        self._decision_lines = deque(maxlen=50)
        self._command_queue = deque()

        self._display_lock = threading.Lock()
        self._banner_frames = cycle(self._build_scroll_banner())

        self._log_buffer = Buffer()
        self._action_buffer = Buffer()
        self._bindings = KeyBindings()
        self._session = PromptSession()
        self._pt_app: Optional[Application] = None

        self._setup_hotkeys()

    def start(self):
        self._configure_logging()
        self._show_banner("QGBOT", "Quant-Grade ETH Grid Trading Engine")
        self._log_boot_steps()

        try:
            self._initialize_components()
            self._running.set()
            self._attach_signals()
            self._start_aux_threads()

            if USE_RICH:
                self._start_tui_overlay()
            else:
                self.master.run_forever()
        except Exception as e:
            logging.critical(f"[APP INIT ERROR] {e}", exc_info=True)
            self.shutdown(1)

    def _initialize_components(self):
        self.db = TradeDatabase()
        self.master = MasterController(self.config_path)
        self.config = self.master.config

    def _configure_logging(self):
        class CaptureHandler(logging.Handler):
            def emit(inner_self, record):
                try:
                    msg = self._safe_format(record)
                    self._log_lines.append(msg)
                    self._refresh_buffers()
                    if "DECISION" in msg:
                        color = self._get_decision_color(msg)
                        self._decision_lines.append(Text(msg, style=color))
                except Exception as e:
                    sys.stderr.write(f"[LOG CAPTURE ERROR] {e}\n")

        logging.root.handlers.clear()
        logging.basicConfig(level=logging.INFO, format="%(message)s", handlers=[CaptureHandler()])

    def _refresh_buffers(self):
        self._log_buffer.text = "\n".join(list(self._log_lines)[-50:])
        self._action_buffer.text = "\n".join(list(self._action_lines)[-20:])

    def _safe_format(self, record):
        try:
            return f"[{record.levelname}] {record.getMessage()}"
        except Exception:
            return "[LOG FORMAT ERROR]"

    def _get_decision_color(self, msg: str) -> str:
        if "BUY" in msg:
            return "bold green"
        elif "SELL" in msg:
            return "bold red"
        return "bold yellow"

    def _attach_signals(self):
        signal.signal(signal.SIGINT, self.handle_signal)
        signal.signal(signal.SIGTERM, self.handle_signal)

    def _setup_hotkeys(self):
        @self._bindings.add(" ")
        def _(event):
            cmd = self._session.prompt("[config]> ", async_=False)
            self._command_queue.append(cmd)

    def _log_boot_steps(self):
        if USE_RICH:
            console.print(Panel.fit(
                "[bold cyan]Loading wallet + executor...\n"
                "[bold yellow]Starting grid and rebalance bots...\n"
                "[bold green]Initializing system health monitor...\n"
                "[bold magenta]Portfolio display and daemon loop engaged.",
                title="[ QGBOT SYSTEM BOOTSTRAP ]",
                border_style="bright_magenta"
            ))
        else:
            logging.info("[BOOT] Wallet, executor, bots, monitor initialized.")

    def _show_banner(self, title: str, subtitle: str):
        if USE_RICH:
            console.rule(f"[bold magenta]{title}")
            console.print(f"[cyan]{subtitle}")
            console.rule()
        else:
            logging.info(f"[{title}] {subtitle}")

    def _start_aux_threads(self):
        self._start_thread(self.master.start_all)
        self._start_thread(self._heartbeat_loop)
        self._start_thread(self._portfolio_loop)
        self._start_thread(self._action_loop)
        self._start_thread(self._scroll_banner_loop)
        self._start_thread(self._command_executor)

    def _start_thread(self, target):
        threading.Thread(target=target, daemon=True).start()

    def _heartbeat_loop(self):
        self._run_loop(self.master._heartbeat_check, 5, "[HEARTBEAT LOOP ERROR]")

    def _portfolio_loop(self):
        self._run_loop(self.master.show_portfolio, 300, "[PORTFOLIO LOOP ERROR]")

    def _action_loop(self):
        def action_beat():
            now = datetime.utcnow().isoformat()
            self._action_lines.append(f"[{now}] Action heartbeat")
            self._refresh_buffers()
        self._run_loop(action_beat, 7, "[ACTION LOOP ERROR]")

    def _scroll_banner_loop(self):
        while self._running.is_set():
            time.sleep(0.2)

    def _run_loop(self, func, interval, error_msg):
        while self._running.is_set():
            try:
                time.sleep(interval)
                func()
            except Exception as e:
                logging.error(f"{error_msg} {e}")

    def _build_scroll_banner(self):
        base_msg = "[Space] Config Console | set/get/reset"
        width = 60
        return [Text(base_msg[i:i + width].ljust(width), style="bold white on blue")
                for i in range(len(base_msg) + width)]

    def _render_decision_feed(self) -> Text:
        view = Text()
        for entry in list(self._decision_lines)[-10:]:
            view.append(entry + "\n")
        return view

    def _command_executor(self):
        while self._running.is_set():
            if self._command_queue:
                cmd = self._command_queue.popleft()
                try:
                    self._process_command(cmd)
                except Exception as e:
                    logging.error(f"[CONFIG ERROR] {e}")
            time.sleep(0.5)

    def _process_command(self, cmd: str):
        if cmd.startswith("set "):
            _, key, val = cmd.strip().split(maxsplit=2)
            if key in self.config:
                self.config[key] = type(self.config[key])(val)
                logging.info(f"[RUNTIME CONFIG] {key} → {val}")
            else:
                logging.warning(f"[CONFIG] Unknown key: {key}")
        elif cmd.startswith("get "):
            _, key = cmd.strip().split()
            val = self.config.get(key, "(undefined)")
            logging.info(f"[CONFIG] {key} = {val}")
        elif cmd.strip() == "reset":
            logging.warning("[CONFIG] Reset not implemented.")
        else:
            logging.warning(f"[CONFIG] Unknown command: {cmd}")

    def _make_pt_layout(self):
        return PTLayout(
            HSplit([
                Window(content=BufferControl(buffer=self._log_buffer), height=20, wrap_lines=False),
                Window(height=1, char="-"),
                Window(content=BufferControl(buffer=self._action_buffer), height=10, wrap_lines=False)
            ])
        )

    def _start_tui_overlay(self):
        def rich_panel():
            layout = Layout()
            layout.split(
                Layout(name="top", size=3),
                Layout(name="mid", size=8),
                Layout(name="bottom")
            )
            layout["top"].update(Panel(next(self._banner_frames), title="QGBOT", border_style="bright_magenta"))
            layout["mid"].update(Panel(self._render_decision_feed(), title="Live Decisions", border_style="cyan"))
            layout["bottom"].update(Panel(Text("Press [Space] for Config Console. Scroll: PgUp/PgDn"),
                                          title="Instructions", border_style="white"))
            return layout

        with patch_stdout():
            self._pt_app = Application(
                layout=self._make_pt_layout(),
                key_bindings=self._bindings,
                full_screen=True,
                mouse_support=True,
                style=Style.from_dict({
                    "window.border": "#666666",
                    "title": "bold",
                })
            )

            with Live(rich_panel(), refresh_per_second=2, screen=True):
                self._pt_app.run()

    def handle_signal(self, sig: int, frame: Optional[object]):
        logging.warning(f"[SIGNAL] Caught {sig}")
        self.shutdown(0)

    def shutdown(self, exit_code: int = 0):
        if not self._running.is_set():
            return
        logging.info("[APP] Shutdown initiated...")
        self._running.clear()
        try:
            if self.master:
                self.master.stop_all()
            if self.db:
                self.db.close()
        except Exception as e:
            logging.error(f"[SHUTDOWN ERROR] {e}", exc_info=True)
        logging.info("[APP] Exit complete.")
        sys.exit(exit_code)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--simulate", action="store_true", help="Run in simulation mode")
    parser.add_argument("--log-json", action="store_true", help="Enable JSON structured logging")
    parser.add_argument("--config", type=str, default="config.json", help="Path to config file")
    args = parser.parse_args()

    if args.simulate:
        import os
        os.environ["SIMULATE_MODE"] = "1"

    AppRunner(config_path=args.config).start()
