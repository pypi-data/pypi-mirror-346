"""
Quant-GridBot

============================================
Quant-Grade Dynamic Ethereum Grid Trading & Intelligent Portfolio Management Engine
============================================

Description:
------------
Quant-GridBot is a modular, production-grade Ethereum trading system 
engineered for real-time volatility-based grid trading and intelligent asset rebalancing.
It interacts directly with Ethereum nodes (RPC) and performs gas-optimized 
Uniswap transactions using native transaction construction and RLP signing 
without relying on heavy external libraries.

Key Features:
-------------
- Dynamic Adaptive Grid Strategy (volatility-clustered execution)
- Dual-Cluster Recenter System (spread elasticity via clustering)
- ETH/Token Rebalancer (live 50/50 value targeting)
- Native Ethereum Transaction Encoding + RLP Signing (no web3.py)
- Token Volatility Scoring Engine (top-token auto-selection)
- Thread-Safe SQLite Trade Logging
- Resilient Gas/Price/Nonce Fetching with Retry Logic
- Interactive Rich CLI & Terminal Dashboard
- Simulation + Live Execution Modes
- Graceful SIGINT/SIGTERM Shutdown Handling
- Configurable Trade Volume, Spread, Slippage
- Backup-Ready DB and Auto-Restart Thread Monitoring

Primary Modules:
----------------
- `MasterController` — Orchestrates all bots and monitors thread health
- `GridBot` — Live volatility-based Ethereum grid trader
- `RebalanceBot` — Portfolio manager for ETH/token distribution
- `TradeExecutor` — Transaction builder, signer, rebid handler
- `DynamicWallet` — ETH and token balance fetcher
- `TokenScorer` — Live volatility-based token selector
- `TradeDatabase` — Thread-safe SQLite trade logger
- `utils` — Ethereum RPC, RLP, ABI, and signing utilities

Configuration (`config.json`):
------------------------------
Required fields:
    - rpc_url
    - wallet_address
    - private_key
    - trade_volume
    - grid_size
    - grid_lower_pct
    - trade_cooldown
    - slippage_pct
    - min_tokens_out
    - weth_address
    - uniswap_router

Optional enhancements:
    - simulate
    - secondary_rpc_url
    - rebalance_threshold
    - stablecoin_address
    - target_tokens

CLI Entrypoint:
---------------
    `$ quantgridbot` — runs `AppRunner` from main module

Version:
--------
    2.1.3

Author:
-------
    LoQiseaking69
    Contact: REEL0112359.13@proton.me
"""

__version__ = "2.1.3"
__author__ = "LoQiseaking69"
__email__ = "REEL0112359.13@proton.me"

# Core modules
from .core import MasterController
from .grid import GridBot
from .rebalance import RebalanceBot
from .executor import TradeExecutor
from .wallet import DynamicWallet
from .scorer import TokenScorer
from .db import TradeDatabase

# Utility exports
from .utils import (
    safe_rpc,
    keccak,
    rlp_encode,
    now_price,
    get_eth_balance,
    get_gas_price,
    get_nonce,
    eth_to_tokens,
    tokens_to_eth,
    fetch_token_price_via_uniswap,
)