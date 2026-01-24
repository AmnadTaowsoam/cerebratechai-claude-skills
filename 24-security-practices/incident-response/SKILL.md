---
name: Incident Response
description: Systematic approach to handling security breaches and incidents to minimize damage, reduce recovery time, preserve evidence, and prevent future occurrences through structured response procedures.
---

# Incident Response

> **Current Level:** Intermediate  
> **Domain:** Security / Operations

---

## Overview

Incident response is the systematic approach to handling security breaches and incidents to minimize damage, reduce recovery time, and prevent future occurrences. Effective incident response includes preparation, detection, containment, eradication, recovery, and lessons learned.

## What is Incident Response

### Incident Response Goals

| Goal | Description |
|-------|-------------|
| **Minimize Impact** | Reduce blast radius of incident |
| **Preserve Evidence** | Maintain data for investigation |
| **Restore Services** | Get systems back online quickly |
| **Prevent Recurrence** | Learn and improve |
| **Maintain Trust** | Communicate transparently |

### Why Incident Response Matters

| Benefit | Impact |
|---------|---------|
| **Faster Containment** | Reduce damage from hours to minutes |
| **Evidence Preservation** | Enable root cause analysis |
| **Compliance** | Meet SOC2, ISO 27001 requirements |
| **Customer Trust** | Professional handling builds confidence |
| **Cost Reduction** | Faster recovery = less downtime cost |

## Incident Types

### Common Incident Categories

| Type | Description | Example |
|-------|-------------|---------|
| **Data Breach** | Unauthorized access to sensitive data | Customer database exposed |
| **Malware Infection** | Malicious software on systems | Ransomware, trojans |
| **DDoS Attack** | Distributed denial of service | Website overwhelmed |
| **Account Compromise** | Stolen credentials | Employee account hacked |
| **Insider Threat** | Malicious employee | Data theft by employee |
| **Supply Chain Attack** | Compromised dependency | Malicious npm package |
| **Phishing Campaign** | Social engineering attack | Fake login pages |

## Incident Response Phases

### The Incident Response Lifecycle

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ Preparation │───▶│ Detection   │───▶│ Containment │───▶│ Eradication│───▶│ Recovery    │
│             │    │ & Analysis  │    │             │    │             │    │             │
│ Before      │    │ Incident   │    │ Stop the    │    │ Remove      │    │ Restore     │
│ incident    │    │ identified │    │ bleeding    │    │ threat      │    │ services    │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
      │                  │                  │                  │                  │
      └──────────────────┴──────────────────┴──────────────────┴──────────────────┘
                                      │
                                      ▼
                              ┌─────────────┐
                              │ Post-Incident│
                              │   Activity   │
                              │             │
                              │ Lessons      │
                              │ learned     │
                              └─────────────┘
```

## Preparation Phase

### Incident Response Plan

Document procedures for handling incidents.

**Components**:
- Incident classification
- Escalation procedures
- Communication templates
- Technical procedures
- Contact information

### Incident Response Team

| Role | Responsibilities |
|-------|-----------------|
| **Incident Commander** | Overall coordination, decision making |
| **Technical Lead** | Investigation, remediation |
| **Communications Lead** | Internal/external communication |
| **Legal/Compliance** | Regulatory requirements |
| **PR/Marketing** | Public statements |

### Tools and Resources

| Category | Tools |
|-----------|--------|
| **SIEM** | Splunk, ELK, Datadog |
| **Forensics** | EnCase, FTK, Autopsy |
| **Network Analysis** | Wireshark, tcpdump |
| **Communication** | Slack, PagerDuty, Zoom |
| **Documentation** | Confluence, Google Docs |

### Training and Drills

| Activity | Frequency | Purpose |
|-----------|------------|---------|
| **Tabletop Exercise** | Quarterly | Test procedures |
| **Red Team Exercise** | Annually | Simulate real attack |
| **Incident Review** | After each incident | Learn and improve |
| **Training** | Quarterly | Keep skills current |

### Contact Lists

**Internal**:
- Incident response team
- Executive team
- Legal counsel
- PR/Marketing

**External**:
- Security vendors
- Law enforcement
- Regulatory bodies
- Customers (if needed)

## Detection and Analysis

### Monitoring and Alerting

| Tool Type | Examples | Use Case |
|-----------|-----------|----------|
| **SIEM** | Splunk, ELK Stack | Log aggregation, correlation |
| **IDS/IPS** | Snort, Suricata | Intrusion detection |
| **EDR** | CrowdStrike, SentinelOne | Endpoint protection |
| **WAF** | Cloudflare, AWS WAF | Web application protection |

### Log Analysis

```bash
# Search for suspicious login attempts
grep "Failed password" /var/log/auth.log | tail -100

# Find unusual access patterns
awk '$9 > 1000 {print}' /var/log/nginx/access.log

# Correlate events across systems
# (Use SIEM for complex correlation)
```

### Threat Intelligence

| Source | Type | Use Case |
|---------|-------|----------|
| **CVE Database** | Known vulnerabilities | Check for exploited CVEs |
| **IOC Feeds** | Indicators of compromise | Block known bad IPs |
| **Threat Reports** | Industry-specific threats | Understand attack landscape |

### Initial Assessment

| Question | Why It Matters |
|-----------|----------------|
| **What happened?** | Understand the incident |
| **When did it happen?** | Determine timeline |
| **Who is affected?** | Assess impact |
| **What is the scope?** | Determine blast radius |
| **What is the severity?** | Prioritize response |

## Incident Severity Levels

### Severity Classification

| Level | Name | Description | Response Time |
|--------|-------|-------------|---------------|
| **SEV1** | Critical | Massive impact, complete outage, data breach | < 15 min |
| **SEV2** | High | Significant impact, partial outage, active attack | < 1 hour |
| **SEV3** | Medium | Moderate impact, suspicious activity | < 4 hours |
| **SEV4** | Low | Minor impact, failed login attempts | < 24 hours |

### Severity Examples

| Scenario | Severity | Rationale |
|----------|-----------|-------------|
| Production database exposed publicly | SEV1 | Critical data breach |
| Ransomware encrypting production servers | SEV1 | Complete outage |
| DDoS attack degrading service | SEV2 | Partial outage |
| Suspicious login attempts from new IP | SEV3 | Potential attack |
| Single employee account compromised | SEV3 | Limited impact |
| Failed login attempts from known bad IP | SEV4 | Routine security event |

## Containment Strategies

### Short-term Containment

Immediate actions to stop the bleeding.

| Action | When to Use |
|---------|---------------|
| **Isolate affected systems** | Active malware spreading |
| **Block malicious IPs** | Ongoing attack |
| **Disable compromised accounts** | Account takeover |
| **Shut down vulnerable services** | Exploit in progress |
| **Switch to backup systems** | Production unavailable |

### Long-term Containment

Permanent fixes to prevent recurrence.

| Action | Example |
|---------|-----------|
| **Patch vulnerabilities** | Apply security patches |
| **Update configurations** | Secure misconfigured services |
| **Implement controls** | Add new security measures |
| **Improve monitoring** | Add alerts for similar incidents |

### Evidence Preservation

**Why Important**: Enables root cause analysis and legal proceedings.

**Actions**:
- Take forensic images of affected systems
- Preserve logs (don't modify)
- Document timeline
- Chain of custody for evidence

### Rebuild vs Clean

| Option | When to Use | Pros | Cons |
|--------|--------------|-------|-------|
| **Rebuild** | Malware infection, unknown compromise | Clean slate | Time-consuming |
| **Clean** | Known compromise, limited scope | Faster | Risk of missing malware |

## Eradication

### Actions

| Action | Description |
|---------|-------------|
| **Remove malware** | Delete malicious files, processes |
| **Remove backdoors** | Eliminate unauthorized access |
| **Patch vulnerabilities** | Fix exploited vulnerabilities |
| **Reset credentials** | Change compromised passwords |
| **Remove unauthorized accounts** | Delete attacker-created accounts |

### Verification

**Confirm threat is eliminated**:

```bash
# Scan for malware
clamscan -r /path/to/system

# Check for suspicious processes
ps aux | grep -v grep | grep suspicious

# Verify no unauthorized access
lastlog | grep suspicious_user

# Check for modified files
find /path -mtime -1 -ls
```

## Recovery

### Restore Systems

| Action | Description |
|---------|-------------|
| **Restore from clean backups** | Use verified backup |
| **Rebuild from scratch** | Fresh installation |
| **Verify system integrity** | Check for backdoors |
| **Update configurations** | Apply security hardening |
| **Monitor for reinfection** | Watch for suspicious activity |

### Gradual Return

**Staged recovery to minimize risk**:

1. **Phase 1**: Restore critical services
2. **Phase 2**: Verify functionality
3. **Phase 3**: Restore remaining services
4. **Phase 4**: Full production

### Monitoring Post-Recovery

| What to Monitor | Why |
|-----------------|------|
| **System logs** | Detect reinfection |
| **Performance metrics** | Ensure stability |
| **Security alerts** | Catch new threats |
| **User reports** | Identify issues |

## Post-Incident Activity

### Incident Report

**Components**:

1. **Executive Summary**
   - What happened
   - Impact
   - Timeline

2. **Incident Details**
   - Detection
   - Analysis
   - Actions taken

3. **Root Cause Analysis**
   - How did it happen?
   - Why did it happen?

4. **Lessons Learned**
   - What went well
   - What didn't
   - Recommendations

### Root Cause Analysis

**Techniques**:

| Technique | Description |
|-----------|-------------|
| **5 Whys** | Ask "why" 5 times to find root cause |
| **Fishbone Diagram** | Visualize causes and effects |
| **Timeline Analysis** | Reconstruct incident chronology |
| **Evidence Review** | Analyze all collected data |

**Example (5 Whys)**:
1. Why was the database exposed? → Misconfigured firewall
2. Why was firewall misconfigured? → No documentation
3. Why was there no documentation? → Not required by process
4. Why not required? → Gap in security procedures
5. Why gap in procedures? → No regular security review

**Root Cause**: Lack of regular security review procedures

### Lessons Learned

| Category | Questions |
|-----------|------------|
| **Detection** | How could we detect this faster? |
| **Containment** | How could we contain this faster? |
| **Recovery** | How could we recover faster? |
| **Prevention** | How could we prevent this? |
| **Communication** | How could we communicate better? |

### Update Response Plan

**Based on lessons learned**:

- Update procedures
- Improve monitoring
- Add new tools
- Update contact lists
- Schedule training

## Communication

### Internal Communication

| Stakeholder | When | What |
|-------------|-------|-------|
| **Executive Team** | Immediately | Severity, impact, actions |
| **Affected Teams** | As needed | Specific impact, workarounds |
| **All Employees** | If public incident | What to say to customers |

### External Communication

| Stakeholder | When | What |
|-------------|-------|-------|
| **Customers** | If data breach or outage | Impact, timeline, next steps |
| **Partners** | If affected | Impact, mitigation |
| **Regulators** | If required by law | Breach notification |
| **Media** | If public incident | Official statement |

### Timing

| Requirement | Timeline |
|-------------|-----------|
| **GDPR** | 72 hours |
| **US State Laws** | Varies (30-90 days) |
| **PCI DSS** | Immediately |
| **HIPAA** | 60 days |

### Message Guidelines

| Do | Don't |
|-----|-------|
| Be transparent | Hide information |
| Provide timelines | Make promises you can't keep |
| Offer mitigation | Blame others |
| Show empathy | Be defensive |
| Update regularly | Leave people in the dark |

### Communication Templates

**Initial Notification**:
```
Subject: [SEV1] Security Incident - [Brief Description]

We are currently investigating a security incident affecting [affected systems/data].

Impact: [Description]
Current Status: [Status]
Next Update: [Time]

Incident Commander: [Name]
```

**Customer Notification**:
```
Subject: Important Security Notice

We recently discovered a security incident that may have affected your [data type].

What happened: [Description]
What we're doing: [Actions]
What you should do: [Customer actions]
When to expect next update: [Time]

We apologize for any inconvenience and are committed to resolving this issue.
```

## Legal and Compliance

### Data Breach Notification Laws

| Regulation | Timeline | Requirements |
|-------------|-----------|--------------|
| **GDPR** | 72 hours | Notify supervisory authority, affected individuals |
| **CCPA** | No specific timeline | Reasonable security practices |
| **US State Laws** | 30-90 days | Varies by state |
| **PCI DSS** | Immediately | Notify card brands, affected customers |

### Evidence Preservation

**Chain of Custody**:
- Document who collected evidence
- Document when evidence was collected
- Document how evidence was stored
- Maintain integrity (hashes, write-once media)

### Law Enforcement Involvement

| When to Involve | Actions |
|-----------------|----------|
| **Data breach** | Contact FBI, local law enforcement |
| **Financial crime** | Contact financial crimes unit |
| **Cybercrime** | Contact cybercrime division |

### Legal Counsel

**Consult before**:
- Public statements
- Notifying regulators
- Disclosing to customers
- Providing evidence to law enforcement

## Incident Response Team Roles

### Incident Commander

**Responsibilities**:
- Overall coordination
- Decision making
- Resource allocation
- Communication with executives

### Technical Lead

**Responsibilities**:
- Investigation
- Remediation
- Technical guidance
- Evidence collection

### Communications Lead

**Responsibilities**:
- Internal communication
- External communication
- Media relations
- Customer notifications

### Legal/Compliance

**Responsibilities**:
- Regulatory requirements
- Legal guidance
- Evidence handling
- Law enforcement coordination

## Tools for Incident Response

### SIEM (Security Information and Event Management)

| Tool | Strengths | Pricing |
|------|-----------|---------|
| **Splunk** | Powerful, enterprise | $$$ |
| **ELK Stack** | Open-source, flexible | Free/$ |
| **Datadog** | Cloud-native, easy | $$ |
| **Sumo Logic** | Cloud logs, good UI | $$ |

### Forensics Tools

| Tool | Type | Use Case |
|------|-------|----------|
| **EnCase** | Commercial | Enterprise forensics |
| **FTK** | Commercial | Digital forensics |
| **Autopsy** | Open-source | Disk analysis |
| **Volatility** | Open-source | Memory forensics |

### Network Analysis

| Tool | Type | Use Case |
|------|-------|----------|
| **Wireshark** | GUI | Packet capture, analysis |
| **tcpdump** | CLI | Packet capture |
| **nmap** | CLI | Port scanning |
| **netcat** | CLI | Network debugging |

### Malware Analysis

| Tool | Type | Use Case |
|------|-------|----------|
| **Cuckoo Sandbox** | Open-source | Malware analysis |
| **VirusTotal** | Online | File scanning |
| **YARA** | Open-source | Malware detection rules |

## Runbooks for Common Incidents

### Data Breach Response

```
1. Identify scope (what data, how many users)
2. Contain (stop data exfiltration)
3. Preserve evidence
4. Notify legal/compliance
5. Notify affected users
6. Investigate root cause
7. Remediate vulnerabilities
8. Implement controls
9. Document lessons learned
```

### Ransomware Response

```
1. Isolate infected systems
2. Identify ransomware variant
3. Assess impact (encrypted files)
4. Preserve evidence
5. Evaluate decryption options
6. Restore from backups
7. Verify backups are clean
8. Patch vulnerabilities
9. Update security controls
10. Document lessons learned
```

### DDoS Mitigation

```
1. Identify attack type/volume
2. Implement rate limiting
3. Enable DDoS protection (Cloudflare, AWS Shield)
4. Filter malicious traffic
5. Scale infrastructure
6. Monitor for bypass attempts
7. Document attack details
8. Update DDoS response plan
```

### Account Takeover Response

```
1. Disable compromised account
2. Reset credentials
3. Investigate access logs
4. Check for lateral movement
5. Reset other potentially compromised accounts
6. Enable MFA
7. Review account activity
8. Document incident
9. Educate user on security
```

## Metrics to Track

### Key Performance Indicators

| Metric | Formula | Target |
|---------|---------|---------|
| **MTTD** | Mean Time To Detect | < 1 hour |
| **MTTR** | Mean Time To Respond | < 4 hours |
| **MTTC** | Mean Time To Contain | < 8 hours |
| **Incidents per month** | Count of incidents | Trending down |
| **False positive rate** | False alerts / Total alerts | < 5% |

### Calculating Metrics

```python
import numpy as np
from datetime import datetime, timedelta

# Example incident data
incidents = [
    {
        'detected_at': datetime(2024, 1, 15, 10, 0),
        'responded_at': datetime(2024, 1, 15, 10, 30),
        'contained_at': datetime(2024, 1, 15, 14, 0),
        'resolved_at': datetime(2024, 1, 15, 18, 0)
    },
    # ... more incidents
]

def calculate_metrics(incidents):
    """Calculate incident response metrics."""
    mttd = []
    mttr = []
    mttc = []
    mttr_resolved = []

    for incident in incidents:
        mttd.append((incident['responded_at'] - incident['detected_at']).total_seconds() / 3600)
        mttr.append((incident['responded_at'] - incident['detected_at']).total_seconds() / 3600)
        mttc.append((incident['contained_at'] - incident['detected_at']).total_seconds() / 3600)
        mttr_resolved.append((incident['resolved_at'] - incident['detected_at']).total_seconds() / 3600)

    return {
        'MTTD (hours)': np.mean(mttd),
        'MTTR (hours)': np.mean(mttr),
        'MTTC (hours)': np.mean(mttc),
        'MTTR Resolved (hours)': np.mean(mttr_resolved)
    }

metrics = calculate_metrics(incidents)
print(metrics)
```

## Tabletop Exercises

### Purpose

- Test incident response procedures
- Identify gaps
- Train team members
- Improve coordination

### Exercise Types

| Type | Description |
|-------|-------------|
| **Scenario-based** | Walk through specific incident |
| **Functional** | Simulate technical response |
| **Full-scale** | Complete simulation with all teams |

### Sample Scenario

**Scenario**: Ransomware attack on production database

**Questions**:
1. Who is notified first?
2. What containment actions are taken?
3. How do we communicate with customers?
4. What recovery procedures are followed?
5. What decisions need to be made?

### After-Action Review

| Question | Purpose |
|-----------|---------|
| What went well? | Reinforce good practices |
| What didn't go well? | Identify gaps |
| What should we change? | Improve procedures |
| What tools do we need? | Resource planning |

## Third-Party Incident Response

### When to Engage External Help

| Situation | Action |
|-----------|--------|
| **Major breach** | Engage incident response firm |
| **Lack of expertise** | Hire security consultant |
| **Forensics needed** | Use professional forensics team |

### Incident Response Retainers

**Benefits**:
- Pre-negotiated rates
- Faster response time
- Familiarity with your systems
- Access to specialized tools

### Cyber Insurance

**Coverage**:
- Data breach response costs
- Legal fees
- Customer notification costs
- Business interruption
- Ransomware payments (some policies)

## Real Incident Examples

### Example 1: SQL Injection Leading to Data Breach

**Incident**:
- Attacker exploited SQL injection vulnerability
- Accessed customer database
- Exposed 100,000 records

**Response**:
1. **Detection**: Anomaly in database queries
2. **Containment**: Blocked attacker IP, disabled vulnerable endpoint
3. **Eradication**: Patched vulnerability, reset credentials
4. **Recovery**: Restored from clean backup
5. **Lessons**: Added input validation, implemented WAF

### Example 2: Ransomware Attack

**Incident**:
- Phishing email delivered ransomware
- Encrypted production servers
- Demanded $1M ransom

**Response**:
1. **Detection**: User reported suspicious activity
2. **Containment**: Isolated infected servers
3. **Eradication**: Restored from backups, reimaged systems
4. **Recovery**: Gradual restoration of services
5. **Lessons**: Improved email filtering, user training

### Example 3: Compromised Credentials

**Incident**:
- Employee credentials stolen via phishing
- Attacker accessed internal systems
- Data exfiltration detected

**Response**:
1. **Detection**: Unusual access patterns
2. **Containment**: Disabled compromised account, blocked attacker IP
3. **Eradication**: Reset credentials, reviewed access logs
4. **Recovery**: Verified no lateral movement
5. **Lessons**: Implemented MFA, security awareness training

---

## Quick Start

### Incident Response Plan

```markdown
# Incident Response Plan

## Team
- Incident Commander: [Name]
- Security Lead: [Name]
- Engineering Lead: [Name]
- Communications: [Name]

## Phases
1. **Preparation** - Tools, training, documentation
2. **Detection** - Monitoring, alerts, identification
3. **Containment** - Isolate affected systems
4. **Eradication** - Remove threat
5. **Recovery** - Restore services
6. **Lessons Learned** - Post-mortem, improvements
```

### Incident Detection

```typescript
// Monitor for security incidents
async function detectIncident(alert: SecurityAlert) {
  if (alert.severity === 'critical') {
    await createIncident({
      title: alert.title,
      severity: 'critical',
      status: 'open',
      detectedAt: new Date()
    })
    
    await notifyIncidentTeam()
  }
}
```

---

## Production Checklist

- [ ] **Response Plan**: Documented incident response plan
- [ ] **Team**: Incident response team identified
- [ ] **Tools**: Security tools and resources available
- [ ] **Training**: Regular training and drills
- [ ] **Communication**: Communication channels established
- [ ] **Monitoring**: Security monitoring in place
- [ ] **Containment**: Containment procedures defined
- [ ] **Recovery**: Recovery procedures documented
- [ ] **Post-mortem**: Post-mortem process
- [ ] **Documentation**: Document all incidents
- [ ] **Improvement**: Continuous improvement
- [ ] **Compliance**: Meet compliance requirements

---

## Anti-patterns

### ❌ Don't: No Plan

```markdown
# ❌ Bad - No plan
"Figure it out when it happens"
```

```markdown
# ✅ Good - Documented plan
# Incident Response Plan
- Team roles defined
- Procedures documented
- Tools ready
- Regular drills
```

### ❌ Don't: Slow Response

```markdown
# ❌ Bad - Slow response
Incident detected → Wait 24 hours → Respond
# Damage spreads!
```

```markdown
# ✅ Good - Fast response
Incident detected → Immediate containment → Investigation
# Minimize damage
```

---

## Integration Points

- **Vulnerability Management** (`24-security-practices/vulnerability-management/`) - Vulnerability handling
- **Security Audit** (`24-security-practices/security-audit/`) - Security reviews
- **Monitoring** (`14-monitoring-observability/`) - Security monitoring

---

## Further Reading

- [NIST Incident Response Guide](https://www.nist.gov/publications/computer-security-incident-handling-guide)
- [SANS Incident Response](https://www.sans.org/reading-room/whitepapers/incident/incident-handlers-handbook-33901)

### During Incident

- [ ] Severity assessed
- [ ] Incident commander assigned
- [ ] Containment actions taken
- [ ] Evidence preserved
- [ ] Stakeholders notified

### After Incident

- [ ] Root cause identified
- [ ] Incident report completed
- [ ] Lessons learned documented
- [ ] Response plan updated
- [ ] Improvements implemented
