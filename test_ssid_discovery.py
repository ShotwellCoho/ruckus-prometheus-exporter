#!/usr/bin/env python3

import asyncio
from pysnmp.hlapi import *

def test_ssid_discovery():
    ap_host = '192.168.1.58'
    community = 'public'
    
    print(f'Testing SSID discovery on {ap_host}...')
    
    # Try the SSID name OID that should work for Ruckus
    ssid_oids = [
        '1.3.6.1.4.1.25053.1.2.1.4.1.1.3',  # Main SSID table
        '1.3.6.1.4.1.25053.1.2.2.1.1.2.1.1.2',  # Alternative SSID table
        '1.3.6.1.4.1.25053.1.15.1.1.1.1.9',  # WLAN SSID table
        '1.3.6.1.4.1.25053.1.1.1.1.1.1.2',  # Another possible SSID table
    ]
    
    for oid in ssid_oids:
        print(f'\nTrying OID: {oid}')
        try:
            iterator = nextCmd(
                SnmpEngine(),
                CommunityData(community),
                UdpTransportTarget((ap_host, 161)),
                ContextData(),
                ObjectType(ObjectIdentity(oid)),
                lexicographicMode=False,
                ignoreNonIncreasingOid=True,
                maxRows=10)
            
            for (errorIndication, errorStatus, errorIndex, varBinds) in iterator:
                if errorIndication:
                    print(f'  Error: {errorIndication}')
                    break
                elif errorStatus:
                    error_msg = f'  SNMP Error: {errorStatus.prettyPrint()}'
                    if errorIndex:
                        error_msg += f' at {varBinds[int(errorIndex) - 1][0]}'
                    print(error_msg)
                    break
                else:
                    for varBind in varBinds:
                        oid_str, value = varBind
                        print(f'  Found: {oid_str} = {value}')
        except Exception as e:
            print(f'  Exception: {e}')

if __name__ == '__main__':
    test_ssid_discovery()