"""Sample insurance-related data for local development and seeding."""

from __future__ import annotations

from typing import Dict, List

POLICY_HOLDERS: List[Dict[str, object]] = [
    {
        "id": "holder-001",
        "name": "Alicia Gomez",
        "policy_number": "POL-1001",
        "plan": "Auto Premium",
        "coverage": ["Collision", "Liability", "Roadside Assistance"],
    },
    {
        "id": "holder-002",
        "name": "Daniel Kim",
        "policy_number": "POL-1002",
        "plan": "HomeShield",
        "coverage": ["Fire", "Theft", "Water Damage"],
    },
]

POLICIES: List[Dict[str, object]] = [
    {
        "policy_number": "POL-1001",
        "type": "auto",
        "premium": 120.0,
        "deductible": 500,
        "status": "active",
    },
    {
        "policy_number": "POL-1002",
        "type": "home",
        "premium": 95.0,
        "deductible": 1000,
        "status": "active",
    },
]

CLAIMS: List[Dict[str, object]] = [
    {
        "claim_id": "CLAIM-2001",
        "policy_number": "POL-1001",
        "status": "pending",
        "incident_type": "car accident",
        "description": "Rear-end collision at an intersection.",
    },
    {
        "claim_id": "CLAIM-2002",
        "policy_number": "POL-1002",
        "status": "approved",
        "incident_type": "water leak",
        "description": "Bathroom pipe burst caused minor water damage.",
    },
]
