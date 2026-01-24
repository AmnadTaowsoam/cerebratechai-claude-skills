---
name: Device Management
description: Handling the complete lifecycle of IoT devices from registration to decommissioning, including device twins, OTA updates, provisioning, and AWS IoT Core integration.
---

# Device Management

> **Current Level:** Intermediate  
> **Domain:** IoT / Device Operations

---

## Overview

Device management handles the complete lifecycle of IoT devices from registration to decommissioning. This guide covers device twins, OTA updates, and AWS IoT Core integration for managing large fleets of IoT devices efficiently and securely.

---

## Device Lifecycle

```
Registration → Provisioning → Active → Maintenance → Decommissioning
```

**Stages:**
1. **Registration** - Device added to system
2. **Provisioning** - Credentials and config assigned
3. **Active** - Device operational
4. **Maintenance** - Updates and repairs
5. **Decommissioning** - Device retired

## Database Schema

```sql
-- devices table
CREATE TABLE devices (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  device_id VARCHAR(255) UNIQUE NOT NULL,
  device_name VARCHAR(255) NOT NULL,
  device_type VARCHAR(100) NOT NULL,
  
  manufacturer VARCHAR(255),
  model VARCHAR(255),
  serial_number VARCHAR(255),
  firmware_version VARCHAR(50),
  hardware_version VARCHAR(50),
  
  status VARCHAR(50) DEFAULT 'registered',
  last_seen TIMESTAMP,
  last_ip_address INET,
  
  location JSONB,
  metadata JSONB,
  
  group_id UUID REFERENCES device_groups(id),
  
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  
  INDEX idx_device_id (device_id),
  INDEX idx_status (status),
  INDEX idx_group (group_id),
  INDEX idx_last_seen (last_seen)
);

-- device_credentials table
CREATE TABLE device_credentials (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  device_id UUID REFERENCES devices(id) ON DELETE CASCADE,
  
  credential_type VARCHAR(50) NOT NULL,
  credential_value TEXT NOT NULL,
  
  expires_at TIMESTAMP,
  revoked BOOLEAN DEFAULT FALSE,
  
  created_at TIMESTAMP DEFAULT NOW(),
  
  INDEX idx_device (device_id)
);

-- device_shadows table
CREATE TABLE device_shadows (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  device_id UUID REFERENCES devices(id) ON DELETE CASCADE,
  
  reported_state JSONB,
  desired_state JSONB,
  
  version INTEGER DEFAULT 1,
  
  updated_at TIMESTAMP DEFAULT NOW(),
  
  UNIQUE(device_id)
);

-- device_configurations table
CREATE TABLE device_configurations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  device_id UUID REFERENCES devices(id) ON DELETE CASCADE,
  
  config_key VARCHAR(255) NOT NULL,
  config_value JSONB NOT NULL,
  
  version INTEGER DEFAULT 1,
  applied BOOLEAN DEFAULT FALSE,
  applied_at TIMESTAMP,
  
  created_at TIMESTAMP DEFAULT NOW(),
  
  INDEX idx_device (device_id)
);

-- firmware_versions table
CREATE TABLE firmware_versions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  
  version VARCHAR(50) NOT NULL,
  device_type VARCHAR(100) NOT NULL,
  
  file_url VARCHAR(500) NOT NULL,
  file_size BIGINT,
  checksum VARCHAR(64),
  
  release_notes TEXT,
  
  is_latest BOOLEAN DEFAULT FALSE,
  
  created_at TIMESTAMP DEFAULT NOW(),
  
  UNIQUE(version, device_type)
);

-- device_groups table
CREATE TABLE device_groups (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  
  name VARCHAR(255) NOT NULL,
  description TEXT,
  
  filters JSONB,
  
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

## Device Registration

```typescript
// services/device-registration.service.ts
export class DeviceRegistrationService {
  async registerDevice(data: RegisterDeviceDto): Promise<Device> {
    // Generate device credentials
    const credentials = await this.generateCredentials(data.deviceType);

    // Create device
    const device = await db.device.create({
      data: {
        deviceId: data.deviceId,
        deviceName: data.deviceName,
        deviceType: data.deviceType,
        manufacturer: data.manufacturer,
        model: data.model,
        serialNumber: data.serialNumber,
        status: 'registered',
        metadata: data.metadata
      }
    });

    // Store credentials
    await db.deviceCredential.create({
      data: {
        deviceId: device.id,
        credentialType: 'x509',
        credentialValue: credentials.certificate
      }
    });

    // Create device shadow
    await db.deviceShadow.create({
      data: {
        deviceId: device.id,
        reportedState: {},
        desiredState: {}
      }
    });

    return device;
  }

  private async generateCredentials(deviceType: string): Promise<Credentials> {
    // Generate X.509 certificate
    const { privateKey, certificate } = await this.generateCertificate();

    return {
      privateKey,
      certificate,
      caCertificate: process.env.CA_CERTIFICATE!
    };
  }

  private async generateCertificate(): Promise<{ privateKey: string; certificate: string }> {
    // Implementation using node-forge or openssl
    return {
      privateKey: '-----BEGIN PRIVATE KEY-----\n...',
      certificate: '-----BEGIN CERTIFICATE-----\n...'
    };
  }
}

interface RegisterDeviceDto {
  deviceId: string;
  deviceName: string;
  deviceType: string;
  manufacturer?: string;
  model?: string;
  serialNumber?: string;
  metadata?: any;
}

interface Credentials {
  privateKey: string;
  certificate: string;
  caCertificate: string;
}
```

## Device Authentication

```typescript
// services/device-authentication.service.ts
import jwt from 'jsonwebtoken';

export class DeviceAuthenticationService {
  async authenticateDevice(deviceId: string, credential: string): Promise<boolean> {
    const device = await db.device.findUnique({
      where: { deviceId },
      include: { credentials: true }
    });

    if (!device || device.status !== 'active') {
      return false;
    }

    // Verify credential
    const isValid = await this.verifyCredential(credential, device.credentials);

    if (isValid) {
      // Update last seen
      await db.device.update({
        where: { id: device.id },
        data: { lastSeen: new Date() }
      });
    }

    return isValid;
  }

  async generateDeviceToken(deviceId: string): Promise<string> {
    return jwt.sign(
      { deviceId, type: 'device' },
      process.env.JWT_SECRET!,
      { expiresIn: '30d' }
    );
  }

  async verifyDeviceToken(token: string): Promise<{ deviceId: string } | null> {
    try {
      const decoded = jwt.verify(token, process.env.JWT_SECRET!) as any;
      return { deviceId: decoded.deviceId };
    } catch (error) {
      return null;
    }
  }

  private async verifyCredential(credential: string, storedCredentials: any[]): Promise<boolean> {
    // Verify X.509 certificate or other credential types
    return true; // Simplified
  }
}
```

## Device Twins/Shadows

```typescript
// services/device-shadow.service.ts
export class DeviceShadowService {
  async getDeviceShadow(deviceId: string): Promise<DeviceShadow> {
    const shadow = await db.deviceShadow.findUnique({
      where: { deviceId }
    });

    if (!shadow) {
      throw new Error('Device shadow not found');
    }

    return shadow;
  }

  async updateReportedState(deviceId: string, state: any): Promise<DeviceShadow> {
    const shadow = await db.deviceShadow.update({
      where: { deviceId },
      data: {
        reportedState: state,
        version: { increment: 1 },
        updatedAt: new Date()
      }
    });

    // Emit event
    await this.emitShadowUpdate(deviceId, shadow);

    return shadow;
  }

  async updateDesiredState(deviceId: string, state: any): Promise<DeviceShadow> {
    const shadow = await db.deviceShadow.update({
      where: { deviceId },
      data: {
        desiredState: state,
        version: { increment: 1 },
        updatedAt: new Date()
      }
    });

    // Notify device of desired state change
    await this.notifyDevice(deviceId, shadow.desiredState);

    return shadow;
  }

  async getDelta(deviceId: string): Promise<any> {
    const shadow = await this.getDeviceShadow(deviceId);

    // Calculate difference between desired and reported
    return this.calculateDelta(shadow.desiredState, shadow.reportedState);
  }

  private calculateDelta(desired: any, reported: any): any {
    const delta: any = {};

    Object.keys(desired).forEach(key => {
      if (JSON.stringify(desired[key]) !== JSON.stringify(reported[key])) {
        delta[key] = desired[key];
      }
    });

    return delta;
  }

  private async notifyDevice(deviceId: string, desiredState: any): Promise<void> {
    // Publish to MQTT topic
    mqttClient.publish(`devices/${deviceId}/shadow/update`, JSON.stringify({
      state: { desired: desiredState }
    }));
  }

  private async emitShadowUpdate(deviceId: string, shadow: DeviceShadow): Promise<void> {
    // Emit WebSocket event
    io.emit('shadow-updated', { deviceId, shadow });
  }
}

interface DeviceShadow {
  deviceId: string;
  reportedState: any;
  desiredState: any;
  version: number;
}
```

## Configuration Management

```typescript
// services/device-configuration.service.ts
export class DeviceConfigurationService {
  async setConfiguration(deviceId: string, config: Record<string, any>): Promise<void> {
    for (const [key, value] of Object.entries(config)) {
      await db.deviceConfiguration.create({
        data: {
          deviceId,
          configKey: key,
          configValue: value,
          applied: false
        }
      });
    }

    // Notify device
    await this.pushConfiguration(deviceId, config);
  }

  async getConfiguration(deviceId: string): Promise<Record<string, any>> {
    const configs = await db.deviceConfiguration.findMany({
      where: { deviceId, applied: true },
      orderBy: { createdAt: 'desc' }
    });

    return Object.fromEntries(
      configs.map(c => [c.configKey, c.configValue])
    );
  }

  async markConfigurationApplied(deviceId: string, configKeys: string[]): Promise<void> {
    await db.deviceConfiguration.updateMany({
      where: {
        deviceId,
        configKey: { in: configKeys }
      },
      data: {
        applied: true,
        appliedAt: new Date()
      }
    });
  }

  private async pushConfiguration(deviceId: string, config: Record<string, any>): Promise<void> {
    mqttClient.publish(`devices/${deviceId}/config`, JSON.stringify(config));
  }
}
```

## Firmware Updates (OTA)

```typescript
// services/firmware-update.service.ts
export class FirmwareUpdateService {
  async createFirmwareVersion(data: CreateFirmwareDto): Promise<FirmwareVersion> {
    // Mark previous versions as not latest
    await db.firmwareVersion.updateMany({
      where: {
        deviceType: data.deviceType,
        isLatest: true
      },
      data: { isLatest: false }
    });

    // Create new version
    return db.firmwareVersion.create({
      data: {
        ...data,
        isLatest: true
      }
    });
  }

  async initiateUpdate(deviceId: string, firmwareVersionId: string): Promise<void> {
    const [device, firmware] = await Promise.all([
      db.device.findUnique({ where: { id: deviceId } }),
      db.firmwareVersion.findUnique({ where: { id: firmwareVersionId } })
    ]);

    if (!device || !firmware) {
      throw new Error('Device or firmware not found');
    }

    // Send update command
    await mqttClient.publish(`devices/${device.deviceId}/ota/update`, JSON.stringify({
      version: firmware.version,
      url: firmware.fileUrl,
      checksum: firmware.checksum,
      size: firmware.fileSize
    }));

    // Log update initiation
    await db.deviceEvent.create({
      data: {
        deviceId,
        eventType: 'firmware_update_initiated',
        eventData: { firmwareVersion: firmware.version }
      }
    });
  }

  async reportUpdateProgress(deviceId: string, progress: number): Promise<void> {
    // Emit progress event
    io.emit('firmware-update-progress', { deviceId, progress });
  }

  async reportUpdateComplete(deviceId: string, success: boolean, newVersion?: string): Promise<void> {
    if (success && newVersion) {
      await db.device.update({
        where: { id: deviceId },
        data: { firmwareVersion: newVersion }
      });
    }

    await db.deviceEvent.create({
      data: {
        deviceId,
        eventType: success ? 'firmware_update_success' : 'firmware_update_failed',
        eventData: { version: newVersion }
      }
    });
  }
}

interface CreateFirmwareDto {
  version: string;
  deviceType: string;
  fileUrl: string;
  fileSize: number;
  checksum: string;
  releaseNotes?: string;
}
```

## Device Monitoring

```typescript
// services/device-monitoring.service.ts
export class DeviceMonitoringService {
  async getDeviceHealth(deviceId: string): Promise<DeviceHealth> {
    const device = await db.device.findUnique({
      where: { id: deviceId },
      include: { shadow: true }
    });

    if (!device) {
      throw new Error('Device not found');
    }

    const isOnline = this.isDeviceOnline(device.lastSeen);
    const batteryLevel = device.shadow?.reportedState?.battery;
    const signalStrength = device.shadow?.reportedState?.signal;

    return {
      deviceId: device.deviceId,
      status: device.status,
      isOnline,
      lastSeen: device.lastSeen,
      batteryLevel,
      signalStrength,
      firmwareVersion: device.firmwareVersion
    };
  }

  private isDeviceOnline(lastSeen: Date | null): boolean {
    if (!lastSeen) return false;
    const fiveMinutesAgo = new Date(Date.now() - 5 * 60 * 1000);
    return lastSeen > fiveMinutesAgo;
  }

  async getDeviceMetrics(deviceId: string, period: string): Promise<DeviceMetrics> {
    // Query time-series data
    const metrics = await timeseriesDb.query(`
      SELECT 
        AVG(cpu_usage) as avg_cpu,
        AVG(memory_usage) as avg_memory,
        AVG(temperature) as avg_temp
      FROM device_metrics
      WHERE device_id = $1 AND timestamp > NOW() - INTERVAL '${period}'
    `, [deviceId]);

    return metrics.rows[0];
  }
}

interface DeviceHealth {
  deviceId: string;
  status: string;
  isOnline: boolean;
  lastSeen: Date | null;
  batteryLevel?: number;
  signalStrength?: number;
  firmwareVersion?: string;
}
```

---

## Quick Start

### Device Registration

```typescript
async function registerDevice(deviceInfo: DeviceInfo) {
  // 1. Generate device credentials
  const deviceId = generateDeviceId()
  const certificate = await generateCertificate(deviceId)
  
  // 2. Create device record
  const device = await db.devices.create({
    data: {
      deviceId,
      name: deviceInfo.name,
      type: deviceInfo.type,
      status: 'provisioning',
      certificate: certificate.pem,
      createdAt: new Date()
    }
  })
  
  // 3. Provision on IoT platform
  await iotPlatform.provisionDevice(deviceId, certificate)
  
  return device
}
```

### Device Twin (AWS IoT)

```javascript
const awsIot = require('aws-iot-device-sdk')

const device = awsIot.device({
  keyPath: './device.key',
  certPath: './device.crt',
  caPath: './root-CA.crt',
  clientId: deviceId,
  host: IOT_ENDPOINT
})

// Update device shadow
device.publish('$aws/things/device-001/shadow/update', JSON.stringify({
  state: {
    desired: {
      firmwareVersion: '1.2.0',
      config: { interval: 60 }
    }
  }
}))
```

---

## Production Checklist

- [ ] **Device Identity**: Unique device identifiers
- [ ] **Authentication**: Strong device authentication (certificates)
- [ ] **Provisioning**: Automated device provisioning
- [ ] **Device Twin**: Device state synchronization
- [ ] **OTA Updates**: Over-the-air firmware updates
- [ ] **Monitoring**: Device health monitoring
- [ ] **Lifecycle**: Complete lifecycle management
- [ ] **Security**: Secure device credentials
- [ ] **Scalability**: Support large device fleets
- [ ] **Testing**: Test with real devices
- [ ] **Documentation**: Document device management process
- [ ] **Compliance**: Meet IoT security standards

---

## Anti-patterns

### ❌ Don't: Hardcoded Credentials

```javascript
// ❌ Bad - Hardcoded credentials
const device = awsIot.device({
  keyPath: './device.key',  // Same for all devices!
  clientId: 'device-001'
})
```

```javascript
// ✅ Good - Unique credentials per device
const device = awsIot.device({
  keyPath: `./devices/${deviceId}/device.key`,  // Unique per device
  certPath: `./devices/${deviceId}/device.crt`,
  clientId: deviceId  // Unique client ID
})
```

### ❌ Don't: No Device State Sync

```javascript
// ❌ Bad - No state sync
// Device state unknown!
```

```javascript
// ✅ Good - Device twin/shadow
// Update device shadow
await updateDeviceShadow(deviceId, {
  desired: { firmwareVersion: '1.2.0' }
})

// Device reports state
device.on('message', (topic, payload) => {
  if (topic.includes('/shadow/update/delta')) {
    // Handle state change
  }
})
```

---

## Integration Points

- **IoT Protocols** (`36-iot-integration/iot-protocols/`) - Device communication
- **IoT Security** (`36-iot-integration/iot-security/`) - Device security
- **OTA Updates** (`73-iot-fleet-management/differential-ota-updates/`) - Firmware updates

---

## Further Reading

- [AWS IoT Device Management](https://docs.aws.amazon.com/iot/latest/developerguide/iot-device-management.html)
- [Azure IoT Hub Device Management](https://docs.microsoft.com/en-us/azure/iot-hub/iot-hub-device-management-overview)
- [Device Twins](https://docs.aws.amazon.com/iot/latest/developerguide/iot-device-shadows.html)
3. **Shadows** - Use device shadows for state management
4. **OTA Updates** - Implement secure firmware updates
5. **Monitoring** - Monitor device health continuously
6. **Groups** - Organize devices into groups
7. **Configuration** - Centralize configuration management
8. **Lifecycle** - Track complete device lifecycle
9. **Security** - Rotate credentials regularly
10. **Scalability** - Design for millions of devices

## Resources

- [AWS IoT Core](https://aws.amazon.com/iot-core/)
- [Azure IoT Hub](https://azure.microsoft.com/en-us/services/iot-hub/)
- [Google Cloud IoT](https://cloud.google.com/iot-core)
- [Device Shadow Pattern](https://docs.aws.amazon.com/iot/latest/developerguide/iot-device-shadows.html)
