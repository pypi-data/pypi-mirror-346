# src/qgbot/executor.py

import time
import json
import logging
import random
import threading
import requests
from decimal import Decimal, InvalidOperation
from hashlib import sha3_256
from ecdsa import SigningKey, SECP256k1
from typing import Dict, Optional, Any

from .utils import (
    safe_rpc, get_eth_balance, get_gas_price, now_price,
    get_nonce, eth_to_tokens, tokens_to_eth, rlp_encode,
    fetch_token_price_via_uniswap
)
from .scorer import TokenScorer
from .db import log_trade


class TradeExecutor:
    def __init__(self, wallet, config: Dict[str, Any]) -> None:
        self.wallet = wallet
        self.config = config
        self.stop_event = threading.Event()
        self.token_scorer = TokenScorer(config.get("target_tokens", []))

    def sign_tx(self, tx: Dict[str, Any], private_key_hex: str) -> Optional[str]:
        try:
            sk = SigningKey.from_string(bytes.fromhex(private_key_hex.replace('0x', '')), curve=SECP256k1)
            unsigned = [
                tx["nonce"], tx["gasPrice"], tx["gas"],
                bytes.fromhex(tx["to"][2:]), tx["value"],
                tx["data"], tx["chainId"], 0, 0
            ]
            rlp_unsigned = rlp_encode(unsigned)
            tx_hash = sha3_256(rlp_unsigned).digest()
            sig = sk.sign_digest(tx_hash, sigencode=lambda r, s, _: r.to_bytes(32, 'big') + s.to_bytes(32, 'big'))
            r, s = int.from_bytes(sig[:32], 'big'), int.from_bytes(sig[32:], 'big')
            v = tx['chainId'] * 2 + 35 + (1 if s % 2 else 0)
            signed = rlp_encode([*unsigned[:-3], v, r, s])
            return "0x" + signed.hex()
        except Exception as e:
            logging.error(f"[SIGN ERROR] {e}")
            return None

    def send_tx(self, signed_tx_hex: str) -> Optional[str]:
        for attempt in range(3):
            try:
                rpc_url = self.config.get("secondary_rpc_url") if attempt == 1 else self.config["rpc_url"]
                response = requests.post(
                    rpc_url,
                    json={"jsonrpc": "2.0", "method": "eth_sendRawTransaction", "params": [signed_tx_hex], "id": 1},
                    headers={"Content-Type": "application/json"}, timeout=10
                )
                response.raise_for_status()
                result = response.json()
                if "error" in result:
                    raise Exception(result["error"])
                return result["result"]
            except Exception as e:
                logging.error(f"[SEND TX RETRY {attempt+1}] {e}")
                time.sleep(2 * (attempt + 1))
        return None

    def wait_for_receipt(self, tx_hash: str, tx: Optional[Dict[str, Any]] = None, timeout: int = 60) -> Optional[Dict[str, Any]]:
        start = time.time()
        while time.time() - start < timeout:
            try:
                receipt = safe_rpc("eth_getTransactionReceipt", [tx_hash])
                if receipt:
                    logging.info(f"[RECEIPT] TX {tx_hash[:12]} confirmed.")
                    return receipt
                time.sleep(5)
            except Exception as e:
                logging.warning(f"[RECEIPT ERROR] {e}")
        logging.warning(f"[TIMEOUT] TX {tx_hash[:12]} unconfirmed after {timeout}s.")
        if tx:
            return self.rebid_gas_and_resend(tx, tx_hash)
        return None

    def rebid_gas_and_resend(self, tx: Dict[str, Any], tx_hash: str) -> Optional[str]:
        try:
            logging.warning(f"[REBID] Increasing gas for TX {tx_hash[:12]}")
            tx["gasPrice"] = int(Decimal(tx["gasPrice"]) * Decimal("1.25"))
            signed = self.sign_tx(tx, self.config["private_key"])
            if not signed:
                return None
            new_hash = self.send_tx(signed)
            if new_hash:
                self.wait_for_receipt(new_hash)
                return new_hash
        except Exception as e:
            logging.error(f"[REBID ERROR] {e}")
        return None

    def _estimate_gas(self) -> int:
        try:
            price = get_gas_price()
            return int(Decimal(price) * Decimal("1.2"))
        except Exception:
            return 30_000_000_000

    def _check_slippage(self, expected: Decimal, actual: Decimal) -> bool:
        try:
            max_slip = Decimal(str(self.config.get("slippage_pct", 0.02)))
            return abs(expected - actual) <= (expected * max_slip)
        except Exception as e:
            logging.error(f"[SLIPPAGE ERROR] {e}")
            return False

    def _prepare_eth_swap_tx(self, token_out: str, eth_amount: Decimal, nonce: int, gas_price: int) -> Optional[Dict[str, Any]]:
        try:
            deadline = int(time.time()) + 600
            path = [self.config["weth_address"], token_out]
            value_wei = int(eth_amount * Decimal("1e18"))
            data = eth_to_tokens(self.config["min_tokens_out"], path, self.config["wallet_address"], deadline)
            return {
                "nonce": nonce,
                "gasPrice": gas_price,
                "gas": self.config["gas_limit"],
                "to": self.config["uniswap_router"],
                "value": value_wei,
                "data": data,
                "chainId": 1
            }
        except Exception as e:
            logging.error(f"[PREPARE TX ERROR] {e}")
            return None

    def execute_trade(self, adaptive_volume: Decimal = Decimal("1.0")) -> None:
        if self.stop_event.is_set():
            return
        try:
            wallet = self.config["wallet_address"]
            eth_balance = get_eth_balance(wallet)
            gas_price = self._estimate_gas()
            gas_cost_eth = Decimal(gas_price * self.config["gas_limit"]) / Decimal("1e18")
            usable_eth = eth_balance - gas_cost_eth
            if usable_eth <= Decimal("0.001"):
                return
            trade_eth = min(Decimal(self.config["trade_volume"]) * adaptive_volume, usable_eth)
            if trade_eth < Decimal("0.001"):
                return
            nonce = get_nonce(wallet)
            if nonce is None:
                return
            token_out = self.token_scorer.best_token()
            expected = self.safe_get_price()
            tx = self._prepare_eth_swap_tx(token_out, trade_eth, nonce, gas_price)
            actual = self.safe_get_price()
            if not self._check_slippage(expected, actual):
                return
            signed = self.sign_tx(tx, self.config["private_key"])
            if not signed:
                return
            if self.config.get("simulate"):
                logging.info(f"[SIMULATED] Would swap {trade_eth:.5f} ETH to {token_out[:6]}")
                return
            tx_hash = self.send_tx(signed)
            if tx_hash:
                self.wait_for_receipt(tx_hash, tx)
                log_trade(time.strftime('%Y-%m-%d %H:%M:%S'), "SWAP", tx_hash, float(actual), float(trade_eth))
        except Exception as e:
            logging.error(f"[EXECUTE TRADE ERROR] {e}")

    def safe_get_price(self, token: Optional[str] = None) -> Decimal:
        try:
            return fetch_token_price_via_uniswap(token) if token else now_price()
        except Exception:
            return Decimal("0")