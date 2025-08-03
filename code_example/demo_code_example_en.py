#!/usr/bin/env python3
"""
PicPay Digital Assets - Circle API Integration Demo
---------------------------------------------------

This demo script showcases the integration between PicPay and Circle APIs
for implementing USDC functionality within the PicPay ecosystem.

The script demonstrates:
1. User wallet creation
2. BRL to USDC conversion (minting)
3. USDC to BRL conversion (redemption)
4. International transfers using USDC
5. Transaction history and reporting

Author: Circle Solutions Engineering
Date: July 28, 2025
"""

import os
import uuid
import json
import time
import requests
from datetime import datetime
from typing import Dict, List, Optional, Union

# Configuration
# In production, these would be stored securely and not in code
API_KEY = os.environ.get("CIRCLE_API_KEY", "SANDBOX_API_KEY")
BASE_URL = os.environ.get("CIRCLE_API_URL", "https://api-sandbox.circle.com")
PICPAY_WALLET_ID = "picpay-master-wallet"

# Exchange rate service (simplified for demo)
EXCHANGE_RATES = {
    "BRL_USD": 0.20,  # 1 BRL = 0.20 USD
    "USD_BRL": 5.0,    # 1 USD = 5.0 BRL
}

class CircleClient:
    """Client for interacting with Circle APIs"""
    
    def __init__(self, api_key: str, base_url: str):
        self.api_key = api_key
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        })
    
    def _generate_idempotency_key(self) -> str:
        """Generate a unique idempotency key for API requests"""
        return str(uuid.uuid4())
    
    def get_wallet_balance(self, wallet_id: str) -> Dict:
        """Get the balance of a specific wallet"""
        url = f"{self.base_url}/v1/businessAccount/wallets/{wallet_id}/balances"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()
    
    def mint_usdc(self, amount_usd: float, destination_address: str) -> Dict:
        """Mint USDC from USD and send to destination address"""
        url = f"{self.base_url}/v1/businessAccount/transfers"
        payload = {
            "idempotencyKey": self._generate_idempotency_key(),
            "source": {
                "type": "wallet",
                "id": PICPAY_WALLET_ID
            },
            "destination": {
                "type": "blockchain",
                "address": destination_address,
                "chain": "ETH"
            },
            "amount": {
                "amount": str(amount_usd),
                "currency": "USD"
            }
        }
        response = self.session.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    
    def redeem_usdc(self, amount_usdc: float, blockchain_address: str) -> Dict:
        """Redeem USDC to USD by transferring from blockchain to wallet"""
        url = f"{self.base_url}/v1/businessAccount/transfers"
        payload = {
            "idempotencyKey": self._generate_idempotency_key(),
            "source": {
                "type": "blockchain",
                "address": blockchain_address,
                "chain": "ETH"
            },
            "destination": {
                "type": "wallet",
                "id": PICPAY_WALLET_ID
            },
            "amount": {
                "amount": str(amount_usdc),
                "currency": "USD"
            }
        }
        response = self.session.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    
    def create_transfer(self, 
                       source_wallet_id: str, 
                       destination_wallet_id: str, 
                       amount: float, 
                       currency: str) -> Dict:
        """Create a transfer between wallets"""
        url = f"{self.base_url}/v1/transfers"
        payload = {
            "idempotencyKey": self._generate_idempotency_key(),
            "source": {
                "type": "wallet",
                "id": source_wallet_id
            },
            "destination": {
                "type": "wallet",
                "id": destination_wallet_id
            },
            "amount": {
                "amount": str(amount),
                "currency": currency
            }
        }
        response = self.session.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    
    def get_transfer_status(self, transfer_id: str) -> Dict:
        """Get the status of a transfer"""
        url = f"{self.base_url}/v1/transfers/{transfer_id}"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()
    
    def get_transaction_history(self, wallet_id: str, 
                               from_date: Optional[str] = None, 
                               to_date: Optional[str] = None, 
                               page_size: int = 50) -> Dict:
        """Get transaction history for a wallet"""
        url = f"{self.base_url}/v1/wallets/{wallet_id}/transactions"
        params = {"pageSize": page_size}
        if from_date:
            params["from"] = from_date
        if to_date:
            params["to"] = to_date
            
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()


class PicPayUSDCService:
    """Service for handling USDC operations within PicPay"""
    
    def __init__(self, circle_client: CircleClient):
        self.circle_client = circle_client
        self.user_wallets = {}  # In production, this would be in a database
    
    def create_user_wallet(self, user_id: str) -> Dict:
        """Create a new USDC wallet for a user"""
        # In production, this would involve creating a blockchain address
        # and storing it securely in a database
        wallet_address = f"0x{uuid.uuid4().hex}"
        self.user_wallets[user_id] = {
            "wallet_address": wallet_address,
            "created_at": datetime.now().isoformat(),
            "balance_usdc": 0.0
        }
        return self.user_wallets[user_id]
    
    def convert_brl_to_usdc(self, user_id: str, amount_brl: float) -> Dict:
        """Convert BRL to USDC for a user"""
        # Check if user has a wallet
        if user_id not in self.user_wallets:
            self.create_user_wallet(user_id)
        
        # Convert BRL to USD
        amount_usd = amount_brl * EXCHANGE_RATES["BRL_USD"]
        
        # Mint USDC and send to user's wallet
        wallet_address = self.user_wallets[user_id]["wallet_address"]
        mint_result = self.circle_client.mint_usdc(amount_usd, wallet_address)
        
        # Update user's balance (in production, this would be based on blockchain confirmation)
        self.user_wallets[user_id]["balance_usdc"] += amount_usd
        
        return {
            "user_id": user_id,
            "amount_brl": amount_brl,
            "amount_usdc": amount_usd,
            "transaction_id": mint_result.get("id"),
            "status": mint_result.get("status", "pending"),
            "timestamp": datetime.now().isoformat()
        }
    
    def convert_usdc_to_brl(self, user_id: str, amount_usdc: float) -> Dict:
        """Convert USDC to BRL for a user"""
        # Check if user has a wallet and sufficient balance
        if user_id not in self.user_wallets:
            raise ValueError(f"User {user_id} does not have a wallet")
        
        if self.user_wallets[user_id]["balance_usdc"] < amount_usdc:
            raise ValueError(f"Insufficient USDC balance")
        
        # Redeem USDC to USD
        wallet_address = self.user_wallets[user_id]["wallet_address"]
        redeem_result = self.circle_client.redeem_usdc(amount_usdc, wallet_address)
        
        # Convert USD to BRL
        amount_brl = amount_usdc * EXCHANGE_RATES["USD_BRL"]
        
        # Update user's balance
        self.user_wallets[user_id]["balance_usdc"] -= amount_usdc
        
        return {
            "user_id": user_id,
            "amount_usdc": amount_usdc,
            "amount_brl": amount_brl,
            "transaction_id": redeem_result.get("id"),
            "status": redeem_result.get("status", "pending"),
            "timestamp": datetime.now().isoformat()
        }
    
    def send_international_payment(self, 
                                  sender_id: str, 
                                  recipient_id: str, 
                                  amount_usdc: float) -> Dict:
        """Send an international payment using USDC"""
        # Check if sender has a wallet and sufficient balance
        if sender_id not in self.user_wallets:
            raise ValueError(f"Sender {sender_id} does not have a wallet")
        
        if self.user_wallets[sender_id]["balance_usdc"] < amount_usdc:
            raise ValueError(f"Insufficient USDC balance")
        
        # Create transfer between wallets
        # In production, this would involve blockchain transactions
        sender_wallet = self.user_wallets[sender_id]["wallet_address"]
        
        # Ensure recipient has a wallet
        if recipient_id not in self.user_wallets:
            self.create_user_wallet(recipient_id)
        
        recipient_wallet = self.user_wallets[recipient_id]["wallet_address"]
        
        # Simulate transfer (in production, this would be a blockchain transaction)
        transfer_id = str(uuid.uuid4())
        
        # Update balances
        self.user_wallets[sender_id]["balance_usdc"] -= amount_usdc
        self.user_wallets[recipient_id]["balance_usdc"] += amount_usdc
        
        return {
            "sender_id": sender_id,
            "recipient_id": recipient_id,
            "amount_usdc": amount_usdc,
            "transaction_id": transfer_id,
            "status": "completed",
            "timestamp": datetime.now().isoformat()
        }
    
    def get_user_balance(self, user_id: str) -> Dict:
        """Get a user's USDC balance"""
        if user_id not in self.user_wallets:
            raise ValueError(f"User {user_id} does not have a wallet")
        
        balance_usdc = self.user_wallets[user_id]["balance_usdc"]
        balance_brl_equivalent = balance_usdc * EXCHANGE_RATES["USD_BRL"]
        
        return {
            "user_id": user_id,
            "balance_usdc": balance_usdc,
            "balance_brl_equivalent": balance_brl_equivalent,
            "wallet_address": self.user_wallets[user_id]["wallet_address"],
            "timestamp": datetime.now().isoformat()
        }


def run_demo():
    """Run a demonstration of the PicPay USDC integration"""
    print("PicPay Digital Assets - Circle API Integration Demo")
    print("==================================================\n")
    
    # Initialize clients
    circle_client = CircleClient(API_KEY, BASE_URL)
    picpay_service = PicPayUSDCService(circle_client)
    
    # Create users
    print("Creating user wallets...")
    alice = "alice_123"
    bob = "bob_456"
    alice_wallet = picpay_service.create_user_wallet(alice)
    bob_wallet = picpay_service.create_user_wallet(bob)
    print(f"Alice's wallet: {alice_wallet['wallet_address']}")
    print(f"Bob's wallet: {bob_wallet['wallet_address']}\n")
    
    # Convert BRL to USDC
    print("Converting BRL to USDC...")
    brl_amount = 500.0
    conversion_result = picpay_service.convert_brl_to_usdc(alice, brl_amount)
    print(f"Converted {brl_amount} BRL to {conversion_result['amount_usdc']} USDC")
    print(f"Transaction ID: {conversion_result['transaction_id']}\n")
    
    # Check balance
    alice_balance = picpay_service.get_user_balance(alice)
    print(f"Alice's balance: {alice_balance['balance_usdc']} USDC")
    print(f"BRL equivalent: {alice_balance['balance_brl_equivalent']} BRL\n")
    
    # Send international payment
    print("Sending international payment...")
    payment_amount = 50.0
    payment_result = picpay_service.send_international_payment(alice, bob, payment_amount)
    print(f"Sent {payment_amount} USDC from Alice to Bob")
    print(f"Transaction ID: {payment_result['transaction_id']}\n")
    
    # Check balances after transfer
    alice_balance = picpay_service.get_user_balance(alice)
    bob_balance = picpay_service.get_user_balance(bob)
    print(f"Alice's new balance: {alice_balance['balance_usdc']} USDC")
    print(f"Bob's new balance: {bob_balance['balance_usdc']} USDC\n")
    
    # Convert USDC back to BRL
    print("Converting USDC back to BRL...")
    usdc_amount = 20.0
    redemption_result = picpay_service.convert_usdc_to_brl(bob, usdc_amount)
    print(f"Converted {usdc_amount} USDC to {redemption_result['amount_brl']} BRL")
    print(f"Transaction ID: {redemption_result['transaction_id']}\n")
    
    # Final balances
    alice_balance = picpay_service.get_user_balance(alice)
    bob_balance = picpay_service.get_user_balance(bob)
    print("Final balances:")
    print(f"Alice: {alice_balance['balance_usdc']} USDC ({alice_balance['balance_brl_equivalent']} BRL)")
    print(f"Bob: {bob_balance['balance_usdc']} USDC ({bob_balance['balance_brl_equivalent']} BRL)\n")
    
    print("Demo completed successfully!")


if __name__ == "__main__":
    run_demo()

