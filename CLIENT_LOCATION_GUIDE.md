# 🎯 Client Location Configuration Guide

## Environment Variables

Configure AP coordinates for accurate triangulation:

```bash
# Enable client location tracking
ENABLE_TRIANGULATION=true

# Configure AP physical coordinates (x,y,z in meters)
# Format: "IP1:x,y,z;IP2:x,y,z"
AP_COORDINATES="192.168.1.100:0,0,2.5;192.168.1.101:30,0,2.5;192.168.1.102:15,20,2.5"

# Example for a vault facility
AP_COORDINATES="192.168.1.100:0,0,3.0;192.168.1.101:25,0,3.0;192.168.1.102:50,0,3.0;192.168.1.103:25,30,3.0"
```

## Docker Compose Example

```yaml
services:
  ruckus-exporter:
    image: shotwellcoho/ruckus-ap-exporter:latest
    restart: unless-stopped
    ports: ["8000:8000"]
    environment:
      RUCKUS_AP_HOSTS: "192.168.1.100,192.168.1.101,192.168.1.102"
      ENABLE_TRIANGULATION: "true"
      AP_COORDINATES: "192.168.1.100:0,0,3.0;192.168.1.101:30,0,3.0;192.168.1.102:15,20,3.0"
      SNMP_COMMUNITY: "public"
      SCRAPE_INTERVAL: "15"  # More frequent for better location tracking
```

## New Prometheus Metrics

### Client Location Metrics

- `ruckus_client_location_x_meters` - Client X coordinate in meters
- `ruckus_client_location_y_meters` - Client Y coordinate in meters  
- `ruckus_client_location_confidence` - Location confidence (0-1)
- `ruckus_client_location_error_radius_meters` - Estimated error radius
- `ruckus_client_rssi_dbm` - Client RSSI from each AP
- `ruckus_client_distance_meters` - Estimated distance from each AP

### Example Queries

```promql
# Show client positions
{__name__=~"ruckus_client_location_[xy]_meters"}

# Client with highest confidence
max by (client_mac) (ruckus_client_location_confidence)

# Clients within 10m of origin
sqrt(
  (ruckus_client_location_x_meters{ap_host="triangulated"})^2 + 
  (ruckus_client_location_y_meters{ap_host="triangulated"})^2
) < 10
```

## Coordinate System Setup

### Method 1: Measure Your Environment

1. Choose an origin point (0, 0) - typically a corner
2. Measure AP positions from origin:
   - X-axis: horizontal distance (meters)
   - Y-axis: vertical distance (meters)  
   - Z-axis: height above floor (meters)

### Method 2: Use Building Plans

1. Load floor plan into CAD software
2. Set scale and origin
3. Read AP coordinates from plan
4. Convert to meters

### Example Layouts

#### Small Office (30m x 20m)
```bash
AP_COORDINATES="192.168.1.100:0,0,2.5;192.168.1.101:30,0,2.5;192.168.1.102:15,20,2.5"
```

#### Vault-Tec Facility (50m x 40m)
```bash
AP_COORDINATES="192.168.1.100:0,0,3.0;192.168.1.101:50,0,3.0;192.168.1.102:0,40,3.0;192.168.1.103:50,40,3.0"
```

#### Linear Corridor (100m x 5m)
```bash  
AP_COORDINATES="192.168.1.100:0,2.5,3.0;192.168.1.101:25,2.5,3.0;192.168.1.102:50,2.5,3.0;192.168.1.103:75,2.5,3.0"
```

## Triangulation Algorithm

The system uses RSSI-based trilateration:

1. **Distance Estimation**: Converts RSSI to distance using path loss model
2. **Circle Intersection**: Finds intersection of distance circles from multiple APs
3. **Least Squares**: Optimizes position when using 3+ APs
4. **Confidence Scoring**: Rates accuracy based on signal consistency

### Path Loss Models

- **Indoor**: Path loss exponent 2.5, suitable for offices/homes
- **Outdoor**: Path loss exponent 3.5, for open areas
- **Vault**: Path loss exponent 3.0, for concrete/steel structures

## Accuracy Expectations

| Scenario | Typical Accuracy | Confidence Range |
|----------|------------------|------------------|
| 2 APs, good signal | ±3-8 meters | 0.3-0.7 |
| 3+ APs, good signal | ±2-5 meters | 0.6-0.9 |
| Obstructed/weak signal | ±5-15 meters | 0.1-0.4 |

## Troubleshooting

### No Location Data
- Check `ENABLE_TRIANGULATION=true`
- Verify at least 2 APs configured
- Check AP coordinates format
- View logs for client signal detection

### Poor Accuracy
- Add more APs for better triangulation
- Verify AP coordinates are correct
- Reduce scrape interval for more samples
- Check for RF interference

### Demo Mode
If no real client data is available, the system generates demo clients for testing. Look for "demo" SSID in metrics.

## Security & Privacy

- Client MACs are truncated to first 8 characters + "..." in metrics
- Full MACs are only used internally for tracking
- Location data is relative to your coordinate system
- No external data transmission (everything stays local)

---

*🎯 Happy hunting in the wasteland, vault dweller! Your client tracking system is now operational.*