from typing import Dict, Any
import subprocess
import re
import logging
import yaml
import os
import configparser
import csle_collector.five_g_du_manager.five_g_du_manager_pb2
import csle_collector.constants.constants as constants


class FiveGDUManagerUtil:
    """
    Class with utility functions for the 5G DU manager
    """

    @staticmethod
    def get_du_status(control_script_path: str) -> Dict[str, bool]:
        """
        Executes the control script, parses the output, and return the status of the 5G DU

        :param control_script_path: the path to the control script
        :return: A dict with the names of the statuses and boolean values indicating if the DU is running
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
            logging.error(f"Script execution failed: {e.stderr}")
        except Exception as e:
            logging.error(f"An unexpected error occurred during status retrieval: {e}")

        return status_map

    @staticmethod
    def start_du(control_script_path: str) -> bool:
        """
        Starts the 5G DU using the control script with the 'start' command.

        :param control_script_path: the path to the control script
        :return: True if the script execution completed successfully, False otherwise.
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
            logging.error(f"Script execution failed to start the DU. Stderr: {e.stderr.strip()}")
            logging.error(f"Stdout: {e.stdout.strip()}")
            return False
        except Exception as e:
            logging.error(f"An unexpected error occurred during starting the DU: {e}")
            return False

    @staticmethod
    def stop_du(control_script_path: str) -> bool:
        """
        Stops the 5G DU using the control script with the 'stop' command.

        :param control_script_path: the path to the control script
        :return: True if the script execution completed successfully, False otherwise.
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
            logging.error(f"Script execution failed to stop the DU. Stderr: {e.stderr.strip()}")
            logging.error(f"Stdout: {e.stdout.strip()}")
            return False
        except Exception as e:
            logging.error(f"An unexpected error occurred during stopping the DU: {e}")
            return False

    @staticmethod
    def start_ue(control_script_path: str) -> bool:
        """
        Starts the 5G UE using the control script with the 'start' command.

        :param control_script_path: the path to the control script
        :return: True if the script execution completed successfully, False otherwise.
        """
        logging.info(f"Attempting to start the 5G UE using: {control_script_path} start")
        try:
            result = subprocess.run([control_script_path, constants.FIVE_G_DU.START],
                                    capture_output=True, text=True, check=True, cwd=".")

            logging.info(f"UE start command output: {result.stdout.strip()}")
            return True

        except FileNotFoundError:
            logging.error(f"5G UE control script not found at {control_script_path}")
            return False
        except subprocess.CalledProcessError as e:
            logging.error(f"Script execution failed to start the UE. Stderr: {e.stderr.strip()}")
            logging.error(f"Stdout: {e.stdout.strip()}")
            return False
        except Exception as e:
            logging.error(f"An unexpected error occurred during starting the UE: {e}")
            return False

    @staticmethod
    def stop_ue(control_script_path: str) -> bool:
        """
        Stops the 5G UE using the control script with the 'start' command.

        :param control_script_path: the path to the control script
        :return: True if the script execution completed successfully, False otherwise.
        """
        logging.info(f"Attempting to stop the 5G UE using: {control_script_path} start")
        try:
            result = subprocess.run([control_script_path, constants.FIVE_G_DU.STOP],
                                    capture_output=True, text=True, check=True, cwd=".")

            logging.info(f"UE stop command output: {result.stdout.strip()}")
            return True

        except FileNotFoundError:
            logging.error(f"5G UE control script not found at {control_script_path}")
            return False
        except subprocess.CalledProcessError as e:
            logging.error(f"Script execution failed to stop the UE. Stderr: {e.stderr.strip()}")
            logging.error(f"Stdout: {e.stdout.strip()}")
            return False
        except Exception as e:
            logging.error(f"An unexpected error occurred during stopping the UE: {e}")
            return False

    @staticmethod
    def init_ue(control_script_path: str) -> bool:
        """
        Initializes the 5G UE using the control script with the 'init' command.

        :param control_script_path: the path to the control script
        :return: True if the script execution completed successfully, False otherwise.
        """
        logging.info(f"Attempting to initialize the 5G UE using: {control_script_path} init")
        try:
            result = subprocess.run([control_script_path, constants.FIVE_G_DU.INIT],
                                    capture_output=True, text=True, check=True, cwd=".")

            logging.info(f"UE init command output: {result.stdout.strip()}")
            return True

        except FileNotFoundError:
            logging.error(f"5G UE control script not found at {control_script_path}")
            return False
        except subprocess.CalledProcessError as e:
            logging.error(f"Script execution failed to initialize the UE. Stderr: {e.stderr.strip()}")
            logging.error(f"Stdout: {e.stdout.strip()}")
            return False
        except Exception as e:
            logging.error(f"An unexpected error occurred during initializing the UE: {e}")
            return False

    @staticmethod
    def get_ue_status(control_script_path: str) -> Dict[str, bool]:
        """
        Executes the control script, parses the output, and return the statuses of the 5G UE

        :param control_script_path: the path to the control script
        :return: A dict with the names of the statuses and boolean values indicating if the DU is running
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
            logging.error(f"5G UE control script not found at {control_script_path}")
        except subprocess.CalledProcessError as e:
            logging.error(f"Script execution failed: {e.stderr}")
        except Exception as e:
            logging.error(f"An unexpected error occurred during status retrieval: {e}")

        return status_map

    @staticmethod
    def five_g_du_status_dto_to_dict(
            five_g_du_status_dto: csle_collector.five_g_du_manager.five_g_du_manager_pb2.FiveGDUStatusDTO) \
            -> Dict[str, Any]:
        """
        Converts a FiveGDUStatusDTO to a dict

        :param five_g_du_status_dto: the DTO to convert
        :return: a dict representation of the DTO
        """
        d: Dict[str, Any] = {}
        d["du_running"] = five_g_du_status_dto.du_running
        d["ue_running"] = five_g_du_status_dto.ue_running
        d["monitor_running"] = five_g_du_status_dto.monitor_running
        d["ip"] = five_g_du_status_dto.ip
        return d

    @staticmethod
    def five_g_du_status_dto_from_dict(d: Dict[str, Any]) \
            -> csle_collector.five_g_du_manager.five_g_du_manager_pb2.FiveGDUStatusDTO:
        """
        Converts a FiveGDUStatusDTO to a dict

        :param d: the dict to convert
        :return: the converted DTO
        """
        dto = csle_collector.five_g_du_manager.five_g_du_manager_pb2.FiveGDUStatusDTO()
        dto.du_running = d["du_running"]
        dto.ue_running = d["ue_running"]
        dto.ip = d["ip"]
        return dto

    @staticmethod
    def five_g_du_status_dto_empty() -> csle_collector.five_g_du_manager.five_g_du_manager_pb2.FiveGDUStatusDTO:
        """
        :return: An empty FiveGDUStatusDTO
        """
        dto = csle_collector.five_g_du_manager.five_g_du_manager_pb2.FiveGDUStatusDTO()
        dto.du_running = False
        dto.ue_running = False
        dto.ip = "0.0.0.0"
        return dto

    @staticmethod
    def init_du_config_file(cu_fronthaul_ip: str, du_fronthaul_ip: str, pci: int,
                            gnb_du_id: int, sector_id: int) -> bool:
        """
        Modifies the /srsRAN_Project/build/apps/du/du.yml configuration file.

        :param gnb_du_id: The ID of the DU (each DU connected to the same CU must have a unique ID)
        :param sector_id: Part of the cell ID of the DU
        :param pci: Physical Cell ID of the DU
        :param cu_fronthaul_ip: The IP address of the CU (F1-C interface).
        :param du_fronthaul_ip: The IP address of the DU (F1-U interface).
        :return: True if the file was updated successfully, False otherwise.
        """
        config_path = "/srsRAN_Project/build/apps/du/du.yml"
        logging.info(f"Attempting to update DU config at {config_path}")
        logging.info(f"Setting CU IP (cu_cp_addr) to: {cu_fronthaul_ip}")
        logging.info(f"Setting DU IP (bind_addr) to: {du_fronthaul_ip}")
        logging.info(f"Setting DU gnb_du_id to: {gnb_du_id}")
        logging.info(f"Setting DU pci to: {pci}")
        logging.info(f"Setting DU sector_id to: {sector_id}")
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
            try:
                config["gnb_du_id"] = gnb_du_id
                if 'f1ap' in config:
                    config['f1ap']['cu_cp_addr'] = cu_fronthaul_ip
                    config['f1ap']['bind_addr'] = du_fronthaul_ip
                else:
                    logging.error(f"Invalid YAML structure in {config_path}: 'f1ap' section missing.")
                    return False

                if 'f1u' in config and 'socket' in config['f1u']:
                    if isinstance(config['f1u']['socket'], list) and len(config['f1u']['socket']) > 0:
                        config['f1u']['socket'][0]['bind_addr'] = du_fronthaul_ip
                    else:
                        logging.warning(f"{config_path}: 'f1u.socket' list is empty. Skipping F1U update.")
                else:
                    logging.warning(f"{config_path}: 'f1u' section missing. Skipping F1U update.")

                if 'cell_cfg' in config:
                    config['cell_cfg']['pci'] = pci
                    config['cell_cfg']['sector_id'] = sector_id
                else:
                    logging.error(f"Invalid YAML structure in {config_path}: 'cell_cfg' section missing.")
                    return False

            except (TypeError, KeyError, IndexError) as e:
                logging.error(f"Error modifying DU YAML structure: {e}")
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

    @staticmethod
    def init_ue_config_file(imsi: str, key: str, opc: str, imei: str) -> bool:
        """
        Modifies the /srsRAN_4G/build/srsue/src/ue.conf configuration file.
        Updates the [usim] section with subscriber data.

        :param imsi: The imsi of the UE.
        :param key: The private key of the UE.
        :param opc: The operator key of the UE.
        :param imei: The imei of the UE.
        :return: True if the file was updated successfully, False otherwise.
        """
        config_path = "/srsRAN_4G/build/srsue/src/ue.conf"
        logging.info(f"Attempting to update UE config at {config_path}")
        logging.info(f"Setting subscriber data. imsi: {imsi}, key: {key}, opc: {opc}, imei: {imei}")

        # Define a helper class to handle case-sensitivity correctly
        class CaseSensitiveConfigParser(configparser.ConfigParser):
            def optionxform(self, optionstr: str) -> str:
                return optionstr

        try:
            if not os.path.exists(config_path):
                logging.error(f"Configuration file not found at {config_path}")
                return False

            # Use the custom class instead of patching the instance
            config = CaseSensitiveConfigParser()

            files_read = config.read(config_path)
            if not files_read:
                logging.error(f"Failed to read/parse configuration file at {config_path}")
                return False

            if 'usim' not in config:
                logging.error(f"Invalid INI structure in {config_path}: '[usim]' section missing.")
                return False

            # Update the subscriber data
            config['usim']['imsi'] = imsi
            config['usim']['k'] = key
            config['usim']['opc'] = opc
            config['usim']['imei'] = imei

            with open(config_path, 'w') as f:
                config.write(f)

            logging.info(f"Successfully updated {config_path}")
            return True

        except PermissionError:
            logging.error(f"Permission denied. Cannot write to {config_path}.")
            return False
        except Exception as e:
            logging.error(f"An unexpected error occurred processing {config_path}: {e}")
            return False
