#!/usr/bin/env python3
"""
Standalone verification script for CSLE installation.
Can be run outside of pytest for quick checks.

Usage:
    python3 verify_installation.py [--verbose]
"""
import argparse
import subprocess
import sys
import os

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

try:
    import psycopg2
    HAS_PSYCOPG2 = True
except ImportError:
    HAS_PSYCOPG2 = False


# Configuration
CONFIG = {
    "leader_ip": os.environ.get("CSLE_LEADER_IP", "192.168.56.10"),
    "postgres_user": "csle",
    "postgres_password": "csle192105Test",
    "postgres_db": "csle",
    "postgres_port": 5432,
    "flask_port": 7777,
    "grafana_port": 3000,
    "prometheus_port": 9090,
    "node_exporter_port": 9100,
}


class Colors:
    """ANSI color codes for terminal output."""
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    RESET = "\033[0m"
    BOLD = "\033[1m"


def print_header(text):
    """Print a section header."""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}")


def print_check(name, passed, details=""):
    """Print a check result."""
    status = f"{Colors.GREEN}PASS{Colors.RESET}" if passed else f"{Colors.RED}FAIL{Colors.RESET}"
    print(f"  [{status}] {name}")
    if details and not passed:
        print(f"         {Colors.YELLOW}{details}{Colors.RESET}")


def run_command(cmd):
    """Run a shell command and return success status and output."""
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, timeout=30
        )
        return result.returncode == 0, result.stdout.strip()
    except subprocess.TimeoutExpired:
        return False, "Command timed out"
    except Exception as e:
        return False, str(e)


def check_services():
    """Check system services."""
    print_header("System Services")
    results = []

    services = ["postgresql", "nginx", "docker"]
    for service in services:
        passed, output = run_command(f"systemctl is-active {service}")
        print_check(f"{service} service", passed and output == "active", output)
        results.append(passed)

    return all(results)


def check_ports():
    """Check if expected ports are listening."""
    print_header("Port Bindings")
    results = []

    ports = [
        (CONFIG["flask_port"], "Flask API"),
        (CONFIG["prometheus_port"], "Prometheus"),
        (CONFIG["grafana_port"], "Grafana"),
        (CONFIG["node_exporter_port"], "Node Exporter"),
        (CONFIG["postgres_port"], "PostgreSQL"),
    ]

    for port, name in ports:
        passed, _ = run_command(f"ss -tlnp | grep :{port}")
        print_check(f"{name} (port {port})", passed)
        results.append(passed)

    return all(results)


def check_database():
    """Check database connectivity and schema."""
    print_header("Database")
    results = []

    if not HAS_PSYCOPG2:
        print(f"  {Colors.YELLOW}[SKIP] psycopg2 not installed{Colors.RESET}")
        return True

    try:
        conn = psycopg2.connect(
            host=CONFIG["leader_ip"],
            port=CONFIG["postgres_port"],
            user=CONFIG["postgres_user"],
            password=CONFIG["postgres_password"],
            dbname=CONFIG["postgres_db"],
        )
        print_check("Database connection", True)
        results.append(True)

        cursor = conn.cursor()

        # Check Citus extension
        cursor.execute("SELECT extname FROM pg_extension WHERE extname = 'citus';")
        citus = cursor.fetchone()
        passed = citus is not None
        print_check("Citus extension", passed)
        results.append(passed)

        # Check tables
        cursor.execute(
            "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public';"
        )
        table_count = cursor.fetchone()[0]
        passed = table_count >= 20  # Expect at least 20 tables
        print_check(f"Database tables ({table_count} found)", passed)
        results.append(passed)

        # Check admin user
        cursor.execute("SELECT username FROM management_users WHERE username = 'admin';")
        admin = cursor.fetchone()
        passed = admin is not None
        print_check("Admin user exists", passed)
        results.append(passed)

        cursor.close()
        conn.close()
    except psycopg2.Error as e:
        print_check("Database connection", False, str(e))
        results.append(False)

    return all(results)


def check_docker():
    """Check Docker and Swarm setup."""
    print_header("Docker")
    results = []

    # Docker daemon
    passed, output = run_command("docker info --format '{{.ServerVersion}}'")
    print_check(f"Docker daemon (version {output})", passed)
    results.append(passed)

    # Swarm status
    passed, output = run_command("docker info --format '{{.Swarm.LocalNodeState}}'")
    is_active = passed and output == "active"
    print_check("Docker Swarm", is_active, output if not is_active else "")
    results.append(is_active)

    # Manager status
    passed, output = run_command("docker info --format '{{.Swarm.ControlAvailable}}'")
    is_manager = passed and output == "true"
    print_check("Swarm manager", is_manager)
    results.append(is_manager)

    return all(results)


def check_python():
    """Check Python environment and CSLE packages."""
    print_header("Python Environment")
    results = []

    # Conda
    passed, output = run_command(
        "source ~/anaconda3/etc/profile.d/conda.sh && conda --version"
    )
    print_check("Conda installation", passed, output if not passed else "")
    results.append(passed)

    # Python version
    passed, output = run_command(
        "source ~/anaconda3/etc/profile.d/conda.sh && "
        "conda activate base && python --version"
    )
    print_check(f"Python ({output})", passed and "Python 3" in output)
    results.append(passed)

    # CSLE packages
    packages = ["csle-common", "csle-agents", "csle-cli"]
    for pkg in packages:
        passed, _ = run_command(
            f"source ~/anaconda3/etc/profile.d/conda.sh && "
            f"conda activate base && pip show {pkg}"
        )
        print_check(f"Package: {pkg}", passed)
        results.append(passed)

    # CSLE CLI
    passed, _ = run_command(
        "source ~/anaconda3/etc/profile.d/conda.sh && "
        "conda activate base && csle --help"
    )
    print_check("CSLE CLI available", passed)
    results.append(passed)

    return all(results)


def check_endpoints():
    """Check API and monitoring endpoints."""
    print_header("Endpoints")
    results = []

    if not HAS_REQUESTS:
        print(f"  {Colors.YELLOW}[SKIP] requests library not installed{Colors.RESET}")
        return True

    endpoints = [
        (f"http://{CONFIG['leader_ip']}:{CONFIG['flask_port']}/", "Flask API"),
        (f"http://{CONFIG['leader_ip']}:{CONFIG['prometheus_port']}/api/v1/status/config", "Prometheus"),
        (f"http://{CONFIG['leader_ip']}:{CONFIG['grafana_port']}/api/health", "Grafana"),
        (f"http://{CONFIG['leader_ip']}:{CONFIG['node_exporter_port']}/metrics", "Node Exporter"),
    ]

    for url, name in endpoints:
        try:
            response = requests.get(url, timeout=10)
            passed = response.status_code in [200, 302, 404]
            print_check(f"{name} endpoint", passed, f"Status: {response.status_code}")
            results.append(passed)
        except requests.exceptions.ConnectionError:
            print_check(f"{name} endpoint", False, "Connection refused")
            results.append(False)
        except requests.exceptions.Timeout:
            print_check(f"{name} endpoint", False, "Timeout")
            results.append(False)

    return all(results)


def main():
    """Run all verification checks."""
    parser = argparse.ArgumentParser(description="Verify CSLE installation")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    parser.parse_args()  # Parse args but verbose mode is reserved for future use

    print(f"\n{Colors.BOLD}CSLE Installation Verification{Colors.RESET}")
    print(f"Leader IP: {CONFIG['leader_ip']}")

    results = {
        "System Services": check_services(),
        "Port Bindings": check_ports(),
        "Database": check_database(),
        "Docker": check_docker(),
        "Python Environment": check_python(),
        "Endpoints": check_endpoints(),
    }

    # Summary
    print_header("Summary")
    all_passed = True
    for category, passed in results.items():
        status = f"{Colors.GREEN}PASS{Colors.RESET}" if passed else f"{Colors.RED}FAIL{Colors.RESET}"
        print(f"  [{status}] {category}")
        if not passed:
            all_passed = False

    print()
    if all_passed:
        print(f"{Colors.GREEN}{Colors.BOLD}All checks passed!{Colors.RESET}")
        return 0
    else:
        print(f"{Colors.RED}{Colors.BOLD}Some checks failed.{Colors.RESET}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
