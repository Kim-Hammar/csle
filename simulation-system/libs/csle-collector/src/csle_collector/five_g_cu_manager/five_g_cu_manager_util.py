from typing import Dict
import subprocess
import re
import logging
import csle_collector.constants.constants as constants


class FiveGCUManagerUtil:
    """
    Class with utility functions for the 5g CU manager
    """

    @staticmethod
    def get_script_status_map(control_script_path: str) -> Dict[str, bool]:
        """
        Executes the control script, parses the output, and return the statuses of the 5G CU services

        :param control_script_path: the path to the control script
        :return: A dict with the names of the statuses and boolean values indicating if the services are running
        """
        status_map = {}
        try:
            result = subprocess.run(
                [control_script_path, constants.FIVE_G_CU.ALL, constants.FIVE_G_CORE.STATUS],
                capture_output=True, text=True, check=True, cwd=".")

            output_lines = result.stdout.strip().split('\n')

            # Regex to capture the service name and its status
            status_pattern = re.compile(
                rf'^(\w+)\s+'
                rf'({re.escape(constants.FIVE_G_CORE.RUNNING)}|{re.escape(constants.FIVE_G_CORE.STOPPED)})',
                re.IGNORECASE
            )

            for line in output_lines:
                match = status_pattern.match(line.strip())
                if match:
                    service_name = match.group(1).lower()
                    status = match.group(2)
                    status_map[service_name] = (status == constants.FIVE_G_CORE.RUNNING)

        except FileNotFoundError:
            logging.error(f"5G CU control script not found at {control_script_path}")
        except subprocess.CalledProcessError as e:
            logging.error(f"Script execution failed: {e.stderr}")
        except Exception as e:
            logging.error(f"An unexpected error occurred during status retrieval: {e}")

        return status_map

    @staticmethod
    def start_all_services(control_script_path: str) -> bool:
        """
        Starts all 5G CU services using the control script with the 'all start' command.

        :param control_script_path: the path to the control script
        :return: True if the script execution completed successfully, False otherwise.
        """
        logging.info(f"Attempting to start the 5G CU using: {control_script_path} all start")
        try:
            result = subprocess.run(
                [control_script_path, constants.FIVE_G_CORE.ALL, constants.FIVE_G_CORE.START],
                capture_output=True, text=True, check=True, cwd=".")

            logging.info(f"CU start command output: {result.stdout.strip()}")
            return True

        except FileNotFoundError:
            logging.error(f"5G CU control script not found at {control_script_path}")
            return False
        except subprocess.CalledProcessError as e:
            logging.error(f"Script execution failed to start the CU. Stderr: {e.stderr.strip()}")
            logging.error(f"Stdout: {e.stdout.strip()}")
            return False
        except Exception as e:
            logging.error(f"An unexpected error occurred during starting the CU: {e}")
            return False

    @staticmethod
    def stop_all_services(control_script_path: str) -> bool:
        """
        Stops all 5G CU services using the control script with the 'all stop' command.

        :param control_script_path: the path to the control script
        :return: True if the script execution completed successfully, False otherwise.
        """
        logging.info(f"Attempting to stop the 5G CU using: {control_script_path} all stop")
        try:
            result = subprocess.run(
                [control_script_path, constants.FIVE_G_CORE.ALL, constants.FIVE_G_CORE.STOP],
                capture_output=True, text=True, check=True, cwd=".")

            logging.info(f"CU stop command output: {result.stdout.strip()}")
            return True

        except FileNotFoundError:
            logging.error(f"5G CU control script not found at {control_script_path}")
            return False
        except subprocess.CalledProcessError as e:
            logging.error(f"Script execution failed to stop the CU. Stderr: {e.stderr.strip()}")
            logging.error(f"Stdout: {e.stdout.strip()}")
            return False
        except Exception as e:
            logging.error(f"An unexpected error occurred during stopping the CU: {e}")
            return False
