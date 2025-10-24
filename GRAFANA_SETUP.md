# 📊 Grafana Dashboard Setup Guide

## Overview

This directory contains a pre-built Grafana dashboard for monitoring Ruckus Wireless Access Points with beautiful visualizations and comprehensive metrics.

## 🎨 Dashboard Features

### 📡 **Comprehensive Monitoring Panels**
- **AP Uptime Tracking** - Monitor AP availability over time
- **Connected Clients** - Real-time wireless client counts per AP
- **Network Throughput** - TX/RX bandwidth utilization with rate calculations
- **Interface Status Table** - Health status of all AP interfaces  
- **Scrape Performance** - Monitor exporter performance and response times
- **Packet Rate Analysis** - Detailed packet-per-second statistics

### 🎯 **Smart Features**
- **Multi-AP Support** - Automatically detects and displays all monitored APs
- **Dynamic Variables** - Datasource and job selection dropdowns
- **Color-Coded Status** - Green/Red indicators for interface health
- **Rate Calculations** - Proper rate() functions for accurate throughput metrics
- **Performance Thresholds** - Warning colors for slow scrape times

## 🚀 Quick Setup

### Method 1: Import Dashboard JSON

1. **Open Grafana** (http://localhost:3000)
2. **Navigate to Dashboards** → **New** → **Import**
3. **Upload JSON file**: `grafana-dashboard.json`
4. **Configure datasource**: Select your Prometheus instance
5. **Import** and enjoy! 🎉

### Method 2: Dashboard ID (if published)
```
Dashboard ID: [To be assigned when published to grafana.com]
```

## 🔧 Configuration Requirements

### Prometheus Datasource Setup
```yaml
# Add to prometheus.yml
scrape_configs:
  - job_name: 'ruckus-aps'
    static_configs:
      - targets: ['localhost:8000']
    scrape_interval: 30s
    metrics_path: /metrics
```

### Expected Metrics
The dashboard requires these metrics from the Ruckus exporter:
- `ruckus_ap_info` - AP identification
- `ruckus_ap_uptime_seconds` - Uptime tracking  
- `ruckus_wireless_clients_total` - Client connections
- `ruckus_interface_status` - Interface health
- `ruckus_interface_bytes_*` - Network throughput
- `ruckus_interface_packets_*` - Packet statistics
- `ruckus_scrape_duration_seconds` - Performance monitoring

## 📈 Panel Details

### 1. **📡 AP Uptime (Days)**
- **Query**: `ruckus_ap_uptime_seconds / 86400`
- **Visualization**: Time series line chart
- **Purpose**: Track AP availability and identify reboots

### 2. **👥 Connected Clients by AP**  
- **Query**: `sum by (ap_host) (ruckus_wireless_clients_total)`
- **Visualization**: Stat panels with current values
- **Purpose**: Monitor wireless network utilization

### 3. **🌐 Network Throughput (bps)**
- **Query**: `rate(ruckus_interface_bytes_*[5m]) * 8`
- **Visualization**: Multi-series time chart
- **Purpose**: Analyze bandwidth utilization trends

### 4. **🔌 Interface Status**
- **Query**: `ruckus_interface_status`  
- **Visualization**: Color-coded table
- **Purpose**: Quick health overview of all interfaces

### 5. **⚡ Scrape Performance (seconds)**
- **Query**: `ruckus_scrape_duration_seconds`
- **Visualization**: Stat with thresholds
- **Purpose**: Monitor exporter performance

### 6. **📦 Packet Rate (pps)**
- **Query**: `rate(ruckus_interface_packets_*[5m])`
- **Visualization**: Time series with fill
- **Purpose**: Detailed packet analysis

## 🎨 Customization

### Adding Panels
The dashboard is fully customizable. Common additions:

```promql
# Signal Strength (if available)
ruckus_wireless_signal_strength_dbm

# Error Rates  
rate(ruckus_interface_errors_total[5m])

# Top Interfaces by Traffic
topk(5, rate(ruckus_interface_bytes_transmitted_total[5m]))

# AP Comparison
(ruckus_ap_uptime_seconds / 86400) > 30
```

### Alert Rules
Add alerting for critical conditions:
```yaml
# Example alert rules
- alert: RuckusAPDown
  expr: up{job="ruckus-aps"} == 0
  for: 2m
  labels:
    severity: critical
  annotations:
    summary: "Ruckus AP {{$labels.instance}} is down"

- alert: HighScrapeTime  
  expr: ruckus_scrape_duration_seconds > 10
  for: 5m
  labels:
    severity: warning
  annotations:
    summary: "Slow SNMP response from {{$labels.ap_host}}"
```

## 🐳 Docker Compose Integration

Add Grafana to your existing stack:

```yaml
version: '3.8'
services:
  ruckus-exporter:
    image: yourusername/ruckus-ap-exporter:latest
    ports: ["8000:8000"]
    environment:
      - RUCKUS_AP_HOSTS=192.168.1.100,192.168.1.101

  prometheus:
    image: prom/prometheus:latest
    ports: ["9090:9090"]
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml:ro

  grafana:
    image: grafana/grafana:latest
    ports: ["3000:3000"]
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana-storage:/var/lib/grafana
      - ./grafana-dashboard.json:/etc/grafana/provisioning/dashboards/ruckus.json:ro

volumes:
  grafana-storage:
```

## 🔍 Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| **No data showing** | Verify Prometheus is scraping the exporter |
| **Missing panels** | Check metric names match your exporter version |
| **Slow loading** | Reduce time range or increase scrape interval |
| **Interface filter not working** | Ensure `interface` label exists in metrics |

### Debugging Queries
Test these in Prometheus before using in Grafana:
```promql
# Verify basic connectivity
up{job="ruckus-aps"}

# Check available metrics  
{__name__=~"ruckus_.*"}

# Validate AP labels
ruckus_ap_info
```

## 🎯 Performance Tips

- **Time Range**: Start with 1-hour windows for testing
- **Refresh Rate**: 30s matches the default scrape interval  
- **Panel Limits**: Use `topk()` for high-cardinality metrics
- **Caching**: Enable Grafana query caching for better performance

## 🌟 Advanced Features

### Multi-Tenancy Support
Filter by AP groups using label selectors:
```promql
ruckus_ap_uptime_seconds{ap_host=~"192.168.1.*"}  # Building A
ruckus_ap_uptime_seconds{ap_host=~"10.0.1.*"}     # Building B
```

### Capacity Planning
Add panels for growth analysis:
```promql
# Predict when uptime will reset (maintenance windows)
predict_linear(ruckus_ap_uptime_seconds[7d], 86400)

# Client growth rate
deriv(ruckus_wireless_clients_total[1h]) * 3600
```

## 📚 Additional Resources

- **Grafana Documentation**: https://grafana.com/docs/
- **Prometheus Queries**: https://prometheus.io/docs/prometheus/latest/querying/
- **Dashboard Sharing**: https://grafana.com/grafana/dashboards/

---

**🎉 Happy Monitoring!** Your Ruckus wireless infrastructure is now beautifully visualized! 📊⚡