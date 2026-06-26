#!/usr/bin/env python3
"""
CIP-007 Asset Compliance Scanner
Purpose: Audits active TCP ports on a target asset against an approved ICS/OT baseline.
Outputs a compliance report identifying unauthorized listening services.
"""

import socket
import csv
from datetime import datetime

# ==========================================
# CONFIGURATION & BASELINE
# ==========================================

# Target asset (Defaulting to localhost for safe sandbox testing)
TARGET_IP = '127.0.0.1' 

# The "Golden Baseline" of approved ports for this specific OT asset type
APPROVED_TCP_PORTS = {
    22: "SSH (Encrypted Admin Access)",
    443: "HTTPS (Encrypted Web Interface)",
    502: "Modbus TCP (Industrial Control Traffic)",
    20000: "DNP3 (Substation SCADA Traffic)"
}

# Common high-risk ports to actively scan for violations
PORTS_TO_SCAN = [21, 22, 23, 80, 443, 502, 3389, 8080, 20000]

# ==========================================
# SCANNING ENGINE
# ==========================================

def scan_ports(ip, port_list):
    """Attempts a socket connection to determine if a port is open."""
    open_ports = []
    print(f"[*] Initiating CIP compliance scan on {ip}...")
    
    for port in port_list:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5) # Fast timeout for local testing
        result = sock.connect_ex((ip, port))
        
        if result == 0:
            open_ports.append(port)
        sock.close()
        
    return open_ports

# ==========================================
# COMPLIANCE VALIDATION & REPORTING
# ==========================================

def generate_report(open_ports):
    """Compares open ports against the baseline and writes a CSV report."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"cip_compliance_report_{timestamp}.csv"
    
    violations_found = 0
    
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Timestamp', 'Asset IP', 'Port', 'Status', 'Remediation Action'])
        
        print("\n--- COMPLIANCE RESULTS ---")
        for port in open_ports:
            if port in APPROVED_TCP_PORTS:
                status = "COMPLIANT"
                action = "None - Matches Golden Baseline"
                print(f"[PASS] Port {port} is open (Approved: {APPROVED_TCP_PORTS[port]})")
            else:
                status = "VIOLATION"
                action = "IMMEDIATE ACTION: Disable unauthorized service"
                violations_found += 1
                print(f"[FAIL] Port {port} is open (UNAUTHORIZED)")
                
            writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), TARGET_IP, port, status, action])
            
    print(f"\n[*] Scan complete. {violations_found} violation(s) found.")
    print(f"[*] Detailed audit log saved to: {filename}")

if __name__ == "__main__":
    try:
        active_ports = scan_ports(TARGET_IP, PORTS_TO_SCAN)
        generate_report(active_ports)
    except KeyboardInterrupt:
        print("\n[!] Scan aborted by user.")
    except Exception as e:
        print(f"\n[!] An error occurred during the audit: {e}")
