import sys
import os

# Add the backend directory to the Python path to allow imports
backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

from cli import run_cli

def main():
    """Main entry point for the application."""
    try:
        run_cli()
    except KeyboardInterrupt:
        print("\n\nApplication interrupted by user. Exiting.")
        sys.exit(0)

if __name__ == "__main__":
    main()