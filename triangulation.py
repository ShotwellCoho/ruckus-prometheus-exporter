#!/usr/bin/env python3
"""
🎯 Client Location Triangulation Module
=====================================

Uses RSSI data from multiple Ruckus APs to estimate client positions.
Perfect for tracking vault dwellers in the Capital Wasteland! 📡⚔️

Supports:
- RSSI-based trilateration 
- Path loss model calibration
- Multi-AP signal correlation
- Confidence scoring
"""

import math
import logging
from typing import Dict, List, Tuple, Optional, NamedTuple
from dataclasses import dataclass
from collections import defaultdict
import statistics

logger = logging.getLogger(__name__)


@dataclass
class APCoordinates:
    """Physical coordinates of an Access Point"""
    x: float  # meters
    y: float  # meters
    z: float = 2.5  # meters (typical ceiling height)
    name: str = ""


@dataclass 
class ClientSignal:
    """Client signal data from a specific AP"""
    mac_address: str
    ap_name: str
    rssi: float  # dBm
    timestamp: float
    frequency: float = 2.4  # GHz


class LocationEstimate(NamedTuple):
    """Estimated client location with confidence"""
    x: float
    y: float
    confidence: float  # 0.0 to 1.0
    num_aps: int
    error_radius: float  # estimated error in meters


class WastelandTriangulator:
    """
    🎯 Triangulates client positions using RSSI from multiple APs
    
    Uses a path loss model calibrated for indoor environments.
    Perfect for tracking movement in vaults and settlements!
    """
    
    def __init__(self, environment_type: str = "indoor"):
        self.ap_coordinates: Dict[str, APCoordinates] = {}
        self.environment_type = environment_type
        
        # Path loss model parameters (adjust for your environment)
        if environment_type == "indoor":
            self.reference_distance = 1.0  # meters
            self.reference_rssi = -30  # dBm at 1m
            self.path_loss_exponent = 2.5  # indoor typical: 2.0-4.0
            self.shadow_std = 4.0  # standard deviation of shadowing
        elif environment_type == "outdoor": 
            self.reference_distance = 1.0
            self.reference_rssi = -30
            self.path_loss_exponent = 3.5  # outdoor typical: 2.7-5.0
            self.shadow_std = 8.0
        else:  # vault/bunker
            self.reference_distance = 1.0
            self.reference_rssi = -35
            self.path_loss_exponent = 3.0  # concrete/steel
            self.shadow_std = 6.0
            
    def add_ap(self, ap_name: str, x: float, y: float, z: float = 2.5):
        """Add an Access Point with its physical coordinates"""
        self.ap_coordinates[ap_name] = APCoordinates(x, y, z, ap_name)
        logger.info(f"📍 Added AP '{ap_name}' at position ({x}, {y}, {z})")
        
    def rssi_to_distance(self, rssi: float, frequency: float = 2.4) -> float:
        """
        Convert RSSI to estimated distance using path loss model
        
        Formula: RSSI = Reference_RSSI - 10*n*log10(d/d0)
        Where: n = path loss exponent, d = distance, d0 = reference distance
        """
        if rssi > self.reference_rssi:
            # Very close or invalid reading
            return 0.5
            
        # Account for frequency (higher freq = more attenuation)
        freq_correction = 20 * math.log10(frequency / 2.4) if frequency != 2.4 else 0
        adjusted_rssi = rssi - freq_correction
        
        # Calculate distance from path loss model
        db_loss = self.reference_rssi - adjusted_rssi
        distance = self.reference_distance * (10 ** (db_loss / (10 * self.path_loss_exponent)))
        
        # Reasonable bounds (1m to 100m)
        return max(1.0, min(100.0, distance))
        
    def trilaterate(self, signals: List[ClientSignal]) -> Optional[LocationEstimate]:
        """
        Perform trilateration using RSSI from multiple APs
        
        Requires at least 2 APs for basic positioning (3+ for better accuracy)
        """
        if len(signals) < 2:
            logger.warning("Need at least 2 AP signals for triangulation")
            return None
            
        # Convert RSSI to distances
        ap_distances = []
        for signal in signals:
            if signal.ap_name not in self.ap_coordinates:
                logger.warning(f"Unknown AP: {signal.ap_name}")
                continue
                
            distance = self.rssi_to_distance(signal.rssi, signal.frequency)
            ap_coord = self.ap_coordinates[signal.ap_name]
            ap_distances.append((ap_coord, distance))
            
        if len(ap_distances) < 2:
            return None
            
        # Least squares trilateration
        if len(ap_distances) == 2:
            return self._trilaterate_2ap(ap_distances)
        else:
            return self._trilaterate_multiap(ap_distances)
            
    def _trilaterate_2ap(self, ap_distances: List[Tuple[APCoordinates, float]]) -> LocationEstimate:
        """Trilateration with exactly 2 APs (gives 2 possible positions)"""
        (ap1, d1), (ap2, d2) = ap_distances[:2]
        
        # Distance between APs
        dx = ap2.x - ap1.x
        dy = ap2.y - ap1.y
        d_ap = math.sqrt(dx**2 + dy**2)
        
        if d_ap == 0:
            # APs at same location - can't triangulate
            return LocationEstimate(ap1.x, ap1.y, 0.1, 2, max(d1, d2))
            
        # Use law of cosines to find intersection points
        try:
            # Calculate intersection of two circles
            a = (d1**2 - d2**2 + d_ap**2) / (2 * d_ap)
            h_sq = d1**2 - a**2
            
            if h_sq < 0:
                # Circles don't intersect - use midpoint
                x = ap1.x + a * dx / d_ap
                y = ap1.y + a * dy / d_ap
                confidence = 0.3
            else:
                h = math.sqrt(h_sq)
                
                # Two intersection points - choose one (or average them)
                px = ap1.x + a * dx / d_ap
                py = ap1.y + a * dy / d_ap
                
                x1 = px + h * (-dy) / d_ap
                y1 = py + h * dx / d_ap
                x2 = px - h * (-dy) / d_ap  
                y2 = py - h * dx / d_ap
                
                # For now, just take the midpoint
                x = (x1 + x2) / 2
                y = (y1 + y2) / 2
                confidence = 0.7
                
        except (ValueError, ZeroDivisionError):
            # Fallback to weighted average
            x = (ap1.x + ap2.x) / 2
            y = (ap1.y + ap2.y) / 2  
            confidence = 0.2
            
        error_radius = max(d1, d2) * 0.3  # Estimate 30% error
        return LocationEstimate(x, y, confidence, 2, error_radius)
        
    def _trilaterate_multiap(self, ap_distances: List[Tuple[APCoordinates, float]]) -> LocationEstimate:
        """Trilateration with 3+ APs using least squares method"""
        n = len(ap_distances)
        
        # Set up least squares system: A * [x, y] = b
        A = []
        b = []
        
        # Use first AP as reference
        ref_ap, ref_dist = ap_distances[0]
        
        for i in range(1, n):
            ap, dist = ap_distances[i]
            
            # Linear approximation: 2*(xi - x0)*x + 2*(yi - y0)*y = xi² + yi² - x0² - y0² + d0² - di²
            A.append([2 * (ap.x - ref_ap.x), 2 * (ap.y - ref_ap.y)])
            b.append(ap.x**2 + ap.y**2 - ref_ap.x**2 - ref_ap.y**2 + ref_dist**2 - dist**2)
            
        # Solve using pseudo-inverse (least squares)
        try:
            A_T = [[A[j][i] for j in range(len(A))] for i in range(2)]  # Transpose
            ATA = [[sum(A_T[i][k] * A[k][j] for k in range(len(A))) for j in range(2)] for i in range(2)]
            ATb = [sum(A_T[i][k] * b[k] for k in range(len(A))) for i in range(2)]
            
            # Solve 2x2 system
            det = ATA[0][0] * ATA[1][1] - ATA[0][1] * ATA[1][0]
            if abs(det) < 1e-10:
                raise ValueError("Singular matrix")
                
            x = (ATA[1][1] * ATb[0] - ATA[0][1] * ATb[1]) / det
            y = (ATA[0][0] * ATb[1] - ATA[1][0] * ATb[0]) / det
            
            # Calculate confidence based on solution consistency
            residuals = []
            for ap, dist in ap_distances:
                estimated_dist = math.sqrt((x - ap.x)**2 + (y - ap.y)**2)
                residuals.append(abs(estimated_dist - dist))
                
            avg_error = statistics.mean(residuals)
            max_dist = max(dist for _, dist in ap_distances)
            confidence = max(0.1, 1.0 - (avg_error / max_dist))
            error_radius = avg_error
            
        except (ValueError, ZeroDivisionError):
            # Fallback to centroid
            x = statistics.mean(ap.x for ap, _ in ap_distances)
            y = statistics.mean(ap.y for ap, _ in ap_distances)
            confidence = 0.3
            error_radius = statistics.mean(dist for _, dist in ap_distances) * 0.5
            
        return LocationEstimate(x, y, confidence, n, error_radius)
        
    def track_clients(self, all_signals: List[ClientSignal]) -> Dict[str, LocationEstimate]:
        """
        Track multiple clients from aggregated signal data
        
        Groups signals by MAC address and calculates position for each client
        """
        # Group signals by client MAC address
        client_signals = defaultdict(list)
        for signal in all_signals:
            client_signals[signal.mac_address].append(signal)
            
        # Calculate location for each client
        client_locations = {}
        for mac, signals in client_signals.items():
            # Filter recent signals (last 30 seconds)
            if signals:
                latest_time = max(s.timestamp for s in signals)
                recent_signals = [s for s in signals if latest_time - s.timestamp <= 30]
                
                if recent_signals:
                    location = self.trilaterate(recent_signals)
                    if location and location.confidence > 0.1:
                        client_locations[mac] = location
                        logger.debug(f"📍 Client {mac[:8]}... at ({location.x:.1f}, {location.y:.1f}) "
                                   f"confidence={location.confidence:.2f}")
                        
        return client_locations


# Example usage for a typical office/vault setup
def setup_vault_tec_facility():
    """🏢 Example setup for a Vault-Tec facility monitoring system"""
    triangulator = WastelandTriangulator("vault")
    
    # Add APs for a typical office layout (coordinates in meters)
    triangulator.add_ap("vault-ap-01", 0, 0, 3.0)      # Corner office
    triangulator.add_ap("vault-ap-02", 30, 0, 3.0)     # Other corner  
    triangulator.add_ap("vault-ap-03", 15, 20, 3.0)    # Center area
    triangulator.add_ap("vault-ap-04", 0, 40, 3.0)     # Far corner
    
    return triangulator


if __name__ == "__main__":
    # Demo the triangulation system
    logging.basicConfig(level=logging.INFO)
    
    triangulator = setup_vault_tec_facility()
    
    # Simulate some client signals
    import time
    current_time = time.time()
    
    test_signals = [
        ClientSignal("aa:bb:cc:dd:ee:01", "vault-ap-01", -45, current_time),
        ClientSignal("aa:bb:cc:dd:ee:01", "vault-ap-02", -65, current_time),
        ClientSignal("aa:bb:cc:dd:ee:01", "vault-ap-03", -55, current_time),
        
        ClientSignal("11:22:33:44:55:02", "vault-ap-01", -70, current_time),
        ClientSignal("11:22:33:44:55:02", "vault-ap-02", -50, current_time),
    ]
    
    locations = triangulator.track_clients(test_signals)
    
    print("\n🎯 Client Location Results:")
    for mac, location in locations.items():
        print(f"📱 Client {mac}: Position ({location.x:.1f}m, {location.y:.1f}m) "
              f"Confidence: {location.confidence:.2f} Error: ±{location.error_radius:.1f}m")