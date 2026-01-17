---
name: Human-in-the-Loop Workflows
description: Implementing human approval and review workflows for AI systems to ensure quality, safety, and compliance.
---

# Human-in-the-Loop (HITL) Workflows

## Overview

Human-in-the-Loop (HITL) workflows integrate human judgment into AI systems, ensuring that critical decisions receive human oversight while allowing automation for routine cases. HITL is essential for high-stakes applications and regulatory compliance.

**Core Principle**: "Automate the routine, escalate the exceptional. Humans and AI working together outperform either alone."

---

## 1. What is Human-in-the-Loop?

HITL is a design pattern where humans are actively involved in the AI decision-making process, either by:
- **Approving** AI decisions before they take effect
- **Reviewing** AI decisions after they're made
- **Correcting** AI mistakes to improve the model
- **Handling** edge cases the AI can't process

---

## 2. When to Require Human Approval

### High-Stakes Decisions
```typescript
const requiresHumanApproval = (decision: AIDecision): boolean => {
  // Medical decisions
  if (decision.domain === 'medical' && decision.impact === 'diagnosis') {
    return true;
  }
  
  // Financial decisions above threshold
  if (decision.domain === 'financial' && decision.amount > 10000) {
    return true;
  }
  
  // Legal decisions
  if (decision.domain === 'legal') {
    return true;
  }
  
  // Low confidence predictions
  if (decision.confidence < 0.80) {
    return true;
  }
  
  // Edge cases (new patterns)
  if (decision.isNovelPattern) {
    return true;
  }
  
  return false;
};
```

### Regulatory Requirements
- **EU AI Act**: High-risk AI systems require human oversight
- **GDPR**: Right to human review of automated decisions
- **Fair Credit Reporting Act**: Adverse credit decisions must be explainable
- **Medical Device Regulations**: AI-assisted diagnosis requires physician approval

---

## 3. HITL Workflow Patterns

### Pattern 1: Pre-Approval (Human Before AI Acts)
```python
def pre_approval_workflow(input_data):
    """AI suggests, human approves before action"""
    
    # AI generates recommendation
    recommendation = ai_model.predict(input_data)
    confidence = ai_model.predict_proba(input_data).max()
    
    # Create approval request
    approval_request = {
        'id': generate_id(),
        'input': input_data,
        'recommendation': recommendation,
        'confidence': confidence,
        'explanation': generate_explanation(input_data, recommendation),
        'status': 'pending_approval'
    }
    
    # Add to review queue
    review_queue.add(approval_request)
    
    # Wait for human decision
    human_decision = await_human_approval(approval_request['id'])
    
    if human_decision['approved']:
        execute_action(recommendation)
    else:
        # Log override for model improvement
        log_override(approval_request, human_decision)
```

### Pattern 2: Post-Approval (AI Acts, Human Can Override)
```python
def post_approval_workflow(input_data):
    """AI acts immediately, human can override within window"""
    
    # AI makes decision and acts
    decision = ai_model.predict(input_data)
    action_id = execute_action(decision)
    
    # Create review record
    review_record = {
        'action_id': action_id,
        'decision': decision,
        'confidence': ai_model.predict_proba(input_data).max(),
        'executed_at': datetime.now(),
        'override_window': timedelta(hours=24)
    }
    
    # Add to review queue (lower priority)
    review_queue.add(review_record, priority='low')
    
    # Monitor for override
    if override := check_for_override(action_id, window=24):
        rollback_action(action_id)
        execute_action(override['new_decision'])
```

### Pattern 3: Hybrid (AI Suggests, Human Decides)
```python
def hybrid_workflow(input_data):
    """AI provides options, human makes final decision"""
    
    # AI generates multiple options with scores
    options = ai_model.predict_top_k(input_data, k=3)
    
    # Present to human with context
    human_decision = present_options_to_human({
        'input': input_data,
        'ai_recommendations': [
            {
                'option': opt,
                'confidence': conf,
                'pros': generate_pros(opt),
                'cons': generate_cons(opt)
            }
            for opt, conf in options
        ]
    })
    
    # Execute human's choice
    execute_action(human_decision['selected_option'])
    
    # Learn from human's choice
    if human_decision['selected_option'] != options[0][0]:
        log_preference(input_data, human_decision)
```

### Pattern 4: Escalation (AI Handles Routine, Escalate Exceptions)
```python
def escalation_workflow(input_data):
    """AI handles high-confidence cases, escalates uncertain ones"""
    
    prediction = ai_model.predict(input_data)
    confidence = ai_model.predict_proba(input_data).max()
    
    # Confidence-based routing
    if confidence > 0.95:
        # High confidence: Auto-approve
        execute_action(prediction)
        log_decision(input_data, prediction, 'auto_approved')
        
    elif confidence > 0.80:
        # Medium confidence: Human review (async)
        review_queue.add({
            'input': input_data,
            'prediction': prediction,
            'confidence': confidence,
            'priority': 'medium'
        })
        
    else:
        # Low confidence: Immediate human review
        human_decision = request_immediate_review(input_data, prediction)
        execute_action(human_decision)
```

---

## 4. Confidence Thresholds

```python
class ConfidenceThresholds:
    """Define confidence-based routing"""
    
    AUTO_APPROVE = 0.95  # >95%: Automatic approval
    ASYNC_REVIEW = 0.80  # 80-95%: Queue for review
    SYNC_REVIEW = 0.60   # 60-80%: Immediate review required
    REJECT = 0.60        # <60%: Auto-reject, manual handling
    
    @staticmethod
    def get_action(confidence: float) -> str:
        if confidence >= ConfidenceThresholds.AUTO_APPROVE:
            return 'auto_approve'
        elif confidence >= ConfidenceThresholds.ASYNC_REVIEW:
            return 'async_review'
        elif confidence >= ConfidenceThresholds.SYNC_REVIEW:
            return 'sync_review'
        else:
            return 'manual_handling'
```

---

## 5. Review Queue Management

### Prioritization
```python
def prioritize_review_queue(items: List[ReviewItem]) -> List[ReviewItem]:
    """Prioritize review items by impact and urgency"""
    
    def calculate_priority_score(item: ReviewItem) -> float:
        score = 0
        
        # Business impact
        score += item.financial_impact * 0.4
        
        # Urgency (time-sensitive)
        hours_waiting = (datetime.now() - item.created_at).total_seconds() / 3600
        score += min(hours_waiting / 24, 1.0) * 0.3
        
        # Confidence (lower = higher priority)
        score += (1 - item.confidence) * 0.2
        
        # Regulatory requirement
        if item.requires_compliance_review:
            score += 0.1
        
        return score
    
    return sorted(items, key=calculate_priority_score, reverse=True)
```

### Load Balancing
```python
def assign_to_reviewer(item: ReviewItem, reviewers: List[Reviewer]) -> Reviewer:
    """Assign review item to least-loaded qualified reviewer"""
    
    # Filter qualified reviewers
    qualified = [r for r in reviewers if item.domain in r.expertise]
    
    # Calculate load score
    def load_score(reviewer: Reviewer) -> float:
        return (
            reviewer.current_queue_size * 0.5 +
            reviewer.avg_review_time * 0.3 +
            (1 / reviewer.approval_rate) * 0.2  # Prefer decisive reviewers
        )
    
    # Assign to least-loaded
    return min(qualified, key=load_score)
```

### SLA Tracking
```python
class ReviewSLA:
    """Track SLA compliance for human reviews"""
    
    SLA_TARGETS = {
        'critical': timedelta(hours=1),
        'high': timedelta(hours=4),
        'medium': timedelta(hours=24),
        'low': timedelta(days=3)
    }
    
    @staticmethod
    def check_sla_breach(item: ReviewItem) -> bool:
        age = datetime.now() - item.created_at
        target = ReviewSLA.SLA_TARGETS[item.priority]
        return age > target
    
    @staticmethod
    def alert_sla_breach(item: ReviewItem):
        """Escalate if SLA is breached"""
        send_alert(
            severity='warning',
            message=f"Review SLA breached for {item.id}",
            assignee=item.assigned_reviewer,
            escalate_to=item.assigned_reviewer.manager
        )
```

---

## 6. Reviewer Interface

### Context Display
```typescript
interface ReviewContext {
  // Input data
  inputData: Record<string, any>;
  
  // AI decision
  aiDecision: {
    prediction: string;
    confidence: number;
    alternativeOptions?: Array<{option: string; confidence: number}>;
  };
  
  // Explanation
  explanation: {
    topFeatures: Array<{feature: string; importance: number}>;
    reasoning: string;
    similarCases?: Array<{caseId: string; outcome: string}>;
  };
  
  // Historical context
  history: {
    userPreviousDecisions?: Array<Decision>;
    modelAccuracyOnSimilar?: number;
  };
  
  // Metadata
  metadata: {
    createdAt: Date;
    priority: 'critical' | 'high' | 'medium' | 'low';
    slaDeadline: Date;
  };
}
```

### Approval Interface (React Example)
```typescript
const ReviewInterface: React.FC<{item: ReviewItem}> = ({item}) => {
  const [decision, setDecision] = useState<'approve' | 'reject' | 'modify' | null>(null);
  const [feedback, setFeedback] = useState('');
  
  const handleSubmit = async () => {
    await submitReview({
      itemId: item.id,
      decision,
      feedback,
      modifiedDecision: decision === 'modify' ? modifiedValue : null
    });
  };
  
  return (
    <div className="review-interface">
      {/* AI Recommendation */}
      <section className="ai-recommendation">
        <h3>AI Recommendation</h3>
        <div className="prediction">
          {item.aiDecision.prediction}
          <ConfidenceBadge confidence={item.aiDecision.confidence} />
        </div>
      </section>
      
      {/* Explanation */}
      <section className="explanation">
        <h3>Why AI made this decision</h3>
        <FeatureImportanceChart features={item.explanation.topFeatures} />
        <p>{item.explanation.reasoning}</p>
      </section>
      
      {/* Input Data */}
      <section className="input-data">
        <h3>Input Data</h3>
        <DataTable data={item.inputData} />
      </section>
      
      {/* Actions */}
      <section className="actions">
        <button onClick={() => setDecision('approve')}>
          ✓ Approve AI Decision
        </button>
        <button onClick={() => setDecision('reject')}>
          ✗ Reject
        </button>
        <button onClick={() => setDecision('modify')}>
          ✎ Modify
        </button>
        
        {decision && (
          <textarea
            placeholder="Reason for decision (required)"
            value={feedback}
            onChange={(e) => setFeedback(e.target.value)}
          />
        )}
        
        <button onClick={handleSubmit} disabled={!decision || !feedback}>
          Submit Review
        </button>
      </section>
    </div>
  );
};
```

---

## 7. Feedback Loops

### Learning from Human Corrections
```python
def learn_from_override(original_input, ai_prediction, human_decision, reason):
    """Use human overrides to improve model"""
    
    # Log to training dataset
    training_data.append({
        'features': original_input,
        'ai_label': ai_prediction,
        'human_label': human_decision,
        'confidence': ai_model.predict_proba(original_input).max(),
        'override_reason': reason,
        'timestamp': datetime.now()
    })
    
    # Analyze override patterns
    if len(training_data) % 100 == 0:
        analyze_override_patterns()
        
        # Retrain if override rate is high
        override_rate = calculate_override_rate()
        if override_rate > 0.15:  # >15% override rate
            trigger_model_retraining()

def analyze_override_patterns():
    """Identify systematic errors"""
    overrides = [d for d in training_data if d['ai_label'] != d['human_label']]
    
    # Group by feature combinations
    patterns = identify_common_features(overrides)
    
    for pattern in patterns:
        if pattern['frequency'] > 10:
            alert(f"Systematic error detected: {pattern['description']}")
```

### Confidence Calibration
```python
def calibrate_confidence_from_overrides():
    """Adjust confidence based on human agreement"""
    
    # Calculate actual accuracy at each confidence level
    confidence_buckets = defaultdict(list)
    
    for item in reviewed_items:
        bucket = int(item['confidence'] * 10) / 10  # 0.0, 0.1, 0.2, ...
        was_correct = item['ai_prediction'] == item['human_decision']
        confidence_buckets[bucket].append(was_correct)
    
    # Adjust confidence thresholds
    for bucket, results in confidence_buckets.items():
        actual_accuracy = sum(results) / len(results)
        
        if abs(bucket - actual_accuracy) > 0.1:
            logger.warning(
                f"Confidence {bucket} has actual accuracy {actual_accuracy}. "
                "Model needs recalibration."
            )
```

---

## 8. Metrics to Track

```python
class HITLMetrics:
    """Track HITL workflow performance"""
    
    @staticmethod
    def calculate_metrics(period_days: int = 30):
        cutoff = datetime.now() - timedelta(days=period_days)
        items = ReviewItem.filter(created_at__gte=cutoff)
        
        return {
            # Volume metrics
            'total_decisions': len(items),
            'human_review_rate': len([i for i in items if i.required_review]) / len(items),
            'auto_approved_rate': len([i for i in items if i.auto_approved]) / len(items),
            
            # Quality metrics
            'approval_rate': len([i for i in items if i.approved]) / len(items),
            'override_rate': len([i for i in items if i.overridden]) / len(items),
            'modification_rate': len([i for i in items if i.modified]) / len(items),
            
            # Efficiency metrics
            'avg_review_time': mean([i.review_time for i in items if i.reviewed]),
            'sla_compliance': len([i for i in items if not i.sla_breached]) / len(items),
            
            # Model performance
            'ai_accuracy': len([i for i in items if i.ai_correct]) / len(items),
            'confidence_calibration': calculate_calibration_error(items)
        }
```

---

## 9. Reducing HITL Burden Over Time

### Active Learning
```python
def select_items_for_review(predictions, budget=100):
    """Select most valuable items for human review"""
    
    # Uncertainty sampling: Review low-confidence predictions
    uncertainty_scores = [1 - max(p) for p in predictions]
    
    # Diversity sampling: Review diverse examples
    diversity_scores = calculate_diversity(predictions)
    
    # Combined score
    scores = [
        0.6 * uncertainty + 0.4 * diversity
        for uncertainty, diversity in zip(uncertainty_scores, diversity_scores)
    ]
    
    # Select top items
    top_indices = np.argsort(scores)[-budget:]
    return top_indices
```

### Identifying Auto-Approvable Patterns
```python
def identify_safe_auto_approve_rules():
    """Find patterns where AI is consistently correct"""
    
    # Analyze historical data
    high_confidence_items = [
        i for i in reviewed_items
        if i['confidence'] > 0.95
    ]
    
    # Group by feature patterns
    patterns = cluster_by_features(high_confidence_items)
    
    # Identify patterns with 100% accuracy
    safe_patterns = []
    for pattern in patterns:
        accuracy = sum(p['ai_correct'] for p in pattern) / len(pattern)
        if accuracy == 1.0 and len(pattern) > 50:
            safe_patterns.append(pattern)
    
    # Create auto-approve rules
    for pattern in safe_patterns:
        create_auto_approve_rule(pattern['features'])
```

---

## 10. Real-World HITL Examples

### Content Moderation
```python
def content_moderation_hitl(content):
    """Moderate user-generated content with HITL"""
    
    # AI classifies content
    classification = moderation_model.predict(content)
    confidence = moderation_model.predict_proba(content).max()
    
    if classification == 'safe' and confidence > 0.95:
        # Auto-approve safe content
        return 'approved'
        
    elif classification == 'unsafe' and confidence > 0.99:
        # Auto-remove clearly unsafe content
        return 'removed'
        
    else:
        # Human review for edge cases
        return request_moderator_review(content, classification, confidence)
```

### Loan Approval
```python
def loan_approval_hitl(application):
    """Loan approval with regulatory compliance"""
    
    # AI scores application
    score = credit_model.predict_proba(application)[1]
    
    if score > 0.80:
        # High score: Auto-approve
        return approve_loan(application)
        
    elif score < 0.40:
        # Low score: Auto-reject with explanation
        return reject_loan(application, generate_adverse_action_notice(application))
        
    else:
        # Medium score: Human underwriter review (required by regulation)
        return request_underwriter_review(application, score)
```

---

## 11. HITL Workflow Checklist

- [ ] **Thresholds Defined**: Are confidence thresholds set based on business needs?
- [ ] **Review Queue**: Is there a prioritized queue for human reviews?
- [ ] **SLA Tracking**: Are review SLAs defined and monitored?
- [ ] **Reviewer Interface**: Does the interface provide sufficient context?
- [ ] **Feedback Loop**: Are human corrections fed back to improve the model?
- [ ] **Metrics**: Are we tracking review rate, approval rate, and SLA compliance?
- [ ] **Load Balancing**: Are reviews distributed fairly across reviewers?
- [ ] **Escalation**: Is there a process for urgent reviews?

---

## Related Skills
- `44-ai-governance/confidence-scoring`
- `44-ai-governance/override-mechanisms`
- `44-ai-governance/explainability`
- `44-ai-governance/auditability`
