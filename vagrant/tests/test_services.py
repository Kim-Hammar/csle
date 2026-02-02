"""
Tests for verifying system services are running correctly.
"""
import subprocess
from typing import Any, Callable, Dict, Tuple

import pytest


class TestSystemServices:
    """Test that required system services are running."""

    @pytest.mark.parametrize("service", [
        "postgresql",
        "nginx",
        "docker",
    ])
    def test_systemd_service_running(self, service: str, in_vagrant: bool) -> None:
        """
        Test that systemd services are active and running.

        :param service: the service name to check
        :param in_vagrant: whether tests are running inside Vagrant VM
        :return: None
        """
        if not in_vagrant:
            pytest.skip("Test requires running inside Vagrant VM")

        result = subprocess.run(
            ["systemctl", "is-active", service],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0, f"Service {service} is not active"
        assert result.stdout.strip() == "active", f"Service {service} status: {result.stdout}"

    @pytest.mark.parametrize("service", [
        "postgresql",
        "nginx",
        "docker",
    ])
    def test_systemd_service_enabled(self, service: str, in_vagrant: bool) -> None:
        """
        Test that systemd services are enabled to start on boot.

        :param service: the service name to check
        :param in_vagrant: whether tests are running inside Vagrant VM
        :return: None
        """
        if not in_vagrant:
            pytest.skip("Test requires running inside Vagrant VM")

        result = subprocess.run(
            ["systemctl", "is-enabled", service],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0, f"Service {service} is not enabled"


class TestCSLEServices:
    """Test that CSLE-specific services are accessible."""

    def test_flask_api_listening(self, run_shell: Callable[..., Tuple[int, str, str]],
                                 config: Dict[str, Any], in_vagrant: bool) -> None:
        """
        Test that Flask API is listening on the expected port.

        :param run_shell: fixture to run shell commands
        :param config: the test configuration dictionary
        :param in_vagrant: whether tests are running inside Vagrant VM
        :return: None
        """
        if not in_vagrant:
            pytest.skip("Test requires running inside Vagrant VM")

        port = config["flask_port"]
        returncode, stdout, stderr = run_shell(f"ss -tlnp | grep :{port}")
        assert returncode == 0, f"Flask API not listening on port {port}"

    def test_prometheus_listening(self, run_shell: Callable[..., Tuple[int, str, str]],
                                  config: Dict[str, Any], in_vagrant: bool) -> None:
        """
        Test that Prometheus is listening on the expected port (optional).

        :param run_shell: fixture to run shell commands
        :param config: the test configuration dictionary
        :param in_vagrant: whether tests are running inside Vagrant VM
        :return: None
        """
        if not in_vagrant:
            pytest.skip("Test requires running inside Vagrant VM")

        port = config["prometheus_port"]
        returncode, stdout, stderr = run_shell(f"ss -tlnp | grep :{port}")
        if returncode != 0:
            pytest.skip(f"Prometheus not listening on port {port} (service may not be installed)")

    def test_grafana_listening(self, run_shell: Callable[..., Tuple[int, str, str]],
                               config: Dict[str, Any], in_vagrant: bool) -> None:
        """
        Test that Grafana is listening on the expected port (optional).

        :param run_shell: fixture to run shell commands
        :param config: the test configuration dictionary
        :param in_vagrant: whether tests are running inside Vagrant VM
        :return: None
        """
        if not in_vagrant:
            pytest.skip("Test requires running inside Vagrant VM")

        port = config["grafana_port"]
        returncode, stdout, stderr = run_shell(f"ss -tlnp | grep :{port}")
        if returncode != 0:
            pytest.skip(f"Grafana not listening on port {port} (service may not be installed)")

    def test_node_exporter_listening(self, run_shell: Callable[..., Tuple[int, str, str]],
                                     config: Dict[str, Any], in_vagrant: bool) -> None:
        """
        Test that Node Exporter is listening on the expected port (optional).

        :param run_shell: fixture to run shell commands
        :param config: the test configuration dictionary
        :param in_vagrant: whether tests are running inside Vagrant VM
        :return: None
        """
        if not in_vagrant:
            pytest.skip("Test requires running inside Vagrant VM")

        port = config["node_exporter_port"]
        returncode, stdout, stderr = run_shell(f"ss -tlnp | grep :{port}")
        if returncode != 0:
            pytest.skip(f"Node Exporter not listening on port {port} (service may not be installed)")


class TestProcesses:
    """Test that expected processes are running."""

    def test_postgres_process(self, run_shell: Callable[..., Tuple[int, str, str]],
                              in_vagrant: bool) -> None:
        """
        Test that PostgreSQL process is running.

        :param run_shell: fixture to run shell commands
        :param in_vagrant: whether tests are running inside Vagrant VM
        :return: None
        """
        if not in_vagrant:
            pytest.skip("Test requires running inside Vagrant VM")

        returncode, stdout, stderr = run_shell("pgrep -x postgres")
        assert returncode == 0, "PostgreSQL process not found"

    def test_nginx_process(self, run_shell: Callable[..., Tuple[int, str, str]],
                           in_vagrant: bool) -> None:
        """
        Test that Nginx process is running.

        :param run_shell: fixture to run shell commands
        :param in_vagrant: whether tests are running inside Vagrant VM
        :return: None
        """
        if not in_vagrant:
            pytest.skip("Test requires running inside Vagrant VM")

        returncode, stdout, stderr = run_shell("pgrep -x nginx")
        assert returncode == 0, "Nginx process not found"

    def test_dockerd_process(self, run_shell: Callable[..., Tuple[int, str, str]],
                             in_vagrant: bool) -> None:
        """
        Test that Docker daemon is running.

        :param run_shell: fixture to run shell commands
        :param in_vagrant: whether tests are running inside Vagrant VM
        :return: None
        """
        if not in_vagrant:
            pytest.skip("Test requires running inside Vagrant VM")

        returncode, stdout, stderr = run_shell("pgrep -x dockerd")
        assert returncode == 0, "Docker daemon process not found"
