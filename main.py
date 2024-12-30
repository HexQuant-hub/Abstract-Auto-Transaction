import json
import os
import time
import random
from typing import List
from web3 import Web3
from eth_account import Account
import eth_account
from rich.console import Console
from rich.table import Table
from rich.progress import track

console = Console()

CONFIG_FILE = 'config.json'
ENV_FILE = '.env'

HEADER = """
[bold cyan]
██╗  ██╗███████╗██╗  ██╗ ██████╗ ██╗   ██╗ █████╗ ███╗   ██╗████████╗
██║  ██║██╔════╝╚██╗██╔╝██╔═══██╗██║   ██║██╔══██╗████╗  ██║╚══██╔══╝
███████║█████╗   ╚███╔╝ ██║   ██║██║   ██║███████║██╔██╗ ██║   ██║   
██╔══██║██╔══╝   ██╔██╗ ██║▄▄ ██║██║   ██║██╔══██║██║╚██╗██║   ██║   
██║  ██║███████╗██╔╝ ██╗╚██████╔╝╚██████╔╝██║  ██║██║ ╚████║   ██║   
╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝ ╚══▀▀═╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝   ╚═╝   

Abstract Testnet Auto Transaction
[/bold cyan]
"""

# Network Configuration
NETWORK_CONFIG = {
    'rpc_url': 'https://api.testnet.abs.xyz',
    'chain_id': 11124,
    'block_explorer': 'https://explorer.testnet.abs.xyz'
}

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_header():
    """Display the program header."""
    clear_screen()
    console.print(HEADER)
    console.print("\n" + "=" * 70 + "\n", style="bold green")

def load_private_keys() -> List[str]:
    """Load private keys from .env file."""
    if not os.path.exists(ENV_FILE):
        raise FileNotFoundError(f"{ENV_FILE} file not found. Please create it with your private keys.")

    with open(ENV_FILE, 'r') as f:
        keys = [line.strip() for line in f.readlines() if line.strip()]
        return [key if key.startswith('0x') else f'0x{key}' for key in keys]

def get_random_amount() -> float:
    """Generate random amount between 0.00001 and 0.000099 ETH."""
    return random.randint(10, 99) / 1000000

def get_random_delay() -> int:
    """Generate random delay between 3 and 17 seconds."""
    return random.randint(3, 17)

class TransactionManager:
    def __init__(self, w3: Web3, chain_id: int, block_explorer: str):
        self.w3 = w3
        self.chain_id = chain_id
        self.block_explorer = block_explorer

    def check_balance(self, address: str) -> float:
        """Check address balance and return it in ETH."""
        balance = self.w3.eth.get_balance(address)
        return float(self.w3.from_wei(balance, 'ether'))

    def get_gas_price(self) -> int:
        """Get current gas price with safety buffer."""
        try:
            latest_block = self.w3.eth.get_block('latest')
            base_fee = latest_block.get('baseFeePerGas', self.w3.eth.gas_price)
            return int(base_fee * 1.2)
        except Exception as e:
            console.print(f"[bold red]Error getting gas price:[/bold red] {e}")
            return self.w3.to_wei(1, 'gwei')

    def estimate_gas_limit(self, from_address: str, to_address: str, amount: float) -> int:
        """Estimate gas limit for the transaction."""
        try:
            gas_estimate = self.w3.eth.estimate_gas({
                'from': from_address,
                'to': to_address,
                'value': self.w3.to_wei(amount, 'ether')
            })
            return int(gas_estimate * 1.2)
        except Exception as e:
            console.print(f"[bold red]Gas estimation failed:[/bold red] {e}")
            return 21000

    def send_transaction(self, private_key: str, to_address: str, amount: float, nonce: int) -> str:
        """Send a single transaction and return the transaction hash."""
        try:
            account = self.w3.eth.account.from_key(private_key)
            gas_price = self.get_gas_price()
            gas_limit = self.estimate_gas_limit(account.address, to_address, amount)

            tx_params = {
                'chainId': self.chain_id,
                'nonce': nonce,
                'from': account.address,
                'to': to_address,
                'value': self.w3.to_wei(amount, 'ether'),
                'maxFeePerGas': gas_price,
                'maxPriorityFeePerGas': int(gas_price * 0.1),
                'gas': gas_limit,
                'type': '0x2'
            }

            signed_tx = self.w3.eth.account.sign_transaction(tx_params, private_key)
            tx_hash = self.w3.eth.send_raw_transaction(signed_tx.raw_transaction)

            tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)

            if tx_receipt.status != 1:
                raise Exception("Transaction failed")

            return tx_hash.hex()

        except Exception as e:
            raise Exception(f"Transaction failed: {str(e)}")

def process_transactions(w3: Web3, tx_manager: TransactionManager, private_key: str, num_wallets: int):
    """Process transactions for a single private key."""
    try:
        account = eth_account.Account.from_key(private_key)
        console.print(f"\n[bold cyan]Processing transactions for address:[/bold cyan] {account.address}")

        balance = tx_manager.check_balance(account.address)
        console.print(f"[bold yellow]Current balance:[/bold yellow] {balance:.8f} ETH")

        new_wallets = [Account.create() for _ in track(range(num_wallets), description="Creating wallets...")]
        nonce = w3.eth.get_transaction_count(account.address)

        for i, wallet in enumerate(new_wallets, 1):
            try:
                amount = get_random_amount()
                console.print(f"\n[bold green]Processing transaction {i}/{num_wallets}...[/bold green]")

                tx_hash = tx_manager.send_transaction(
                    private_key,
                    wallet.address,
                    amount,
                    nonce
                )

                console.print(f"[bold green]Transaction successful:[/bold green]")
                console.print(f"  [blue]To:[/blue] {wallet.address}")
                console.print(f"  [blue]Amount:[/blue] {amount} ETH")
                console.print(f"  [blue]Hash:[/blue] {tx_hash}")
                console.print(f"  [blue]Explorer:[/blue] {NETWORK_CONFIG['block_explorer']}/tx/{tx_hash}")

                nonce += 1
                delay = get_random_delay()
                console.print(f"[bold yellow]Waiting for {delay} seconds before the next transaction...[/bold yellow]")
                time.sleep(delay)

            except Exception as e:
                console.print(f"[bold red]Transaction {i} failed:[/bold red]")
                console.print(f"  [red]To:[/red] {wallet.address}")
                console.print(f"  [red]Error:[/red] {str(e)}")

        return new_wallets

    except Exception as e:
        console.print(f"[bold red]Error processing transactions for {account.address}:[/bold red] {str(e)}")
        return []

def main():
    display_header()

    try:
        private_keys = load_private_keys()
        console.print(f"[bold cyan]Loaded {len(private_keys)} private keys from {ENV_FILE}[/bold cyan]")

        w3 = Web3(Web3.HTTPProvider(NETWORK_CONFIG['rpc_url']))
        if not w3.is_connected():
            console.print("[bold red]Failed to connect to Abstract Testnet. Please check your internet connection.[/bold red]")
            return

        tx_manager = TransactionManager(
            w3,
            NETWORK_CONFIG['chain_id'],
            NETWORK_CONFIG['block_explorer']
        )

        num_wallets = int(console.input("[bold yellow]Enter the number of wallets to create per private key: [/bold yellow]"))

        all_wallets = []
        for private_key in private_keys:
            wallets = process_transactions(w3, tx_manager, private_key, num_wallets)
            all_wallets.extend(wallets)

        console.print("\n[bold cyan]Saving wallet information...[/bold cyan]")
        with open('wallets.txt', 'w') as f:
            f.write("=== Generated Wallets ===\n\n")
            for i, wallet in enumerate(all_wallets, 1):
                f.write(f"Wallet {i}:\n")
                f.write(f"Address: {wallet.address}\n")
                f.write(f"Private Key: {wallet.key.hex()}\n")
                f.write("-" * 50 + "\n\n")

        console.print("[bold green]✓ Wallet information saved to 'wallets.txt'[/bold green]")
        console.input("\n[bold yellow]Press Enter after you have saved the wallet information elsewhere...[/bold yellow]")
        os.remove('wallets.txt')
        console.print("[bold green]✓ Wallet file has been deleted for security[/bold green]")

    except FileNotFoundError:
        console.print("\n[bold red]Error: .env file not found![/bold red]")
        console.print("[bold yellow]Please create a .env file with your private keys (one per line)[/bold yellow]")
    except Exception as e:
        console.print(f"\n[bold red]An error occurred:[/bold red] {e}")

if __name__ == "__main__":
    main()

