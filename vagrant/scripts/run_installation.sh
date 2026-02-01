#!/bin/bash
# Script to run CSLE Ansible installation manually
# Can be used for re-running installation or debugging

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VAGRANT_DIR="$(dirname "${SCRIPT_DIR}")"
CSLE_HOME="${HOME}/csle"

# Default values
INVENTORY="${VAGRANT_DIR}/ansible/inventory_vagrant"
PLAYBOOK="${CSLE_HOME}/ansible/install.yml"
VERBOSE=""
SKIP_TAGS=""
LIMIT="all"

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -i|--inventory)
            INVENTORY="$2"
            shift 2
            ;;
        -p|--playbook)
            PLAYBOOK="$2"
            shift 2
            ;;
        -v|--verbose)
            VERBOSE="-vvv"
            shift
            ;;
        --skip-tags)
            SKIP_TAGS="--skip-tags $2"
            shift 2
            ;;
        -l|--limit)
            LIMIT="$2"
            shift 2
            ;;
        -h|--help)
            echo "Usage: $0 [options]"
            echo ""
            echo "Options:"
            echo "  -i, --inventory FILE   Ansible inventory file"
            echo "  -p, --playbook FILE    Ansible playbook to run"
            echo "  -v, --verbose          Enable verbose output"
            echo "  --skip-tags TAGS       Skip specified Ansible tags"
            echo "  -l, --limit HOSTS      Limit to specific hosts"
            echo "  -h, --help             Show this help message"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

echo "=============================================="
echo "Running CSLE Ansible Installation"
echo "=============================================="
echo "Inventory: ${INVENTORY}"
echo "Playbook: ${PLAYBOOK}"
echo "Limit: ${LIMIT}"
echo "=============================================="

# Check if inventory exists
if [ ! -f "${INVENTORY}" ]; then
    echo "Error: Inventory file not found: ${INVENTORY}"
    exit 1
fi

# Check if playbook exists
if [ ! -f "${PLAYBOOK}" ]; then
    echo "Error: Playbook file not found: ${PLAYBOOK}"
    exit 1
fi

# Run Ansible playbook
cd "${CSLE_HOME}/ansible"
ansible-playbook \
    -i "${INVENTORY}" \
    ${PLAYBOOK} \
    --limit "${LIMIT}" \
    ${VERBOSE} \
    ${SKIP_TAGS} \
    -e "ansible_python_interpreter=/usr/bin/python3"

echo "=============================================="
echo "Installation complete!"
echo "=============================================="
