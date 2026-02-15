"""Main entry point for the Euler Path Console Application."""

import sys

from src.io_handler import load_graph_from_json, save_result_to_json
from src.console_input import read_graph_from_console
from src.hierholzer import find_euler_path as hierholzer_find
from src.fleury import find_euler_path as fleury_find


ALGORITHM_MAP = {
    "1": ("hierholzer", hierholzer_find),
    "2": ("fleury", fleury_find),
}


def main() -> None:
    """Run the Euler Path Console Application in a loop."""
    print("=" * 50)
    print("  Euler Path Finder")
    print("=" * 50)

    while True:
        print("\n--- Main Menu ---")
        print("  1 — Manual input")
        print("  2 — Load from JSON file")
        print("  0 — Exit")

        choice = input("\nYour choice: ").strip()

        if choice == "0":
            print("Goodbye!")
            break

        if choice == "1":
            graph = _input_manual()
        elif choice == "2":
            graph = _input_json()
        else:
            print(f"Error: invalid choice '{choice}'. Expected 0, 1, or 2.")
            continue

        if graph is None:
            continue

        # Choose algorithm
        print("\nChoose algorithm:")
        print("  1 — Hierholzer")
        print("  2 — Fleury")

        algo_choice = input("\nYour choice (1/2): ").strip()

        if algo_choice not in ALGORITHM_MAP:
            print(f"Error: invalid choice '{algo_choice}'. Expected 1 or 2.")
            continue

        algo_name, algo_func = ALGORITHM_MAP[algo_choice]

        # Run algorithm
        euler_path = algo_func(graph)

        print(f"\n{'=' * 50}")
        print(f"  Algorithm: {algo_name}")
        print(f"  Euler path: {euler_path}")
        print(f"  Path length (edges): {len(euler_path) - 1}")
        print(f"{'=' * 50}")

        # Optionally save result
        save_choice = input("\nSave result to JSON file? (y/n): ").strip().lower()

        if save_choice == "y":
            filepath = input("Enter output file path: ").strip()
            if not filepath:
                print("Error: file path must not be empty.")
                continue
            save_result_to_json(filepath, euler_path, algo_name)
            print(f"Result saved to: {filepath}")


def _input_manual():
    """Handle manual graph input. Returns graph or None on error."""
    print("\n--- Manual Graph Input ---")
    return read_graph_from_console()


def _input_json():
    """Handle JSON file graph input. Returns graph or None on error."""
    filepath = input("\nEnter JSON file path: ").strip()
    if not filepath:
        print("Error: file path must not be empty.")
        return None
    return load_graph_from_json(filepath)


if __name__ == "__main__":
    main()
