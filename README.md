```
██████╗ ██╗   ██╗ ██████╗██╗  ██╗██╗   ██╗███████╗    ███████╗██╗  ██╗██████╗  ██████╗ ██████╗ ████████╗███████╗██████╗ 
██╔══██╗██║   ██║██╔════╝██║ ██╔╝██║   ██║██╔════╝    ██╔════╝╚██╗██╔╝██╔══██╗██╔═══██╗██╔══██╗╚══██╔══╝██╔════╝██╔══██╗
██████╔╝██║   ██║██║     █████╔╝ ██║   ██║███████╗    █████╗   ╚███╔╝ ██████╔╝██║   ██║██████╔╝   ██║   █████╗  ██████╔╝
██╔══██╗██║   ██║██║     ██╔═██╗ ██║   ██║╚════██║    ██╔══╝   ██╔██╗ ██╔═══╝ ██║   ██║██╔══██╗   ██║   ██╔══╝  ██╔══██╗
██║  ██║╚██████╔╝╚██████╗██║  ██╗╚██████╔╝███████║    ███████╗██╔╝ ██╗██║     ╚██████╔╝██║  ██║   ██║   ███████╗██║  ██║
╚═╝  ╚═╝ ╚═════╝  ╚═════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝    ╚══════╝╚═╝  ╚═╝╚═╝      ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═╝

<div align="center">

# 🚀 Ruckus AP Metrics Exporter

[![Docker Pulls](https://img.shields.io/docker/pulls/shotwellcoho/ruckus-ap-exporter?style=for-the-badge&logo=docker&color=2496ED)](https://hub.docker.com/r/shotwellcoho/ruckus-ap-exporter)
[![Docker Image Size](https://img.shields.io/docker/image-size/shotwellcoho/ruckus-ap-exporter/latest?style=for-the-badge&logo=docker&color=2496ED)](https://hub.docker.com/r/shotwellcoho/ruckus-ap-exporter)
[![GitHub release](https://img.shields.io/github/v/release/ShotwellCoho/ruckus-prometheus-exporter?style=for-the-badge&logo=github&color=181717)](https://github.com/ShotwellCoho/ruckus-prometheus-exporter/releases)
[![Build Status](https://img.shields.io/github/actions/workflow/status/ShotwellCoho/ruckus-prometheus-exporter/docker-build.yml?branch=main&style=for-the-badge&logo=github-actions&color=2088FF)](https://github.com/ShotwellCoho/ruckus-prometheus-exporter/actions)
[![License](https://img.shields.io/github/license/ShotwellCoho/ruckus-prometheus-exporter?style=for-the-badge&color=green)](LICENSE)

**Professional Prometheus exporter for Ruckus Wireless Access Points**  
*Multi-platform • Multi-AP • Production Ready*

[🚀 Quick Start](#-quick-start) • [📊 Metrics](#-metrics) • [🐳 Docker Hub](https://hub.docker.com/r/shotwellcoho/ruckus-ap-exporter) • [📖 Documentation](#-documentation)

</div>

## ✨ Features

<table>
<tr>
<td>

🏗️ **Multi-Platform**  
Native support for x86_64 and ARM64

🔗 **Multi-AP Monitoring**  
Monitor multiple APs from one container

📡 **SNMP Collection**  
Real-time metrics via SNMP v2c

</td>
<td>

📊 **Prometheus Ready**  
Labeled metrics for easy querying  

🐳 **Docker Native**  
One-command deployment

⚙️ **Zero Config**  
Works out-of-the-box

</td>
<td>

🛡️ **Production Ready**  
Health checks, logging & error handling

🚀 **High Performance**  
Concurrent AP monitoring

📈 **Rich Metrics**  
System, interface & wireless data

</td>
</tr>
</table>

## 🚀 Quick Start

### 📋 Prerequisites

<div align="center">

| Requirement | Description |
|:-----------:|:------------|
| 🐳 **Docker** | Docker & Docker Compose |
| 💻 **Platform** | x86_64 (AMD64) or ARM64 |
| 🌐 **Network** | Access to your Ruckus AP(s) |
| 📡 **SNMP** | SNMP v2c enabled with community "public" |

</div>

### ⚙️ Configuration

<details>
<summary>🔧 <strong>Environment Variables</strong></summary>

| Variable | Default | Description |
|:---------|:--------|:------------|
| `RUCKUS_AP_HOST` | `192.168.1.100` | 📍 Single AP IP (legacy mode) |
| `RUCKUS_AP_HOSTS` | - | 🔗 **Multi-AP IPs** (comma-separated) |
| `SNMP_COMMUNITY` | `public` | 🔐 SNMP community string |
| `SNMP_PORT` | `161` | 🔌 SNMP port |
| `METRICS_PORT` | `8000` | 📊 Prometheus metrics port |
| `SCRAPE_INTERVAL` | `30` | ⏱️ Collection interval (seconds) |
| `ENABLE_TRIANGULATION` | `true` | 🎯 **Client location tracking** |
| `AP_COORDINATES` | - | 📍 **AP positions** (see guide below) |

</details>

### 🎯 New: Client Location Triangulation

Track client devices across your wireless network using RSSI-based triangulation!

<details>
<summary>📍 <strong>Setup Location Tracking</strong></summary>

**Configure AP Coordinates:**
```bash
# Format: "IP1:x,y,z;IP2:x,y,z" (coordinates in meters)
AP_COORDINATES="192.168.1.100:0,0,2.5;192.168.1.101:30,0,2.5;192.168.1.102:15,20,2.5"
```

**Example Docker Compose with Triangulation:**
```yaml
services:
  ruckus-exporter:
    image: shotwellcoho/ruckus-ap-exporter:latest
    environment:
      RUCKUS_AP_HOSTS: "192.168.1.100,192.168.1.101,192.168.1.102"
      ENABLE_TRIANGULATION: "true"
      AP_COORDINATES: "192.168.1.100:0,0,3.0;192.168.1.101:30,0,3.0;192.168.1.102:15,20,3.0"
      SCRAPE_INTERVAL: "15"  # More frequent for better tracking
```

**New Location Metrics:**
- `ruckus_client_location_x_meters` - Client X coordinate  
- `ruckus_client_location_y_meters` - Client Y coordinate
- `ruckus_client_location_confidence` - Accuracy confidence (0-1)
- `ruckus_client_rssi_dbm` - Client signal strength per AP
- `ruckus_client_distance_meters` - Estimated distance from AP

📖 **Full Guide:** See `CLIENT_LOCATION_GUIDE.md` for detailed setup instructions

</details>

### � Installation Methods

<div align="center">

#### Option 1: Docker Hub (Recommended)

```bash
# 🚀 Single command deployment
docker run -d --name ruckus-exporter -p 8000:8000 \
  -e RUCKUS_AP_HOSTS=192.168.1.100,192.168.1.101 \
  shotwellcoho/ruckus-ap-exporter:latest

# ✅ Verify it's working  
curl http://localhost:8000/metrics | grep ruckus_ap_info
```

</div>

<details>
<summary>📝 <strong>Docker Compose Setup</strong></summary>

```yaml
version: '3.8'
services:
  ruckus-exporter:
    image: shotwellcoho/ruckus-ap-exporter:latest
    restart: unless-stopped
    ports: ["8000:8000"]
    environment:
      - RUCKUS_AP_HOSTS=192.168.1.100,192.168.1.101
      - SNMP_COMMUNITY=public
```

```bash
docker-compose up -d && docker-compose logs -f
```

</details>

<details>
<summary>🔨 <strong>Build from Source</strong></summary>

```bash
# Clone and deploy
git clone https://github.com/ShotwellCoho/ruckus-prometheus-exporter.git
cd ruckus-prometheus-exporter && docker-compose up -d
```

</details>

---

## 📊 Metrics

<div align="center">

**All metrics include `ap_host` labels for multi-AP identification** 🏷️

</div>

<table>
<tr>
<td width="33%">

### 🖥️ **System Metrics**
```prometheus
ruckus_ap_info{ap_host, name, description}
ruckus_ap_uptime_seconds{ap_host}
```

</td>
<td width="33%">

### 🔌 **Interface Metrics**
```prometheus  
ruckus_interface_status{ap_host, interface}
ruckus_interface_bytes_*{ap_host, interface}
ruckus_interface_packets_*{ap_host, interface}
```

</td>
<td width="33%">

### 📡 **Wireless Metrics**
```prometheus
ruckus_wireless_clients_total{ap_host, ssid}
ruckus_wireless_signal_strength_dbm{ap_host}
ruckus_scrape_duration_seconds{ap_host}
```

</td>
</tr>
</table>

### 📈 **Example Queries**

<details>
<summary>🔍 <strong>Grafana Dashboard Queries</strong></summary>

```promql
# AP Uptime (days)
ruckus_ap_uptime_seconds / 86400

# Total Connected Clients  
sum by (ap_host) (ruckus_wireless_clients_total)

# Interface Throughput (MB/s)
rate(ruckus_interface_bytes_transmitted_total[5m]) * 8 / 1024 / 1024

# AP Performance Comparison
ruckus_scrape_duration_seconds > 10
```

</details>

---

## 🔧 Configuration

### Prometheus Setup

```yaml
# prometheus.yml
scrape_configs:
  - job_name: 'ruckus-aps'
    static_configs:
      - targets: ['localhost:8000']
    scrape_interval: 30s
    metrics_path: /metrics
```

### 📊 Grafana Dashboard

Get instant wireless network visibility with our **pre-built Grafana dashboard**!

<div align="center">

**✨ Features: AP Uptime • Client Counts • Network Throughput • Interface Health • Performance Metrics ✨**

[📥 **Download Dashboard**](grafana-dashboard.json) • [📖 **Setup Guide**](GRAFANA_SETUP.md)

</div>

**Quick Import**: 
1. Open Grafana → **Import Dashboard**
2. Upload `grafana-dashboard.json` 
3. Select Prometheus datasource
4. **Done!** 🎉

---

## 🛠️ Development

<details>
<summary>👨‍💻 <strong>Local Development Setup</strong></summary>

```bash
# Clone & setup
git clone https://github.com/ShotwellCoho/ruckus-prometheus-exporter.git
cd ruckus-prometheus-exporter && python -m venv .venv && source .venv/bin/activate

# Install dependencies  
pip install -r requirements.txt

# Test single AP
export RUCKUS_AP_HOSTS=192.168.1.100 && python ruckus_exporter.py

# Test multi-AP
export RUCKUS_AP_HOSTS=192.168.1.100,192.168.1.101 && python ruckus_exporter.py
```

</details>

---

## 🔍 Troubleshooting

<details>
<summary>❗ <strong>Common Issues & Solutions</strong></summary>

| Issue | Solution |
|:------|:---------|
| 🚫 **SNMP Connection Failed** | • Verify AP IP<br>• Check SNMP enabled<br>• Validate community string |
| 📊 **No Metrics** | • `docker logs ruckus-exporter`<br>• `curl localhost:8000/metrics`<br>• Check scrape interval |
| 🏗️ **Platform Issues** | • Use `--platform linux/amd64`<br>• Verify Docker buildx setup |

</details>
   - Use the correct platform in docker-compose.yml

### Logs

View exporter logs:
```bash
docker logs -f ruckus-exporter
```

### Health Check

Check if the exporter is healthy:
```bash
curl http://localhost:8000/metrics
```

## Ruckus-Specific Notes

This exporter uses standard SNMP MIBs that should work with most Ruckus AP models. However, some advanced wireless metrics may require Ruckus-specific MIBs which would need to be added based on your specific AP model.

Common Ruckus AP series supported:
- R series (R610, R650, etc.)
- T series (T610, T750, etc.)
- H series (H320, H510, etc.)

---

## 🔐 Security & Compatibility

<div align="center">

### 🛡️ **Security Features**
Non-root container • Secret management • Network isolation

### 📡 **Supported Ruckus Models**  
**R Series** • **T Series** • **H Series** • **ZoneFlex**

</div>

---

## 📖 Documentation

| Resource | Description |
|:---------|:------------|
| 📊 [**Grafana Dashboard**](GRAFANA_SETUP.md) | Pre-built monitoring dashboard |
| 📊 [**Multi-Platform Guide**](MULTI_PLATFORM_GUIDE.md) | Platform deployment details |
| 🏗️ [**Multi-AP Setup**](MULTI_AP_SETUP.md) | Configuration examples |  
| 🐳 [**Docker Hub**](https://hub.docker.com/r/shotwellcoho/ruckus-ap-exporter) | Container repository |
| 🚀 [**GitHub Actions**](https://github.com/ShotwellCoho/ruckus-prometheus-exporter/actions) | CI/CD pipeline |

---

## 🤝 Community & Support

<div align="center">

### 💬 **Get Help**
[🐛 Issues](https://github.com/ShotwellCoho/ruckus-prometheus-exporter/issues) • [💡 Discussions](https://github.com/ShotwellCoho/ruckus-prometheus-exporter/discussions) • [📖 Wiki](https://github.com/ShotwellCoho/ruckus-prometheus-exporter/wiki)

### 🤲 **Contribute**  
[🔀 Fork](https://github.com/ShotwellCoho/ruckus-prometheus-exporter/fork) • [📋 Contributing Guide](CONTRIBUTING.md) • [🔒 Security Policy](SECURITY.md)

### ⭐ **Support This Project**
**Star** ⭐ • **Share** 🔄 • **Contribute** 🛠️

---

<sub>Built with ❤️ for the networking community</sub>

**[⬆ Back to Top](#-ruckus-ap-metrics-exporter)**

</div>#   D o c k e r   b u i l d   t r i g g e r 
 
 