#!/usr/bin/env python3
"""
Main entry point for Mystic Forge executable.
This ensures the main() function is called properly when run as an executable.
"""

import sys
import traceback


try:
    from mystic_forge import main
except ImportError as e:
    print(f"Error importing mystic_forge module: {e}")
    print("Make sure the mystic_forge package is properly installed.")
    sys.exit(1)


def run() -> None:
    """Main entry point with error handling."""
    try:
        main()
    except Exception as e:  # noqa: BLE001
        print(f"Error running mystic_forge: {e}")
        print("\nFull traceback:")
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    run()
