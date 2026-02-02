"""
Tests for verifying PostgreSQL database setup and connectivity.
"""
from typing import Any, Dict, Generator, List

import pytest

# Try to import psycopg2, mark tests as skipped if not available
try:
    import psycopg2
    HAS_PSYCOPG2 = True
except ImportError:
    HAS_PSYCOPG2 = False


# Expected tables from CSLE schema
EXPECTED_TABLES: List[str] = [
    "emulations",
    "emulation_traces",
    "emulation_statistics",
    "simulation_traces",
    "emulation_simulation_traces",
    "emulation_images",
    "simulations",
    "experiment_executions",
    "simulation_images",
    "multi_threshold_stopping_policies",
    "training_jobs",
    "system_identification_jobs",
    "ppo_policies",
    "system_models",
    "data_collection_jobs",
    "gaussian_mixture_system_models",
    "tabular_policies",
    "alpha_vec_policies",
    "dqn_policies",
    "fnn_w_softmax_policies",
    "vector_policies",
    "emulation_executions",
    "empirical_system_models",
    "gp_system_models",
    "management_users",
    "session_tokens",
    "traces_datasets",
    "statistics_datasets",
    "config",
    "linear_threshold_stopping_policies",
    "mcmc_system_models",
]


@pytest.fixture(scope="module")
def db_connection(db_connection_params: Dict[str, Any], in_vagrant: bool) -> Generator[Any, None, None]:
    """
    Create a database connection for tests.

    :param db_connection_params: dictionary with database connection parameters
    :param in_vagrant: whether tests are running inside Vagrant VM
    :return: database connection object
    """
    if not in_vagrant:
        pytest.skip("Test requires running inside Vagrant VM")
    if not HAS_PSYCOPG2:
        pytest.skip("psycopg2 not installed")

    try:
        conn = psycopg2.connect(**db_connection_params)
        yield conn
        conn.close()
    except psycopg2.OperationalError as e:
        pytest.fail(f"Failed to connect to database: {e}")


class TestDatabaseConnectivity:
    """Test database connectivity and configuration."""

    def test_database_connection(self, db_connection: Any) -> None:
        """
        Test that we can connect to the CSLE database.

        :param db_connection: the database connection fixture
        :return: None
        """
        assert db_connection is not None
        assert not db_connection.closed

    def test_database_version(self, db_connection: Any) -> None:
        """
        Test PostgreSQL version is 15.x.

        :param db_connection: the database connection fixture
        :return: None
        """
        cursor = db_connection.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]
        cursor.close()
        assert "PostgreSQL 15" in version, f"Expected PostgreSQL 15, got: {version}"

    def test_citus_extension(self, db_connection: Any) -> None:
        """
        Test that Citus extension is installed.

        :param db_connection: the database connection fixture
        :return: None
        """
        cursor = db_connection.cursor()
        cursor.execute(
            "SELECT extname FROM pg_extension WHERE extname = 'citus';"
        )
        result = cursor.fetchone()
        cursor.close()
        assert result is not None, "Citus extension not found"
        assert result[0] == "citus"


class TestDatabaseSchema:
    """Test that database schema is correctly set up."""

    def test_csle_user_exists(self, db_connection: Any) -> None:
        """
        Test that csle user exists in the database.

        :param db_connection: the database connection fixture
        :return: None
        """
        cursor = db_connection.cursor()
        cursor.execute(
            "SELECT usename FROM pg_user WHERE usename = 'csle';"
        )
        result = cursor.fetchone()
        cursor.close()
        assert result is not None, "User 'csle' not found"

    @pytest.mark.parametrize("table", EXPECTED_TABLES)
    def test_table_exists(self, db_connection: Any, table: str) -> None:
        """
        Test that expected tables exist in the database.

        :param db_connection: the database connection fixture
        :param table: the table name to check
        :return: None
        """
        cursor = db_connection.cursor()
        cursor.execute(
            """
            SELECT table_name FROM information_schema.tables
            WHERE table_schema = 'public' AND table_name = %s;
            """,
            (table,)
        )
        result = cursor.fetchone()
        cursor.close()
        assert result is not None, f"Table '{table}' not found"

    def test_management_users_table_has_admin(self, db_connection: Any) -> None:
        """
        Test that admin user is created in management_users table.

        :param db_connection: the database connection fixture
        :return: None
        """
        cursor = db_connection.cursor()
        cursor.execute(
            "SELECT username FROM management_users WHERE username = 'admin';"
        )
        result = cursor.fetchone()
        cursor.close()
        assert result is not None, "Admin user not found in management_users"

    def test_config_table_has_entry(self, db_connection: Any) -> None:
        """
        Test that config table has at least one entry.

        :param db_connection: the database connection fixture
        :return: None
        """
        cursor = db_connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM config;")
        count = cursor.fetchone()[0]
        cursor.close()
        assert count >= 1, "Config table is empty"


class TestDatabasePermissions:
    """Test database permissions are correctly set."""

    def test_csle_user_can_select(self, db_connection: Any) -> None:
        """
        Test that csle user has SELECT permissions.

        :param db_connection: the database connection fixture
        :return: None
        """
        cursor = db_connection.cursor()
        try:
            cursor.execute("SELECT * FROM emulations LIMIT 1;")
            cursor.fetchall()  # Consume results
        except psycopg2.Error as e:
            pytest.fail(f"SELECT permission denied: {e}")
        finally:
            cursor.close()

    def test_csle_user_can_insert(self, db_connection: Any) -> None:
        """
        Test that csle user has INSERT permissions (via transaction rollback).

        :param db_connection: the database connection fixture
        :return: None
        """
        cursor = db_connection.cursor()
        try:
            # Start a transaction and roll it back to avoid side effects
            # Use a unique name with timestamp to avoid conflicts
            import time
            test_name = f'test_simulation_temp_{int(time.time())}'
            cursor.execute(
                f"""
                INSERT INTO simulations (name, config)
                VALUES ('{test_name}', '{{}}'::jsonb);
                """
            )
            db_connection.rollback()  # Roll back to avoid persisting test data
        except psycopg2.errors.UniqueViolation:
            # UniqueViolation means we have INSERT permissions, just a constraint issue
            db_connection.rollback()
        except psycopg2.errors.InsufficientPrivilege as e:
            db_connection.rollback()
            pytest.fail(f"INSERT permission denied: {e}")
        except psycopg2.Error as e:
            db_connection.rollback()
            # Only fail if it's actually a permission error
            if "permission denied" in str(e).lower():
                pytest.fail(f"INSERT permission denied: {e}")
        finally:
            cursor.close()
