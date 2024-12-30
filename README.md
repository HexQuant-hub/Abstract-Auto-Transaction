# Auto Transaction Tool for Abstract Testnet

## Introduction

The **Auto Transaction Tool** is a Python-based utility that automates transactions on the Abstract Testnet. It supports the creation of new wallets, transferring small amounts of ETH, and managing gas fees dynamically. This tool is ideal for developers testing their decentralized applications (dApps) or smart contracts in a simulated environment.

Abstract Testnet: Dive into our resources to learn more about the blockchain leading the next generation of consumer crypto.

## Features

- **Automated Transactions**: Send ETH to multiple wallets in one go.
- **Wallet Creation**: Generate new wallets dynamically.
- **Dynamic Gas Management**: Automatically calculates gas price and limits.
- **Secure Key Management**: Uses `.env` files to securely handle private keys.
- **Rich Terminal Interface**: Displays operations in a user-friendly and interactive manner using `rich`.

---

## Prerequisites

1. **Python 3.8 or higher**
2. **Pip** package manager
3. **Dependencies**:
   - `web3`
   - `rich`

Install dependencies with:
```bash
pip install web3 rich
```

4. **Environment File**:
   - Create a `.env` file in the root directory.
   - Add private keys (one per line):
     ```
     0xYOUR_PRIVATE_KEY_1
     0xYOUR_PRIVATE_KEY_2
     ```

5. **Network Configuration**:
   - Default RPC URL: `https://api.testnet.abs.xyz`
   - Chain ID: `11124`
   - Ensure you have sufficient ETH in your wallets on the Abstract Testnet.

---

## Usage

### Clone the Repository

```bash
git clone https://github.com/HexQuant-hub/Abstract-Auto-Transaction.git
Abstract-Auto-Transaction
```

### Run the Tool

1. **Start the script**:
   ```bash
   python main.py
   or
   python3 main.py
   ```

2. **Follow the prompts**:
   - Enter the number of wallets to create per private key.
   - Monitor transaction progress and success messages.

3. **Output**:
   - Wallet information (addresses and private keys) is temporarily saved to `wallets.txt`.
   - This file will be deleted after you confirm its secure storage.

---

## Example

Here is an example of running the script:

```plaintext
██╗  ██╗███████╗██╗  ██╗ ██████╗ ██╗   ██╗ █████╗ ███╗   ██╗████████╗
██║  ██║██╔════╝╚██╗██╔╝██╔═══██╗██║   ██║██╔══██╗████╗  ██║╚══██╔══╝
███████║█████╗   ╚███╔╝ ██║   ██║██║   ██║███████║██╔██╗ ██║   ██║   
██╔══██║██╔══╝   ██╔██╗ ██║▄▄ ██║██║   ██║██╔══██║██║╚██╗██║   ██║   
██║  ██║███████╗██╔╝ ██╗╚██████╔╝╚██████╔╝██║  ██║██║ ╚████║   ██║   
╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝ ╚══▀▀═╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝   ╚═╝  

Loaded 2 private keys from .env
Enter the number of wallets to create per private key: 5

Processing transactions for address: 0xYOUR_ADDRESS
...
Transaction successful:
  To: 0xNEW_WALLET_ADDRESS
  Amount: 0.00005 ETH
  Hash: 0xTRANSACTION_HASH
...
```

---

## Security

- Ensure your `.env` file is stored securely and is excluded from version control (already in `.gitignore`).
- Wallet information saved temporarily in `wallets.txt` is deleted after confirmation.

---

## Contributing

Feel free to fork this repository and submit pull requests to improve the functionality or add new features.

---

## Support

If you encounter any issues or have questions, feel free to open an issue on GitHub or reach out to the maintainer at `https://t.me/HexQuantHub`.

