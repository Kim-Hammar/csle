import time
import logging
import threading
import json
import websocket
from confluent_kafka import Producer
import csle_collector.constants.constants as constants
from csle_collector.five_g_du_manager.dao.du_metrics import DUMetrics
from csle_collector.five_g_du_manager.dao.cell_metrics import CellMetrics
from csle_collector.five_g_du_manager.dao.du_low_metrics import DULowMetrics
from csle_collector.five_g_du_manager.dao.rlc_metrics import RLCMetrics
from csle_collector.five_g_du_manager.dao.app_resource_usage_metrics import AppResourceUsageMetrics
from csle_collector.five_g_du_manager.dao.buffer_pool_metrics import BufferPoolMetrics


class DUMonitorThread(threading.Thread):
    """
    Thread that collects the 5G DU statistics via WebSockets and pushes them to Kafka.
    """

    def __init__(self, kafka_ip: str, kafka_port: int, ip: str, hostname: str,
                 du_port: int = 55555) -> None:
        """
        Initializes the thread

        :param kafka_ip: IP of the Kafka server to push to
        :param kafka_port: port of the Kafka server to push to
        :param ip: ip of the server we are pushing from (the DU IP)
        :param hostname: hostname of the server we are pushing from
        :param du_port: The WebSocket port configured in du.yml (default 55555)
        """
        threading.Thread.__init__(self)
        self.kafka_ip = kafka_ip
        self.kafka_port = kafka_port
        self.ip = ip
        self.hostname = hostname
        self.du_port = du_port
        self.conf = {
            constants.KAFKA.BOOTSTRAP_SERVERS_PROPERTY: f"{self.kafka_ip}:{self.kafka_port}",
            constants.KAFKA.CLIENT_ID_PROPERTY: self.hostname
        }
        self.producer = Producer(**self.conf)
        self.running = True
        self.ws = None

        logging.info(f"DU Monitor thread initialized. Target DU: {self.ip}:{self.du_port}")

    def _on_open(self, ws):
        """
        Callback when WebSocket connection is opened.
        Sends the subscription command immediately.
        """
        logging.info(f"[DU Monitor] Connected to {self.ip}. Sending subscription...")
        ws.send(json.dumps({"cmd": "metrics_subscribe"}))

    def _on_message(self, ws, message):
        """
        Callback when a message is received from the DU.
        Parses JSON, converts to DTO, and pushes to Kafka.
        """
        try:
            data = json.loads(message)

            # Skip command responses (e.g. confirmation of subscription)
            if "cmd" in data:
                return

            # 1. Cell Metrics
            if "cells" in data:
                dto = CellMetrics.from_ws_dict(data, ip=self.ip)
                dto.ip = self.ip
                record = dto.to_kafka_record(ip=self.ip)
                self.producer.produce(constants.KAFKA_CONFIG.CELL_METRICS_TOPIC_NAME, record)

            # 2. DU High Metrics (Latency/CPU)
            elif "du" in data:
                dto = DUMetrics.from_ws_dict(data, ip=self.ip)
                dto.ip = self.ip
                record = dto.to_kafka_record(ip=self.ip)
                self.producer.produce(constants.KAFKA_CONFIG.DU_METRICS_TOPIC_NAME, record)

            # 3. DU Low Metrics (PHY)
            elif "du_low" in data:
                dto = DULowMetrics.from_ws_dict(data, ip=self.ip)
                dto.ip = self.ip
                record = dto.to_kafka_record(ip=self.ip)
                self.producer.produce(constants.KAFKA_CONFIG.DU_LOW_METRICS_TOPIC_NAME, record)

            # 4. RLC Metrics
            elif "rlc_metrics" in data:
                dto = RLCMetrics.from_ws_dict(data, ip=self.ip)
                dto.ip = self.ip
                record = dto.to_kafka_record(ip=self.ip)
                self.producer.produce(constants.KAFKA_CONFIG.RLC_METRICS_TOPIC_NAME, record)

            # 5. App Resource Usage
            elif "app_resource_usage" in data:
                dto = AppResourceUsageMetrics.from_ws_dict(data, ip=self.ip)
                dto.ip = self.ip
                record = dto.to_kafka_record(ip=self.ip)
                self.producer.produce(constants.KAFKA_CONFIG.APP_RESOURCE_USAGE_METRICS_TOPIC_NAME, record)

            # 6. Buffer Pool
            elif "buffer_pool" in data:
                dto = BufferPoolMetrics.from_ws_dict(data, ip=self.ip)
                dto.ip = self.ip
                record = dto.to_kafka_record(ip=self.ip)
                self.producer.produce(constants.KAFKA_CONFIG.BUFFER_POOL_METRICS_TOPIC_NAME, record)

            # Flush periodically to ensure data is sent
            self.producer.poll(0)

        except json.JSONDecodeError:
            logging.error(f"[DU Monitor] Received non-JSON message: {message}")
        except Exception as e:
            logging.error(f"[DU Monitor] Error processing message: {e}")

    def _on_error(self, ws, error):
        logging.error(f"[DU Monitor] WebSocket Error: {error}")

    def _on_close(self, ws, close_status_code, close_msg):
        logging.warning(f"[DU Monitor] WebSocket Closed: {close_msg} ({close_status_code})")

    def run(self) -> None:
        """
        Main loop of the thread. Starts the WebSocket client loop.
        """
        logging.info("DU Monitor [Running]")

        ws_url = f"ws://127.0.0.1:{self.du_port}"

        while self.running:
            try:
                # Initialize WebSocket App
                self.ws = websocket.WebSocketApp(
                    ws_url,
                    on_open=self._on_open,
                    on_message=self._on_message,
                    on_error=self._on_error,
                    on_close=self._on_close
                )

                # Run the blocking loop
                # ping_interval keeps connection alive through silence
                self.ws.run_forever(ping_interval=30, ping_timeout=10)

            except Exception as e:
                logging.error(f"[DU Monitor] Connection failed: {e}")

            if self.running:
                logging.info("[DU Monitor] Reconnecting in 5 seconds...")
                time.sleep(5)

    def stop(self) -> None:
        """
        Stops the thread and closes the WebSocket
        """
        self.running = False
        if self.ws:
            self.ws.close()
        self.producer.flush()
        logging.info("DU Monitor [Stopped]")