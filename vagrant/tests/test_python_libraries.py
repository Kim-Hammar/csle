"""
Tests for verifying CSLE Python libraries are installed correctly.
"""
from typing import Callable, List, Tuple

import pytest


# CSLE Python packages that should be installed
CSLE_PACKAGES: List[str] = [
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

    def test_conda_installed(self, run_shell: Callable[..., Tuple[int, str, str]],
                             in_vagrant: bool) -> None:
        """
        Test that Conda is installed.

        :param run_shell: fixture to run shell commands
        :param in_vagrant: whether tests are running inside Vagrant VM
        :return: None
        """
        if not in_vagrant:
            pytest.skip("Test requires running inside Vagrant VM")

        returncode, stdout, stderr = run_shell(
            "source /home/vagrant/anaconda3/etc/profile.d/conda.sh && conda --version"
        )
        assert returncode == 0, f"Conda not installed: {stderr}"
        assert "conda" in stdout.lower()

    def test_base_environment_exists(self, run_shell: Callable[..., Tuple[int, str, str]],
                                     in_vagrant: bool) -> None:
        """
        Test that base Conda environment exists.

        :param run_shell: fixture to run shell commands
        :param in_vagrant: whether tests are running inside Vagrant VM
        :return: None
        """
        if not in_vagrant:
            pytest.skip("Test requires running inside Vagrant VM")

        returncode, stdout, stderr = run_shell(
            "source /home/vagrant/anaconda3/etc/profile.d/conda.sh && conda env list"
        )
        assert returncode == 0, f"Failed to list Conda environments: {stderr}"
        assert "base" in stdout

    def test_python_version(self, run_shell: Callable[..., Tuple[int, str, str]],
                            in_vagrant: bool) -> None:
        """
        Test Python version in Conda environment.

        :param run_shell: fixture to run shell commands
        :param in_vagrant: whether tests are running inside Vagrant VM
        :return: None
        """
        if not in_vagrant:
            pytest.skip("Test requires running inside Vagrant VM")

        returncode, stdout, stderr = run_shell(
            "source /home/vagrant/anaconda3/etc/profile.d/conda.sh && "
            "conda activate base && python --version"
        )
        assert returncode == 0, f"Failed to get Python version: {stderr}"
        assert "Python 3" in stdout


class TestCSLEPackages:
    """Test CSLE Python packages are installed."""

    @pytest.mark.parametrize("package", CSLE_PACKAGES)
    def test_package_installed(self, run_shell: Callable[..., Tuple[int, str, str]],
                               in_vagrant: bool, package: str) -> None:
        """
        Test that CSLE package is installed.

        :param run_shell: fixture to run shell commands
        :param in_vagrant: whether tests are running inside Vagrant VM
        :param package: the package name to check
        :return: None
        """
        if not in_vagrant:
            pytest.skip("Test requires running inside Vagrant VM")

        returncode, stdout, stderr = run_shell(
            f"source /home/vagrant/anaconda3/etc/profile.d/conda.sh && "
            f"conda activate base && pip show {package}"
        )
        assert returncode == 0, f"Package {package} not installed: {stderr}"
        assert package.replace("-", "_") in stdout.lower() or package in stdout.lower()

    def test_csle_cli_available(self, run_shell: Callable[..., Tuple[int, str, str]],
                                in_vagrant: bool) -> None:
        """
        Test that CSLE CLI is available.

        :param run_shell: fixture to run shell commands
        :param in_vagrant: whether tests are running inside Vagrant VM
        :return: None
        """
        if not in_vagrant:
            pytest.skip("Test requires running inside Vagrant VM")

        returncode, stdout, stderr = run_shell(
            "source /home/vagrant/anaconda3/etc/profile.d/conda.sh && "
            "conda activate base && csle --help"
        )
        assert returncode == 0, f"CSLE CLI not available: {stderr}"
        assert "csle" in stdout.lower() or "usage" in stdout.lower()


class TestCSLEImports:
    """Test that CSLE packages can be imported."""

    def test_import_csle_common(self, run_shell: Callable[..., Tuple[int, str, str]],
                                in_vagrant: bool) -> None:
        """
        Test that csle_common can be imported.

        :param run_shell: fixture to run shell commands
        :param in_vagrant: whether tests are running inside Vagrant VM
        :return: None
        """
        if not in_vagrant:
            pytest.skip("Test requires running inside Vagrant VM")

        returncode, stdout, stderr = run_shell(
            "source /home/vagrant/anaconda3/etc/profile.d/conda.sh && "
            "conda activate base && "
            "python -c 'import csle_common; print(csle_common.__version__)'"
        )
        assert returncode == 0, f"Failed to import csle_common: {stderr}"

    def test_import_csle_agents(self, run_shell: Callable[..., Tuple[int, str, str]],
                                in_vagrant: bool) -> None:
        """
        Test that csle_agents can be imported.

        :param run_shell: fixture to run shell commands
        :param in_vagrant: whether tests are running inside Vagrant VM
        :return: None
        """
        if not in_vagrant:
            pytest.skip("Test requires running inside Vagrant VM")

        returncode, stdout, stderr = run_shell(
            "source /home/vagrant/anaconda3/etc/profile.d/conda.sh && "
            "conda activate base && "
            "python -c 'import csle_agents; print(csle_agents.__version__)'"
        )
        assert returncode == 0, f"Failed to import csle_agents: {stderr}"

    def test_import_gymnasium(self, run_shell: Callable[..., Tuple[int, str, str]],
                              in_vagrant: bool) -> None:
        """
        Test that gymnasium can be imported.

        :param run_shell: fixture to run shell commands
        :param in_vagrant: whether tests are running inside Vagrant VM
        :return: None
        """
        if not in_vagrant:
            pytest.skip("Test requires running inside Vagrant VM")

        returncode, stdout, stderr = run_shell(
            "source /home/vagrant/anaconda3/etc/profile.d/conda.sh && "
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
    def test_dependency_installed(self, run_shell: Callable[..., Tuple[int, str, str]],
                                  in_vagrant: bool, package: str) -> None:
        """
        Test that key dependencies are installed.

        :param run_shell: fixture to run shell commands
        :param in_vagrant: whether tests are running inside Vagrant VM
        :param package: the package name to check
        :return: None
        """
        if not in_vagrant:
            pytest.skip("Test requires running inside Vagrant VM")

        returncode, stdout, stderr = run_shell(
            f"source /home/vagrant/anaconda3/etc/profile.d/conda.sh && "
            f"conda activate base && pip show {package}"
        )
        # Some packages might have different names
        if returncode != 0:
            # Try import as fallback
            import_name = package.replace("-", "_").split("[")[0]
            returncode, stdout, stderr = run_shell(
                f"source /home/vagrant/anaconda3/etc/profile.d/conda.sh && "
                f"conda activate base && python -c 'import {import_name}'"
            )
        assert returncode == 0, f"Dependency {package} not available"
