# main.py
from core.network import start_server, start_client
from core.utils import setup_logging  # Make sure utils is imported
import argparse

def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="LSNP Protocol - Peer-to-Peer Networking")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")  # Flag for verbose logging
    parser.add_argument("--server", action="store_true", help="Start as server")
    parser.add_argument("--client", action="store_true", help="Start as client")
    args = parser.parse_args()

    # Set up logging based on the verbose flag
    setup_logging(args.verbose)
    print(f"Verbose mode is set to: {args.verbose}")

    if args.server:
        start_server()  # Starts the server
    elif args.client:
        start_client()  # Starts the client
    else:
        print("Please specify --server or --client to start the application.")

if __name__ == "__main__":
    main()
