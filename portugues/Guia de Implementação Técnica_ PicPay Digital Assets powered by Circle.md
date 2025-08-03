# Guia de Implementação Técnica: PicPay Digital Assets powered by Circle

## Visão Geral da Integração

Este documento fornece um guia detalhado para a implementação técnica da solução PicPay Digital Assets usando as APIs da Circle. A integração permitirá que o PicPay ofereça funcionalidades nativas de USDC, incluindo mint, redeem, transferências e pagamentos globais.

## Arquitetura da Solução

### Componentes Principais

1. **PicPay Backend** - Sistema existente do PicPay
2. **Circle APIs** - Conjunto de APIs para operações com USDC
3. **Blockchain** - Rede Ethereum/Polygon para transações USDC
4. **Banco de Dados** - Armazenamento de saldos e transações
5. **Interface Mobile** - App PicPay com novas funcionalidades

### Fluxo de Dados

```
PicPay App → PicPay Backend → Circle APIs → Blockchain
                ↓
        Banco de Dados PicPay
        (saldos multi-moeda)
```

## APIs da Circle Utilizadas

### 1. Circle Mint API

**Endpoint Base:** `https://api.circle.com/v1/`

**Funcionalidades:**
- Mint de USDC (conversão USD → USDC)
- Redeem de USDC (conversão USDC → USD)
- Consulta de saldos
- Histórico de transações

### 2. Payments API

**Funcionalidades:**
- Recebimento de pagamentos em USDC
- Processamento de pagamentos P2P
- Integração com merchants

### 3. Payouts API

**Funcionalidades:**
- Envio de pagamentos globais
- Transferências internacionais
- Conversões automáticas

## Implementação por Fases

### Fase 1: MVP (3 meses)

#### 1.1 Configuração Inicial

**Pré-requisitos:**
- Conta Circle Business
- Chaves de API (sandbox e produção)
- Certificados SSL
- Ambiente de desenvolvimento

**Configuração de Ambiente:**
```bash
# Variáveis de ambiente
CIRCLE_API_KEY=your_api_key_here
CIRCLE_API_BASE=https://api-sandbox.circle.com
CIRCLE_ENVIRONMENT=sandbox
```

#### 1.2 Integração Circle Mint

**Estrutura de Dados:**
```sql
-- Tabela para saldos USDC
CREATE TABLE usdc_wallets (
    id BIGINT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    usdc_balance DECIMAL(18,6) DEFAULT 0,
    wallet_address VARCHAR(42),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Tabela para transações USDC
CREATE TABLE usdc_transactions (
    id BIGINT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    transaction_type ENUM('mint', 'redeem', 'transfer_in', 'transfer_out'),
    amount DECIMAL(18,6) NOT NULL,
    circle_transaction_id VARCHAR(255),
    status ENUM('pending', 'completed', 'failed'),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

#### 1.3 Implementação Backend

**Classe de Integração Circle:**
```python
import requests
import json
from typing import Dict, Any, Optional

class CircleIntegration:
    def __init__(self, api_key: str, base_url: str):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
    
    def mint_usdc(self, amount: float, source_wallet_id: str) -> Dict[str, Any]:
        """
        Minta USDC a partir de USD
        """
        endpoint = f"{self.base_url}/v1/businessAccount/transfers"
        payload = {
            "idempotencyKey": self._generate_idempotency_key(),
            "source": {
                "type": "wallet",
                "id": source_wallet_id
            },
            "destination": {
                "type": "blockchain",
                "chain": "ETH"
            },
            "amount": {
                "amount": str(amount),
                "currency": "USD"
            }
        }
        
        response = requests.post(endpoint, headers=self.headers, json=payload)
        return response.json()
    
    def redeem_usdc(self, amount: float, destination_wallet_id: str) -> Dict[str, Any]:
        """
        Resgata USDC para USD
        """
        endpoint = f"{self.base_url}/v1/businessAccount/transfers"
        payload = {
            "idempotencyKey": self._generate_idempotency_key(),
            "source": {
                "type": "blockchain",
                "chain": "ETH"
            },
            "destination": {
                "type": "wallet",
                "id": destination_wallet_id
            },
            "amount": {
                "amount": str(amount),
                "currency": "USD"
            }
        }
        
        response = requests.post(endpoint, headers=self.headers, json=payload)
        return response.json()
    
    def get_wallet_balance(self, wallet_id: str) -> Dict[str, Any]:
        """
        Consulta saldo da carteira
        """
        endpoint = f"{self.base_url}/v1/wallets/{wallet_id}"
        response = requests.get(endpoint, headers=self.headers)
        return response.json()
    
    def create_transfer(self, from_wallet: str, to_wallet: str, amount: float) -> Dict[str, Any]:
        """
        Cria transferência USDC entre carteiras
        """
        endpoint = f"{self.base_url}/v1/transfers"
        payload = {
            "idempotencyKey": self._generate_idempotency_key(),
            "source": {
                "type": "wallet",
                "id": from_wallet
            },
            "destination": {
                "type": "wallet",
                "id": to_wallet
            },
            "amount": {
                "amount": str(amount),
                "currency": "USD"
            }
        }
        
        response = requests.post(endpoint, headers=self.headers, json=payload)
        return response.json()
    
    def _generate_idempotency_key(self) -> str:
        """
        Gera chave de idempotência única
        """
        import uuid
        return str(uuid.uuid4())
```

#### 1.4 Serviços de Negócio

**Serviço de Carteira USDC:**
```python
from decimal import Decimal
from typing import Optional

class USDCWalletService:
    def __init__(self, circle_client: CircleIntegration, db_connection):
        self.circle = circle_client
        self.db = db_connection
    
    def convert_brl_to_usdc(self, user_id: int, brl_amount: Decimal) -> Dict[str, Any]:
        """
        Converte BRL para USDC
        """
        try:
            # 1. Validar saldo BRL do usuário
            user_brl_balance = self._get_user_brl_balance(user_id)
            if user_brl_balance < brl_amount:
                return {"success": False, "error": "Saldo insuficiente"}
            
            # 2. Converter BRL para USD (usando taxa de câmbio atual)
            usd_amount = self._convert_brl_to_usd(brl_amount)
            
            # 3. Debitar BRL da conta do usuário
            self._debit_brl_balance(user_id, brl_amount)
            
            # 4. Mint USDC via Circle
            mint_response = self.circle.mint_usdc(float(usd_amount), self._get_circle_wallet_id())
            
            if mint_response.get('data', {}).get('status') == 'pending':
                # 5. Registrar transação pendente
                transaction_id = self._create_usdc_transaction(
                    user_id=user_id,
                    transaction_type='mint',
                    amount=usd_amount,
                    circle_transaction_id=mint_response['data']['id'],
                    status='pending'
                )
                
                return {
                    "success": True,
                    "transaction_id": transaction_id,
                    "usdc_amount": usd_amount,
                    "status": "pending"
                }
            else:
                # Reverter débito BRL em caso de erro
                self._credit_brl_balance(user_id, brl_amount)
                return {"success": False, "error": "Erro no mint USDC"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def convert_usdc_to_brl(self, user_id: int, usdc_amount: Decimal) -> Dict[str, Any]:
        """
        Converte USDC para BRL
        """
        try:
            # 1. Validar saldo USDC do usuário
            user_usdc_balance = self._get_user_usdc_balance(user_id)
            if user_usdc_balance < usdc_amount:
                return {"success": False, "error": "Saldo USDC insuficiente"}
            
            # 2. Debitar USDC da conta do usuário
            self._debit_usdc_balance(user_id, usdc_amount)
            
            # 3. Redeem USDC via Circle
            redeem_response = self.circle.redeem_usdc(float(usdc_amount), self._get_circle_wallet_id())
            
            if redeem_response.get('data', {}).get('status') == 'pending':
                # 4. Converter USD para BRL
                brl_amount = self._convert_usd_to_brl(usdc_amount)
                
                # 5. Creditar BRL na conta do usuário
                self._credit_brl_balance(user_id, brl_amount)
                
                # 6. Registrar transação
                transaction_id = self._create_usdc_transaction(
                    user_id=user_id,
                    transaction_type='redeem',
                    amount=usdc_amount,
                    circle_transaction_id=redeem_response['data']['id'],
                    status='pending'
                )
                
                return {
                    "success": True,
                    "transaction_id": transaction_id,
                    "brl_amount": brl_amount,
                    "status": "pending"
                }
            else:
                # Reverter débito USDC em caso de erro
                self._credit_usdc_balance(user_id, usdc_amount)
                return {"success": False, "error": "Erro no redeem USDC"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def transfer_usdc(self, from_user_id: int, to_user_id: int, amount: Decimal) -> Dict[str, Any]:
        """
        Transfere USDC entre usuários
        """
        try:
            # 1. Validar saldo do remetente
            sender_balance = self._get_user_usdc_balance(from_user_id)
            if sender_balance < amount:
                return {"success": False, "error": "Saldo insuficiente"}
            
            # 2. Debitar do remetente
            self._debit_usdc_balance(from_user_id, amount)
            
            # 3. Creditar ao destinatário
            self._credit_usdc_balance(to_user_id, amount)
            
            # 4. Registrar transações
            self._create_usdc_transaction(from_user_id, 'transfer_out', amount)
            self._create_usdc_transaction(to_user_id, 'transfer_in', amount)
            
            return {"success": True, "transferred_amount": amount}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    # Métodos auxiliares privados
    def _get_user_brl_balance(self, user_id: int) -> Decimal:
        # Implementar consulta ao saldo BRL
        pass
    
    def _get_user_usdc_balance(self, user_id: int) -> Decimal:
        # Implementar consulta ao saldo USDC
        pass
    
    def _convert_brl_to_usd(self, brl_amount: Decimal) -> Decimal:
        # Implementar conversão usando taxa de câmbio atual
        pass
    
    def _convert_usd_to_brl(self, usd_amount: Decimal) -> Decimal:
        # Implementar conversão usando taxa de câmbio atual
        pass
    
    # Outros métodos auxiliares...
```

#### 1.5 API Endpoints

**Controller REST:**
```python
from flask import Flask, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

app = Flask(__name__)

@app.route('/api/v1/usdc/convert/brl-to-usdc', methods=['POST'])
@jwt_required()
def convert_brl_to_usdc():
    """
    Endpoint para converter BRL para USDC
    """
    user_id = get_jwt_identity()
    data = request.get_json()
    
    # Validação de entrada
    if not data or 'amount' not in data:
        return jsonify({"error": "Amount is required"}), 400
    
    try:
        amount = Decimal(str(data['amount']))
        if amount <= 0:
            return jsonify({"error": "Amount must be positive"}), 400
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid amount format"}), 400
    
    # Processar conversão
    wallet_service = USDCWalletService(circle_client, db_connection)
    result = wallet_service.convert_brl_to_usdc(user_id, amount)
    
    if result['success']:
        return jsonify({
            "success": True,
            "transaction_id": result['transaction_id'],
            "usdc_amount": str(result['usdc_amount']),
            "status": result['status']
        }), 200
    else:
        return jsonify({"error": result['error']}), 400

@app.route('/api/v1/usdc/convert/usdc-to-brl', methods=['POST'])
@jwt_required()
def convert_usdc_to_brl():
    """
    Endpoint para converter USDC para BRL
    """
    user_id = get_jwt_identity()
    data = request.get_json()
    
    # Validação similar ao endpoint anterior
    if not data or 'amount' not in data:
        return jsonify({"error": "Amount is required"}), 400
    
    try:
        amount = Decimal(str(data['amount']))
        if amount <= 0:
            return jsonify({"error": "Amount must be positive"}), 400
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid amount format"}), 400
    
    # Processar conversão
    wallet_service = USDCWalletService(circle_client, db_connection)
    result = wallet_service.convert_usdc_to_brl(user_id, amount)
    
    if result['success']:
        return jsonify({
            "success": True,
            "transaction_id": result['transaction_id'],
            "brl_amount": str(result['brl_amount']),
            "status": result['status']
        }), 200
    else:
        return jsonify({"error": result['error']}), 400

@app.route('/api/v1/usdc/transfer', methods=['POST'])
@jwt_required()
def transfer_usdc():
    """
    Endpoint para transferir USDC entre usuários
    """
    from_user_id = get_jwt_identity()
    data = request.get_json()
    
    # Validação
    required_fields = ['to_user_id', 'amount']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"{field} is required"}), 400
    
    try:
        to_user_id = int(data['to_user_id'])
        amount = Decimal(str(data['amount']))
        if amount <= 0:
            return jsonify({"error": "Amount must be positive"}), 400
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid data format"}), 400
    
    # Processar transferência
    wallet_service = USDCWalletService(circle_client, db_connection)
    result = wallet_service.transfer_usdc(from_user_id, to_user_id, amount)
    
    if result['success']:
        return jsonify({
            "success": True,
            "transferred_amount": str(result['transferred_amount'])
        }), 200
    else:
        return jsonify({"error": result['error']}), 400

@app.route('/api/v1/usdc/balance', methods=['GET'])
@jwt_required()
def get_usdc_balance():
    """
    Endpoint para consultar saldo USDC
    """
    user_id = get_jwt_identity()
    
    wallet_service = USDCWalletService(circle_client, db_connection)
    balance = wallet_service._get_user_usdc_balance(user_id)
    
    return jsonify({
        "user_id": user_id,
        "usdc_balance": str(balance)
    }), 200
```

## Segurança e Compliance

### 1. Autenticação e Autorização

**Implementação JWT:**
```python
from flask_jwt_extended import JWTManager, create_access_token, verify_jwt_in_request

# Configuração JWT
app.config['JWT_SECRET_KEY'] = 'your-secret-key'
jwt = JWTManager(app)

@app.route('/api/v1/auth/login', methods=['POST'])
def login():
    # Implementar autenticação do usuário
    # Retornar JWT token
    pass
```

### 2. Validação KYC/AML

**Integração com sistema de compliance:**
```python
class ComplianceService:
    def validate_transaction(self, user_id: int, amount: Decimal, transaction_type: str) -> bool:
        """
        Valida transação conforme regras de compliance
        """
        # 1. Verificar limites diários/mensais
        # 2. Validar status KYC do usuário
        # 3. Aplicar regras AML
        # 4. Verificar listas de sanções
        pass
    
    def report_suspicious_activity(self, user_id: int, transaction_data: Dict):
        """
        Reporta atividade suspeita
        """
        pass
```

### 3. Auditoria e Logs

**Sistema de auditoria:**
```python
import logging
from datetime import datetime

class AuditLogger:
    def __init__(self):
        self.logger = logging.getLogger('audit')
    
    def log_transaction(self, user_id: int, transaction_type: str, amount: Decimal, status: str):
        """
        Registra transação para auditoria
        """
        audit_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "user_id": user_id,
            "transaction_type": transaction_type,
            "amount": str(amount),
            "status": status
        }
        self.logger.info(f"TRANSACTION: {audit_data}")
```

## Monitoramento e Observabilidade

### 1. Métricas de Negócio

**Métricas importantes:**
- Volume total de USDC mintado
- Número de transações por dia
- Tempo médio de processamento
- Taxa de sucesso das transações
- Saldo total em USDC

### 2. Alertas

**Configuração de alertas:**
```python
class AlertService:
    def __init__(self):
        self.thresholds = {
            'high_volume_transaction': 10000,  # USD
            'failed_transaction_rate': 0.05,   # 5%
            'api_response_time': 5.0           # seconds
        }
    
    def check_transaction_volume(self, amount: Decimal):
        if amount > self.thresholds['high_volume_transaction']:
            self.send_alert(f"High volume transaction: ${amount}")
    
    def send_alert(self, message: str):
        # Implementar envio de alertas (email, Slack, etc.)
        pass
```

## Testes

### 1. Testes Unitários

**Exemplo de teste:**
```python
import unittest
from unittest.mock import Mock, patch
from decimal import Decimal

class TestUSDCWalletService(unittest.TestCase):
    def setUp(self):
        self.mock_circle = Mock()
        self.mock_db = Mock()
        self.service = USDCWalletService(self.mock_circle, self.mock_db)
    
    def test_convert_brl_to_usdc_success(self):
        # Arrange
        user_id = 123
        brl_amount = Decimal('100.00')
        
        self.service._get_user_brl_balance = Mock(return_value=Decimal('200.00'))
        self.service._convert_brl_to_usd = Mock(return_value=Decimal('20.00'))
        self.mock_circle.mint_usdc.return_value = {
            'data': {'id': 'tx123', 'status': 'pending'}
        }
        
        # Act
        result = self.service.convert_brl_to_usdc(user_id, brl_amount)
        
        # Assert
        self.assertTrue(result['success'])
        self.assertEqual(result['usdc_amount'], Decimal('20.00'))
        self.mock_circle.mint_usdc.assert_called_once()
    
    def test_convert_brl_to_usdc_insufficient_balance(self):
        # Arrange
        user_id = 123
        brl_amount = Decimal('100.00')
        
        self.service._get_user_brl_balance = Mock(return_value=Decimal('50.00'))
        
        # Act
        result = self.service.convert_brl_to_usdc(user_id, brl_amount)
        
        # Assert
        self.assertFalse(result['success'])
        self.assertEqual(result['error'], 'Saldo insuficiente')
```

### 2. Testes de Integração

**Teste com ambiente sandbox:**
```python
class TestCircleIntegration(unittest.TestCase):
    def setUp(self):
        self.circle = CircleIntegration(
            api_key=os.getenv('CIRCLE_SANDBOX_API_KEY'),
            base_url='https://api-sandbox.circle.com'
        )
    
    def test_mint_usdc_sandbox(self):
        # Teste real com ambiente sandbox da Circle
        result = self.circle.mint_usdc(10.0, 'sandbox_wallet_id')
        self.assertIn('data', result)
```

## Deployment e DevOps

### 1. Containerização

**Dockerfile:**
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
```

### 2. Configuração Kubernetes

**deployment.yaml:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: picpay-usdc-service
spec:
  replicas: 3
  selector:
    matchLabels:
      app: picpay-usdc-service
  template:
    metadata:
      labels:
        app: picpay-usdc-service
    spec:
      containers:
      - name: picpay-usdc-service
        image: picpay/usdc-service:latest
        ports:
        - containerPort: 5000
        env:
        - name: CIRCLE_API_KEY
          valueFrom:
            secretKeyRef:
              name: circle-secrets
              key: api-key
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-secrets
              key: url
```

## Considerações de Performance

### 1. Cache

**Implementação de cache Redis:**
```python
import redis
import json

class CacheService:
    def __init__(self):
        self.redis_client = redis.Redis(host='localhost', port=6379, db=0)
    
    def cache_exchange_rate(self, from_currency: str, to_currency: str, rate: float, ttl: int = 300):
        """
        Cache taxa de câmbio por 5 minutos
        """
        key = f"exchange_rate:{from_currency}:{to_currency}"
        self.redis_client.setex(key, ttl, json.dumps({"rate": rate}))
    
    def get_cached_exchange_rate(self, from_currency: str, to_currency: str) -> Optional[float]:
        """
        Recupera taxa de câmbio do cache
        """
        key = f"exchange_rate:{from_currency}:{to_currency}"
        cached_data = self.redis_client.get(key)
        if cached_data:
            return json.loads(cached_data)["rate"]
        return None
```

### 2. Processamento Assíncrono

**Implementação com Celery:**
```python
from celery import Celery

celery_app = Celery('picpay_usdc')

@celery_app.task
def process_mint_transaction(user_id: int, amount: float, transaction_id: str):
    """
    Processa mint de USDC de forma assíncrona
    """
    # Implementar processamento assíncrono
    pass

@celery_app.task
def sync_blockchain_transactions():
    """
    Sincroniza transações da blockchain
    """
    # Implementar sincronização periódica
    pass
```

## Próximos Passos

### Fase 2: Pagamentos (Meses 4-6)

1. **Implementar Payments API**
   - Pagamentos P2P
   - Integração com merchants
   - Sistema de cashback

2. **Cartão Internacional**
   - Integração com processadora
   - Conversão automática USDC → moeda local
   - Controles de limite e segurança

### Fase 3: Expansão (Meses 7-9)

1. **Multi-blockchain**
   - Suporte a Polygon, Solana
   - Cross-chain transfers
   - Otimização de taxas

2. **Produtos Avançados**
   - Yield farming com USDC
   - Empréstimos garantidos por USDC
   - APIs para parceiros

## Conclusão

Este guia fornece uma base sólida para a implementação da solução PicPay Digital Assets. A arquitetura proposta é escalável, segura e está em conformidade com as melhores práticas da indústria.

Para dúvidas técnicas ou suporte durante a implementação, a equipe de Solutions Engineers da Circle está disponível para apoio contínuo.

---

**Contato Técnico:**
- Email: solutions@circle.com
- Documentação: https://developers.circle.com
- Suporte: https://support.circle.com

