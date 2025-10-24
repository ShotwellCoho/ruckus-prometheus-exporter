# 🎯 Common AP Layout Templates

## Small Office (30m x 20m)
```bash
# 3 APs covering typical office space
RUCKUS_AP_HOSTS="192.168.1.100,192.168.1.101,192.168.1.102"
AP_COORDINATES="192.168.1.100:0,0,2.5;192.168.1.101:30,0,2.5;192.168.1.102:15,20,2.5"
```

## Large Office (50m x 30m)
```bash
# 4 APs for comprehensive coverage
RUCKUS_AP_HOSTS="192.168.1.100,192.168.1.101,192.168.1.102,192.168.1.103"
AP_COORDINATES="192.168.1.100:0,0,2.5;192.168.1.101:50,0,2.5;192.168.1.102:0,30,2.5;192.168.1.103:50,30,2.5"
```

## Vault-Tec Facility (60m x 40m)
```bash
# Underground bunker with 4 APs
RUCKUS_AP_HOSTS="192.168.1.100,192.168.1.101,192.168.1.102,192.168.1.103"
AP_COORDINATES="192.168.1.100:0,0,3.0;192.168.1.101:60,0,3.0;192.168.1.102:0,40,3.0;192.168.1.103:60,40,3.0"
```

## Linear Corridor (100m x 5m)
```bash
# Hospital or school hallway
RUCKUS_AP_HOSTS="192.168.1.100,192.168.1.101,192.168.1.102,192.168.1.103"
AP_COORDINATES="192.168.1.100:0,2.5,2.5;192.168.1.101:33,2.5,2.5;192.168.1.102:66,2.5,2.5;192.168.1.103:100,2.5,2.5"
```

## Warehouse (80m x 60m)
```bash
# Large open space with high ceilings
RUCKUS_AP_HOSTS="192.168.1.100,192.168.1.101,192.168.1.102,192.168.1.103,192.168.1.104,192.168.1.105"
AP_COORDINATES="192.168.1.100:0,0,6.0;192.168.1.101:40,0,6.0;192.168.1.102:80,0,6.0;192.168.1.103:0,60,6.0;192.168.1.104:40,60,6.0;192.168.1.105:80,60,6.0"
```

## Multi-Floor Building
```bash
# 2 floors with 3 APs each (Z coordinate = floor height)
RUCKUS_AP_HOSTS="192.168.1.100,192.168.1.101,192.168.1.102,192.168.1.103,192.168.1.104,192.168.1.105"
AP_COORDINATES="192.168.1.100:0,0,2.5;192.168.1.101:25,0,2.5;192.168.1.102:50,0,2.5;192.168.1.103:0,0,5.5;192.168.1.104:25,0,5.5;192.168.1.105:50,0,5.5"
```

## Outdoor Campus (200m x 150m)
```bash
# University or corporate campus
RUCKUS_AP_HOSTS="192.168.1.100,192.168.1.101,192.168.1.102,192.168.1.103,192.168.1.104"
AP_COORDINATES="192.168.1.100:0,0,4.0;192.168.1.101:100,0,4.0;192.168.1.102:200,0,4.0;192.168.1.103:50,150,4.0;192.168.1.104:150,150,4.0"
```

## Tips for Measuring Your Environment

### Using a Floor Plan
1. Import floor plan into any image editor
2. Set scale (measure a known distance)
3. Choose origin point (usually a corner)
4. Read AP coordinates from the plan
5. Convert to meters

### Physical Measurement
1. Choose corner as origin (0,0)
2. Use measuring tape or laser measure
3. Measure X (horizontal) distance from origin
4. Measure Y (vertical) distance from origin  
5. Measure Z (height) from floor to AP

### Using Building Information
- Standard office ceiling: 2.4-3.0m
- Warehouse/industrial: 4.0-8.0m
- Outdoor mounting: 3.0-6.0m
- Residential: 2.4-2.7m

## Quick Setup Commands

### Run Interactive Setup
```bash
python setup_coordinates.py
```

### Test Your Configuration
```bash
# Start with demo mode first
docker run -d --name ruckus-test -p 8000:8000 \
  -e RUCKUS_AP_HOSTS="192.168.1.100,192.168.1.101" \
  -e ENABLE_TRIANGULATION="true" \
  -e AP_COORDINATES="192.168.1.100:0,0,2.5;192.168.1.101:20,0,2.5" \
  shotwellcoho/ruckus-ap-exporter:latest

# Check metrics
curl http://localhost:8000/metrics | grep client_location
```

### Import Enhanced Dashboard
1. Open Grafana (http://localhost:3000)
2. Go to Dashboards → Import
3. Upload `grafana-dashboard-with-location.json`
4. Select your Prometheus data source
5. View client positions in real-time!

---

*Choose your layout wisely, vault dweller. The wasteland is vast, but your surveillance network will track every movement.* 🎯📡⚔️