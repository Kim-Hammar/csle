import time
import logging
import threading
import json
import websocket
from typing import Optional, Dict, Any
from confluent_kafka import Producer
import csle_collector.constants.constants as constants
from csle_collector.five_g_cu_manager.dao.five_g_cu_cp_metrics import FiveGCUCPMetrics
from csle_collector.five_g_cu_manager.dao.five_g_cu_app_resource_usage_metrics import FiveGCUAppResourceUsageMetrics
from csle_collector.five_g_cu_manager.dao.five_g_cu_buffer_pool_metrics import FiveGCUBufferPoolMetrics


class FiveGCUMonitorThread(threading.Thread):
    """
    Thread that collects the 5G CU (Central Unit) statistics via WebSockets and pushes them to Kafka
    periodically.
    """

    def __init__(self, kafka_ip: str, kafka_port: int, ip: str, hostname: str,
                 time_step_len_seconds: int, cu_port: int = 55556) -> None:
        """
        Initializes the thread

        :param kafka_ip: IP of the Kafka server to push to
        :param kafka_port: port of the Kafka server to push to
        :param ip: ip of the server we are pushing from (the CU IP)
        :param hostname: hostname of the server we are pushing from
        :param time_step_len_seconds: How often to push metrics to Kafka (throttling)
        :param cu_port: The WebSocket port configured in cu.yml (default 55555)
        """
        threading.Thread.__init__(self)
        self.kafka_ip = kafka_ip
        self.kafka_port = kafka_port
        self.ip = ip
        self.hostname = hostname
        self.time_step_len_seconds = time_step_len_seconds
        self.cu_port = cu_port
        self.conf = {
            constants.KAFKA.BOOTSTRAP_SERVERS_PROPERTY: f"{self.kafka_ip}:{self.kafka_port}",
            constants.KAFKA.CLIENT_ID_PROPERTY: self.hostname
        }
        self.producer = Producer(**self.conf)
        self.running = True
        self.ws: Optional[websocket.WebSocketApp] = None
        self.ws_thread: Optional[threading.Thread] = None
        self.metrics_buffer: Dict[str, Any] = {}
        self.buffer_lock = threading.Lock()

        logging.info(
            f"5G CU Monitor thread initialized. Target: {self.ip}:{self.cu_port}, "
            f"Interval: {self.time_step_len_seconds}s")

    def _on_open(self, ws) -> None:
        """
        Callback when websocket is opened

        :param ws: the websocket connection
        :return: None
        """
        logging.info(f"[5G CU Monitor] Connected to {self.ip}.")
        ws.send(json.dumps({"cmd": "metrics_subscribe"}))

    def _on_message(self, ws, message):
        """
        Ingestion Callback:
        Parses JSON, converts to DTO, and updates the shared buffer.

        :return: None
        """
        try:
            data = json.loads(message)
            if "cmd" in data:
                return
            dto = None
            key = None
            if "cu-cp" in data:
                dto = FiveGCUCPMetrics.from_ws_dict(data, ip=self.ip)
                key = "cu_cp"
            elif "app_resource_usage" in data:
                dto = FiveGCUAppResourceUsageMetrics.from_ws_dict(data, ip=self.ip)
                key = "app"
            elif "buffer_pool" in data:
                dto = FiveGCUBufferPoolMetrics.from_ws_dict(data, ip=self.ip)
                key = "buffer"
            if dto and key:
                with self.buffer_lock:
                    self.metrics_buffer[key] = dto

        except json.JSONDecodeError:
            logging.error("[5G CU Monitor] Received non-JSON message")
        except Exception as e:
            logging.error(f"[5G CU Monitor] Error parsing message: {e}")

    def _on_error(self, ws, error) -> None:
        """
        Callback when an error occurs with the websocket connection

        :param ws: the websocket connection
        :param error: the error that occurred
        :return: None
        """
        logging.error(f"[5G CU Monitor] WebSocket Error: {error}")

    def _on_close(self, ws, close_status_code, close_msg) -> None:
        """
        Callback when the websocket is closed

        :param ws: the websocket connection
        :param close_status_code: the status code
        :param close_msg: the closing msg from the connection
        :return: None
        """
        logging.warning(f"[5G CU Monitor] WebSocket Closed: {close_msg}")

    def _run_ws_client(self):
        """
        The blocking loop for the WebSocket client.
        Runs in a separate thread so it doesn't block the Kafka timer.

        :return: None
        """
        ws_url = f"ws://127.0.0.1:{self.cu_port}"

        while self.running:
            try:
                logging.info(f"[5G CU Monitor] Connecting WS to {ws_url}...")
                self.ws = websocket.WebSocketApp(
                    ws_url,
                    on_open=self._on_open,
                    on_message=self._on_message,
                    on_error=self._on_error,
                    on_close=self._on_close
                )
                self.ws.run_forever(ping_interval=30, ping_timeout=10)
            except Exception as e:
                logging.error(f"[5G CU Monitor] WS Connection failed: {e}")

            if self.running:
                time.sleep(5)  # Wait before reconnecting

    def run(self) -> None:
        """
        Main loop:
        1. Starts the WS client in background.
        2. Loops every `time_step_len_seconds` to push buffered metrics to Kafka.

        :return: None
        """
        logging.info("5G CU Monitor [Running]")
        self.ws_thread = threading.Thread(target=self._run_ws_client, daemon=True)
        self.ws_thread.start()

        while self.running:
            time.sleep(self.time_step_len_seconds)

            try:
                snapshot = {}
                with self.buffer_lock:
                    if not self.metrics_buffer:
                        continue
                    snapshot = self.metrics_buffer.copy()
                if "cu_cp" in snapshot:
                    record = snapshot["cu_cp"].to_kafka_record(ip=self.ip)
                    self.producer.produce(constants.KAFKA_CONFIG.FIVE_G_CU_CP_METRICS_TOPIC_NAME, record)
                if "app" in snapshot:
                    record = snapshot["app"].to_kafka_record(ip=self.ip)
                    self.producer.produce(constants.KAFKA_CONFIG.FIVE_G_CU_APP_RESOURCE_USAGE_METRICS_TOPIC_NAME,
                                          record)
                if "buffer" in snapshot:
                    record = snapshot["buffer"].to_kafka_record(ip=self.ip)
                    self.producer.produce(constants.KAFKA_CONFIG.FIVE_G_CU_BUFFER_POOL_METRICS_TOPIC_NAME, record)
                self.producer.poll(0)

            except Exception as e:
                logging.error(f"[5G CU Monitor] Error in reporting loop: {e}")

    def stop(self) -> None:
        """
        Stops the thread and closes the WebSocket
        :return: None
        """
        self.running = False
        if self.ws is not None:
            self.ws.close()
        self.producer.flush()
        logging.info("5G CU Monitor [Stopped]")
