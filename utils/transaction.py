import logging
import asyncio

from cdp import CdpClient
from cdp.evm_call_types import EncodedCall

from dotenv import load_dotenv

from web3 import Web3
from decimal import Decimal


load_dotenv()


async def transfer_baseeth(from_smart_address, from_smart_owner, to_address, amount=0):
    logging.debug('Running transfer_eth')
    try:
        async with CdpClient() as cdp: # Instantiate CDP Client
            # Extract smart account inputs
            owner_account = await cdp.evm.get_account(from_smart_owner)
            smart_account = await cdp.evm.get_smart_account(from_smart_address, owner_account)
            logging.info(f"Obtained {smart_account} with owner {smart_account.owners}")
           
           # Send user operation
            user_operation = await cdp.evm.send_user_operation(
                smart_account= smart_account,
                network="base-sepolia",
                calls=[
                    EncodedCall(
                        to=to_address,
                        data="0x",
                        value=Web3.to_wei(Decimal(amount), "ether"),
                    )
                ],
            )
            logging.info(f"User operation status: {user_operation.status}")

            # Wait for user operation confirmation
            logging.debug("Waiting for user operation to be confirmed...")
            user_operation = await cdp.evm.wait_for_user_operation(
                smart_account_address=smart_account.address,
                user_op_hash=user_operation.user_op_hash,
            )
            
            if user_operation.status == "complete":
                logging.info(f"User operation confirmed. Transaction hash: {user_operation.transaction_hash}")
            else:
                logging.error("User operation failed")
    except Exception as e:
        logging.exception('Exception error:')