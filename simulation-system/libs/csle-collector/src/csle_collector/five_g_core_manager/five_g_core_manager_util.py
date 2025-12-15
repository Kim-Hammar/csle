from typing import Dict, Any
import subprocess
import re
import logging
import csle_collector.five_g_core_manager.five_g_core_manager_pb2
import csle_collector.constants.constants as constants


class FiveGCoreManagerUtil:
    """
    Class with utility functions for the 5g core manager
    """

    @staticmethod
    def get_core_status(control_script_path: str) -> Dict[str, bool]:
        """
        Executes the control script, parses the output, and return the statuses of the 5G core services

        :param control_script_path: the path to the control script
        :return: A dict with the names of the statuses and boolean values indicating if the services are running
        """
        status_map = {}
        try:
            result = subprocess.run(
                [control_script_path, constants.FIVE_G_CORE.ALL, constants.FIVE_G_CORE.STATUS],
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
            logging.error(f"5G Core control script not found at {control_script_path}")
        except subprocess.CalledProcessError as e:
            logging.error(f"Script execution failed: {e.stderr}")
        except Exception as e:
            logging.error(f"An unexpected error occurred during status retrieval: {e}")

        return status_map

    @staticmethod
    def start_all_core_services(control_script_path: str) -> bool:
        """
        Starts all 5G core services using the control script with the 'all start' command.

        :param control_script_path: the path to the control script
        :return: True if the script execution completed successfully, False otherwise.
        """
        logging.info(f"Attempting to start all 5G core services using: {control_script_path} all start")
        try:
            result = subprocess.run(
                [control_script_path, constants.FIVE_G_CORE.ALL, constants.FIVE_G_CORE.START],
                capture_output=True, text=True, check=True, cwd=".")

            logging.info(f"All services started command output: {result.stdout.strip()}")
            return True

        except FileNotFoundError:
            logging.error(f"5G Core control script not found at {control_script_path}")
            return False
        except subprocess.CalledProcessError as e:
            logging.error(f"Script execution failed to start all services. Stderr: {e.stderr.strip()}")
            logging.error(f"Stdout: {e.stdout.strip()}")
            return False
        except Exception as e:
            logging.error(f"An unexpected error occurred during service start: {e}")
            return False

    @staticmethod
    def stop_all_core_services(control_script_path: str) -> bool:
        """
        Stops all 5G core services using the control script with the 'all stop' command.

        :param control_script_path: the path to the control script
        :return: True if the script execution completed successfully, False otherwise.
        """
        logging.info(f"Attempting to stop all 5G core services using: {control_script_path} all stop")
        try:
            result = subprocess.run(
                [control_script_path, constants.FIVE_G_CORE.ALL, constants.FIVE_G_CORE.STOP],
                capture_output=True, text=True, check=True, cwd=".")

            logging.info(f"All services stopped command output: {result.stdout.strip()}")
            return True

        except FileNotFoundError:
            logging.error(f"5G Core control script not found at {control_script_path}")
            return False
        except subprocess.CalledProcessError as e:
            logging.error(f"Script execution failed to stop all services. Stderr: {e.stderr.strip()}")
            logging.error(f"Stdout: {e.stdout.strip()}")
            return False
        except Exception as e:
            logging.error(f"An unexpected error occurred during service stopping: {e}")
            return False

    @staticmethod
    def init_all_core_services(control_script_path: str) -> bool:
        """
        Initializes all 5G core services using the control script with the 'all init' command.

        :param control_script_path: the path to the control script
        :return: True if the script execution completed successfully, False otherwise.
        """
        logging.info(f"Attempting to initialize all 5G core services using: {control_script_path} all init")
        try:
            result = subprocess.run(
                [control_script_path, constants.FIVE_G_CORE.ALL, constants.FIVE_G_CORE.INIT],
                capture_output=True, text=True, check=True, cwd=".")

            logging.info(f"All services initialized command output: {result.stdout.strip()}")
            return True

        except FileNotFoundError:
            logging.error(f"5G Core control script not found at {control_script_path}")
            return False
        except subprocess.CalledProcessError as e:
            logging.error(f"Script execution failed to initialize all services. Stderr: {e.stderr.strip()}")
            logging.error(f"Stdout: {e.stdout.strip()}")
            return False
        except Exception as e:
            logging.error(f"An unexpected error occurred during service initialization: {e}")
            return False

    @staticmethod
    def five_g_core_status_dto_to_dict(
            five_g_core_status_dto: csle_collector.five_g_core_manager.five_g_core_manager_pb2.FiveGCoreStatusDTO) \
            -> Dict[str, Any]:
        """
        Converts a FiveGCoreStatusDTO to a dict

        :param five_g_core_status_dto: the DTO to convert
        :return: a dict representation of the DTO
        """
        d: Dict[str, Any] = {}
        d["mongo_running"] = five_g_core_status_dto.mongo_running
        d["mme_running"] = five_g_core_status_dto.mme_running
        d["sgwc_running"] = five_g_core_status_dto.sgwc_running
        d["smf_running"] = five_g_core_status_dto.smf_running
        d["amf_running"] = five_g_core_status_dto.amf_running
        d["sgwu_running"] = five_g_core_status_dto.sgwu_running
        d["upf_running"] = five_g_core_status_dto.upf_running
        d["hss_running"] = five_g_core_status_dto.hss_running
        d["pcrf_running"] = five_g_core_status_dto.pcrf_running
        d["nrf_running"] = five_g_core_status_dto.nrf_running
        d["scp_running"] = five_g_core_status_dto.scp_running
        d["sepp_running"] = five_g_core_status_dto.sepp_running
        d["ausf_running"] = five_g_core_status_dto.ausf_running
        d["udm_running"] = five_g_core_status_dto.udm_running
        d["pcf_running"] = five_g_core_status_dto.pcf_running
        d["nssf_running"] = five_g_core_status_dto.nssf_running
        d["bsf_running"] = five_g_core_status_dto.bsf_running
        d["udr_running"] = five_g_core_status_dto.udr_running
        d["webui_running"] = five_g_core_status_dto.webui_running
        d["ip"] = five_g_core_status_dto.ip
        return d

    @staticmethod
    def five_g_core_status_dto_from_dict(d: Dict[str, Any]) \
            -> csle_collector.five_g_core_manager.five_g_core_manager_pb2.FiveGCoreStatusDTO:
        """
        Converts a FiveGCoreStatusDTO to a dict

        :param d: the dict to convert
        :return: the converted DTO
        """
        dto = csle_collector.five_g_core_manager.five_g_core_manager_pb2.FiveGCoreStatusDTO()
        dto.mongo_running = d["mongo_running"]
        dto.mme_running = d["mme_running"]
        dto.sgwc_running = d["sgwc_running"]
        dto.smf_running = d["smf_running"]
        dto.amf_running = d["amf_running"]
        dto.sgwu_running = d["sgwu_running"]
        dto.upf_running = d["upf_running"]
        dto.hss_running = d["hss_running"]
        dto.pcrf_running = d["pcrf_running"]
        dto.nrf_running = d["nrf_running"]
        dto.scp_running = d["scp_running"]
        dto.sepp_running = d["sepp_running"]
        dto.ausf_running = d["ausf_running"]
        dto.udm_running = d["udm_running"]
        dto.pcf_running = d["pcf_running"]
        dto.nssf_running = d["nssf_running"]
        dto.bsf_running = d["bsf_running"]
        dto.udr_running = d["udr_running"]
        dto.webui_running = d["webui_running"]
        dto.ip = d["ip"]
        return dto

    @staticmethod
    def five_g_core_status_dto_empty() -> csle_collector.five_g_core_manager.five_g_core_manager_pb2.FiveGCoreStatusDTO:
        """
        :return: An empty FiveGCoreStatusDTO
        """
        dto = csle_collector.five_g_core_manager.five_g_core_manager_pb2.FiveGCoreStatusDTO()
        dto.mongo_running = False
        dto.mme_running = False
        dto.sgwc_running = False
        dto.smf_running = False
        dto.amf_running = False
        dto.sgwu_running = False
        dto.upf_running = False
        dto.hss_running = False
        dto.pcrf_running = False
        dto.nrf_running = False
        dto.scp_running = False
        dto.sepp_running = False
        dto.ausf_running = False
        dto.udm_running = False
        dto.pcf_running = False
        dto.nssf_running = False
        dto.bsf_running = False
        dto.udr_running = False
        dto.webui_running = False
        dto.ip = "0.0.0.0"
        return dto

    @staticmethod
    def init_subscriber_data(control_script_path: str) -> bool:
        """
        Initializes the subscriber data for the 5G core.

        :param control_script_path: the path to the control script
        :return: True if the script execution completed successfully, False otherwise.
        """
        logging.info(f"Attempting to initialize the subscriber data for the 5G core using: {control_script_path}")
        try:
            result = subprocess.run([control_script_path], capture_output=True, text=True, check=True, cwd=".")
            logging.info(f"Subscriber data initialized, command output: {result.stdout.strip()}")
            return True

        except FileNotFoundError:
            logging.error(f"5G Core control script not found at {control_script_path}")
            return False
        except subprocess.CalledProcessError as e:
            logging.error(f"Script execution failed to initialize subscriber data. Stderr: {e.stderr.strip()}")
            logging.error(f"Stdout: {e.stdout.strip()}")
            return False
        except Exception as e:
            logging.error(f"An unexpected error occurred during initialization of subscriber data: {e}")
            return False
