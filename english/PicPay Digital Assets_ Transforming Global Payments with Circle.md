# PicPay Digital Assets: Transforming Global Payments with Circle
## Presentation Narrative Script

### Slide 1: Title Slide

Good morning/afternoon everyone. I'm [Your Name], Solutions Engineer at Circle, and today I'm excited to present a transformative opportunity for PicPay: integrating digital assets into your superapp ecosystem to revolutionize global payments for your 58 million users.

Over the next 30-40 minutes, I'll walk you through how Circle's infrastructure can help PicPay become the first Brazilian superapp with native digital dollar capabilities, dramatically improving your international payment offerings while creating new revenue streams.

### Slide 2: Agenda

Here's what we'll cover today:

First, we'll look at why now is the perfect time for this initiative, examining the Brazilian market landscape and PicPay's current challenges in international payments.

Then, I'll introduce Circle and our key products that power global financial infrastructure.

Next, we'll dive into our proposed solution, including the technical architecture and implementation approach.

We'll explore real-world use cases, quantify the business benefits, and outline a practical implementation roadmap.

By the end, you'll have a clear understanding of how this partnership can create significant value for PicPay and your users.

### Slide 3: Why Now?

Let's start with why this is the perfect moment for PicPay to embrace digital assets.

First, we're seeing explosive growth in cross-border demand. Brazilian e-commerce international purchases grew 45% in 2024, with over 10 million PicPay users already making international transactions annually.

Second, Brazil now has regulatory clarity. Law 14.478/22 established a clear framework for digital assets, with the Central Bank actively encouraging innovation in cross-border payments.

Third, the superapp evolution continues. To maintain your competitive edge, global payment capabilities are becoming essential as international players enter the Brazilian market.

Finally, Circle's recent partnership with Matera in June 2025 has created the infrastructure for seamless BRL-USDC integration in Brazilian financial institutions.

The chart on the right shows the pain points your users experience with cross-border payments. As you can see, high fees and slow processing times are the most significant issues, affecting 78% and 65% of users respectively.

### Slide 4: Brazilian Market Overview

Let's look at PicPay's position in the Brazilian market.

With 58 million active accounts, PicPay is the third-largest neobank in Brazil, behind Nubank and Inter. However, you have a unique advantage as the only one with true superapp positioning.

The Brazilian fintech market continues its impressive growth trajectory, reaching $18.7 billion in 2024 and projected to hit $22.1 billion this year.

Looking at payment methods, PIX dominates domestic transfers with 45% market share, but international payments remain fragmented and inefficient, creating an opportunity for innovation.

### Slide 5: PicPay's Current Challenges

Let's examine the specific challenges PicPay faces in international payments.

First, high international fees: Your users currently pay 4-6% in explicit fees through traditional banking partners, plus hidden FX spreads of 2-3%. This amounts to approximately R$120 million in excessive fees paid by your users annually.

Second, slow processing times: International transfers take 2-3 business days, causing frustration for users sending money to family abroad or making time-sensitive payments. Our research shows 65% of users report dissatisfaction with transfer speed.

Third, limited global reach: Your current infrastructure only supports 12 countries directly. Users must leave the PicPay ecosystem for unsupported regions, with 40% of international payment attempts failing or requiring redirection.

Finally, competitive pressure: Global fintechs like Wise and Revolut are entering Brazil with native multi-currency solutions. Nubank and Inter are developing similar offerings, threatening your superapp strategy and potentially leading to a loss of 15% of high-value users within 12 months.

### Slide 6: Circle: Global Financial Infrastructure

Now, let me introduce Circle and our solutions.

Circle is a global financial technology firm that enables businesses to harness the power of digital currencies and public blockchains for payments, commerce, and financial applications worldwide.

We have over $50 billion in USDC in circulation, support 180+ countries, process 10+ million monthly transactions, and serve 1,000+ enterprise customers.

For PicPay, we're proposing three key products:

First, Circle Mint: Our enterprise-grade solution for minting and redeeming USDC stablecoins, enabling seamless conversion between fiat and digital currencies.

Second, Cross-Currency API: This enables instant, low-cost currency conversions and transfers across borders using USDC as a bridge currency.

Third, Payments API: Allowing you to accept and make payments globally using traditional and digital currencies with unified settlement.

These products work together to create a comprehensive solution for PicPay's global payment needs.

### Slide 7: PicPay Digital Assets Solution

Here's our proposed solution: seamlessly integrating USDC into PicPay's superapp ecosystem.

At the core, we have PicPay on the left and Circle on the right, with USDC serving as the bridge between them. The flow is simple: users convert BRL to USDC using Circle Mint, and can convert back from USDC to BRL when needed.

This solution enables four key features:

1. Native USDC Wallet: Fully integrated within the PicPay app, allowing users to hold, send, and receive USDC alongside BRL balances.

2. Instant Conversion: One-click conversion between BRL and USDC with competitive rates and minimal fees.

3. Global Transfers: Send money internationally in minutes instead of days, with up to 50% lower fees than traditional methods.

4. International Payments: Pay international merchants directly with USDC or instantly convert to local currency at point of sale.

This creates a seamless experience for users, merchants, and the broader financial ecosystem.

### Slide 8: Technical Architecture

Let's look at the technical architecture of the solution.

The architecture consists of four layers:

At the top, we have the PicPay Mobile App Layer with the USDC Wallet UI, Conversion UI, and Transfer UI components.

Below that is the PicPay Backend Layer with User Service, USDC Service, and Payment Service.

The third layer is the Circle API Layer, featuring Circle Mint API and Cross-Currency API.

At the bottom is the Blockchain Layer, where we'll initially support Ethereum and Polygon.

On the right, you can see the implementation steps and recommended tech stack. We suggest using Node.js or Java for the backend, PostgreSQL for the database, HSM/KMS for security, and Datadog or New Relic for monitoring.

The code example shows how simple it is to integrate with the Circle Mint API for converting BRL to USDC.

### Slide 9: Use Cases

Let's explore four key use cases that demonstrate the value of this solution.

First, Instant Remittances: Currently, international transfers take up to 2 business days. With our solution, users convert BRL to USDC and transfer instantly, reducing the process from days to minutes.

Second, Multi-Currency Wallet: Many PicPay users find their debit cards don't work abroad. Our solution provides BRL, USD, and USDC balances in the same wallet, creating a unified global experience.

Third, International E-commerce: Users currently face high spreads on credit cards for international purchases. With direct USDC payments, they'll enjoy lower fees and even USDC cashback.

Fourth, Digital Dollar Savings: Many Brazilians want USD exposure but find it difficult to access. Our solution allows easy BRL to USDC conversion as "dollar savings," providing a currency hedge with full liquidity.

### Slide 10: Benefits and ROI

Let's quantify the benefits of this solution.

For PicPay, the benefits include:
- Competitive differentiation as the first superapp with native USDC
- New revenue stream from FX spreads without intermediaries
- Improved user retention with USDC balances
- Infrastructure for international expansion

For users, the benefits include:
- Speed: International transfers in minutes
- Lower costs: Up to 50% reduction in fees
- Convenience: Everything in one app
- Global access: Simplified international payments

Looking at projections, we expect to reach $100M USDC in circulation and 1M active users within the first year. The cost comparison chart shows dramatic improvements in FX rates, transfer fees, and processing time compared to the current process.

### Slide 11: Implementation Roadmap

Here's our proposed implementation roadmap, divided into three phases:

Phase 1 (MVP) in the first 3 months focuses on Circle Mint API integration, basic interface development, USDC wallet implementation, and initial compliance work.

Phase 2 (Payments) in months 4-6 expands to USDC P2P transfers, international merchant payments, international card with USDC balance, and a USDC cashback program.

Phase 3 (Expansion) in months 7-9 adds support for more blockchains, EURC for the European market, APIs for partners, and advanced financial products.

On the regulatory side, we'll help you navigate Law 14.478/22, obtain VASP authorization from the Central Bank, and leverage your existing KYC/AML infrastructure.

For next steps, we propose signing an MOU, providing access to Circle's sandbox environment, defining the technical team, conducting a detailed workshop, and creating an implementation timeline.

### Slide 12: Call to Action

In conclusion, we invite you to join Circle and PicPay in transforming global payments together.

This partnership will create the first Brazilian superapp with native digital assets, offering a unified global experience for your 58 million users.

Our next steps are clear: MOU signing, sandbox access, technical team definition, and implementation timeline development.

I'm excited about the potential of this partnership and look forward to your questions. Thank you for your attention.

## Handling Potential Questions

### Technical Questions

**Q: How secure is the USDC infrastructure?**
A: USDC operates on public blockchains with battle-tested security. Circle employs institutional-grade security measures, including multi-signature wallets, cold storage, and regular security audits. All USDC is fully backed by cash and short-dated U.S. government obligations, with monthly attestations from major accounting firms.

**Q: What happens if a user sends USDC to the wrong address?**
A: The PicPay interface will include multiple safeguards to prevent errors, such as address book functionality, QR code scanning, and confirmation screens. However, blockchain transactions are irreversible by design. We recommend implementing a gradual approach to transfer limits and whitelisted addresses to mitigate this risk.

**Q: How will the system handle high transaction volumes?**
A: Circle's infrastructure is designed for enterprise-scale operations, currently processing millions of transactions monthly. The architecture includes load balancing, auto-scaling, and redundancy. We'll work with your team to implement proper caching strategies and asynchronous processing for optimal performance.

### Business Questions

**Q: How does this solution compare to traditional correspondent banking relationships?**
A: Traditional correspondent banking involves multiple intermediaries, each adding fees and delays. Our solution creates a direct path using USDC as a bridge currency, reducing fees by up to 50% and settlement times from days to minutes. It also provides greater transparency and 24/7 operation versus banking hours.

**Q: What's the revenue model for PicPay?**
A: PicPay can generate revenue through: 1) Conversion fees when users exchange BRL to USDC and vice versa (typically 0.5-1%), 2) International transfer fees that are competitive yet profitable, 3) Merchant services fees for international payment processing, and 4) Premium features for power users or businesses.

**Q: How will this affect our relationships with existing banking partners?**
A: This solution complements rather than replaces your banking relationships. For large-value or specialized transactions, traditional banking channels remain important. We recommend a phased approach, starting with consumer remittances and e-commerce payments, then gradually expanding based on performance and user feedback.

### Regulatory Questions

**Q: How does this comply with Brazilian regulations?**
A: Brazil's Law 14.478/22 established a clear framework for virtual assets. PicPay will register as a Virtual Asset Service Provider (VASP) with the Central Bank. Circle is committed to regulatory compliance and has a dedicated team to support partners through the regulatory process. Our solution leverages your existing KYC/AML infrastructure, which already meets regulatory requirements.

**Q: What about tax implications for users?**
A: Users will need to report capital gains or losses from USDC transactions, similar to foreign currency transactions. We'll provide comprehensive transaction reports and educational content to help users understand their tax obligations. The solution can also include features to help track cost basis and calculate gains/losses.

**Q: How will you handle compliance with international regulations?**
A: Circle maintains compliance with regulations across 180+ countries where we operate. Our APIs include built-in compliance tools for transaction monitoring, sanctions screening, and suspicious activity reporting. We'll work with your compliance team to ensure all international transfers meet both Brazilian and destination country requirements.

### Implementation Questions

**Q: What resources will we need to allocate for this project?**
A: For successful implementation, we recommend: 4-6 backend developers, 2-3 frontend developers, 1 dedicated product manager, 1-2 compliance specialists, 1 security engineer, and 2-3 QA engineers. Circle will provide a dedicated solutions engineer, technical documentation, sample code, and regular check-in meetings.

**Q: How will this integrate with our existing systems?**
A: We'll provide comprehensive APIs and SDKs that can integrate with your existing payment infrastructure. The solution is designed to be modular, allowing you to implement components incrementally. We'll conduct a detailed technical workshop to map integration points with your user management, payment processing, and accounting systems.

**Q: What happens if Circle or USDC face issues?**
A: USDC is fully reserved and regularly audited, making it one of the most stable digital assets. Circle has robust business continuity plans and multiple redundancies. However, we recommend implementing circuit breakers and fallback mechanisms as part of the integration to ensure service continuity under any circumstances.

