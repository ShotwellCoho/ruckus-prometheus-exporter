#!/usr/bin/env python3
"""
Local test script for Ruckus AP monitoring with triangulation
"""
import os
import sys
import time
from prometheus_client import start_http_server
from ruckus_exporter import RuckusAPExporter

def main():
    # Set up environment for testing with real APs
    os.environ['RUCKUS_AP_HOSTS'] = '192.168.1.100,192.168.1.101'
    os.environ['SNMP_COMMUNITY'] = 'public'  # Change if needed
    os.environ['ENABLE_TRIANGULATION'] = 'true'
    os.environ['AP_COORDINATES'] = '192.168.1.100:0,0,2.5;192.168.1.101:20,0,2.5'
    os.environ['DEMO_MODE'] = 'false'  # Use real data
    
    print("🎯 Starting Ruckus AP Exporter with Triangulation")
    print(f"APs: {os.environ['RUCKUS_AP_HOSTS']}")
    print(f"Coordinates: {os.environ['AP_COORDINATES']}")
    print(f"Demo Mode: {os.environ['DEMO_MODE']}")
    print("-" * 50)
    
    # Parse configuration
    ap_hosts = ['192.168.1.58', '192.168.1.29']
    ap_coordinates = {
        '192.168.1.58': (0, 0, 2.5),
        '192.168.1.29': (20, 0, 2.5)
    }
    
    try:
        # Initialize the exporter
        print("Initializing exporter...")
        exporter = RuckusAPExporter(
            ap_hosts=ap_hosts,
            snmp_community='public',
            port=161,
            enable_triangulation=True,
            ap_coordinates=ap_coordinates
        )
        
        # Start metrics server on port 8000
        print("Starting metrics server on http://localhost:8000")
        start_http_server(8000)
        
        print("\n📊 Metrics available at:")
        print("  • http://localhost:8000/metrics - All metrics")
        print("  • Look for 'ruckus_client_rssi_dbm' for RSSI data")
        print("  • Look for 'ruckus_client_location_*' for triangulation")
        
        # Run a few collection cycles to test
        for i in range(3):
            print(f"\n--- Collection Cycle {i+1} ---")
            start_time = time.time()
            
            try:
                # Collect metrics
                exporter.collect_metrics()
                print("✅ Metrics collection completed")
            except Exception as e:
                print(f"❌ Collection error: {e}")
                import traceback
                traceback.print_exc()
            
            duration = time.time() - start_time
            print(f"⚡ Collection took {duration:.2f} seconds")
            
            if i < 2:  # Don't sleep on last iteration
                print("Waiting 10 seconds for next collection...")
                time.sleep(10)
        
        print("\n🌐 Test complete! Check metrics at http://localhost:8000/metrics")
        print("\n🚀 To run continuously, press Ctrl+C to stop, then run:")
        print("python test_local.py --serve")
        
    except KeyboardInterrupt:
        print("\n👋 Shutting down...")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--serve":
        # Continuous mode - just run the main exporter
        os.environ['RUCKUS_AP_HOSTS'] = '192.168.1.58,192.168.1.29'
        os.environ['SNMP_COMMUNITY'] = 'public'
        os.environ['ENABLE_TRIANGULATION'] = 'true'
        os.environ['AP_COORDINATES'] = '192.168.1.58:0,0,2.5;192.168.1.29:20,0,2.5'
        os.environ['DEMO_MODE'] = 'false'
        
        from ruckus_exporter import main as exporter_main
        exporter_main()
    else:
        main()