# System Security Plan (SSP) 

**System Name:** CIP/OT-Sandbox  
**Categorization:** MODERATE Impact  
**Version:** 1.0  
**Date:** 2026-06-26  

## 1. System Description & Purpose
The CIP/OT-Sandbox is a containerized, container-orchestrated environment designed to emulate industrial control network segments. Its primary purpose is to research defensive security controls, validate configuration baselines, and automate compliance auditing for industrial-grade network nodes.

## 2. Network Architecture & Segmentation
The environment utilizes Docker-based containerization to simulate isolated network zones:
* **Management Zone:** A dedicated container running the Python-based audit suite and Nmap for network reconnaissance.
* **Service Zone:** Containers simulating Industrial Data Historians, communicating over standard OT protocols.
* **Restricted OT Zone:** Containers simulating PLCs, with traffic restricted to approved ports only via custom Docker network policies.

## 3. Security Control Implementation
### 3.1 Access Control (AC)
* **SSH Key Enforcement:** All access to simulated nodes is restricted to SSH key-based authentication. Passwords are disabled.
* **Least Privilege:** The automated audit suite runs under a dedicated, non-privileged service account to limit system impact.

### 3.2 Configuration Management (CM)
* **Baseline Integrity:** All container configurations are defined in `docker-compose.yml` files (Infrastructure-as-Code).
* **Automated Auditing:** The `cip_asset_scan.py` script continuously compares the active container port state against the defined security baseline.

### 3.3 Identification & Authentication (IA)
* **Network Access:** Docker network bridges are configured to enforce strict micro-segmentation, preventing unauthorized lateral movement between the OT Zone and Management Zone.

## 4. Maintenance & Continuous Monitoring
* **Vulnerability Scanning:** Automated audits are conducted upon every container initialization.
* **Logging:** Audit logs and compliance results are exported to localized CSV artifacts for manual review and baseline validation.

## 5. Incident Response & Contingency (IR)
* **Containment:** If a containerized node displays anomalous behavior (e.g., unauthorized port opening), the node is programmatically isolated via `docker network disconnect`.
* **Disaster Recovery:** The lab utilizes container-based redeployment. If a simulated node is compromised, it is destroyed and redeployed from a "known-good" container image.
