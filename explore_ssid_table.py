#!/usr/bin/env python3

from pysnmp.hlapi import *

def explore_ssid_table(host):
    '''Explore the SSID table we just discovered'''
    print(f'🔍 Exploring SSID table 1.3.6.1.4.1.25053.1.1.6 on {host}')
    
    ssid_table_base = '1.3.6.1.4.1.25053.1.1.6'
    
    try:
        all_data = []
        
        for (errorIndication, errorStatus, errorIndex, varBinds) in nextCmd(
            SnmpEngine(),
            CommunityData('public'),
            UdpTransportTarget((host, 161)),
            ContextData(),
            ObjectType(ObjectIdentity(ssid_table_base)),
            lexicographicMode=False,
            maxRows=50):
            
            if errorIndication or errorStatus:
                break
                
            for varBind in varBinds:
                oid = str(varBind[0])
                value = str(varBind[1])
                
                if not oid.startswith(ssid_table_base):
                    break
                    
                if value and value.strip():
                    all_data.append((oid, value))
                    
        print(f'Found {len(all_data)} entries in SSID table:')
        
        # Group by pattern to understand the structure
        ssid_entries = {}
        other_entries = []
        
        for oid, value in all_data:
            # Look for SSID-like values (alphabetic strings)
            if any(char.isalpha() for char in value) and len(value.strip()) <= 32:
                # Extract the index pattern
                parts = oid.split('.')
                if len(parts) >= 10:
                    # Pattern like 1.3.6.1.4.1.25053.1.1.6.1.1.1.1.1.1.X
                    index = parts[-1]  # Last part is the index
                    base_oid = '.'.join(parts[:-1])  # Everything except last part
                    
                    if base_oid not in ssid_entries:
                        ssid_entries[base_oid] = {}
                    ssid_entries[base_oid][index] = value
                    
                    print(f'  📡 SSID entry: {oid} = {value}')
            else:
                other_entries.append((oid, value))
                print(f'  📊 Other: {oid} = {value}')
        
        # Analyze patterns
        print(f'\n🔍 SSID table structure analysis:')
        for base_oid, indices in ssid_entries.items():
            print(f'  Base OID: {base_oid}')
            for index, ssid in indices.items():
                print(f'    Index {index}: {ssid}')
        
        return ssid_entries, other_entries
        
    except Exception as e:
        print(f'Error exploring SSID table: {e}')
        return {}, []

def find_client_counts_for_ssids(host, ssid_entries):
    '''Try to find client counts for discovered SSIDs'''
    print(f'\n🔍 Looking for client counts in related OIDs...')
    
    client_mappings = {}
    
    for base_oid, indices in ssid_entries.items():
        for index, ssid in indices.items():
            print(f'\n📡 Checking for client data for SSID "{ssid}" (index {index}):')
            
            # Try different potential client count OIDs
            potential_client_oids = [
                # Try different columns in the same table
                base_oid.replace('.1.1.1.1.1.1', '.1.1.1.1.1.2'),  # Next column
                base_oid.replace('.1.1.1.1.1.1', '.1.1.1.1.1.3'),  # Another column
                base_oid.replace('.1.1.1.1.1.1', '.1.1.1.1.2.1'),  # Different sub-table
                base_oid.replace('.1.1.1.1.1.1', '.1.1.1.2.1.1'),  # Another pattern
                base_oid.replace('.1.1.1.1.1.1', '.1.1.2.1.1.1'),  # Yet another pattern
                base_oid.replace('.1.1.1.1.1.1', '.1.2.1.1.1.1'),  # And another
            ]
            
            found_values = []
            
            for test_oid in potential_client_oids:
                try:
                    full_oid = f'{test_oid}.{index}'
                    
                    for (errorIndication, errorStatus, errorIndex, varBinds) in getCmd(
                        SnmpEngine(),
                        CommunityData('public'),
                        UdpTransportTarget((host, 161)),
                        ContextData(),
                        ObjectType(ObjectIdentity(full_oid))):
                        
                        if not errorIndication and not errorStatus:
                            for varBind in varBinds:
                                value = str(varBind[1])
                                if value and value.strip():
                                    found_values.append((full_oid, value))
                                    if value.isdigit():
                                        print(f'    ✅ Potential client count in {full_oid}: {value}')
                                    else:
                                        print(f'    📝 Other data in {full_oid}: {value}')
                                        
                except Exception as e:
                    pass  # Ignore errors for non-existent OIDs
            
            if found_values:
                client_mappings[ssid] = found_values
    
    return client_mappings

def create_dynamic_ssid_discovery_function():
    '''Generate code for dynamic SSID discovery based on our findings'''
    code = '''
def discover_ssids_dynamically(self, ap_host):
    """
    🎯 Dynamically discover SSIDs and their client counts from SNMP
    Based on discovered OID: 1.3.6.1.4.1.25053.1.1.6.1.1.1.1.1.1
    """
    ssid_client_map = {}
    
    try:
        # Base OID for SSID names 
        ssid_name_base = "1.3.6.1.4.1.25053.1.1.6.1.1.1.1.1.1"
        
        # Walk the SSID table to get all configured SSIDs
        ssid_data = self.snmp_walk(ap_host, ssid_name_base)
        
        if ssid_data:
            logger.info(f"🔍 Found SSID table data for {ap_host}: {len(ssid_data)} entries")
            
            for oid, ssid_name in ssid_data.items():
                if ssid_name and str(ssid_name).strip():
                    # Extract the index from the OID
                    index = oid.split('.')[-1]
                    ssid_str = str(ssid_name).strip()
                    
                    logger.info(f"📡 Found SSID: {ssid_str} (index: {index})")
                    
                    # Try to get client count from related OIDs
                    client_count = 0
                    
                    # Try different potential client count OIDs
                    client_oid_patterns = [
                        f"1.3.6.1.4.1.25053.1.1.6.1.1.1.1.1.2.{index}",  # Next column
                        f"1.3.6.1.4.1.25053.1.1.6.1.1.1.1.2.1.{index}",  # Different sub-table
                        f"1.3.6.1.4.1.25053.1.1.6.1.1.1.2.1.1.{index}",  # Another pattern
                    ]
                    
                    for client_oid in client_oid_patterns:
                        try:
                            count = self.snmp_get(ap_host, client_oid)
                            if count is not None and str(count).isdigit():
                                client_count = int(count)
                                logger.info(f"📊 Found client count for {ssid_str}: {client_count}")
                                break
                        except:
                            continue
                    
                    # If no direct client count found, estimate from interface traffic
                    if client_count == 0:
                        # Map SSID index to interface (this is AP-specific logic)
                        interface_mapping = {
                            '0': 'wlan1',  # Based on screenshot: Wireless 1 = Jeff
                            '8': 'wlan8',  # Wireless 8
                            '10': 'wlan10' # Wireless 10
                        }
                        
                        if index in interface_mapping:
                            interface_name = interface_mapping[index]
                            # Use interface traffic to estimate clients
                            client_count = self.estimate_clients_from_interface_traffic(ap_host, interface_name)
                    
                    ssid_client_map[ssid_str] = client_count
                    
        return ssid_client_map
        
    except Exception as e:
        logger.error(f"❌ Error in dynamic SSID discovery for {ap_host}: {e}")
        return {}
'''
    
    print("\n🔧 Generated dynamic SSID discovery function:")
    print(code)
    return code

if __name__ == "__main__":
    # Explore the table
    ssids, others = explore_ssid_table('192.168.1.58')
    
    if ssids:
        # Look for client counts
        client_data = find_client_counts_for_ssids('192.168.1.58', ssids)
        
        print(f'\n📊 Summary of SSID mappings found:')
        for ssid, data in client_data.items():
            print(f'  SSID: {ssid}')
            for oid, value in data:
                print(f'    {oid}: {value}')
        
        # Generate the discovery function
        create_dynamic_ssid_discovery_function()
    else:
        print("No SSID data found")