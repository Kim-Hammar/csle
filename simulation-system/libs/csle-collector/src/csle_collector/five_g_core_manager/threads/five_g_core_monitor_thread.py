import time
import logging
import threading
from confluent_kafka import Producer
from csle_collector.five_g_core_manager.five_g_core_manager_util import FiveGCoreManagerUtil
import csle_collector.constants.constants as constants


class FiveGCoreMonitorThread(threading.Thread):
    """
    Thread that collects the 5G core statistics and pushes it to Kafka periodically
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
        logging.info("5G CoreMonitor thread started successfully")

    def run(self) -> None:
        """
        Main loop of the thread. Parses 5G core metrics and pushes it to Kafka periodically

        :return: None
        """
        logging.info("5G CoreMonitor [Running]")
        while self.running:
            time.sleep(self.time_step_len_seconds)
            try:
                amf_metrics = FiveGCoreManagerUtil.fetch_amf_metrics(ip=self.ip)
                record = amf_metrics.to_kafka_record(ip=self.ip)
                self.producer.produce(constants.KAFKA_CONFIG.FIVE_G_CORE_AMF_METRICS_TOPIC_NAME, record)
                self.producer.poll(0)
                upf_metrics = FiveGCoreManagerUtil.fetch_upf_metrics(ip=self.ip)
                record = upf_metrics.to_kafka_record(ip=self.ip)
                self.producer.produce(constants.KAFKA_CONFIG.FIVE_G_CORE_UPF_METRICS_TOPIC_NAME, record)
                self.producer.poll(0)
                mme_metrics = FiveGCoreManagerUtil.fetch_mme_metrics(ip=self.ip)
                record = mme_metrics.to_kafka_record(ip=self.ip)
                self.producer.produce(constants.KAFKA_CONFIG.FIVE_G_CORE_MME_METRICS_TOPIC_NAME, record)
                self.producer.poll(0)
                smf_metrics = FiveGCoreManagerUtil.fetch_smf_metrics(ip=self.ip)
                record = smf_metrics.to_kafka_record(ip=self.ip)
                self.producer.produce(constants.KAFKA_CONFIG.FIVE_G_CORE_SMF_METRICS_TOPIC_NAME, record)
                self.producer.poll(0)
                hss_metrics = FiveGCoreManagerUtil.fetch_hss_metrics(ip=self.ip)
                record = hss_metrics.to_kafka_record(ip=self.ip)
                self.producer.produce(constants.KAFKA_CONFIG.FIVE_G_CORE_HSS_METRICS_TOPIC_NAME, record)
                self.producer.poll(0)
                pcrf_metrics = FiveGCoreManagerUtil.fetch_pcrf_metrics(ip=self.ip)
                record = pcrf_metrics.to_kafka_record(ip=self.ip)
                self.producer.produce(constants.KAFKA_CONFIG.FIVE_G_CORE_PCRF_METRICS_TOPIC_NAME, record)
                self.producer.poll(0)
                pcf_metrics = FiveGCoreManagerUtil.fetch_pcf_metrics(ip=self.ip)
                record = pcf_metrics.to_kafka_record(ip=self.ip)
                self.producer.produce(constants.KAFKA_CONFIG.FIVE_G_CORE_PCF_METRICS_TOPIC_NAME, record)
                self.producer.poll(0)
            except Exception as e:
                logging.info(f"[5G Core monitor thread], "
                             f"There was an exception reading 5G core metrics and producing to kafka: "
                             f"{str(e)}, {repr(e)}")
