---
title: Tests
permalink: /docs/tests/
---

## Tests

CSLE uses `pytest` for Python tests and integration tests, and `jest` for JavaScript tests.

The Python unit tests are available at:

- `csle/simulation-system/libs/csle-base/tests`
- `csle/simulation-system/libs/csle-agents/tests`
- `csle/simulation-system/libs/csle-attacker/tests`
- `csle/simulation-system/libs/csle-collector/tests`
- `csle/simulation-system/libs/csle-common/tests`
- `csle/simulation-system/libs/csle-defender/tests`
- `csle/simulation-system/libs/csle-rest-api/tests`
- `csle/simulation-system/libs/csle-ryu/tests`
- `csle/simulation-system/libs/csle-system-identification/tests`
- `csle/simulation-system/libs/gym-csle-stopping-game/tests`
- `csle/simulation-system/libs/csle-cluster/tests`
- `csle/simulation-system/libs/gym-csle-intrusion-response-game/tests`
- `csle/simulation-system/libs/gym-csle-apt-game/tests`
- `csle/simulation-system/libs/gym-csle-cyborg/tests`
- `csle/simulation-system/libs/csle-tolerance/tests`
- `csle/simulation-system/libs/csle-attack-profiler/tests`

To run the Python unit tests, execute the command:

```bash
simulation-system/libs/unit_tests.sh
```

<p class="captionFig">
Listing 135: Command to run the Python unit tests.
</p>

When adding new Python unit tests note that:

- All unit tests must be written in a `tests/` directory inside the Python project.
- File names should strictly start with "`tests_`".
- Function names should strictly start with "`test`".

The JavaScript unit tests are available at:

```bash
csle/management-system/csle-mgmt-webapp/src/
```

<p class="captionFig">
Listing 136: Directory with the JavaScript unit tests.
</p>

To run the JavaScript unit tests, execute the command:

```bash
cd management-system/csle-mgmt-webapp; npm test
```

<p class="captionFig">
Listing 137: Command to run the JavaScript unit tests.
</p>

### Integration Tests

The CSLE integration tests use Vagrant to provision virtual machines and validate the complete installation
of the CSLE platform. The integration tests spin up Ubuntu VMs, run the Ansible installation playbooks,
and verify that all components are working correctly.

#### Prerequisites

Before running the integration tests, install Vagrant and VirtualBox:

```bash
# On Ubuntu/Debian
sudo apt-get install virtualbox vagrant

# On macOS
brew install --cask virtualbox vagrant
```

<p class="captionFig">
Listing 138: Installing Vagrant and VirtualBox.
</p>

#### Running the Integration Tests

To run the single-node integration test, execute the commands:

```bash
cd vagrant
vagrant up
```

<p class="captionFig">
Listing 139: Commands to run the single-node integration test.
</p>

To run the two-node integration test (leader + worker topology), execute the commands:

```bash
cd vagrant
VAGRANT_CONFIG=config/two_node.yaml vagrant up
```

<p class="captionFig">
Listing 140: Commands to run the two-node integration test.
</p>

#### Verification Tests

After the VMs are provisioned, you can run the pytest verification suite:

```bash
vagrant ssh leader -c "cd /vagrant/tests && python3 -m pytest -v"
```

<p class="captionFig">
Listing 141: Command to run the verification tests.
</p>

The verification tests check:

- **Services**: PostgreSQL, Nginx, and Docker systemd services are running.
- **CSLE Services**: Flask API, Prometheus, Grafana, and Node Exporter are accessible.
- **Database**: Connection to the csle database, Citus extension, and all expected tables exist.
- **Docker**: Docker daemon is running, Swarm is initialized, and pgAdmin container is running.
- **Python**: Conda environment exists, all CSLE packages are installed, and the CLI is available.
- **API**: Login, emulations, and simulations endpoints respond correctly.

#### Cleanup

To destroy the VMs and free up disk space, execute the commands:

```bash
cd vagrant
vagrant destroy -f
vagrant box remove ubuntu/jammy64
```

<p class="captionFig">
Listing 142: Commands to clean up after running integration tests.
</p>
