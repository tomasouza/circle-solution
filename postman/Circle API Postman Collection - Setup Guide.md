# Circle API Postman Collection - Setup Guide

## 📋 Overview

This Postman collection provides a comprehensive set of API calls for integrating PicPay with Circle's APIs, including:

- **Circle Mint API** - BRL ↔ USDC conversion
- **Circle Cross-Currency API** - International transfers  
- **Circle Payments API** - Wallet management
- **Webhook Testing** - Notification simulation

## 🚀 Quick Setup

### 1. Import Collection & Environment

1. **Import Collection**: Import `Circle_API_PicPay_Integration.postman_collection.json`
2. **Import Environment**: Import `Circle_API_PicPay_Integration.postman_environment.json`
3. **Select Environment**: Choose "Circle PicPay Integration - Sandbox" environment

### 2. Configure API Key

1. Go to **Environments** → **Circle PicPay Integration - Sandbox**
2. Update the `circle_api_key` variable with your actual Circle Sandbox API key:
   ```
   SAND_API_KEY:your-actual-sandbox-api-key-here
   ```

### 3. Get Your Circle Sandbox API Key

1. Visit [Circle Developer Console](https://console.circle.com/)
2. Sign up/Login to your account
3. Navigate to **API Keys** section
4. Create a new **Sandbox API Key**
5. Copy the key (format: `SAND_API_KEY:xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`)

## 📁 Collection Structure

### 1. **Account & Configuration**
- Get Account Configuration
- Get Business Account Details  
- Get PIX Bank Accounts

### 2. **Circle Mint API - BRL ↔ USDC**
- Create BRL → USDC Quote
- Create USDC → BRL Quote (Redeem)
- Execute Trade (Mint/Redeem)
- Get Trade Status
- Get Settlement Batches
- Get PIX Payment Instructions

### 3. **Cross-Currency API - International Transfers**
- Create Cross-Currency Quote
- Create International Transfer
- Get Transfer Status
- List All Transfers

### 4. **Wallets & Payments API**
- List Wallets
- Create Wallet
- Get Wallet Details
- Generate Blockchain Address
- List Wallet Addresses

### 5. **Webhook Testing**
- Trade Complete Webhook
- Settlement Complete Webhook
- Transfer Complete Webhook

### 6. **Monitoring & Analytics**
- Get Exchange Rates
- List All Trades
- Get Account Balance

## 🔄 Typical Workflow Examples

### **BRL → USDC Mint Process**

1. **Create BRL → USDC Quote**
   - Amount: R$ 100
   - Auto-stores `quote_id` in environment

2. **Execute Trade (Mint)**
   - Uses stored `quote_id`
   - Auto-stores `trade_id` and `settlement_id`

3. **Get PIX Payment Instructions**
   - Get bank details for BRL settlement

4. **Get Trade Status**
   - Monitor trade completion

### **International Transfer Process**

1. **Create BRL → USDC Quote** (from Mint API)
2. **Execute Trade** to get USDC
3. **Create Cross-Currency Quote** (USDC → USD)
4. **Create International Transfer**
5. **Get Transfer Status** to monitor delivery

### **USDC → BRL Redeem Process**

1. **Create USDC → BRL Quote**
2. **Execute Trade (Redeem)**
3. **Get Trade Status**
4. Monitor settlement via webhooks

## 🔧 Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `circle_base_url` | Circle Sandbox API URL | `https://api-sandbox.circle.com` |
| `circle_api_key` | Your Circle API Key | `SAND_API_KEY:your-key-here` |
| `picpay_wallet_id` | PicPay Master Wallet ID | `1000066041` |
| `webhook_endpoint` | PicPay Webhook URL | `https://picpay.com/webhooks/circle` |
| `idempotency_key` | Dynamic UUID | Auto-generated |
| `quote_id` | Stored from quote responses | Auto-populated |
| `trade_id` | Stored from trade responses | Auto-populated |
| `settlement_id` | Stored from settlement responses | Auto-populated |
| `transfer_id` | Stored from transfer responses | Auto-populated |

## 🔐 Authentication

The collection uses **Bearer Token** authentication with your Circle API key. The authentication is configured at the collection level, so all requests automatically include the authorization header.

## ⚡ Auto-Scripts

The collection includes JavaScript test scripts that automatically:

- Generate unique idempotency keys for each request
- Store response IDs (quote_id, trade_id, etc.) for subsequent requests
- Log important values to the console for debugging

## 🧪 Testing Webhooks

The webhook testing folder includes sample webhook payloads that Circle would send to PicPay:

- **Trade Complete**: When BRL ↔ USDC conversion finishes
- **Settlement Complete**: When PIX settlement completes  
- **Transfer Complete**: When international transfer finishes

**Note**: Update the `X-Circle-Signature` header with actual HMAC signatures for production testing.

## 📊 Monitoring & Analytics

Use the monitoring endpoints to:

- Track exchange rates over time
- Analyze trade volumes and patterns
- Monitor account balances
- Generate compliance reports

## 🚨 Important Notes

1. **Sandbox Environment**: This collection is configured for Circle's sandbox environment
2. **Quote Expiry**: Quotes expire in 30 seconds - execute trades quickly
3. **Idempotency**: Each request uses a unique idempotency key to prevent duplicates
4. **Rate Limits**: Circle has rate limits - avoid rapid successive calls
5. **PIX Integration**: Actual PIX transfers require integration with Brazilian banking system

## 🔗 Additional Resources

- [Circle API Documentation](https://developers.circle.com/)
- [Circle Mint API Guide](https://developers.circle.com/circle-mint)
- [Circle Cross-Currency API Guide](https://developers.circle.com/cross-currency)
- [PIX Integration Guide](https://developers.circle.com/pix)

## 🆘 Troubleshooting

### Common Issues:

1. **401 Unauthorized**: Check your API key format and validity
2. **Quote Expired**: Quotes expire in 30 seconds, create new quote
3. **Insufficient Balance**: Ensure adequate balance in source currency
4. **Invalid Wallet ID**: Verify wallet exists and is accessible

### Debug Tips:

- Check Postman Console for auto-generated values
- Verify environment variables are set correctly
- Use the monitoring endpoints to check account status
- Test with small amounts first

