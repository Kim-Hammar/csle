#!/bin/bash

# --- CONFIGURATION ---
BIN_DIR="/usr/bin"          # Location of Open5GS binaries
CONF_DIR="/etc/open5gs"     # Location of YAML config files
LOG_DIR="$(pwd)/logs"       # <--- FIXED: Uses absolute path
WEBUI_DIR="/usr/lib/node_modules/open5gs" # WebUI source location

# Define the local IPs needed for the Open5GS Core. These are added to 'lo' in network_init.
declare -a CORE_IPS=(
    "127.0.0.2/8"   # MME
    "127.0.0.3/8"   # SGWC
    "127.0.0.4/8"   # SMF
    "127.0.0.6/8"   # SGWU
    "127.0.0.8/8"   # HSS
    "127.0.0.9/8"   # PCRF
    "127.0.0.10/8"  # NRF
    "127.0.0.11/8"  # AUSF
    "127.0.0.12/8"  # UDM
    "127.0.0.13/8"  # PCF
    "127.0.0.14/8"  # NSSF
    "127.0.0.15/8"  # BSF
    "127.0.0.20/8"  # UDR
    "127.0.0.200/8" # SCP
    "127.0.0.250/8" # SEPP (Primary)
    "127.0.0.251/8" # SEPP
    "127.0.0.252/8" # SEPP
)

mkdir -p "$LOG_DIR"

START_ORDER=(
    "mongo"
    "mme" "sgwc" "smf" "amf" "sgwu" "upf" "hss"
    "pcrf" "nrf" "scp" "sepp" "ausf" "udm" "pcf"
    "nssf" "bsf" "udr"
    "webui"
)

declare -A SERVICES
SERVICES=(
    ["mongo"]="mongod none"
    ["mme"]="open5gs-mmed mme.yaml"
    ["sgwc"]="open5gs-sgwcd sgwc.yaml"
    ["smf"]="open5gs-smfd smf.yaml"
    ["amf"]="open5gs-amfd amf.yaml"
    ["sgwu"]="open5gs-sgwud sgwu.yaml"
    ["upf"]="open5gs-upfd upf.yaml"
    ["hss"]="open5gs-hssd hss.yaml"
    ["pcrf"]="open5gs-pcrfd pcrf.yaml"
    ["nrf"]="open5gs-nrfd nrf.yaml"
    ["scp"]="open5gs-scpd scp.yaml"
    ["sepp"]="open5gs-seppd sepp1.yaml"
    ["ausf"]="open5gs-ausfd ausf.yaml"
    ["udm"]="open5gs-udmd udm.yaml"
    ["pcf"]="open5gs-pcfd pcf.yaml"
    ["nssf"]="open5gs-nssfd nssf.yaml"
    ["bsf"]="open5gs-bsfd bsf.yaml"
    ["udr"]="open5gs-udrd udr.yaml"
    ["webui"]="node_server_index.js none"
)

usage() {
    echo "Usage: $0 <service_name|all> <start|stop|status|init>"
    echo "  $0 mongo init       : Initialize MongoDB database."
    echo "  $0 all init         : Run network and database initialization."
    echo "Example: $0 all start"
    exit 1
}

is_running() {
    pgrep -f "$1" > /dev/null
}

network_init() {
    echo "Setting up loopback addresses..."

    for ip_mask in "${CORE_IPS[@]}"; do
        echo "  Adding $ip_mask to loopback (lo)..."
        sudo ip addr add "$ip_mask" dev lo
    done

    echo "Network initialization complete (ogstun setup deferred to UPF start)."
    return 0
}

start_service() {
    local bin=$1
    local conf=$2
    local name=$3
    local console_log="$LOG_DIR/${name}_console.log"

    if [ "$name" == "mongo" ]; then
        if is_running "mongod"; then
            echo "mongo is already running."
        else
            echo "Starting mongo (logging console output to $console_log)..."
            sudo mkdir -p /var/log/mongodb
            sudo nohup "$BIN_DIR/mongod" --bind_ip_all --fork --logpath /var/log/mongodb/mongod.log > "$console_log" 2>&1 &
        fi
        return
    fi

    if [ "$name" == "webui" ]; then
        if is_running "server/index.js"; then
            echo "webui is already running."
        else
            echo "Starting webui..."
            (
                cd "$WEBUI_DIR" || exit
                export NODE_ENV=production
                export HOSTNAME="0.0.0.0"
                nohup /usr/bin/node server/index.js > "$console_log" 2>&1 &
            )
            sleep 1
        fi
        return
    fi

    if is_running "$bin"; then
        echo "$name is already running."
    else
        echo "Starting $name..."
        nohup "$bin" -c "$FULL_CONF" > "$LOG_DIR/${name}d.log" 2>&1 &
        sleep 0.5

        if [ "$name" == "upf" ]; then
            echo "Running ogstun network setup after UPF start..."
            if ! ip link show ogstun > /dev/null 2>&1; then
                echo "  Creating missing ogstun TUN interface..."
                sudo ip tuntap add dev ogstun mode tun user root
            else
                echo "  ogstun interface already exists."
            fi

            sudo ip addr add 10.45.0.1/16 dev ogstun
            sudo ip link set ogstun up
            echo "ogstun setup complete."
        fi
    fi
}

stop_service() {
    local bin=$1
    local name=$2
    local search_str="$bin"

    if [ "$name" == "mongo" ]; then
        search_str="mongod"
    elif [ "$name" == "webui" ]; then
        search_str="server/index.js"
    fi

    if is_running "$search_str"; then
        echo "Stopping $name..."
        pkill -f "$search_str"
    else
        echo "$name is not running."
    fi
}

check_status() {
    local bin=$1
    local name=$2
    local search_str="$bin"

    if [ "$name" == "mongo" ]; then
        search_str="mongod"
    elif [ "$name" == "webui" ]; then
        search_str="server/index.js"
    fi

    local pid=$(pgrep -f "$search_str" | head -n 1)

    if [ -n "$pid" ]; then
        printf "%-10s RUNNING (PID: %s)\n" "$name" "$pid"
    else
        printf "%-10s STOPPED\n" "$name"
    fi
}

init_mongo() {
    echo "Initializing MongoDB with Open5GS data..."
    local console_log="$LOG_DIR/mongo_init_console.log"
    local MONGO_PID=""

    if ! is_running "mongod"; then
        echo "MongoDB not running. Starting temporarily for initialization (logging to $console_log)..."
        sudo mongod --bind_ip_all > "$console_log" 2>&1 &
        MONGO_PID=$!
        sleep 3
    fi

    mongosh open5gs "$WEBUI_DIR/mongo-init.js"

    if [ -n "$MONGO_PID" ]; then
        kill $MONGO_PID 2>/dev/null
        echo "Temporarily started MongoDB stopped."
    fi
    echo "MongoDB initialization complete."
}

process_single() {
    local service=$1
    local action=$2

    if [ "$service" == "all" ] && [ "$action" == "init" ]; then
        network_init
        process_single "mongo" "init"
        return
    fi

    if [[ -z "${SERVICES[$service]}" ]]; then
        echo "Error: Service '$service' is not defined."
        usage
    fi

    IFS=' ' read -r BIN_NAME CONF_NAME <<< "${SERVICES[$service]}"
    FULL_BIN="$BIN_DIR/$BIN_NAME"

    if [ "$CONF_NAME" == "none" ]; then
        FULL_CONF="none"
    else
        FULL_CONF="$CONF_DIR/$CONF_NAME"
    fi

    case "$action" in
        start)   start_service "$FULL_BIN" "$FULL_CONF" "$service" ;;
        stop)    stop_service "$FULL_BIN" "$service" ;;
        status)  check_status "$FULL_BIN" "$service" ;;
        init)
            if [ "$service" == "mongo" ]; then
                init_mongo
            else
                echo "Error: 'init' is only valid for 'mongo' or 'all'."
            fi
            ;;
        *)       usage ;;
    esac
}

if [ $# -ne 2 ]; then
    usage
fi

TARGET=$1
ACTION=$2

if [ "$TARGET" == "all" ]; then
    if [ "$ACTION" == "start" ]; then
        for svc in "${START_ORDER[@]}"; do
            process_single "$svc" "start"
        done
    elif [ "$ACTION" == "stop" ]; then
        for (( idx=${#START_ORDER[@]}-1 ; idx>=0 ; idx-- )) ; do
            process_single "${START_ORDER[idx]}" "stop"
        done
    elif [ "$ACTION" == "status" ]; then
        for svc in "${START_ORDER[@]}"; do
            process_single "$svc" "status"
        done
    elif [ "$ACTION" == "init" ]; then
        process_single "all" "init"
    else
        usage
    fi
else
    process_single "$TARGET" "$ACTION"
fi