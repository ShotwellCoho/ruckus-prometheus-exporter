#!/usr/bin/env python3
"""
SNMP Diagnostic Tool for Ruckus AP
Tests different SNMP configurations to find working settings.
"""

import time
from pysnmp.hlapi import *

def test_snmp_connection(host, community, version='v2c'):
    """Test SNMP connection with given parameters."""
    print(f"Testing {host} with community '{community}' (SNMP {version})...")
    
    try:
        # Create SNMP version-specific data
        if version == 'v1':
            community_data = CommunityData(community, mpModel=0)  # SNMPv1
        else:
            community_data = CommunityData(community, mpModel=1)  # SNMPv2c
        
        for (errorIndication, errorStatus, errorIndex, varBinds) in getCmd(
            SnmpEngine(),
            community_data,
            UdpTransportTarget((host, 161), timeout=5, retries=1),
            ContextData(),
            ObjectType(ObjectIdentity('1.3.6.1.2.1.1.1.0'))  # sysDescr
        ):
            if errorIndication:
                print(f"  ❌ Error: {errorIndication}")
                return False
            elif errorStatus:
                print(f"  ❌ SNMP Error: {errorStatus.prettyPrint()}")
                return False
            else:
                for varBind in varBinds:
                    print(f"  ✅ SUCCESS: {varBind[1]}")
                    return True
    except Exception as e:
        print(f"  ❌ Exception: {e}")
        return False

def main():
    """Test various SNMP configurations."""
    host = '192.168.1.100'  # Replace with your Ruckus AP IP
    
    print("=== RUCKUS AP SNMP DIAGNOSTIC TOOL ===")
    print(f"Target: {host}")
    print(f"Testing common SNMP configurations...\n")
    
    # Test common community strings with SNMPv2c
    communities = ['public', 'private', 'admin', 'ruckus', 'community']
    
    print("Testing SNMPv2c...")
    for community in communities:
        if test_snmp_connection(host, community, 'v2c'):
            print(f"\n🎉 WORKING CONFIGURATION FOUND!")
            print(f"   Host: {host}")
            print(f"   Community: {community}")
            print(f"   Version: SNMPv2c")
            print(f"\nUpdate your exporter with:")
            print(f"   export RUCKUS_AP_HOST={host}")
            print(f"   export SNMP_COMMUNITY={community}")
            return
        time.sleep(1)
    
    print("\nTesting SNMPv1...")
    for community in communities:
        if test_snmp_connection(host, community, 'v1'):
            print(f"\n🎉 WORKING CONFIGURATION FOUND!")
            print(f"   Host: {host}")
            print(f"   Community: {community}")
            print(f"   Version: SNMPv1")
            print(f"\nNote: You may need to modify the exporter for SNMPv1")
            return
        time.sleep(1)
    
    print("\n❌ NO WORKING SNMP CONFIGURATION FOUND")
    print("\nPossible solutions:")
    print("1. Check if SNMP is enabled on the Ruckus AP")
    print("2. Verify the IP address is correct")
    print("3. Check network connectivity")
    print("4. Try accessing AP web interface and enable SNMP")
    print("5. Check firewall settings")

if __name__ == '__main__':
    main()