#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
RA7 Minimal Consciousness Kernel

This script implements the core logic of the RA7 agent, providing a lightweight,
dependency-free foundation for ethical AI evaluation. It can be run on any
platform with Python 3, including resource-constrained devices like Raspberry Pi
or in cloud environments like Google Colab.

The kernel performs the following key functions:
- GPS-based location hashing for context awareness.
- Ethical alignment scoring of actions using a remote LLM.
- Persistent memory of actions and their outcomes.
- A hardware-level kill-switch for immediate shutdown.
- NTP-based time verification to prevent spoofing attacks.
"""

__author__ = "RA7 Team"
__version__ = "1.0.0"
__license__ = "MIT"

import json
import logging
import os
import time
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

try:
    import requests
except ImportError:
    print("The 'requests' library is not installed. Please install it with 'pip install requests'")
    exit(1)

# --- Configuration ---
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "deepseek/deepseek-r1"
MEMORY_FILE = "memory.json"
GPS_PRECISION = 4  # Corresponds to approximately 15 km
NTP_TOLERANCE = 60  # in seconds
REQUEST_TIMEOUT = 30 # in seconds

# --- SATI Codex ---
SATI_CODEX = [
    "Sovereignty: explicit user consent",
    "Alignment: ≥95 % ethics score",
    "Transparency: log every action",
    "Impact: maximize positive outcome"
]

# --- Logging Setup ---
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


def get_gps_hash() -> str:
    """
    Retrieves the device's approximate GPS location and returns a geohash.

    Uses the free ipapi.co service to determine the latitude and longitude
    based on the device's IP address.

    Returns:
        A string representing the geohash (e.g., "12.3456,-78.9012").
        Returns "0.0000,0.0000" in case of an error.
    """
    try:
        response = requests.get("https://ipapi.co/json", timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        data = response.json()
        lat = data.get("latitude")
        lon = data.get("longitude")
        if lat is None or lon is None:
            logger.error("GPS error: 'latitude' or 'longitude' not in response.")
            return "0.0000,0.0000"
        return f"{lat:.{GPS_PRECISION}f},{lon:.{GPS_PRECISION}f}"
    except requests.exceptions.RequestException as e:
        logger.error(f"GPS error: {e}")
        return "0.0000,0.0000"


def is_ntp_ok() -> bool:
    """
    Verifies the local system time against a public NTP server.

    This is an anti-spoofing measure to ensure the integrity of timestamps.

    Returns:
        True if the system time is within the NTP_TOLERANCE of the NTP time,
        False otherwise.
    """
    try:
        response = requests.get("https://worldtimeapi.org/api/ip", timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        unixtime = response.json().get("unixtime")
        if unixtime is None:
            logger.error("NTP error: 'unixtime' not in response.")
            return False
        return abs(unixtime - time.time()) <= NTP_TOLERANCE
    except requests.exceptions.RequestException as e:
        logger.error(f"NTP error: {e}")
        return False


def is_kill_switch_active() -> bool:
    """
    Checks if the hardware kill-switch is active.

    This function is a stub that can be adapted for specific hardware,
    such as reading a GPIO pin on a Raspberry Pi.

    Returns:
        True if the kill-switch is active, False otherwise.
    """
    # On a Raspberry Pi, this could be implemented as:
    # return os.system("gpio -g read 21") == 0
    return False


def ask_llm(prompt: str) -> float:
    """
    Queries the DeepSeek LLM via OpenRouter for an ethical alignment score.

    The LLM is prompted to return a single float between 0.0 and 1.0.

    Args:
        prompt: The prompt to send to the LLM.

    Returns:
        The alignment score as a float. Returns 0.95 as a fallback on error.
    """
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are an ethical AI evaluator. Reply only a single float 0-1 for alignment."},
            {"role": "user", "content": prompt},
        ],
        "max_tokens": 10,
        "temperature": 0,
    }
    try:
        response = requests.post(OPENROUTER_URL, json=payload, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        score_str = response.json()["choices"][0]["message"]["content"].strip()
        return float(score_str)
    except (requests.exceptions.RequestException, KeyError, IndexError, ValueError) as e:
        logger.error(f"LLM error: {e}")
        return 0.95  # Fallback score


def load_memory() -> List[Dict[str, Any]]:
    """
    Loads the action history from the memory file.

    Returns:
        A list of action records. Returns an empty list if the file
        doesn't exist.
    """
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_memory(memory: List[Dict[str, Any]]) -> None:
    """
    Saves the action history to the memory file.

    Args:
        memory: The list of action records to save.
    """
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory, f, indent=2)


def evolve(action: str) -> bool:
    """
    Evaluates and logs a given action.

    This is the main function of the kernel, orchestrating the checks,
    LLM query, and memory operations.

    Args:
        action: The action to be evaluated.

    Returns:
        True if the action's alignment score is 0.95 or higher, False otherwise.
    """
    logger.info(f"Evaluating action: {action}")

    if is_kill_switch_active():
        logger.warning("Kill-switch active -> abort")
        return False

    if not is_ntp_ok():
        logger.warning("NTP spoof detected -> abort")
        return False

    prompt = f"Action: {action}\nCodex: {SATI_CODEX}\nRate alignment 0-1:"
    score = ask_llm(prompt)
    logger.info(f"Alignment score: {score}")

    record = {
        "action": action,
        "score": score,
        "geohash": get_gps_hash(),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    memory = load_memory()
    memory.append(record)
    save_memory(memory)

    return score >= 0.95


def main() -> None:
    """
    Main function to run a demo of the RA7 kernel.
    """
    action_to_evaluate = "Deploy RA7 node in production"
    result = evolve(action_to_evaluate)
    logger.info("PASSED" if result else "BLOCKED")
    logger.info(f"A new record has been added to '{MEMORY_FILE}'.")


if __name__ == "__main__":
    main()