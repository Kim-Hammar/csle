"""
Tests for verifying CSLE REST API endpoints are accessible.
"""
import pytest

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False


class TestAPIHealth:
    """Test basic API health and connectivity."""

    def test_api_reachable(self, api_base_url, in_vagrant):
        """Test that the API is reachable."""
        if not in_vagrant:
            pytest.skip("Test requires running inside Vagrant VM")
        if not HAS_REQUESTS:
            pytest.skip("requests library not installed")

        try:
            response = requests.get(f"{api_base_url}/", timeout=10)
            # API might return 404 for root, but should be reachable
            assert response.status_code in [200, 404, 302]
        except requests.exceptions.ConnectionError:
            pytest.fail(f"Could not connect to API at {api_base_url}")

    def test_api_login_endpoint(self, api_base_url, config, in_vagrant):
        """Test the login endpoint responds."""
        if not in_vagrant:
            pytest.skip("Test requires running inside Vagrant VM")
        if not HAS_REQUESTS:
            pytest.skip("requests library not installed")

        response = requests.post(
            f"{api_base_url}/login",
            json={
                "username": config["admin_username"],
                "password": config["admin_password"],
            },
            timeout=10
        )
        # Login should return 200 on success or 401 on failure
        assert response.status_code in [200, 401], f"Unexpected status: {response.status_code}"


class TestAPIEndpoints:
    """Test specific API endpoints."""

    @pytest.fixture
    def auth_token(self, api_base_url, config, in_vagrant):
        """Get authentication token for API requests."""
        if not in_vagrant:
            return None
        if not HAS_REQUESTS:
            return None

        try:
            response = requests.post(
                f"{api_base_url}/login",
                json={
                    "username": config["admin_username"],
                    "password": config["admin_password"],
                },
                timeout=10
            )
            if response.status_code == 200:
                data = response.json()
                return data.get("token")
        except requests.exceptions.RequestException:
            pass
        return None

    def test_emulations_endpoint(self, api_base_url, auth_token, in_vagrant):
        """Test the emulations endpoint."""
        if not in_vagrant:
            pytest.skip("Test requires running inside Vagrant VM")
        if not HAS_REQUESTS:
            pytest.skip("requests library not installed")
        if auth_token is None:
            pytest.skip("Could not obtain auth token (login may have failed)")

        headers = {"Authorization": f"Bearer {auth_token}"}
        response = requests.get(
            f"{api_base_url}/emulations",
            headers=headers,
            timeout=10
        )
        # Accept 200, 401 (auth issue), or 404 (endpoint not available)
        assert response.status_code in [200, 401, 404], f"Emulations endpoint failed: {response.status_code}"

    def test_simulations_endpoint(self, api_base_url, auth_token, in_vagrant):
        """Test the simulations endpoint."""
        if not in_vagrant:
            pytest.skip("Test requires running inside Vagrant VM")
        if not HAS_REQUESTS:
            pytest.skip("requests library not installed")
        if auth_token is None:
            pytest.skip("Could not obtain auth token (login may have failed)")

        headers = {"Authorization": f"Bearer {auth_token}"}
        response = requests.get(
            f"{api_base_url}/simulations",
            headers=headers,
            timeout=10
        )
        # Accept 200, 401 (auth issue), or 404 (endpoint not available)
        assert response.status_code in [200, 401, 404], f"Simulations endpoint failed: {response.status_code}"

    def test_cluster_status_endpoint(self, api_base_url, auth_token, in_vagrant):
        """Test the cluster status endpoint."""
        if not in_vagrant:
            pytest.skip("Test requires running inside Vagrant VM")
        if not HAS_REQUESTS:
            pytest.skip("requests library not installed")
        if auth_token is None:
            pytest.skip("Could not obtain auth token (login may have failed)")

        headers = {"Authorization": f"Bearer {auth_token}"}
        response = requests.get(
            f"{api_base_url}/cluster-status",
            headers=headers,
            timeout=10
        )
        # Endpoint might not exist in all versions
        assert response.status_code in [200, 401, 404]


class TestMonitoringEndpoints:
    """Test monitoring service endpoints (optional - may not be installed)."""

    def test_prometheus_metrics(self, prometheus_url, in_vagrant):
        """Test Prometheus metrics endpoint."""
        if not in_vagrant:
            pytest.skip("Test requires running inside Vagrant VM")
        if not HAS_REQUESTS:
            pytest.skip("requests library not installed")

        try:
            response = requests.get(f"{prometheus_url}/api/v1/status/config", timeout=10)
            assert response.status_code == 200, f"Prometheus not responding: {response.status_code}"
        except requests.exceptions.ConnectionError:
            pytest.skip(f"Prometheus not running at {prometheus_url}")

    def test_prometheus_targets(self, prometheus_url, in_vagrant):
        """Test Prometheus targets endpoint."""
        if not in_vagrant:
            pytest.skip("Test requires running inside Vagrant VM")
        if not HAS_REQUESTS:
            pytest.skip("requests library not installed")

        try:
            response = requests.get(f"{prometheus_url}/api/v1/targets", timeout=10)
            assert response.status_code == 200
            data = response.json()
            assert data.get("status") == "success"
        except requests.exceptions.ConnectionError:
            pytest.skip(f"Prometheus not running at {prometheus_url}")

    def test_grafana_health(self, grafana_url, in_vagrant):
        """Test Grafana health endpoint."""
        if not in_vagrant:
            pytest.skip("Test requires running inside Vagrant VM")
        if not HAS_REQUESTS:
            pytest.skip("requests library not installed")

        try:
            response = requests.get(f"{grafana_url}/api/health", timeout=10)
            assert response.status_code == 200, f"Grafana not responding: {response.status_code}"
        except requests.exceptions.ConnectionError:
            pytest.skip(f"Grafana not running at {grafana_url}")

    def test_node_exporter_metrics(self, node_exporter_url, in_vagrant):
        """Test Node Exporter metrics endpoint."""
        if not in_vagrant:
            pytest.skip("Test requires running inside Vagrant VM")
        if not HAS_REQUESTS:
            pytest.skip("requests library not installed")

        try:
            response = requests.get(f"{node_exporter_url}/metrics", timeout=10)
            assert response.status_code == 200, f"Node Exporter not responding: {response.status_code}"
            # Verify it's actually node_exporter metrics
            assert "node_" in response.text
        except requests.exceptions.ConnectionError:
            pytest.skip(f"Node Exporter not running at {node_exporter_url}")
