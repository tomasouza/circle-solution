#!/usr/bin/env python3
"""
Demo: Integração PicPay com Circle APIs
Exemplo simplificado para demonstração na apresentação

Este código mostra como seria a integração básica entre o PicPay e as APIs da Circle
para funcionalidades de mint/redeem de USDC e transferências.

ATENÇÃO: Este é um exemplo educativo. Código de produção requer tratamento de erros,
segurança, logging, e outras práticas de desenvolvimento robustas.
"""

import requests
import json
import uuid
from datetime import datetime
from typing import Dict, Any, Optional
from decimal import Decimal

class CircleAPIDemo:
    """
    Classe de demonstração para integração com APIs da Circle
    """
    
    def __init__(self, api_key: str, environment: str = "sandbox"):
        """
        Inicializa cliente Circle
        
        Args:
            api_key: Chave de API da Circle
            environment: "sandbox" ou "production"
        """
        self.api_key = api_key
        self.base_url = {
            "sandbox": "https://api-sandbox.circle.com",
            "production": "https://api.circle.com"
        }[environment]
        
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        print(f"🔧 Circle API Client inicializado - Ambiente: {environment}")
        print(f"🌐 Base URL: {self.base_url}")
    
    def generate_idempotency_key(self) -> str:
        """
        Gera chave de idempotência única para evitar transações duplicadas
        """
        return str(uuid.uuid4())
    
    def get_account_info(self) -> Dict[str, Any]:
        """
        Obtém informações da conta Circle
        """
        print("\n📊 Consultando informações da conta...")
        
        try:
            response = requests.get(
                f"{self.base_url}/v1/businessAccount/balances",
                headers=self.headers
            )
            
            if response.status_code == 200:
                data = response.json()
                print("✅ Conta consultada com sucesso!")
                
                # Exibir saldos disponíveis
                if 'data' in data:
                    for balance in data['data']:
                        currency = balance.get('currency', 'N/A')
                        amount = balance.get('amount', '0')
                        print(f"   💰 {currency}: ${amount}")
                
                return data
            else:
                print(f"❌ Erro ao consultar conta: {response.status_code}")
                return {"error": response.text}
                
        except Exception as e:
            print(f"❌ Exceção ao consultar conta: {str(e)}")
            return {"error": str(e)}
    
    def mint_usdc(self, usd_amount: float, source_wallet_id: str) -> Dict[str, Any]:
        """
        Demonstra mint de USDC a partir de USD
        
        Args:
            usd_amount: Valor em USD para converter em USDC
            source_wallet_id: ID da carteira de origem (USD)
        """
        print(f"\n🪙 Iniciando mint de USDC...")
        print(f"   💵 Valor: ${usd_amount}")
        print(f"   🏦 Carteira origem: {source_wallet_id}")
        
        payload = {
            "idempotencyKey": self.generate_idempotency_key(),
            "source": {
                "type": "wallet",
                "id": source_wallet_id
            },
            "destination": {
                "type": "blockchain",
                "chain": "ETH",  # Ethereum mainnet
                "address": "0x..." # Endereço de destino (seria da carteira PicPay)
            },
            "amount": {
                "amount": str(usd_amount),
                "currency": "USD"
            }
        }
        
        try:
            print("🔄 Enviando requisição para Circle...")
            
            # Em demonstração, simularemos a resposta
            if True:  # Simulação - em produção seria: response = requests.post(...)
                # Resposta simulada da Circle
                mock_response = {
                    "data": {
                        "id": f"mint_{uuid.uuid4().hex[:8]}",
                        "source": payload["source"],
                        "destination": payload["destination"],
                        "amount": payload["amount"],
                        "status": "pending",
                        "createDate": datetime.utcnow().isoformat() + "Z"
                    }
                }
                
                print("✅ Mint iniciado com sucesso!")
                print(f"   🆔 Transaction ID: {mock_response['data']['id']}")
                print(f"   📅 Data: {mock_response['data']['createDate']}")
                print(f"   ⏳ Status: {mock_response['data']['status']}")
                
                return mock_response
            
        except Exception as e:
            print(f"❌ Erro no mint: {str(e)}")
            return {"error": str(e)}
    
    def redeem_usdc(self, usdc_amount: float, destination_wallet_id: str) -> Dict[str, Any]:
        """
        Demonstra redeem de USDC para USD
        
        Args:
            usdc_amount: Valor em USDC para converter em USD
            destination_wallet_id: ID da carteira de destino (USD)
        """
        print(f"\n💸 Iniciando redeem de USDC...")
        print(f"   🪙 Valor: {usdc_amount} USDC")
        print(f"   🏦 Carteira destino: {destination_wallet_id}")
        
        payload = {
            "idempotencyKey": self.generate_idempotency_key(),
            "source": {
                "type": "blockchain",
                "chain": "ETH",
                "address": "0x..." # Endereço da carteira PicPay com USDC
            },
            "destination": {
                "type": "wallet",
                "id": destination_wallet_id
            },
            "amount": {
                "amount": str(usdc_amount),
                "currency": "USD"
            }
        }
        
        try:
            print("🔄 Enviando requisição para Circle...")
            
            # Simulação da resposta
            mock_response = {
                "data": {
                    "id": f"redeem_{uuid.uuid4().hex[:8]}",
                    "source": payload["source"],
                    "destination": payload["destination"],
                    "amount": payload["amount"],
                    "status": "pending",
                    "createDate": datetime.utcnow().isoformat() + "Z"
                }
            }
            
            print("✅ Redeem iniciado com sucesso!")
            print(f"   🆔 Transaction ID: {mock_response['data']['id']}")
            print(f"   📅 Data: {mock_response['data']['createDate']}")
            print(f"   ⏳ Status: {mock_response['data']['status']}")
            print("   ℹ️  Processamento: 1-3 dias úteis para wire transfer")
            
            return mock_response
            
        except Exception as e:
            print(f"❌ Erro no redeem: {str(e)}")
            return {"error": str(e)}
    
    def transfer_usdc(self, from_address: str, to_address: str, amount: float) -> Dict[str, Any]:
        """
        Demonstra transferência USDC entre endereços
        
        Args:
            from_address: Endereço de origem
            to_address: Endereço de destino
            amount: Valor em USDC
        """
        print(f"\n🔄 Iniciando transferência USDC...")
        print(f"   📤 De: {from_address[:10]}...{from_address[-8:]}")
        print(f"   📥 Para: {to_address[:10]}...{to_address[-8:]}")
        print(f"   💰 Valor: {amount} USDC")
        
        # Em uma implementação real, isso seria feito através de smart contracts
        # ou APIs específicas da Circle para transferências
        
        mock_response = {
            "data": {
                "id": f"transfer_{uuid.uuid4().hex[:8]}",
                "from": from_address,
                "to": to_address,
                "amount": amount,
                "currency": "USDC",
                "status": "completed",  # Transferências USDC são instantâneas
                "transactionHash": f"0x{uuid.uuid4().hex}",
                "createDate": datetime.utcnow().isoformat() + "Z"
            }
        }
        
        print("✅ Transferência concluída!")
        print(f"   🆔 Transaction ID: {mock_response['data']['id']}")
        print(f"   🔗 Hash: {mock_response['data']['transactionHash'][:20]}...")
        print(f"   ⚡ Status: {mock_response['data']['status']} (instantâneo)")
        
        return mock_response

class PicPayUSDCService:
    """
    Serviço simulado do PicPay para operações USDC
    """
    
    def __init__(self, circle_client: CircleAPIDemo):
        self.circle = circle_client
        self.exchange_rate_brl_usd = 5.0  # Taxa simulada: 1 USD = 5 BRL
        
        # Simulação de dados de usuários
        self.users = {
            123: {"name": "Maria Silva", "brl_balance": 1000.0, "usdc_balance": 50.0},
            456: {"name": "João Santos", "brl_balance": 2000.0, "usdc_balance": 100.0}
        }
        
        print(f"🏦 PicPay USDC Service inicializado")
        print(f"💱 Taxa BRL/USD: {self.exchange_rate_brl_usd}")
    
    def convert_brl_to_usdc(self, user_id: int, brl_amount: float) -> Dict[str, Any]:
        """
        Converte BRL para USDC para um usuário
        """
        print(f"\n🔄 Conversão BRL → USDC")
        print(f"   👤 Usuário: {user_id} ({self.users[user_id]['name']})")
        print(f"   💰 Valor: R$ {brl_amount}")
        
        # Verificar saldo BRL
        user = self.users[user_id]
        if user["brl_balance"] < brl_amount:
            print("❌ Saldo BRL insuficiente!")
            return {"success": False, "error": "Saldo insuficiente"}
        
        # Converter BRL para USD
        usd_amount = brl_amount / self.exchange_rate_brl_usd
        print(f"   💵 Equivalente em USD: ${usd_amount:.2f}")
        
        # Debitar BRL
        user["brl_balance"] -= brl_amount
        print(f"   ➖ BRL debitado. Novo saldo: R$ {user['brl_balance']}")
        
        # Simular mint USDC via Circle
        mint_result = self.circle.mint_usdc(usd_amount, "picpay_usd_wallet")
        
        if "error" not in mint_result:
            # Creditar USDC
            user["usdc_balance"] += usd_amount
            print(f"   ➕ USDC creditado. Novo saldo: {user['usdc_balance']} USDC")
            
            return {
                "success": True,
                "brl_debited": brl_amount,
                "usdc_credited": usd_amount,
                "transaction_id": mint_result["data"]["id"]
            }
        else:
            # Reverter débito BRL em caso de erro
            user["brl_balance"] += brl_amount
            print("❌ Erro no mint. Débito BRL revertido.")
            return {"success": False, "error": "Erro no mint USDC"}
    
    def send_international_transfer(self, from_user_id: int, to_email: str, usdc_amount: float) -> Dict[str, Any]:
        """
        Envia transferência internacional em USDC
        """
        print(f"\n🌍 Transferência Internacional")
        print(f"   👤 De: {from_user_id} ({self.users[from_user_id]['name']})")
        print(f"   📧 Para: {to_email}")
        print(f"   💰 Valor: {usdc_amount} USDC")
        
        user = self.users[from_user_id]
        
        # Verificar saldo USDC
        if user["usdc_balance"] < usdc_amount:
            print("❌ Saldo USDC insuficiente!")
            return {"success": False, "error": "Saldo USDC insuficiente"}
        
        # Debitar USDC
        user["usdc_balance"] -= usdc_amount
        print(f"   ➖ USDC debitado. Novo saldo: {user['usdc_balance']} USDC")
        
        # Simular transferência
        transfer_result = self.circle.transfer_usdc(
            "0xPicPayWallet123...",
            "0xDestinationWallet456...",
            usdc_amount
        )
        
        if "error" not in transfer_result:
            print("✅ Transferência internacional concluída!")
            
            # Em produção, aqui enviaria notificação por email para o destinatário
            print(f"   📧 Notificação enviada para {to_email}")
            print(f"   ⏱️  Tempo total: ~2 minutos (vs 2 dias no processo atual)")
            
            return {
                "success": True,
                "amount_sent": usdc_amount,
                "recipient": to_email,
                "transaction_hash": transfer_result["data"]["transactionHash"]
            }
        else:
            # Reverter débito em caso de erro
            user["usdc_balance"] += usdc_amount
            print("❌ Erro na transferência. Débito revertido.")
            return {"success": False, "error": "Erro na transferência"}
    
    def show_user_balances(self):
        """
        Exibe saldos dos usuários para demonstração
        """
        print("\n👥 Saldos dos Usuários:")
        for user_id, data in self.users.items():
            print(f"   {user_id} - {data['name']}:")
            print(f"      💰 BRL: R$ {data['brl_balance']}")
            print(f"      🪙 USDC: {data['usdc_balance']} USDC")

def main():
    """
    Demonstração principal - simula casos de uso do PicPay com Circle
    """
    print("=" * 60)
    print("🚀 DEMO: PicPay Digital Assets powered by Circle")
    print("=" * 60)
    
    # Inicializar clientes
    circle_client = CircleAPIDemo(
        api_key="demo_api_key_sandbox",
        environment="sandbox"
    )
    
    picpay_service = PicPayUSDCService(circle_client)
    
    # Mostrar informações da conta Circle
    circle_client.get_account_info()
    
    # Mostrar saldos iniciais dos usuários
    picpay_service.show_user_balances()
    
    print("\n" + "=" * 60)
    print("📋 CENÁRIO 1: Maria converte R$ 500 para USDC")
    print("=" * 60)
    
    result1 = picpay_service.convert_brl_to_usdc(123, 500.0)
    if result1["success"]:
        print(f"✅ Conversão realizada com sucesso!")
        print(f"   Transaction ID: {result1['transaction_id']}")
    
    print("\n" + "=" * 60)
    print("📋 CENÁRIO 2: Maria envia USDC para filha nos EUA")
    print("=" * 60)
    
    result2 = picpay_service.send_international_transfer(
        123, 
        "filha@universidade.edu", 
        50.0
    )
    if result2["success"]:
        print(f"✅ Transferência internacional realizada!")
        print(f"   Hash: {result2['transaction_hash'][:20]}...")
    
    # Mostrar saldos finais
    print("\n" + "=" * 60)
    print("📊 SALDOS FINAIS")
    print("=" * 60)
    picpay_service.show_user_balances()
    
    print("\n" + "=" * 60)
    print("💡 BENEFÍCIOS DEMONSTRADOS:")
    print("   ⚡ Conversão BRL → USDC: ~30 segundos")
    print("   🌍 Transferência internacional: ~2 minutos")
    print("   💰 Economia vs processo atual: ~50% em taxas")
    print("   📱 Tudo integrado no app PicPay")
    print("=" * 60)

if __name__ == "__main__":
    main()

