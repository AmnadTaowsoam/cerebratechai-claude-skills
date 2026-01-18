# Escrow Workflow Patterns

## Overview

Patterns for implementing escrow and milestone-based payment systems in marketplace and service platforms. This skill covers escrow state machines, milestone tracking, dispute resolution, automated payouts, and compliance requirements.

---

## 1. Escrow Architecture

### Escrow System Components

```markdown
# Escrow System Architecture

## Core Components
1. **Escrow Account**: Holds funds temporarily
2. **State Machine**: Manages escrow lifecycle
3. **Milestone Tracker**: Tracks project milestones
4. **Payout Engine**: Automates fund releases
5. **Dispute Handler**: Manages conflicts
6. **Audit Trail**: Records all transactions

## Escrow Flow
```
Buyer → Payment → Escrow Account
                      ↓
                  Held Funds
                      ↓
           Milestone Completed?
                      ↓
              Yes → Release → Seller
              No → Hold → Wait
                      ↓
              Dispute? → Resolution
```

## Use Cases
- Freelance marketplaces
- Event planning services
- E-commerce platforms
- Service booking systems
- Real estate transactions
```

---

## 2. Escrow State Machine

### State Definitions

```typescript
// Escrow States
enum EscrowState {
  CREATED = 'created',
  FUNDED = 'funded',
  IN_PROGRESS = 'in_progress',
  MILESTONE_PENDING = 'milestone_pending',
  MILESTONE_APPROVED = 'milestone_approved',
  COMPLETED = 'completed',
  DISPUTED = 'disputed',
  CANCELLED = 'cancelled',
  REFUNDED = 'refunded',
}

// Escrow Events
enum EscrowEvent {
  FUND = 'fund',
  START_WORK = 'start_work',
  SUBMIT_MILESTONE = 'submit_milestone',
  APPROVE_MILESTONE = 'approve_milestone',
  REJECT_MILESTONE = 'reject_milestone',
  COMPLETE = 'complete',
  DISPUTE = 'dispute',
  RESOLVE_DISPUTE = 'resolve_dispute',
  CANCEL = 'cancel',
  REFUND = 'refund',
}

// State Transitions
const stateTransitions: Record<EscrowState, Partial<Record<EscrowEvent, EscrowState>>> = {
  [EscrowState.CREATED]: {
    [EscrowEvent.FUND]: EscrowState.FUNDED,
    [EscrowEvent.CANCEL]: EscrowState.CANCELLED,
  },
  [EscrowState.FUNDED]: {
    [EscrowEvent.START_WORK]: EscrowState.IN_PROGRESS,
    [EscrowEvent.CANCEL]: EscrowState.CANCELLED,
    [EscrowEvent.REFUND]: EscrowState.REFUNDED,
  },
  [EscrowState.IN_PROGRESS]: {
    [EscrowEvent.SUBMIT_MILESTONE]: EscrowState.MILESTONE_PENDING,
    [EscrowEvent.COMPLETE]: EscrowState.COMPLETED,
    [EscrowEvent.DISPUTE]: EscrowState.DISPUTED,
  },
  [EscrowState.MILESTONE_PENDING]: {
    [EscrowEvent.APPROVE_MILESTONE]: EscrowState.MILESTONE_APPROVED,
    [EscrowEvent.REJECT_MILESTONE]: EscrowState.IN_PROGRESS,
    [EscrowEvent.DISPUTE]: EscrowState.DISPUTED,
  },
  [EscrowState.MILESTONE_APPROVED]: {
    [EscrowEvent.SUBMIT_MILESTONE]: EscrowState.MILESTONE_PENDING,
    [EscrowEvent.COMPLETE]: EscrowState.COMPLETED,
  },
  [EscrowState.DISPUTED]: {
    [EscrowEvent.RESOLVE_DISPUTE]: EscrowState.IN_PROGRESS,
  },
  [EscrowState.COMPLETED]: {},
  [EscrowState.CANCELLED]: {},
  [EscrowState.REFUNDED]: {},
}
```

### State Machine Implementation

```typescript
// Escrow State Machine
interface Escrow {
  id: string
  buyerId: string
  sellerId: string
  amount: number
  currency: string
  state: EscrowState
  milestones: Milestone[]
  createdAt: Date
  updatedAt: Date
  metadata?: Record<string, any>
}

interface Milestone {
  id: string
  title: string
  description: string
  amount: number
  dueDate: Date
  status: 'pending' | 'submitted' | 'approved' | 'rejected' | 'paid'
  submittedAt?: Date
  approvedAt?: Date
  paidAt?: Date
  evidence?: string[]
}

class EscrowStateMachine {
  private escrow: Escrow
  private auditLog: AuditEntry[] = []

  constructor(escrow: Escrow) {
    this.escrow = escrow
  }

  async transition(event: EscrowEvent, metadata?: any): Promise<Escrow> {
    const currentState = this.escrow.state
    const nextState = stateTransitions[currentState]?.[event]

    if (!nextState) {
      throw new Error(
        `Invalid transition: ${event} from state ${currentState}`
      )
    }

    // Validate transition
    await this.validateTransition(event, metadata)

    // Execute pre-transition hooks
    await this.beforeTransition(event, metadata)

    // Update state
    this.escrow.state = nextState
    this.escrow.updatedAt = new Date()

    // Log transition
    this.logTransition(currentState, nextState, event, metadata)

    // Execute post-transition hooks
    await this.afterTransition(event, metadata)

    // Save to database
    await this.save()

    return this.escrow
  }

  private async validateTransition(event: EscrowEvent, metadata?: any): Promise<void> {
    switch (event) {
      case EscrowEvent.FUND:
        if (this.escrow.amount <= 0) {
          throw new Error('Invalid escrow amount')
        }
        break

      case EscrowEvent.APPROVE_MILESTONE:
        if (!metadata?.milestoneId) {
          throw new Error('Milestone ID required')
        }
        const milestone = this.escrow.milestones.find(m => m.id === metadata.milestoneId)
        if (!milestone || milestone.status !== 'submitted') {
          throw new Error('Invalid milestone state')
        }
        break

      // Add more validations as needed
    }
  }

  private async beforeTransition(event: EscrowEvent, metadata?: any): Promise<void> {
    switch (event) {
      case EscrowEvent.FUND:
        // Process payment
        await this.processPayment()
        break

      case EscrowEvent.APPROVE_MILESTONE:
        // Release milestone payment
        await this.releaseMilestonePayment(metadata.milestoneId)
        break

      case EscrowEvent.COMPLETE:
        // Release remaining funds
        await this.releaseRemainingFunds()
        break

      case EscrowEvent.REFUND:
        // Process refund
        await this.processRefund()
        break
    }
  }

  private async afterTransition(event: EscrowEvent, metadata?: any): Promise<void> {
    switch (event) {
      case EscrowEvent.FUND:
        // Notify seller
        await this.notifySeller('Escrow funded')
        break

      case EscrowEvent.APPROVE_MILESTONE:
        // Notify seller of payment
        await this.notifySeller('Milestone approved and paid')
        break

      case EscrowEvent.COMPLETE:
        // Notify both parties
        await this.notifyBuyer('Escrow completed')
        await this.notifySeller('Final payment released')
        break

      case EscrowEvent.DISPUTE:
        // Notify admin
        await this.notifyAdmin('Dispute raised')
        break
    }
  }

  private logTransition(
    from: EscrowState,
    to: EscrowState,
    event: EscrowEvent,
    metadata?: any
  ): void {
    this.auditLog.push({
      timestamp: new Date(),
      from,
      to,
      event,
      metadata,
    })
  }

  private async processPayment(): Promise<void> {
    // Implementation depends on payment gateway
  }

  private async releaseMilestonePayment(milestoneId: string): Promise<void> {
    const milestone = this.escrow.milestones.find(m => m.id === milestoneId)
    if (!milestone) return

    // Transfer funds to seller
    await this.transferFunds(this.escrow.sellerId, milestone.amount)

    // Update milestone status
    milestone.status = 'paid'
    milestone.paidAt = new Date()
  }

  private async releaseRemainingFunds(): Promise<void> {
    const paidAmount = this.escrow.milestones
      .filter(m => m.status === 'paid')
      .reduce((sum, m) => sum + m.amount, 0)

    const remainingAmount = this.escrow.amount - paidAmount

    if (remainingAmount > 0) {
      await this.transferFunds(this.escrow.sellerId, remainingAmount)
    }
  }

  private async processRefund(): Promise<void> {
    const paidAmount = this.escrow.milestones
      .filter(m => m.status === 'paid')
      .reduce((sum, m) => sum + m.amount, 0)

    const refundAmount = this.escrow.amount - paidAmount

    if (refundAmount > 0) {
      await this.transferFunds(this.escrow.buyerId, refundAmount)
    }
  }

  private async transferFunds(recipientId: string, amount: number): Promise<void> {
    // Implementation depends on payment system
  }

  private async notifyBuyer(message: string): Promise<void> {
    // Send notification to buyer
  }

  private async notifySeller(message: string): Promise<void> {
    // Send notification to seller
  }

  private async notifyAdmin(message: string): Promise<void> {
    // Send notification to admin
  }

  private async save(): Promise<void> {
    // Save escrow to database
  }
}

interface AuditEntry {
  timestamp: Date
  from: EscrowState
  to: EscrowState
  event: EscrowEvent
  metadata?: any
}
```

---

## 3. Milestone Management

### Milestone Tracker

```typescript
// Milestone Tracker
class MilestoneTracker {
  async createMilestone(
    escrowId: string,
    milestone: Omit<Milestone, 'id' | 'status'>
  ): Promise<Milestone> {
    const newMilestone: Milestone = {
      ...milestone,
      id: this.generateMilestoneId(),
      status: 'pending',
    }

    // Validate total milestone amounts
    const escrow = await this.getEscrow(escrowId)
    const totalMilestoneAmount = [
      ...escrow.milestones,
      newMilestone,
    ].reduce((sum, m) => sum + m.amount, 0)

    if (totalMilestoneAmount > escrow.amount) {
      throw new Error('Total milestone amount exceeds escrow amount')
    }

    // Add milestone to escrow
    escrow.milestones.push(newMilestone)
    await this.updateEscrow(escrow)

    return newMilestone
  }

  async submitMilestone(
    escrowId: string,
    milestoneId: string,
    evidence: string[]
  ): Promise<Milestone> {
    const escrow = await this.getEscrow(escrowId)
    const milestone = escrow.milestones.find(m => m.id === milestoneId)

    if (!milestone) {
      throw new Error('Milestone not found')
    }

    if (milestone.status !== 'pending') {
      throw new Error('Milestone already submitted')
    }

    // Update milestone
    milestone.status = 'submitted'
    milestone.submittedAt = new Date()
    milestone.evidence = evidence

    await this.updateEscrow(escrow)

    // Notify buyer
    await this.notifyBuyer(
      escrow.buyerId,
      `Milestone submitted: ${milestone.title}`
    )

    return milestone
  }

  async approveMilestone(
    escrowId: string,
    milestoneId: string
  ): Promise<Milestone> {
    const escrow = await this.getEscrow(escrowId)
    const milestone = escrow.milestones.find(m => m.id === milestoneId)

    if (!milestone) {
      throw new Error('Milestone not found')
    }

    if (milestone.status !== 'submitted') {
      throw new Error('Milestone not submitted')
    }

    // Approve milestone
    milestone.status = 'approved'
    milestone.approvedAt = new Date()

    await this.updateEscrow(escrow)

    // Trigger escrow state transition
    const stateMachine = new EscrowStateMachine(escrow)
    await stateMachine.transition(EscrowEvent.APPROVE_MILESTONE, { milestoneId })

    return milestone
  }

  async rejectMilestone(
    escrowId: string,
    milestoneId: string,
    reason: string
  ): Promise<Milestone> {
    const escrow = await this.getEscrow(escrowId)
    const milestone = escrow.milestones.find(m => m.id === milestoneId)

    if (!milestone) {
      throw new Error('Milestone not found')
    }

    if (milestone.status !== 'submitted') {
      throw new Error('Milestone not submitted')
    }

    // Reject milestone
    milestone.status = 'rejected'

    await this.updateEscrow(escrow)

    // Notify seller
    await this.notifySeller(
      escrow.sellerId,
      `Milestone rejected: ${milestone.title}\nReason: ${reason}`
    )

    return milestone
  }

  private generateMilestoneId(): string {
    return `MILESTONE-${Date.now()}`
  }

  private async getEscrow(escrowId: string): Promise<Escrow> {
    // Fetch from database
    return {} as Escrow
  }

  private async updateEscrow(escrow: Escrow): Promise<void> {
    // Update in database
  }

  private async notifyBuyer(buyerId: string, message: string): Promise<void> {
    // Send notification
  }

  private async notifySeller(sellerId: string, message: string): Promise<void> {
    // Send notification
  }
}
```

### Milestone Templates

```typescript
// Milestone Templates for Different Event Types
interface MilestoneTemplate {
  name: string
  milestones: Array<{
    title: string
    description: string
    percentage: number
    daysFromStart: number
  }>
}

const milestoneTemplates: Record<string, MilestoneTemplate> = {
  wedding: {
    name: 'งานแต่งงาน',
    milestones: [
      {
        title: 'มัดจำเริ่มต้น',
        description: 'ชำระเมื่อยืนยันการจอง',
        percentage: 30,
        daysFromStart: 0,
      },
      {
        title: 'งวดที่ 2',
        description: 'ชำระ 30 วันก่อนงาน',
        percentage: 40,
        daysFromStart: -30,
      },
      {
        title: 'งวดสุดท้าย',
        description: 'ชำระหลังงานเสร็จสิ้น',
        percentage: 30,
        daysFromStart: 1,
      },
    ],
  },
  party: {
    name: 'งานเลี้ยง',
    milestones: [
      {
        title: 'มัดจำ',
        description: 'ชำระเมื่อยืนยันการจอง',
        percentage: 50,
        daysFromStart: 0,
      },
      {
        title: 'ชำระเต็มจำนวน',
        description: 'ชำระหลังงานเสร็จสิ้น',
        percentage: 50,
        daysFromStart: 1,
      },
    ],
  },
  merit: {
    name: 'งานบุญ',
    milestones: [
      {
        title: 'มัดจำ',
        description: 'ชำระเมื่อยืนยันการจอง',
        percentage: 40,
        daysFromStart: 0,
      },
      {
        title: 'งวดสุดท้าย',
        description: 'ชำระหลังงานเสร็จสิ้น',
        percentage: 60,
        daysFromStart: 1,
      },
    ],
  },
}

function createMilestonesFromTemplate(
  templateName: string,
  totalAmount: number,
  eventDate: Date
): Omit<Milestone, 'id' | 'status'>[] {
  const template = milestoneTemplates[templateName]

  if (!template) {
    throw new Error('Template not found')
  }

  return template.milestones.map((m) => {
    const dueDate = new Date(eventDate)
    dueDate.setDate(dueDate.getDate() + m.daysFromStart)

    return {
      title: m.title,
      description: m.description,
      amount: (totalAmount * m.percentage) / 100,
      dueDate,
    }
  })
}

// Usage
const milestones = createMilestonesFromTemplate(
  'wedding',
  100000, // 100,000 THB
  new Date('2026-06-15')
)
```

---

## 4. Dispute Resolution

### Dispute Handler

```typescript
// Dispute Management
enum DisputeStatus {
  OPEN = 'open',
  UNDER_REVIEW = 'under_review',
  RESOLVED = 'resolved',
  CLOSED = 'closed',
}

enum DisputeResolution {
  BUYER_FAVOR = 'buyer_favor',
  SELLER_FAVOR = 'seller_favor',
  PARTIAL_REFUND = 'partial_refund',
  MEDIATION = 'mediation',
}

interface Dispute {
  id: string
  escrowId: string
  raisedBy: 'buyer' | 'seller'
  reason: string
  description: string
  evidence: string[]
  status: DisputeStatus
  resolution?: DisputeResolution
  resolutionDetails?: string
  refundAmount?: number
  createdAt: Date
  resolvedAt?: Date
}

class DisputeHandler {
  async raiseDispute(
    escrowId: string,
    raisedBy: 'buyer' | 'seller',
    reason: string,
    description: string,
    evidence: string[]
  ): Promise<Dispute> {
    // Validate escrow
    const escrow = await this.getEscrow(escrowId)

    if (escrow.state === EscrowState.COMPLETED || escrow.state === EscrowState.CANCELLED) {
      throw new Error('Cannot dispute completed or cancelled escrow')
    }

    // Create dispute
    const dispute: Dispute = {
      id: this.generateDisputeId(),
      escrowId,
      raisedBy,
      reason,
      description,
      evidence,
      status: DisputeStatus.OPEN,
      createdAt: new Date(),
    }

    // Save dispute
    await this.saveDispute(dispute)

    // Update escrow state
    const stateMachine = new EscrowStateMachine(escrow)
    await stateMachine.transition(EscrowEvent.DISPUTE)

    // Notify parties
    await this.notifyParties(escrow, dispute)

    // Notify admin
    await this.notifyAdmin(dispute)

    return dispute
  }

  async reviewDispute(disputeId: string): Promise<Dispute> {
    const dispute = await this.getDispute(disputeId)

    if (dispute.status !== DisputeStatus.OPEN) {
      throw new Error('Dispute already under review')
    }

    dispute.status = DisputeStatus.UNDER_REVIEW
    await this.updateDispute(dispute)

    return dispute
  }

  async resolveDispute(
    disputeId: string,
    resolution: DisputeResolution,
    details: string,
    refundAmount?: number
  ): Promise<Dispute> {
    const dispute = await this.getDispute(disputeId)
    const escrow = await this.getEscrow(dispute.escrowId)

    if (dispute.status !== DisputeStatus.UNDER_REVIEW) {
      throw new Error('Dispute not under review')
    }

    // Update dispute
    dispute.status = DisputeStatus.RESOLVED
    dispute.resolution = resolution
    dispute.resolutionDetails = details
    dispute.refundAmount = refundAmount
    dispute.resolvedAt = new Date()

    await this.updateDispute(dispute)

    // Execute resolution
    await this.executeResolution(escrow, dispute)

    // Notify parties
    await this.notifyResolution(escrow, dispute)

    return dispute
  }

  private async executeResolution(escrow: Escrow, dispute: Dispute): Promise<void> {
    const stateMachine = new EscrowStateMachine(escrow)

    switch (dispute.resolution) {
      case DisputeResolution.BUYER_FAVOR:
        // Full refund to buyer
        await stateMachine.transition(EscrowEvent.REFUND)
        break

      case DisputeResolution.SELLER_FAVOR:
        // Release all funds to seller
        await stateMachine.transition(EscrowEvent.COMPLETE)
        break

      case DisputeResolution.PARTIAL_REFUND:
        // Partial refund
        if (dispute.refundAmount) {
          await this.processPartialRefund(escrow, dispute.refundAmount)
        }
        await stateMachine.transition(EscrowEvent.RESOLVE_DISPUTE)
        break

      case DisputeResolution.MEDIATION:
        // Continue with mediation
        await stateMachine.transition(EscrowEvent.RESOLVE_DISPUTE)
        break
    }
  }

  private async processPartialRefund(escrow: Escrow, refundAmount: number): Promise<void> {
    // Transfer refund to buyer
    await this.transferFunds(escrow.buyerId, refundAmount)

    // Calculate remaining amount for seller
    const paidAmount = escrow.milestones
      .filter(m => m.status === 'paid')
      .reduce((sum, m) => sum + m.amount, 0)

    const sellerAmount = escrow.amount - paidAmount - refundAmount

    if (sellerAmount > 0) {
      await this.transferFunds(escrow.sellerId, sellerAmount)
    }
  }

  private generateDisputeId(): string {
    return `DISPUTE-${Date.now()}`
  }

  private async getEscrow(escrowId: string): Promise<Escrow> {
    // Fetch from database
    return {} as Escrow
  }

  private async getDispute(disputeId: string): Promise<Dispute> {
    // Fetch from database
    return {} as Dispute
  }

  private async saveDispute(dispute: Dispute): Promise<void> {
    // Save to database
  }

  private async updateDispute(dispute: Dispute): Promise<void> {
    // Update in database
  }

  private async transferFunds(recipientId: string, amount: number): Promise<void> {
    // Implementation depends on payment system
  }

  private async notifyParties(escrow: Escrow, dispute: Dispute): Promise<void> {
    // Notify buyer and seller
  }

  private async notifyAdmin(dispute: Dispute): Promise<void> {
    // Notify admin team
  }

  private async notifyResolution(escrow: Escrow, dispute: Dispute): Promise<void> {
    // Notify all parties of resolution
  }
}
```

---

## 5. Automated Payout Triggers

### Payout Automation

```typescript
// Automated Payout System
interface PayoutTrigger {
  type: 'time_based' | 'event_based' | 'manual'
  condition: string
  milestoneId: string
}

class PayoutAutomation {
  async scheduleAutomaticPayouts(escrow: Escrow): Promise<void> {
    for (const milestone of escrow.milestones) {
      if (milestone.status === 'approved' && !milestone.paidAt) {
        await this.schedulePayout(escrow.id, milestone.id, milestone.dueDate)
      }
    }
  }

  async schedulePayout(
    escrowId: string,
    milestoneId: string,
    dueDate: Date
  ): Promise<void> {
    // Schedule job for payout
    const delay = dueDate.getTime() - Date.now()

    if (delay > 0) {
      setTimeout(async () => {
        await this.processPayout(escrowId, milestoneId)
      }, delay)
    } else {
      // Due date passed, process immediately
      await this.processPayout(escrowId, milestoneId)
    }
  }

  async processPayout(escrowId: string, milestoneId: string): Promise<void> {
    const escrow = await this.getEscrow(escrowId)
    const milestone = escrow.milestones.find(m => m.id === milestoneId)

    if (!milestone || milestone.status !== 'approved') {
      return
    }

    try {
      // Process payout
      const stateMachine = new EscrowStateMachine(escrow)
      await stateMachine.transition(EscrowEvent.APPROVE_MILESTONE, { milestoneId })

      // Log successful payout
      await this.logPayout(escrowId, milestoneId, 'success')
    } catch (error) {
      // Log failed payout
      await this.logPayout(escrowId, milestoneId, 'failed', error.message)

      // Retry after delay
      setTimeout(() => {
        this.processPayout(escrowId, milestoneId)
      }, 3600000) // Retry after 1 hour
    }
  }

  private async getEscrow(escrowId: string): Promise<Escrow> {
    // Fetch from database
    return {} as Escrow
  }

  private async logPayout(
    escrowId: string,
    milestoneId: string,
    status: string,
    error?: string
  ): Promise<void> {
    // Log to database
  }
}
```

---

## 6. Compliance & Audit Trail

### Audit Logging

```typescript
// Comprehensive Audit Trail
interface AuditLog {
  id: string
  escrowId: string
  action: string
  actor: string
  actorType: 'buyer' | 'seller' | 'admin' | 'system'
  details: Record<string, any>
  timestamp: Date
  ipAddress?: string
  userAgent?: string
}

class AuditLogger {
  async log(
    escrowId: string,
    action: string,
    actor: string,
    actorType: 'buyer' | 'seller' | 'admin' | 'system',
    details: Record<string, any>,
    metadata?: { ipAddress?: string; userAgent?: string }
  ): Promise<void> {
    const auditLog: AuditLog = {
      id: this.generateLogId(),
      escrowId,
      action,
      actor,
      actorType,
      details,
      timestamp: new Date(),
      ipAddress: metadata?.ipAddress,
      userAgent: metadata?.userAgent,
    }

    await this.saveLog(auditLog)
  }

  async getEscrowAuditTrail(escrowId: string): Promise<AuditLog[]> {
    // Fetch all logs for escrow
    return []
  }

  async generateAuditReport(escrowId: string): Promise<string> {
    const logs = await this.getEscrowAuditTrail(escrowId)

    let report = `Audit Trail for Escrow ${escrowId}\n\n`

    for (const log of logs) {
      report += `[${log.timestamp.toISOString()}] ${log.action}\n`
      report += `Actor: ${log.actor} (${log.actorType})\n`
      report += `Details: ${JSON.stringify(log.details, null, 2)}\n\n`
    }

    return report
  }

  private generateLogId(): string {
    return `LOG-${Date.now()}`
  }

  private async saveLog(log: AuditLog): Promise<void> {
    // Save to database
  }
}
```

---

## Best Practices

1. **Security**
   - Implement proper access controls
   - Encrypt sensitive data
   - Validate all state transitions
   - Maintain comprehensive audit trails

2. **Reliability**
   - Use database transactions for state changes
   - Implement idempotent operations
   - Handle payment failures gracefully
   - Implement retry mechanisms

3. **Transparency**
   - Provide clear status updates
   - Show milestone progress
   - Display transaction history
   - Notify all parties of changes

4. **Compliance**
   - Follow financial regulations
   - Maintain proper records
   - Implement KYC/AML checks
   - Generate audit reports

5. **User Experience**
   - Clear milestone definitions
   - Easy dispute process
   - Automated notifications
   - Transparent fee structure

---

## Common Pitfalls

1. **State Inconsistency**: Not using transactions can lead to inconsistent states
2. **Race Conditions**: Multiple simultaneous state transitions
3. **Payment Failures**: Not handling payment gateway failures
4. **Dispute Delays**: Not responding to disputes quickly
5. **Audit Gaps**: Missing critical audit log entries

---

## Production Checklist

- [ ] State machine tested thoroughly
- [ ] Payment integration verified
- [ ] Dispute process documented
- [ ] Audit logging implemented
- [ ] Notification system configured
- [ ] Error handling comprehensive
- [ ] Compliance requirements met
- [ ] Security measures in place
- [ ] Performance optimized
- [ ] Monitoring configured

---

## Tools & Libraries

| Tool | Purpose |
|------|---------|
| XState | State machine implementation |
| Bull | Job queue for scheduled payouts |
| Prisma | Database ORM |
| Stripe Connect | Payment platform |

---

## Further Reading

- [Escrow Best Practices](https://stripe.com/docs/connect/escrow)
- [State Machine Patterns](https://xstate.js.org/docs/)
- [Payment Security](https://www.pcisecuritystandards.org/)
- [Financial Compliance](https://www.sec.or.th/)
