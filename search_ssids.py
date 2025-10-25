#!/usr/bin/env python3

from pysnmp.hlapi import *

def search_for_ssid_names(host, target_ssid='MyNetwork'):
    '''Search systematically for SSID names in SNMP tree'''
    print(f'\n🔍 Searching for SSID "{target_ssid}" in SNMP tree on {host}')
    
    # More comprehensive search of Ruckus enterprise branches
    search_branches = [
        # Main Ruckus enterprise branches
        '1.3.6.1.4.1.25053.1.1',      # System/Config
        '1.3.6.1.4.1.25053.1.2',      # WLAN  
        '1.3.6.1.4.1.25053.1.3',      # Radio
        '1.3.6.1.4.1.25053.1.4',      # Wireless
        '1.3.6.1.4.1.25053.1.5',      # Network
        '1.3.6.1.4.1.25053.1.6',      # Interface
        '1.3.6.1.4.1.25053.1.7',      # VAP
        '1.3.6.1.4.1.25053.1.8',      # BSS
        '1.3.6.1.4.1.25053.1.9',      # Station
        '1.3.6.1.4.1.25053.1.10',     # Management
        '1.3.6.1.4.1.25053.1.11',     # Configuration
        '1.3.6.1.4.1.25053.1.12',     # Status
        '1.3.6.1.4.1.25053.1.13',     # Statistics
        '1.3.6.1.4.1.25053.1.14',     # Security  
        '1.3.6.1.4.1.25053.1.15',     # SSID
        '1.3.6.1.4.1.25053.2',        # Alternative branch
        '1.3.6.1.4.1.25053.3',        # Management branch (we found some data here)
    ]
    
    found_ssids = []
    
    for branch in search_branches:
        print(f'\n📡 Searching branch {branch}...')
        try:
            string_values = []
            
            for (errorIndication, errorStatus, errorIndex, varBinds) in nextCmd(
                SnmpEngine(),
                CommunityData('public'),
                UdpTransportTarget((host, 161)),
                ContextData(),
                ObjectType(ObjectIdentity(branch)),
                lexicographicMode=False,
                maxRows=100):  # Search deeper
                
                if errorIndication or errorStatus:
                    break
                    
                for varBind in varBinds:
                    oid = str(varBind[0])
                    value = str(varBind[1])
                    
                    if not oid.startswith(branch):
                        break
                        
                    # Look for string values that could be SSID names
                    if value and len(value.strip()) > 0:
                        # Check if it contains our target SSID
                        if target_ssid.lower() in value.lower():
                            found_ssids.append((oid, value, 'EXACT_MATCH'))
                            print(f'  🎯 FOUND "{target_ssid}" in {oid}: {value}')
                        
                        # Look for other potential SSID-like strings
                        elif (any(char.isalpha() for char in value) and 
                              len(value.strip()) <= 32 and  # SSIDs are max 32 chars
                              not any(bad in value.lower() for bad in ['error', 'timeout', 'null', 'none']) and
                              not value.isdigit()):  # Not just numbers
                            string_values.append((oid, value))
                            
            # Show other interesting strings found
            if string_values and len(string_values) <= 10:  # Don't spam too much
                print(f'  📝 Other strings in {branch}:')
                for oid, value in string_values[:5]:  # Show first 5
                    display_val = value[:30] + '...' if len(value) > 30 else value
                    print(f'    {oid}: {display_val}')
                if len(string_values) > 5:
                    print(f'    ... and {len(string_values) - 5} more')
                    
        except Exception as e:
            print(f'  ❌ Error searching {branch}: {e}')
    
    return found_ssids

def test_specific_ssid_oids(host):
    '''Test some specific OIDs that commonly contain SSID information'''
    print(f'\n🎯 Testing specific SSID-related OIDs on {host}')
    
    # Common SSID OIDs to test
    ssid_oids = [
        # Standard wireless OIDs
        '1.2.840.10036.1.1.1.1.2',     # dot11DesiredSSID
        '1.2.840.10036.1.1.1.1.5',     # dot11OperationalRateSet
        '1.2.840.10036.2.1.1.2',       # dot11NetworkName
        
        # Ruckus specific attempts
        '1.3.6.1.4.1.25053.1.15.1.1.1.2',   # Possible SSID table
        '1.3.6.1.4.1.25053.1.2.1.1.1.2',    # WLAN table entry
        '1.3.6.1.4.1.25053.1.7.1.1.1.2',    # VAP table entry
        '1.3.6.1.4.1.25053.1.8.1.1.1.2',    # BSS table entry
    ]
    
    found_data = []
    
    for test_oid in ssid_oids:
        print(f'\n🔍 Testing {test_oid}...')
        try:
            for (errorIndication, errorStatus, errorIndex, varBinds) in nextCmd(
                SnmpEngine(),
                CommunityData('public'),
                UdpTransportTarget((host, 161)),
                ContextData(),
                ObjectType(ObjectIdentity(test_oid)),
                lexicographicMode=False,
                maxRows=20):
                
                if errorIndication or errorStatus:
                    break
                    
                for varBind in varBinds:
                    oid = str(varBind[0])
                    value = str(varBind[1])
                    
                    if not oid.startswith(test_oid):
                        break
                        
                    if value and value.strip():
                        found_data.append((oid, value))
                        print(f'  ✅ {oid}: {value}')
                        
                if len(found_data) >= 5:
                    break
                    
            if not any(data[0].startswith(test_oid) for data in found_data):
                print(f'  ❌ No data found')
                
        except Exception as e:
            print(f'  ❌ Error: {e}')
    
    return found_data

if __name__ == "__main__":
    # Search for example SSID specifically
    found = search_for_ssid_names('192.168.1.100', 'MyNetwork')
    
    if found:
        print(f'\n🎯 Summary: Found {len(found)} matches for "MyNetwork":')
        for oid, value, match_type in found:
            print(f'  {match_type}: {oid} = {value}')
    else:
        print(f'\n❌ No direct matches for "MyNetwork" found in SNMP tree')
        print('Trying specific SSID OIDs...')
        
        # Try specific OIDs
        specific_data = test_specific_ssid_oids('192.168.1.100')
        
        if specific_data:
            print(f'\n📊 Found {len(specific_data)} entries in specific OID tests:')
            for oid, value in specific_data:
                print(f'  {oid}: {value}')