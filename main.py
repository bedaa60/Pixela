#!/usr/bin/env python3
"""
Pixela — OTC order book and cross-chain settlement client for the Hurrah contract.

Use as:
- CLI to post, fill, cancel orders and query the Hurrah order book.
- Library for building orders, deriving order IDs, and calling contract views.
- Optional Web3 integration to submit transactions (post, fill, cancel, settlement).
"""

from __future__ import annotations

import argparse
import dataclasses
import hashlib
import json
import os
import random
import sys
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple, Union

APP_NAME = "Pixela"
APP_VERSION = "2.0.0"

# ---------------------------------------------------------------------------
# DATA MODELS
# ---------------------------------------------------------------------------


@dataclass
class OrderParams:
    """Parameters for a single OTC order (maker side)."""
    side: int  # 0 = buy, 1 = sell
    chain_id_origin: int
    chain_id_settle: int
    asset_in: bytes
    asset_out: bytes
    amount_in: int
    amount_out_min: int
    expiry_block: int

    def to_contract_args(self) -> Dict[str, Any]:
        return {
            "side": self.side,
            "chainIdOrigin": self.chain_id_origin,
            "chainIdSettle": self.chain_id_settle,
            "assetIn": self._bytes32(self.asset_in),
            "assetOut": self._bytes32(self.asset_out),
            "amountIn": self.amount_in,
            "amountOutMin": self.amount_out_min,
            "expiryBlock": self.expiry_block,
        }

    @staticmethod
    def _bytes32(b: bytes) -> str:
        if len(b) >= 32:
            return "0x" + b[:32].hex()
        return "0x" + b.hex().zfill(64)
