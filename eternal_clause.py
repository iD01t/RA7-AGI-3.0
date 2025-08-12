#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""RA-7 Eternal Clause Simulator.

This script simulates the deployment and verification of an immutable
"Eternal Clause" as described in the RA-7 governance documents.

- Deploy: Creates a contract file with a clear-text statement and its SHA-256
  hash.
- Verify: Checks if the contract file's content still matches its stored hash.
"""

__author__ = "RA-7 Team (Inspired)"
__version__ = "1.0.0"

import argparse
import hashlib
import json
import os


CONTRACT_FILE = "EternalLock.sol_lock"


def calculate_hash(content: str) -> str:
    """Calculate the SHA-256 hash of a string."""
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def deploy_clause() -> None:
    """Deploy the Eternal Clause."""
    if os.path.exists(CONTRACT_FILE):
        print(
            f"'{CONTRACT_FILE}' already exists. Deployment aborted to preserve immutability."
        )
        return

    print("Deploying the Eternal Clause...")

    eternal_clause_content = "No upgrade path in EternalLock.sol contract. DAO cannot override."
    content_hash = calculate_hash(eternal_clause_content)

    contract_data = {
        "clause_content": eternal_clause_content,
        "deployment_hash": content_hash,
        "note": "This file represents an immutable contract. Its hash must always match its content.",
    }

    with open(CONTRACT_FILE, "w", encoding="utf-8") as f:
        json.dump(contract_data, f, indent=2)

    print(f"✅ Eternal Clause deployed to '{CONTRACT_FILE}'.")
    print(f"   Hash: {content_hash}")


def verify_clause() -> None:
    """Verify the integrity of the Eternal Clause."""
    if not os.path.exists(CONTRACT_FILE):
        print(f"Error: Contract file '{CONTRACT_FILE}' not found. Cannot verify.")
        return

    print(f"Verifying integrity of '{CONTRACT_FILE}'...")

    try:
        with open(CONTRACT_FILE, "r", encoding="utf-8") as f:
            contract_data = json.load(f)

        content = contract_data.get("clause_content")
        stored_hash = contract_data.get("deployment_hash")

        if not content or not stored_hash:
            print("❌ Verification Failed: Contract file is corrupted or missing key fields.")
            return

        current_hash = calculate_hash(content)

        print(f"   Stored Hash:   {stored_hash}")
        print(f"   Calculated Hash: {current_hash}")

        if current_hash == stored_hash:
            print("\n✅ Verification Successful: The Eternal Clause is intact and immutable.")
        else:
            print("\n❌ VERIFICATION FAILED: The contract has been tampered with. IMMUTABILITY VIOLATED.")

    except (json.JSONDecodeError, KeyError) as e:
        print(f"❌ Verification Failed: Error reading contract file. Details: {e}")


def main() -> None:
    """Handle deployment and verification."""
    parser = argparse.ArgumentParser(
        description="RA-7 Eternal Clause Simulator",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--deploy", action="store_true", help="Deploy the immutable contract."
    )
    group.add_argument(
        "--verify", action="store_true", help="Verify the integrity of the contract."
    )

    args = parser.parse_args()

    if args.deploy:
        deploy_clause()
    elif args.verify:
        verify_clause()


if __name__ == "__main__":
    main()
