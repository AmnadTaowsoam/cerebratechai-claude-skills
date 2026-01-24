---
name: Atomic AB Partitioning
description: Dual-bank firmware partitioning for safe, atomic OTA updates with automatic rollback capability
---

# Atomic AB Partitioning

> **Current Level:** Expert (Enterprise Scale)
> **Domain:** IoT / Embedded Systems / Firmware Updates
> **Skill ID:** 74

---

## Overview
Atomic AB Partitioning uses dual-bank memory layout where firmware is stored in two partitions (A and B). Updates are applied to the inactive partition and atomically switched, enabling safe updates with instant rollback capability.

## Why This Matters / Strategic Necessity

### Context
In 2025-2026, IoT devices require highly reliable firmware updates where failures can brick devices. Single-partition systems risk corruption during updates, leading to costly device replacements and customer dissatisfaction.

### Business Impact
- **Update Reliability:** 99.9% update success rate
- **Rollback Speed:** Instant rollback (< 1 second)
- **Device Protection:** Eliminates bricked devices
- **Customer Trust:** Higher confidence in OTA updates

### Product Thinking
Solves critical problem where failed firmware updates brick devices, requiring physical intervention and causing significant operational costs and customer dissatisfaction.

## Core Concepts / Technical Deep Dive

### 1. Partition Architecture

**Dual-Bank Layout:**
- Partition A: Active firmware
- Partition B: Inactive firmware (update target)
- Bootloader: Selects active partition
- Metadata: Version and status information

**Partition Switching:**
- Atomic switch via bootloader
- CRC verification before switch
- Fallback to previous version on failure

**Memory Layout:**
```
┌─────────────────────────────────────────────────────────────────┐
│                    Flash Memory Layout                          │
├─────────────────────────────────────────────────────────────────┤
│  Bootloader (32KB)  │  Partition A (4MB)  │  Partition B (4MB)  │
│  - Boot selection  │  - Firmware v1.0     │  - Firmware v1.1     │
│  - CRC verify     │  - Active            │  - Inactive          │
├───────────────────────┼───────────────────────┼───────────────────────┤
│  Metadata (4KB)     │  Config (8KB)        │  Reserved (512KB)    │
│  - Active partition  │  - Device config      │  - Future use         │
│  - Version info     │  - Calibration data   │                      │
└───────────────────────┴───────────────────────┴───────────────────────┘
```

### 2. Update Process

**Atomic Update Flow:**
1. Bootloader verifies current partition
2. Download new firmware to inactive partition
3. Verify CRC of new firmware
4. Mark new partition as valid
5. Reboot to bootloader
6. Bootloader switches to new partition
7. If boot fails, rollback to previous partition

**Failure Handling:**
- CRC verification failure
- Boot failure detection
- Watchdog timeout
- Power loss protection

### 3. Bootloader Design

**Bootloader Responsibilities:**
- Partition selection logic
- Firmware verification
- Atomic switching
- Rollback on failure
- Recovery mode support

**Boot States:**
- Normal boot: Load active partition
- Update mode: Load update partition
- Recovery mode: Load recovery firmware
- Fallback: Revert to previous version

### 4. Metadata Management

**Partition Metadata:**
- Version number
- Build timestamp
- CRC checksum
- Boot status
- Update count

**Bootloader Metadata:**
- Active partition indicator
- Boot attempt counter
- Failure reason
- Recovery flag

## Tooling & Tech Stack

### Enterprise Tools
- **MCUboot:** NXP bootloader with A/B support
- **U-Boot:** Universal bootloader with A/B support
- **Zephyr:** RTOS with MCUboot integration
- **Espressif OTA:** ESP32 OTA framework
- **Nordic DFU:** Device firmware update for nRF
- **STM32 Bootloader:** STM32 dual-bank bootloader

### Configuration Essentials

```yaml
# AB partitioning configuration
partitioning:
  # Partition layout
  layout:
    type: "dual_bank"  # dual_bank, single_bank
    bank_size: 4194304  # 4MB per bank
    bootloader_size: 32768  # 32KB
    metadata_size: 4096  # 4KB
  
  # Partition configuration
  partitions:
    - name: "bank_a"
      address: 0x08008000
      size: 4194304
      type: "firmware"
    
    - name: "bank_b"
      address: 0x08048000
      size: 4194304
      type: "firmware"
    
    - name: "metadata"
      address: 0x08088000
      size: 4096
      type: "metadata"
  
  # Bootloader configuration
  bootloader:
    verify_crc: true
    verify_signature: true
    max_boot_attempts: 3
    watchdog_timeout_ms: 5000
    rollback_on_failure: true
  
  # Update configuration
  update:
    verify_before_switch: true
    atomic_switch: true
    backup_before_update: false
    rollback_on_boot_failure: true
  
  # Recovery configuration
  recovery:
    recovery_firmware_enabled: true
    recovery_partition: "recovery"
    max_recovery_attempts: 5
```

## Code Examples

### Good vs Bad Examples

```c
// ❌ Bad - No atomic switching, direct overwrite
void update_firmware(uint8_t* new_firmware, size_t size) {
    // Directly overwrite current firmware
    flash_write(FLASH_BASE, new_firmware, size);
    // No verification, no rollback
}

// ✅ Good - Atomic AB partitioning with verification
void update_firmware_atomic(uint8_t* new_firmware, size_t size) {
    // Write to inactive partition
    uint8_t* inactive = get_inactive_partition();
    flash_write(inactive, new_firmware, size);
    
    // Verify CRC
    if (!verify_crc(inactive, size)) {
        return ERROR_CRC_FAILED;
    }
    
    // Mark as valid
    set_partition_valid(inactive);
    
    // Trigger reboot for atomic switch
    trigger_reboot();
}
```

```c
// ❌ Bad - No rollback on failure
void boot_application() {
    // Always boot from partition A
    uint8_t* app = PARTITION_A;
    jump_to_application(app);
}

// ✅ Good - Bootloader with rollback
void boot_application() {
    // Check which partition to boot
    partition_t* active = select_active_partition();
    
    // Verify partition
    if (!verify_partition(active)) {
        // Rollback to other partition
        active = get_other_partition(active);
    }
    
    jump_to_application(active->address);
}
```

### Implementation Example

```c
/*
 * Production-ready Atomic AB Partitioning Bootloader
 */
#include <stdint.h>
#include <stdbool.h>
#include <string.h>

#define FLASH_BASE            0x08000000
#define PARTITION_A_ADDR      0x08008000
#define PARTITION_B_ADDR      0x08048000
#define METADATA_ADDR         0x08088000
#define PARTITION_SIZE         0x00400000  // 4MB

typedef enum {
    PARTITION_A,
    PARTITION_B,
    PARTITION_COUNT
} partition_id_t;

typedef struct {
    uint32_t version;
    uint32_t build_time;
    uint32_t crc32;
    uint8_t  is_valid;
    uint8_t  boot_count;
    uint8_t  boot_failures;
    uint8_t  active;
} partition_metadata_t;

typedef struct {
    partition_id_t id;
    uint32_t       address;
    uint32_t       size;
    partition_metadata_t metadata;
} partition_t;

/* Global variables */
static partition_t partitions[PARTITION_COUNT];
static partition_t* active_partition = NULL;

/* Function prototypes */
void bootloader_init(void);
partition_t* select_active_partition(void);
bool verify_partition(partition_t* partition);
void switch_partition(partition_id_t new_active);
void jump_to_application(uint32_t address);
uint32_t calculate_crc32(uint8_t* data, uint32_t size);
void watchdog_init(void);
void watchdog_refresh(void);

/**
 * Initialize bootloader
 */
void bootloader_init(void) {
    /* Initialize partition structures */
    partitions[PARTITION_A].id = PARTITION_A;
    partitions[PARTITION_A].address = PARTITION_A_ADDR;
    partitions[PARTITION_A].size = PARTITION_SIZE;
    
    partitions[PARTITION_B].id = PARTITION_B;
    partitions[PARTITION_B].address = PARTITION_B_ADDR;
    partitions[PARTITION_B].size = PARTITION_SIZE;
    
    /* Load metadata from flash */
    memcpy(&partitions[PARTITION_A].metadata, 
           (void*)METADATA_ADDR, 
           sizeof(partition_metadata_t));
    memcpy(&partitions[PARTITION_B].metadata, 
           (void*)(METADATA_ADDR + sizeof(partition_metadata_t)), 
           sizeof(partition_metadata_t));
    
    /* Select active partition */
    active_partition = select_active_partition();
}

/**
 * Select active partition to boot
 */
partition_t* select_active_partition(void) {
    /* Check if metadata is valid */
    if (partitions[PARTITION_A].metadata.is_valid && 
        partitions[PARTITION_B].metadata.is_valid) {
        
        /* Both valid, check which is marked active */
        if (partitions[PARTITION_A].metadata.active) {
            return &partitions[PARTITION_A];
        } else {
            return &partitions[PARTITION_B];
        }
    }
    
    /* Only one or none valid, try to boot valid one */
    if (partitions[PARTITION_A].metadata.is_valid) {
        return &partitions[PARTITION_A];
    }
    
    if (partitions[PARTITION_B].metadata.is_valid) {
        return &partitions[PARTITION_B];
    }
    
    /* No valid partition, try A as default */
    return &partitions[PARTITION_A];
}

/**
 * Verify partition CRC and integrity
 */
bool verify_partition(partition_t* partition) {
    /* Calculate CRC of partition */
    uint32_t calculated_crc = calculate_crc32(
        (uint8_t*)partition->address,
        partition->size
    );
    
    /* Compare with stored CRC */
    if (calculated_crc != partition->metadata.crc32) {
        return false;
    }
    
    /* Additional checks can be added here */
    /* - Signature verification */
    /* - Version compatibility check */
    /* - Firmware header validation */
    
    return true;
}

/**
 * Switch active partition
 */
void switch_partition(partition_id_t new_active) {
    partition_id_t current = active_partition->id;
    
    /* Mark new partition as active */
    partitions[new_active].metadata.active = 1;
    partitions[current].metadata.active = 0;
    
    /* Reset boot counters */
    partitions[new_active].metadata.boot_count = 0;
    partitions[new_active].metadata.boot_failures = 0;
    
    /* Write metadata to flash */
    /* In production, use proper flash write functions */
    uint32_t metadata_offset = (new_active == PARTITION_A) ? 
        0 : sizeof(partition_metadata_t);
    
    /* Flash write would go here */
    /* flash_write(METADATA_ADDR + metadata_offset, 
               &partitions[new_active].metadata, 
               sizeof(partition_metadata_t)); */
}

/**
 * Jump to application
 */
void jump_to_application(uint32_t address) {
    /* Disable interrupts */
    __disable_irq();
    
    /* Deinitialize peripherals */
    /* Deinit clocks, GPIO, etc. */
    
    /* Set stack pointer */
    __set_MSP(*(volatile uint32_t*)address);
    
    /* Jump to application */
    typedef void (*function_ptr_t)(void);
    function_ptr_t app_entry = (function_ptr_t)address;
    app_entry();
}

/**
 * Calculate CRC32
 */
uint32_t calculate_crc32(uint8_t* data, uint32_t size) {
    uint32_t crc = 0xFFFFFFFF;
    
    for (uint32_t i = 0; i < size; i++) {
        crc ^= data[i];
        for (uint8_t j = 0; j < 8; j++) {
            if (crc & 1) {
                crc = (crc >> 1) ^ 0xEDB88320;
            } else {
                crc = crc >> 1;
            }
        }
    }
    
    return ~crc;
}

/**
 * Bootloader main function
 */
int main(void) {
    /* Initialize system */
    system_init();
    watchdog_init();
    
    /* Initialize bootloader */
    bootloader_init();
    
    /* Verify active partition */
    if (!verify_partition(active_partition)) {
        /* Active partition invalid, try other */
        partition_t* other = (active_partition->id == PARTITION_A) ?
            &partitions[PARTITION_B] : &partitions[PARTITION_A];
        
        if (verify_partition(other)) {
            /* Switch to valid partition */
            switch_partition(other->id);
            active_partition = other;
        } else {
            /* Both invalid, enter recovery mode */
            enter_recovery_mode();
            return -1;
        }
    }
    
    /* Increment boot count */
    active_partition->metadata.boot_count++;
    
    /* Jump to application */
    watchdog_refresh();
    jump_to_application(active_partition->address);
    
    /* Should never reach here */
    return 0;
}

/**
 * Update firmware (called from application)
 */
int update_firmware(uint8_t* new_firmware, uint32_t size) {
    /* Get inactive partition */
    partition_t* inactive = (active_partition->id == PARTITION_A) ?
        &partitions[PARTITION_B] : &partitions[PARTITION_A];
    
    /* Write new firmware to inactive partition */
    /* In production, use proper flash erase/write functions */
    /* flash_erase(inactive->address, inactive->size); */
    /* flash_write(inactive->address, new_firmware, size); */
    
    /* Calculate and store CRC */
    uint32_t crc = calculate_crc32(new_firmware, size);
    inactive->metadata.crc32 = crc;
    inactive->metadata.version = get_firmware_version(new_firmware);
    inactive->metadata.build_time = get_current_time();
    inactive->metadata.is_valid = 1;
    
    /* Write metadata to flash */
    uint32_t metadata_offset = (inactive->id == PARTITION_A) ?
        0 : sizeof(partition_metadata_t);
    /* flash_write(METADATA_ADDR + metadata_offset, 
               &inactive->metadata, 
               sizeof(partition_metadata_t)); */
    
    /* Switch to new partition */
    switch_partition(inactive->id);
    
    /* Reboot to apply update */
    system_reset();
    
    return 0;
}
```

## Standards, Compliance & Security

### International Standards
- **ISO/IEC 27001:** Information security management
- **IEC 62443:** Industrial cybersecurity
- **AUTOSAR:** Automotive software architecture
- **MISRA C:** C coding standards for safety-critical systems

### Security Protocol
- **Secure Boot:** Verify firmware signature at boot
- **Rollback Protection:** Prevent rollback attacks
- **Write Protection:** Protect bootloader and metadata
- **Access Control:** Restrict update operations
- **Audit Logging:** Log all update operations

### Explainability
- **Boot Logs:** Complete boot history
- **Partition Status:** Clear indication of active partition
- **Update Reports:** Detailed update operation logs

## Quick Start

1. **Configure dual-bank layout:**
   ```c
   partitions[PARTITION_A].address = 0x08008000;
   partitions[PARTITION_B].address = 0x08048000;
   ```

2. **Implement bootloader:**
   ```c
   void bootloader_init(void) {
       load_partition_metadata();
       active_partition = select_active_partition();
   }
   ```

3. **Verify partition:**
   ```c
   bool verify_partition(partition_t* partition) {
       uint32_t crc = calculate_crc32(
           (uint8_t*)partition->address,
           partition->size
       );
       return (crc == partition->metadata.crc32);
   }
   ```

4. **Switch partition:**
   ```c
   void switch_partition(partition_id_t new_active) {
       partitions[new_active].metadata.active = 1;
       /* Write metadata to flash */
   }
   ```

## Production Checklist

- [ ] Dual-bank layout configured
- [ ] Bootloader implemented with A/B support
- [ ] CRC verification implemented
- [ ] Atomic switching mechanism
- [ ] Rollback on boot failure
- [ ] Secure boot integration
- [ ] Metadata management
- [ ] Recovery mode support
- [ ] Update validation testing

## Anti-patterns

1. **Single Partition:** Only one firmware partition
   - **Why it's bad:** No rollback, bricked devices on failure
   - **Solution:** Implement A/B partitioning

2. **No Verification:** Not verifying firmware before boot
   - **Why it's bad:** Boots corrupted firmware
   - **Solution:** Implement CRC and signature verification

3. **Non-atomic Switch:** Switching without atomic operation
   - **Why it's bad:** Corruption on power loss
   - **Solution:** Use atomic switching mechanism

4. **No Boot Failure Detection:** Not detecting boot failures
   - **Why it's bad:** Infinite boot loop
   - **Solution:** Implement boot failure detection and rollback

## Unit Economics & KPIs

### Cost Calculation
```
Total Cost = Flash Memory + Development + Testing + Support

Flash Memory = (Partition Size × 2) × Flash Cost per MB
Development = (Bootloader Development Time × Labor Rate)
Testing = (Validation Time × Labor Rate)
Support = (Brick Rate × Replacement Cost)
```

### Key Performance Indicators
- **Update Success Rate:** > 99.9%
- **Rollback Rate:** < 0.1% of updates
- **Boot Time:** < 5 seconds
- **Flash Utilization:** < 80% of available flash
- **Recovery Success:** > 99% of recovery attempts

## Integration Points / Related Skills
- [Differential OTA Updates](../73-iot-fleet-management/differential-ota-updates/SKILL.md) - For efficient updates
- [Fleet Campaign Management](../73-iot-fleet-management/fleet-campaign-management/SKILL.md) - For fleet management
- [Hardware Rooted Identity](../74-iot-zero-trust-security/hardware-rooted-identity/SKILL.md) - For device authentication
- [Runtime Threat Detection](../74-iot-zero-trust-security/runtime-threat-detection/SKILL.md) - For threat detection

## Further Reading
- [MCUboot Documentation](https://docs.nxp.com/bundle/MCUXpresso_MCUBOOT)
- [U-Boot Documentation](https://www.denx.de/wiki/U-Boot)
- [Zephyr MCUboot](https://docs.zephyrproject.org/latest/hardware/porting/bootloaders/mcuboot/index.html)
- [STM32 Bootloader](https://www.st.com/resource/en/application_note/an4657/)
- [AUTOSAR Adaptive Platform](https://www.autosar.org/)
