import logging
import asyncio

from cdp import CdpClient

from dotenv import load_dotenv

load_dotenv()


async def create_eoa_wallet(name=None):
    logging.debug('Running create_eoa_wallet')
    try:
        async with CdpClient() as cdp: # Instantiate CDP Client
            logging.debug(f"Running with cdp client {cdp}")
            account = await cdp.evm.create_account(name)
            logging.info(f"Created EVM account: {account.address} with name {name}")
        return account
    except Exception as e:
        logging.exception('Exception error:')


async def create_smart_wallet(owner_address=None):
    logging.debug('Running create_smart_wallet')
    try:
        async with CdpClient() as cdp: # Instantiate CDP Client
            if owner_address is None: # If owner_address is not provided
                account = await create_eoa_wallet()
                logging.info(f"Owner account created {account.address}")
            else:
                account = await cdp.evm.get_account(address=owner_address)
                logging.info(f"Owner account obtained {account.address}")
            
            smart_account = await cdp.evm.create_smart_account(account)
            logging.info(f"Created Smart account: {smart_account.address} with owner {smart_account.owners}")
        return smart_account
    except Exception as e:
        logging.exception('Exception error:')


async def fund_wallet(fund_address=None, network="base-sepolia", token="eth"):
    logging.debug('Running fund_wallet')
    try:
        async with CdpClient() as cdp: # Instantiate CDP Client
            if fund_address is None: # If fund_address is not provided
                fund_account = await create_smart_wallet()
                fund_address = fund_account.address
                logging.info(f"Creating new EOA account {fund_address}")

            faucet_hash = await cdp.evm.request_faucet(
                address=fund_address,
                network=network,
                token=token
            )

            if network == "base-sepolia": # Choosing scanner for hash URL
                scanner = "basescan.org"
            else:
                scanner = "etherscan.io"

            logging.info(f"Requested funds from {token} faucet on {network}: https://sepolia.{scanner}/tx/{faucet_hash}")
    except Exception as e:
        logging.exception('Exception error:')