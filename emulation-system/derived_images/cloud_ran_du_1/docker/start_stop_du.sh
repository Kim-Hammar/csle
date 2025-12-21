#!/bin/bash

# --- CONFIGURATION ---
BASE_PATH="/srsRAN_Project/build/apps/du"
BINARY="srsdu"
CONF_FILE="du.yml"
LOG_FILE="/du.log"

FULL_BIN="${BASE_PATH}/${BINARY}"
FULL_CONF="${BASE_PATH}/${CONF_FILE}"

# --- FUNCTIONS ---

usage() {
    echo "Usage: $0 <start|stop|status>"
    exit 1
}

get_pid() {
    pgrep -f "$FULL_BIN"
}

# Function to start the DU
start_du() {
    if get_pid > /dev/null; then
        echo "$BINARY is already running."
        return 0
    fi

    echo "Starting $BINARY from $FULL_BIN (Output forced to $LOG_FILE via 'script')..."
    nohup script -f "$LOG_FILE" -c "\"$FULL_BIN\" -c \"$FULL_CONF\"" > /dev/null 2>&1 &
    sleep 2
    if get_pid > /dev/null; then
        echo "$BINARY started successfully (PID: $(get_pid))."
        echo "LOG: All output is now in $LOG_FILE"
    else
        echo "Error: $BINARY failed to start. Check $LOG_FILE for details."
    fi
}

stop_du() {
    local pid=$(get_pid)

    if [ -z "$pid" ]; then
        echo "$BINARY is not running."
        return 0
    fi

    echo "Stopping $BINARY (PID: $pid)..."
    pkill -f "$FULL_BIN"

    sleep 1
    if get_pid > /dev/null; then
        echo "Warning: $BINARY might still be running. Sending SIGKILL."
        pkill -9 -f "$FULL_BIN"
    else
        echo "$BINARY stopped successfully."
    fi
}

status_du() {
    local pid=$(get_pid | head -n1)

    if [ -n "$pid" ]; then
        echo "$BINARY RUNNING (PID: $pid)"
    else
        echo "$BINARY STOPPED"
    fi
}

if [ $# -ne 1 ]; then
    usage
fi

ACTION=$1

case "$ACTION" in
    start)
        start_du
        ;;
    stop)
        stop_du
        ;;
    status)
        status_du
        ;;
    *)
        usage
        ;;
esac