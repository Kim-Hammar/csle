from typing import Dict, Any
import subprocess
import re
import logging
import yaml
import csle_collector.five_g_cu_manager.five_g_cu_manager_pb2
import csle_collector.constants.constants as constants


class FiveGCUManagerUtil:
    """
    Class with utility functions for the 5G CU manager
    """

    @staticmethod
    def get_cu_status(control_script_path: str) -> Dict[str, bool]:
        """
        Executes the control script, parses the output, and return the statuses of the 5G CU services

        :param control_script_path: the path to the control script
        :return: A dict with the names of the statuses and boolean values indicating if the services are running
        """
        status_map = {}
        try:
            result = subprocess.run([control_script_path, constants.FIVE_G_CU.STATUS],
                                    capture_output=True, text=True, check=True, cwd=".")

            output_lines = result.stdout.strip().split('\n')

            # Regex to capture the service name and its status
            status_pattern = re.compile(
                rf'^(\w+)\s+'
                rf'({re.escape(constants.FIVE_G_CU.RUNNING)}|{re.escape(constants.FIVE_G_CU.STOPPED)})',
                re.IGNORECASE
            )

            for line in output_lines:
                match = status_pattern.match(line.strip())
                if match:
                    service_name = match.group(1).lower()
                    status = match.group(2)
                    status_map[service_name] = (status == constants.FIVE_G_CU.RUNNING)

        except FileNotFoundError:
            logging.error(f"5G CU control script not found at {control_script_path}")
        except subprocess.CalledProcessError as e:
            logging.error(f"Script execution failed: {e.stderr}")
        except Exception as e:
            logging.error(f"An unexpected error occurred during status retrieval: {e}")

        return status_map

    @staticmethod
    def start_cu(control_script_path: str) -> bool:
        """
        Starts the 5G CU using the control script with the 'start' command.

        :param control_script_path: the path to the control script
        :return: True if the script execution completed successfully, False otherwise.
        """
        logging.info(f"Attempting to start the 5G CU using: {control_script_path} start")
        try:
            result = subprocess.run([control_script_path, constants.FIVE_G_CU.START],
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
    def stop_cu(control_script_path: str) -> bool:
        """
        Stops the 5G CU using the control script with the 'stop' command.

        :param control_script_path: the path to the control script
        :return: True if the script execution completed successfully, False otherwise.
        """
        logging.info(f"Attempting to stop the 5G CU using: {control_script_path} stop")
        try:
            result = subprocess.run([control_script_path, constants.FIVE_G_CU.STOP],
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

    @staticmethod
    def five_g_cu_status_dto_to_dict(
            five_g_cu_status_dto: csle_collector.five_g_cu_manager.five_g_cu_manager_pb2.FiveGCUStatusDTO) \
            -> Dict[str, Any]:
        """
        Converts a FiveGCUStatusDTO to a dict

        :param five_g_cu_status_dto: the DTO to convert
        :return: a dict representation of the DTO
        """
        d: Dict[str, Any] = {}
        d["cu_running"] = five_g_cu_status_dto.cu_running
        d["ip"] = five_g_cu_status_dto.ip
        return d

    @staticmethod
    def five_g_cu_status_dto_from_dict(d: Dict[str, Any]) \
            -> csle_collector.five_g_cu_manager.five_g_cu_manager_pb2.FiveGCUStatusDTO:
        """
        Converts a FiveGCUStatusDTO to a dict

        :param d: the dict to convert
        :return: the converted DTO
        """
        dto = csle_collector.five_g_cu_manager.five_g_cu_manager_pb2.FiveGCUStatusDTO()
        dto.cu_running = d["cu_running"]
        dto.ip = d["ip"]
        return dto

    @staticmethod
    def five_g_cu_status_dto_empty() -> csle_collector.five_g_cu_manager.five_g_cu_manager_pb2.FiveGCUStatusDTO:
        """
        :return: An empty FiveGCUStatusDTO
        """
        dto = csle_collector.five_g_cu_manager.five_g_cu_manager_pb2.FiveGCUStatusDTO()
        dto.cu_running = False
        dto.ip = "0.0.0.0"
        return dto

    @staticmethod
    def init_config_file(core_backhaul_ip: str, cu_ip: str) -> bool:
        """
        Initializes the /srsRAN_Project/build/apps/cu/cu.yml configuration file.

        :param core_backhaul_ip: The backhaul IP address of the 5G Core (AMF).
        :param cu_ip: The IP address of the CU (Central Unit).
        :return: True if the file was updated successfully, False otherwise.
        """
        config_path = "/srsRAN_Project/build/apps/cu/cu.yml"
        logging.info(f"Attempting to update CU config at {config_path}")
        logging.info(f"Setting Core IP (AMF addr) to: {core_backhaul_ip}")
        logging.info(f"Setting CU IP (AMF bind_addr) to: {cu_ip}")

        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
            try:
                if 'cu_cp' in config and 'amf' in config['cu_cp']:
                    config['cu_cp']['amf']['addr'] = core_backhaul_ip
                    config['cu_cp']['amf']['bind_addr'] = cu_ip
                else:
                    logging.error(f"Invalid YAML structure in {config_path}: 'cu_cp.amf' section missing.")
                    return False

                if 'cu_cp' in config and 'f1ap' in config['cu_cp']:
                    config['cu_cp']['f1ap']['bind_addr'] = cu_ip
                if 'cu_up' in config and 'f1u' in config['cu_up'] and 'socket' in config['cu_up']['f1u']:
                    if len(config['cu_up']['f1u']['socket']) > 0:
                        config['cu_up']['f1u']['socket'][0]['bind_addr'] = cu_ip

            except (TypeError, KeyError) as e:
                logging.error(f"Error modifying YAML structure: {e}")
                return False

            with open(config_path, 'w') as f:
                yaml.dump(config, f, default_flow_style=False, sort_keys=False)

            logging.info(f"Successfully updated {config_path}")
            return True

        except FileNotFoundError:
            logging.error(f"Configuration file not found at {config_path}")
            return False
        except PermissionError:
            logging.error(f"Permission denied. Cannot write to {config_path}.")
            return False
        except Exception as e:
            logging.error(f"An unexpected error occurred processing {config_path}: {e}")
            return False
