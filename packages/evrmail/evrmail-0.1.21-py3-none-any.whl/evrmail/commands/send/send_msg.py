# ─────────────────────────────────────────────────────────
# 📬 evrmail.send.msg
#
# 📜 USAGE:
#   $ evrmail send msg --to <recipient> --outbox <ASSET> --file <path>
#
# 🛠️ DESCRIPTION:
#   Sends a message by transferring a tagged asset with an IPFS CID.
#   Uses the asset name in --outbox to determine the sender address.
#
# 🔧 OPTIONS:
#   --to         Recipient Evrmore address
#   --outbox     Owned asset name (e.g. EVRMAIL~PHOENIX) to send from
#   --file       Path to the message file to upload to IPFS
#   --fee-rate   Fee rate in EVR per kB (default: 0.01)
#   --dry-run    Simulate transaction without broadcasting
#   --debug      Show debug info
#   --raw        Output raw JSON (dry-run only)
# ─────────────────────────────────────────────────────────

import math
import json
import typer
from typing import Optional
from evrmail.commands.ipfs import ipfs_add
from evrmail.wallet.addresses import get_outbox_address, get_all_addresses
from evrmail.wallet.tx.create.send_asset import create_send_asset_transaction

send_msg_app = typer.Typer()
__all__ = ["send_msg_app"]

@send_msg_app.command(name="msg", help="📬 Send an IPFS-backed message")
def send_msg(
    to: str = typer.Option(..., "--to", help="📥 Recipient Evrmore address"),
    outbox: Optional[str] = typer.Option(None, "--outbox", help="📤 Your outbox asset (e.g. EVRMAIL~PHOENIX)"),
    subject: str = typer.Option(..., "--subject", help="📝 Subject of the message"),
    content: str = typer.Option(..., "--content", help="📝 Content of the message"),
    fee_rate: float = typer.Option(0.01, "--fee-rate", help="💸 Fee rate in EVR per kB"),
    dry_run: bool = typer.Option(False, "--dry-run", help="🧪 Simulate transaction without sending"),
    debug: bool = typer.Option(False, "--debug", help="🔍 Show debug info"),
    raw: bool = typer.Option(False, "--raw", help="📄 Output raw JSON (dry-run only)")
):
    from evrmail.utils.create_message_payload import create_message_payload
    from evrmail import rpc_client
    from evrmail.wallet import addresses 
    import sys   
  
  
    # Check the fee rate, min is 0.01 EVR/kB
    if fee_rate:
        fee_rate = math.ceil(int(fee_rate * 1e8))  # EVR → satoshis

    from evrmail.wallet.addresses import validate
    valid = validate(to)
    to_address = None
    if valid.get('isvalid'):
        # user provided an evrmore address
        from evrmail.config import load_config
        config = load_config()
        contacts = config.get("contacts")
        for contact in contacts:
            if contact == to:
                to_address = to
                to_pubkey = contacts.get(contact).get("pubkey")
        if not to_address:
            print(f"{to} is not in your contacts")
            sys.exit(1)

    else:
        # user did not provide evrmore address, lets assume its a friendly name
        from evrmail.config import load_config
        config = load_config()
        contacts = config.get("contacts")
        for contact in contacts:
            if contacts.get(contact).get("friendly_name") == to:
                to_address = contact
                to_pubkey = contacts.get(contact).get("pubkey")
        if not to_address:
            print(f"{to} is not in your contacts")
            sys.exit(1)

    # Now we have know we have a valid to address and to pubkey for encryption
    # Time to find a suitable from address, one with an asset
    from_address = None
    outbox_balance = None
    if outbox:
        from_address = get_outbox_address(outbox)
        if not from_address:
            print(f"You do not own {outbox}")
            sys.exit(1)
        
        balances = rpc_client.getaddressbalance({"addresses": [from_address]}, True)
        for balance in balances:
            if balance.get("assetName") == outbox:
                if balance.get("balance") > 576:
                    outbox_balance = balance.get("balance")
                else:
                    print(f"You do not own a suitible amount of {outbox_balance} to send a message.")
                    sys.exit(1)
    else:
        wallet_addresses = get_all_addresses()
        balances = rpc_client.getaddressbalance({"addresses": wallet_addresses}, True)
        for balance in balances:
            if balance.get("assetName") != "EVR":
                if balance.get("balance") > 576:
                    from_address = get_outbox_address(balance.get("assetName"))
                    outbox_balance = balance.get("balance")
                    outbox = balance.get("assetName")

    if not from_address:
        print("Could not find a suitable outbox asset from which to send the message.")
        sys.exit(1)

    # Create an encrypted message payload
    message_payload = create_message_payload(
        from_address,
        to,
        subject,
        content
    )

    # Now we just add it to IPFS
    from evrmail.commands.ipfs import add_to_ipfs
    cid = add_to_ipfs(message_payload)
    if not cid:
        typer.echo("❌ Failed to upload message to IPFS")
        raise typer.Exit(code=1)
    
    tx, txid = create_send_asset_transaction(
        from_addresses=[from_address],
        to_address=from_address,
        asset_name=outbox,
        asset_amount=outbox_balance,
        fee_rate=fee_rate,
        ipfs_cidv0=cid
    )
    

    result = rpc_client.testmempoolaccept([tx])
    status = result[0] if result else {}

    if dry_run:
        if raw:
            typer.echo(json.dumps({
                "txid": txid,
                "raw_tx": tx,
                "ipfs": cid,
                "mempool_accept": status
            }, indent=2))
        else:
            if status.get("txid") == txid and status.get("allowed"):
                typer.echo("✅ Transaction accepted by node using `testmempoolaccept` ✅")
            else:
                typer.echo(f"❌ Rejected by node: {status.get('reject-reason', 'unknown reason')}")
                return None

        typer.echo("\n🔍 Dry run Info:")
        typer.echo("─────────────────────────────────────")
        typer.echo(f"🆔 TXID       : {txid}")
        typer.echo(f"📦 IPFS CID  : {cid}")
        typer.echo(f"🧾 Raw Hex    : {tx}")
        typer.echo("─────────────────────────────────────")
    else:
        # 📡 Real broadcast
        typer.echo("📡 Broadcasting asset message transaction...")
        tx_hash = rpc_client.sendrawtransaction(tx)
        typer.echo(f"✅ Message sent! TXID: {tx_hash}")
        return tx_hash


def send_msg_core(
    to: str,
    outbox: str,
    subject: str,
    content: str,
    fee_rate: float,
    dry_run: bool,
    debug: bool,
    raw: bool,
    encrypted: bool = False
):
    from evrmail.utils.create_message_payload import create_message_payload
    from evrmail import rpc_client
    from evrmail.wallet import addresses 
    import sys   
  
  
    # Check the fee rate, min is 0.01 EVR/kB
    if fee_rate:
        fee_rate = math.ceil(int(fee_rate * 1e8))  # EVR → satoshis

    from evrmail.wallet.addresses import validate
    valid = validate(to)
    to_address = None
    
    if valid.get('isvalid'):
        if encrypted:
            # user provided an evrmore address
            from evrmail.config import load_config
            config = load_config()
            contacts = config.get("contacts")
            for contact in contacts:
                if contact == to:
                    to_address = to
                    to_pubkey = contacts.get(contact).get("pubkey")
            if not to_address:
                print(f"{to} is not in your contacts")
                sys.exit(1)
        else:
            to_address = to
    else:
        if encrypted:
            # user did not provide evrmore address, lets assume its a friendly name
            from evrmail.config import load_config
            config = load_config()
            contacts = config.get("contacts")
            for contact in contacts:
                if contacts.get(contact).get("friendly_name") == to:
                    to_address = contact
                    to_pubkey = contacts.get(contact).get("pubkey")
            if not to_address:
                print(f"{to} is not in your contacts")
                sys.exit(1)
        else:
            print("Invalid evrmore address.")
    # Now we have know we have a valid to address and to pubkey for encryption
    # Time to find a suitable from address, one with an asset
    from_address = None
    outbox_balance = None
    if outbox:
        from_address = get_outbox_address(outbox)
        if not from_address:
            print(f"You do not own {outbox}")
            sys.exit(1)
        
        balances = rpc_client.getaddressbalance({"addresses": [from_address]}, True)
        for balance in balances:
            if balance.get("assetName") == outbox:
                if balance.get("balance") > 576:
                    outbox_balance = balance.get("balance")
                else:
                    print(f"You do not own a suitible amount of {outbox_balance} to send a message.")
                    sys.exit(1)
    else:
        wallet_addresses = get_all_addresses()
        balances = rpc_client.getaddressbalance({"addresses": wallet_addresses}, True)
        for balance in balances:
            if balance.get("assetName") != "EVR":
                if balance.get("balance") > 576:
                    from_address = get_outbox_address(balance.get("assetName"))
                    outbox_balance = balance.get("balance")
                    outbox = balance.get("assetName")

    if not from_address:
        print("Could not find a suitable outbox asset from which to send the message.")
        sys.exit(1)

    # Create an encrypted message payload
    message_payload = create_message_payload(
        from_address,
        to,
        subject,
        content
    )
    from evrmail.utils.create_batch_payload import create_batch_payload
    batch_payload = create_batch_payload(from_address, message_payload)

    # Now we just add it to IPFS
    from evrmail.commands.ipfs import add_to_ipfs
    cid = add_to_ipfs(batch_payload)
    if not cid:
        typer.echo("❌ Failed to upload message to IPFS")
        raise typer.Exit(code=1)
    print("-"*25)
    print(to_address)
    print(from_address)
    print(outbox)
    print("-"*25)

    tx, txid = create_send_asset_transaction(
        from_addresses=[from_address],
        to_address=from_address,
        asset_name=outbox,
        asset_amount=outbox_balance,
        fee_rate=fee_rate,
        ipfs_cidv0=cid
    )

    print(tx,txid)

    result = rpc_client.testmempoolaccept([tx])
    status = result[0] if result else {}

    if dry_run:
        if raw:
            typer.echo(json.dumps({
                "txid": txid,
                "raw_tx": tx,
                "ipfs": cid,
                "mempool_accept": status
            }, indent=2))
        else:
            if status.get("txid") == txid and status.get("allowed"):
                typer.echo("✅ Transaction accepted by node using `testmempoolaccept` ✅")
            else:
                typer.echo(f"❌ Rejected by node: {status.get('reject-reason', 'unknown reason')}")
                return None

        typer.echo("\n🔍 Dry run Info:")
        typer.echo("─────────────────────────────────────")
        typer.echo(f"🆔 TXID       : {txid}")
        typer.echo(f"📦 IPFS CID  : {cid}")
        typer.echo(f"🧾 Raw Hex    : {tx}")
        typer.echo("─────────────────────────────────────")
    else:
        # 📡 Real broadcast
        typer.echo("📡 Broadcasting asset message transaction...")
        tx_hash = rpc_client.sendrawtransaction(tx)
        typer.echo(f"✅ Message sent! TXID: {tx_hash}")
        return tx_hash
