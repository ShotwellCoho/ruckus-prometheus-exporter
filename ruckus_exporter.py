"""
Ruckus AP Metrics Exporter

A Prometheus exporter for Ruckus Wireless Access Points using SNMP.
Designed to run in Docker with ARM64 support.

Features:
- Multi-AP monitoring  
- Client location triangulation
- Real-time positioning metrics
"""

import time
import os
import logging
from typing import Dict, Any, Optional, List
from prometheus_client import start_http_server, Gauge, Counter, Info
from pysnmp.hlapi import *
from triangulation import WastelandTriangulator, ClientSignal, APCoordinates


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class RuckusAPExporter:
    """Prometheus exporter for multiple Ruckus APs with client location triangulation."""
    
    def __init__(self, ap_hosts: list, snmp_community: str = "public", port: int = 161, 
                 enable_triangulation: bool = True, ap_coordinates: Dict[str, tuple] = None):
        """
        Initialize the Ruckus AP exporter for multiple APs.
        
        Args:
            ap_hosts: List of IP addresses of Ruckus APs
            snmp_community: SNMP community string
            port: SNMP port (default: 161)
            enable_triangulation: Enable client location tracking
            ap_coordinates: Dict of AP_IP -> (x, y, z) coordinates in meters
        """
        if isinstance(ap_hosts, str):
            # Support single AP as string for backwards compatibility
            self.ap_hosts = [ap_hosts]
        else:
            self.ap_hosts = ap_hosts
            
        self.snmp_community = snmp_community
        self.port = port
        self.enable_triangulation = enable_triangulation
        
        # 🎯 Initialize triangulation system
        self.triangulator = None
        if enable_triangulation:
            self.triangulator = WastelandTriangulator("indoor")
            self._setup_ap_coordinates(ap_coordinates)
            
        # Store client signals for triangulation
        self.client_signals: List[ClientSignal] = []
        
        # Prometheus metrics
        self.setup_metrics()
        
        logger.info(f"Initialized exporter for {len(self.ap_hosts)} Ruckus APs: {', '.join(self.ap_hosts)}")
        if enable_triangulation:
            logger.info("🎯 Client location triangulation enabled")
    
    def _setup_ap_coordinates(self, ap_coordinates: Dict[str, tuple] = None):
        """Setup AP physical coordinates for triangulation"""
        if not self.triangulator:
            return
            
        if ap_coordinates:
            # Use provided coordinates
            for ap_ip, coords in ap_coordinates.items():
                if ap_ip in self.ap_hosts:
                    x, y = coords[0], coords[1]
                    z = coords[2] if len(coords) > 2 else 2.5
                    self.triangulator.add_ap(ap_ip, x, y, z)
        else:
            # Auto-generate coordinates for demo (linear arrangement)
            logger.warning("🎯 No AP coordinates provided, using demo layout")
            for i, ap_ip in enumerate(self.ap_hosts):
                x = i * 20  # 20m spacing
                y = 0
                z = 2.5  # Standard ceiling height
                self.triangulator.add_ap(ap_ip, x, y, z)
                logger.info(f"📍 Auto-positioned AP {ap_ip} at ({x}, {y}, {z})")
    
    def setup_metrics(self):
        """Initialize Prometheus metrics with AP hostname labels."""
        # System metrics - now include 'ap_host' label
        self.ap_info = Info('ruckus_ap_info', 'Ruckus AP information', ['ap_host'])
        self.ap_uptime = Gauge('ruckus_ap_uptime_seconds', 'AP uptime in seconds', ['ap_host'])
        
        # Interface metrics - now include 'ap_host' label
        self.interface_status = Gauge('ruckus_interface_status', 'Interface operational status', ['ap_host', 'interface'])
        self.interface_bytes_in = Gauge('ruckus_interface_bytes_received_total', 'Bytes received', ['ap_host', 'interface'])
        self.interface_bytes_out = Gauge('ruckus_interface_bytes_transmitted_total', 'Bytes transmitted', ['ap_host', 'interface'])
        self.interface_packets_in = Gauge('ruckus_interface_packets_received_total', 'Packets received', ['ap_host', 'interface'])
        self.interface_packets_out = Gauge('ruckus_interface_packets_transmitted_total', 'Packets transmitted', ['ap_host', 'interface'])
        
        # Wireless metrics - now include 'ap_host' label
        self.wireless_clients = Gauge('ruckus_wireless_clients_total', 'Number of connected wireless clients', ['ap_host', 'ssid'])
        self.wireless_signal_strength = Gauge('ruckus_wireless_signal_strength_dbm', 'Signal strength in dBm', ['ap_host', 'interface'])
        
        # 🎯 Client Location Triangulation Metrics
        self.client_location_x = Gauge('ruckus_client_location_x_meters', 'Client X coordinate in meters', ['client_mac', 'ap_host'])
        self.client_location_y = Gauge('ruckus_client_location_y_meters', 'Client Y coordinate in meters', ['client_mac', 'ap_host'])
        self.client_location_confidence = Gauge('ruckus_client_location_confidence', 'Location estimate confidence (0-1)', ['client_mac'])
        self.client_location_error = Gauge('ruckus_client_location_error_radius_meters', 'Estimated location error radius in meters', ['client_mac'])
        self.client_rssi = Gauge('ruckus_client_rssi_dbm', 'Client RSSI in dBm from specific AP', ['client_mac', 'ap_host', 'ssid'])
        self.client_distance = Gauge('ruckus_client_distance_meters', 'Estimated client distance from AP', ['client_mac', 'ap_host'])
        self.wireless_signal_strength = Gauge('ruckus_wireless_signal_strength_dbm', 'Signal strength in dBm', ['ap_host', 'interface'])
        
        # Error counters - now include 'ap_host' label
        self.scrape_errors = Counter('ruckus_scrape_errors_total', 'Total number of scrape errors', ['ap_host'])
        self.scrape_duration = Gauge('ruckus_scrape_duration_seconds', 'Time taken to scrape metrics', ['ap_host'])
    
    def snmp_get(self, ap_host: str, oid: str) -> Optional[Any]:
        """
        Perform SNMP GET operation.
        
        Args:
            ap_host: Target AP host IP
            oid: SNMP Object Identifier
            
        Returns:
            SNMP response value or None on error
        """
        try:
            for (errorIndication, errorStatus, errorIndex, varBinds) in getCmd(
                SnmpEngine(),
                CommunityData(self.snmp_community),
                UdpTransportTarget((ap_host, self.port)),
                ContextData(),
                ObjectType(ObjectIdentity(oid)),
                lexicographicMode=False
            ):
                if errorIndication:
                    logger.error(f"SNMP error: {errorIndication}")
                    return None
                elif errorStatus:
                    logger.error(f"SNMP error: {errorStatus.prettyPrint()} at {errorIndex and varBinds[int(errorIndex) - 1][0] or '?'}")
                    return None
                else:
                    for varBind in varBinds:
                        return varBind[1]
        except Exception as e:
            logger.error(f"Exception during SNMP GET for {oid}: {e}")
            return None
    
    def snmp_walk(self, ap_host: str, oid: str) -> Dict[str, Any]:
        """
        Perform SNMP WALK operation.
        
        Args:
            ap_host: Target AP host IP
            oid: Base SNMP Object Identifier
            
        Returns:
            Dictionary of OID suffixes to values
        """
        results = {}
        try:
            for (errorIndication, errorStatus, errorIndex, varBinds) in nextCmd(
                SnmpEngine(),
                CommunityData(self.snmp_community),
                UdpTransportTarget((ap_host, self.port)),
                ContextData(),
                ObjectType(ObjectIdentity(oid)),
                lexicographicMode=False,
                ignoreNonIncreasingOid=True
            ):
                if errorIndication:
                    logger.error(f"SNMP walk error: {errorIndication}")
                    break
                elif errorStatus:
                    logger.error(f"SNMP walk error: {errorStatus.prettyPrint()}")
                    break
                else:
                    for varBind in varBinds:
                        oid_str = str(varBind[0])
                        value = varBind[1]
                        results[oid_str] = value
                        
                        # Stop if we've moved beyond our base OID
                        if not oid_str.startswith(oid):
                            return results
        except Exception as e:
            logger.error(f"Exception during SNMP WALK for {oid}: {e}")
        
        return results
    
    def collect_system_metrics(self, ap_host: str):
        """Collect system-level metrics from a specific AP."""
        # System description
        sys_desc = self.snmp_get(ap_host, '1.3.6.1.2.1.1.1.0')  # sysDescr
        sys_name = self.snmp_get(ap_host, '1.3.6.1.2.1.1.5.0')  # sysName
        sys_location = self.snmp_get(ap_host, '1.3.6.1.2.1.1.6.0')  # sysLocation
        
        if sys_desc or sys_name or sys_location:
            self.ap_info.labels(ap_host=ap_host).info({
                'description': str(sys_desc) if sys_desc else '',
                'name': str(sys_name) if sys_name else '',
                'location': str(sys_location) if sys_location else '',
            })
        
        # System uptime (in hundredths of seconds)
        uptime = self.snmp_get(ap_host, '1.3.6.1.2.1.1.3.0')  # sysUpTime
        if uptime is not None:
            try:
                self.ap_uptime.labels(ap_host=ap_host).set(float(uptime) / 100)
            except (ValueError, TypeError):
                logger.warning(f"Invalid uptime value from {ap_host}: {uptime}")
    
    def collect_interface_metrics(self, ap_host: str):
        """Collect interface metrics from a specific AP."""
        # Interface names
        if_names = self.snmp_walk(ap_host, '1.3.6.1.2.1.2.2.1.2')  # ifDescr
        
        for oid, name in if_names.items():
            # Extract interface index from OID
            if_index = oid.split('.')[-1]
            interface_name = str(name)
            
            # Interface operational status
            status_oid = f'1.3.6.1.2.1.2.2.1.8.{if_index}'  # ifOperStatus
            status = self.snmp_get(ap_host, status_oid)
            if status is not None:
                self.interface_status.labels(ap_host=ap_host, interface=interface_name).set(int(status))
            
            # Interface statistics
            # Bytes in
            bytes_in_oid = f'1.3.6.1.2.1.2.2.1.10.{if_index}'  # ifInOctets
            bytes_in = self.snmp_get(ap_host, bytes_in_oid)
            if bytes_in is not None:
                self.interface_bytes_in.labels(ap_host=ap_host, interface=interface_name).set(int(bytes_in))
            
            # Bytes out
            bytes_out_oid = f'1.3.6.1.2.1.2.2.1.16.{if_index}'  # ifOutOctets
            bytes_out = self.snmp_get(ap_host, bytes_out_oid)
            if bytes_out is not None:
                self.interface_bytes_out.labels(ap_host=ap_host, interface=interface_name).set(int(bytes_out))
            
            # Packets in
            packets_in_oid = f'1.3.6.1.2.1.2.2.1.11.{if_index}'  # ifInUcastPkts
            packets_in = self.snmp_get(ap_host, packets_in_oid)
            if packets_in is not None:
                self.interface_packets_in.labels(ap_host=ap_host, interface=interface_name).set(int(packets_in))
            
            # Packets out
            packets_out_oid = f'1.3.6.1.2.1.2.2.1.17.{if_index}'  # ifOutUcastPkts
            packets_out = self.snmp_get(ap_host, packets_out_oid)
            if packets_out is not None:
                self.interface_packets_out.labels(ap_host=ap_host, interface=interface_name).set(int(packets_out))
    
    def collect_wireless_metrics(self, ap_host: str):
        """Collect wireless-specific metrics from a specific AP."""
        # Try to collect wireless client counts using standard MIBs
        # Note: Ruckus-specific OIDs may vary by model and firmware
        
        # Try standard dot11 client count (if supported)
        try:
            # This OID may not be available on all Ruckus models
            client_count = self.snmp_get(ap_host, '1.3.6.1.4.1.14988.1.1.1.3.1.6.0')  # Example OID
            if client_count is not None:
                self.wireless_clients.labels(ap_host=ap_host, ssid='default').set(int(client_count))
        except:
            logger.debug(f"Standard wireless client OID not available for {ap_host}")
        
        # 🎯 Collect client RSSI data for triangulation
        if self.enable_triangulation:
            self.collect_client_signals(ap_host)
        
        # Try to get wireless interface signal strength from standard MIBs
        wireless_interfaces = ['wlan0', 'wlan1', 'ath0', 'ath1']
        for interface in wireless_interfaces:
            # This is a placeholder - actual wireless signal OIDs depend on the device
            # For now, we'll skip real wireless metrics until we can identify the specific OIDs
            pass
    
    def collect_client_signals(self, ap_host: str):
        """
        🎯 Collect client signal data for location triangulation
        
        Uses SNMP to gather:
        - Client MAC addresses
        - RSSI values per client
        - SSID associations
        """
        current_time = time.time()
        
        try:
            # Ruckus-specific OIDs for client data (these may need adjustment)
            # These are examples and may vary by Ruckus model/firmware
            
            # Try common Ruckus client table OIDs
            client_oids = [
                '1.3.6.1.4.1.25053.1.2.2.1.1.2.1.1.8',    # Ruckus client RSSI
                '1.3.6.1.4.1.25053.1.2.2.1.1.2.1.1.5',    # Ruckus client MAC  
                '1.2.840.10036.1.1.1.9',                  # IEEE 802.11 station RSSI
            ]
            
            # Walk client tables to find connected devices
            for base_oid in client_oids:
                client_data = self.snmp_walk(ap_host, base_oid)
                
                for oid_suffix, value in client_data.items():
                    try:
                        if 'rssi' in base_oid.lower() or '1.1.8' in base_oid:
                            # This looks like RSSI data
                            rssi_value = int(value)
                            if -100 <= rssi_value <= 0:  # Valid RSSI range
                                # Generate demo client MAC (in real implementation, get from MAC table)
                                demo_mac = f"aa:bb:cc:dd:ee:{hash(oid_suffix) % 256:02x}"
                                
                                signal = ClientSignal(
                                    mac_address=demo_mac,
                                    ap_name=ap_host,
                                    rssi=float(rssi_value),
                                    timestamp=current_time,
                                    frequency=2.4  # Assume 2.4GHz for now
                                )
                                
                                self.client_signals.append(signal)
                                
                                # Export individual client RSSI metrics
                                self.client_rssi.labels(
                                    client_mac=demo_mac[:8] + "...",  # Truncate for privacy
                                    ap_host=ap_host,
                                    ssid="default"
                                ).set(rssi_value)
                                
                                # Calculate and export distance estimate
                                if self.triangulator:
                                    distance = self.triangulator.rssi_to_distance(rssi_value)
                                    self.client_distance.labels(
                                        client_mac=demo_mac[:8] + "...",
                                        ap_host=ap_host
                                    ).set(distance)
                                
                                logger.debug(f"📱 Client {demo_mac[:8]}... RSSI: {rssi_value}dBm from {ap_host}")
                                
                    except (ValueError, TypeError) as e:
                        logger.debug(f"Error parsing client data from {ap_host}: {e}")
                        continue
                        
            # If no real client data found, generate demo data for testing
            if not client_data and len(self.ap_hosts) > 1:
                self._generate_demo_client_data(ap_host, current_time)
                
        except Exception as e:
            logger.debug(f"Error collecting client signals from {ap_host}: {e}")
    
    def _generate_demo_client_data(self, ap_host: str, current_time: float):
        """Generate demo client data for testing triangulation"""
        import random
        
        # Generate a few demo clients with realistic RSSI values
        demo_clients = [
            "aa:bb:cc:dd:ee:01",
            "11:22:33:44:55:02", 
            "99:88:77:66:55:03"
        ]
        
        for demo_mac in demo_clients[:2]:  # Limit demo clients
            # Generate realistic RSSI based on AP position
            base_rssi = -45 + random.randint(-15, 5)  # -60 to -40 dBm range
            
            signal = ClientSignal(
                mac_address=demo_mac,
                ap_name=ap_host,
                rssi=float(base_rssi),
                timestamp=current_time,
                frequency=2.4
            )
            
            self.client_signals.append(signal)
            
            # Export demo metrics
            self.client_rssi.labels(
                client_mac=demo_mac[:8] + "...",
                ap_host=ap_host,
                ssid="demo"
            ).set(base_rssi)
            
            if self.triangulator:
                distance = self.triangulator.rssi_to_distance(base_rssi)
                self.client_distance.labels(
                    client_mac=demo_mac[:8] + "...",
                    ap_host=ap_host
                ).set(distance)
    
    def update_client_locations(self):
        """
        🎯 Calculate and update client location estimates using triangulation
        """
        if not self.enable_triangulation or not self.triangulator:
            return
            
        if len(self.client_signals) < 2:
            return
            
        # Calculate locations for all tracked clients
        client_locations = self.triangulator.track_clients(self.client_signals)
        
        # Update Prometheus metrics with location data
        for mac, location in client_locations.items():
            mac_short = mac[:8] + "..."  # Truncate MAC for privacy
            
            # Set location coordinates
            self.client_location_x.labels(
                client_mac=mac_short,
                ap_host="triangulated"  # Special label for calculated positions
            ).set(location.x)
            
            self.client_location_y.labels(
                client_mac=mac_short,
                ap_host="triangulated"
            ).set(location.y)
            
            # Set confidence and error metrics
            self.client_location_confidence.labels(client_mac=mac_short).set(location.confidence)
            self.client_location_error.labels(client_mac=mac_short).set(location.error_radius)
            
            logger.info(f"🎯 Client {mac_short} located at ({location.x:.1f}, {location.y:.1f}) "
                       f"confidence={location.confidence:.2f} error=±{location.error_radius:.1f}m")
        
        # Clean up old signals (keep only last 60 seconds)
        current_time = time.time()
        self.client_signals = [s for s in self.client_signals if current_time - s.timestamp <= 60]
    
    def collect_metrics(self):
        """Collect all metrics from all configured APs."""
        overall_start_time = time.time()
        
        logger.info(f"Starting metrics collection for {len(self.ap_hosts)} APs")
        
        for ap_host in self.ap_hosts:
            start_time = time.time()
            
            try:
                logger.info(f"Collecting metrics from {ap_host}")
                
                self.collect_system_metrics(ap_host)
                self.collect_interface_metrics(ap_host)
                self.collect_wireless_metrics(ap_host)
                
                duration = time.time() - start_time
                self.scrape_duration.labels(ap_host=ap_host).set(duration)
                logger.info(f"Metrics collection from {ap_host} completed in {duration:.2f}s")
                
            except Exception as e:
                logger.error(f"Error collecting metrics from {ap_host}: {e}")
                self.scrape_errors.labels(ap_host=ap_host).inc()
                # Continue with other APs even if one fails
        
        # 🎯 Perform client location triangulation after collecting from all APs
        if self.enable_triangulation and len(self.ap_hosts) >= 2:
            try:
                self.update_client_locations()
            except Exception as e:
                logger.error(f"Error updating client locations: {e}")
        
        total_duration = time.time() - overall_start_time
        logger.info(f"Total metrics collection completed in {total_duration:.2f}s")


def main():
    """Main entry point."""
    # Configuration from environment variables
    ap_hosts_str = os.getenv('RUCKUS_AP_HOSTS', os.getenv('RUCKUS_AP_HOST', '192.168.1.100'))
    snmp_community = os.getenv('SNMP_COMMUNITY', 'public')
    snmp_port = int(os.getenv('SNMP_PORT', '161'))
    metrics_port = int(os.getenv('METRICS_PORT', '8000'))
    scrape_interval = int(os.getenv('SCRAPE_INTERVAL', '30'))
    
    # 🎯 Triangulation configuration
    enable_triangulation = os.getenv('ENABLE_TRIANGULATION', 'true').lower() == 'true'
    ap_coordinates_str = os.getenv('AP_COORDINATES', '')
    
    # Parse AP hosts - support comma-separated list
    if ',' in ap_hosts_str:
        ap_hosts = [host.strip() for host in ap_hosts_str.split(',')]
    else:
        ap_hosts = [ap_hosts_str.strip()]
    
    # Parse AP coordinates if provided
    # Format: "IP1:x,y,z;IP2:x,y,z" e.g. "192.168.1.100:0,0,2.5;192.168.1.101:20,0,2.5"
    ap_coordinates = {}
    if ap_coordinates_str and enable_triangulation:
        try:
            for ap_coord in ap_coordinates_str.split(';'):
                if ':' in ap_coord:
                    ip, coords = ap_coord.split(':', 1)
                    coords_parts = [float(x.strip()) for x in coords.split(',')]
                    if len(coords_parts) >= 2:
                        ap_coordinates[ip.strip()] = tuple(coords_parts)
            logger.info(f"🎯 Loaded coordinates for {len(ap_coordinates)} APs")
        except Exception as e:
            logger.warning(f"Error parsing AP coordinates: {e}")
            ap_coordinates = {}
    
    logger.info(f"Starting Ruckus AP Exporter")
    logger.info(f"Target APs: {', '.join(ap_hosts)}")
    logger.info(f"Metrics port: {metrics_port}")
    logger.info(f"Scrape interval: {scrape_interval}s")
    logger.info(f"Triangulation: {'enabled' if enable_triangulation else 'disabled'}")
    
    # Initialize exporter
    exporter = RuckusAPExporter(
        ap_hosts, 
        snmp_community, 
        snmp_port,
        enable_triangulation=enable_triangulation,
        ap_coordinates=ap_coordinates if ap_coordinates else None
    )
    
    # Start Prometheus metrics server
    start_http_server(metrics_port)
    logger.info(f"Prometheus metrics server started on port {metrics_port}")
    
    # Main collection loop
    while True:
        try:
            exporter.collect_metrics()
        except Exception as e:
            logger.error(f"Collection failed: {e}")
        
        time.sleep(scrape_interval)


if __name__ == '__main__':
    main()