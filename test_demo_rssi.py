#!/usr/bin/env python3
"""
Test RSSI with demo mode enabled to verify the triangulation system works
"""
import os

# Set environment for demo mode testing
os.environ['RUCKUS_AP_HOSTS'] = '192.168.1.58,192.168.1.29'
os.environ['SNMP_COMMUNITY'] = 'public'
os.environ['ENABLE_TRIANGULATION'] = 'true'
os.environ['AP_COORDINATES'] = '192.168.1.58:0,0,2.5;192.168.1.29:20,0,2.5'
os.environ['DEMO_MODE'] = 'true'  # Enable demo mode for RSSI testing
os.environ['METRICS_PORT'] = '8001'  # Different port to avoid conflicts
os.environ['SCRAPE_INTERVAL'] = '15'  # Faster for testing

print("🧪 Starting RSSI Demo Mode Test")
print("=" * 50)
print("This will generate fake RSSI data to test triangulation")
print("📊 Metrics: http://localhost:8001/metrics")
print("🔍 Look for:")
print("  • ruckus_client_rssi_dbm")
print("  • ruckus_client_location_x_meters")
print("  • ruckus_client_location_y_meters")
print("  • ruckus_client_location_confidence")
print("\nPress Ctrl+C to stop...")

from ruckus_exporter import main

if __name__ == "__main__":
    main()