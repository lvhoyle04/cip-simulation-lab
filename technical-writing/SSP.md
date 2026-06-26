# System Security Plan (SSP) 

**System Name:** Upstate Substation Alpha (Fictional OT Environment)  
**System Categorization:** HIGH Impact (FIPS 199)  
**Operational Status:** Active Simulation  

## 1. System Description & Purpose
This system emulates a localized power distribution substation utilizing simulated Programmable Logic Controllers (PLCs) and remote terminal units. The purpose of this environment is to test configuration baselines, execute intermediate Python-based vulnerability scanners, and validate Electronic Security Perimeter (ESP) integrity without jeopardizing enterprise IT networks.

## 2. Network Architecture & Segmentation (CIP-005)
To ensure isolation from standard internet traffic, the architecture is segmented into three distinct zones:
*   **Corporate IT Zone:** Standard internet-facing VLAN for general business operations.
*   **Industrial DMZ:** Houses the data historians and patch management servers. Acts as the sole bridge between IT and OT.
*   **Operational Technology (OT) Zone:** Air-gapped network segment containing the PLCs and critical control hardware. Strict Deny-All inbound firewall rules applied.

## 3. Baseline Security Controls (CIP-007)
### 3.1 Ports and Services Management
*   Only ports explicitly required for operations (e.g., Modbus TCP Port 502, DNP3 Port 20000) are enabled on the industrial hardware.
*   Telnet (Port 23) and FTP (Port 21) are strictly disabled at the host level across all OT devices.

### 3.2 Malicious Code Prevention
*   Anti-malware signatures are updated manually via physical USB transfer to maintain the air-gap integrity.
*   Continuous monitoring scripts audit the file integrity of all active logic controllers every 24 hours to detect unauthorized configuration changes.

## 4. Incident Response & Containment (CIP-008)
In the event of anomalous network traffic detected within the OT Zone, the primary response action is the physical disconnection of the managed switch uplink to the DMZ. Logical containment protocols follow the standard CISA ICS playbooks to ensure malware cannot bridge the Electronic Security Perimeter.
