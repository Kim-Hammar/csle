#!/bin/bash

# --- CONFIGURATION ---
BASE_PATH="/srsRAN_4G/build/srsue/src"
BINARY="srsue"
CONF_FILE="ue.conf"
LOG_FILE="ue.log"
NETNS_NAME="ue1"
PING_TARGET="10.45.0.1"

FULL_BIN="${BASE_PATH}/${BINARY}"
FULL_CONF="${BASE_PATH}/${CONF_FILE}"

# --- FUNCTIONS ---

usage() {
    echo "Usage: $0 <start|stop|status|init|ping>"
    echo "  init    : Creates the '$NETNS_NAME' network namespace and lists all namespaces."
    echo "  ping    : Pings the Core Network ($PING_TARGET) from inside '$NETNS_NAME'."
    exit 1
}

get_pid() {
    pgrep -f "$FULL_BIN"
}

start_ue() {
    if get_pid > /dev/null; then
        echo "$BINARY is already running."
        return 0
    fi

    echo "Starting $BINARY from $FULL_BIN (Output forced to $LOG_FILE via 'script')..."
    nohup script -f "$LOG_FILE" -c "\"$FULL_BIN\" \"$FULL_CONF\"" > /dev/null 2>&1 &

    sleep 3
    if get_pid > /dev/null; then
        echo "$BINARY started successfully (PID: $(get_pid))."
        echo "LOG: All output is now in $LOG_FILE"
    else
        echo "Error: $BINARY failed to start. Check $LOG_FILE for details."
        pkill -f "script -f $LOG_FILE" 2>/dev/null
    fi
}

stop_ue() {
    local pid=$(get_pid)

    if [ -z "$pid" ]; then
        echo "$BINARY is not running."
        return 0
    fi

    echo "Stopping $BINARY (PID: $pid)..."
    pkill -f "$FULL_BIN"
    pkill -f "script -f $LOG_FILE" 2>/dev/null

    sleep 1
    if get_pid > /dev/null; then
        echo "Warning: $BINARY might still be running. Sending SIGKILL."
        pkill -9 -f "$FULL_BIN"
    else
        echo "$BINARY stopped successfully."
    fi
}

status_ue() {
    local pid=$(get_pid)

    if [ -n "$pid" ]; then
        echo "$BINARY is RUNNING (PID: $pid)."
    else
        echo "$BINARY is STOPPED."
    fi
}

init_namespace() {
    if ip netns list | grep -q "$NETNS_NAME"; then
        echo "Network Namespace '$NETNS_NAME' already exists."
        ip netns list
        return 0
    fi

    echo "Creating Network Namespace '$NETNS_NAME'..."
    sudo ip netns add "$NETNS_NAME"
    if [ $? -eq 0 ]; then
        echo "Namespace '$NETNS_NAME' created successfully."
        ip netns list
    else
        echo "Error creating Network Namespace."
        return 1
    fi
}

ping_core() {
    if ! ip netns list | grep -q "$NETNS_NAME"; then
        echo "Error: Network Namespace '$NETNS_NAME' does not exist."
        echo "Please run './$0 init' first."
        return 1
    fi

    echo "--- Pinging $PING_TARGET from inside '$NETNS_NAME'. Press Ctrl+C to stop. ---"
    sudo ip netns exec "$NETNS_NAME" ping "$PING_TARGET"
}

if [ $# -ne 1 ]; then
    usage
fi

ACTION=$1

case "$ACTION" in
    start)
        start_ue
        ;;
    stop)
        stop_ue
        ;;
    status)
        status_ue
        ;;
    init)
        init_namespace
        ;;
    ping)
        ping_core
        ;;
    *)
        usage
        ;;
esac