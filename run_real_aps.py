#!/usr/bin/env python3
"""
Simple test script to run the exporter with real APs
"""
import os

# Set environment variables for your real APs
os.environ['RUCKUS_AP_HOSTS'] = '192.168.1.58,192.168.1.29'
os.environ['SNMP_COMMUNITY'] = 'public'  # Change if needed
os.environ['ENABLE_TRIANGULATION'] = 'true'
os.environ['AP_COORDINATES'] = '192.168.1.58:0,0,2.5;192.168.1.29:20,0,2.5'
os.environ['DEMO_MODE'] = 'false'  # Use real data
os.environ['METRICS_PORT'] = '8000'
os.environ['SCRAPE_INTERVAL'] = '30'

print("🎯 Starting Ruckus AP Exporter with your real APs:")
print(f"  📡 APs: {os.environ['RUCKUS_AP_HOSTS']}")
print(f"  📍 Coordinates: {os.environ['AP_COORDINATES']}")
print(f"  🌐 Metrics: http://localhost:8000/metrics")
print(f"  🔄 Demo Mode: {os.environ['DEMO_MODE']}")
print("-" * 60)

# Import and run the main function
from ruckus_exporter import main

if __name__ == "__main__":
    main()