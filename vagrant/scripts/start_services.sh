#!/bin/bash
# Script to start CSLE services after installation
# Starts services directly to avoid CSLE CLI/gRPC permission issues in Vagrant
# Note: We intentionally don't use set -e here so all services are attempted

CSLE_USER=${1:-"vagrant"}
CSLE_HOME="/home/${CSLE_USER}/csle"
CONDA_PATH="/home/${CSLE_USER}/anaconda3"

# Correct paths based on Ansible installation
PROMETHEUS_DIR="${CSLE_HOME}/management-system/prometheus"
NODE_EXPORTER_DIR="${CSLE_HOME}/management-system/node_exporter"
PROMETHEUS_CONFIG="${CSLE_HOME}/management-system/prometheus.yml"
MANAGEMENT_SYSTEM_DIR="${CSLE_HOME}/management-system"
WEBAPP_DIR="${CSLE_HOME}/management-system/csle-mgmt-webapp"

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
# Install node_exporter if not present
if [ ! -f "${NODE_EXPORTER_DIR}/node_exporter" ]; then
    echo "[*] Node Exporter not found, installing..."
    cd "${MANAGEMENT_SYSTEM_DIR}"
    wget -q https://github.com/prometheus/node_exporter/releases/download/v1.0.1/node_exporter-1.0.1.linux-amd64.tar.gz
    tar xzf node_exporter-1.0.1.linux-amd64.tar.gz
    mv node_exporter-1.0.1.linux-amd64 node_exporter 2>/dev/null || true
    rm -f node_exporter-1.0.1.linux-amd64.tar.gz
    chown -R ${CSLE_USER}:${CSLE_USER} node_exporter
fi

# Start node_exporter if not running
if ! pgrep -x node_exporter > /dev/null; then
    if [ -f "${NODE_EXPORTER_DIR}/node_exporter" ]; then
        nohup "${NODE_EXPORTER_DIR}/node_exporter" \
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
# Install prometheus if not present
if [ ! -f "${PROMETHEUS_DIR}/prometheus" ]; then
    echo "[*] Prometheus not found, installing..."
    cd "${MANAGEMENT_SYSTEM_DIR}"
    wget -q https://github.com/prometheus/prometheus/releases/download/v2.23.0/prometheus-2.23.0.linux-amd64.tar.gz
    tar xzf prometheus-2.23.0.linux-amd64.tar.gz
    mv prometheus-2.23.0.linux-amd64 prometheus 2>/dev/null || true
    rm -f prometheus-2.23.0.linux-amd64.tar.gz
    # Copy the prometheus.yml config if it exists in the parent directory
    if [ -f "${MANAGEMENT_SYSTEM_DIR}/prometheus.yml" ] && [ ! -f "${PROMETHEUS_DIR}/prometheus.yml" ]; then
        cp "${MANAGEMENT_SYSTEM_DIR}/prometheus.yml" "${PROMETHEUS_DIR}/prometheus.yml"
    fi
    chown -R ${CSLE_USER}:${CSLE_USER} prometheus
fi

# Start prometheus if not running
if ! pgrep -x prometheus > /dev/null; then
    if [ -f "${PROMETHEUS_DIR}/prometheus" ]; then
        mkdir -p "${PROMETHEUS_DIR}/data"
        chown -R ${CSLE_USER}:${CSLE_USER} "${PROMETHEUS_DIR}/data"
        # Use the config file in prometheus dir if it exists, otherwise use the one in management-system
        CONFIG_FILE="${PROMETHEUS_DIR}/prometheus.yml"
        if [ ! -f "${CONFIG_FILE}" ]; then
            CONFIG_FILE="${PROMETHEUS_CONFIG}"
        fi
        nohup "${PROMETHEUS_DIR}/prometheus" \
            --config.file="${CONFIG_FILE}" \
            --storage.tsdb.path="${PROMETHEUS_DIR}/data" \
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
if docker ps -a --format '{{.Names}}' 2>/dev/null | grep -q '^grafana$'; then
    docker start grafana 2>/dev/null || true
    echo "[+] Grafana container started"
else
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
if docker ps --format '{{.Names}}' 2>/dev/null | grep -q 'pgadmin'; then
    echo "[+] pgAdmin already running"
else
    echo "[-] pgAdmin not running (may need manual start due to Docker Hub rate limit)"
fi
sleep 2

echo "[7/8] Starting Nginx..."
systemctl start nginx
systemctl enable nginx
echo "[+] Nginx started"
sleep 2

echo "[8/8] Starting Flask API..."
# The Flask API is started by running the server.py script
# First, check if the web app is built
if [ ! -d "${WEBAPP_DIR}/build" ]; then
    echo "[*] Building web application..."
    sudo -u ${CSLE_USER} bash -c "
        source ${CONDA_PATH}/etc/profile.d/conda.sh
        conda activate base
        export CSLE_HOME=${CSLE_HOME}
        export PATH=\$PATH:/home/${CSLE_USER}/.nvm/versions/node/*/bin
        cd ${WEBAPP_DIR}
        npm run build 2>/dev/null || echo 'npm build failed, continuing anyway'
    " 2>/dev/null || true
fi

# Kill any existing Flask process
pkill -f 'server.py' 2>/dev/null || true
pkill -f 'csle_rest_api' 2>/dev/null || true
sleep 1

# Start Flask API using a custom server script
# Create the Flask startup script first
cat > /tmp/flask_server.py << PYEOF
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import csle_rest_api.rest_api as rest_api

if __name__ == '__main__':
    static_folder_path = '${WEBAPP_DIR}/build'
    rest_api.start_server(static_folder=static_folder_path, port=7777, num_threads=100, host='0.0.0.0', https=False)
PYEOF

chown ${CSLE_USER}:${CSLE_USER} /tmp/flask_server.py

sudo -u ${CSLE_USER} bash -c "
    source ${CONDA_PATH}/etc/profile.d/conda.sh
    conda activate base
    export CSLE_HOME=${CSLE_HOME}
    nohup python /tmp/flask_server.py > /var/log/csle/flask.log 2>&1 &
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
