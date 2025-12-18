import time
import logging
import threading
from confluent_kafka import Producer
from csle_collector.five_g_du_manager.five_g_du_manager_util import FiveGDUManagerUtil
import csle_collector.constants.constants as constants


class DUMonitorThread(threading.Thread):
    """
    Thread that collects the 5G DU statistics and pushes it to Kafka periodically
    """

    def __init__(self, kafka_ip: str, kafka_port: int, ip: str, hostname: str, time_step_len_seconds: int) -> None:
        """
        Initializes the thread

        :param kafka_ip: IP of the Kafka server to push to
        :param kafka_port: port of the Kafka server to push to
        :param ip: ip of the server we are pushing from
        :param hostname: hostname of the server we are pushing from
        :param time_step_len_seconds: the length of a timestep
        """
        threading.Thread.__init__(self)
        self.kafka_ip = kafka_ip
        self.kafka_port = kafka_port
        self.ip = ip
        self.hostname = hostname
        self.latest_ts = time.time()
        self.time_step_len_seconds = time_step_len_seconds
        self.conf = {
            constants.KAFKA.BOOTSTRAP_SERVERS_PROPERTY: f"{self.kafka_ip}:{self.kafka_port}",
            constants.KAFKA.CLIENT_ID_PROPERTY: self.hostname}
        self.producer = Producer(**self.conf)
        self.running = True
        logging.info("DU Monitor thread started successfully")

    def run(self) -> None:
        """
        Main loop of the thread. Parses 5G CU metrics and pushes it to Kafka periodically

        :return: None
        """
        logging.info("DU Monitor [Running]")
        while self.running:
            time.sleep(self.time_step_len_seconds)
            try:
                du_metrics = FiveGDUManagerUtil.fetch_du_metrics(ip=self.ip)
                record = du_metrics.to_kafka_record(ip=self.ip)
                self.producer.produce(constants.KAFKA_CONFIG.AMF_METRICS_TOPIC_NAME, record)
                self.producer.poll(0)
            except Exception as e:
                logging.info(f"[DU monitor thread], "
                             f"There was an exception reading 5G DU metrics and producing to kafka: "
                             f"{str(e)}, {repr(e)}")
