# Thai Payment Integration

## Overview

Integration with Thai payment systems including PromptPay, Thai QR Payment Standard, and local payment gateways (Omise, 2C2P). This skill covers payment processing, reconciliation, refunds, and compliance with Bank of Thailand regulations.

---

## 1. Thai Payment Landscape

### Payment Methods in Thailand

```markdown
# Thai Payment Methods

## Popular Payment Methods
1. **PromptPay**: National e-payment system
2. **Thai QR Payment**: Standardized QR code payment
3. **Credit/Debit Cards**: Visa, Mastercard, JCB
4. **Mobile Banking**: SCB Easy, Krungthai NEXT, Bangkok Bank Mobile
5. **E-Wallets**: TrueMoney, Rabbit LINE Pay, AirPay
6. **Cash on Delivery**: Still popular for e-commerce

## Market Share (2026)
- PromptPay/QR: 45%
- Mobile Banking: 25%
- Credit/Debit Cards: 20%
- E-Wallets: 8%
- Others: 2%
```

### Bank of Thailand Regulations

```markdown
# BOT Regulations

## Key Requirements
1. **PCI DSS Compliance**: For card payments
2. **Data Localization**: Customer data must be stored in Thailand
3. **KYC Requirements**: Know Your Customer verification
4. **Transaction Limits**: Daily/monthly limits for different payment types
5. **Refund Policy**: Must support refunds within 30 days
6. **Reporting**: Monthly transaction reports to BOT

## PromptPay Regulations
- Maximum transaction: 50,000 THB per transaction
- Daily limit: 200,000 THB
- QR code expiry: Maximum 15 minutes
- Settlement: T+1 (next business day)
```

---

## 2. PromptPay Integration

### PromptPay QR Code Generation

```typescript
// PromptPay QR Code Generator
import QRCode from 'qrcode'
import crc16 from 'crc/crc16xmodem'

interface PromptPayQROptions {
  phoneNumber?: string
  nationalId?: string
  eWalletId?: string
  amount?: number
  reference?: string
}

class PromptPayQR {
  private static readonly PAYLOAD_FORMAT_INDICATOR = '000201'
  private static readonly POINT_OF_INITIATION = '010212'
  private static readonly MERCHANT_CATEGORY_CODE = '5311'
  private static readonly TRANSACTION_CURRENCY = '5303764' // THB
  private static readonly COUNTRY_CODE = '5802TH'

  static generateQR(options: PromptPayQROptions): string {
    let payload = ''

    // Payload Format Indicator
    payload += this.PAYLOAD_FORMAT_INDICATOR

    // Point of Initiation Method
    payload += this.POINT_OF_INITIATION

    // Merchant Account Information
    payload += this.buildMerchantInfo(options)

    // Merchant Category Code
    payload += '52040000'

    // Transaction Currency
    payload += this.TRANSACTION_CURRENCY

    // Transaction Amount
    if (options.amount) {
      const amountStr = options.amount.toFixed(2)
      payload += `54${String(amountStr.length).padStart(2, '0')}${amountStr}`
    }

    // Country Code
    payload += this.COUNTRY_CODE

    // Additional Data
    if (options.reference) {
      const ref = options.reference.substring(0, 25)
      payload += `62${String(ref.length + 4).padStart(2, '0')}05${String(ref.length).padStart(2, '0')}${ref}`
    }

    // CRC
    payload += '6304'
    const crc = this.calculateCRC(payload)
    payload += crc

    return payload
  }

  private static buildMerchantInfo(options: PromptPayQROptions): string {
    const AID = '0016A000000677010111'
    let merchantInfo = AID

    if (options.phoneNumber) {
      // Mobile number format: 0066XXXXXXXXX (remove leading 0, add country code)
      const mobile = options.phoneNumber.replace(/^0/, '66')
      merchantInfo += `01${String(mobile.length).padStart(2, '0')}${mobile}`
    } else if (options.nationalId) {
      // National ID or Tax ID
      merchantInfo += `02${String(options.nationalId.length).padStart(2, '0')}${options.nationalId}`
    } else if (options.eWalletId) {
      // E-Wallet ID
      merchantInfo += `03${String(options.eWalletId.length).padStart(2, '0')}${options.eWalletId}`
    }

    return `29${String(merchantInfo.length).padStart(2, '0')}${merchantInfo}`
  }

  private static calculateCRC(payload: string): string {
    const crc = crc16(payload).toString(16).toUpperCase().padStart(4, '0')
    return crc
  }

  static async generateQRImage(options: PromptPayQROptions): Promise<string> {
    const qrString = this.generateQR(options)
    return await QRCode.toDataURL(qrString)
  }
}

// Usage Example
const qrCode = await PromptPayQR.generateQRImage({
  phoneNumber: '0812345678',
  amount: 1500.00,
  reference: 'INV-2026-001'
})

console.log('QR Code Data URL:', qrCode)
```

### PromptPay Payment Verification

```typescript
// PromptPay Payment Verification
interface PromptPayTransaction {
  transactionId: string
  amount: number
  reference: string
  timestamp: Date
  status: 'pending' | 'completed' | 'failed'
}

class PromptPayVerification {
  async verifyPayment(
    transactionId: string,
    expectedAmount: number,
    reference: string
  ): Promise<boolean> {
    try {
      // Call bank API to verify payment
      const transaction = await this.fetchTransaction(transactionId)

      // Verify amount matches
      if (Math.abs(transaction.amount - expectedAmount) > 0.01) {
        console.error('Amount mismatch')
        return false
      }

      // Verify reference matches
      if (transaction.reference !== reference) {
        console.error('Reference mismatch')
        return false
      }

      // Verify transaction is completed
      if (transaction.status !== 'completed') {
        console.error('Transaction not completed')
        return false
      }

      return true
    } catch (error) {
      console.error('Payment verification failed:', error)
      return false
    }
  }

  private async fetchTransaction(transactionId: string): Promise<PromptPayTransaction> {
    // Implementation depends on bank API
    // This is a placeholder
    const response = await fetch(`/api/promptpay/transactions/${transactionId}`)
    return await response.json()
  }
}
```

---

## 3. Thai QR Payment Standard

### Thai QR Code Generation

```typescript
// Thai QR Payment Standard (EMVCo)
interface ThaiQROptions {
  merchantId: string
  merchantName: string
  amount?: number
  billerId?: string
  reference1?: string
  reference2?: string
  terminalId?: string
}

class ThaiQRPayment {
  static generateQR(options: ThaiQROptions): string {
    let payload = ''

    // Payload Format Indicator
    payload += '000201'

    // Point of Initiation Method
    if (options.amount) {
      payload += '010212' // Dynamic QR
    } else {
      payload += '010211' // Static QR
    }

    // Merchant Account Information (Tag 30)
    payload += this.buildMerchantAccount(options)

    // Merchant Category Code
    payload += '52045814' // Retail

    // Transaction Currency (THB)
    payload += '5303764'

    // Transaction Amount
    if (options.amount) {
      const amountStr = options.amount.toFixed(2)
      payload += `54${String(amountStr.length).padStart(2, '0')}${amountStr}`
    }

    // Country Code
    payload += '5802TH'

    // Merchant Name
    const merchantName = options.merchantName.substring(0, 25)
    payload += `59${String(merchantName.length).padStart(2, '0')}${merchantName}`

    // Additional Data Field Template
    payload += this.buildAdditionalData(options)

    // CRC
    payload += '6304'
    const crc = this.calculateCRC(payload)
    payload += crc

    return payload
  }

  private static buildMerchantAccount(options: ThaiQROptions): string {
    const AID = '0016A000000677010111'
    let merchantInfo = AID

    // Merchant ID (Tag 01)
    merchantInfo += `01${String(options.merchantId.length).padStart(2, '0')}${options.merchantId}`

    // Biller ID (Tag 02) - Optional
    if (options.billerId) {
      merchantInfo += `02${String(options.billerId.length).padStart(2, '0')}${options.billerId}`
    }

    return `30${String(merchantInfo.length).padStart(2, '0')}${merchantInfo}`
  }

  private static buildAdditionalData(options: ThaiQROptions): string {
    let additionalData = ''

    // Bill Number (Tag 01)
    if (options.reference1) {
      const ref1 = options.reference1.substring(0, 25)
      additionalData += `01${String(ref1.length).padStart(2, '0')}${ref1}`
    }

    // Reference Number (Tag 02)
    if (options.reference2) {
      const ref2 = options.reference2.substring(0, 25)
      additionalData += `02${String(ref2.length).padStart(2, '0')}${ref2}`
    }

    // Terminal ID (Tag 07)
    if (options.terminalId) {
      const terminal = options.terminalId.substring(0, 8)
      additionalData += `07${String(terminal.length).padStart(2, '0')}${terminal}`
    }

    if (additionalData) {
      return `62${String(additionalData.length).padStart(2, '0')}${additionalData}`
    }

    return ''
  }

  private static calculateCRC(payload: string): string {
    // CRC-16/CCITT-FALSE
    let crc = 0xFFFF
    for (let i = 0; i < payload.length; i++) {
      crc ^= payload.charCodeAt(i) << 8
      for (let j = 0; j < 8; j++) {
        if (crc & 0x8000) {
          crc = (crc << 1) ^ 0x1021
        } else {
          crc = crc << 1
        }
      }
    }
    return (crc & 0xFFFF).toString(16).toUpperCase().padStart(4, '0')
  }
}

// Usage Example
const thaiQR = ThaiQRPayment.generateQR({
  merchantId: '1234567890123',
  merchantName: 'Malai Platform',
  amount: 2500.00,
  reference1: 'ORDER-2026-001',
  reference2: 'CUSTOMER-12345',
  terminalId: 'TERM001'
})
```

---

## 4. Payment Gateway Integration

### Omise Integration

```typescript
// Omise Payment Gateway Integration
import Omise from 'omise'

interface OmiseConfig {
  publicKey: string
  secretKey: string
}

interface ChargeOptions {
  amount: number // in satang (1 THB = 100 satang)
  currency: string
  description: string
  customer?: string
  card?: string
  source?: string
  metadata?: Record<string, any>
}

class OmisePayment {
  private omise: any

  constructor(config: OmiseConfig) {
    this.omise = Omise({
      publicKey: config.publicKey,
      secretKey: config.secretKey,
    })
  }

  async createCharge(options: ChargeOptions): Promise<any> {
    try {
      const charge = await this.omise.charges.create({
        amount: options.amount,
        currency: options.currency || 'THB',
        description: options.description,
        customer: options.customer,
        card: options.card,
        source: options.source,
        metadata: options.metadata,
        return_uri: `${process.env.APP_URL}/payment/callback`,
      })

      return charge
    } catch (error) {
      console.error('Charge creation failed:', error)
      throw error
    }
  }

  async createPromptPayCharge(
    amount: number,
    description: string,
    metadata?: Record<string, any>
  ): Promise<any> {
    try {
      // Create PromptPay source
      const source = await this.omise.sources.create({
        type: 'promptpay',
        amount: amount,
        currency: 'THB',
      })

      // Create charge with PromptPay source
      const charge = await this.createCharge({
        amount,
        currency: 'THB',
        description,
        source: source.id,
        metadata,
      })

      return {
        charge,
        qrCodeUrl: source.scannable_code.image.download_uri,
      }
    } catch (error) {
      console.error('PromptPay charge creation failed:', error)
      throw error
    }
  }

  async createInternetBankingCharge(
    amount: number,
    bank: string,
    description: string
  ): Promise<any> {
    try {
      const source = await this.omise.sources.create({
        type: 'internet_banking_' + bank, // e.g., 'internet_banking_scb'
        amount: amount,
        currency: 'THB',
      })

      const charge = await this.createCharge({
        amount,
        currency: 'THB',
        description,
        source: source.id,
      })

      return {
        charge,
        authorizeUri: charge.authorize_uri,
      }
    } catch (error) {
      console.error('Internet banking charge creation failed:', error)
      throw error
    }
  }

  async getCharge(chargeId: string): Promise<any> {
    return await this.omise.charges.retrieve(chargeId)
  }

  async refundCharge(chargeId: string, amount?: number): Promise<any> {
    try {
      const refund = await this.omise.refunds.create(chargeId, {
        amount: amount, // If not specified, full refund
      })

      return refund
    } catch (error) {
      console.error('Refund failed:', error)
      throw error
    }
  }
}

// Usage Example
const omise = new OmisePayment({
  publicKey: process.env.OMISE_PUBLIC_KEY!,
  secretKey: process.env.OMISE_SECRET_KEY!,
})

// Create PromptPay charge
const promptPayCharge = await omise.createPromptPayCharge(
  150000, // 1,500 THB in satang
  'Event Booking Payment',
  { orderId: 'ORDER-001', userId: 'USER-123' }
)

console.log('QR Code URL:', promptPayCharge.qrCodeUrl)
```

### 2C2P Integration

```typescript
// 2C2P Payment Gateway Integration
import crypto from 'crypto'

interface C2PConfig {
  merchantId: string
  secretKey: string
  apiUrl: string
}

interface PaymentRequest {
  amount: number
  currency: string
  description: string
  orderId: string
  customerEmail: string
  customerName: string
  returnUrl: string
}

class C2PPayment {
  private config: C2PConfig

  constructor(config: C2PConfig) {
    this.config = config
  }

  async createPayment(request: PaymentRequest): Promise<any> {
    const payload = {
      merchantID: this.config.merchantId,
      invoiceNo: request.orderId,
      description: request.description,
      amount: (request.amount / 100).toFixed(2), // Convert from satang
      currencyCode: request.currency,
      customerEmail: request.customerEmail,
      customerName: request.customerName,
      returnUrl: request.returnUrl,
    }

    // Generate hash
    const hash = this.generateHash(payload)
    payload['hashValue'] = hash

    // Send request to 2C2P
    const response = await fetch(`${this.config.apiUrl}/payment/request`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
    })

    return await response.json()
  }

  private generateHash(payload: any): string {
    const data = `${payload.merchantID}${payload.invoiceNo}${payload.amount}${payload.currencyCode}${this.config.secretKey}`
    return crypto.createHash('sha256').update(data).digest('hex')
  }

  verifyCallback(params: any): boolean {
    const receivedHash = params.hashValue
    const calculatedHash = this.generateHash(params)
    return receivedHash === calculatedHash
  }

  async refund(transactionId: string, amount: number): Promise<any> {
    const payload = {
      merchantID: this.config.merchantId,
      transactionID: transactionId,
      amount: (amount / 100).toFixed(2),
    }

    const hash = this.generateHash(payload)
    payload['hashValue'] = hash

    const response = await fetch(`${this.config.apiUrl}/payment/refund`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
    })

    return await response.json()
  }
}
```

---

## 5. Payment Reconciliation

### Transaction Reconciliation

```typescript
// Payment Reconciliation System
interface Transaction {
  id: string
  orderId: string
  amount: number
  currency: string
  status: 'pending' | 'completed' | 'failed' | 'refunded'
  paymentMethod: string
  gatewayTransactionId?: string
  createdAt: Date
  completedAt?: Date
}

class PaymentReconciliation {
  async reconcileDaily(date: Date): Promise<{
    matched: Transaction[]
    unmatched: Transaction[]
    discrepancies: any[]
  }> {
    // Fetch transactions from database
    const dbTransactions = await this.fetchDBTransactions(date)

    // Fetch transactions from payment gateway
    const gatewayTransactions = await this.fetchGatewayTransactions(date)

    const matched: Transaction[] = []
    const unmatched: Transaction[] = []
    const discrepancies: any[] = []

    // Match transactions
    for (const dbTx of dbTransactions) {
      const gatewayTx = gatewayTransactions.find(
        (tx) => tx.id === dbTx.gatewayTransactionId
      )

      if (!gatewayTx) {
        unmatched.push(dbTx)
        continue
      }

      // Check for discrepancies
      if (Math.abs(dbTx.amount - gatewayTx.amount) > 0.01) {
        discrepancies.push({
          transaction: dbTx,
          issue: 'amount_mismatch',
          dbAmount: dbTx.amount,
          gatewayAmount: gatewayTx.amount,
        })
      }

      matched.push(dbTx)
    }

    return { matched, unmatched, discrepancies }
  }

  private async fetchDBTransactions(date: Date): Promise<Transaction[]> {
    // Fetch from database
    // Implementation depends on your database
    return []
  }

  private async fetchGatewayTransactions(date: Date): Promise<any[]> {
    // Fetch from payment gateway
    // Implementation depends on your gateway
    return []
  }

  async generateReconciliationReport(date: Date): Promise<string> {
    const result = await this.reconcileDaily(date)

    let report = `Payment Reconciliation Report - ${date.toISOString()}\n\n`
    report += `Matched Transactions: ${result.matched.length}\n`
    report += `Unmatched Transactions: ${result.unmatched.length}\n`
    report += `Discrepancies: ${result.discrepancies.length}\n\n`

    if (result.unmatched.length > 0) {
      report += `Unmatched Transactions:\n`
      result.unmatched.forEach((tx) => {
        report += `- ${tx.id}: ${tx.amount} ${tx.currency}\n`
      })
    }

    if (result.discrepancies.length > 0) {
      report += `\nDiscrepancies:\n`
      result.discrepancies.forEach((d) => {
        report += `- ${d.transaction.id}: ${d.issue} (DB: ${d.dbAmount}, Gateway: ${d.gatewayAmount})\n`
      })
    }

    return report
  }
}
```

---

## 6. Refund Workflows

### Refund Processing

```typescript
// Refund Management
interface RefundRequest {
  transactionId: string
  amount?: number // Partial refund if specified
  reason: string
  requestedBy: string
}

interface Refund {
  id: string
  transactionId: string
  amount: number
  status: 'pending' | 'processing' | 'completed' | 'failed'
  reason: string
  requestedBy: string
  requestedAt: Date
  completedAt?: Date
}

class RefundManager {
  async createRefund(request: RefundRequest): Promise<Refund> {
    // Validate transaction
    const transaction = await this.getTransaction(request.transactionId)

    if (!transaction) {
      throw new Error('Transaction not found')
    }

    if (transaction.status !== 'completed') {
      throw new Error('Cannot refund incomplete transaction')
    }

    // Calculate refund amount
    const refundAmount = request.amount || transaction.amount

    if (refundAmount > transaction.amount) {
      throw new Error('Refund amount exceeds transaction amount')
    }

    // Create refund record
    const refund: Refund = {
      id: this.generateRefundId(),
      transactionId: request.transactionId,
      amount: refundAmount,
      status: 'pending',
      reason: request.reason,
      requestedBy: request.requestedBy,
      requestedAt: new Date(),
    }

    // Save to database
    await this.saveRefund(refund)

    // Process refund with payment gateway
    await this.processRefundWithGateway(refund)

    return refund
  }

  private async processRefundWithGateway(refund: Refund): Promise<void> {
    try {
      // Update status to processing
      refund.status = 'processing'
      await this.updateRefund(refund)

      // Call payment gateway API
      // Implementation depends on gateway
      const transaction = await this.getTransaction(refund.transactionId)

      if (transaction.paymentMethod === 'omise') {
        // Process with Omise
        await this.processOmiseRefund(refund)
      } else if (transaction.paymentMethod === '2c2p') {
        // Process with 2C2P
        await this.process2C2PRefund(refund)
      }

      // Update status to completed
      refund.status = 'completed'
      refund.completedAt = new Date()
      await this.updateRefund(refund)
    } catch (error) {
      refund.status = 'failed'
      await this.updateRefund(refund)
      throw error
    }
  }

  private async processOmiseRefund(refund: Refund): Promise<void> {
    // Implementation for Omise refund
  }

  private async process2C2PRefund(refund: Refund): Promise<void> {
    // Implementation for 2C2P refund
  }

  private generateRefundId(): string {
    return `REF-${Date.now()}`
  }

  private async getTransaction(id: string): Promise<Transaction | null> {
    // Fetch from database
    return null
  }

  private async saveRefund(refund: Refund): Promise<void> {
    // Save to database
  }

  private async updateRefund(refund: Refund): Promise<void> {
    // Update in database
  }
}
```

---

## 7. Multi-Currency Support

### Currency Conversion

```typescript
// Currency Conversion for Thai Payments
interface ExchangeRate {
  from: string
  to: string
  rate: number
  timestamp: Date
}

class CurrencyConverter {
  private rates: Map<string, ExchangeRate> = new Map()

  async getExchangeRate(from: string, to: string): Promise<number> {
    const key = `${from}-${to}`
    const cached = this.rates.get(key)

    // Use cached rate if less than 1 hour old
    if (cached && Date.now() - cached.timestamp.getTime() < 3600000) {
      return cached.rate
    }

    // Fetch latest rate
    const rate = await this.fetchExchangeRate(from, to)

    this.rates.set(key, {
      from,
      to,
      rate,
      timestamp: new Date(),
    })

    return rate
  }

  private async fetchExchangeRate(from: string, to: string): Promise<number> {
    // Fetch from exchange rate API
    // Example: https://api.exchangerate-api.com/v4/latest/THB
    const response = await fetch(`https://api.exchangerate-api.com/v4/latest/${from}`)
    const data = await response.json()
    return data.rates[to]
  }

  async convert(amount: number, from: string, to: string): Promise<number> {
    if (from === to) return amount

    const rate = await this.getExchangeRate(from, to)
    return amount * rate
  }

  formatTHB(amount: number): string {
    return new Intl.NumberFormat('th-TH', {
      style: 'currency',
      currency: 'THB',
    }).format(amount)
  }
}

// Usage Example
const converter = new CurrencyConverter()

const usdAmount = 100
const thbAmount = await converter.convert(usdAmount, 'USD', 'THB')
console.log(`${usdAmount} USD = ${converter.formatTHB(thbAmount)}`)
```

---

## Best Practices

1. **Security**
   - Never store card details directly
   - Use PCI DSS compliant payment gateways
   - Implement proper encryption for sensitive data
   - Validate all payment callbacks with signatures

2. **User Experience**
   - Show QR codes with clear expiry times
   - Provide multiple payment options
   - Display payment status in real-time
   - Send payment confirmations via email/SMS

3. **Compliance**
   - Follow Bank of Thailand regulations
   - Implement proper KYC procedures
   - Store customer data in Thailand
   - Maintain transaction logs for auditing

4. **Error Handling**
   - Handle payment timeouts gracefully
   - Implement retry mechanisms
   - Provide clear error messages in Thai
   - Log all payment errors for debugging

5. **Testing**
   - Use sandbox environments for testing
   - Test all payment methods thoroughly
   - Verify refund workflows
   - Test edge cases (timeouts, network errors)

---

## Common Pitfalls

1. **QR Code Expiry**: Not implementing proper QR code expiry can lead to duplicate payments
2. **Amount Mismatch**: Always verify amounts in the smallest currency unit (satang)
3. **Callback Verification**: Always verify payment gateway callbacks to prevent fraud
4. **Refund Timing**: Some payment methods have different refund processing times
5. **Currency Conversion**: Be careful with rounding errors in currency conversion

---

## Production Checklist

- [ ] PCI DSS compliance verified
- [ ] Payment gateway credentials secured
- [ ] QR code generation tested
- [ ] Payment verification implemented
- [ ] Refund workflow tested
- [ ] Reconciliation process automated
- [ ] Error handling implemented
- [ ] Logging and monitoring configured
- [ ] Webhook endpoints secured
- [ ] BOT compliance verified

---

## Tools & Libraries

| Tool | Purpose |
|------|---------|
| Omise Node.js SDK | Omise payment integration |
| qrcode | QR code generation |
| crc | CRC checksum calculation |
| crypto | Hash generation for 2C2P |

---

## Further Reading

- [Bank of Thailand Payment Systems](https://www.bot.or.th/English/PaymentSystems/Pages/default.aspx)
- [PromptPay Specification](https://www.bot.or.th/Thai/PaymentSystems/StandardPS/Documents/PromptPay_Specification.pdf)
- [Thai QR Payment Standard](https://www.bot.or.th/Thai/PaymentSystems/StandardPS/Documents/Thai_QR_Payment_Standard.pdf)
- [Omise Documentation](https://docs.opn.ooo/)
- [2C2P Documentation](https://developer.2c2p.com/)
