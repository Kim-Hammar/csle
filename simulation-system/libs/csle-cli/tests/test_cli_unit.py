"""
Unit tests for csle-cli.

These tests use mocked dependencies and can run independently without
requiring the full CSLE platform (database, Docker, cluster manager, etc.).
"""
import click
from click.testing import CliRunner


class TestCliCommandStructure:
    """
    Test suite for CLI command structure and argument parsing.

    These tests verify that CLI commands are properly defined with correct
    arguments, options, and help text without invoking actual functionality.
    """

    def test_ls_command_exists(self) -> None:
        """
        Tests that the ls command is properly defined.

        :return: None
        """
        from csle_cli.cli import ls
        assert ls is not None
        assert isinstance(ls, click.Command)
        assert ls.name == "ls"

    def test_ls_command_has_help(self) -> None:
        """
        Tests that the ls command has help text.

        :return: None
        """
        from csle_cli.cli import ls
        assert ls.help is not None
        assert len(ls.help) > 0
        assert "containers" in ls.help
        assert "networks" in ls.help
        assert "emulations" in ls.help

    def test_ls_command_has_options(self) -> None:
        """
        Tests that the ls command has the expected options.

        :return: None
        """
        from csle_cli.cli import ls
        option_names = [param.name for param in ls.params]
        assert "all" in option_names
        assert "running" in option_names
        assert "stopped" in option_names
        assert "ip" in option_names
        assert "name" in option_names
        assert "id" in option_names

    def test_init_command_exists(self) -> None:
        """
        Tests that the init command is properly defined.

        :return: None
        """
        from csle_cli.cli import init
        assert init is not None
        assert isinstance(init, click.Command)
        assert init.name == "init"

    def test_start_command_exists(self) -> None:
        """
        Tests that the start command is properly defined.

        :return: None
        """
        from csle_cli.cli import start
        assert start is not None
        assert isinstance(start, click.Command)
        assert start.name == "start"

    def test_stop_command_exists(self) -> None:
        """
        Tests that the stop command is properly defined.

        :return: None
        """
        from csle_cli.cli import stop
        assert stop is not None
        assert isinstance(stop, click.Command)
        assert stop.name == "stop"

    def test_rm_command_exists(self) -> None:
        """
        Tests that the rm command is properly defined.

        :return: None
        """
        from csle_cli.cli import rm
        assert rm is not None
        assert isinstance(rm, click.Command)
        assert rm.name == "rm"

    def test_clean_command_exists(self) -> None:
        """
        Tests that the clean command is properly defined.

        :return: None
        """
        from csle_cli.cli import clean
        assert clean is not None
        assert isinstance(clean, click.Command)
        assert clean.name == "clean"

    def test_install_command_exists(self) -> None:
        """
        Tests that the install command is properly defined.

        :return: None
        """
        from csle_cli.cli import install
        assert install is not None
        assert isinstance(install, click.Command)
        assert install.name == "install"

    def test_uninstall_command_exists(self) -> None:
        """
        Tests that the uninstall command is properly defined.

        :return: None
        """
        from csle_cli.cli import uninstall
        assert uninstall is not None
        assert isinstance(uninstall, click.Command)
        assert uninstall.name == "uninstall"

    def test_em_command_exists(self) -> None:
        """
        Tests that the em (emulation) command is properly defined.

        :return: None
        """
        from csle_cli.cli import em
        assert em is not None
        assert isinstance(em, click.Command)
        assert em.name == "em"

    def test_attacker_command_exists(self) -> None:
        """
        Tests that the attacker command is properly defined.

        :return: None
        """
        from csle_cli.cli import attacker
        assert attacker is not None
        assert isinstance(attacker, click.Command)
        assert attacker.name == "attacker"

    def test_shell_command_exists(self) -> None:
        """
        Tests that the shell command is properly defined.

        :return: None
        """
        from csle_cli.cli import shell
        assert shell is not None
        assert isinstance(shell, click.Command)
        assert shell.name == "shell"

    def test_commands_group_exists(self) -> None:
        """
        Tests that the main commands group is properly defined.

        :return: None
        """
        from csle_cli.cli import commands
        assert commands is not None
        assert isinstance(commands, click.Group)


class TestLsCommandWithMocks:
    """
    Test suite for the ls command with mocked dependencies.

    These tests use Click's CliRunner to test CLI help and argument parsing
    without invoking actual functionality.
    """

    def test_ls_help_option(self) -> None:
        """
        Tests that ls --help works correctly.

        :return: None
        """
        runner = CliRunner()
        from csle_cli.cli import ls
        result = runner.invoke(ls, ["--help"])
        assert result.exit_code == 0
        assert "containers" in result.output
        assert "networks" in result.output
        assert "emulations" in result.output
        assert "--all" in result.output
        assert "--running" in result.output
        assert "--stopped" in result.output


class TestCliHelpMessages:
    """
    Test suite for CLI help messages.

    These tests verify that all commands have proper help text.
    """

    def test_ls_help_contains_all_entities(self) -> None:
        """
        Tests that ls help contains documentation for all supported entities.

        :return: None
        """
        from csle_cli.cli import ls
        help_text = ls.help
        entities = [
            "containers", "networks", "images", "emulations", "all",
            "environments", "prometheus", "node_exporter", "cadvisor",
            "pgadmin", "statsmanager", "flask", "simulations",
            "emulation_executions", "cluster", "nginx", "postgresql", "docker"
        ]
        for entity in entities:
            assert entity in help_text, f"Entity '{entity}' not found in ls help text"

    def test_init_help_exists(self) -> None:
        """
        Tests that init command has help text.

        :return: None
        """
        from csle_cli.cli import init
        assert init.help is not None
        assert "initializes" in init.help.lower() or "init" in init.help.lower()

    def test_start_help_exists(self) -> None:
        """
        Tests that start command has help text.

        :return: None
        """
        from csle_cli.cli import start
        assert start.help is not None
        assert len(start.help) > 0

    def test_stop_help_exists(self) -> None:
        """
        Tests that stop command has help text.

        :return: None
        """
        from csle_cli.cli import stop
        assert stop.help is not None
        assert len(stop.help) > 0


class TestCliOptionTypes:
    """
    Test suite for CLI option types and defaults.
    """

    def test_ls_all_option_is_flag(self) -> None:
        """
        Tests that the --all option is a boolean flag.

        :return: None
        """
        from csle_cli.cli import ls
        all_param = next((p for p in ls.params if p.name == "all"), None)
        assert all_param is not None
        assert all_param.is_flag is True

    def test_ls_running_option_is_flag(self) -> None:
        """
        Tests that the --running option is a boolean flag.

        :return: None
        """
        from csle_cli.cli import ls
        running_param = next((p for p in ls.params if p.name == "running"), None)
        assert running_param is not None
        assert running_param.is_flag is True

    def test_ls_stopped_option_is_flag(self) -> None:
        """
        Tests that the --stopped option is a boolean flag.

        :return: None
        """
        from csle_cli.cli import ls
        stopped_param = next((p for p in ls.params if p.name == "stopped"), None)
        assert stopped_param is not None
        assert stopped_param.is_flag is True

    def test_ls_ip_option_is_string(self) -> None:
        """
        Tests that the --ip option is a string type.

        :return: None
        """
        from csle_cli.cli import ls
        ip_param = next((p for p in ls.params if p.name == "ip"), None)
        assert ip_param is not None
        assert ip_param.type == click.STRING

    def test_ls_id_option_is_int(self) -> None:
        """
        Tests that the --id option is an integer type.

        :return: None
        """
        from csle_cli.cli import ls
        id_param = next((p for p in ls.params if p.name == "id"), None)
        assert id_param is not None
        assert id_param.type == click.INT

    def test_ls_entity_argument_default(self) -> None:
        """
        Tests that the entity argument has a default value of 'all'.

        :return: None
        """
        from csle_cli.cli import ls
        entity_param = next((p for p in ls.params if p.name == "entity"), None)
        assert entity_param is not None
        assert entity_param.default == "all"


class TestLsShellComplete:
    """
    Test suite for ls shell completion function.

    Note: The actual ls_shell_complete function requires Docker and database
    connections. These tests only verify the function exists and is callable.
    """

    def test_ls_shell_complete_function_exists(self) -> None:
        """
        Tests that the ls_shell_complete function exists.

        :return: None
        """
        from csle_cli.cli import ls_shell_complete
        assert ls_shell_complete is not None
        assert callable(ls_shell_complete)


class TestAttackerShellComplete:
    """
    Test suite for attacker shell completion function.

    Note: The actual attacker_shell_complete function requires database
    connections. These tests only verify the function exists.
    """

    def test_attacker_shell_complete_function_exists(self) -> None:
        """
        Tests that the attacker_shell_complete function exists.

        :return: None
        """
        from csle_cli.cli import attacker_shell_complete
        assert attacker_shell_complete is not None
        assert callable(attacker_shell_complete)
