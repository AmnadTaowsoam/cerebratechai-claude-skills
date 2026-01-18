# QR Code Features

## Overview

QR code generation, scanning, validation, and use cases for events, payments, and guest management. This skill covers various QR code formats, security measures, dynamic QR codes, and integration with event management systems.

---

## 1. QR Code Architecture

### QR Code System Components

```markdown
# QR Code System

## Components
1. **QR Generator**: Creates QR codes
2. **QR Scanner**: Reads and validates QR codes
3. **QR Validator**: Verifies authenticity
4. **QR Analytics**: Tracks scans and usage
5. **QR Storage**: Manages QR code data

## Use Cases
- Event tickets and invitations
- Guest check-in
- Payment processing
- Vendor verification
- Table assignments
- Menu access
- Feedback collection

## QR Code Types
- **Static QR**: Fixed data, cannot be changed
- **Dynamic QR**: Redirects to URL, data can be updated
- **Encrypted QR**: Contains encrypted data
- **Signed QR**: Digitally signed for authenticity
```

---

## 2. QR Code Generation

### Basic QR Code Generation

```typescript
// QR Code Generator
import QRCode from 'qrcode'
import crypto from 'crypto'

interface QRCodeOptions {
  data: string
  size?: number
  errorCorrectionLevel?: 'L' | 'M' | 'Q' | 'H'
  color?: {
    dark?: string
    light?: string
  }
  logo?: string
}

class QRCodeGenerator {
  async generateQRCode(options: QRCodeOptions): Promise<string> {
    const qrOptions = {
      errorCorrectionLevel: options.errorCorrectionLevel || 'M',
      type: 'image/png' as const,
      quality: 0.92,
      margin: 1,
      width: options.size || 300,
      color: {
        dark: options.color?.dark || '#000000',
        light: options.color?.light || '#FFFFFF',
      },
    }

    try {
      // Generate QR code as data URL
      const qrDataUrl = await QRCode.toDataURL(options.data, qrOptions)

      // Add logo if provided
      if (options.logo) {
        return await this.addLogoToQR(qrDataUrl, options.logo)
      }

      return qrDataUrl
    } catch (error) {
      console.error('QR code generation failed:', error)
      throw error
    }
  }

  async generateQRCodeBuffer(data: string): Promise<Buffer> {
    return await QRCode.toBuffer(data, {
      errorCorrectionLevel: 'H',
      type: 'png',
      width: 500,
    })
  }

  async generateQRCodeSVG(data: string): Promise<string> {
    return await QRCode.toString(data, {
      type: 'svg',
      errorCorrectionLevel: 'M',
    })
  }

  private async addLogoToQR(qrDataUrl: string, logoUrl: string): Promise<string> {
    // Implementation to overlay logo on QR code
    // This would use canvas or image processing library
    return qrDataUrl
  }
}

// Usage Example
const generator = new QRCodeGenerator()

const qrCode = await generator.generateQRCode({
  data: 'https://malai.app/event/EVENT-001',
  size: 400,
  errorCorrectionLevel: 'H',
  color: {
    dark: '#FF6B6B',
    light: '#FFFFFF',
  },
})
```

### Event Ticket QR Code

```typescript
// Event Ticket QR Code
interface TicketData {
  ticketId: string
  eventId: string
  guestName: string
  guestEmail: string
  ticketType: string
  seatNumber?: string
  issuedAt: Date
  validUntil: Date
}

class TicketQRGenerator {
  private secretKey: string

  constructor(secretKey: string) {
    this.secretKey = secretKey
  }

  async generateTicketQR(ticket: TicketData): Promise<{
    qrCode: string
    qrData: string
  }> {
    // Create ticket payload
    const payload = {
      tid: ticket.ticketId,
      eid: ticket.eventId,
      name: ticket.guestName,
      type: ticket.ticketType,
      seat: ticket.seatNumber,
      exp: ticket.validUntil.getTime(),
    }

    // Sign payload
    const signature = this.signPayload(payload)

    // Create QR data
    const qrData = JSON.stringify({
      ...payload,
      sig: signature,
    })

    // Generate QR code
    const generator = new QRCodeGenerator()
    const qrCode = await generator.generateQRCode({
      data: qrData,
      size: 400,
      errorCorrectionLevel: 'H',
    })

    return { qrCode, qrData }
  }

  private signPayload(payload: any): string {
    const data = JSON.stringify(payload)
    return crypto
      .createHmac('sha256', this.secretKey)
      .update(data)
      .digest('hex')
  }

  verifyTicketQR(qrData: string): {
    valid: boolean
    ticket?: TicketData
    error?: string
  } {
    try {
      const data = JSON.parse(qrData)

      // Verify signature
      const { sig, ...payload } = data
      const expectedSignature = this.signPayload(payload)

      if (sig !== expectedSignature) {
        return { valid: false, error: 'Invalid signature' }
      }

      // Check expiry
      if (payload.exp < Date.now()) {
        return { valid: false, error: 'Ticket expired' }
      }

      // Reconstruct ticket data
      const ticket: TicketData = {
        ticketId: payload.tid,
        eventId: payload.eid,
        guestName: payload.name,
        guestEmail: '', // Not included in QR for privacy
        ticketType: payload.type,
        seatNumber: payload.seat,
        issuedAt: new Date(),
        validUntil: new Date(payload.exp),
      }

      return { valid: true, ticket }
    } catch (error) {
      return { valid: false, error: 'Invalid QR data' }
    }
  }
}

// Usage
const ticketGenerator = new TicketQRGenerator(process.env.QR_SECRET_KEY!)

const { qrCode, qrData } = await ticketGenerator.generateTicketQR({
  ticketId: 'TICKET-001',
  eventId: 'EVENT-001',
  guestName: 'สมชาย ใจดี',
  guestEmail: 'somchai@example.com',
  ticketType: 'VIP',
  seatNumber: 'A-15',
  issuedAt: new Date(),
  validUntil: new Date('2026-06-15T23:59:59'),
})
```

### Dynamic QR Codes

```typescript
// Dynamic QR Code System
interface DynamicQRData {
  id: string
  shortCode: string
  targetUrl: string
  metadata: Record<string, any>
  createdAt: Date
  expiresAt?: Date
  scanCount: number
  maxScans?: number
}

class DynamicQRManager {
  async createDynamicQR(
    targetUrl: string,
    metadata?: Record<string, any>,
    options?: {
      expiresAt?: Date
      maxScans?: number
    }
  ): Promise<DynamicQRData> {
    const shortCode = this.generateShortCode()

    const qrData: DynamicQRData = {
      id: this.generateId(),
      shortCode,
      targetUrl,
      metadata: metadata || {},
      createdAt: new Date(),
      expiresAt: options?.expiresAt,
      scanCount: 0,
      maxScans: options?.maxScans,
    }

    // Save to database
    await this.saveQRData(qrData)

    return qrData
  }

  async generateDynamicQRCode(qrData: DynamicQRData): Promise<string> {
    const redirectUrl = `${process.env.APP_URL}/qr/${qrData.shortCode}`

    const generator = new QRCodeGenerator()
    return await generator.generateQRCode({
      data: redirectUrl,
      size: 400,
      errorCorrectionLevel: 'M',
    })
  }

  async handleQRScan(shortCode: string): Promise<{
    valid: boolean
    targetUrl?: string
    error?: string
  }> {
    const qrData = await this.getQRData(shortCode)

    if (!qrData) {
      return { valid: false, error: 'QR code not found' }
    }

    // Check expiry
    if (qrData.expiresAt && qrData.expiresAt < new Date()) {
      return { valid: false, error: 'QR code expired' }
    }

    // Check max scans
    if (qrData.maxScans && qrData.scanCount >= qrData.maxScans) {
      return { valid: false, error: 'QR code scan limit reached' }
    }

    // Increment scan count
    qrData.scanCount++
    await this.updateQRData(qrData)

    // Log scan
    await this.logScan(qrData)

    return { valid: true, targetUrl: qrData.targetUrl }
  }

  async updateTargetUrl(shortCode: string, newTargetUrl: string): Promise<void> {
    const qrData = await this.getQRData(shortCode)

    if (!qrData) {
      throw new Error('QR code not found')
    }

    qrData.targetUrl = newTargetUrl
    await this.updateQRData(qrData)
  }

  private generateShortCode(): string {
    return crypto.randomBytes(4).toString('hex').toUpperCase()
  }

  private generateId(): string {
    return `QR-${Date.now()}`
  }

  private async saveQRData(qrData: DynamicQRData): Promise<void> {
    // Save to database
  }

  private async getQRData(shortCode: string): Promise<DynamicQRData | null> {
    // Fetch from database
    return null
  }

  private async updateQRData(qrData: DynamicQRData): Promise<void> {
    // Update in database
  }

  private async logScan(qrData: DynamicQRData): Promise<void> {
    // Log scan analytics
  }
}
```

---

## 3. QR Code Scanning

### QR Scanner Component

```typescript
// QR Scanner React Component
'use client'

import { useEffect, useRef, useState } from 'react'
import jsQR from 'jsqr'

interface QRScannerProps {
  onScan: (data: string) => void
  onError?: (error: string) => void
}

export default function QRScanner({ onScan, onError }: QRScannerProps) {
  const videoRef = useRef<HTMLVideoElement>(null)
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const [scanning, setScanning] = useState(false)
  const [error, setError] = useState<string>('')

  useEffect(() => {
    startScanning()

    return () => {
      stopScanning()
    }
  }, [])

  async function startScanning() {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: 'environment' },
      })

      if (videoRef.current) {
        videoRef.current.srcObject = stream
        videoRef.current.play()
        setScanning(true)
        requestAnimationFrame(scan)
      }
    } catch (err) {
      const errorMsg = 'ไม่สามารถเข้าถึงกล้องได้'
      setError(errorMsg)
      onError?.(errorMsg)
    }
  }

  function stopScanning() {
    if (videoRef.current?.srcObject) {
      const stream = videoRef.current.srcObject as MediaStream
      stream.getTracks().forEach((track) => track.stop())
    }
    setScanning(false)
  }

  function scan() {
    if (!scanning || !videoRef.current || !canvasRef.current) {
      return
    }

    const video = videoRef.current
    const canvas = canvasRef.current
    const context = canvas.getContext('2d')

    if (!context) return

    if (video.readyState === video.HAVE_ENOUGH_DATA) {
      canvas.width = video.videoWidth
      canvas.height = video.videoHeight

      context.drawImage(video, 0, 0, canvas.width, canvas.height)

      const imageData = context.getImageData(0, 0, canvas.width, canvas.height)
      const code = jsQR(imageData.data, imageData.width, imageData.height)

      if (code) {
        onScan(code.data)
        stopScanning()
        return
      }
    }

    requestAnimationFrame(scan)
  }

  return (
    <div className="qr-scanner">
      {error && <div className="error">{error}</div>}

      <video
        ref={videoRef}
        style={{
          width: '100%',
          maxWidth: '500px',
          border: '2px solid #FF6B6B',
          borderRadius: '8px',
        }}
      />

      <canvas ref={canvasRef} style={{ display: 'none' }} />

      {scanning && (
        <div className="scanning-overlay">
          <div className="scan-line" />
          <p>กำลังสแกน QR Code...</p>
        </div>
      )}
    </div>
  )
}
```

### QR Scanner with Validation

```typescript
// QR Scanner with Ticket Validation
'use client'

import { useState } from 'react'
import QRScanner from './QRScanner'

interface ValidationResult {
  valid: boolean
  ticket?: any
  error?: string
}

export default function TicketScanner() {
  const [result, setResult] = useState<ValidationResult | null>(null)
  const [loading, setLoading] = useState(false)

  async function handleScan(qrData: string) {
    setLoading(true)

    try {
      // Validate ticket
      const response = await fetch('/api/tickets/validate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ qrData }),
      })

      const result: ValidationResult = await response.json()
      setResult(result)

      // Play sound based on result
      if (result.valid) {
        playSuccessSound()
      } else {
        playErrorSound()
      }
    } catch (error) {
      setResult({
        valid: false,
        error: 'เกิดข้อผิดพลาดในการตรวจสอบ',
      })
      playErrorSound()
    } finally {
      setLoading(false)
    }
  }

  function playSuccessSound() {
    const audio = new Audio('/sounds/success.mp3')
    audio.play()
  }

  function playErrorSound() {
    const audio = new Audio('/sounds/error.mp3')
    audio.play()
  }

  function resetScanner() {
    setResult(null)
  }

  if (result) {
    return (
      <div className="validation-result">
        {result.valid ? (
          <div className="success">
            <h2>✅ ตั๋วถูกต้อง</h2>
            <p>ชื่อ: {result.ticket?.guestName}</p>
            <p>ประเภท: {result.ticket?.ticketType}</p>
            {result.ticket?.seatNumber && (
              <p>ที่นั่ง: {result.ticket.seatNumber}</p>
            )}
          </div>
        ) : (
          <div className="error">
            <h2>❌ ตั๋วไม่ถูกต้อง</h2>
            <p>{result.error}</p>
          </div>
        )}

        <button onClick={resetScanner}>สแกนต่อ</button>
      </div>
    )
  }

  return (
    <div className="ticket-scanner">
      <h1>สแกนตั๋ว</h1>
      {loading ? (
        <div>กำลังตรวจสอบ...</div>
      ) : (
        <QRScanner onScan={handleScan} />
      )}
    </div>
  )
}
```

---

## 4. Guest Check-in System

### Check-in QR Code

```typescript
// Guest Check-in System
interface GuestCheckIn {
  id: string
  eventId: string
  guestId: string
  guestName: string
  ticketId: string
  checkInTime: Date
  checkInLocation?: string
  checkInBy?: string
}

class CheckInManager {
  async checkInGuest(
    qrData: string,
    checkInBy?: string,
    location?: string
  ): Promise<{
    success: boolean
    checkIn?: GuestCheckIn
    error?: string
  }> {
    // Validate QR code
    const ticketGenerator = new TicketQRGenerator(process.env.QR_SECRET_KEY!)
    const validation = ticketGenerator.verifyTicketQR(qrData)

    if (!validation.valid || !validation.ticket) {
      return { success: false, error: validation.error }
    }

    const ticket = validation.ticket

    // Check if already checked in
    const existingCheckIn = await this.getCheckIn(ticket.ticketId)

    if (existingCheckIn) {
      return {
        success: false,
        error: 'แขกเช็คอินแล้ว',
      }
    }

    // Create check-in record
    const checkIn: GuestCheckIn = {
      id: this.generateCheckInId(),
      eventId: ticket.eventId,
      guestId: ticket.ticketId,
      guestName: ticket.guestName,
      ticketId: ticket.ticketId,
      checkInTime: new Date(),
      checkInLocation: location,
      checkInBy: checkInBy,
    }

    // Save check-in
    await this.saveCheckIn(checkIn)

    // Send notification
    await this.notifyCheckIn(checkIn)

    return { success: true, checkIn }
  }

  async getCheckInStats(eventId: string): Promise<{
    totalGuests: number
    checkedIn: number
    notCheckedIn: number
    checkInRate: number
  }> {
    const totalGuests = await this.getTotalGuests(eventId)
    const checkedIn = await this.getCheckedInCount(eventId)
    const notCheckedIn = totalGuests - checkedIn
    const checkInRate = totalGuests > 0 ? (checkedIn / totalGuests) * 100 : 0

    return {
      totalGuests,
      checkedIn,
      notCheckedIn,
      checkInRate,
    }
  }

  async getCheckInHistory(eventId: string): Promise<GuestCheckIn[]> {
    // Fetch check-in history from database
    return []
  }

  private generateCheckInId(): string {
    return `CHECKIN-${Date.now()}`
  }

  private async getCheckIn(ticketId: string): Promise<GuestCheckIn | null> {
    // Fetch from database
    return null
  }

  private async saveCheckIn(checkIn: GuestCheckIn): Promise<void> {
    // Save to database
  }

  private async getTotalGuests(eventId: string): Promise<number> {
    // Count total guests from database
    return 0
  }

  private async getCheckedInCount(eventId: string): Promise<number> {
    // Count checked-in guests from database
    return 0
  }

  private async notifyCheckIn(checkIn: GuestCheckIn): Promise<void> {
    // Send notification to event organizer
  }
}
```

### Check-in Dashboard

```typescript
// Real-time Check-in Dashboard
'use client'

import { useEffect, useState } from 'react'

interface CheckInStats {
  totalGuests: number
  checkedIn: number
  notCheckedIn: number
  checkInRate: number
}

export default function CheckInDashboard({ eventId }: { eventId: string }) {
  const [stats, setStats] = useState<CheckInStats | null>(null)
  const [recentCheckIns, setRecentCheckIns] = useState<GuestCheckIn[]>([])

  useEffect(() => {
    fetchStats()

    // Poll for updates every 5 seconds
    const interval = setInterval(fetchStats, 5000)

    return () => clearInterval(interval)
  }, [eventId])

  async function fetchStats() {
    try {
      const response = await fetch(`/api/events/${eventId}/checkin/stats`)
      const data = await response.json()
      setStats(data.stats)
      setRecentCheckIns(data.recentCheckIns)
    } catch (error) {
      console.error('Failed to fetch stats:', error)
    }
  }

  if (!stats) {
    return <div>กำลังโหลด...</div>
  }

  return (
    <div className="checkin-dashboard">
      <h1>สถานะการเช็คอิน</h1>

      <div className="stats-grid">
        <div className="stat-card">
          <h3>แขกทั้งหมด</h3>
          <p className="stat-value">{stats.totalGuests}</p>
        </div>

        <div className="stat-card success">
          <h3>เช็คอินแล้ว</h3>
          <p className="stat-value">{stats.checkedIn}</p>
        </div>

        <div className="stat-card warning">
          <h3>ยังไม่เช็คอิน</h3>
          <p className="stat-value">{stats.notCheckedIn}</p>
        </div>

        <div className="stat-card info">
          <h3>อัตราเช็คอิน</h3>
          <p className="stat-value">{stats.checkInRate.toFixed(1)}%</p>
        </div>
      </div>

      <div className="recent-checkins">
        <h2>เช็คอินล่าสุด</h2>
        <div className="checkin-list">
          {recentCheckIns.map((checkIn) => (
            <div key={checkIn.id} className="checkin-item">
              <div className="guest-name">{checkIn.guestName}</div>
              <div className="checkin-time">
                {new Date(checkIn.checkInTime).toLocaleTimeString('th-TH')}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
```

---

## 5. Payment QR Codes

### Payment QR Integration

```typescript
// Payment QR Code (PromptPay)
import { PromptPayQR } from '../thai-payment-integration'

class PaymentQRManager {
  async generatePaymentQR(
    amount: number,
    reference: string,
    phoneNumber: string
  ): Promise<{
    qrCode: string
    qrData: string
    expiresAt: Date
  }> {
    // Generate PromptPay QR
    const qrData = PromptPayQR.generateQR({
      phoneNumber,
      amount,
      reference,
    })

    // Generate QR code image
    const generator = new QRCodeGenerator()
    const qrCode = await generator.generateQRCode({
      data: qrData,
      size: 400,
      errorCorrectionLevel: 'M',
    })

    // Set expiry (15 minutes)
    const expiresAt = new Date()
    expiresAt.setMinutes(expiresAt.getMinutes() + 15)

    // Save payment QR
    await this.savePaymentQR({
      qrData,
      reference,
      amount,
      expiresAt,
    })

    return { qrCode, qrData, expiresAt }
  }

  async verifyPayment(reference: string): Promise<{
    paid: boolean
    amount?: number
    paidAt?: Date
  }> {
    // Check payment status from payment gateway
    // Implementation depends on payment gateway
    return { paid: false }
  }

  private async savePaymentQR(data: any): Promise<void> {
    // Save to database
  }
}
```

---

## 6. QR Code Security

### Encrypted QR Codes

```typescript
// Encrypted QR Code
import crypto from 'crypto'

class EncryptedQRGenerator {
  private algorithm = 'aes-256-gcm'
  private key: Buffer

  constructor(secretKey: string) {
    this.key = crypto.scryptSync(secretKey, 'salt', 32)
  }

  encrypt(data: string): {
    encrypted: string
    iv: string
    authTag: string
  } {
    const iv = crypto.randomBytes(16)
    const cipher = crypto.createCipheriv(this.algorithm, this.key, iv)

    let encrypted = cipher.update(data, 'utf8', 'hex')
    encrypted += cipher.final('hex')

    const authTag = cipher.getAuthTag().toString('hex')

    return {
      encrypted,
      iv: iv.toString('hex'),
      authTag,
    }
  }

  decrypt(
    encrypted: string,
    iv: string,
    authTag: string
  ): string {
    const decipher = crypto.createDecipheriv(
      this.algorithm,
      this.key,
      Buffer.from(iv, 'hex')
    )

    decipher.setAuthTag(Buffer.from(authTag, 'hex'))

    let decrypted = decipher.update(encrypted, 'hex', 'utf8')
    decrypted += decipher.final('utf8')

    return decrypted
  }

  async generateEncryptedQR(data: any): Promise<string> {
    const jsonData = JSON.stringify(data)
    const { encrypted, iv, authTag } = this.encrypt(jsonData)

    const qrPayload = JSON.stringify({ encrypted, iv, authTag })

    const generator = new QRCodeGenerator()
    return await generator.generateQRCode({
      data: qrPayload,
      size: 400,
      errorCorrectionLevel: 'H',
    })
  }

  verifyEncryptedQR(qrData: string): {
    valid: boolean
    data?: any
    error?: string
  } {
    try {
      const { encrypted, iv, authTag } = JSON.parse(qrData)
      const decrypted = this.decrypt(encrypted, iv, authTag)
      const data = JSON.parse(decrypted)

      return { valid: true, data }
    } catch (error) {
      return { valid: false, error: 'Invalid or corrupted QR code' }
    }
  }
}
```

---

## Best Practices

1. **Security**
   - Sign QR codes with HMAC
   - Encrypt sensitive data
   - Set expiry times
   - Implement rate limiting
   - Validate all scanned data

2. **User Experience**
   - Use high error correction level
   - Ensure adequate size (minimum 300x300px)
   - Test on different devices
   - Provide fallback options
   - Clear instructions

3. **Performance**
   - Cache generated QR codes
   - Optimize image size
   - Use CDN for QR images
   - Implement lazy loading

4. **Reliability**
   - Handle camera permissions
   - Provide manual entry option
   - Test in various lighting conditions
   - Support multiple QR formats

5. **Analytics**
   - Track scan locations
   - Monitor scan times
   - Analyze usage patterns
   - Detect fraud attempts

---

## Common Pitfalls

1. **QR Code Size**: Too small QR codes are hard to scan
2. **Error Correction**: Low error correction fails with damaged codes
3. **Expiry**: Not implementing expiry can lead to security issues
4. **Validation**: Not validating scanned data properly
5. **Camera Access**: Not handling camera permission denials

---

## Production Checklist

- [ ] QR generation tested
- [ ] QR scanning implemented
- [ ] Validation logic verified
- [ ] Security measures in place
- [ ] Error handling comprehensive
- [ ] Analytics configured
- [ ] Performance optimized
- [ ] Mobile devices tested
- [ ] Offline support considered
- [ ] Documentation complete

---

## Tools & Libraries

| Tool | Purpose |
|------|---------|
| qrcode | QR code generation |
| jsQR | QR code scanning |
| crypto | Encryption and signing |
| canvas | Image manipulation |

---

## Further Reading

- [QR Code Specification](https://www.qrcode.com/en/about/standards.html)
- [Error Correction Levels](https://www.qrcode.com/en/about/error_correction.html)
- [Best Practices for QR Codes](https://www.denso-wave.com/en/technology/vol1.html)
- [PromptPay QR Standard](https://www.bot.or.th/Thai/PaymentSystems/StandardPS/Documents/PromptPay_Specification.pdf)
