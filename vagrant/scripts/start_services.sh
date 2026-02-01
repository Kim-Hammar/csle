#!/bin/bash
# Script to start CSLE services after installation
# Service order follows cluster_controller.py

set -e

CSLE_USER=${1:-"vagrant"}
CSLE_HOME="/home/${CSLE_USER}/csle"
CONDA_PATH="/home/${CSLE_USER}/anaconda3"

echo "=============================================="
echo "Starting CSLE Services"
echo "CSLE_HOME: ${CSLE_HOME}"
echo "CSLE_USER: ${CSLE_USER}"
echo "=============================================="

# Function to run a command in the conda environment
run_csle_cmd() {
    sudo -u ${CSLE_USER} bash -c "source ${CONDA_PATH}/etc/profile.d/conda.sh && conda activate base && export CSLE_HOME=${CSLE_HOME} && $1"
}

# Function to start a service with error handling
start_service() {
    local service=$1
    local delay=${2:-2}
    echo "[*] Starting ${service}..."
    if run_csle_cmd "csle start ${service}" 2>&1; then
        echo "[+] ${service} started successfully"
    else
        echo "[-] Warning: ${service} may have failed to start (continuing anyway)"
    fi
    sleep ${delay}
}

# Start services in the order defined in cluster_controller.py
echo ""
echo "[1/8] Starting cAdvisor..."
start_service "cadvisor" 2

echo "[2/8] Starting Grafana..."
start_service "grafana" 2

echo "[3/8] Starting Node Exporter..."
start_service "node_exporter" 2

echo "[4/8] Starting Prometheus..."
start_service "prometheus" 2

echo "[5/8] Starting pgAdmin..."
start_service "pgadmin" 2

echo "[6/8] Starting Nginx..."
start_service "nginx" 2

echo "[7/8] Starting Docker Engine (if not running)..."
start_service "docker" 2

echo "[8/8] Starting Flask API..."
start_service "flask" 5

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
