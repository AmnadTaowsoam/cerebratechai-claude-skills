---
name: IoT Security
description: Protecting IoT devices, data, and networks from cyber threats through device authentication, encryption, secure boot, certificate management, and compliance with security standards.
---

# IoT Security

> **Current Level:** Advanced  
> **Domain:** IoT / Security

---

## Overview

IoT security protects devices, data, and networks from cyber threats. This guide covers authentication, encryption, secure boot, and compliance for securing IoT deployments at scale with proper device identity and data protection.

## IoT Security Challenges

1. **Resource Constraints** - Limited CPU/memory
2. **Physical Access** - Devices in public spaces
3. **Scale** - Millions of devices
4. **Lifetime** - Long deployment periods
5. **Updates** - Difficult to patch
6. **Heterogeneity** - Different protocols/platforms

## Device Authentication

### X.509 Certificates

```python
# certificate_auth.py
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from datetime import datetime, timedelta

class CertificateManager:
    def __init__(self, ca_cert_path: str, ca_key_path: str):
        with open(ca_cert_path, 'rb') as f:
            self.ca_cert = x509.load_pem_x509_certificate(f.read())
        
        with open(ca_key_path, 'rb') as f:
            self.ca_key = serialization.load_pem_private_key(f.read(), password=None)
    
    def generate_device_certificate(self, device_id: str) -> tuple:
        """Generate X.509 certificate for device"""
        
        # Generate private key
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        
        # Build certificate
        subject = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, "US"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, "IoT Devices"),
            x509.NameAttribute(NameOID.COMMON_NAME, device_id)
        ])
        
        cert = x509.CertificateBuilder().subject_name(
            subject
        ).issuer_name(
            self.ca_cert.subject
        ).public_key(
            private_key.public_key()
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            datetime.utcnow()
        ).not_valid_after(
            datetime.utcnow() + timedelta(days=365)
        ).add_extension(
            x509.SubjectAlternativeName([
                x509.DNSName(f"{device_id}.iot.example.com")
            ]),
            critical=False
        ).sign(self.ca_key, hashes.SHA256())
        
        # Serialize
        cert_pem = cert.public_bytes(serialization.Encoding.PEM)
        key_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        
        return cert_pem, key_pem
    
    def verify_certificate(self, cert_pem: bytes) -> bool:
        """Verify device certificate"""
        try:
            cert = x509.load_pem_x509_certificate(cert_pem)
            
            # Verify signature
            self.ca_cert.public_key().verify(
                cert.signature,
                cert.tbs_certificate_bytes,
                cert.signature_algorithm_parameters
            )
            
            # Check validity period
            now = datetime.utcnow()
            if now < cert.not_valid_before or now > cert.not_valid_after:
                return False
            
            return True
        except Exception as e:
            print(f"Certificate verification failed: {e}")
            return False
```

### Token-Based Authentication

```typescript
// device-auth.service.ts
import jwt from 'jsonwebtoken';
import crypto from 'crypto';

export class DeviceAuthService {
  private deviceSecrets = new Map<string, string>();

  async registerDevice(deviceId: string): Promise<{ deviceId: string; secret: string }> {
    const secret = crypto.randomBytes(32).toString('hex');
    this.deviceSecrets.set(deviceId, secret);

    return { deviceId, secret };
  }

  generateToken(deviceId: string, secret: string): string {
    return jwt.sign(
      { deviceId, type: 'device' },
      secret,
      { expiresIn: '30d' }
    );
  }

  verifyToken(token: string, deviceId: string): boolean {
    try {
      const secret = this.deviceSecrets.get(deviceId);
      if (!secret) return false;

      jwt.verify(token, secret);
      return true;
    } catch (error) {
      return false;
    }
  }

  rotateSecret(deviceId: string): string {
    const newSecret = crypto.randomBytes(32).toString('hex');
    this.deviceSecrets.set(deviceId, newSecret);
    return newSecret;
  }
}
```

## Secure Communication (TLS/DTLS)

### MQTT with TLS

```python
# mqtt_tls_client.py
import paho.mqtt.client as mqtt
import ssl

class SecureMQTTClient:
    def __init__(self, broker: str, port: int = 8883):
        self.client = mqtt.Client()
        
        # Configure TLS
        self.client.tls_set(
            ca_certs='ca.crt',
            certfile='client.crt',
            keyfile='client.key',
            cert_reqs=ssl.CERT_REQUIRED,
            tls_version=ssl.PROTOCOL_TLSv1_2
        )
        
        # Verify hostname
        self.client.tls_insecure_set(False)
        
        self.client.connect(broker, port, 60)
    
    def publish_secure(self, topic: str, payload: str):
        """Publish with TLS encryption"""
        self.client.publish(topic, payload, qos=1)
```

### End-to-End Encryption

```python
# e2e_encryption.py
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2

class E2EEncryption:
    def __init__(self, shared_secret: bytes):
        # Derive encryption key from shared secret
        kdf = PBKDF2(
            algorithm=hashes.SHA256(),
            length=32,
            salt=b'iot_device_salt',
            iterations=100000
        )
        key = kdf.derive(shared_secret)
        self.cipher = Fernet(key)
    
    def encrypt(self, data: str) -> bytes:
        """Encrypt data before sending"""
        return self.cipher.encrypt(data.encode())
    
    def decrypt(self, encrypted_data: bytes) -> str:
        """Decrypt received data"""
        return self.cipher.decrypt(encrypted_data).decode()

# Usage
encryption = E2EEncryption(b'shared_secret_key')

# Device side
encrypted = encryption.encrypt('{"temperature": 23.5}')
mqtt_client.publish('sensors/data', encrypted)

# Server side
decrypted = encryption.decrypt(encrypted)
```

## Certificate Management

```typescript
// certificate-manager.service.ts
export class CertificateManagerService {
  async issueCertificate(deviceId: string): Promise<Certificate> {
    // Generate CSR
    const csr = await this.generateCSR(deviceId);

    // Sign with CA
    const certificate = await this.signCSR(csr);

    // Store in database
    await db.deviceCertificate.create({
      data: {
        deviceId,
        certificate,
        expiresAt: new Date(Date.now() + 365 * 24 * 60 * 60 * 1000),
        revoked: false
      }
    });

    return certificate;
  }

  async revokeCertificate(deviceId: string): Promise<void> {
    await db.deviceCertificate.updateMany({
      where: { deviceId },
      data: { revoked: true }
    });

    // Add to CRL (Certificate Revocation List)
    await this.addToCRL(deviceId);
  }

  async checkCertificateExpiry(): Promise<void> {
    const expiringCerts = await db.deviceCertificate.findMany({
      where: {
        expiresAt: {
          lte: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000) // 30 days
        },
        revoked: false
      }
    });

    for (const cert of expiringCerts) {
      await this.notifyExpiringCertificate(cert);
    }
  }

  async rotateCertificate(deviceId: string): Promise<Certificate> {
    // Revoke old certificate
    await this.revokeCertificate(deviceId);

    // Issue new certificate
    return this.issueCertificate(deviceId);
  }

  private async generateCSR(deviceId: string): Promise<string> {
    // Implementation
    return '';
  }

  private async signCSR(csr: string): Promise<string> {
    // Implementation
    return '';
  }

  private async addToCRL(deviceId: string): Promise<void> {
    // Implementation
  }

  private async notifyExpiringCertificate(cert: any): Promise<void> {
    // Send notification
  }
}
```

## Secure Boot

```python
# secure_boot_verification.py
import hashlib
import hmac

class SecureBootVerifier:
    def __init__(self, trusted_hash: str, secret_key: bytes):
        self.trusted_hash = trusted_hash
        self.secret_key = secret_key
    
    def verify_firmware(self, firmware_path: str) -> bool:
        """Verify firmware integrity before boot"""
        
        # Calculate firmware hash
        sha256_hash = hashlib.sha256()
        with open(firmware_path, 'rb') as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        
        firmware_hash = sha256_hash.hexdigest()
        
        # Verify against trusted hash
        if firmware_hash != self.trusted_hash:
            print("Firmware integrity check failed!")
            return False
        
        # Verify HMAC signature
        with open(firmware_path, 'rb') as f:
            firmware_data = f.read()
        
        expected_hmac = hmac.new(
            self.secret_key,
            firmware_data,
            hashlib.sha256
        ).hexdigest()
        
        # Compare with stored HMAC
        stored_hmac = self.get_stored_hmac()
        
        if not hmac.compare_digest(expected_hmac, stored_hmac):
            print("HMAC verification failed!")
            return False
        
        print("Firmware verified successfully")
        return True
    
    def get_stored_hmac(self) -> str:
        """Get stored HMAC from secure storage"""
        # Implementation
        return ""
```

## Encryption at Rest

```python
# data_encryption.py
from cryptography.fernet import Fernet
import json

class DataEncryption:
    def __init__(self, key_path: str):
        with open(key_path, 'rb') as f:
            self.key = f.read()
        self.cipher = Fernet(self.key)
    
    def encrypt_data(self, data: dict) -> bytes:
        """Encrypt data before storing"""
        json_data = json.dumps(data)
        return self.cipher.encrypt(json_data.encode())
    
    def decrypt_data(self, encrypted_data: bytes) -> dict:
        """Decrypt stored data"""
        decrypted = self.cipher.decrypt(encrypted_data)
        return json.loads(decrypted.decode())
    
    @staticmethod
    def generate_key() -> bytes:
        """Generate new encryption key"""
        return Fernet.generate_key()

# Usage
encryption = DataEncryption('encryption.key')

# Encrypt sensitive data
sensor_data = {'temperature': 23.5, 'location': 'secret'}
encrypted = encryption.encrypt_data(sensor_data)

# Store encrypted data
with open('data.enc', 'wb') as f:
    f.write(encrypted)

# Decrypt when needed
with open('data.enc', 'rb') as f:
    encrypted = f.read()
decrypted = encryption.decrypt_data(encrypted)
```

## Access Control

```typescript
// access-control.service.ts
export class AccessControlService {
  async checkPermission(
    deviceId: string,
    resource: string,
    action: string
  ): Promise<boolean> {
    const device = await db.device.findUnique({
      where: { id: deviceId },
      include: { role: { include: { permissions: true } } }
    });

    if (!device || !device.role) {
      return false;
    }

    return device.role.permissions.some(
      p => p.resource === resource && p.action === action
    );
  }

  async assignRole(deviceId: string, roleId: string): Promise<void> {
    await db.device.update({
      where: { id: deviceId },
      data: { roleId }
    });
  }

  async createRole(name: string, permissions: Permission[]): Promise<Role> {
    return db.role.create({
      data: {
        name,
        permissions: {
          create: permissions
        }
      }
    });
  }
}

interface Permission {
  resource: string;
  action: string;
}
```

## Network Segmentation

```yaml
# network-segmentation.yml
# Separate IoT devices into VLANs

vlans:
  - id: 10
    name: iot-sensors
    subnet: 192.168.10.0/24
    firewall_rules:
      - allow: mqtt (1883, 8883)
      - allow: https (443)
      - deny: all

  - id: 20
    name: iot-gateways
    subnet: 192.168.20.0/24
    firewall_rules:
      - allow: mqtt (1883, 8883)
      - allow: https (443)
      - allow: ssh (22) from admin_network
      - deny: all

  - id: 30
    name: iot-management
    subnet: 192.168.30.0/24
    firewall_rules:
      - allow: all from admin_network
      - deny: all
```

## Security Testing

```python
# security_scanner.py
import nmap
import requests

class IoTSecurityScanner:
    def __init__(self):
        self.nm = nmap.PortScanner()
    
    def scan_device(self, ip_address: str) -> dict:
        """Scan device for security vulnerabilities"""
        
        results = {
            'ip': ip_address,
            'open_ports': [],
            'vulnerabilities': []
        }
        
        # Port scan
        self.nm.scan(ip_address, '1-1000')
        
        for host in self.nm.all_hosts():
            for proto in self.nm[host].all_protocols():
                ports = self.nm[host][proto].keys()
                results['open_ports'] = list(ports)
        
        # Check for common vulnerabilities
        results['vulnerabilities'].extend(self.check_default_credentials(ip_address))
        results['vulnerabilities'].extend(self.check_unencrypted_protocols(results['open_ports']))
        
        return results
    
    def check_default_credentials(self, ip_address: str) -> list:
        """Check for default credentials"""
        vulnerabilities = []
        
        default_creds = [
            ('admin', 'admin'),
            ('root', 'root'),
            ('admin', 'password')
        ]
        
        for username, password in default_creds:
            if self.test_credentials(ip_address, username, password):
                vulnerabilities.append({
                    'type': 'default_credentials',
                    'severity': 'critical',
                    'description': f'Default credentials {username}:{password} accepted'
                })
        
        return vulnerabilities
    
    def check_unencrypted_protocols(self, open_ports: list) -> list:
        """Check for unencrypted protocols"""
        vulnerabilities = []
        
        unencrypted_ports = {
            80: 'HTTP',
            23: 'Telnet',
            21: 'FTP',
            1883: 'MQTT (unencrypted)'
        }
        
        for port in open_ports:
            if port in unencrypted_ports:
                vulnerabilities.append({
                    'type': 'unencrypted_protocol',
                    'severity': 'high',
                    'description': f'{unencrypted_ports[port]} on port {port}'
                })
        
        return vulnerabilities
    
    def test_credentials(self, ip_address: str, username: str, password: str) -> bool:
        """Test credentials (implementation depends on protocol)"""
        # Implementation
        return False
```

## Best Practices

1. **Authentication** - Use strong device authentication
2. **Encryption** - Encrypt all communications (TLS/DTLS)
3. **Certificates** - Manage certificate lifecycle
4. **Secure Boot** - Verify firmware integrity
5. **Access Control** - Implement role-based access
6. **Network Segmentation** - Isolate IoT devices
7. **Updates** - Regular security updates
8. **Monitoring** - Monitor for security events
9. **Testing** - Regular security audits
10. **Compliance** - Follow industry standards

---

## Quick Start

### Device Certificate

```python
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization

# Generate device certificate
def generate_device_certificate(device_id: str, private_key):
    subject = issuer = x509.Name([
        x509.NameAttribute(x509.NameOID.COMMON_NAME, device_id)
    ])
    
    cert = x509.CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        issuer
    ).public_key(
        private_key.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.utcnow()
    ).not_valid_after(
        datetime.utcnow() + timedelta(days=365)
    ).add_extension(
        x509.BasicConstraints(ca=False, path_length=None),
        critical=True
    ).sign(private_key, hashes.SHA256())
    
    return cert
```

### Secure Communication

```python
import ssl

# TLS connection
context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
context.load_verify_locations('ca-cert.pem')
context.load_cert_chain('device-cert.pem', 'device-key.pem')

# Connect with TLS
conn = socket.create_connection((host, port))
tls_conn = context.wrap_socket(conn, server_hostname=host)
```

---

## Production Checklist

- [ ] **Device Authentication**: Strong device authentication
- [ ] **Encryption**: Encrypt all communications (TLS/DTLS)
- [ ] **Certificates**: Certificate lifecycle management
- [ ] **Secure Boot**: Verify firmware integrity
- [ ] **Key Management**: Secure key storage
- [ ] **Updates**: Secure OTA updates
- [ ] **Access Control**: Device access control
- [ ] **Monitoring**: Security monitoring
- [ ] **Compliance**: Meet security standards
- [ ] **Documentation**: Document security practices
- [ ] **Testing**: Security testing
- [ ] **Incident Response**: Incident response plan

---

## Anti-patterns

### ❌ Don't: Default Credentials

```python
# ❌ Bad - Default credentials
device.connect(username='admin', password='admin')
# Easy to hack!
```

```python
# ✅ Good - Unique credentials
device.connect(
    certificate='device-cert.pem',
    private_key='device-key.pem'
)
```

### ❌ Don't: No Encryption

```python
# ❌ Bad - No encryption
socket.send(data)  # Plain text!
```

```python
# ✅ Good - TLS encryption
tls_socket.send(data)  # Encrypted
```

---

## Integration Points

- **Device Management** (`36-iot-integration/device-management/`) - Device lifecycle
- **IoT Protocols** (`36-iot-integration/iot-protocols/`) - Secure protocols
- **Edge Computing** (`36-iot-integration/edge-computing/`) - Edge security

---

## Further Reading

- [IoT Security Best Practices](https://owasp.org/www-project-internet-of-things/)
- [Device Certificate Management](https://aws.amazon.com/iot-core/features/device-management/)

## Resources

- [OWASP IoT Top 10](https://owasp.org/www-project-internet-of-things/)
- [NIST IoT Security](https://www.nist.gov/topics/internet-things-iot)
- [IoT Security Foundation](https://www.iotsecurityfoundation.org/)
- [AWS IoT Security](https://docs.aws.amazon.com/iot/latest/developerguide/security.html)
