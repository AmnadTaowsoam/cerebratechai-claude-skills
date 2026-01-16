---
name: PII Detection
description: Comprehensive guide to detecting Personally Identifiable Information (PII) across systems, databases, and logs using regex patterns, NER models, and automated scanning tools.
---

# PII Detection

## Overview

Personally Identifiable Information (PII) detection is the process of identifying data that can be used to identify, contact, or locate an individual. Effective PII detection is critical for:

- **Compliance**: GDPR, CCPA, PDPA, HIPAA requirements
- **Security**: Preventing data breaches and unauthorized access
- **Privacy**: Protecting user information
- **Risk Management**: Understanding what sensitive data you have and where

## 1. What is PII (Legal Definitions)

### GDPR Definition (EU)

**Personal Data**: Any information relating to an identified or identifiable natural person ('data subject').

**Identifiable Person**: One who can be identified, directly or indirectly, by reference to:
- Name
- Identification number
- Location data
- Online identifier (IP address, cookie ID)
- Physical, physiological, genetic, mental, economic, cultural, or social identity factors

**Special Categories** (Article 9 - requires explicit consent):
- Racial or ethnic origin
- Political opinions
- Religious or philosophical beliefs
- Trade union membership
- Genetic data
- Biometric data (for unique identification)
- Health data
- Sex life or sexual orientation

### CCPA Definition (California)

**Personal Information**: Information that identifies, relates to, describes, is reasonably capable of being associated with, or could reasonably be linked with a particular consumer or household.

**Categories**:
- Identifiers (name, alias, postal address, unique personal identifier, online identifier, IP address, email, account name, SSN, driver's license, passport)
- Commercial information (purchase history, tendencies)
- Biometric information
- Internet or network activity
- Geolocation data
- Audio, electronic, visual, thermal, olfactory, or similar information
- Professional or employment-related information
- Education information
- Inferences (preferences, characteristics, behavior)

### PDPA Definition (Thailand)

**Personal Data**: Information relating to a person which enables identification of such person (similar to GDPR).

**Sensitive Personal Data**:
- Racial or ethnic origin
- Political opinions
- Religious or philosophical beliefs
- Sexual behavior
- Criminal records
- Health data
- Disability
- Trade union information
- Genetic data
- Biometric data

### HIPAA PHI (Healthcare)

**Protected Health Information (PHI)**: Individually identifiable health information held or transmitted by a covered entity or business associate.

**18 HIPAA Identifiers**:
1. Names
2. Geographic subdivisions smaller than state
3. Dates (birth, admission, discharge, death, age >89)
4. Telephone numbers
5. Fax numbers
6. Email addresses
7. Social Security numbers
8. Medical record numbers
9. Health plan beneficiary numbers
10. Account numbers
11. Certificate/license numbers
12. Vehicle identifiers and serial numbers
13. Device identifiers and serial numbers
14. Web URLs
15. IP addresses
16. Biometric identifiers (fingerprints, voiceprints)
17. Full-face photos
18. Any other unique identifying number, characteristic, or code

## 2. Types of PII

### Direct Identifiers

Information that directly identifies an individual:

```
- Full name: "John Michael Smith"
- Government ID: SSN, passport number, national ID
- Email address: john.smith@example.com
- Phone number: +1-555-123-4567
- Physical address: "123 Main St, Apt 4B, New York, NY 10001"
- Driver's license number
- Passport number
- Biometric data: Fingerprints, facial recognition, iris scans
- Medical record number
- Financial account numbers
```

### Indirect Identifiers

Information that can identify someone when combined:

```
- IP address: 192.168.1.100
- Device ID: IMEI, MAC address
- Cookie ID: session tokens, tracking cookies
- Username: john_smith_1985
- Geolocation: GPS coordinates, check-ins
- Browser fingerprint
- User agent string
- Demographic data: Age + ZIP code + Gender
```

### Sensitive PII

High-risk information requiring extra protection:

```
- Health information: Diagnoses, medications, lab results
- Financial data: Credit card numbers, bank accounts, salary
- Biometric data: Fingerprints, retina scans, voice prints
- Political opinions: Party affiliation, voting records
- Religious beliefs
- Sexual orientation
- Genetic information
- Criminal history
- Children's data (COPPA - under 13)
```

### Quasi-Identifiers

Attributes that don't identify alone but can in combination:

```
Example: 87% of US population can be uniquely identified by:
- ZIP code
- Birth date
- Gender

Other quasi-identifiers:
- Age + City
- Job title + Company + Location
- Education level + Employer + City
- Rare disease + Geographic region
```

## 3. Domain-Specific PII

### Financial Domain

```
- Credit card numbers (PAN): 4532-1234-5678-9010
- CVV/CVC: 123
- Bank account numbers
- Routing numbers (ABA): 021000021
- IBAN: GB82 WEST 1234 5698 7654 32
- SWIFT/BIC codes
- Transaction history
- Credit scores
- Investment portfolios
- Tax identification numbers
```

### Healthcare Domain

```
- Medical record numbers (MRN)
- Patient identifiers
- Diagnoses (ICD-10 codes)
- Prescriptions and medications
- Lab results
- Insurance policy numbers
- Provider identifiers (NPI)
- Treatment plans
- Genetic test results
- Mental health records
```

### HR/Employment Domain

```
- Employee ID numbers
- Salary and compensation
- Performance reviews
- Disciplinary records
- Background check results
- Resume/CV data
- Emergency contacts
- Benefit elections
- Time and attendance records
- Termination reasons
```

### E-commerce Domain

```
- Purchase history
- Payment methods on file
- Shipping addresses
- Wish lists
- Product reviews (with user info)
- Browsing history
- Cart abandonment data
- Loyalty program numbers
- Gift recipient information
```

## 4. PII Detection Methods

### Regex Patterns

Fast, deterministic pattern matching for structured PII:

```python
import re

# Email detection
EMAIL_PATTERN = r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b'

# US Phone number (multiple formats)
PHONE_PATTERNS = [
    r'\b\d{3}-\d{3}-\d{4}\b',           # 555-123-4567
    r'\b\(\d{3}\)\s*\d{3}-\d{4}\b',     # (555) 123-4567
    r'\b\d{3}\.\d{3}\.\d{4}\b',         # 555.123.4567
    r'\b\d{10}\b',                       # 5551234567
]

# US Social Security Number
SSN_PATTERN = r'\b\d{3}-\d{2}-\d{4}\b'

# Credit card (basic - use Luhn for validation)
CC_PATTERN = r'\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b'

# IPv4 address
IPV4_PATTERN = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'

# Thai National ID (13 digits with checksum)
THAI_ID_PATTERN = r'\b\d{1}-\d{4}-\d{5}-\d{2}-\d{1}\b'

def detect_pii_regex(text):
    """Detect PII using regex patterns."""
    findings = []
    
    # Email
    for match in re.finditer(EMAIL_PATTERN, text):
        findings.append({
            'type': 'EMAIL',
            'value': match.group(),
            'start': match.start(),
            'end': match.end()
        })
    
    # Phone numbers
    for pattern in PHONE_PATTERNS:
        for match in re.finditer(pattern, text):
            findings.append({
                'type': 'PHONE',
                'value': match.group(),
                'start': match.start(),
                'end': match.end()
            })
    
    # SSN
    for match in re.finditer(SSN_PATTERN, text):
        findings.append({
            'type': 'SSN',
            'value': match.group(),
            'start': match.start(),
            'end': match.end()
        })
    
    return findings
```

### Named Entity Recognition (NER)

ML-based detection for unstructured text:

```python
import spacy

# Load pre-trained NER model
nlp = spacy.load("en_core_web_sm")

def detect_pii_ner(text):
    """Detect PII using NER."""
    doc = nlp(text)
    findings = []
    
    for ent in doc.ents:
        if ent.label_ in ['PERSON', 'GPE', 'ORG', 'DATE', 'MONEY']:
            findings.append({
                'type': ent.label_,
                'value': ent.text,
                'start': ent.start_char,
                'end': ent.end_char,
                'confidence': 0.85  # Model-dependent
            })
    
    return findings

# Example
text = "John Smith lives in New York and works at Acme Corp. His email is john@acme.com."
entities = detect_pii_ner(text)
# [
#   {'type': 'PERSON', 'value': 'John Smith', ...},
#   {'type': 'GPE', 'value': 'New York', ...},
#   {'type': 'ORG', 'value': 'Acme Corp', ...}
# ]
```

### Dictionary Matching

Lookup-based detection for known PII values:

```python
class DictionaryMatcher:
    def __init__(self):
        self.known_names = set(['john smith', 'jane doe', ...])
        self.known_emails = set(['john@example.com', ...])
    
    def detect(self, text):
        text_lower = text.lower()
        findings = []
        
        for name in self.known_names:
            if name in text_lower:
                findings.append({
                    'type': 'KNOWN_NAME',
                    'value': name,
                    'method': 'dictionary'
                })
        
        return findings
```

### Statistical Detection

Entropy and pattern analysis:

```python
import math
from collections import Counter

def calculate_entropy(s):
    """Calculate Shannon entropy of a string."""
    if not s:
        return 0
    
    counts = Counter(s)
    length = len(s)
    
    entropy = -sum(
        (count / length) * math.log2(count / length)
        for count in counts.values()
    )
    
    return entropy

def is_likely_identifier(value):
    """Detect if a value is likely a unique identifier."""
    # High entropy suggests random/unique value
    entropy = calculate_entropy(value)
    
    # Heuristics
    has_numbers = any(c.isdigit() for c in value)
    has_special = any(not c.isalnum() for c in value)
    length = len(value)
    
    # Example: UUID-like, session tokens
    if entropy > 3.5 and length > 16 and has_numbers:
        return True
    
    return False

# Example
print(is_likely_identifier("a1b2c3d4-e5f6-7890"))  # True
print(is_likely_identifier("hello"))               # False
```

### ML-Based Classification

Train custom models for domain-specific PII:

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer

class PIIClassifier:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        self.classifier = RandomForestClassifier()
    
    def train(self, texts, labels):
        """Train on labeled examples."""
        X = self.vectorizer.fit_transform(texts)
        self.classifier.fit(X, labels)
    
    def predict(self, text):
        """Predict if text contains PII."""
        X = self.vectorizer.transform([text])
        return self.classifier.predict(X)[0]

# Training data
texts = [
    "My email is john@example.com",      # PII
    "The weather is nice today",         # Not PII
    "Call me at 555-1234",               # PII
    "I like pizza",                      # Not PII
]
labels = [1, 0, 1, 0]

clf = PIIClassifier()
clf.train(texts, labels)

# Predict
print(clf.predict("My phone is 555-9999"))  # 1 (PII)
```

## 5. Tools and Libraries

### Python Libraries

#### Microsoft Presidio

```python
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine

# Initialize
analyzer = AnalyzerEngine()
anonymizer = AnonymizerEngine()

# Analyze
text = "My name is John and my email is john@example.com"
results = analyzer.analyze(
    text=text,
    language='en',
    entities=['PERSON', 'EMAIL_ADDRESS', 'PHONE_NUMBER']
)

# Results
for result in results:
    print(f"Type: {result.entity_type}")
    print(f"Text: {text[result.start:result.end]}")
    print(f"Score: {result.score}")

# Anonymize
anonymized = anonymizer.anonymize(
    text=text,
    analyzer_results=results
)
print(anonymized.text)  # "My name is <PERSON> and my email is <EMAIL_ADDRESS>"
```

#### scrubadub

```python
import scrubadub

text = "My name is John Smith and my phone is 555-123-4567"

# Auto-detect and scrub
cleaned = scrubadub.clean(text)
print(cleaned)  # "My name is {{NAME}} and my phone is {{PHONE}}"

# Custom detectors
class CustomDetector(scrubadub.detectors.Detector):
    def iter_filth(self, text):
        # Custom detection logic
        pass
```

#### piicatcher

```bash
# Scan databases for PII
piicatcher --scan-type deep --connection-string "postgresql://user:pass@localhost/db"
```

### Cloud Services

#### AWS Macie

```python
import boto3

macie = boto3.client('macie2')

# Create classification job
response = macie.create_classification_job(
    s3JobDefinition={
        'bucketDefinitions': [{
            'accountId': '123456789012',
            'buckets': ['my-bucket']
        }]
    },
    jobType='ONE_TIME',
    name='PII-Scan-Job'
)

# Get findings
findings = macie.list_findings(
    findingCriteria={
        'criterion': {
            'category': {'eq': ['SENSITIVE_DATA']}
        }
    }
)
```

#### GCP DLP API

```python
from google.cloud import dlp_v2

dlp = dlp_v2.DlpServiceClient()

# Inspect content
item = {'value': 'My SSN is 123-45-6789'}

inspect_config = {
    'info_types': [
        {'name': 'US_SOCIAL_SECURITY_NUMBER'},
        {'name': 'EMAIL_ADDRESS'},
        {'name': 'PHONE_NUMBER'}
    ]
}

response = dlp.inspect_content(
    request={
        'parent': f'projects/{project_id}',
        'inspect_config': inspect_config,
        'item': item
    }
)

for finding in response.result.findings:
    print(f'Type: {finding.info_type.name}')
    print(f'Likelihood: {finding.likelihood}')
```

#### Azure Purview

```python
from azure.purview.scanning import PurviewScanningClient

client = PurviewScanningClient(endpoint, credential)

# Create scan
scan = client.scans.create_or_update(
    data_source_name="AzureSQL",
    scan_name="pii-scan",
    body={
        "kind": "AzureSqlDatabaseCredential",
        "properties": {
            "scanRulesetName": "AzureSqlDatabase",
            "scanRulesetType": "System"
        }
    }
)
```

## 6. Detection Patterns

### Email Validation

```python
import re

def validate_email(email):
    """Comprehensive email validation."""
    # RFC 5322 simplified
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if not re.match(pattern, email):
        return False
    
    # Additional checks
    local, domain = email.split('@')
    
    # Local part checks
    if len(local) > 64:
        return False
    if local.startswith('.') or local.endswith('.'):
        return False
    if '..' in local:
        return False
    
    # Domain checks
    if len(domain) > 255:
        return False
    
    return True
```

### Phone Number Detection

```python
import phonenumbers

def detect_phone_numbers(text):
    """Detect phone numbers with international support."""
    findings = []
    
    # Try to parse with default region
    for match in phonenumbers.PhoneNumberMatcher(text, "US"):
        findings.append({
            'type': 'PHONE',
            'value': phonenumbers.format_number(
                match.number,
                phonenumbers.PhoneNumberFormat.E164
            ),
            'country': phonenumbers.region_code_for_number(match.number),
            'valid': phonenumbers.is_valid_number(match.number)
        })
    
    return findings

# Example
text = "Call me at +1-555-123-4567 or (555) 987-6543"
phones = detect_phone_numbers(text)
```

### Credit Card Detection with Luhn

```python
def luhn_checksum(card_number):
    """Calculate Luhn checksum."""
    def digits_of(n):
        return [int(d) for d in str(n)]
    
    digits = digits_of(card_number)
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    
    checksum = sum(odd_digits)
    for d in even_digits:
        checksum += sum(digits_of(d * 2))
    
    return checksum % 10

def is_valid_credit_card(card_number):
    """Validate credit card using Luhn algorithm."""
    # Remove spaces and dashes
    card_number = card_number.replace(' ', '').replace('-', '')
    
    # Must be digits only
    if not card_number.isdigit():
        return False
    
    # Length check (13-19 digits)
    if not 13 <= len(card_number) <= 19:
        return False
    
    # Luhn check
    return luhn_checksum(card_number) == 0

def detect_credit_cards(text):
    """Detect and validate credit card numbers."""
    pattern = r'\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b'
    findings = []
    
    for match in re.finditer(pattern, text):
        card = match.group()
        if is_valid_credit_card(card):
            # Determine card type
            first_digit = card[0]
            card_type = {
                '4': 'Visa',
                '5': 'Mastercard',
                '3': 'Amex',
                '6': 'Discover'
            }.get(first_digit, 'Unknown')
            
            findings.append({
                'type': 'CREDIT_CARD',
                'value': card,
                'card_type': card_type,
                'valid': True
            })
    
    return findings
```

### SSN Detection

```python
def is_valid_ssn(ssn):
    """Validate US Social Security Number."""
    # Remove dashes
    ssn_clean = ssn.replace('-', '')
    
    # Must be 9 digits
    if not ssn_clean.isdigit() or len(ssn_clean) != 9:
        return False
    
    # Invalid SSN patterns
    area = ssn_clean[:3]
    group = ssn_clean[3:5]
    serial = ssn_clean[5:]
    
    # Area cannot be 000, 666, or 900-999
    if area in ['000', '666'] or area.startswith('9'):
        return False
    
    # Group cannot be 00
    if group == '00':
        return False
    
    # Serial cannot be 0000
    if serial == '0000':
        return False
    
    return True

def detect_ssn(text):
    """Detect US Social Security Numbers."""
    pattern = r'\b\d{3}-\d{2}-\d{4}\b'
    findings = []
    
    for match in re.finditer(pattern, text):
        ssn = match.group()
        if is_valid_ssn(ssn):
            findings.append({
                'type': 'SSN',
                'value': ssn,
                'valid': True
            })
    
    return findings
```

### Thai National ID

```python
def validate_thai_id(id_number):
    """Validate Thai National ID with checksum."""
    # Remove dashes
    id_clean = id_number.replace('-', '')
    
    if not id_clean.isdigit() or len(id_clean) != 13:
        return False
    
    # Calculate checksum
    total = sum(
        int(id_clean[i]) * (13 - i)
        for i in range(12)
    )
    
    check_digit = (11 - (total % 11)) % 10
    
    return int(id_clean[12]) == check_digit
```

## 7. Context-Aware Detection

### Field Name Hints

```python
def detect_pii_with_context(field_name, value):
    """Use field names to improve detection accuracy."""
    field_lower = field_name.lower()
    
    # Email fields
    if any(keyword in field_lower for keyword in ['email', 'e-mail', 'mail']):
        if '@' in value:
            return {'type': 'EMAIL', 'confidence': 0.95}
    
    # Phone fields
    if any(keyword in field_lower for keyword in ['phone', 'tel', 'mobile', 'cell']):
        if re.match(r'\d{3}[-.]?\d{3}[-.]?\d{4}', value):
            return {'type': 'PHONE', 'confidence': 0.90}
    
    # Name fields
    if any(keyword in field_lower for keyword in ['name', 'full_name', 'firstname', 'lastname']):
        if value.replace(' ', '').isalpha():
            return {'type': 'NAME', 'confidence': 0.85}
    
    # Address fields
    if 'address' in field_lower:
        return {'type': 'ADDRESS', 'confidence': 0.80}
    
    # Fallback to pattern matching
    return detect_pii_regex(value)
```

### Contextual Analysis

```python
def analyze_with_context(text):
    """Analyze text with surrounding context."""
    findings = []
    
    # Look for patterns like "My email is X" or "Contact: X"
    email_contexts = [
        r'email\s*(?:is|:)?\s*([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})',
        r'contact\s*(?:me\s*)?(?:at|:)?\s*([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})',
    ]
    
    for pattern in email_contexts:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            findings.append({
                'type': 'EMAIL',
                'value': match.group(1),
                'confidence': 0.95,  # Higher confidence due to context
                'context': match.group(0)
            })
    
    return findings
```

## 8. False Positive Handling

### Allowlists

```python
class PIIDetectorWithAllowlist:
    def __init__(self):
        self.email_allowlist = {
            'test@example.com',
            'noreply@company.com',
            'admin@localhost',
        }
        
        self.phone_allowlist = {
            '555-555-5555',  # Common test number
            '000-000-0000',
        }
        
        self.cc_allowlist = {
            '4111111111111111',  # Test Visa
            '5555555555554444',  # Test Mastercard
        }
    
    def detect(self, text):
        findings = detect_pii_regex(text)
        
        # Filter out allowlisted values
        filtered = []
        for finding in findings:
            if finding['type'] == 'EMAIL' and finding['value'] in self.email_allowlist:
                continue
            if finding['type'] == 'PHONE' and finding['value'] in self.phone_allowlist:
                continue
            if finding['type'] == 'CREDIT_CARD' and finding['value'].replace('-', '').replace(' ', '') in self.cc_allowlist:
                continue
            
            filtered.append(finding)
        
        return filtered
```

### Test Data Detection

```python
def is_test_data(value, value_type):
    """Detect if value is likely test data."""
    value_clean = value.lower().replace(' ', '').replace('-', '')
    
    # Test emails
    if value_type == 'EMAIL':
        test_domains = ['example.com', 'test.com', 'localhost', 'example.org']
        domain = value.split('@')[1] if '@' in value else ''
        if any(test_domain in domain for test_domain in test_domains):
            return True
    
    # Test credit cards
    if value_type == 'CREDIT_CARD':
        # All same digit
        if len(set(value_clean)) == 1:
            return True
        # Known test cards
        if value_clean in ['4111111111111111', '5555555555554444']:
            return True
    
    # Test phones
    if value_type == 'PHONE':
        if value_clean in ['5555555555', '0000000000']:
            return True
    
    return False
```

## 9. Scanning Strategies

### Database Scanning

```python
import psycopg2
from presidio_analyzer import AnalyzerEngine

def scan_database_table(connection_string, table_name, sample_size=1000):
    """Scan a database table for PII."""
    analyzer = AnalyzerEngine()
    conn = psycopg2.connect(connection_string)
    cursor = conn.cursor()
    
    # Get column names
    cursor.execute(f"""
        SELECT column_name, data_type
        FROM information_schema.columns
        WHERE table_name = '{table_name}'
    """)
    columns = cursor.fetchall()
    
    findings = {}
    
    for column_name, data_type in columns:
        # Skip non-text columns
        if data_type not in ['text', 'varchar', 'char']:
            continue
        
        # Sample data
        cursor.execute(f"""
            SELECT DISTINCT "{column_name}"
            FROM "{table_name}"
            WHERE "{column_name}" IS NOT NULL
            LIMIT {sample_size}
        """)
        
        samples = [row[0] for row in cursor.fetchall()]
        
        # Analyze samples
        pii_found = []
        for sample in samples:
            results = analyzer.analyze(text=str(sample), language='en')
            if results:
                pii_found.extend([r.entity_type for r in results])
        
        if pii_found:
            findings[column_name] = {
                'pii_types': list(set(pii_found)),
                'sample_count': len(samples),
                'pii_count': len(pii_found)
            }
    
    conn.close()
    return findings

# Usage
findings = scan_database_table(
    "postgresql://user:pass@localhost/mydb",
    "users"
)
print(findings)
# {
#   'email': {'pii_types': ['EMAIL_ADDRESS'], 'sample_count': 1000, 'pii_count': 950},
#   'phone': {'pii_types': ['PHONE_NUMBER'], 'sample_count': 800, 'pii_count': 750}
# }
```

### Log File Scanning

```python
import gzip
import json

def scan_log_file(log_path, max_lines=10000):
    """Scan log file for PII."""
    analyzer = AnalyzerEngine()
    findings = []
    
    # Handle gzipped logs
    open_func = gzip.open if log_path.endswith('.gz') else open
    
    with open_func(log_path, 'rt') as f:
        for i, line in enumerate(f):
            if i >= max_lines:
                break
            
            # Parse JSON logs
            try:
                log_entry = json.loads(line)
                text = json.dumps(log_entry)
            except:
                text = line
            
            # Analyze
            results = analyzer.analyze(text=text, language='en')
            
            if results:
                findings.append({
                    'line_number': i + 1,
                    'pii_types': [r.entity_type for r in results],
                    'snippet': text[:100]
                })
    
    return findings
```

### S3 Bucket Scanning

```python
import boto3

def scan_s3_bucket(bucket_name, prefix='', max_files=100):
    """Scan S3 bucket for PII in files."""
    s3 = boto3.client('s3')
    analyzer = AnalyzerEngine()
    
    # List objects
    response = s3.list_objects_v2(
        Bucket=bucket_name,
        Prefix=prefix,
        MaxKeys=max_files
    )
    
    findings = []
    
    for obj in response.get('Contents', []):
        key = obj['Key']
        
        # Skip large files
        if obj['Size'] > 10 * 1024 * 1024:  # 10MB
            continue
        
        # Download and analyze
        try:
            response = s3.get_object(Bucket=bucket_name, Key=key)
            content = response['Body'].read().decode('utf-8')
            
            results = analyzer.analyze(text=content, language='en')
            
            if results:
                findings.append({
                    'file': key,
                    'pii_types': list(set(r.entity_type for r in results)),
                    'count': len(results)
                })
        except Exception as e:
            print(f"Error scanning {key}: {e}")
    
    return findings
```

### Git Repository Scanning

```bash
# Use truffleHog for secrets
trufflehog git https://github.com/user/repo --only-verified

# Use gitleaks
gitleaks detect --source . --verbose

# Custom PII scan
git log -p | grep -E '\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
```

## 10. PII Inventory Creation

### Inventory Template

```python
from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

@dataclass
class PIIInventoryItem:
    """PII inventory item."""
    pii_type: str  # EMAIL, PHONE, SSN, etc.
    data_category: str  # Customer, Employee, Partner
    system: str  # Database name, service name
    location: str  # Table.column, S3 bucket, etc.
    purpose: str  # Why we collect it
    legal_basis: str  # Consent, Contract, Legitimate Interest
    retention_period: str  # "30 days", "7 years", etc.
    encryption: bool  # Is it encrypted at rest?
    access_control: str  # Who can access?
    third_parties: List[str]  # Who do we share with?
    discovered_date: datetime
    last_reviewed: datetime
    owner: str  # Data owner/steward

def create_pii_inventory():
    """Create PII inventory."""
    inventory = [
        PIIInventoryItem(
            pii_type="EMAIL",
            data_category="Customer",
            system="users-db",
            location="users.email",
            purpose="Account authentication and communication",
            legal_basis="Contract",
            retention_period="Account lifetime + 30 days",
            encryption=True,
            access_control="Engineering, Support (read-only)",
            third_parties=["SendGrid", "Segment"],
            discovered_date=datetime(2024, 1, 1),
            last_reviewed=datetime(2024, 6, 1),
            owner="engineering@company.com"
        ),
        PIIInventoryItem(
            pii_type="CREDIT_CARD",
            data_category="Customer",
            system="payments-db",
            location="Stripe (tokenized)",
            purpose="Payment processing",
            legal_basis="Contract",
            retention_period="7 years (tax compliance)",
            encryption=True,
            access_control="Stripe only (tokenized)",
            third_parties=["Stripe"],
            discovered_date=datetime(2024, 1, 1),
            last_reviewed=datetime(2024, 6, 1),
            owner="finance@company.com"
        ),
    ]
    
    return inventory
```

## 11. Automated PII Discovery

### PostgreSQL Discovery

```sql
-- Find columns that might contain PII based on name
SELECT 
    table_schema,
    table_name,
    column_name,
    data_type,
    CASE
        WHEN column_name ILIKE '%email%' THEN 'EMAIL'
        WHEN column_name ILIKE '%phone%' OR column_name ILIKE '%mobile%' THEN 'PHONE'
        WHEN column_name ILIKE '%ssn%' OR column_name ILIKE '%social_security%' THEN 'SSN'
        WHEN column_name ILIKE '%address%' THEN 'ADDRESS'
        WHEN column_name ILIKE '%name%' THEN 'NAME'
        WHEN column_name ILIKE '%dob%' OR column_name ILIKE '%birth%' THEN 'DOB'
        ELSE 'UNKNOWN'
    END AS suspected_pii_type
FROM information_schema.columns
WHERE table_schema NOT IN ('pg_catalog', 'information_schema')
    AND (
        column_name ILIKE '%email%'
        OR column_name ILIKE '%phone%'
        OR column_name ILIKE '%ssn%'
        OR column_name ILIKE '%address%'
        OR column_name ILIKE '%name%'
        OR column_name ILIKE '%dob%'
    )
ORDER BY table_schema, table_name, column_name;
```

### MongoDB Discovery

```javascript
// Find collections with potential PII fields
db.getCollectionNames().forEach(function(collName) {
    var sample = db[collName].findOne();
    if (sample) {
        var piiFields = [];
        for (var key in sample) {
            var lowerKey = key.toLowerCase();
            if (lowerKey.includes('email') || 
                lowerKey.includes('phone') ||
                lowerKey.includes('ssn') ||
                lowerKey.includes('address') ||
                lowerKey.includes('name')) {
                piiFields.push(key);
            }
        }
        if (piiFields.length > 0) {
            print(collName + ": " + piiFields.join(', '));
        }
    }
});
```

## 12. PII Detection SLA

### Scanning Frequency

```yaml
# pii-scanning-schedule.yaml
scanning_schedule:
  production_databases:
    frequency: weekly
    day: Sunday
    time: "02:00 UTC"
    
  log_files:
    frequency: daily
    time: "01:00 UTC"
    retention: 90 days
    
  s3_buckets:
    frequency: monthly
    day: 1
    time: "03:00 UTC"
    
  git_repositories:
    frequency: on_commit
    tool: pre-commit hook
    
  new_services:
    frequency: on_deployment
    automated: true
```

### Implementation

```python
from apscheduler.schedulers.background import BackgroundScheduler

def schedule_pii_scans():
    """Schedule automated PII scans."""
    scheduler = BackgroundScheduler()
    
    # Weekly database scan
    scheduler.add_job(
        scan_all_databases,
        'cron',
        day_of_week='sun',
        hour=2,
        minute=0
    )
    
    # Daily log scan
    scheduler.add_job(
        scan_log_files,
        'cron',
        hour=1,
        minute=0
    )
    
    # Monthly S3 scan
    scheduler.add_job(
        scan_s3_buckets,
        'cron',
        day=1,
        hour=3,
        minute=0
    )
    
    scheduler.start()
```

## 13. Reporting and Alerting

### PII Detection Report

```python
from datetime import datetime
import json

def generate_pii_report(findings):
    """Generate PII detection report."""
    report = {
        'scan_date': datetime.now().isoformat(),
        'summary': {
            'total_findings': len(findings),
            'by_type': {},
            'by_system': {},
            'critical_findings': []
        },
        'findings': findings
    }
    
    # Aggregate by type
    for finding in findings:
        pii_type = finding['type']
        report['summary']['by_type'][pii_type] = \
            report['summary']['by_type'].get(pii_type, 0) + 1
        
        # Aggregate by system
        system = finding.get('system', 'unknown')
        report['summary']['by_system'][system] = \
            report['summary']['by_system'].get(system, 0) + 1
        
        # Flag critical findings
        if finding.get('encrypted') == False:
            report['summary']['critical_findings'].append({
                'type': pii_type,
                'location': finding['location'],
                'reason': 'Unencrypted PII'
            })
    
    return report

# Save report
report = generate_pii_report(findings)
with open(f'pii-report-{datetime.now().date()}.json', 'w') as f:
    json.dump(report, f, indent=2)
```

### Alerting

```python
import requests

def alert_on_pii_in_logs(finding):
    """Alert when PII is found in logs (critical!)."""
    if finding['system'] == 'application-logs':
        # Send to Slack
        requests.post(
            'https://hooks.slack.com/services/YOUR/WEBHOOK/URL',
            json={
                'text': f"🚨 PII DETECTED IN LOGS! Type: {finding['type']}, Location: {finding['location']}"
            }
        )
        
        # Create PagerDuty incident
        requests.post(
            'https://api.pagerduty.com/incidents',
            headers={'Authorization': 'Token token=YOUR_TOKEN'},
            json={
                'incident': {
                    'type': 'incident',
                    'title': 'PII detected in application logs',
                    'service': {'id': 'SERVICE_ID', 'type': 'service_reference'},
                    'urgency': 'high'
                }
            }
        )
```

## 14. Implementation Examples

### Complete TypeScript Implementation

```typescript
import { AnalyzerEngine, RecognizerResult } from 'presidio-analyzer';

interface PIIFinding {
  type: string;
  value: string;
  start: number;
  end: number;
  confidence: number;
}

class PIIDetector {
  private emailPattern = /\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b/g;
  private phonePattern = /\b\d{3}[-.]?\d{3}[-.]?\d{4}\b/g;
  private ssnPattern = /\b\d{3}-\d{2}-\d{4}\b/g;

  detectPII(text: string): PIIFinding[] {
    const findings: PIIFinding[] = [];

    // Email detection
    let match;
    while ((match = this.emailPattern.exec(text)) !== null) {
      findings.push({
        type: 'EMAIL',
        value: match[0],
        start: match.index,
        end: match.index + match[0].length,
        confidence: 0.95
      });
    }

    // Phone detection
    while ((match = this.phonePattern.exec(text)) !== null) {
      findings.push({
        type: 'PHONE',
        value: match[0],
        start: match.index,
        end: match.index + match[0].length,
        confidence: 0.90
      });
    }

    // SSN detection
    while ((match = this.ssnPattern.exec(text)) !== null) {
      if (this.isValidSSN(match[0])) {
        findings.push({
          type: 'SSN',
          value: match[0],
          start: match.index,
          end: match.index + match[0].length,
          confidence: 0.98
        });
      }
    }

    return findings;
  }

  private isValidSSN(ssn: string): boolean {
    const clean = ssn.replace(/-/g, '');
    const area = clean.substring(0, 3);
    const group = clean.substring(3, 5);
    const serial = clean.substring(5);

    if (area === '000' || area === '666' || area.startsWith('9')) return false;
    if (group === '00') return false;
    if (serial === '0000') return false;

    return true;
  }

  redactPII(text: string): string {
    const findings = this.detectPII(text);
    let redacted = text;

    // Sort by position (reverse) to maintain indices
    findings.sort((a, b) => b.start - a.start);

    for (const finding of findings) {
      const replacement = `[${finding.type}_REDACTED]`;
      redacted = redacted.substring(0, finding.start) + 
                 replacement + 
                 redacted.substring(finding.end);
    }

    return redacted;
  }
}

// Usage
const detector = new PIIDetector();
const text = "Contact John at john@example.com or 555-123-4567. SSN: 123-45-6789";
const findings = detector.detectPII(text);
console.log(findings);

const redacted = detector.redactPII(text);
console.log(redacted);
// "Contact John at [EMAIL_REDACTED] or [PHONE_REDACTED]. SSN: [SSN_REDACTED]"
```

## 15. Real-World Detection Scenarios

### Scenario 1: User Signup Form

```python
def validate_signup_form(form_data):
    """Validate and detect PII in signup form."""
    detector = PIIDetector()
    
    pii_collected = {
        'email': form_data.get('email'),
        'phone': form_data.get('phone'),
        'name': form_data.get('full_name'),
        'address': form_data.get('address')
    }
    
    # Verify PII is valid
    if not validate_email(pii_collected['email']):
        raise ValueError("Invalid email address")
    
    # Log PII collection (with consent)
    log_pii_collection(
        user_id=None,  # Not yet created
        pii_types=['EMAIL', 'PHONE', 'NAME', 'ADDRESS'],
        purpose='Account creation',
        legal_basis='Consent',
        consent_timestamp=datetime.now()
    )
    
    return pii_collected
```

### Scenario 2: Customer Support Ticket

```python
def scan_support_ticket(ticket_text):
    """Scan support ticket for accidental PII disclosure."""
    detector = PIIDetector()
    findings = detector.detect(ticket_text)
    
    # Alert if sensitive PII found
    sensitive_types = ['SSN', 'CREDIT_CARD', 'PASSPORT']
    for finding in findings:
        if finding['type'] in sensitive_types:
            alert_security_team(
                message=f"Sensitive PII ({finding['type']}) found in support ticket",
                ticket_id=ticket.id,
                severity='HIGH'
            )
            
            # Auto-redact
            ticket_text = detector.redact(ticket_text)
    
    return ticket_text
```

### Scenario 3: Data Export Request

```python
def handle_data_export_request(user_id):
    """Handle GDPR data export request."""
    # Collect all PII for user
    user_data = {
        'profile': get_user_profile(user_id),
        'transactions': get_user_transactions(user_id),
        'logs': get_user_activity_logs(user_id),
        'third_party_data': get_third_party_data(user_id)
    }
    
    # Verify completeness
    pii_inventory = get_pii_inventory_for_user(user_id)
    for item in pii_inventory:
        if item['location'] not in user_data:
            raise ValueError(f"Missing data from {item['location']}")
    
    # Generate export
    export_file = generate_export(user_data)
    
    # Log export
    log_data_export(
        user_id=user_id,
        export_date=datetime.now(),
        data_types=list(user_data.keys())
    )
    
    return export_file
```

## Best Practices

1. **Defense in Depth**: Use multiple detection methods (regex + NER + context)
2. **Regular Scanning**: Automate PII discovery on schedule
3. **Context Matters**: Use field names and surrounding text for better accuracy
4. **Handle False Positives**: Maintain allowlists for test data
5. **Encrypt at Rest**: All detected PII should be encrypted
6. **Access Control**: Limit who can access PII
7. **Audit Logging**: Log all PII access and modifications
8. **Data Minimization**: Only collect PII you actually need
9. **Retention Policies**: Delete PII when no longer needed
10. **Third-Party Audits**: Verify vendors handle PII correctly

## Common Pitfalls

- **Over-reliance on regex**: Misses context and generates false positives
- **Ignoring indirect identifiers**: IP + timestamp can identify users
- **Not scanning logs**: PII often leaks into application logs
- **Forgetting backups**: PII in backups must also be managed
- **Missing third-party systems**: Track where you send PII
- **No inventory**: Can't protect what you don't know you have
- **Static detection**: PII patterns evolve, update regularly

## Summary

PII detection is a critical component of privacy compliance and data security. Use a combination of pattern matching, machine learning, and context-aware analysis to identify PII across your systems. Maintain a comprehensive PII inventory, scan regularly, and implement strong access controls and encryption for all detected PII.
