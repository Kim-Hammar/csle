"""
Tests for verifying system services are running correctly.
"""
import subprocess
import pytest


class TestSystemServices:
    """Test that required system services are running."""

    @pytest.mark.parametrize("service", [
        "postgresql",
        "nginx",
        "docker",
    ])
    def test_systemd_service_running(self, service, in_vagrant):
        """Test that systemd services are active and running."""
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
    def test_systemd_service_enabled(self, service, in_vagrant):
        """Test that systemd services are enabled to start on boot."""
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

    def test_flask_api_listening(self, run_shell, config, in_vagrant):
        """Test that Flask API is listening on the expected port."""
        if not in_vagrant:
            pytest.skip("Test requires running inside Vagrant VM")

        port = config["flask_port"]
        returncode, stdout, stderr = run_shell(f"ss -tlnp | grep :{port}")
        assert returncode == 0, f"Flask API not listening on port {port}"

    def test_prometheus_listening(self, run_shell, config, in_vagrant):
        """Test that Prometheus is listening on the expected port."""
        if not in_vagrant:
            pytest.skip("Test requires running inside Vagrant VM")

        port = config["prometheus_port"]
        returncode, stdout, stderr = run_shell(f"ss -tlnp | grep :{port}")
        assert returncode == 0, f"Prometheus not listening on port {port}"

    def test_grafana_listening(self, run_shell, config, in_vagrant):
        """Test that Grafana is listening on the expected port."""
        if not in_vagrant:
            pytest.skip("Test requires running inside Vagrant VM")

        port = config["grafana_port"]
        returncode, stdout, stderr = run_shell(f"ss -tlnp | grep :{port}")
        assert returncode == 0, f"Grafana not listening on port {port}"

    def test_node_exporter_listening(self, run_shell, config, in_vagrant):
        """Test that Node Exporter is listening on the expected port."""
        if not in_vagrant:
            pytest.skip("Test requires running inside Vagrant VM")

        port = config["node_exporter_port"]
        returncode, stdout, stderr = run_shell(f"ss -tlnp | grep :{port}")
        assert returncode == 0, f"Node Exporter not listening on port {port}"


class TestProcesses:
    """Test that expected processes are running."""

    def test_postgres_process(self, run_shell, in_vagrant):
        """Test that PostgreSQL process is running."""
        if not in_vagrant:
            pytest.skip("Test requires running inside Vagrant VM")

        returncode, stdout, stderr = run_shell("pgrep -x postgres")
        assert returncode == 0, "PostgreSQL process not found"

    def test_nginx_process(self, run_shell, in_vagrant):
        """Test that Nginx process is running."""
        if not in_vagrant:
            pytest.skip("Test requires running inside Vagrant VM")

        returncode, stdout, stderr = run_shell("pgrep -x nginx")
        assert returncode == 0, "Nginx process not found"

    def test_dockerd_process(self, run_shell, in_vagrant):
        """Test that Docker daemon is running."""
        if not in_vagrant:
            pytest.skip("Test requires running inside Vagrant VM")

        returncode, stdout, stderr = run_shell("pgrep -x dockerd")
        assert returncode == 0, "Docker daemon process not found"
