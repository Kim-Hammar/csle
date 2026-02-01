"""
Tests for verifying CSLE Python libraries are installed correctly.
"""
import pytest


# CSLE Python packages that should be installed
CSLE_PACKAGES = [
    "csle-base",
    "csle-common",
    "csle-collector",
    "csle-ryu",
    "csle-attacker",
    "csle-defender",
    "csle-agents",
    "csle-system-identification",
    "csle-rest-api",
    "csle-cli",
    "csle-cluster",
    "gym-csle-stopping-game",
    "gym-csle-apt-game",
    "gym-csle-intrusion-response-game",
    "gym-csle-cyborg",
]


class TestCondaEnvironment:
    """Test Conda environment setup."""

    def test_conda_installed(self, run_shell, in_vagrant):
        """Test that Conda is installed."""
        if not in_vagrant:
            pytest.skip("Test requires running inside Vagrant VM")

        returncode, stdout, stderr = run_shell(
            "source ~/anaconda3/etc/profile.d/conda.sh && conda --version"
        )
        assert returncode == 0, f"Conda not installed: {stderr}"
        assert "conda" in stdout.lower()

    def test_base_environment_exists(self, run_shell, in_vagrant):
        """Test that base Conda environment exists."""
        if not in_vagrant:
            pytest.skip("Test requires running inside Vagrant VM")

        returncode, stdout, stderr = run_shell(
            "source ~/anaconda3/etc/profile.d/conda.sh && conda env list"
        )
        assert returncode == 0, f"Failed to list Conda environments: {stderr}"
        assert "base" in stdout

    def test_python_version(self, run_shell, in_vagrant):
        """Test Python version in Conda environment."""
        if not in_vagrant:
            pytest.skip("Test requires running inside Vagrant VM")

        returncode, stdout, stderr = run_shell(
            "source ~/anaconda3/etc/profile.d/conda.sh && "
            "conda activate base && python --version"
        )
        assert returncode == 0, f"Failed to get Python version: {stderr}"
        assert "Python 3" in stdout


class TestCSLEPackages:
    """Test CSLE Python packages are installed."""

    @pytest.mark.parametrize("package", CSLE_PACKAGES)
    def test_package_installed(self, run_shell, in_vagrant, package):
        """Test that CSLE package is installed."""
        if not in_vagrant:
            pytest.skip("Test requires running inside Vagrant VM")

        returncode, stdout, stderr = run_shell(
            f"source ~/anaconda3/etc/profile.d/conda.sh && "
            f"conda activate base && pip show {package}"
        )
        assert returncode == 0, f"Package {package} not installed: {stderr}"
        assert package.replace("-", "_") in stdout.lower() or package in stdout.lower()

    def test_csle_cli_available(self, run_shell, in_vagrant):
        """Test that CSLE CLI is available."""
        if not in_vagrant:
            pytest.skip("Test requires running inside Vagrant VM")

        returncode, stdout, stderr = run_shell(
            "source ~/anaconda3/etc/profile.d/conda.sh && "
            "conda activate base && csle --help"
        )
        assert returncode == 0, f"CSLE CLI not available: {stderr}"
        assert "csle" in stdout.lower() or "usage" in stdout.lower()


class TestCSLEImports:
    """Test that CSLE packages can be imported."""

    def test_import_csle_common(self, run_shell, in_vagrant):
        """Test that csle_common can be imported."""
        if not in_vagrant:
            pytest.skip("Test requires running inside Vagrant VM")

        returncode, stdout, stderr = run_shell(
            "source ~/anaconda3/etc/profile.d/conda.sh && "
            "conda activate base && "
            "python -c 'import csle_common; print(csle_common.__version__)'"
        )
        assert returncode == 0, f"Failed to import csle_common: {stderr}"

    def test_import_csle_agents(self, run_shell, in_vagrant):
        """Test that csle_agents can be imported."""
        if not in_vagrant:
            pytest.skip("Test requires running inside Vagrant VM")

        returncode, stdout, stderr = run_shell(
            "source ~/anaconda3/etc/profile.d/conda.sh && "
            "conda activate base && "
            "python -c 'import csle_agents; print(csle_agents.__version__)'"
        )
        assert returncode == 0, f"Failed to import csle_agents: {stderr}"

    def test_import_gymnasium(self, run_shell, in_vagrant):
        """Test that gymnasium can be imported."""
        if not in_vagrant:
            pytest.skip("Test requires running inside Vagrant VM")

        returncode, stdout, stderr = run_shell(
            "source ~/anaconda3/etc/profile.d/conda.sh && "
            "conda activate base && "
            "python -c 'import gymnasium; print(gymnasium.__version__)'"
        )
        assert returncode == 0, f"Failed to import gymnasium: {stderr}"


class TestDependencies:
    """Test key dependencies are installed."""

    @pytest.mark.parametrize("package", [
        "torch",
        "numpy",
        "pandas",
        "requests",
        "flask",
        "grpcio",
        "psycopg2-binary",
        "docker",
    ])
    def test_dependency_installed(self, run_shell, in_vagrant, package):
        """Test that key dependencies are installed."""
        if not in_vagrant:
            pytest.skip("Test requires running inside Vagrant VM")

        returncode, stdout, stderr = run_shell(
            f"source ~/anaconda3/etc/profile.d/conda.sh && "
            f"conda activate base && pip show {package}"
        )
        # Some packages might have different names
        if returncode != 0:
            # Try import as fallback
            import_name = package.replace("-", "_").split("[")[0]
            returncode, stdout, stderr = run_shell(
                f"source ~/anaconda3/etc/profile.d/conda.sh && "
                f"conda activate base && python -c 'import {import_name}'"
            )
        assert returncode == 0, f"Dependency {package} not available"
