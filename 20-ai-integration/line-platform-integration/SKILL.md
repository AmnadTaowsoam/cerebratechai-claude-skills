# LINE Platform Integration

## Overview

Complete integration with LINE ecosystem including LINE Official Account (OA), LIFF (LINE Front-end Framework), Messaging API, LINE Login, and LINE Pay. This skill covers building chatbots, rich menus, flex messages, and seamless user experiences within the LINE platform.

---

## 1. LINE Platform Architecture

### LINE Ecosystem Components

```markdown
# LINE Platform Components

## Core Services
1. **LINE Official Account (OA)**: Business account for messaging
2. **LIFF**: Web apps that run inside LINE
3. **Messaging API**: Send/receive messages programmatically
4. **LINE Login**: OAuth 2.0 authentication
5. **LINE Pay**: Payment integration
6. **LINE Beacon**: Proximity-based messaging
7. **LINE Things**: IoT device integration

## Integration Flow
```
User → LINE App → LIFF/Messaging API → Your Backend → Database
                      ↓
                  Webhook ← LINE Platform
                      ↓
                  Your Backend → Process → Response
```

## Use Cases
- Customer support chatbots
- E-commerce in LINE
- Event registration
- Appointment booking
- Loyalty programs
- Payment processing
```

---

## 2. LINE Official Account Setup

### Creating LINE OA

```markdown
# LINE Official Account Setup

## Steps
1. Go to [LINE Official Account Manager](https://manager.line.biz/)
2. Create new account
3. Choose account type:
   - **Unverified Account**: Free, limited features
   - **Verified Account**: Paid, full features, blue badge
4. Configure account settings:
   - Profile name
   - Profile image
   - Status message
   - Background image

## Channel Settings
1. Go to [LINE Developers Console](https://developers.line.biz/)
2. Create new provider
3. Create Messaging API channel
4. Get credentials:
   - Channel ID
   - Channel Secret
   - Channel Access Token

## Webhook Configuration
1. Enable webhook
2. Set webhook URL: `https://your-domain.com/webhook/line`
3. Verify webhook
4. Enable auto-reply (optional)
```

### Environment Configuration

```typescript
// .env
LINE_CHANNEL_ID=your_channel_id
LINE_CHANNEL_SECRET=your_channel_secret
LINE_CHANNEL_ACCESS_TOKEN=your_access_token
LINE_LIFF_ID=your_liff_id
```

---

## 3. Messaging API Integration

### LINE Bot SDK Setup

```typescript
// LINE Bot SDK Configuration
import { Client, ClientConfig, middleware, WebhookEvent } from '@line/bot-sdk'
import express from 'express'

const config: ClientConfig = {
  channelAccessToken: process.env.LINE_CHANNEL_ACCESS_TOKEN!,
  channelSecret: process.env.LINE_CHANNEL_SECRET!,
}

const client = new Client(config)
const app = express()

// Webhook endpoint
app.post('/webhook/line', middleware(config), async (req, res) => {
  const events: WebhookEvent[] = req.body.events

  // Process all events
  await Promise.all(
    events.map(async (event) => {
      try {
        await handleEvent(event)
      } catch (error) {
        console.error('Error handling event:', error)
      }
    })
  )

  res.status(200).send('OK')
})

async function handleEvent(event: WebhookEvent): Promise<void> {
  if (event.type === 'message') {
    await handleMessage(event)
  } else if (event.type === 'follow') {
    await handleFollow(event)
  } else if (event.type === 'unfollow') {
    await handleUnfollow(event)
  } else if (event.type === 'postback') {
    await handlePostback(event)
  }
}

app.listen(3000, () => {
  console.log('LINE Bot server running on port 3000')
})
```

### Message Handling

```typescript
// Message Event Handler
import { MessageEvent, TextMessage } from '@line/bot-sdk'

async function handleMessage(event: MessageEvent): Promise<void> {
  if (event.message.type !== 'text') {
    return
  }

  const userId = event.source.userId
  const messageText = event.message.text

  // Get user profile
  const profile = await client.getProfile(userId!)

  console.log(`Message from ${profile.displayName}: ${messageText}`)

  // Process message
  let replyText = ''

  if (messageText.toLowerCase().includes('hello')) {
    replyText = `สวัสดีครับคุณ ${profile.displayName}! 👋`
  } else if (messageText.toLowerCase().includes('help')) {
    replyText = 'ฉันสามารถช่วยคุณได้ดังนี้:\n1. ดูข้อมูลอีเวนต์\n2. จองตั๋ว\n3. ติดต่อเรา'
  } else {
    replyText = 'ขอบคุณสำหรับข้อความครับ!'
  }

  // Reply to user
  await client.replyMessage(event.replyToken, {
    type: 'text',
    text: replyText,
  })
}
```

### Follow/Unfollow Events

```typescript
// Follow Event Handler
import { FollowEvent, UnfollowEvent } from '@line/bot-sdk'

async function handleFollow(event: FollowEvent): Promise<void> {
  const userId = event.source.userId!
  const profile = await client.getProfile(userId)

  console.log(`New follower: ${profile.displayName}`)

  // Save user to database
  await saveUser({
    lineUserId: userId,
    displayName: profile.displayName,
    pictureUrl: profile.pictureUrl,
    statusMessage: profile.statusMessage,
  })

  // Send welcome message
  await client.replyMessage(event.replyToken, {
    type: 'text',
    text: `ยินดีต้อนรับครับคุณ ${profile.displayName}! 🎉\n\nขอบคุณที่เพิ่มเราเป็นเพื่อน`,
  })
}

async function handleUnfollow(event: UnfollowEvent): Promise<void> {
  const userId = event.source.userId!

  console.log(`User unfollowed: ${userId}`)

  // Update user status in database
  await updateUserStatus(userId, 'unfollowed')
}

async function saveUser(user: any): Promise<void> {
  // Save to database
}

async function updateUserStatus(userId: string, status: string): Promise<void> {
  // Update in database
}
```

---

## 4. Rich Messages

### Flex Messages

```typescript
// Flex Message - Event Card
import { FlexMessage } from '@line/bot-sdk'

function createEventCard(event: {
  title: string
  date: string
  location: string
  price: number
  imageUrl: string
  eventId: string
}): FlexMessage {
  return {
    type: 'flex',
    altText: event.title,
    contents: {
      type: 'bubble',
      hero: {
        type: 'image',
        url: event.imageUrl,
        size: 'full',
        aspectRatio: '20:13',
        aspectMode: 'cover',
      },
      body: {
        type: 'box',
        layout: 'vertical',
        contents: [
          {
            type: 'text',
            text: event.title,
            weight: 'bold',
            size: 'xl',
            wrap: true,
          },
          {
            type: 'box',
            layout: 'vertical',
            margin: 'lg',
            spacing: 'sm',
            contents: [
              {
                type: 'box',
                layout: 'baseline',
                spacing: 'sm',
                contents: [
                  {
                    type: 'text',
                    text: '📅',
                    size: 'sm',
                    flex: 0,
                  },
                  {
                    type: 'text',
                    text: event.date,
                    size: 'sm',
                    color: '#666666',
                    flex: 5,
                  },
                ],
              },
              {
                type: 'box',
                layout: 'baseline',
                spacing: 'sm',
                contents: [
                  {
                    type: 'text',
                    text: '📍',
                    size: 'sm',
                    flex: 0,
                  },
                  {
                    type: 'text',
                    text: event.location,
                    size: 'sm',
                    color: '#666666',
                    flex: 5,
                    wrap: true,
                  },
                ],
              },
              {
                type: 'box',
                layout: 'baseline',
                spacing: 'sm',
                contents: [
                  {
                    type: 'text',
                    text: '💰',
                    size: 'sm',
                    flex: 0,
                  },
                  {
                    type: 'text',
                    text: `${event.price.toLocaleString('th-TH')} บาท`,
                    size: 'sm',
                    color: '#666666',
                    flex: 5,
                  },
                ],
              },
            ],
          },
        ],
      },
      footer: {
        type: 'box',
        layout: 'vertical',
        spacing: 'sm',
        contents: [
          {
            type: 'button',
            style: 'primary',
            action: {
              type: 'uri',
              label: 'ดูรายละเอียด',
              uri: `https://liff.line.me/${process.env.LINE_LIFF_ID}/events/${event.eventId}`,
            },
          },
          {
            type: 'button',
            style: 'secondary',
            action: {
              type: 'postback',
              label: 'จองเลย',
              data: `action=book&eventId=${event.eventId}`,
            },
          },
        ],
      },
    },
  }
}

// Usage
const eventCard = createEventCard({
  title: 'งานแต่งงานริมทะเล',
  date: '15 มีนาคม 2026',
  location: 'โรงแรมหรู ภูเก็ต',
  price: 50000,
  imageUrl: 'https://example.com/event.jpg',
  eventId: 'EVENT-001',
})

await client.pushMessage(userId, eventCard)
```

### Carousel Messages

```typescript
// Flex Message - Event Carousel
import { FlexMessage } from '@line/bot-sdk'

function createEventCarousel(events: any[]): FlexMessage {
  return {
    type: 'flex',
    altText: 'รายการอีเวนต์',
    contents: {
      type: 'carousel',
      contents: events.map((event) => ({
        type: 'bubble',
        hero: {
          type: 'image',
          url: event.imageUrl,
          size: 'full',
          aspectRatio: '20:13',
          aspectMode: 'cover',
        },
        body: {
          type: 'box',
          layout: 'vertical',
          contents: [
            {
              type: 'text',
              text: event.title,
              weight: 'bold',
              size: 'lg',
              wrap: true,
            },
            {
              type: 'text',
              text: `${event.price.toLocaleString('th-TH')} บาท`,
              size: 'md',
              color: '#FF6B6B',
              margin: 'md',
            },
          ],
        },
        footer: {
          type: 'box',
          layout: 'vertical',
          contents: [
            {
              type: 'button',
              action: {
                type: 'uri',
                label: 'ดูเพิ่มเติม',
                uri: `https://liff.line.me/${process.env.LINE_LIFF_ID}/events/${event.id}`,
              },
            },
          ],
        },
      })),
    },
  }
}
```

### Quick Reply

```typescript
// Quick Reply Buttons
import { TextMessage } from '@line/bot-sdk'

const messageWithQuickReply: TextMessage = {
  type: 'text',
  text: 'คุณสนใจอีเวนต์ประเภทไหนครับ?',
  quickReply: {
    items: [
      {
        type: 'action',
        action: {
          type: 'message',
          label: 'งานแต่งงาน',
          text: 'แสดงงานแต่งงาน',
        },
      },
      {
        type: 'action',
        action: {
          type: 'message',
          label: 'งานเลี้ยง',
          text: 'แสดงงานเลี้ยง',
        },
      },
      {
        type: 'action',
        action: {
          type: 'message',
          label: 'งานบุญ',
          text: 'แสดงงานบุญ',
        },
      },
      {
        type: 'action',
        action: {
          type: 'postback',
          label: 'ดูทั้งหมด',
          data: 'action=view_all_events',
          displayText: 'ดูอีเวนต์ทั้งหมด',
        },
      },
    ],
  },
}

await client.pushMessage(userId, messageWithQuickReply)
```

---

## 5. Rich Menu

### Creating Rich Menu

```typescript
// Rich Menu Configuration
import { RichMenu, RichMenuSize, RichMenuArea } from '@line/bot-sdk'

async function createRichMenu(): Promise<string> {
  const richMenu: RichMenu = {
    size: {
      width: 2500,
      height: 1686,
    },
    selected: true,
    name: 'Malai Platform Menu',
    chatBarText: 'เมนู',
    areas: [
      {
        bounds: {
          x: 0,
          y: 0,
          width: 833,
          height: 843,
        },
        action: {
          type: 'uri',
          label: 'ค้นหาอีเวนต์',
          uri: `https://liff.line.me/${process.env.LINE_LIFF_ID}/search`,
        },
      },
      {
        bounds: {
          x: 833,
          y: 0,
          width: 834,
          height: 843,
        },
        action: {
          type: 'uri',
          label: 'อีเวนต์ของฉัน',
          uri: `https://liff.line.me/${process.env.LINE_LIFF_ID}/my-events`,
        },
      },
      {
        bounds: {
          x: 1667,
          y: 0,
          width: 833,
          height: 843,
        },
        action: {
          type: 'uri',
          label: 'โปรไฟล์',
          uri: `https://liff.line.me/${process.env.LINE_LIFF_ID}/profile`,
        },
      },
      {
        bounds: {
          x: 0,
          y: 843,
          width: 1250,
          height: 843,
        },
        action: {
          type: 'postback',
          label: 'สร้างอีเวนต์',
          data: 'action=create_event',
          displayText: 'สร้างอีเวนต์ใหม่',
        },
      },
      {
        bounds: {
          x: 1250,
          y: 843,
          width: 1250,
          height: 843,
        },
        action: {
          type: 'message',
          label: 'ติดต่อเรา',
          text: 'ติดต่อเรา',
        },
      },
    ],
  }

  // Create rich menu
  const richMenuId = await client.createRichMenu(richMenu)

  // Upload rich menu image
  const imagePath = './assets/richmenu.png'
  await client.setRichMenuImage(richMenuId, fs.createReadStream(imagePath))

  // Set as default rich menu
  await client.setDefaultRichMenu(richMenuId)

  return richMenuId
}
```

### Rich Menu Management

```typescript
// Rich Menu Manager
class RichMenuManager {
  async createUserRichMenu(userId: string, menuType: string): Promise<void> {
    let richMenuId: string

    if (menuType === 'organizer') {
      richMenuId = await this.createOrganizerMenu()
    } else {
      richMenuId = await this.createGuestMenu()
    }

    // Link rich menu to user
    await client.linkRichMenuToUser(userId, richMenuId)
  }

  async createOrganizerMenu(): Promise<string> {
    // Create rich menu for event organizers
    const richMenu: RichMenu = {
      size: { width: 2500, height: 1686 },
      selected: true,
      name: 'Organizer Menu',
      chatBarText: 'เมนูผู้จัดงาน',
      areas: [
        // Define areas for organizer-specific actions
      ],
    }

    return await client.createRichMenu(richMenu)
  }

  async createGuestMenu(): Promise<string> {
    // Create rich menu for guests
    const richMenu: RichMenu = {
      size: { width: 2500, height: 1686 },
      selected: true,
      name: 'Guest Menu',
      chatBarText: 'เมนูแขก',
      areas: [
        // Define areas for guest-specific actions
      ],
    }

    return await client.createRichMenu(richMenu)
  }

  async unlinkRichMenu(userId: string): Promise<void> {
    await client.unlinkRichMenuFromUser(userId)
  }
}
```

---

## 6. LIFF (LINE Front-end Framework)

### LIFF Setup

```typescript
// LIFF Configuration
import liff from '@line/liff'

// Initialize LIFF
async function initializeLIFF(): Promise<void> {
  try {
    await liff.init({ liffId: process.env.NEXT_PUBLIC_LIFF_ID! })

    if (!liff.isLoggedIn()) {
      liff.login()
    }
  } catch (error) {
    console.error('LIFF initialization failed:', error)
  }
}

// Get user profile
async function getUserProfile() {
  if (liff.isLoggedIn()) {
    const profile = await liff.getProfile()
    return {
      userId: profile.userId,
      displayName: profile.displayName,
      pictureUrl: profile.pictureUrl,
      statusMessage: profile.statusMessage,
    }
  }
  return null
}

// Send message to chat
function sendMessageToChat(message: string): void {
  if (liff.isInClient()) {
    liff.sendMessages([
      {
        type: 'text',
        text: message,
      },
    ])
  }
}

// Close LIFF window
function closeLIFF(): void {
  liff.closeWindow()
}
```

### LIFF React Component

```typescript
// LIFF Event Booking Component
'use client'

import { useEffect, useState } from 'react'
import liff from '@line/liff'

interface Event {
  id: string
  title: string
  date: string
  price: number
}

export default function EventBooking() {
  const [profile, setProfile] = useState<any>(null)
  const [event, setEvent] = useState<Event | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    initLIFF()
  }, [])

  async function initLIFF() {
    try {
      await liff.init({ liffId: process.env.NEXT_PUBLIC_LIFF_ID! })

      if (!liff.isLoggedIn()) {
        liff.login()
        return
      }

      // Get user profile
      const userProfile = await liff.getProfile()
      setProfile(userProfile)

      // Get event ID from URL
      const params = new URLSearchParams(window.location.search)
      const eventId = params.get('eventId')

      if (eventId) {
        // Fetch event details
        const eventData = await fetchEvent(eventId)
        setEvent(eventData)
      }

      setLoading(false)
    } catch (error) {
      console.error('LIFF init failed:', error)
      setLoading(false)
    }
  }

  async function fetchEvent(eventId: string): Promise<Event> {
    const response = await fetch(`/api/events/${eventId}`)
    return await response.json()
  }

  async function handleBooking() {
    if (!event || !profile) return

    try {
      // Create booking
      const response = await fetch('/api/bookings', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          eventId: event.id,
          userId: profile.userId,
        }),
      })

      const booking = await response.json()

      // Send confirmation message to chat
      if (liff.isInClient()) {
        await liff.sendMessages([
          {
            type: 'text',
            text: `✅ จองสำเร็จ!\n\nอีเวนต์: ${event.title}\nรหัสการจอง: ${booking.id}`,
          },
        ])

        // Close LIFF window
        liff.closeWindow()
      }
    } catch (error) {
      console.error('Booking failed:', error)
      alert('เกิดข้อผิดพลาดในการจอง กรุณาลองใหม่อีกครั้ง')
    }
  }

  if (loading) {
    return <div>กำลังโหลด...</div>
  }

  if (!event) {
    return <div>ไม่พบข้อมูลอีเวนต์</div>
  }

  return (
    <div className="container">
      <h1>{event.title}</h1>
      <p>วันที่: {event.date}</p>
      <p>ราคา: {event.price.toLocaleString('th-TH')} บาท</p>

      {profile && (
        <div className="profile">
          <img src={profile.pictureUrl} alt={profile.displayName} />
          <p>ผู้จอง: {profile.displayName}</p>
        </div>
      )}

      <button onClick={handleBooking}>ยืนยันการจอง</button>
    </div>
  )
}
```

---

## 7. LINE Login

### LINE Login Integration

```typescript
// LINE Login with Next.js
import { NextApiRequest, NextApiResponse } from 'next'
import axios from 'axios'

// Login endpoint
export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method === 'GET') {
    // Redirect to LINE login
    const state = generateRandomState()
    const nonce = generateRandomNonce()

    // Save state and nonce to session
    req.session.state = state
    req.session.nonce = nonce

    const authUrl = `https://access.line.me/oauth2/v2.1/authorize?` +
      `response_type=code&` +
      `client_id=${process.env.LINE_CHANNEL_ID}&` +
      `redirect_uri=${encodeURIComponent(process.env.LINE_REDIRECT_URI!)}&` +
      `state=${state}&` +
      `scope=profile%20openid%20email&` +
      `nonce=${nonce}`

    res.redirect(authUrl)
  }
}

// Callback endpoint
export async function callbackHandler(req: NextApiRequest, res: NextApiResponse) {
  const { code, state } = req.query

  // Verify state
  if (state !== req.session.state) {
    return res.status(400).json({ error: 'Invalid state' })
  }

  try {
    // Exchange code for access token
    const tokenResponse = await axios.post(
      'https://api.line.me/oauth2/v2.1/token',
      new URLSearchParams({
        grant_type: 'authorization_code',
        code: code as string,
        redirect_uri: process.env.LINE_REDIRECT_URI!,
        client_id: process.env.LINE_CHANNEL_ID!,
        client_secret: process.env.LINE_CHANNEL_SECRET!,
      }),
      {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
      }
    )

    const { access_token, id_token } = tokenResponse.data

    // Get user profile
    const profileResponse = await axios.get('https://api.line.me/v2/profile', {
      headers: {
        Authorization: `Bearer ${access_token}`,
      },
    })

    const profile = profileResponse.data

    // Save user to database
    await saveUser({
      lineUserId: profile.userId,
      displayName: profile.displayName,
      pictureUrl: profile.pictureUrl,
      email: profile.email,
    })

    // Create session
    req.session.user = profile

    res.redirect('/dashboard')
  } catch (error) {
    console.error('LINE login failed:', error)
    res.status(500).json({ error: 'Login failed' })
  }
}

function generateRandomState(): string {
  return Math.random().toString(36).substring(7)
}

function generateRandomNonce(): string {
  return Math.random().toString(36).substring(7)
}

async function saveUser(user: any): Promise<void> {
  // Save to database
}
```

---

## 8. Postback Handling

### Postback Event Handler

```typescript
// Postback Event Handler
import { PostbackEvent } from '@line/bot-sdk'

async function handlePostback(event: PostbackEvent): Promise<void> {
  const userId = event.source.userId!
  const data = parsePostbackData(event.postback.data)

  console.log('Postback data:', data)

  if (data.action === 'book') {
    await handleBookingPostback(userId, data.eventId, event.replyToken)
  } else if (data.action === 'create_event') {
    await handleCreateEventPostback(userId, event.replyToken)
  } else if (data.action === 'view_all_events') {
    await handleViewAllEventsPostback(userId, event.replyToken)
  }
}

function parsePostbackData(data: string): Record<string, string> {
  const params = new URLSearchParams(data)
  const result: Record<string, string> = {}

  params.forEach((value, key) => {
    result[key] = value
  })

  return result
}

async function handleBookingPostback(
  userId: string,
  eventId: string,
  replyToken: string
): Promise<void> {
  // Open LIFF for booking
  const liffUrl = `https://liff.line.me/${process.env.LINE_LIFF_ID}/booking?eventId=${eventId}`

  await client.replyMessage(replyToken, {
    type: 'text',
    text: 'กรุณากดปุ่มด้านล่างเพื่อดำเนินการจอง',
    quickReply: {
      items: [
        {
          type: 'action',
          action: {
            type: 'uri',
            label: 'จองเลย',
            uri: liffUrl,
          },
        },
      ],
    },
  })
}

async function handleCreateEventPostback(
  userId: string,
  replyToken: string
): Promise<void> {
  const liffUrl = `https://liff.line.me/${process.env.LINE_LIFF_ID}/create-event`

  await client.replyMessage(replyToken, {
    type: 'text',
    text: 'เริ่มสร้างอีเวนต์ใหม่',
    quickReply: {
      items: [
        {
          type: 'action',
          action: {
            type: 'uri',
            label: 'สร้างอีเวนต์',
            uri: liffUrl,
          },
        },
      ],
    },
  })
}

async function handleViewAllEventsPostback(
  userId: string,
  replyToken: string
): Promise<void> {
  // Fetch all events
  const events = await fetchAllEvents()

  // Create carousel
  const carousel = createEventCarousel(events)

  await client.replyMessage(replyToken, carousel)
}

async function fetchAllEvents(): Promise<any[]> {
  // Fetch from database
  return []
}
```

---

## Best Practices

1. **User Experience**
   - Use rich messages for better engagement
   - Implement quick replies for common actions
   - Design intuitive rich menus
   - Keep messages concise and in Thai

2. **Performance**
   - Use webhook efficiently
   - Implement message queuing for high traffic
   - Cache user profiles
   - Optimize LIFF loading time

3. **Security**
   - Verify webhook signatures
   - Validate postback data
   - Secure LIFF endpoints
   - Implement rate limiting

4. **Error Handling**
   - Handle webhook timeouts gracefully
   - Provide fallback messages
   - Log all errors for debugging
   - Implement retry mechanisms

5. **Testing**
   - Test in LINE app on both iOS and Android
   - Verify rich menu on different screen sizes
   - Test LIFF on various devices
   - Use LINE's simulator tools

---

## Common Pitfalls

1. **Webhook Timeout**: LINE expects response within 30 seconds
2. **Rich Menu Image Size**: Must be exactly 2500x1686 or 2500x843 pixels
3. **LIFF URL**: Must use HTTPS in production
4. **Message Limits**: Free accounts have monthly message limits
5. **Flex Message Complexity**: Too complex flex messages may not render properly

---

## Production Checklist

- [ ] Webhook endpoint configured and verified
- [ ] Channel access token secured
- [ ] Rich menu created and tested
- [ ] LIFF app registered and tested
- [ ] Error handling implemented
- [ ] Logging configured
- [ ] Rate limiting implemented
- [ ] User data privacy compliant
- [ ] Message templates in Thai
- [ ] Tested on real devices

---

## Tools & Libraries

| Tool | Purpose |
|------|---------|
| @line/bot-sdk | LINE Messaging API SDK |
| @line/liff | LIFF SDK for web apps |
| express | Web server framework |

---

## Further Reading

- [LINE Developers Documentation](https://developers.line.biz/en/docs/)
- [Messaging API Reference](https://developers.line.biz/en/reference/messaging-api/)
- [LIFF Documentation](https://developers.line.biz/en/docs/liff/)
- [Flex Message Simulator](https://developers.line.biz/flex-simulator/)
- [LINE Official Account Manager](https://manager.line.biz/)
