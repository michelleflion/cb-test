import logging
import argparse

from dotenv import load_dotenv
import asyncio

# Importing created functions from utils directory
from utils.wallet2 import create_eoa_wallet, create_smart_wallet, fund_wallet
from utils.transaction2 import transfer_baseeth


# Load .env variables
load_dotenv()

# Configure logging
def configure_logging(level):
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

# Main app function
def main():

    # Initialize CLI Argument Parsing
    parser = argparse.ArgumentParser(description="Coinbase Wallet API v2 App")

    # Add an argument for app logging level
    parser.add_argument(
        '--log-level',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        default='INFO',
        help="Set the logging level (default: INFO)"
    )

    # Adding a command subparser for the different functions
    subparsers = parser.add_subparsers(dest="command")

    # Subcommand for creating EOA wallet
    eoa_parser = subparsers.add_parser("create-eoa", help="Create an Externally Owned Account (EOA) wallet")
    eoa_parser.add_argument("--name", type=str, default=None, help="Name assigned to the account created for future reference (Default: None)")

    # Subcommand for creating a Smart Contract wallet
    smart_parser = subparsers.add_parser("create-smart", help="Create a Smart Contract wallet")
    smart_parser.add_argument("--owner-address", type=str, default=None, help="Address of owner wallet if previously created (Default: None)")

    # Subcommand for funding a wallet from faucet
    fund_parser = subparsers.add_parser("fund-wallet", help="Fund a wallet with a specified token on a specified network")
    fund_parser.add_argument("--address", type=str, default=None, help="The wallet address for faucet funding. If not set, a new EOA wallet will be created (Default: None)")
    fund_parser.add_argument("--network", type=str, default="base-sepolia", help="The network for faucet funding (Default: base-sepolia)")
    fund_parser.add_argument("--token", type=str, default="eth", help="The token for faucet funding (Default: eth)")

    # Subcommand for transferring ETH from Smart Contract wallet
    transfer_parser = subparsers.add_parser("transfer-baseeth", help="Transfer token from smart wallet to a specified EOA wallet")
    transfer_parser.add_argument("--from-smart-address", type=str, help="The smart wallet address to transfer token from")
    transfer_parser.add_argument("--from-smart-owner", type=str, help="The smart wallet address' owner to sign transactions")
    transfer_parser.add_argument("--to-address", type=str, help="Destination address for transfer")
    transfer_parser.add_argument("--amount", type=str, default="0", help="ETH amount to transfer (Default: 0)")

    # Parsing args provided
    args = parser.parse_args()

    # Configure logging based on the user’s chosen level
    log_level = getattr(logging, args.log_level)
    configure_logging(log_level)

    logging.info(f"Logging configured to {args.log_level}")

    # Running respective functions
    if args.command == "create-eoa":
        asyncio.run(create_eoa_wallet(args.name))
    elif args.command == "create-smart":
        asyncio.run(create_smart_wallet(args.owner_address))
    elif args.command == "fund-wallet":
        asyncio.run(fund_wallet(args.address, args.network, args.token))
    elif args.command == "transfer-baseeth":
        # Check if required arguments are provided
        if not args.from_smart_address: 
            print("Error: --from-smart-address is required for transfer")
            return
        if not args.from_smart_owner:
            print("Error: --from-smart-owner is required for transfer")
            return
        if not args.to_address:
            print("Error: --to-address is required for transfer")
            return
        asyncio.run(transfer_baseeth(args.from_smart_address, args.from_smart_owner, args.to_address, args.amount))
    else:
        parser.print_help()


# Run main() function
if __name__ == '__main__':
    main()