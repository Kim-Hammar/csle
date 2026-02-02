"""
Pytest configuration for csle-cli tests.

This module provides fixtures and setup for both unit and integration tests.
For unit tests, it mocks the database and cluster connections to allow
testing CLI structure without requiring the full CSLE platform.
"""
import os
import sys
from unittest.mock import MagicMock

import pytest


def create_mock_config() -> MagicMock:
    """
    Create a mock Config object for testing.

    :return: mocked Config object
    """
    mock_config = MagicMock()
    mock_config.localhost = True
    mock_config.management_admin_username_default = "admin"
    mock_config.management_admin_password_default = "test"
    mock_config.management_admin_email_default = "admin@test.com"
    mock_config.management_admin_organization_default = "test"
    mock_config.management_admin_first_name_default = "Admin"
    mock_config.management_admin_last_name_default = "User"
    mock_config.ssh_admin_username = "admin"
    mock_config.ssh_admin_password = "test"
    mock_config.management_guest_username_default = "guest"
    mock_config.management_guest_password_default = "test"
    mock_config.management_guest_email_default = "guest@test.com"
    mock_config.management_guest_organization_default = "test"
    mock_config.management_guest_first_name_default = "Guest"
    mock_config.management_guest_last_name_default = "User"
    mock_config.ssh_agent_username = "agent"
    mock_config.ssh_agent_password = "test"
    mock_config.cluster_config = MagicMock()
    mock_config.cluster_config.cluster_nodes = []
    return mock_config


# Set up environment and mocks BEFORE any csle modules are imported
# This must happen at module load time, not in a fixture
_CSLE_HOME_SET = "CSLE_HOME" in os.environ
if not _CSLE_HOME_SET:
    os.environ["CSLE_HOME"] = "/tmp/csle_unit_test"

# Create mock config
_mock_config = create_mock_config()

# Pre-create mock modules to prevent actual database connections
_mock_metastore_module = MagicMock()
_mock_metastore_module.MetastoreFacade = MagicMock()
_mock_metastore_module.MetastoreFacade.get_config.return_value = _mock_config
_mock_metastore_module.MetastoreFacade.list_emulations.return_value = []
_mock_metastore_module.MetastoreFacade.list_simulations.return_value = []

# Inject mocks into sys.modules before csle_cli.cli is imported
if 'csle_common.metastore.metastore_facade' not in sys.modules:
    sys.modules['csle_common.metastore.metastore_facade'] = _mock_metastore_module


@pytest.fixture(scope="session")
def mock_config() -> MagicMock:
    """
    Provide a mock Config for tests.

    :return: mocked Config
    """
    return _mock_config


@pytest.fixture
def mock_metastore() -> MagicMock:
    """
    Provide a mock MetastoreFacade for tests.

    :return: mocked MetastoreFacade
    """
    return _mock_metastore_module.MetastoreFacade
