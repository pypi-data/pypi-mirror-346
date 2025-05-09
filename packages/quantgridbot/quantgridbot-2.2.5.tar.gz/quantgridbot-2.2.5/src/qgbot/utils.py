# src/qgbot/utils.py

import json
import logging
import requests
from decimal import Decimal, InvalidOperation
from typing import Optional, Any, List, Union
from eth_utils import keccak as eth_keccak

_config = None  # Private config singleton


# === CONFIG MANAGEMENT ===

def set_config(c: dict) -> None:
    global _config
    _config = c

def require_config() -> None:
    if _config is None:
        raise RuntimeError("Configuration not loaded. Use set_config(config) first.")


# === SAFE RPC WRAPPER ===

def safe_rpc(method: str, params: list, retries: int = 3) -> Optional[Any]:
    require_config()
    url = _config.get("rpc_url")
    if not url:
        raise ValueError("RPC URL missing in config.")

    for attempt in range(retries):
        try:
            payload = {"jsonrpc": "2.0", "method": method, "params": params, "id": 1}
            headers = {'Content-Type': 'application/json'}
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            response.raise_for_status()
            result = response.json()
            if 'error' in result:
                raise Exception(result['error'])
            return result.get("result")
        except Exception as e:
            logging.error(f"[SAFE_RPC RETRY {attempt+1}] {method}: {e}")
    logging.error(f"[SAFE_RPC FAILURE] {method} retries exhausted.")
    return None


# === BASIC ENCODERS ===

def keccak(data: Union[str, bytes]) -> bytes:
    if isinstance(data, str):
        data = bytes.fromhex(data.replace("0x", ""))
    return eth_keccak(data)

def rlp_encode(item: Any) -> bytes:
    """Minimal RLP encoder."""
    if isinstance(item, int):
        return rlp_encode(item.to_bytes((item.bit_length() + 7) // 8 or 1, 'big'))
    elif isinstance(item, bytes):
        if len(item) == 1 and item[0] < 0x80:
            return item
        elif len(item) <= 55:
            return bytes([0x80 + len(item)]) + item
        else:
            length = len(item)
            length_bytes = length.to_bytes((length.bit_length() + 7) // 8, 'big')
            return bytes([0xb7 + len(length_bytes)]) + length_bytes + item
    elif isinstance(item, list):
        encoded = b''.join(rlp_encode(x) for x in item)
        if len(encoded) <= 55:
            return bytes([0xc0 + len(encoded)]) + encoded
        else:
            length_bytes = len(encoded).to_bytes((len(encoded).bit_length() + 7) // 8, 'big')
            return bytes([0xf7 + len(length_bytes)]) + length_bytes + encoded
    raise TypeError(f"[RLP ERROR] Unsupported type: {type(item)}")


# === MARKET DATA UTILITIES ===

def now_price(token_address: Optional[str] = None) -> Decimal:
    require_config()
    try:
        if not token_address:
            result = safe_rpc("eth_call", [{
                "to": _config["price_feed_address"],
                "data": "0xfeaf968c"
            }, "latest"])
            if result and len(result) >= 194:
                price = Decimal(int(result[130:194], 16)) / Decimal('1e8')
                return price if price > 0 else Decimal('0')
        else:
            return fetch_token_price_via_uniswap(token_address)
    except Exception as e:
        logging.error(f"[NOW_PRICE ERROR] {e}")
        return Decimal("0")


def get_eth_balance(address: str) -> Decimal:
    try:
        balance = safe_rpc("eth_getBalance", [address, "latest"])
        return Decimal(int(balance, 16)) / Decimal("1e18") if balance else Decimal("0")
    except Exception as e:
        logging.error(f"[BALANCE ERROR] {e}")
        return Decimal("0")

def get_gas_price() -> int:
    try:
        gas = safe_rpc("eth_gasPrice", [])
        return int(gas, 16) if gas else 0
    except Exception as e:
        logging.error(f"[GAS ERROR] {e}")
        return 0

def get_nonce(address: str) -> int:
    try:
        nonce = safe_rpc("eth_getTransactionCount", [address, "latest"])
        return int(nonce, 16) if nonce else 0
    except Exception as e:
        logging.error(f"[NONCE ERROR] {e}")
        return 0


# === ENCODERS FOR UNISWAP TRADES ===

def eth_to_tokens(min_tokens_out: int, path: List[str], to: str, deadline: int) -> bytes:
    try:
        method = '7ff36ab5'
        encoded = (
            method +
            hex(min_tokens_out)[2:].rjust(64, '0') +
            hex(len(path))[2:].rjust(64, '0') +
            ''.join(x.lower().replace('0x', '').rjust(64, '0') for x in path) +
            to.lower().replace('0x', '').rjust(64, '0') +
            hex(deadline)[2:].rjust(64, '0')
        )
        return bytes.fromhex(encoded)
    except Exception as e:
        logging.error(f"[ENCODE ETH->TOKENS ERROR] {e}")
        return b''

def tokens_to_eth(amount_in: int, amount_out_min: int, path: List[str], to: str, deadline: int) -> bytes:
    try:
        method = '18cbafe5'
        encoded = (
            method +
            hex(amount_in)[2:].rjust(64, '0') +
            hex(amount_out_min)[2:].rjust(64, '0') +
            hex(len(path))[2:].rjust(64, '0') +
            ''.join(x.lower().replace('0x', '').rjust(64, '0') for x in path) +
            to.lower().replace('0x', '').rjust(64, '0') +
            hex(deadline)[2:].rjust(64, '0')
        )
        return bytes.fromhex(encoded)
    except Exception as e:
        logging.error(f"[ENCODE TOKENS->ETH ERROR] {e}")
        return b''


# === UNISWAP PRICE FETCHER ===

def fetch_token_price_via_uniswap(token_address: str) -> Decimal:
    """Fetch token price from Uniswap router using getAmountsOut."""
    require_config()
    try:
        router = _config.get("uniswap_router")
        weth = _config.get("weth_address")
        if not router or not weth:
            raise ValueError("Router or WETH missing from config.")

        # Dummy call: getAmountsOut(1, [token, WETH])
        data = (
            "0x54cf2aeb" +
            "0000000000000000000000000000000000000000000000000000000000000064" +  # 100
            "0000000000000000000000000000000000000000000000000000000000000042" +  # 66
            token_address.lower().replace('0x', '').rjust(64, '0') +
            weth.lower().replace('0x', '').rjust(64, '0')
        )
        result = safe_rpc("eth_call", [{"to": router, "data": data}, "latest"])
        if result and len(result) >= 130:
            amount_out = int(result[-64:], 16)
            return Decimal(amount_out) / Decimal("1e18") if amount_out > 0 else Decimal("0")
    except Exception as e:
        logging.error(f"[UNISWAP PRICE ERROR] {e}")
    return Decimal("0")