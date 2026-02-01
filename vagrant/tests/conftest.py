"""
Pytest configuration and fixtures for CSLE Vagrant integration tests.
"""
import os
import subprocess
import pytest


# Default configuration values
DEFAULT_CONFIG = {
    "leader_ip": "192.168.56.10",
    "postgres_user": "csle",
    "postgres_password": "csle192105Test",
    "postgres_db": "csle",
    "postgres_port": 5432,
    "flask_port": 7777,
    "grafana_port": 3000,
    "prometheus_port": 9090,
    "node_exporter_port": 9100,
    "pgadmin_port": 7778,
    "admin_username": "admin",
    "admin_password": "csle192105Test",
}


def get_config():
    """Get configuration from environment or use defaults."""
    config = DEFAULT_CONFIG.copy()
    config["leader_ip"] = os.environ.get("CSLE_LEADER_IP", config["leader_ip"])
    config["postgres_password"] = os.environ.get(
        "CSLE_POSTGRES_PASSWORD", config["postgres_password"]
    )
    return config


@pytest.fixture(scope="session")
def config():
    """Provide test configuration."""
    return get_config()


@pytest.fixture(scope="session")
def leader_ip(config):
    """Get leader IP address."""
    return config["leader_ip"]


@pytest.fixture(scope="session")
def db_connection_params(config):
    """Get database connection parameters."""
    return {
        "host": config["leader_ip"],
        "port": config["postgres_port"],
        "user": config["postgres_user"],
        "password": config["postgres_password"],
        "dbname": config["postgres_db"],
    }


@pytest.fixture(scope="session")
def api_base_url(config):
    """Get Flask API base URL."""
    return f"http://{config['leader_ip']}:{config['flask_port']}"


@pytest.fixture(scope="session")
def grafana_url(config):
    """Get Grafana URL."""
    return f"http://{config['leader_ip']}:{config['grafana_port']}"


@pytest.fixture(scope="session")
def prometheus_url(config):
    """Get Prometheus URL."""
    return f"http://{config['leader_ip']}:{config['prometheus_port']}"


@pytest.fixture(scope="session")
def node_exporter_url(config):
    """Get Node Exporter URL."""
    return f"http://{config['leader_ip']}:{config['node_exporter_port']}"


def run_command(cmd, timeout=30):
    """Run a shell command and return output."""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "Command timed out"


@pytest.fixture
def run_shell():
    """Fixture to run shell commands."""
    return run_command


def is_running_in_vagrant():
    """Check if tests are running inside a Vagrant VM."""
    return os.path.exists("/vagrant") or os.environ.get("VAGRANT_VM") == "true"


@pytest.fixture(scope="session")
def in_vagrant():
    """Check if running inside Vagrant VM."""
    return is_running_in_vagrant()
