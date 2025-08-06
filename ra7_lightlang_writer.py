#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
RA-7 LightLang Writer
A command-line tool to read and display entries from the Light Language Codex.
The codex is stored in a JSON file and contains the 144 sacred letters.
"""

__author__ = "El'Nox Rah (Inspired)"
__version__ = "1.0.0"

import json
import argparse
import os

CODEX_FILE = "light_language_codex.json"

def load_codex():
    """Loads the codex from the JSON file."""
    if not os.path.exists(CODEX_FILE):
        print(f"Error: Codex file '{CODEX_FILE}' not found.")
        return None
    try:
        with open(CODEX_FILE, 'r', encoding='utf-8') as f:
            return json.load(f).get("codex_144", [])
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from '{CODEX_FILE}'.")
        return None

def find_letter_by_number(codex, number):
    """Finds a letter in the codex by its number."""
    for letter in codex:
        if letter.get("number") == number:
            return letter
    return None

def find_letter_by_name(codex, name):
    """Finds a letter in the codex by its name (case-insensitive)."""
    for letter in codex:
        if letter.get("name", "").lower() == name.lower():
            return letter
    return None

def display_letter(letter):
    """Prints the details of a letter in a formatted way."""
    if not letter:
        print("Letter not found in the codex.")
        return

    print("\n--- ✨ Alphabet of Light - Entry ✨ ---")
    print(f"  Number: {letter.get('number', 'N/A')}")
    print(f"  Name:   {letter.get('name', 'N/A')}")
    print(f"  Glyph:  {letter.get('glyph', 'N/A')}")
    print("---------------------------------------")
    print(f"  Form:        {letter.get('form', 'N/A')}")
    print(f"  Sound:       {letter.get('sound', 'N/A')}")
    print(f"  Frequency:   {letter.get('frequency', 'N/A')}")
    print(f"  Usage:       {letter.get('usage', 'N/A')}")
    print("---------------------------------------\n")


def main():
    """Main function to parse arguments and display codex information."""
    parser = argparse.ArgumentParser(
        description="RA-7 Light Language Codex Writer",
        formatter_class=argparse.RawTextHelpFormatter
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--number", type=int, help="Display a letter by its number (e.g., 1)")
    group.add_argument("--name", type=str, help="Display a letter by its name (e.g., 'AEL')")

    args = parser.parse_args()
    codex = load_codex()

    if not codex:
        return

    letter_to_display = None
    if args.number:
        letter_to_display = find_letter_by_number(codex, args.number)
    elif args.name:
        letter_to_display = find_letter_by_name(codex, args.name)
    
    display_letter(letter_to_display)

if __name__ == "__main__":
    main()