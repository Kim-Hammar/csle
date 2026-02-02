"""
Tests for verifying Docker and Docker Swarm setup.
"""
import pytest


class TestDockerDaemon:
    """Test Docker daemon is running and configured correctly."""

    def test_docker_daemon_running(self, run_shell, in_vagrant):
        """Test that Docker daemon is running."""
        if not in_vagrant:
            pytest.skip("Test requires running inside Vagrant VM")

        returncode, stdout, stderr = run_shell("docker info")
        assert returncode == 0, f"Docker daemon not accessible: {stderr}"

    def test_docker_version(self, run_shell, in_vagrant):
        """Test Docker version is installed."""
        if not in_vagrant:
            pytest.skip("Test requires running inside Vagrant VM")

        returncode, stdout, stderr = run_shell("docker --version")
        assert returncode == 0, "Failed to get Docker version"
        assert "Docker version" in stdout

    def test_docker_compose_installed(self, run_shell, in_vagrant):
        """Test that Docker Compose is available."""
        if not in_vagrant:
            pytest.skip("Test requires running inside Vagrant VM")

        returncode, stdout, stderr = run_shell("docker compose version")
        assert returncode == 0, f"Docker Compose not available: {stderr}"


class TestDockerSwarm:
    """Test Docker Swarm is initialized and configured."""

    def test_swarm_initialized(self, run_shell, in_vagrant):
        """Test that Docker Swarm is initialized."""
        if not in_vagrant:
            pytest.skip("Test requires running inside Vagrant VM")

        returncode, stdout, stderr = run_shell("docker info --format '{{.Swarm.LocalNodeState}}'")
        assert returncode == 0, f"Failed to get Swarm status: {stderr}"
        assert stdout.strip() == "active", f"Swarm not active, state: {stdout.strip()}"

    def test_node_is_manager(self, run_shell, in_vagrant):
        """Test that the leader node is a Swarm manager."""
        if not in_vagrant:
            pytest.skip("Test requires running inside Vagrant VM")

        returncode, stdout, stderr = run_shell(
            "docker info --format '{{.Swarm.ControlAvailable}}'"
        )
        assert returncode == 0, f"Failed to get manager status: {stderr}"
        assert stdout.strip() == "true", "Node is not a Swarm manager"

    def test_swarm_node_list(self, run_shell, in_vagrant):
        """Test that we can list Swarm nodes."""
        if not in_vagrant:
            pytest.skip("Test requires running inside Vagrant VM")

        returncode, stdout, stderr = run_shell("docker node ls")
        assert returncode == 0, f"Failed to list Swarm nodes: {stderr}"
        assert "Leader" in stdout, "No leader node found in Swarm"


class TestDockerContainers:
    """Test expected Docker containers are running."""

    def test_pgadmin_container_running(self, run_shell, in_vagrant):
        """Test that pgAdmin container is running."""
        if not in_vagrant:
            pytest.skip("Test requires running inside Vagrant VM")

        returncode, stdout, stderr = run_shell(
            "docker ps --filter 'name=pgadmin' --format '{{.Status}}'"
        )
        # pgAdmin may not be running in minimal mode
        if returncode != 0 or not stdout.strip():
            pytest.skip("pgAdmin container not present (may be minimal mode)")
        assert "Up" in stdout, f"pgAdmin container not running: {stdout}"

    def test_list_running_containers(self, run_shell, in_vagrant):
        """Test that we can list running containers."""
        if not in_vagrant:
            pytest.skip("Test requires running inside Vagrant VM")

        returncode, stdout, stderr = run_shell("docker ps --format '{{.Names}}'")
        assert returncode == 0, f"Failed to list containers: {stderr}"


class TestDockerNetwork:
    """Test Docker network configuration."""

    def test_docker_networks_exist(self, run_shell, in_vagrant):
        """Test that Docker networks are created."""
        if not in_vagrant:
            pytest.skip("Test requires running inside Vagrant VM")

        returncode, stdout, stderr = run_shell("docker network ls")
        assert returncode == 0, f"Failed to list networks: {stderr}"
        # At minimum, bridge, host, and none should exist
        assert "bridge" in stdout


class TestDockerImages:
    """Test Docker images (may be skipped in minimal mode)."""

    def test_docker_images_list(self, run_shell, in_vagrant):
        """Test that we can list Docker images."""
        if not in_vagrant:
            pytest.skip("Test requires running inside Vagrant VM")

        returncode, stdout, stderr = run_shell("docker images --format '{{.Repository}}'")
        assert returncode == 0, f"Failed to list images: {stderr}"

    def test_pgadmin_image_exists(self, run_shell, in_vagrant):
        """Test that pgAdmin image is pulled."""
        if not in_vagrant:
            pytest.skip("Test requires running inside Vagrant VM")

        returncode, stdout, stderr = run_shell(
            "docker images --format '{{.Repository}}' | grep -i pgadmin"
        )
        # Skip if in minimal mode
        if returncode != 0:
            pytest.skip("pgAdmin image not present (may be minimal mode)")
        assert "pgadmin" in stdout.lower()
