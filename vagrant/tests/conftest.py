"""
Pytest configuration and fixtures for CSLE Vagrant integration tests.
"""
import os
import subprocess
from typing import Any, Callable, Dict, Tuple

import pytest


# Default configuration values
DEFAULT_CONFIG: Dict[str, Any] = {
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


def get_config() -> Dict[str, Any]:
    """
    Get configuration from environment or use defaults.

    :return: configuration dictionary with test settings
    """
    config = DEFAULT_CONFIG.copy()
    config["leader_ip"] = os.environ.get("CSLE_LEADER_IP", config["leader_ip"])
    config["postgres_password"] = os.environ.get(
        "CSLE_POSTGRES_PASSWORD", config["postgres_password"]
    )
    return config


@pytest.fixture(scope="session")
def config() -> Dict[str, Any]:
    """
    Provide test configuration.

    :return: configuration dictionary
    """
    return get_config()


@pytest.fixture(scope="session")
def leader_ip(config: Dict[str, Any]) -> str:
    """
    Get leader IP address.

    :param config: the test configuration dictionary
    :return: leader IP address string
    """
    return config["leader_ip"]


@pytest.fixture(scope="session")
def db_connection_params(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Get database connection parameters.

    :param config: the test configuration dictionary
    :return: dictionary with database connection parameters
    """
    return {
        "host": config["leader_ip"],
        "port": config["postgres_port"],
        "user": config["postgres_user"],
        "password": config["postgres_password"],
        "dbname": config["postgres_db"],
    }


@pytest.fixture(scope="session")
def api_base_url(config: Dict[str, Any]) -> str:
    """
    Get Flask API base URL.

    :param config: the test configuration dictionary
    :return: Flask API base URL string
    """
    return f"http://{config['leader_ip']}:{config['flask_port']}"


@pytest.fixture(scope="session")
def grafana_url(config: Dict[str, Any]) -> str:
    """
    Get Grafana URL.

    :param config: the test configuration dictionary
    :return: Grafana URL string
    """
    return f"http://{config['leader_ip']}:{config['grafana_port']}"


@pytest.fixture(scope="session")
def prometheus_url(config: Dict[str, Any]) -> str:
    """
    Get Prometheus URL.

    :param config: the test configuration dictionary
    :return: Prometheus URL string
    """
    return f"http://{config['leader_ip']}:{config['prometheus_port']}"


@pytest.fixture(scope="session")
def node_exporter_url(config: Dict[str, Any]) -> str:
    """
    Get Node Exporter URL.

    :param config: the test configuration dictionary
    :return: Node Exporter URL string
    """
    return f"http://{config['leader_ip']}:{config['node_exporter_port']}"


def run_command(cmd: str, timeout: int = 30) -> Tuple[int, str, str]:
    """
    Run a shell command and return output.

    :param cmd: the shell command to execute
    :param timeout: command timeout in seconds
    :return: tuple of (return code, stdout, stderr)
    """
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            executable='/bin/bash',
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "Command timed out"


@pytest.fixture
def run_shell() -> Callable[..., Tuple[int, str, str]]:
    """
    Fixture to run shell commands.

    :return: the run_command function
    """
    return run_command


def is_running_in_vagrant() -> bool:
    """
    Check if tests are running inside a Vagrant VM.

    :return: True if running in Vagrant, False otherwise
    """
    return os.path.exists("/vagrant") or os.environ.get("VAGRANT_VM") == "true"


@pytest.fixture(scope="session")
def in_vagrant() -> bool:
    """
    Check if running inside Vagrant VM.

    :return: True if running in Vagrant, False otherwise
    """
    return is_running_in_vagrant()
