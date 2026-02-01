# CSLE Vagrant Integration Test

This directory contains Vagrant configurations and test suites for validating the complete CSLE platform installation via Ansible playbooks.

## Prerequisites

- [Vagrant](https://www.vagrantup.com/downloads) >= 2.3.0
- [VirtualBox](https://www.virtualbox.org/wiki/Downloads) >= 7.0
- At least 16GB RAM
- At least 200GB free disk space
- [vagrant-disksize plugin](https://github.com/sprotheroe/vagrant-disksize) (install with `vagrant plugin install vagrant-disksize`)

## Quick Start

### Single Node (Full Installation)

```bash
cd vagrant
vagrant up
```

### Two Node Cluster

```bash
cd vagrant
VAGRANT_CONFIG=config/two_node.yaml vagrant up
```

## Configuration Options

| Config File | RAM | CPUs | Description |
|------------|-----|------|-------------|
| `config/single_node.yaml` | 16GB | 6 | Full single-node installation |
| `config/two_node.yaml` | 12GB + 8GB | 4 + 4 | Leader + Worker topology |

## Running Tests

### Inside the VM

```bash
# SSH into the leader node
vagrant ssh leader

# Run pytest tests
cd /vagrant/tests
pip3 install pytest requests psycopg2-binary
python3 -m pytest -v

# Or run the standalone verification script
python3 verify_installation.py
```

### From Host

```bash
# Run tests via SSH
vagrant ssh leader -c "cd /vagrant/tests && python3 -m pytest -v"

# Run verification script
vagrant ssh leader -c "cd /vagrant/tests && python3 verify_installation.py"
```

## Test Categories

| Test File | What It Verifies |
|-----------|-----------------|
| `test_services.py` | SystemD services (PostgreSQL, Nginx, Docker) |
| `test_database.py` | Database connectivity, Citus extension, schema tables |
| `test_docker.py` | Docker daemon, Swarm initialization, containers |
| `test_python_libraries.py` | Conda environment, CSLE packages, CLI |
| `test_endpoints.py` | REST API, Prometheus, Grafana, Node Exporter |

## Port Forwarding

When running locally, the following ports are forwarded to your host:

| Service | Guest Port | Host Port |
|---------|-----------|-----------|
| Nginx | 80 | 8080 |
| Flask API | 7777 | 7777 |
| Grafana | 3000 | 3000 |
| Prometheus | 9090 | 9090 |
| Node Exporter | 9100 | 9100 |
| PostgreSQL | 5432 | 5432 |
| pgAdmin | 7778 | 7778 |

## Managing VMs

```bash
# Check status
vagrant status

# SSH into a node
vagrant ssh leader
vagrant ssh worker  # (two-node config only)

# Halt VMs (preserves state)
vagrant halt

# Resume VMs
vagrant up

# Destroy VMs completely
vagrant destroy -f

# Re-run provisioning
vagrant provision
```

## Re-running Ansible Installation

If you need to re-run the Ansible installation manually:

```bash
vagrant ssh leader -c "/vagrant/scripts/run_installation.sh"

# With verbose output
vagrant ssh leader -c "/vagrant/scripts/run_installation.sh -v"

# Skip specific tags
vagrant ssh leader -c "/vagrant/scripts/run_installation.sh --skip-tags docker_images"
```

## Applying Vagrantfile Changes

If you modify the Vagrantfile or provisioner scripts, you need to destroy and recreate the VM for changes to take effect:

```bash
cd vagrant
vagrant destroy -f
vagrant up
```

Alternatively, to re-run provisioners on an existing VM:

```bash
vagrant provision
```

Note: `vagrant provision` only re-runs provisioners, it does not apply changes to VM configuration (memory, CPUs, disk size).

## Starting CSLE Services

CSLE services are automatically started after the Ansible installation completes. The services are started in the following order (as defined in `cluster_controller.py`):

1. cAdvisor
2. Grafana
3. Node Exporter
4. Prometheus
5. pgAdmin
6. Nginx
7. Docker Engine
8. Flask API

To manually start services:

```bash
# Start all services
vagrant ssh leader -c "/vagrant/scripts/start_services.sh vagrant"

# Or start individual services
vagrant ssh leader -c "source /home/vagrant/anaconda3/etc/profile.d/conda.sh && conda activate base && export CSLE_HOME=/home/vagrant/csle && csle start flask"
```

## Cleanup

After testing, you can clean up to free disk space. The VMs and box images can consume 50-100GB+.

### Quick Cleanup (Destroy VMs Only)

This removes the VMs but keeps the downloaded box image for faster future runs:

```bash
cd vagrant
vagrant destroy -f
```

### Full Cleanup (Free All Disk Space)

To completely remove everything and reclaim all disk space:

```bash
cd vagrant

# 1. Destroy all VMs
vagrant destroy -f

# 2. Remove the downloaded box image (~2GB)
vagrant box remove ubuntu/jammy64 --all

# 3. Clean up any orphaned VirtualBox VMs (if needed)
VBoxManage list vms
# If you see leftover "csle-leader" or "csle-worker" VMs:
VBoxManage unregistervm "csle-leader" --delete
VBoxManage unregistervm "csle-worker" --delete

# 4. Remove Vagrant's local state
rm -rf .vagrant/
```

### Disk Space Reference

| Component | Approximate Size |
|-----------|-----------------|
| Ubuntu box image | ~2 GB |
| Single-node VM disk | ~100-150 GB |
| Two-node VM disks | ~150-250 GB |
| Total (single-node) | ~100-150 GB |
| Total (two-node) | ~150-250 GB |

### Verify Cleanup

```bash
# Check no VMs are running
vagrant global-status --prune

# Check no boxes remain (if you want full cleanup)
vagrant box list

# Check VirtualBox has no leftover VMs
VBoxManage list vms
```

## Troubleshooting

### VirtualBox Kernel Extension (macOS)

If VirtualBox fails to start on macOS:

1. Go to System Preferences > Security & Privacy
2. Allow the Oracle kernel extension
3. Restart your computer

### Ansible Provisioning Fails

Check the Ansible log:

```bash
vagrant ssh leader -c "cat /var/log/ansible.log"
```

Re-run provisioning with verbose output:

```bash
vagrant provision --debug
```

### SSH Connection Issues

```bash
# Regenerate SSH key
vagrant ssh-config > ssh-config
ssh -F ssh-config leader
```

### Out of Disk Space

The default VM disk size is 200GB. CSLE Docker images require ~100GB of disk space. Ensure you have sufficient free space on your host:

```bash
df -h
```

If you see "no space left on device" errors during provisioning, you may need to:
1. Install the vagrant-disksize plugin: `vagrant plugin install vagrant-disksize`
2. Destroy and recreate the VM: `vagrant destroy -f && vagrant up`

### Services Not Starting

Check service status inside the VM:

```bash
vagrant ssh leader
sudo systemctl status postgresql nginx docker
sudo journalctl -u postgresql -n 50
```

## File Structure

```
vagrant/
├── Vagrantfile                  # Main Vagrant configuration
├── README.md                    # This file
├── config/
│   ├── single_node.yaml         # Full single-node config
│   └── two_node.yaml            # Leader + Worker config
├── scripts/
│   ├── provision.sh             # VM provisioning script
│   ├── run_installation.sh      # Manual Ansible runner
│   └── start_services.sh        # Start CSLE services after installation
├── tests/
│   ├── conftest.py              # pytest fixtures
│   ├── test_services.py         # Service tests
│   ├── test_database.py         # Database tests
│   ├── test_docker.py           # Docker tests
│   ├── test_python_libraries.py # Python package tests
│   ├── test_endpoints.py        # API endpoint tests
│   └── verify_installation.py   # Standalone verification
└── ansible/
    ├── inventory_vagrant        # Single-node inventory
    └── inventory_vagrant_two_node # Two-node inventory
```

## Default Credentials

| Service | Username | Password |
|---------|----------|----------|
| CSLE Admin | admin | csle192105Test |
| PostgreSQL | csle | csle192105Test |
| Grafana | admin | csle192105Test |
| pgAdmin | csle@csle.com | csle192105Test |

## Author & Maintainer

Kim Hammar <kimham@kth.se>

## Copyright and license

[LICENSE](../LICENSE.md)

Creative Commons

(C) 2020-2026, Kim Hammar
