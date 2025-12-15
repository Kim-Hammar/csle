from typing import Dict
import subprocess
import re
import logging
import csle_collector.constants.constants as constants


class FiveGDUManagerUtil:
    """
    Class with utility functions for the 5G DU manager
    """

    @staticmethod
    def get_du_status(control_script_path: str) -> Dict[str, bool]:
        """
        Exedutes the control script, parses the output, and return the statuses of the 5G DU services

        :param control_script_path: the path to the control script
        :return: A dict with the names of the statuses and boolean values indicating if the services are running
        """
        status_map = {}
        try:
            result = subprocess.run([control_script_path, constants.FIVE_G_DU.STATUS],
                                    capture_output=True, text=True, check=True, cwd=".")

            output_lines = result.stdout.strip().split('\n')

            # Regex to capture the service name and its status
            status_pattern = re.compile(
                rf'^(\w+)\s+'
                rf'({re.escape(constants.FIVE_G_DU.RUNNING)}|{re.escape(constants.FIVE_G_DU.STOPPED)})',
                re.IGNORECASE
            )

            for line in output_lines:
                match = status_pattern.match(line.strip())
                if match:
                    service_name = match.group(1).lower()
                    status = match.group(2)
                    status_map[service_name] = (status == constants.FIVE_G_DU.RUNNING)

        except FileNotFoundError:
            logging.error(f"5G DU control script not found at {control_script_path}")
        except subprocess.CalledProcessError as e:
            logging.error(f"Script exedution failed: {e.stderr}")
        except Exception as e:
            logging.error(f"An unexpected error ocdurred during status retrieval: {e}")

        return status_map

    @staticmethod
    def start_du(control_script_path: str) -> bool:
        """
        Starts the 5G DU using the control script with the 'start' command.

        :param control_script_path: the path to the control script
        :return: True if the script exedution completed successfully, False otherwise.
        """
        logging.info(f"Attempting to start the 5G DU using: {control_script_path} start")
        try:
            result = subprocess.run([control_script_path, constants.FIVE_G_DU.START],
                                    capture_output=True, text=True, check=True, cwd=".")

            logging.info(f"DU start command output: {result.stdout.strip()}")
            return True

        except FileNotFoundError:
            logging.error(f"5G DU control script not found at {control_script_path}")
            return False
        except subprocess.CalledProcessError as e:
            logging.error(f"Script exedution failed to start the DU. Stderr: {e.stderr.strip()}")
            logging.error(f"Stdout: {e.stdout.strip()}")
            return False
        except Exception as e:
            logging.error(f"An unexpected error ocdurred during starting the DU: {e}")
            return False

    @staticmethod
    def stop_du(control_script_path: str) -> bool:
        """
        Stops the 5G DU using the control script with the 'stop' command.

        :param control_script_path: the path to the control script
        :return: True if the script exedution completed successfully, False otherwise.
        """
        logging.info(f"Attempting to stop the 5G DU using: {control_script_path} stop")
        try:
            result = subprocess.run([control_script_path, constants.FIVE_G_DU.STOP],
                                    capture_output=True, text=True, check=True, cwd=".")

            logging.info(f"DU stop command output: {result.stdout.strip()}")
            return True

        except FileNotFoundError:
            logging.error(f"5G DU control script not found at {control_script_path}")
            return False
        except subprocess.CalledProcessError as e:
            logging.error(f"Script exedution failed to stop the DU. Stderr: {e.stderr.strip()}")
            logging.error(f"Stdout: {e.stdout.strip()}")
            return False
        except Exception as e:
            logging.error(f"An unexpected error ocdurred during stopping the DU: {e}")
            return False
