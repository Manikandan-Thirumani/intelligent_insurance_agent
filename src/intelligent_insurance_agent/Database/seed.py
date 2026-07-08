"""Seed sample insurance data into a simple in-memory store."""

from __future__ import annotations

from typing import Dict, List

from .database import CLAIMS, POLICIES, POLICY_HOLDERS


def seed_data() -> Dict[str, List[Dict[str, object]]]:
    """Return a simple seed payload that can be used by a future database layer."""
    return {
        "policy_holders": POLICY_HOLDERS,
        "policies": POLICIES,
        "claims": CLAIMS,
    }


if __name__ == "__main__":
    print(seed_data())
