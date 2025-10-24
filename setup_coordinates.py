#!/usr/bin/env python3
"""
🎯 AP Coordinate Setup Assistant
==============================

Interactive tool to help you configure AP coordinates for triangulation.
Perfect for setting up your Vault-Tec facility monitoring! 📡⚔️
"""

import math
import json
from typing import Dict, Tuple, List


class APCoordinateSetup:
    """Interactive setup assistant for AP coordinates"""
    
    def __init__(self):
        self.aps = {}
        self.environment_type = "indoor"
        
    def run_interactive_setup(self):
        """Run the interactive setup wizard"""
        print("🎯 Wasteland Wireless Monitoring - AP Coordinate Setup")
        print("=" * 60)
        print("Welcome, vault dweller! Let's configure your AP positions for")
        print("optimal client tracking across the wasteland.\n")
        
        # Get environment info
        self.get_environment_info()
        
        # Get AP information
        self.get_ap_information()
        
        # Generate configurations
        self.generate_configurations()
        
    def get_environment_info(self):
        """Get information about the environment"""
        print("📐 Environment Setup")
        print("-" * 20)
        
        env_types = {
            "1": ("indoor", "Indoor office/building (2.5m ceiling)"),
            "2": ("vault", "Vault-Tec facility (3.0m ceiling)"),
            "3": ("outdoor", "Outdoor area"),
            "4": ("custom", "Custom environment")
        }
        
        print("Select your environment type:")
        for key, (env_type, description) in env_types.items():
            print(f"  {key}. {description}")
        
        choice = input("\nEnvironment [1]: ").strip() or "1"
        
        if choice in env_types:
            self.environment_type = env_types[choice][0]
            print(f"✅ Selected: {env_types[choice][1]}\n")
        else:
            self.environment_type = "indoor"
            print("✅ Defaulting to indoor environment\n")
            
    def get_ap_information(self):
        """Get AP IP addresses and positions"""
        print("📡 Access Point Configuration")
        print("-" * 30)
        
        # Get number of APs
        while True:
            try:
                num_aps = int(input("How many APs do you have? [2]: ") or "2")
                if num_aps >= 2:
                    break
                else:
                    print("❌ You need at least 2 APs for triangulation")
            except ValueError:
                print("❌ Please enter a valid number")
        
        print(f"\n🔧 Configuring {num_aps} Access Points")
        print("Tip: Use a floor plan or measure distances from a corner origin point\n")
        
        for i in range(num_aps):
            print(f"AP #{i+1}:")
            
            # Get IP address
            while True:
                ip = input(f"  IP address [192.168.1.{100+i}]: ").strip()
                if not ip:
                    ip = f"192.168.1.{100+i}"
                if self.is_valid_ip(ip):
                    break
                else:
                    print("  ❌ Invalid IP address format")
            
            # Get coordinates
            print("  📍 Position (in meters from origin point):")
            
            try:
                x = float(input(f"    X coordinate [{ i * 20}]: ") or str(i * 20))
                y = float(input("    Y coordinate [0]: ") or "0")
                
                if self.environment_type == "vault":
                    default_z = "3.0"
                elif self.environment_type == "outdoor":
                    default_z = "4.0"
                else:
                    default_z = "2.5"
                    
                z = float(input(f"    Z coordinate (height) [{default_z}]: ") or default_z)
                
                self.aps[ip] = (x, y, z)
                print(f"  ✅ AP {ip} positioned at ({x}, {y}, {z})\n")
                
            except ValueError:
                print("  ❌ Invalid coordinates, using defaults")
                self.aps[ip] = (i * 20, 0, 2.5)
    
    def is_valid_ip(self, ip: str) -> bool:
        """Validate IP address format"""
        parts = ip.split('.')
        if len(parts) != 4:
            return False
        try:
            return all(0 <= int(part) <= 255 for part in parts)
        except ValueError:
            return False
    
    def generate_configurations(self):
        """Generate configuration strings and files"""
        print("🚀 Generated Configuration")
        print("=" * 40)
        
        # Generate environment variable
        ap_coords_str = ";".join([f"{ip}:{x},{y},{z}" for ip, (x, y, z) in self.aps.items()])
        ap_hosts_str = ",".join(self.aps.keys())
        
        print("📋 Environment Variables:")
        print(f'RUCKUS_AP_HOSTS="{ap_hosts_str}"')
        print(f'AP_COORDINATES="{ap_coords_str}"')
        print(f'ENABLE_TRIANGULATION="true"')
        print()
        
        # Generate Docker Compose
        print("🐳 Docker Compose Configuration:")
        print("```yaml")
        print("services:")
        print("  ruckus-exporter:")
        print("    image: shotwellcoho/ruckus-ap-exporter:latest")
        print("    restart: unless-stopped")
        print("    ports: [\"8000:8000\"]")
        print("    environment:")
        print(f'      RUCKUS_AP_HOSTS: "{ap_hosts_str}"')
        print(f'      AP_COORDINATES: "{ap_coords_str}"')
        print('      ENABLE_TRIANGULATION: "true"')
        print('      SCRAPE_INTERVAL: "15"  # More frequent for better tracking')
        print('      SNMP_COMMUNITY: "public"')
        print("```")
        print()
        
        # Generate Docker run command
        print("🏃 Docker Run Command:")
        print("```bash")
        print("docker run -d --name ruckus-exporter -p 8000:8000 \\")
        print(f'  -e RUCKUS_AP_HOSTS="{ap_hosts_str}" \\')
        print(f'  -e AP_COORDINATES="{ap_coords_str}" \\')
        print('  -e ENABLE_TRIANGULATION="true" \\')
        print('  -e SCRAPE_INTERVAL="15" \\')
        print('  shotwellcoho/ruckus-ap-exporter:latest')
        print("```")
        print()
        
        # Show layout visualization
        self.show_layout()
        
        # Generate setup file
        self.save_configuration(ap_hosts_str, ap_coords_str)
    
    def show_layout(self):
        """Show ASCII layout of AP positions"""
        print("🗺️ AP Layout Visualization:")
        print("-" * 25)
        
        if not self.aps:
            return
            
        # Find bounds
        coords = list(self.aps.values())
        min_x = min(x for x, y, z in coords)
        max_x = max(x for x, y, z in coords)
        min_y = min(y for x, y, z in coords)
        max_y = max(y for x, y, z in coords)
        
        # Create simple ASCII grid
        width = int(max_x - min_x) + 5
        height = int(max_y - min_y) + 5
        
        if width > 50 or height > 20:
            scale = max(width / 50, height / 20)
            width = int(width / scale)
            height = int(height / scale)
        else:
            scale = 1
        
        # Plot APs
        print("Legend: [#] = AP position")
        print(f"Scale: 1 char ≈ {scale:.1f} meters\n")
        
        for i, (ip, (x, y, z)) in enumerate(self.aps.items()):
            print(f"AP{i+1}: {ip} at ({x:.1f}, {y:.1f}, {z:.1f}m)")
        
        print()
        
    def save_configuration(self, ap_hosts: str, ap_coords: str):
        """Save configuration to files"""
        config = {
            "environment_type": self.environment_type,
            "ap_hosts": ap_hosts,
            "ap_coordinates": ap_coords,
            "aps": {ip: {"x": x, "y": y, "z": z} for ip, (x, y, z) in self.aps.items()}
        }
        
        try:
            with open("ap_config.json", "w") as f:
                json.dump(config, f, indent=2)
            print("💾 Configuration saved to 'ap_config.json'")
        except Exception as e:
            print(f"⚠️ Could not save config file: {e}")
        
        print("\n🎯 Setup Complete!")
        print("Next steps:")
        print("1. Copy the environment variables above")
        print("2. Update your docker-compose.yml or docker run command")
        print("3. Restart your container")
        print("4. Import the enhanced Grafana dashboard")
        print("5. Watch clients being tracked in real-time!")
        print("\n*Welcome to the future of wasteland surveillance!* 📡⚔️")


def main():
    """Main entry point"""
    try:
        setup = APCoordinateSetup()
        setup.run_interactive_setup()
    except KeyboardInterrupt:
        print("\n\n👋 Setup cancelled. Stay safe in the wasteland!")
    except Exception as e:
        print(f"\n❌ Setup error: {e}")
        print("Please try again or check the CLIENT_LOCATION_GUIDE.md for manual setup.")


if __name__ == "__main__":
    main()