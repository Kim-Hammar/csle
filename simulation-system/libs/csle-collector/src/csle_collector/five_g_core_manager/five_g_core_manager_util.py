from typing import Dict, Any, List, Union
import subprocess
import re
import logging
import yaml
import requests
import time
import csle_collector.five_g_core_manager.five_g_core_manager_pb2
import csle_collector.constants.constants as constants
from csle_collector.five_g_core_manager.dao.five_g_core_amf_metrics import FiveGCoreAMFMetrics
from csle_collector.five_g_core_manager.dao.five_g_core_upf_metrics import FiveGCoreUPFMetrics
from csle_collector.five_g_core_manager.dao.five_g_core_mme_metrics import FiveGCoreMMEMetrics
from csle_collector.five_g_core_manager.dao.five_g_core_smf_metrics import FiveGCoreSMFMetrics
from csle_collector.five_g_core_manager.dao.five_g_core_hss_metrics import FiveGCoreHSSMetrics
from csle_collector.five_g_core_manager.dao.five_g_core_pcrf_metrics import FiveGCorePCRFMetrics
from csle_collector.five_g_core_manager.dao.five_g_core_pcf_metrics import FiveGCorePCFMetrics


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
        d["monitor_running"] = five_g_core_status_dto.monitor_running
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
    def init_subscriber_data(
            control_script_path: str,
            subscribers: List[csle_collector.five_g_core_manager.five_g_core_manager_pb2.FiveGSubscriberDTO]) -> bool:
        """
        Initializes the subscriber data for the 5G core.

        :param control_script_path: the path to the control script
        :param subscribers: list of subscribers
        :return: True if the script execution completed successfully, False otherwise.
        """
        logging.info(f"Attempting to initialize {len(subscribers)} subscribers using: {control_script_path}")

        for sub in subscribers:
            cmd_args = [
                control_script_path,
                sub.imsi,
                sub.key,
                sub.opc,
                sub.amf,
                str(sub.sqn)
            ]

            try:
                logging.debug(f"Adding subscriber IMSI: {sub.imsi}")
                subprocess.run(cmd_args, capture_output=True, text=True, check=True, cwd=".")
                logging.info(f"Subscriber {sub.imsi} initialized.")

            except FileNotFoundError:
                logging.error(f"5G Core control script not found at {control_script_path}")
                return False
            except subprocess.CalledProcessError as e:
                logging.error(f"Failed to initialize subscriber {sub.imsi}. Stderr: {e.stderr.strip()}")
                logging.error(f"Stdout: {e.stdout.strip()}")
                return False
            except Exception as e:
                logging.error(f"An unexpected error occurred during initialization of subscriber {sub.imsi}: {e}")
                return False

        logging.info("All subscriber data initialized successfully.")
        return True

    @staticmethod
    def init_config_files(ip: str) -> bool:
        """
        Modifies the Open5GS configuration files to set the bind IP addresses.
        Specifically updates:
        1. /etc/open5gs/amf.yaml (amf -> ngap -> server -> address)
        2. /etc/open5gs/upf.yaml (upf -> pfcp -> server -> address)

        :param ip: The new IP address to set.
        :return: True if all files were updated successfully, False otherwise.
        """
        target_configs = [
            (
                "/etc/open5gs/amf.yaml",
                ["amf", "ngap", "server"]
            ),
            (
                "/etc/open5gs/upf.yaml",
                ["upf", "gtpu", "server"]
            )
        ]

        success = True

        for file_path, key_path in target_configs:
            logging.info(f"Attempting to update IP to {ip} in {file_path}")

            try:
                with open(file_path, 'r') as f:
                    config = yaml.safe_load(f)

                current_node = config
                path_valid = True

                for key in key_path:
                    if isinstance(current_node, dict) and key in current_node:
                        current_node = current_node[key]
                    else:
                        logging.error(f"Invalid structure in {file_path}: Key '{key}' not found.")
                        path_valid = False
                        break

                if path_valid and isinstance(current_node, list) and len(current_node) > 0:
                    current_node[0]['address'] = ip
                elif path_valid:
                    logging.error(f"Invalid structure in {file_path}: Target key is not a list or is empty.")
                    success = False
                    continue

                if path_valid:
                    with open(file_path, 'w') as f:
                        yaml.dump(config, f, default_flow_style=False, sort_keys=False)
                    logging.info(f"Successfully updated {file_path}")
                else:
                    success = False

            except FileNotFoundError:
                logging.error(f"Configuration file not found at {file_path}")
                success = False
            except PermissionError:
                logging.error(f"Permission denied. Cannot write to {file_path}. (Run as root?)")
                success = False
            except Exception as e:
                logging.error(f"An unexpected error occurred processing {file_path}: {e}")
                success = False

        return success

    @staticmethod
    def fetch_amf_metrics(ip: str) -> FiveGCoreAMFMetrics:
        """
        Fetches AMF metrics from the given URL and parses them into an AMFMetrics DTO.

        :param ip: The IP address string to populate the 'ip' field of the DTO
        :return: A populated AMFMetrics object
        """
        try:
            response = requests.get(constants.FIVE_G_CORE.AMF_METRICS_URL, timeout=5)
            response.raise_for_status()
            content = response.text
        except requests.RequestException as e:
            print(f"Error fetching metrics from {constants.FIVE_G_CORE.AMF_METRICS_URL}: {e}")
            return FiveGCoreAMFMetrics(ip=ip, ts=time.time())

        parsed_data = {}
        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            parts = line.split()
            if len(parts) < 2:
                continue
            raw_key = parts[0]
            raw_value = parts[-1]
            metric_name = raw_key.split('{')[0]
            try:
                value = int(float(raw_value))
                parsed_data[metric_name] = value
            except ValueError:
                continue
        valid_args = FiveGCoreAMFMetrics.__init__.__code__.co_varnames
        filtered_args: Dict[str, Union[int, str, float]]
        filtered_args = {k: v for k, v in parsed_data.items() if k in valid_args and k != 'self'}
        filtered_args['ip'] = str(ip)
        filtered_args['ts'] = float(time.time())

        return FiveGCoreAMFMetrics(**filtered_args)  # type: ignore

    @staticmethod
    def fetch_upf_metrics(ip: str) -> FiveGCoreUPFMetrics:
        """
        Fetches UPF metrics from the given URL and parses them into an UPFMetrics DTO.

        :param ip: The IP address string to populate the 'ip' field of the DTO
        :return: A populated UPFMetrics object
        """
        try:
            response = requests.get(constants.FIVE_G_CORE.UPF_METRICS_URL, timeout=5)
            response.raise_for_status()
            content = response.text
        except requests.RequestException as e:
            print(f"Error fetching metrics from {constants.FIVE_G_CORE.UPF_METRICS_URL}: {e}")
            return FiveGCoreUPFMetrics(ip=ip, ts=time.time())

        parsed_data = {}
        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            parts = line.split()
            if len(parts) < 2:
                continue
            raw_key = parts[0]
            raw_value = parts[-1]
            metric_name = raw_key.split('{')[0]
            try:
                value = int(float(raw_value))
                parsed_data[metric_name] = value
            except ValueError:
                continue
        valid_args = FiveGCoreUPFMetrics.__init__.__code__.co_varnames
        filtered_args: Dict[str, Union[int, str, float]]
        filtered_args = {k: v for k, v in parsed_data.items() if k in valid_args and k != 'self'}
        filtered_args['ip'] = str(ip)
        filtered_args['ts'] = float(time.time())

        return FiveGCoreUPFMetrics(**filtered_args)  # type: ignore

    @staticmethod
    def fetch_mme_metrics(ip: str) -> FiveGCoreMMEMetrics:
        """
        Fetches MME metrics from the given URL and parses them into an MMEMetrics DTO.

        :param ip: The IP address string to populate the 'ip' field of the DTO
        :return: A populated MMEMetrics object
        """
        try:
            response = requests.get(constants.FIVE_G_CORE.MME_METRICS_URL, timeout=5)
            response.raise_for_status()
            content = response.text
        except requests.RequestException as e:
            print(f"Error fetching metrics from {constants.FIVE_G_CORE.MME_METRICS_URL}: {e}")
            return FiveGCoreMMEMetrics(ip=ip, ts=time.time())

        parsed_data = {}
        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            parts = line.split()
            if len(parts) < 2:
                continue
            raw_key = parts[0]
            raw_value = parts[-1]
            metric_name = raw_key.split('{')[0]
            try:
                value = int(float(raw_value))
                parsed_data[metric_name] = value
            except ValueError:
                continue
        valid_args = FiveGCoreMMEMetrics.__init__.__code__.co_varnames
        filtered_args: Dict[str, Union[int, str, float]]
        filtered_args = {k: v for k, v in parsed_data.items() if k in valid_args and k != 'self'}
        filtered_args['ip'] = str(ip)
        filtered_args['ts'] = float(time.time())

        return FiveGCoreMMEMetrics(**filtered_args)  # type: ignore

    @staticmethod
    def fetch_smf_metrics(ip: str) -> FiveGCoreSMFMetrics:
        """
        Fetches SMF metrics from the given URL and parses them into an SMFMetrics DTO.

        :param ip: The IP address string to populate the 'ip' field of the DTO
        :return: A populated SMFMetrics object
        """
        try:
            response = requests.get(constants.FIVE_G_CORE.SMF_METRICS_URL, timeout=5)
            response.raise_for_status()
            content = response.text
        except requests.RequestException as e:
            print(f"Error fetching metrics from {constants.FIVE_G_CORE.SMF_METRICS_URL}: {e}")
            return FiveGCoreSMFMetrics(ip=ip, ts=time.time())

        parsed_data = {}
        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            parts = line.split()
            if len(parts) < 2:
                continue
            raw_key = parts[0]
            raw_value = parts[-1]
            metric_name = raw_key.split('{')[0]
            try:
                value = int(float(raw_value))
                parsed_data[metric_name] = value
            except ValueError:
                continue
        valid_args = FiveGCoreSMFMetrics.__init__.__code__.co_varnames
        filtered_args: Dict[str, Union[int, str, float]]
        filtered_args = {k: v for k, v in parsed_data.items() if k in valid_args and k != 'self'}
        filtered_args['ip'] = str(ip)
        filtered_args['ts'] = float(time.time())

        return FiveGCoreSMFMetrics(**filtered_args)  # type: ignore

    @staticmethod
    def fetch_hss_metrics(ip: str) -> FiveGCoreHSSMetrics:
        """
        Fetches HSS metrics from the given URL and parses them into an HSSMetrics DTO.

        :param ip: The IP address string to populate the 'ip' field of the DTO
        :return: A populated HSSMetrics object
        """
        try:
            response = requests.get(constants.FIVE_G_CORE.HSS_METRICS_URL, timeout=5)
            response.raise_for_status()
            content = response.text
        except requests.RequestException as e:
            print(f"Error fetching metrics from {constants.FIVE_G_CORE.HSS_METRICS_URL}: {e}")
            return FiveGCoreHSSMetrics(ip=ip, ts=time.time())

        parsed_data = {}
        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            parts = line.split()
            if len(parts) < 2:
                continue
            raw_key = parts[0]
            raw_value = parts[-1]
            metric_name = raw_key.split('{')[0]
            try:
                value = int(float(raw_value))
                parsed_data[metric_name] = value
            except ValueError:
                continue
        valid_args = FiveGCoreHSSMetrics.__init__.__code__.co_varnames
        filtered_args: Dict[str, Union[int, str, float]]
        filtered_args = {k: v for k, v in parsed_data.items() if k in valid_args and k != 'self'}
        filtered_args['ip'] = str(ip)
        filtered_args['ts'] = float(time.time())

        return FiveGCoreHSSMetrics(**filtered_args)  # type: ignore

    @staticmethod
    def fetch_pcrf_metrics(ip: str) -> FiveGCorePCRFMetrics:
        """
        Fetches PCRF metrics from the given URL and parses them into an PCRFMetrics DTO.

        :param ip: The IP address string to populate the 'ip' field of the DTO
        :return: A populated PCRFMetrics object
        """
        try:
            response = requests.get(constants.FIVE_G_CORE.PCRF_METRICS_URL, timeout=5)
            response.raise_for_status()
            content = response.text
        except requests.RequestException as e:
            print(f"Error fetching metrics from {constants.FIVE_G_CORE.PCRF_METRICS_URL}: {e}")
            return FiveGCorePCRFMetrics(ip=ip, ts=time.time())

        parsed_data = {}
        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            parts = line.split()
            if len(parts) < 2:
                continue
            raw_key = parts[0]
            raw_value = parts[-1]
            metric_name = raw_key.split('{')[0]
            try:
                value = int(float(raw_value))
                parsed_data[metric_name] = value
            except ValueError:
                continue
        valid_args = FiveGCorePCRFMetrics.__init__.__code__.co_varnames
        filtered_args: Dict[str, Union[int, str, float]]
        filtered_args = {k: v for k, v in parsed_data.items() if k in valid_args and k != 'self'}
        filtered_args['ip'] = str(ip)
        filtered_args['ts'] = float(time.time())

        return FiveGCorePCRFMetrics(**filtered_args)  # type: ignore

    @staticmethod
    def fetch_pcf_metrics(ip: str) -> FiveGCorePCFMetrics:
        """
        Fetches PCF metrics from the given URL and parses them into an PCFMetrics DTO.

        :param ip: The IP address string to populate the 'ip' field of the DTO
        :return: A populated PCFMetrics object
        """
        try:
            response = requests.get(constants.FIVE_G_CORE.PCF_METRICS_URL, timeout=5)
            response.raise_for_status()
            content = response.text
        except requests.RequestException as e:
            print(f"Error fetching metrics from {constants.FIVE_G_CORE.PCF_METRICS_URL}: {e}")
            return FiveGCorePCFMetrics(ip=ip, ts=time.time())

        parsed_data = {}
        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            parts = line.split()
            if len(parts) < 2:
                continue
            raw_key = parts[0]
            raw_value = parts[-1]
            metric_name = raw_key.split('{')[0]
            try:
                value = int(float(raw_value))
                parsed_data[metric_name] = value
            except ValueError:
                continue
        valid_args = FiveGCorePCFMetrics.__init__.__code__.co_varnames
        filtered_args: Dict[str, Union[int, str, float]]
        filtered_args = {k: v for k, v in parsed_data.items() if k in valid_args and k != 'self'}
        filtered_args['ip'] = str(ip)
        filtered_args['ts'] = float(time.time())

        return FiveGCorePCFMetrics(**filtered_args)  # type: ignore
