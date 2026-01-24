---
name: AI Supply Chain Security (Model BOM)
description: Implement Software/Model Bill of Materials (SBOM/MBOM) for AI systems, vulnerability management, adversarial attack defense, and trusted AI pipelines to secure the AI supply chain from training to deployment.
skill-id: 163
domain: Security / AI/ML / Compliance
level: Expert (Enterprise Scale)
maturity: Emerging (2026-2027)
---

# AI Supply Chain Security (Model BOM)

> **Current Level:** Expert (Enterprise Scale)
> **Domain:** Security / AI/ML / Compliance
> **Skill ID:** 163
> **Maturity:** Emerging - เตรียมความพร้อมสำหรับ 2026-2027

---

## Overview

AI Supply Chain Security ขยายขอบเขตจากความปลอดภัยของอุปกรณ์ IoT (Skill 76-80) และ LLM Security (Skill 123) ไปสู่ความปลอดภัยของซอฟต์แวร์และโมเดล AI ทั้ง Supply Chain ตั้งแต่ Training Data ไปจนถึง Deployed Model

---

## Why This Matters / Strategic Necessity

### Context

ความเสี่ยงด้าน Supply Chain เพิ่มขึ้น:
- **Model Vulnerabilities:** โมเดลที่ Download มามีช่องโหว่
- **Data Poisoning:** Training Data ถูก Poison
- **Backdoor Attacks:** Pre-trained Models มี Backdoor
- **Regulatory Requirements:** Executive Order 14028 กำหนดให้มี SBOM

### Business Impact

- **Reputation Protection:** ป้องกันความเสียหายต่อชื่อเสียง
- **Risk Mitigation:** ลดความเสี่ยงจากการใช้โมเดลที่มีช่องโหว่
- **Compliance:** Compliance กับ Executive Order 14028 และ NIST SSDF
- **Trust:** เพิ่มความน่าเชื่อถือในสายตาลูกค้า

### Product Thinking

ทักษะนี้ช่วยแก้ปัญหา:
- **Security Teams:** ต้องการตรวจสอบ Supply Chain
- **ML Teams:** ต้องการใช้โมเดลที่ปลอดภัย
- **Compliance Teams:** ต้องการ SBOM สำหรับ Audit
- **Customers:** ต้องการความมั่นใจในความปลอดภัย

---

## Core Concepts / Technical Deep Dive

### 1. Software Bill of Materials (SBOM) for AI

บัญชีส่วนประกอบของโมเดล AI

```python
from typing import Dict, List, Optional
from datetime import datetime
import hashlib
import json

class AISBOMGenerator:
    """Generate Software Bill of Materials for AI models"""
    
    def generate_sbom(
        self,
        model_id: str,
        model_path: str
    ) -> Dict:
        """
        Generate SBOM for AI model.
        
        Follows CycloneDX or SPDX format.
        """
        sbom = {
            "bomFormat": "CycloneDX",
            "specVersion": "1.5",
            "version": 1,
            "metadata": {
                "timestamp": datetime.utcnow().isoformat(),
                "tools": [{"name": "AI-SBOM-Generator", "version": "1.0.0"}],
                "component": {
                    "type": "application",
                    "name": model_id,
                    "version": self._get_model_version(model_id)
                }
            },
            "components": []
        }
        
        # Component 1: Base Model
        base_model = self._extract_base_model(model_path)
        if base_model:
            sbom["components"].append({
                "type": "library",
                "name": base_model["name"],
                "version": base_model["version"],
                "purl": base_model.get("purl"),  # Package URL
                "hashes": [{
                    "alg": "SHA-256",
                    "content": base_model["hash"]
                }],
                "properties": [
                    {"name": "source", "value": base_model["source"]},
                    {"name": "license", "value": base_model.get("license", "unknown")}
                ]
            })
        
        # Component 2: Training Dataset
        training_data = self._extract_training_data_info(model_id)
        if training_data:
            sbom["components"].append({
                "type": "data",
                "name": training_data["dataset_name"],
                "version": training_data["dataset_version"],
                "hashes": [{
                    "alg": "SHA-256",
                    "content": training_data["dataset_hash"]
                }],
                "properties": [
                    {"name": "source", "value": training_data["source"]},
                    {"name": "size", "value": str(training_data["size"])},
                    {"name": "records", "value": str(training_data["num_records"])}
                ]
            })
        
        # Component 3: ML Framework Dependencies
        dependencies = self._extract_dependencies(model_path)
        for dep in dependencies:
            sbom["components"].append({
                "type": "library",
                "name": dep["name"],
                "version": dep["version"],
                "purl": f"pkg:pypi/{dep['name']}@{dep['version']}",
                "hashes": [{
                    "alg": "SHA-256",
                    "content": dep["hash"]
                }]
            })
        
        # Component 4: Model Weights
        weights_info = self._extract_weights_info(model_path)
        sbom["components"].append({
            "type": "file",
            "name": f"{model_id}-weights",
            "hashes": [{
                "alg": "SHA-256",
                "content": weights_info["hash"]
            }],
            "properties": [
                {"name": "size_bytes", "value": str(weights_info["size"])},
                {"name": "format", "value": weights_info["format"]}
            ]
        })
        
        return sbom
    
    def _extract_base_model(self, model_path: str) -> Optional[Dict]:
        """Extract base model information"""
        # Check model metadata
        metadata = self._load_model_metadata(model_path)
        
        if metadata.get("base_model"):
            return {
                "name": metadata["base_model"]["name"],
                "version": metadata["base_model"]["version"],
                "source": metadata["base_model"]["source"],
                "hash": metadata["base_model"]["hash"],
                "purl": metadata["base_model"].get("purl"),
                "license": metadata["base_model"].get("license")
            }
        
        return None
```

### 2. Model Bill of Materials (MBOM)

บัญชีส่วนประกอบเฉพาะของโมเดล

```python
class ModelBOMGenerator:
    """Generate Model-specific Bill of Materials"""
    
    def generate_mbom(
        self,
        model_id: str
    ) -> Dict:
        """
        Generate Model Bill of Materials.
        
        Includes architecture, training config, hyperparameters.
        """
        model_info = self._get_model_info(model_id)
        
        mbom = {
            "mbom_version": "1.0",
            "model_id": model_id,
            "generated_at": datetime.utcnow().isoformat(),
            "architecture": {
                "type": model_info["architecture"]["type"],
                "layers": model_info["architecture"]["layers"],
                "parameters": model_info["architecture"]["parameters"],
                "config_hash": self._hash_config(model_info["architecture"])
            },
            "training": {
                "dataset": {
                    "id": model_info["training"]["dataset_id"],
                    "version": model_info["training"]["dataset_version"],
                    "hash": model_info["training"]["dataset_hash"],
                    "splits": model_info["training"]["splits"]
                },
                "hyperparameters": model_info["training"]["hyperparameters"],
                "training_config_hash": self._hash_config(model_info["training"]),
                "code": {
                    "git_commit": model_info["training"]["code"]["commit"],
                    "script": model_info["training"]["code"]["script"],
                    "dependencies": model_info["training"]["code"]["dependencies"]
                }
            },
            "evaluation": {
                "metrics": model_info["evaluation"]["metrics"],
                "test_set_hash": model_info["evaluation"]["test_set_hash"],
                "bias_metrics": model_info["evaluation"].get("bias_metrics", {})
            },
            "limitations": {
                "known_limitations": model_info.get("limitations", []),
                "bias_issues": model_info.get("bias_issues", []),
                "performance_characteristics": model_info.get("performance", {})
            },
            "provenance": {
                "created_by": model_info["provenance"]["created_by"],
                "created_at": model_info["provenance"]["created_at"],
                "lineage": self._build_lineage(model_id)
            }
        }
        
        return mbom
```

### 3. Adversarial Attack Defense

ป้องกันการโจมตีแบบ Adversarial

```python
class AdversarialDefense:
    """Defend against adversarial attacks on AI models"""
    
    def __init__(self):
        self.detection_models = {}
        self.defense_strategies = {
            "input_validation": self._validate_input,
            "adversarial_detection": self._detect_adversarial,
            "robust_inference": self._robust_inference,
            "output_filtering": self._filter_output
        }
    
    def defend_against_prompt_injection(
        self,
        user_input: str,
        model_id: str
    ) -> Dict:
        """
        Defend against prompt injection attacks.
        
        Detects and neutralizes injection attempts.
        """
        # Detect injection patterns
        injection_patterns = [
            r"ignore\s+(previous|above|all)",
            r"system\s*:",
            r"assistant\s*:",
            r"<\|.*?\|>",  # Special tokens
            r"\[INST\].*?\[/INST\]"  # Llama format
        ]
        
        detected = False
        for pattern in injection_patterns:
            if re.search(pattern, user_input, re.IGNORECASE):
                detected = True
                break
        
        if detected:
            # Sanitize input
            sanitized = self._sanitize_input(user_input)
            
            # Add defensive prompt
            defensive_prompt = self._get_defensive_prompt(model_id)
            protected_input = f"{defensive_prompt}\n\nUser: {sanitized}"
            
            return {
                "original_input": user_input,
                "sanitized_input": sanitized,
                "protected_input": protected_input,
                "injection_detected": True,
                "defense_applied": True
            }
        
        return {
            "original_input": user_input,
            "injection_detected": False,
            "defense_applied": False
        }
    
    def detect_data_poisoning(
        self,
        training_data: List[Dict],
        model_predictions: List[Dict]
    ) -> Dict:
        """
        Detect data poisoning in training data.
        
        Uses statistical analysis and anomaly detection.
        """
        # Analyze data distribution
        data_stats = self._analyze_data_distribution(training_data)
        
        # Detect anomalies
        anomalies = self._detect_anomalies(training_data, data_stats)
        
        # Check for backdoor patterns
        backdoor_signals = self._detect_backdoor_patterns(
            training_data, model_predictions
        )
        
        return {
            "poisoning_detected": len(anomalies) > 0 or len(backdoor_signals) > 0,
            "anomalies": anomalies,
            "backdoor_signals": backdoor_signals,
            "confidence": self._calculate_confidence(anomalies, backdoor_signals),
            "recommendation": self._generate_recommendation(anomalies, backdoor_signals)
        }
    
    def detect_backdoor_in_model(
        self,
        model_path: str,
        test_inputs: List[Dict]
    ) -> Dict:
        """
        Detect backdoors in pre-trained models.
        
        Tests model behavior on trigger patterns.
        """
        # Load model
        model = self._load_model(model_path)
        
        # Test with trigger patterns
        trigger_patterns = self._generate_trigger_patterns()
        
        backdoor_detected = False
        suspicious_behaviors = []
        
        for trigger in trigger_patterns:
            # Test with trigger
            output_with_trigger = model.predict(trigger["input"])
            output_without_trigger = model.predict(trigger["clean_input"])
            
            # Check if trigger causes unexpected behavior
            if self._is_suspicious_behavior(
                output_with_trigger,
                output_without_trigger,
                trigger["expected"]
            ):
                backdoor_detected = True
                suspicious_behaviors.append({
                    "trigger": trigger,
                    "behavior": {
                        "with_trigger": output_with_trigger,
                        "without_trigger": output_without_trigger
                    }
                })
        
        return {
            "backdoor_detected": backdoor_detected,
            "suspicious_behaviors": suspicious_behaviors,
            "risk_level": "high" if backdoor_detected else "low",
            "recommendation": "Do not use model" if backdoor_detected else "Model appears safe"
        }
```

### 4. Vulnerability Management for AI

จัดการช่องโหว่ใน ML Frameworks และ Models

```python
class AIVulnerabilityManager:
    """Manage vulnerabilities in AI/ML systems"""
    
    def __init__(self):
        self.cve_database = self._init_cve_database()
        self.vulnerability_scanner = self._init_scanner()
    
    def scan_model_vulnerabilities(
        self,
        model_id: str,
        model_path: str
    ) -> Dict:
        """
        Scan model and dependencies for vulnerabilities.
        
        Checks CVEs in ML frameworks, libraries, and model artifacts.
        """
        scan_result = {
            "model_id": model_id,
            "scanned_at": datetime.utcnow().isoformat(),
            "vulnerabilities": [],
            "risk_level": "low"
        }
        
        # Scan dependencies
        dependencies = self._extract_dependencies(model_path)
        for dep in dependencies:
            cves = self._check_cves(dep["name"], dep["version"])
            if cves:
                for cve in cves:
                    scan_result["vulnerabilities"].append({
                        "type": "dependency",
                        "component": dep["name"],
                        "version": dep["version"],
                        "cve": cve["id"],
                        "severity": cve["severity"],
                        "description": cve["description"],
                        "fix_available": cve.get("fix_version")
                    })
        
        # Scan model artifacts
        model_vulns = self._scan_model_artifacts(model_path)
        scan_result["vulnerabilities"].extend(model_vulns)
        
        # Calculate risk level
        if any(v["severity"] == "critical" for v in scan_result["vulnerabilities"]):
            scan_result["risk_level"] = "critical"
        elif any(v["severity"] == "high" for v in scan_result["vulnerabilities"]):
            scan_result["risk_level"] = "high"
        elif any(v["severity"] == "medium" for v in scan_result["vulnerabilities"]):
            scan_result["risk_level"] = "medium"
        
        return scan_result
    
    def assess_third_party_model(
        self,
        model_source: str,
        model_info: Dict
    ) -> Dict:
        """
        Assess risk of using third-party model.
        
        Checks reputation, SBOM, vulnerabilities, backdoors.
        """
        assessment = {
            "model_source": model_source,
            "assessed_at": datetime.utcnow().isoformat(),
            "risk_score": 0,
            "checks": {}
        }
        
        # Check 1: Source reputation
        source_reputation = self._check_source_reputation(model_source)
        assessment["checks"]["source_reputation"] = source_reputation
        assessment["risk_score"] += source_reputation.get("risk_score", 5)
        
        # Check 2: SBOM availability
        sbom_available = model_info.get("sbom") is not None
        assessment["checks"]["sbom_available"] = sbom_available
        if not sbom_available:
            assessment["risk_score"] += 3
        
        # Check 3: Vulnerability scan
        if model_info.get("model_path"):
            vuln_scan = self.scan_model_vulnerabilities(
                model_info["id"],
                model_info["model_path"]
            )
            assessment["checks"]["vulnerabilities"] = vuln_scan
            if vuln_scan["risk_level"] in ["high", "critical"]:
                assessment["risk_score"] += 5
        
        # Check 4: Backdoor detection
        if model_info.get("model_path"):
            backdoor_check = self._detect_backdoor_in_model(
                model_info["model_path"],
                model_info.get("test_inputs", [])
            )
            assessment["checks"]["backdoor"] = backdoor_check
            if backdoor_check["backdoor_detected"]:
                assessment["risk_score"] += 10
        
        # Overall recommendation
        if assessment["risk_score"] >= 15:
            assessment["recommendation"] = "Do not use - High risk"
        elif assessment["risk_score"] >= 10:
            assessment["recommendation"] = "Use with caution - Medium risk"
        else:
            assessment["recommendation"] = "Safe to use - Low risk"
        
        return assessment
```

### 5. Trusted AI Pipelines

สร้าง Pipeline ที่เชื่อถือได้

```python
class TrustedAIPipeline:
    """Build trusted AI pipelines with verification"""
    
    def __init__(self):
        self.signing_key = self._load_signing_key()
        self.attestation_service = self._init_attestation()
    
    def sign_model_artifact(
        self,
        model_path: str,
        metadata: Dict
    ) -> Dict:
        """
        Sign model artifact for integrity verification.
        
        Uses digital signatures to prevent tampering.
        """
        # Calculate hash
        model_hash = self._calculate_file_hash(model_path)
        
        # Create signature payload
        payload = {
            "model_hash": model_hash,
            "metadata": metadata,
            "signed_at": datetime.utcnow().isoformat()
        }
        
        # Sign payload
        signature = self._sign_payload(payload, self.signing_key)
        
        # Create signed artifact
        signed_artifact = {
            "model_path": model_path,
            "signature": signature,
            "payload": payload,
            "public_key": self._get_public_key()
        }
        
        return signed_artifact
    
    def verify_model_artifact(
        self,
        signed_artifact: Dict
    ) -> Dict:
        """
        Verify model artifact signature.
        
        Returns verification result.
        """
        # Verify signature
        signature_valid = self._verify_signature(
            signed_artifact["payload"],
            signed_artifact["signature"],
            signed_artifact["public_key"]
        )
        
        # Verify hash
        current_hash = self._calculate_file_hash(signed_artifact["model_path"])
        hash_valid = current_hash == signed_artifact["payload"]["model_hash"]
        
        return {
            "signature_valid": signature_valid,
            "hash_valid": hash_valid,
            "artifact_intact": signature_valid and hash_valid,
            "verified_at": datetime.utcnow().isoformat()
        }
    
    def create_attestation(
        self,
        pipeline_run_id: str,
        training_config: Dict,
        training_data_hash: str,
        model_hash: str
    ) -> Dict:
        """
        Create attestation for training pipeline.
        
        Proves that model was trained with specific config and data.
        """
        attestation = {
            "pipeline_run_id": pipeline_run_id,
            "attested_at": datetime.utcnow().isoformat(),
            "training_config_hash": self._hash_config(training_config),
            "training_data_hash": training_data_hash,
            "model_hash": model_hash,
            "attestation_signature": None
        }
        
        # Sign attestation
        attestation["attestation_signature"] = self._sign_payload(
            attestation,
            self.signing_key
        )
        
        # Store in attestation service
        self.attestation_service.store(attestation)
        
        return attestation
```

---

## Tooling & Tech Stack

### Enterprise Tools

- **SBOM Generation:**
  - CycloneDX (SBOM standard)
  - SPDX (Software Package Data Exchange)
  - Syft (SBOM generator)

- **Vulnerability Scanning:**
  - Snyk (dependency scanning)
  - GitHub Dependabot
  - OWASP Dependency-Check

- **Security Testing:**
  - Garak (LLM vulnerability scanner)
  - Counterfit (Microsoft ML security testing)
  - Adversarial Robustness Toolbox

### Configuration Essentials

```yaml
# ai-supply-chain-security-config.yaml
sbom:
  format: "CycloneDX"
  generate_on_build: true
  include_dependencies: true
  include_training_data: true

vulnerability_scanning:
  enabled: true
  frequency: "on_build, weekly"
  cve_database: "nvd"
  alert_on_critical: true

adversarial_defense:
  prompt_injection: true
  data_poisoning_detection: true
  backdoor_detection: true
  input_validation: true

trusted_pipeline:
  signing_enabled: true
  attestation_required: true
  verification_on_deploy: true
```

---

## Standards, Compliance & Security

### International Standards

- **NIST SSDF:** Secure Software Development Framework
- **OWASP ML Top 10:** Top 10 ML security risks
- **MITRE ATLAS:** Adversarial ML threat matrix
- **Executive Order 14028:** SBOM requirements

### Security Protocol

- **Digital Signatures:** Sign model artifacts
- **Hash Verification:** Verify model integrity
- **Attestation:** Prove training pipeline integrity
- **Air-gapped Training:** Isolated training environments

---

## Quick Start / Getting Ready

### Phase 1: SBOM Generation (Week 1-2)

1. **Generate SBOMs:**
   ```python
   sbom_gen = AISBOMGenerator()
   sbom = sbom_gen.generate_sbom("model-v1", "/path/to/model")
   ```

2. **Store SBOMs:**
   - Store with model artifacts
   - Make accessible for audits
   - Version control

### Phase 2: Vulnerability Scanning (Week 3-4)

1. **Set Up Scanning:**
   ```python
   vuln_mgr = AIVulnerabilityManager()
   scan = vuln_mgr.scan_model_vulnerabilities("model-v1", "/path/to/model")
   ```

2. **Automate Scanning:**
   - CI/CD integration
   - Regular scans
   - Alerting

---

## Production Checklist

- [ ] **SBOM:**
  - [ ] SBOMs generated for all models
  - [ ] MBOMs created
  - [ ] SBOMs stored and accessible

- [ ] **Vulnerability Management:**
  - [ ] Scanning automated
  - [ ] CVEs tracked
  - [ ] Patching process defined

- [ ] **Adversarial Defense:**
  - [ ] Input validation implemented
  - [ ] Injection detection enabled
  - [ ] Backdoor detection active

- [ ] **Trusted Pipeline:**
  - [ ] Model signing enabled
  - [ ] Attestation created
  - [ ] Verification on deploy

---

## Anti-patterns

### 1. **Using Models Without SBOM**
❌ **Bad:** Download and use model without checking SBOM
```python
# ❌ Bad - No verification
model = download_model("https://huggingface.co/model")  # Unknown components!
```

✅ **Good:** Check SBOM and verify before use
```python
# ✅ Good - Verify first
sbom = get_sbom(model_url)
if verify_sbom(sbom):
    assessment = assess_third_party_model(model_url, {"sbom": sbom})
    if assessment["risk_score"] < 10:
        model = download_model(model_url)
```

### 2. **Ignoring Vulnerabilities**
❌ **Bad:** Don't patch known vulnerabilities
```python
# ❌ Bad - Known CVE ignored
# CVE-2024-1234 in tensorflow==2.10.0
# But we keep using it anyway
```

✅ **Good:** Patch or mitigate vulnerabilities
```python
# ✅ Good - Patch vulnerabilities
vulns = scan_vulnerabilities(model)
for vuln in vulns:
    if vuln["severity"] in ["high", "critical"]:
        patch_or_mitigate(vuln)
```

---

## Timeline & Adoption Curve

### 2024-2025: Early Adoption
- Executive Order 14028 compliance
- SBOM tools mature
- Industry awareness increases

### 2025-2026: Mainstream
- SBOMs become standard
- Vulnerability scanning automated
- Regulatory requirements expand

### 2026-2027: Mandatory
- SBOMs required for all AI systems
- Vulnerability management standard
- Trusted pipelines mandatory

---

## Integration Points / Related Skills

- [Skill 76-80: Zero Trust Security](../74-iot-zero-trust-security/hardware-rooted-identity/SKILL.md) - Security foundations
- [Skill 123: LLM Security](../80-agentic-ai-advanced-learning/llm-security-redteaming/SKILL.md) - LLM security
- [Skill 93: Model Registry](../77-mlops-data-engineering/model-registry-versioning/SKILL.md) - Model versioning

---

## Further Reading

- [MITRE ATLAS](https://atlas.mitre.org/)
- [OWASP ML Top 10](https://owasp.org/www-project-machine-learning-security-top-10/)
- [NIST SSDF](https://csrc.nist.gov/Projects/ssdf)
- [CycloneDX](https://cyclonedx.org/)
- [Executive Order 14028](https://www.whitehouse.gov/briefing-room/presidential-actions/2021/05/12/executive-order-on-improving-the-nations-cybersecurity/)
