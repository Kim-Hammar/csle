#!/bin/bash
# Script to start CSLE services after installation
# Starts services directly to avoid CSLE CLI/gRPC permission issues in Vagrant
# Note: We intentionally don't use set -e here so all services are attempted

CSLE_USER=${1:-"vagrant"}
CSLE_HOME="/home/${CSLE_USER}/csle"
CONDA_PATH="/home/${CSLE_USER}/anaconda3"

echo "=============================================="
echo "Starting CSLE Services"
echo "CSLE_HOME: ${CSLE_HOME}"
echo "CSLE_USER: ${CSLE_USER}"
echo "=============================================="

echo ""
echo "[1/8] Starting Docker Engine..."
systemctl start docker
systemctl enable docker
sleep 2

echo "[2/8] Starting Node Exporter..."
# Check if node_exporter is already running
if ! pgrep -x node_exporter > /dev/null; then
    if [ -f /home/${CSLE_USER}/node_exporter-1.3.1.linux-amd64/node_exporter ]; then
        nohup /home/${CSLE_USER}/node_exporter-1.3.1.linux-amd64/node_exporter \
            --web.listen-address=":9100" > /var/log/csle/node_exporter.log 2>&1 &
        echo "[+] Node Exporter started"
    else
        echo "[-] Node Exporter binary not found, skipping"
    fi
else
    echo "[+] Node Exporter already running"
fi
sleep 2

echo "[3/8] Starting Prometheus..."
# Check if prometheus is already running
if ! pgrep -x prometheus > /dev/null; then
    if [ -f /home/${CSLE_USER}/prometheus-2.34.0.linux-amd64/prometheus ]; then
        # Ensure data directory exists
        mkdir -p /home/${CSLE_USER}/prometheus-2.34.0.linux-amd64/data
        chown -R ${CSLE_USER}:${CSLE_USER} /home/${CSLE_USER}/prometheus-2.34.0.linux-amd64/data
        nohup /home/${CSLE_USER}/prometheus-2.34.0.linux-amd64/prometheus \
            --config.file=/home/${CSLE_USER}/prometheus-2.34.0.linux-amd64/prometheus.yml \
            --storage.tsdb.path=/home/${CSLE_USER}/prometheus-2.34.0.linux-amd64/data \
            --web.listen-address=":9090" > /var/log/csle/prometheus.log 2>&1 &
        echo "[+] Prometheus started"
    else
        echo "[-] Prometheus binary not found, skipping"
    fi
else
    echo "[+] Prometheus already running"
fi
sleep 2

echo "[4/8] Starting Grafana..."
# Use sudo to ensure we have docker access
if docker ps -a --format '{{.Names}}' 2>/dev/null | grep -q '^grafana$'; then
    docker start grafana 2>/dev/null || true
    echo "[+] Grafana container started"
else
    # Run Grafana container
    docker run -d --name grafana \
        -p 3000:3000 \
        --restart unless-stopped \
        grafana/grafana:latest 2>/dev/null || true
    echo "[+] Grafana container created and started"
fi
sleep 2

echo "[5/8] Starting cAdvisor..."
if docker ps -a --format '{{.Names}}' 2>/dev/null | grep -q '^cadvisor$'; then
    docker start cadvisor 2>/dev/null || true
    echo "[+] cAdvisor container started"
else
    docker run -d --name cadvisor \
        -p 8081:8080 \
        --volume=/:/rootfs:ro \
        --volume=/var/run:/var/run:ro \
        --volume=/sys:/sys:ro \
        --volume=/var/lib/docker/:/var/lib/docker:ro \
        --restart unless-stopped \
        gcr.io/cadvisor/cadvisor:latest 2>/dev/null || true
    echo "[+] cAdvisor container created and started"
fi
sleep 2

echo "[6/8] Starting pgAdmin..."
# pgAdmin should already be running from Ansible installation
if docker ps --format '{{.Names}}' 2>/dev/null | grep -q 'pgadmin'; then
    echo "[+] pgAdmin already running"
else
    echo "[-] pgAdmin not running (may need manual start)"
fi
sleep 2

echo "[7/8] Starting Nginx..."
systemctl start nginx
systemctl enable nginx
echo "[+] Nginx started"
sleep 2

echo "[8/8] Starting Flask API..."
# Start Flask API in the conda environment
sudo -u ${CSLE_USER} bash -c "
    source ${CONDA_PATH}/etc/profile.d/conda.sh
    conda activate base
    export CSLE_HOME=${CSLE_HOME}
    cd ${CSLE_HOME}/management-system/csle-rest-api

    # Kill any existing Flask process
    pkill -f 'csle_rest_api' 2>/dev/null || true
    sleep 1

    # Start Flask API
    nohup python -m csle_rest_api.csle_rest_app > /var/log/csle/flask.log 2>&1 &
    echo '[+] Flask API started'
"
sleep 5

echo ""
echo "=============================================="
echo "CSLE Services Started"
echo "=============================================="

# Verify services are running
echo ""
echo "Checking service status..."
echo ""

check_port() {
    local port=$1
    local service=$2
    if ss -tlnp | grep -q ":${port} "; then
        echo "[+] ${service} is listening on port ${port}"
    else
        echo "[-] ${service} is NOT listening on port ${port}"
    fi
}

check_port 7777 "Flask API"
check_port 9090 "Prometheus"
check_port 3000 "Grafana"
check_port 9100 "Node Exporter"

echo ""
echo "Service startup complete."
