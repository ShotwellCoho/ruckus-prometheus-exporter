#!/usr/bin/env python3
"""
Test RSSI functionality with demo mode first, then real APs
"""
import os
import subprocess
import sys

def test_demo_mode():
    """Test with demo mode to verify RSSI metrics work"""
    print("🧪 Testing RSSI collection with DEMO MODE...")
    
    # Set demo mode environment
    env = os.environ.copy()
    env['RUCKUS_AP_HOSTS'] = '192.168.1.58,192.168.1.29'
    env['SNMP_COMMUNITY'] = 'public'
    env['ENABLE_TRIANGULATION'] = 'true'
    env['AP_COORDINATES'] = '192.168.1.58:0,0,2.5;192.168.1.29:20,0,2.5'
    env['DEMO_MODE'] = 'true'  # Use demo data first
    env['METRICS_PORT'] = '8001'  # Different port
    
    print("Starting demo mode exporter...")
    print("This will generate fake RSSI data to test the triangulation system")
    print("Open http://localhost:8001/metrics in your browser to see the data")
    print("Press Ctrl+C to stop and test with real APs")
    
    try:
        # Run in demo mode
        subprocess.run([sys.executable, 'ruckus_exporter.py'], env=env)
    except KeyboardInterrupt:
        print("\n✅ Demo mode test complete!")
        
def test_real_aps():
    """Test with real APs"""
    print("\n🎯 Testing RSSI collection with REAL APs...")
    
    # Set real AP environment 
    env = os.environ.copy()
    env['RUCKUS_AP_HOSTS'] = '192.168.1.58,192.168.1.29'
    env['SNMP_COMMUNITY'] = 'public'
    env['ENABLE_TRIANGULATION'] = 'true'
    env['AP_COORDINATES'] = '192.168.1.58:0,0,2.5;192.168.1.29:20,0,2.5'
    env['DEMO_MODE'] = 'false'  # Use real data
    env['METRICS_PORT'] = '8000'
    
    print("Starting real AP exporter...")
    print("This will try to collect actual RSSI data from your APs")
    print("Open http://localhost:8000/metrics in your browser to see the data")
    print("Look for 'ruckus_client_rssi_dbm' metrics")
    print("Press Ctrl+C to stop")
    
    try:
        # Run with real APs
        subprocess.run([sys.executable, 'ruckus_exporter.py'], env=env)
    except KeyboardInterrupt:
        print("\n✅ Real AP test complete!")

if __name__ == "__main__":
    print("🔧 RSSI Data Collection Testing")
    print("=" * 50)
    
    choice = input("\nChoose test mode:\n1. Demo mode (fake data)\n2. Real APs\n3. Both (demo first, then real)\n\nEnter choice (1-3): ").strip()
    
    if choice == "1":
        test_demo_mode()
    elif choice == "2":
        test_real_aps()
    elif choice == "3":
        test_demo_mode()
        test_real_aps()
    else:
        print("Invalid choice. Running demo mode...")
        test_demo_mode()