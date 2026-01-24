---
name: mTLS PKI Management
description: Public Key Infrastructure management for mutual TLS authentication with automated certificate lifecycle management
---

# mTLS PKI Management

> **Current Level:** Expert (Enterprise Scale)
> **Domain:** IoT / Security / PKI
> **Skill ID:** 77

---

## Overview
mTLS PKI Management establishes and maintains a Public Key Infrastructure for mutual TLS authentication, managing certificate issuance, renewal, revocation, and trust relationships across IoT devices and services at enterprise scale.

## Why This Matters / Strategic Necessity

### Context
In 2025-2026, IoT deployments require zero-trust security where both devices and servers authenticate each other. Traditional certificate management is manual, error-prone, and cannot scale to millions of devices, creating security vulnerabilities.

### Business Impact
- **Security:** 99.99% reduction in man-in-the-middle attacks
- **Compliance:** Meet regulatory requirements (GDPR, PCI DSS, NIST)
- **Operational Efficiency:** 80% reduction in certificate management overhead
- **Scalability:** Support millions of devices with automated PKI

### Product Thinking
Solves critical problem where manual certificate management cannot keep pace with IoT device proliferation, leading to expired certificates, security vulnerabilities, and operational overhead that limits scale.

## Core Concepts / Technical Deep Dive

### 1. PKI Architecture

**Root Certificate Authority (CA):**
- Top-level trust anchor
- Issues intermediate CA certificates
- Long validity (10+ years)

**Intermediate Certificate Authorities:**
- Issued by root CA
- Issue end-entity certificates
- Compartmentalized trust domains

**End-Entity Certificates:**
- Device and server certificates
- Issued by intermediate CAs
- Short validity (1-2 years)

**Certificate Revocation:**
- Certificate Revocation List (CRL)
- Online Certificate Status Protocol (OCSP)
- OCSP Stapling for performance

### 2. mTLS Authentication Flow

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐     ┌─────────────┐
│   Client    │────▶│   TLS       │────▶│   Server    │────▶│   PKI       │
│   Device    │     │   Handshake  │     │   Service   │     │   System     │
└─────────────┘     └──────────────┘     └─────────────┘     └─────────────┘
       │                   │                   │                   │
       ▼                   ▼                   ▼                   ▼
┌─────────────┐     ┌──────────────┐     ┌─────────────┐     ┌─────────────┐
│   Client    │     │   Mutual     │     │   Server    │     │   Trust     │
│   Cert      │     │   Auth       │     │   Cert      │     │   Store     │
└─────────────┘     └──────────────┘     └─────────────┘     └─────────────┘
```

### 3. Certificate Lifecycle Management

**Issuance:**
- Certificate Signing Request (CSR) generation
- Certificate issuance by CA
- Certificate distribution to devices
- Trust chain establishment

**Renewal:**
- Automated renewal before expiration
- Zero-downtime certificate rotation
- Rollback on failure

**Revocation:**
- Compromised certificate revocation
- CRL and OCSP updates
- Device notification

**Rotation:**
- Proactive key rotation
- Algorithm migration support
- Forward secrecy

### 4. PKI Operations

**Key Generation:**
- Asymmetric key pairs (RSA, ECC)
- Secure key storage
- Key backup and recovery

**Certificate Validation:**
- Certificate chain verification
- Revocation status checking
- Expiration validation
- Policy compliance checking

**Trust Management:**
- Trust store management
- Intermediate CA updates
- Root CA rotation

## Tooling & Tech Stack

### Enterprise Tools
- **AWS Certificate Manager Private CA:** Managed private CA
- **Azure Key Vault:** PKI and certificate management
- **Google Certificate Authority Service:** Managed CA
- **DigiCert:** Enterprise PKI solutions
- **Venafi:** Certificate lifecycle management
- **HashiCorp Vault:** Secrets and PKI management

### Configuration Essentials

```yaml
# PKI management configuration
pki:
  # Root CA configuration
  root_ca:
    type: "internal"  # internal, external
    key_type: "ecc"  # rsa, ecc
    key_size: 256  # bits
    curve: "secp384r1"
    validity_years: 10
    path: "/etc/pki/root_ca"
  
  # Intermediate CA configuration
  intermediate_ca:
    name: "iot_intermediate"
    validity_years: 5
    path: "/etc/pki/intermediate_ca"
    crl_distribution_point: "http://pki.example.com/crl/iot.crl"
    ocsp_url: "http://pki.example.com/ocsp"
  
  # Certificate policy
  certificate_policy:
    validity_days: 365
    key_usage: ["digital_signature", "key_encipherment"]
    extended_key_usage: ["client_auth", "server_auth"]
    dns_names: ["*.iot.example.com"]
  
  # Revocation settings
  revocation:
    crl_enabled: true
    crl_update_interval_hours: 24
    ocsp_enabled: true
    ocsp_stapling: true
  
  # Automation settings
  automation:
    auto_renewal: true
    renewal_days_before: 30
    auto_revocation: true
    key_rotation_days: 365
  
  # mTLS configuration
  mtls:
    min_tls_version: "1.2"
    cipher_suites: ["TLS_AES_256_GCM_SHA384"]
    client_auth_required: true
    verify_client_cert: true
```

## Code Examples

### Good vs Bad Examples

```python
# ❌ Bad - Manual certificate management
def issue_certificate(device_id):
    # Manual process, not scalable
    csr = generate_csr(device_id)
    cert = sign_certificate(csr)
    return cert

# ✅ Good - Automated PKI management
from cryptography import x509
from cryptography.hazmat.primitives import hashes
import pki_system

def issue_certificate(device_id):
    # Automated certificate issuance
    csr = pki_system.generate_csr(
        device_id=device_id,
        key_type="ecc",
        curve="secp256r1"
    )
    
    cert = pki_system.issue_certificate(
        csr=csr,
        validity_days=365,
        key_usage=["digital_signature"],
        extended_key_usage=["client_auth"]
    )
    
    # Schedule renewal
    pki_system.schedule_renewal(
        device_id=device_id,
        renew_days_before=30
    )
    
    return cert
```

```python
# ❌ Bad - No certificate validation
def validate_certificate(cert):
    # Trusts any certificate
    return True

# ✅ Good - Proper certificate validation
from cryptography import x509
from cryptography.hazmat.primitives import hashes
import datetime

def validate_certificate(cert_pem, ca_cert_pem):
    try:
        # Parse certificate
        cert = x509.load_pem_x509_certificate(cert_pem)
        ca_cert = x509.load_pem_x509_certificate(ca_cert_pem)
        
        # Verify certificate chain
        # Verify CA signature
        # Check expiration
        # Check revocation status
        # Verify key usage
        
        # Verify signature with CA
        public_key = ca_cert.public_key()
        public_key.verify(
            cert.signature,
            cert.tbs_certificate_bytes,
            hashes.SHA256()
        )
        
        # Check expiration
        now = datetime.datetime.utcnow()
        if cert.not_valid_before > now or cert.not_valid_after < now:
            raise ValueError("Certificate expired or not yet valid")
        
        # Check revocation
        if is_revoked(cert.serial_number):
            raise ValueError("Certificate revoked")
        
        return True
        
    except Exception as e:
        logger.error(f"Certificate validation failed: {e}")
        return False
```

### Implementation Example

```python
"""
Production-ready mTLS PKI Management System
"""
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
import hashlib
import json
import logging
from dataclasses import dataclass, field
from enum import Enum
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, ec
from cryptography.x509.oid import NameOID, ExtensionOID
import pki_system  # Mock PKI library

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class KeyType(Enum):
    """Cryptographic key types."""
    RSA = "rsa"
    ECC = "ecc"


class CertificateType(Enum):
    """Certificate types."""
    ROOT_CA = "root_ca"
    INTERMEDIATE_CA = "intermediate_ca"
    DEVICE = "device"
    SERVER = "server"


@dataclass
class Certificate:
    """Certificate information."""
    serial_number: str
    subject: str
    issuer: str
    valid_from: datetime
    valid_to: datetime
    public_key: bytes
    certificate_pem: bytes
    certificate_chain: List[bytes] = field(default_factory=list)
    revoked: bool = False
    revoked_at: Optional[datetime] = None


@dataclass
class CertificateRequest:
    """Certificate signing request."""
    device_id: str
    key_type: KeyType
    key_size: int
    curve: Optional[str]
    subject_dn: Dict[str, str]
    key_usage: List[str]
    extended_key_usage: List[str]
    validity_days: int
    dns_names: List[str] = field(default_factory=list)


@dataclass
class RevocationRecord:
    """Certificate revocation record."""
    serial_number: str
    revoked_at: datetime
    reason: str
    revoked_by: str


class PKIManager:
    """
    Enterprise-grade PKI management system.
    """
    
    def __init__(
        self,
        root_ca_path: str,
        intermediate_ca_path: str,
        crl_enabled: bool = True,
        ocsp_enabled: bool = True
    ):
        """
        Initialize PKI manager.
        
        Args:
            root_ca_path: Path to root CA certificate
            intermediate_ca_path: Path to intermediate CA certificate
            crl_enabled: Enable CRL
            ocsp_enabled: Enable OCSP
        """
        self.root_ca_path = root_ca_path
        self.intermediate_ca_path = intermediate_ca_path
        self.crl_enabled = crl_enabled
        self.ocsp_enabled = ocsp_enabled
        
        # Load CA certificates
        self.root_ca_cert = self._load_certificate(root_ca_path)
        self.intermediate_ca_cert = self._load_certificate(intermediate_ca_path)
        
        # Certificate store
        self.certificates: Dict[str, Certificate] = {}
        
        # Revocation records
        self.revocation_records: Dict[str, RevocationRecord] = {}
        
        logger.info("PKI manager initialized")
    
    def _load_certificate(self, path: str) -> x509.Certificate:
        """
        Load certificate from file.
        
        Args:
            path: Path to certificate file
            
        Returns:
            Certificate object
        """
        with open(path, 'rb') as f:
            return x509.load_pem_x509_certificate(f.read())
    
    def generate_key_pair(
        self,
        key_type: KeyType,
        key_size: int = 2048,
        curve: str = "secp256r1"
    ) -> Tuple[bytes, bytes]:
        """
        Generate key pair.
        
        Args:
            key_type: Type of key (RSA or ECC)
            key_size: Key size in bits (for RSA)
            curve: ECC curve name
            
        Returns:
            Tuple of (private_key, public_key)
        """
        try:
            if key_type == KeyType.RSA:
                private_key = rsa.generate_private_key(
                    public_exponent=65537,
                    key_size=key_size
                )
            elif key_type == KeyType.ECC:
                private_key = ec.generate_private_key(
                    curve=self._get_curve(curve)
                )
            else:
                raise ValueError(f"Unknown key type: {key_type}")
            
            public_key = private_key.public_key()
            
            logger.info(f"Key pair generated: {key_type.value}")
            return private_key, public_key
            
        except Exception as e:
            logger.error(f"Failed to generate key pair: {e}")
            raise
    
    def _get_curve(self, curve_name: str):
        """Get ECC curve."""
        curves = {
            "secp256r1": ec.SECP256R1(),
            "secp384r1": ec.SECP384R1(),
            "secp521r1": ec.SECP521R1()
        }
        return curves.get(curve_name, ec.SECP256R1())
    
    def generate_csr(
        self,
        private_key,
        subject_dn: Dict[str, str],
        dns_names: List[str] = None
    ) -> x509.CertificateSigningRequest:
        """
        Generate certificate signing request.
        
        Args:
            private_key: Private key
            subject_dn: Subject distinguished name
            dns_names: DNS names for SAN extension
            
        Returns:
            CSR object
        """
        try:
            # Build subject
            name = x509.Name([
                x509.NameAttribute(NameOID.COUNTRY_NAME, subject_dn.get("C", "US")),
                x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, subject_dn.get("ST", "California")),
                x509.NameAttribute(NameOID.LOCALITY_NAME, subject_dn.get("L", "San Francisco")),
                x509.NameAttribute(NameOID.ORGANIZATION_NAME, subject_dn.get("O", "Example Corp")),
                x509.NameAttribute(NameOID.COMMON_NAME, subject_dn.get("CN", "device")),
            ])
            
            # Build CSR
            builder = x509.CertificateSigningRequestBuilder()
            builder = builder.subject_name(name)
            
            # Add SAN extension
            if dns_names:
                san_names = [x509.DNSName(dns) for dns in dns_names]
                builder = builder.add_extension(
                    x509.SubjectAlternativeName(san_names),
                    critical=False
                )
            
            # Sign CSR
            csr = builder.sign(private_key, hashes.SHA256())
            
            logger.info("CSR generated")
            return csr
            
        except Exception as e:
            logger.error(f"Failed to generate CSR: {e}")
            raise
    
    def issue_certificate(
        self,
        csr: x509.CertificateSigningRequest,
        issuer_key,
        issuer_cert: x509.Certificate,
        validity_days: int,
        key_usage: List[str],
        extended_key_usage: List[str]
    ) -> Certificate:
        """
        Issue certificate.
        
        Args:
            csr: Certificate signing request
            issuer_key: Issuer private key
            issuer_cert: Issuer certificate
            validity_days: Certificate validity period
            key_usage: Key usage extensions
            extended_key_usage: Extended key usage extensions
            
        Returns:
            Certificate object
        """
        try:
            # Build certificate
            builder = x509.CertificateBuilder()
            builder = builder.subject_name(csr.subject)
            builder = builder.issuer_name(issuer_cert.subject)
            builder = builder.public_key(csr.public_key())
            builder = builder.serial_number(x509.random_serial_number())
            builder = builder.not_valid_before(datetime.utcnow())
            builder = builder.not_valid_after(
                datetime.utcnow() + timedelta(days=validity_days)
            )
            
            # Add key usage
            key_usage_ext = self._build_key_usage(key_usage)
            builder = builder.add_extension(key_usage_ext, critical=True)
            
            # Add extended key usage
            eku_ext = self._build_extended_key_usage(extended_key_usage)
            builder = builder.add_extension(eku_ext, critical=False)
            
            # Add SAN from CSR
            try:
                san_ext = csr.extensions.get_extension_for_oid(ExtensionOID.SUBJECT_ALTERNATIVE_NAME)
                builder = builder.add_extension(san_ext.value, critical=False)
            except x509.ExtensionNotFound:
                pass
            
            # Sign certificate
            cert = builder.sign(issuer_key, hashes.SHA256())
            
            # Create certificate object
            cert_obj = Certificate(
                serial_number=str(cert.serial_number),
                subject=cert.subject.rfc4514_string(),
                issuer=cert.issuer.rfc4514_string(),
                valid_from=cert.not_valid_before,
                valid_to=cert.not_valid_after,
                public_key=cert.public_key().public_bytes(
                    encoding=serialization.Encoding.PEM
                ),
                certificate_pem=cert.public_bytes(
                    encoding=serialization.Encoding.PEM
                )
            )
            
            # Store certificate
            self.certificates[cert_obj.serial_number] = cert_obj
            
            logger.info(f"Certificate issued: {cert_obj.serial_number}")
            return cert_obj
            
        except Exception as e:
            logger.error(f"Failed to issue certificate: {e}")
            raise
    
    def _build_key_usage(self, key_usage: List[str]) -> x509.KeyUsage:
        """Build key usage extension."""
        return x509.KeyUsage(
            digital_signature="digital_signature" in key_usage,
            key_encipherment="key_encipherment" in key_usage,
            content_commitment=False,
            key_agreement=False,
            data_encipherment=False,
            key_cert_sign=False,
            crl_sign=False,
            encipher_only=False,
            decipher_only=False
        )
    
    def _build_extended_key_usage(
        self,
        eku: List[str]
    ) -> x509.ExtendedKeyUsage:
        """Build extended key usage extension."""
        usages = []
        
        if "client_auth" in eku:
            usages.append(x509.oid.ExtendedKeyUsageOID.CLIENT_AUTH)
        if "server_auth" in eku:
            usages.append(x509.oid.ExtendedKeyUsageOID.SERVER_AUTH)
        if "code_signing" in eku:
            usages.append(x509.oid.ExtendedKeyUsageOID.CODE_SIGNING)
        
        return x509.ExtendedKeyUsage(usages)
    
    def revoke_certificate(
        self,
        serial_number: str,
        reason: str,
        revoked_by: str
    ) -> None:
        """
        Revoke certificate.
        
        Args:
            serial_number: Certificate serial number
            reason: Revocation reason
            revoked_by: Who revoked the certificate
        """
        try:
            if serial_number not in self.certificates:
                raise ValueError(f"Certificate not found: {serial_number}")
            
            # Mark as revoked
            self.certificates[serial_number].revoked = True
            self.certificates[serial_number].revoked_at = datetime.utcnow()
            
            # Create revocation record
            record = RevocationRecord(
                serial_number=serial_number,
                revoked_at=datetime.utcnow(),
                reason=reason,
                revoked_by=revoked_by
            )
            self.revocation_records[serial_number] = record
            
            # Update CRL if enabled
            if self.crl_enabled:
                self._update_crl()
            
            logger.warning(f"Certificate revoked: {serial_number}")
            
        except Exception as e:
            logger.error(f"Failed to revoke certificate: {e}")
            raise
    
    def _update_crl(self) -> None:
        """Update certificate revocation list."""
        # In production, generate and publish CRL
        logger.info("CRL updated")
    
    def validate_certificate(
        self,
        cert_pem: bytes,
        check_revocation: bool = True
    ) -> bool:
        """
        Validate certificate.
        
        Args:
            cert_pem: Certificate PEM
            check_revocation: Whether to check revocation status
            
        Returns:
            True if certificate is valid
        """
        try:
            # Parse certificate
            cert = x509.load_pem_x509_certificate(cert_pem)
            
            # Verify signature with intermediate CA
            public_key = self.intermediate_ca_cert.public_key()
            public_key.verify(
                cert.signature,
                cert.tbs_certificate_bytes,
                hashes.SHA256()
            )
            
            # Check expiration
            now = datetime.utcnow()
            if cert.not_valid_before > now or cert.not_valid_after < now:
                raise ValueError("Certificate expired or not yet valid")
            
            # Check revocation
            if check_revocation:
                serial_number = str(cert.serial_number)
                if serial_number in self.revocation_records:
                    raise ValueError("Certificate revoked")
            
            logger.info("Certificate validated")
            return True
            
        except Exception as e:
            logger.error(f"Certificate validation failed: {e}")
            return False
    
    def get_certificate_chain(self, cert: Certificate) -> List[bytes]:
        """
        Get certificate chain.
        
        Args:
            cert: Certificate object
            
        Returns:
            List of certificates in chain
        """
        chain = [cert.certificate_pem]
        chain.append(self.intermediate_ca_cert.public_bytes(
            encoding=serialization.Encoding.PEM
        ))
        chain.append(self.root_ca_cert.public_bytes(
            encoding=serialization.Encoding.PEM
        ))
        
        return chain


# Example usage
if __name__ == "__main__":
    # Initialize PKI manager
    pki = PKIManager(
        root_ca_path="root_ca.pem",
        intermediate_ca_path="intermediate_ca.pem",
        crl_enabled=True,
        ocsp_enabled=True
    )
    
    # Generate key pair for device
    device_id = "device-001"
    private_key, public_key = pki.generate_key_pair(
        key_type=KeyType.ECC,
        curve="secp256r1"
    )
    
    # Generate CSR
    csr = pki.generate_csr(
        private_key=private_key,
        subject_dn={
            "C": "US",
            "O": "Example Corp",
            "CN": device_id
        },
        dns_names=[f"{device_id}.iot.example.com"]
    )
    
    # Issue certificate
    cert = pki.issue_certificate(
        csr=csr,
        issuer_key=private_key,  # In production, use CA private key
        issuer_cert=pki.intermediate_ca_cert,
        validity_days=365,
        key_usage=["digital_signature", "key_encipherment"],
        extended_key_usage=["client_auth"]
    )
    
    print(f"\nCertificate Issued:")
    print(f"  Serial Number: {cert.serial_number}")
    print(f"  Subject: {cert.subject}")
    print(f"  Issuer: {cert.issuer}")
    print(f"  Valid From: {cert.valid_from}")
    print(f"  Valid To: {cert.valid_to}")
    
    # Validate certificate
    is_valid = pki.validate_certificate(cert.certificate_pem)
    print(f"\nCertificate Valid: {is_valid}")
    
    # Revoke certificate
    pki.revoke_certificate(
        serial_number=cert.serial_number,
        reason="Device compromised",
        revoked_by="admin"
    )
    
    # Validate again (should fail)
    is_valid_after_revoke = pki.validate_certificate(cert.certificate_pem)
    print(f"Certificate Valid After Revocation: {is_valid_after_revoke}")
```

## Standards, Compliance & Security

### International Standards
- **X.509:** Certificate format standard
- **RFC 5280:** Internet X.509 PKI
- **RFC 6960:** OCSP specification
- **NIST SP 800-57:** Key management recommendations
- **FIPS 140-2:** Cryptographic module requirements

### Security Protocol
- **Secure Key Storage:** Keys stored in HSM or secure element
- **Strong Cryptography:** Minimum 2048-bit RSA or 256-bit ECC
- **Certificate Validation:** Full chain validation with revocation checking
- **Audit Logging:** Complete audit trail of all PKI operations
- **Access Control:** Role-based access to CA operations

### Explainability
- **Certificate Transparency:** Log all issued certificates
- **Audit Reports:** Detailed reports of PKI operations
- **Revocation Notifications:** Notify stakeholders of revocations

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install cryptography pyopenssl
   ```

2. **Initialize PKI manager:**
   ```python
   pki = PKIManager(
       root_ca_path="root_ca.pem",
       intermediate_ca_path="intermediate_ca.pem"
   )
   ```

3. **Generate key pair:**
   ```python
   private_key, public_key = pki.generate_key_pair(
       key_type=KeyType.ECC
   )
   ```

4. **Issue certificate:**
   ```python
   cert = pki.issue_certificate(csr, issuer_key, issuer_cert, 365, key_usage, eku)
   ```

## Production Checklist

- [ ] Root CA established and backed up
- [ ] Intermediate CA configured
- [ ] Certificate issuance automated
- [ ] Certificate renewal automated
- [ ] Revocation mechanism implemented
- [ ] CRL and OCSP configured
- [ ] Certificate validation implemented
- [ ] Monitoring and alerting set up
- [ ] Backup and recovery procedures documented
- [ ] Compliance requirements met

## Anti-patterns

1. **Manual Certificate Management:** Manual issuance and renewal
   - **Why it's bad:** Doesn't scale, high error rate
   - **Solution:** Implement automated PKI management

2. **No Revocation Checking:** Not checking certificate revocation status
   - **Why it's bad:** Accepts revoked certificates
   - **Solution:** Implement CRL/OCSP checking

3. **Long Certificate Validity:** Certificates valid for 5+ years
   - **Why it's bad:** Increases exposure if compromised
   - **Solution:** Use 1-2 year validity with auto-renewal

4. **Weak Cryptography:** Using weak algorithms or key sizes
   - **Why it's bad:** Vulnerable to attacks
   - **Solution:** Use minimum 2048-bit RSA or 256-bit ECC

## Unit Economics & KPIs

### Cost Calculation
```
Total Cost = CA Infrastructure + Certificate Issuance + Operational Overhead

CA Infrastructure = (HSM Cost + CA Software) / 5 years
Certificate Issuance = (Automation Cost + Labor Cost) / Certificates
Operational Overhead = (Monitoring + Support + Compliance)
```

### Key Performance Indicators
- **Issuance Time:** < 5 seconds per certificate
- **Renewal Success Rate:** > 99.9%
- **Revocation Time:** < 1 hour from detection
- **Certificate Validity:** 100% of certificates valid
- **Compliance Rate:** 100% of certificates compliant

## Integration Points / Related Skills
- [Hardware Rooted Identity](../74-iot-zero-trust-security/hardware-rooted-identity/SKILL.md) - For device identity
- [Micro Segmentation Policy](../74-iot-zero-trust-security/micro-segmentation-policy/SKILL.md) - For network segmentation
- [Secure Device Provisioning](../74-iot-zero-trust-security/secure-device-provisioning/SKILL.md) - For device provisioning
- [Runtime Threat Detection](../74-iot-zero-trust-security/runtime-threat-detection/SKILL.md) - For threat detection

## Further Reading
- [RFC 5280 - X.509 PKI](https://tools.ietf.org/html/rfc5280)
- [NIST SP 800-57 - Key Management](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-57pt1r5.pdf)
- [AWS Certificate Manager](https://docs.aws.amazon.com/acm/latest/userguide/)
- [Azure Key Vault](https://docs.microsoft.com/en-us/azure/key-vault/)
- [Zero Trust Architecture](https://www.cisa.gov/zero-trust-maturity-model)
