"""
Tests for verifying PostgreSQL database setup and connectivity.
"""
import pytest

# Try to import psycopg2, mark tests as skipped if not available
try:
    import psycopg2
    HAS_PSYCOPG2 = True
except ImportError:
    HAS_PSYCOPG2 = False


# Expected tables from CSLE schema
EXPECTED_TABLES = [
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
def db_connection(db_connection_params, in_vagrant):
    """Create a database connection for tests."""
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

    def test_database_connection(self, db_connection):
        """Test that we can connect to the CSLE database."""
        assert db_connection is not None
        assert not db_connection.closed

    def test_database_version(self, db_connection):
        """Test PostgreSQL version is 15.x."""
        cursor = db_connection.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]
        cursor.close()
        assert "PostgreSQL 15" in version, f"Expected PostgreSQL 15, got: {version}"

    def test_citus_extension(self, db_connection):
        """Test that Citus extension is installed."""
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

    def test_csle_user_exists(self, db_connection):
        """Test that csle user exists in the database."""
        cursor = db_connection.cursor()
        cursor.execute(
            "SELECT usename FROM pg_user WHERE usename = 'csle';"
        )
        result = cursor.fetchone()
        cursor.close()
        assert result is not None, "User 'csle' not found"

    @pytest.mark.parametrize("table", EXPECTED_TABLES)
    def test_table_exists(self, db_connection, table):
        """Test that expected tables exist in the database."""
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

    def test_management_users_table_has_admin(self, db_connection):
        """Test that admin user is created in management_users table."""
        cursor = db_connection.cursor()
        cursor.execute(
            "SELECT username FROM management_users WHERE username = 'admin';"
        )
        result = cursor.fetchone()
        cursor.close()
        assert result is not None, "Admin user not found in management_users"

    def test_config_table_has_entry(self, db_connection):
        """Test that config table has at least one entry."""
        cursor = db_connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM config;")
        count = cursor.fetchone()[0]
        cursor.close()
        assert count >= 1, "Config table is empty"


class TestDatabasePermissions:
    """Test database permissions are correctly set."""

    def test_csle_user_can_select(self, db_connection):
        """Test that csle user has SELECT permissions."""
        cursor = db_connection.cursor()
        try:
            cursor.execute("SELECT * FROM emulations LIMIT 1;")
            cursor.fetchall()  # Consume results
        except psycopg2.Error as e:
            pytest.fail(f"SELECT permission denied: {e}")
        finally:
            cursor.close()

    def test_csle_user_can_insert(self, db_connection):
        """Test that csle user has INSERT permissions (via transaction rollback)."""
        cursor = db_connection.cursor()
        try:
            # Start a transaction and roll it back to avoid side effects
            cursor.execute(
                """
                INSERT INTO simulations (name, config)
                VALUES ('test_simulation_temp', '{}');
                """
            )
            db_connection.rollback()  # Roll back to avoid persisting test data
        except psycopg2.Error as e:
            db_connection.rollback()
            pytest.fail(f"INSERT permission denied: {e}")
        finally:
            cursor.close()
