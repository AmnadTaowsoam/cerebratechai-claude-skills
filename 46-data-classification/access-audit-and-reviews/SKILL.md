---
name: Access Audit and Reviews
description: Comprehensive guide to access audits, periodic reviews, anomaly detection, and segregation of duties for compliance and security.
---

# Access Audit and Reviews

## Overview

Access audits and periodic reviews ensure that users have appropriate access to systems and data. This is critical for:

- **Compliance**: SOC2, ISO 27001, HIPAA, PCI-DSS requirements
- **Security**: Detect unauthorized access and insider threats
- **Least Privilege**: Ensure users have only necessary access
- **Accountability**: Track who accessed what and when

**Key Principle**: Trust, but verify. Regularly audit access rights and usage.

## 1. Why Access Audits Matter

### Compliance Requirements

**SOC2 (Trust Services Criteria)**:
```
CC6.2: Prior to issuing system credentials and granting system access, the entity registers and authorizes new internal and external users.

CC6.3: The entity authorizes, modifies, or removes access to data, software, functions, and other protected information assets based on roles, responsibilities, or the system design and changes.

Requirement: Quarterly access reviews
```

**ISO 27001**:
```
A.9.2.5: Review of user access rights
- Regular reviews of access rights
- Removal of unnecessary access
- Documentation of review process

Requirement: At least annually, more frequently for privileged access
```

**HIPAA**:
```
§164.308(a)(4)(ii)(C): Access authorization
- Implement procedures for granting access to ePHI
- Periodic review of access

Requirement: Regular access reviews for PHI access
```

**PCI-DSS**:
```
Requirement 7: Restrict access to cardholder data by business need to know
Requirement 8: Identify and authenticate access to system components

Requirement: Quarterly access reviews
```

### Security Benefits

```
Insider Threat Detection:
- 34% of data breaches involve internal actors (Verizon DBIR 2023)
- Access reviews can detect:
  - Excessive permissions
  - Dormant accounts
  - Unauthorized access
  - Privilege creep

Cost of Insider Breach: $4.9M average (IBM 2023)
```

### Least Privilege Enforcement

```
Principle of Least Privilege:
- Users should have minimum access needed for their job
- Reduces blast radius of compromised accounts
- Limits accidental damage

Access Creep Problem:
- Users accumulate permissions over time
- Job changes don't trigger access removal
- Result: 30-50% of users have excessive access
```

## 2. What to Audit

### User Access

```python
def audit_user_access():
    """Audit what users can access."""
    
    users = get_all_users()
    audit_results = []
    
    for user in users:
        access_summary = {
            'user_id': user.id,
            'email': user.email,
            'role': user.role,
            'permissions': get_user_permissions(user.id),
            'resources': get_accessible_resources(user.id),
            'last_login': user.last_login_at,
            'account_age': (datetime.now() - user.created_at).days,
            'status': user.status
        }
        
        # Flag issues
        issues = []
        
        # Dormant account
        if user.last_login_at and (datetime.now() - user.last_login_at).days > 90:
            issues.append('dormant_account')
        
        # Excessive permissions
        if len(access_summary['permissions']) > 20:
            issues.append('excessive_permissions')
        
        # Admin without MFA
        if 'admin' in user.role and not user.mfa_enabled:
            issues.append('admin_without_mfa')
        
        access_summary['issues'] = issues
        audit_results.append(access_summary)
    
    return audit_results
```

### Admin Access

```python
def audit_admin_access():
    """Audit privileged access."""
    
    admins = get_users_with_role('admin')
    audit_results = []
    
    for admin in admins:
        admin_summary = {
            'user_id': admin.id,
            'email': admin.email,
            'role': admin.role,
            'permissions': get_admin_permissions(admin.id),
            'mfa_enabled': admin.mfa_enabled,
            'last_login': admin.last_login_at,
            'recent_actions': get_recent_admin_actions(admin.id, days=30),
            'justification': get_admin_justification(admin.id)
        }
        
        # Flag critical issues
        issues = []
        
        if not admin.mfa_enabled:
            issues.append('CRITICAL: Admin without MFA')
        
        if not admin.last_login_at or (datetime.now() - admin.last_login_at).days > 30:
            issues.append('WARNING: Unused admin account')
        
        if not get_admin_justification(admin.id):
            issues.append('WARNING: No justification for admin access')
        
        admin_summary['issues'] = issues
        audit_results.append(admin_summary)
    
    return audit_results
```

### Service Account Access

```python
def audit_service_accounts():
    """Audit service account access."""
    
    service_accounts = get_service_accounts()
    audit_results = []
    
    for sa in service_accounts:
        sa_summary = {
            'account_id': sa.id,
            'name': sa.name,
            'type': sa.type,  # API key, OAuth app, etc.
            'permissions': get_service_account_permissions(sa.id),
            'owner': sa.owner_email,
            'created_at': sa.created_at,
            'last_used': sa.last_used_at,
            'rotation_policy': sa.rotation_policy,
            'last_rotated': sa.last_rotated_at
        }
        
        # Flag issues
        issues = []
        
        # Never used
        if not sa.last_used_at:
            issues.append('never_used')
        
        # Not used in 90 days
        if sa.last_used_at and (datetime.now() - sa.last_used_at).days > 90:
            issues.append('dormant')
        
        # No rotation policy
        if not sa.rotation_policy:
            issues.append('no_rotation_policy')
        
        # Overdue for rotation
        if sa.rotation_policy and sa.last_rotated_at:
            days_since_rotation = (datetime.now() - sa.last_rotated_at).days
            if days_since_rotation > sa.rotation_policy.days:
                issues.append('overdue_rotation')
        
        # No owner
        if not sa.owner_email:
            issues.append('no_owner')
        
        sa_summary['issues'] = issues
        audit_results.append(sa_summary)
    
    return audit_results
```

### Database Access

```sql
-- PostgreSQL: Audit database access
SELECT 
    usename as username,
    usecreatedb as can_create_db,
    usesuper as is_superuser,
    valuntil as password_expiry,
    (SELECT array_agg(datname) 
     FROM pg_database d 
     WHERE has_database_privilege(u.usename, d.datname, 'CONNECT')) as accessible_databases
FROM pg_user u
ORDER BY is_superuser DESC, username;

-- List table-level permissions
SELECT 
    grantee,
    table_schema,
    table_name,
    privilege_type
FROM information_schema.table_privileges
WHERE grantee NOT IN ('postgres', 'PUBLIC')
ORDER BY grantee, table_schema, table_name;
```

### File System Access

```python
import os
import pwd
import grp

def audit_file_permissions(directory):
    """Audit file system permissions."""
    
    audit_results = []
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            filepath = os.path.join(root, file)
            stat_info = os.stat(filepath)
            
            # Get owner and group
            owner = pwd.getpwuid(stat_info.st_uid).pw_name
            group = grp.getgrgid(stat_info.st_gid).gr_name
            
            # Get permissions
            permissions = oct(stat_info.st_mode)[-3:]
            
            audit_results.append({
                'file': filepath,
                'owner': owner,
                'group': group,
                'permissions': permissions,
                'size': stat_info.st_size,
                'modified': datetime.fromtimestamp(stat_info.st_mtime)
            })
            
            # Flag issues
            if permissions == '777':
                logger.warning(f"World-writable file: {filepath}")
            
            if owner == 'root' and permissions[1] == '7':
                logger.warning(f"Root-owned file with group write: {filepath}")
    
    return audit_results
```

### Third-Party Access

```python
def audit_third_party_access():
    """Audit third-party vendor access."""
    
    vendors = get_third_party_vendors()
    audit_results = []
    
    for vendor in vendors:
        vendor_summary = {
            'vendor_name': vendor.name,
            'access_type': vendor.access_type,  # API, VPN, SSH, etc.
            'permissions': vendor.permissions,
            'data_accessed': vendor.data_accessed,
            'contract_start': vendor.contract_start_date,
            'contract_end': vendor.contract_end_date,
            'last_access': vendor.last_access_at,
            'access_frequency': vendor.access_frequency,
            'dpa_signed': vendor.dpa_signed,  # Data Processing Agreement
            'security_review_date': vendor.security_review_date
        }
        
        # Flag issues
        issues = []
        
        # Contract expired
        if vendor.contract_end_date and datetime.now() > vendor.contract_end_date:
            issues.append('CRITICAL: Contract expired, access should be revoked')
        
        # No DPA
        if not vendor.dpa_signed:
            issues.append('WARNING: No Data Processing Agreement')
        
        # Stale security review
        if not vendor.security_review_date or (datetime.now() - vendor.security_review_date).days > 365:
            issues.append('WARNING: Security review overdue')
        
        vendor_summary['issues'] = issues
        audit_results.append(vendor_summary)
    
    return audit_results
```

## 3. Audit Frequency

### Recommended Schedules

```yaml
# audit-schedule.yaml
audit_schedule:
  user_access:
    frequency: quarterly
    scope: all_users
    owner: security_team
    
  admin_access:
    frequency: monthly
    scope: privileged_users
    owner: security_team
    
  service_accounts:
    frequency: quarterly
    scope: all_service_accounts
    owner: engineering_team
    
  database_access:
    frequency: monthly
    scope: production_databases
    owner: dba_team
    
  third_party_access:
    frequency: quarterly
    scope: all_vendors
    owner: compliance_team
    
  critical_systems:
    frequency: monthly
    scope: payment_systems, phi_systems
    owner: security_team
    
  comprehensive_audit:
    frequency: annually
    scope: all_access
    owner: compliance_team
```

### Implementation

```python
from apscheduler.schedulers.background import BackgroundScheduler

def schedule_access_audits():
    """Schedule automated access audits."""
    
    scheduler = BackgroundScheduler()
    
    # Monthly: Admin access review
    scheduler.add_job(
        audit_admin_access,
        'cron',
        day=1,
        hour=9,
        minute=0
    )
    
    # Quarterly: User access review
    scheduler.add_job(
        audit_user_access,
        'cron',
        month='1,4,7,10',
        day=1,
        hour=9,
        minute=0
    )
    
    # Quarterly: Service account review
    scheduler.add_job(
        audit_service_accounts,
        'cron',
        month='1,4,7,10',
        day=15,
        hour=9,
        minute=0
    )
    
    # Annual: Comprehensive audit
    scheduler.add_job(
        comprehensive_access_audit,
        'cron',
        month=1,
        day=1,
        hour=9,
        minute=0
    )
    
    scheduler.start()
```

## 4. Access Review Process

### Step-by-Step Process

```python
from enum import Enum

class ReviewStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    APPROVED = "approved"
    REJECTED = "rejected"
    REMEDIATED = "remediated"

class AccessReview:
    """Manage access review process."""
    
    def __init__(self, review_id, review_type, scope):
        self.review_id = review_id
        self.review_type = review_type  # user, admin, service_account
        self.scope = scope
        self.status = ReviewStatus.PENDING
        self.created_at = datetime.now()
        self.findings = []
    
    def generate_report(self):
        """Step 1: Generate access report."""
        
        if self.review_type == 'user':
            self.findings = audit_user_access()
        elif self.review_type == 'admin':
            self.findings = audit_admin_access()
        elif self.review_type == 'service_account':
            self.findings = audit_service_accounts()
        
        # Save report
        save_audit_report(self.review_id, self.findings)
        
        logger.info(f"Generated audit report {self.review_id} with {len(self.findings)} findings")
    
    def assign_reviewers(self):
        """Step 2: Assign to managers for review."""
        
        # Group findings by manager
        by_manager = {}
        
        for finding in self.findings:
            manager = get_manager_for_user(finding['user_id'])
            
            if manager not in by_manager:
                by_manager[manager] = []
            
            by_manager[manager].append(finding)
        
        # Send to each manager
        for manager, findings in by_manager.items():
            send_review_request(
                manager_email=manager,
                review_id=self.review_id,
                findings=findings
            )
        
        self.status = ReviewStatus.IN_PROGRESS
        
        logger.info(f"Assigned review {self.review_id} to {len(by_manager)} managers")
    
    def collect_responses(self):
        """Step 3: Collect manager responses."""
        
        responses = get_review_responses(self.review_id)
        
        # Check if all responded
        total_reviewers = count_assigned_reviewers(self.review_id)
        
        if len(responses) < total_reviewers:
            # Send reminders
            send_review_reminders(self.review_id)
            return False
        
        # All responded
        return True
    
    def remediate_findings(self):
        """Step 4: Remediate excessive access."""
        
        responses = get_review_responses(self.review_id)
        
        for response in responses:
            if response.action == 'revoke':
                # Revoke access
                revoke_user_access(
                    user_id=response.user_id,
                    permissions=response.permissions_to_revoke
                )
                
                logger.info(f"Revoked access for user {response.user_id}")
            
            elif response.action == 'modify':
                # Modify access
                modify_user_access(
                    user_id=response.user_id,
                    new_permissions=response.new_permissions
                )
                
                logger.info(f"Modified access for user {response.user_id}")
            
            elif response.action == 'approve':
                # Access is appropriate
                logger.info(f"Approved access for user {response.user_id}")
        
        self.status = ReviewStatus.REMEDIATED
    
    def document_findings(self):
        """Step 5: Document findings for compliance."""
        
        report = {
            'review_id': self.review_id,
            'review_type': self.review_type,
            'scope': self.scope,
            'created_at': self.created_at.isoformat(),
            'completed_at': datetime.now().isoformat(),
            'total_findings': len(self.findings),
            'issues_found': sum(1 for f in self.findings if f.get('issues')),
            'remediation_actions': count_remediation_actions(self.review_id),
            'status': self.status.value
        }
        
        # Save for compliance
        save_compliance_report(report)
        
        logger.info(f"Documented review {self.review_id}")

# Orchestrate full review
def run_quarterly_access_review():
    """Run quarterly access review."""
    
    review = AccessReview(
        review_id=generate_review_id(),
        review_type='user',
        scope='all_users'
    )
    
    # Step 1: Generate report
    review.generate_report()
    
    # Step 2: Assign to managers
    review.assign_reviewers()
    
    # Step 3: Wait for responses (async)
    # This would be handled by a separate job
    
    # Step 4: Remediate (after responses collected)
    # review.remediate_findings()
    
    # Step 5: Document
    # review.document_findings()
    
    return review
```

## 5. Access Review Questions

### Manager Review Checklist

```python
REVIEW_QUESTIONS = [
    {
        'question': 'Does this user still need access to this system?',
        'options': ['Yes', 'No', 'Unsure'],
        'action_if_no': 'revoke_all_access'
    },
    {
        'question': 'Is the current access level appropriate for their role?',
        'options': ['Yes', 'No - Too much', 'No - Too little'],
        'action_if_too_much': 'reduce_access',
        'action_if_too_little': 'escalate_to_security'
    },
    {
        'question': 'Has the user changed roles since access was granted?',
        'options': ['Yes', 'No'],
        'action_if_yes': 'review_access_for_new_role'
    },
    {
        'question': 'Is this a dormant account (no login in 90+ days)?',
        'options': ['Yes', 'No'],
        'action_if_yes': 'disable_account'
    },
    {
        'question': 'Are there any service accounts owned by this user?',
        'options': ['Yes', 'No', 'Unsure'],
        'action_if_yes': 'review_service_accounts'
    }
]

def generate_review_form(user_id):
    """Generate review form for manager."""
    
    user = get_user(user_id)
    access_summary = get_user_access_summary(user_id)
    
    form = {
        'user': {
            'id': user.id,
            'email': user.email,
            'role': user.role,
            'department': user.department,
            'manager': user.manager_email
        },
        'access_summary': access_summary,
        'questions': REVIEW_QUESTIONS,
        'recommendations': generate_recommendations(user_id)
    }
    
    return form

def generate_recommendations(user_id):
    """Generate automated recommendations."""
    
    recommendations = []
    
    user = get_user(user_id)
    
    # Dormant account
    if user.last_login_at and (datetime.now() - user.last_login_at).days > 90:
        recommendations.append({
            'type': 'disable_account',
            'reason': 'Account dormant for 90+ days',
            'severity': 'medium'
        })
    
    # Excessive permissions
    permissions = get_user_permissions(user_id)
    if len(permissions) > 20:
        recommendations.append({
            'type': 'review_permissions',
            'reason': f'User has {len(permissions)} permissions (above average)',
            'severity': 'low'
        })
    
    # Admin without MFA
    if 'admin' in user.role and not user.mfa_enabled:
        recommendations.append({
            'type': 'enable_mfa',
            'reason': 'Admin account without MFA',
            'severity': 'high'
        })
    
    return recommendations
```

## 6. Automation for Access Reviews

### Automated Access Report Generation

```python
def generate_automated_access_report():
    """Generate comprehensive access report."""
    
    report = {
        'generated_at': datetime.now().isoformat(),
        'summary': {
            'total_users': count_users(),
            'active_users': count_active_users(),
            'dormant_users': count_dormant_users(),
            'admin_users': count_admin_users(),
            'service_accounts': count_service_accounts()
        },
        'findings': {
            'users': audit_user_access(),
            'admins': audit_admin_access(),
            'service_accounts': audit_service_accounts(),
            'third_parties': audit_third_party_access()
        },
        'issues': {
            'critical': [],
            'high': [],
            'medium': [],
            'low': []
        }
    }
    
    # Categorize issues by severity
    for finding in report['findings']['users']:
        for issue in finding.get('issues', []):
            severity = classify_issue_severity(issue)
            report['issues'][severity].append({
                'user_id': finding['user_id'],
                'issue': issue
            })
    
    # Generate PDF report
    pdf_path = generate_pdf_report(report)
    
    # Send to stakeholders
    send_report_to_stakeholders(pdf_path)
    
    return report
```

### Manager Notifications

```python
def send_review_request(manager_email, review_id, findings):
    """Send access review request to manager."""
    
    # Generate review link
    review_link = f"https://app.company.com/access-review/{review_id}"
    
    # Email template
    email_body = f"""
    Hi,
    
    It's time for the quarterly access review. Please review the access rights 
    for your team members and confirm they are appropriate.
    
    Team members to review: {len(findings)}
    
    Review link: {review_link}
    
    Please complete by: {(datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')}
    
    If you have questions, contact security@company.com
    
    Thanks,
    Security Team
    """
    
    send_email(
        to=manager_email,
        subject=f"Action Required: Quarterly Access Review ({review_id})",
        body=email_body
    )
    
    logger.info(f"Sent review request to {manager_email}")
```

### Self-Service Access Requests

```python
class AccessRequest:
    """Self-service access request workflow."""
    
    def __init__(self, requester_id, resource, justification):
        self.request_id = generate_request_id()
        self.requester_id = requester_id
        self.resource = resource
        self.justification = justification
        self.status = 'pending'
        self.created_at = datetime.now()
    
    def submit(self):
        """Submit access request."""
        
        # Store request
        db.execute("""
            INSERT INTO access_requests (request_id, requester_id, resource, justification, status, created_at)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, [self.request_id, self.requester_id, self.resource, self.justification, self.status, self.created_at])
        
        # Route to approver
        approver = get_approver_for_resource(self.resource)
        
        send_approval_request(
            approver_email=approver,
            request_id=self.request_id,
            requester=get_user(self.requester_id).email,
            resource=self.resource,
            justification=self.justification
        )
        
        logger.info(f"Access request {self.request_id} submitted")
    
    def approve(self, approver_id):
        """Approve access request."""
        
        self.status = 'approved'
        
        # Grant access
        grant_access(
            user_id=self.requester_id,
            resource=self.resource
        )
        
        # Log approval
        log_access_grant(
            request_id=self.request_id,
            requester_id=self.requester_id,
            approver_id=approver_id,
            resource=self.resource
        )
        
        # Notify requester
        send_approval_notification(self.requester_id, self.resource)
        
        logger.info(f"Access request {self.request_id} approved by {approver_id}")
    
    def reject(self, approver_id, reason):
        """Reject access request."""
        
        self.status = 'rejected'
        
        # Log rejection
        log_access_rejection(
            request_id=self.request_id,
            requester_id=self.requester_id,
            approver_id=approver_id,
            reason=reason
        )
        
        # Notify requester
        send_rejection_notification(self.requester_id, reason)
        
        logger.info(f"Access request {self.request_id} rejected by {approver_id}")

# API endpoints
@app.route('/api/access/request', methods=['POST'])
def request_access():
    """Request access to resource."""
    
    requester_id = get_current_user_id()
    resource = request.json['resource']
    justification = request.json['justification']
    
    access_request = AccessRequest(requester_id, resource, justification)
    access_request.submit()
    
    return {'request_id': access_request.request_id}

@app.route('/api/access/approve/<request_id>', methods=['POST'])
def approve_access(request_id):
    """Approve access request."""
    
    approver_id = get_current_user_id()
    
    access_request = get_access_request(request_id)
    access_request.approve(approver_id)
    
    return {'status': 'approved'}
```

### Approval Workflows

```python
class ApprovalWorkflow:
    """Multi-level approval workflow."""
    
    def __init__(self, request_id, approvers):
        self.request_id = request_id
        self.approvers = approvers  # List of approver IDs
        self.current_approver_index = 0
        self.approvals = []
    
    def request_approval(self):
        """Request approval from current approver."""
        
        if self.current_approver_index >= len(self.approvers):
            # All approved
            self.finalize_approval()
            return
        
        current_approver = self.approvers[self.current_approver_index]
        
        send_approval_request(
            approver_id=current_approver,
            request_id=self.request_id
        )
    
    def approve(self, approver_id):
        """Record approval and move to next approver."""
        
        self.approvals.append({
            'approver_id': approver_id,
            'approved_at': datetime.now(),
            'decision': 'approved'
        })
        
        self.current_approver_index += 1
        
        # Request next approval
        self.request_approval()
    
    def reject(self, approver_id, reason):
        """Reject request (stops workflow)."""
        
        self.approvals.append({
            'approver_id': approver_id,
            'approved_at': datetime.now(),
            'decision': 'rejected',
            'reason': reason
        })
        
        # Notify requester
        notify_rejection(self.request_id, reason)
    
    def finalize_approval(self):
        """All approvals received, grant access."""
        
        access_request = get_access_request(self.request_id)
        
        grant_access(
            user_id=access_request.requester_id,
            resource=access_request.resource
        )
        
        notify_approval(self.request_id)

# Example: Two-level approval for admin access
def request_admin_access(user_id):
    """Request admin access (requires manager + security approval)."""
    
    manager = get_manager(user_id)
    security_lead = get_security_lead()
    
    workflow = ApprovalWorkflow(
        request_id=generate_request_id(),
        approvers=[manager, security_lead]
    )
    
    workflow.request_approval()
```

## 7. Access Logging and Monitoring

### Access Logging

```python
def log_access(user_id, resource, action, result):
    """Log access attempt."""
    
    db.execute("""
        INSERT INTO access_logs (user_id, resource, action, result, timestamp, ip_address, user_agent)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, [
        user_id,
        resource,
        action,
        result,
        datetime.now(),
        request.remote_addr,
        request.user_agent.string
    ])

# Middleware to log all access
@app.before_request
def log_request():
    """Log all requests."""
    
    if request.endpoint:
        log_access(
            user_id=get_current_user_id(),
            resource=request.endpoint,
            action=request.method,
            result='pending'
        )

@app.after_request
def log_response(response):
    """Log response."""
    
    update_access_log(
        user_id=get_current_user_id(),
        resource=request.endpoint,
        result=response.status_code
    )
    
    return response
```

### Failed Access Attempts

```python
def monitor_failed_access():
    """Monitor failed access attempts."""
    
    # Find users with multiple failed attempts
    failed_attempts = db.query("""
        SELECT user_id, COUNT(*) as failed_count
        FROM access_logs
        WHERE result IN (401, 403)
        AND timestamp > NOW() - INTERVAL '1 hour'
        GROUP BY user_id
        HAVING COUNT(*) >= 5
    """)
    
    for attempt in failed_attempts:
        # Alert security team
        alert_security_team(
            message=f"User {attempt['user_id']} has {attempt['failed_count']} failed access attempts in the last hour",
            severity='high'
        )
        
        # Consider locking account
        if attempt['failed_count'] >= 10:
            lock_account(attempt['user_id'])
```

### Privilege Escalations

```python
def monitor_privilege_escalations():
    """Monitor privilege escalation attempts."""
    
    # Find users who recently gained admin access
    recent_escalations = db.query("""
        SELECT user_id, old_role, new_role, changed_at, changed_by
        FROM role_changes
        WHERE new_role = 'admin'
        AND changed_at > NOW() - INTERVAL '24 hours'
    """)
    
    for escalation in recent_escalations:
        # Alert security team
        alert_security_team(
            message=f"User {escalation['user_id']} escalated from {escalation['old_role']} to {escalation['new_role']} by {escalation['changed_by']}",
            severity='high'
        )
        
        # Require justification
        require_escalation_justification(escalation['user_id'])
```

### After-Hours Access

```python
def monitor_after_hours_access():
    """Monitor access outside business hours."""
    
    # Define business hours (9 AM - 6 PM)
    business_hours_start = 9
    business_hours_end = 18
    
    # Find after-hours access
    after_hours_access = db.query("""
        SELECT user_id, resource, timestamp
        FROM access_logs
        WHERE EXTRACT(HOUR FROM timestamp) < %s
           OR EXTRACT(HOUR FROM timestamp) > %s
        AND timestamp > NOW() - INTERVAL '24 hours'
    """, [business_hours_start, business_hours_end])
    
    for access in after_hours_access:
        # Log for review
        log_after_hours_access(access)
        
        # Alert if accessing sensitive resources
        if is_sensitive_resource(access['resource']):
            alert_security_team(
                message=f"User {access['user_id']} accessed {access['resource']} after hours at {access['timestamp']}",
                severity='medium'
            )
```

### Geographic Anomalies

```python
import geoip2.database

def monitor_geographic_anomalies():
    """Monitor access from unusual locations."""
    
    reader = geoip2.database.Reader('GeoLite2-City.mmdb')
    
    # Get recent access logs
    recent_access = db.query("""
        SELECT user_id, ip_address, timestamp
        FROM access_logs
        WHERE timestamp > NOW() - INTERVAL '1 hour'
    """)
    
    for access in recent_access:
        # Get location from IP
        try:
            response = reader.city(access['ip_address'])
            country = response.country.name
            city = response.city.name
        except:
            continue
        
        # Get user's usual location
        usual_location = get_usual_location(access['user_id'])
        
        # Check if anomalous
        if country != usual_location['country']:
            alert_security_team(
                message=f"User {access['user_id']} accessed from {city}, {country} (usual: {usual_location['city']}, {usual_location['country']})",
                severity='high'
            )
            
            # Require additional authentication
            require_step_up_auth(access['user_id'])
```

## 8. Tools for Access Auditing

### AWS IAM Access Analyzer

```python
import boto3

def analyze_iam_access():
    """Analyze IAM access using AWS Access Analyzer."""
    
    analyzer = boto3.client('accessanalyzer')
    
    # Create analyzer
    analyzer.create_analyzer(
        analyzerName='access-audit',
        type='ACCOUNT'
    )
    
    # Get findings
    findings = analyzer.list_findings(
        analyzerArn='arn:aws:access-analyzer:us-east-1:123456789012:analyzer/access-audit'
    )
    
    for finding in findings['findings']:
        print(f"Resource: {finding['resource']}")
        print(f"Principal: {finding['principal']}")
        print(f"Action: {finding['action']}")
        print(f"Condition: {finding.get('condition', 'None')}")
        print()
```

### GCP Access Transparency

```python
from google.cloud import logging_v2

def analyze_gcp_access():
    """Analyze GCP access using Access Transparency logs."""
    
    client = logging_v2.Client()
    
    # Query Access Transparency logs
    filter_str = 'protoPayload.serviceName="cloudaudit.googleapis.com"'
    
    for entry in client.list_entries(filter_=filter_str):
        print(f"Principal: {entry.payload['authenticationInfo']['principalEmail']}")
        print(f"Resource: {entry.payload['resourceName']}")
        print(f"Method: {entry.payload['methodName']}")
        print()
```

### Azure AD Access Reviews

```python
from azure.identity import DefaultAzureCredential
from azure.mgmt.authorization import AuthorizationManagementClient

def analyze_azure_access():
    """Analyze Azure access using Azure AD Access Reviews."""
    
    credential = DefaultAzureCredential()
    client = AuthorizationManagementClient(credential, subscription_id)
    
    # List role assignments
    role_assignments = client.role_assignments.list()
    
    for assignment in role_assignments:
        print(f"Principal: {assignment.principal_id}")
        print(f"Role: {assignment.role_definition_id}")
        print(f"Scope: {assignment.scope}")
        print()
```

### Database Audit Logs

**PostgreSQL**:
```sql
-- Enable audit logging
ALTER SYSTEM SET log_connections = 'on';
ALTER SYSTEM SET log_disconnections = 'on';
ALTER SYSTEM SET log_statement = 'all';

-- Query audit logs
SELECT 
    usename,
    datname,
    client_addr,
    backend_start,
    state,
    query
FROM pg_stat_activity
WHERE state = 'active';
```

**MySQL**:
```sql
-- Enable audit plugin
INSTALL PLUGIN audit_log SONAME 'audit_log.so';

-- Query audit log
SELECT * FROM mysql.general_log
WHERE command_type = 'Query'
ORDER BY event_time DESC
LIMIT 100;
```

## 9. Access Anomaly Detection

### Unusual Access Patterns

```python
from sklearn.ensemble import IsolationForest
import numpy as np

def detect_access_anomalies():
    """Detect unusual access patterns using ML."""
    
    # Get access logs
    access_logs = db.query("""
        SELECT 
            user_id,
            EXTRACT(HOUR FROM timestamp) as hour,
            EXTRACT(DOW FROM timestamp) as day_of_week,
            COUNT(*) as access_count
        FROM access_logs
        WHERE timestamp > NOW() - INTERVAL '30 days'
        GROUP BY user_id, hour, day_of_week
    """)
    
    # Prepare features
    X = np.array([
        [log['hour'], log['day_of_week'], log['access_count']]
        for log in access_logs
    ])
    
    # Train anomaly detector
    clf = IsolationForest(contamination=0.1)
    clf.fit(X)
    
    # Predict anomalies
    predictions = clf.predict(X)
    
    # Alert on anomalies
    for i, prediction in enumerate(predictions):
        if prediction == -1:  # Anomaly
            log = access_logs[i]
            alert_security_team(
                message=f"Anomalous access pattern detected for user {log['user_id']}",
                severity='medium'
            )
```

### Access from New Locations

```python
def detect_new_location_access():
    """Detect access from new geographic locations."""
    
    # Get recent access
    recent_access = db.query("""
        SELECT user_id, ip_address, timestamp
        FROM access_logs
        WHERE timestamp > NOW() - INTERVAL '24 hours'
    """)
    
    for access in recent_access:
        # Get location
        location = get_location_from_ip(access['ip_address'])
        
        # Check if new location
        known_locations = get_known_locations(access['user_id'])
        
        if location not in known_locations:
            # New location
            alert_user(
                user_id=access['user_id'],
                message=f"New login from {location['city']}, {location['country']}",
                severity='medium'
            )
            
            # Require additional verification
            require_email_verification(access['user_id'])
```

### Bulk Data Downloads

```python
def detect_bulk_downloads():
    """Detect unusual bulk data downloads."""
    
    # Find users downloading large amounts of data
    bulk_downloads = db.query("""
        SELECT 
            user_id,
            SUM(bytes_downloaded) as total_bytes,
            COUNT(*) as download_count
        FROM download_logs
        WHERE timestamp > NOW() - INTERVAL '1 hour'
        GROUP BY user_id
        HAVING SUM(bytes_downloaded) > 1000000000  -- 1GB
    """)
    
    for download in bulk_downloads:
        alert_security_team(
            message=f"User {download['user_id']} downloaded {download['total_bytes']} bytes in the last hour ({download['download_count']} files)",
            severity='high'
        )
        
        # Consider blocking user
        if download['total_bytes'] > 10000000000:  # 10GB
            block_user(download['user_id'])
```

## 10. Remediation Workflows

### Revoke Excessive Access

```python
def revoke_excessive_access(user_id, permissions_to_revoke):
    """Revoke excessive permissions."""
    
    for permission in permissions_to_revoke:
        # Revoke permission
        db.execute("""
            DELETE FROM user_permissions
            WHERE user_id = %s AND permission = %s
        """, [user_id, permission])
        
        # Log revocation
        log_access_revocation(
            user_id=user_id,
            permission=permission,
            reason='Excessive access identified in quarterly review'
        )
    
    # Notify user
    send_access_revocation_notification(user_id, permissions_to_revoke)
    
    logger.info(f"Revoked {len(permissions_to_revoke)} permissions from user {user_id}")
```

### Disable Dormant Accounts

```python
def disable_dormant_accounts():
    """Disable accounts inactive for 90+ days."""
    
    cutoff = datetime.now() - timedelta(days=90)
    
    dormant_accounts = db.query("""
        SELECT id, email, last_login_at
        FROM users
        WHERE last_login_at < %s
        AND status = 'active'
    """, [cutoff])
    
    for account in dormant_accounts:
        # Warn user first
        send_dormant_account_warning(account['id'])
        
        # Disable after 7 days if still inactive
        schedule_account_disable(
            user_id=account['id'],
            disable_date=datetime.now() + timedelta(days=7)
        )
```

### Rotate Compromised Credentials

```python
def rotate_compromised_credentials(user_id):
    """Rotate credentials for potentially compromised account."""
    
    # Invalidate all sessions
    invalidate_all_sessions(user_id)
    
    # Revoke API keys
    revoke_all_api_keys(user_id)
    
    # Force password reset
    force_password_reset(user_id)
    
    # Require MFA setup
    require_mfa_setup(user_id)
    
    # Notify user
    send_security_alert(
        user_id=user_id,
        message="Your account credentials have been rotated due to suspicious activity"
    )
    
    logger.info(f"Rotated credentials for user {user_id}")
```

## 11. Segregation of Duties (SoD)

### SoD Policies

```python
SOD_POLICIES = [
    {
        'name': 'No single person can deploy to production',
        'conflicting_roles': ['developer', 'deployer'],
        'enforcement': 'strict'
    },
    {
        'name': 'Separate dev and prod access',
        'conflicting_resources': ['dev_database', 'prod_database'],
        'enforcement': 'strict'
    },
    {
        'name': 'Multi-person approval for critical changes',
        'critical_actions': ['delete_user', 'modify_permissions', 'deploy_production'],
        'required_approvers': 2,
        'enforcement': 'strict'
    }
]

def check_sod_violations(user_id):
    """Check for segregation of duties violations."""
    
    violations = []
    
    user_roles = get_user_roles(user_id)
    user_resources = get_user_resources(user_id)
    
    for policy in SOD_POLICIES:
        # Check conflicting roles
        if 'conflicting_roles' in policy:
            conflicting = set(policy['conflicting_roles']) & set(user_roles)
            if len(conflicting) > 1:
                violations.append({
                    'policy': policy['name'],
                    'violation': f"User has conflicting roles: {conflicting}"
                })
        
        # Check conflicting resources
        if 'conflicting_resources' in policy:
            conflicting = set(policy['conflicting_resources']) & set(user_resources)
            if len(conflicting) > 1:
                violations.append({
                    'policy': policy['name'],
                    'violation': f"User has access to conflicting resources: {conflicting}"
                })
    
    return violations
```

## 12. Audit Reporting

### Access Review Summary

```python
def generate_access_review_summary(review_id):
    """Generate summary of access review."""
    
    review = get_access_review(review_id)
    
    summary = {
        'review_id': review_id,
        'review_type': review.review_type,
        'start_date': review.created_at.isoformat(),
        'end_date': review.completed_at.isoformat() if review.completed_at else None,
        'status': review.status.value,
        'statistics': {
            'total_users_reviewed': len(review.findings),
            'issues_found': sum(1 for f in review.findings if f.get('issues')),
            'access_revoked': count_revocations(review_id),
            'access_modified': count_modifications(review_id),
            'access_approved': count_approvals(review_id)
        },
        'top_issues': get_top_issues(review.findings),
        'remediation_actions': get_remediation_actions(review_id)
    }
    
    return summary
```

### Compliance Dashboard

```python
def generate_compliance_dashboard():
    """Generate compliance dashboard."""
    
    dashboard = {
        'last_review_date': get_last_review_date(),
        'next_review_date': get_next_review_date(),
        'compliance_status': {
            'soc2': check_soc2_compliance(),
            'iso27001': check_iso27001_compliance(),
            'hipaa': check_hipaa_compliance()
        },
        'metrics': {
            'users_with_mfa': count_users_with_mfa(),
            'dormant_accounts': count_dormant_accounts(),
            'excessive_permissions': count_excessive_permissions(),
            'sod_violations': count_sod_violations()
        },
        'recent_findings': get_recent_audit_findings(days=30),
        'remediation_progress': get_remediation_progress()
    }
    
    return dashboard
```

## Best Practices

1. **Regular Reviews**: Quarterly for users, monthly for admins
2. **Automate Detection**: Use tools to identify anomalies
3. **Least Privilege**: Grant minimum necessary access
4. **Segregation of Duties**: No single person has complete control
5. **Audit Logging**: Log all access attempts
6. **Manager Accountability**: Managers certify team access
7. **Service Account Hygiene**: Review and rotate regularly
8. **Third-Party Audits**: Review vendor access quarterly
9. **Remediate Promptly**: Fix issues within 30 days
10. **Document Everything**: Maintain audit trail for compliance

## Common Pitfalls

- **Infrequent Reviews**: Annual reviews miss issues
- **No Follow-Up**: Findings identified but not remediated
- **Manual Processes**: Error-prone and time-consuming
- **No Service Account Review**: Forgotten and over-privileged
- **Ignoring Third Parties**: Vendors have excessive access
- **No Anomaly Detection**: Insider threats go unnoticed
- **Poor Documentation**: Can't prove compliance

## Summary

Implement regular access audits and reviews to ensure least privilege, detect insider threats, and maintain compliance with SOC2, ISO 27001, and HIPAA. Automate access report generation, use anomaly detection for unusual patterns, and enforce segregation of duties. Document all findings and remediate promptly.
