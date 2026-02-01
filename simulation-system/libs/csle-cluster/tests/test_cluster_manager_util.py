from csle_cluster.cluster_manager.cluster_manager_util import ClusterManagerUtil
import csle_cluster.cluster_manager.cluster_manager_pb2 as cluster_manager_pb2
import csle_collector.traffic_manager.traffic_manager_pb2 as traffic_manager_pb2
import csle_collector.client_manager.client_manager_pb2 as client_manager_pb2


class TestClusterManagerUtilSuite:
    """
    Test suite for ClusterManagerUtil
    """

    def test_convert_traffic_dto_to_traffic_manager_info_dto(self) -> None:
        """
        Tests the convert_traffic_dto_to_traffic_manager_info_dto function
        """
        # Test with None
        result = ClusterManagerUtil.convert_traffic_dto_to_traffic_manager_info_dto(None)
        assert result.running is False
        assert result.script == ""

        # Test with valid DTO
        traffic_dto = traffic_manager_pb2.TrafficDTO(running=True, script="test_script")
        result = ClusterManagerUtil.convert_traffic_dto_to_traffic_manager_info_dto(traffic_dto)
        assert result.running is True
        assert result.script == "test_script"

    def test_convert_traffic_dto_to_traffic_manager_info_dto_reverse(self) -> None:
        """
        Tests the convert_traffic_dto_to_traffic_manager_info_dto_reverse function
        """
        # Test with None
        result = ClusterManagerUtil.convert_traffic_dto_to_traffic_manager_info_dto_reverse(None)
        assert result.running is False
        assert result.script == ""

        # Test with valid DTO
        info_dto = cluster_manager_pb2.TrafficManagerInfoDTO(running=True, script="test_script")
        result = ClusterManagerUtil.convert_traffic_dto_to_traffic_manager_info_dto_reverse(info_dto)
        assert result.running is True
        assert result.script == "test_script"

    def test_get_empty_traffic_manager_info_dto(self) -> None:
        """
        Tests the get_empty_traffic_manager_info_dto function
        """
        result = ClusterManagerUtil.get_empty_traffic_manager_info_dto()
        assert result.running is False
        assert result.script == ""

    def test_get_empty_traffic_managers_info_dto(self) -> None:
        """
        Tests the get_empty_traffic_managers_info_dto function
        """
        result = ClusterManagerUtil.get_empty_traffic_managers_info_dto()
        assert len(result.ips) == 0
        assert result.executionId == -1

    def test_get_empty_client_managers_info_dto(self) -> None:
        """
        Tests the get_empty_client_managers_info_dto function
        """
        result = ClusterManagerUtil.get_empty_client_managers_info_dto()
        assert len(result.ips) == 0
        assert result.executionId == -1

    def test_get_empty_get_num_clients_dto(self) -> None:
        """
        Tests the get_empty_get_num_clients_dto function
        """
        result = ClusterManagerUtil.get_empty_get_num_clients_dto()
        assert result.num_clients == 0
        assert result.client_process_active is False
        assert result.producer_active is False

    def test_convert_client_dto_to_get_num_clients_dto(self) -> None:
        """
        Tests the convert_client_dto_to_get_num_clients_dto function
        """
        clients_dto = client_manager_pb2.ClientsDTO(
            num_clients=10, client_process_active=True, producer_active=True,
            clients_time_step_len_seconds=5, producer_time_step_len_seconds=5
        )
        result = ClusterManagerUtil.convert_client_dto_to_get_num_clients_dto(clients_dto)
        assert result.num_clients == 10
        assert result.client_process_active is True
        assert result.producer_active is True

    def test_convert_client_dto_to_get_num_clients_dto_reverse(self) -> None:
        """
        Tests the convert_client_dto_to_get_num_clients_dto_reverse function
        """
        get_num_clients_dto = cluster_manager_pb2.GetNumClientsDTO(
            num_clients=5, client_process_active=True, producer_active=True
        )
        result = ClusterManagerUtil.convert_client_dto_to_get_num_clients_dto_reverse(get_num_clients_dto)
        assert result.num_clients == 5
        assert result.client_process_active is True
        assert result.producer_active is True

    def test_node_status_dto_to_dict(self) -> None:
        """
        Tests the node_status_dto_to_dict function
        """
        node_status_dto = cluster_manager_pb2.NodeStatusDTO(
            ip="192.168.1.1", leader=True, cAdvisorRunning=True,
            prometheusRunning=True, grafanaRunning=True, pgAdminRunning=True,
            nginxRunning=True, flaskRunning=True, dockerStatsManagerRunning=True,
            nodeExporterRunning=True, postgreSQLRunning=True, dockerEngineRunning=True
        )
        d = ClusterManagerUtil.node_status_dto_to_dict(node_status_dto)
        assert d["ip"] == "192.168.1.1"
        assert d["leader"] is True
        assert d["cAdvisorRunning"] is True

    def test_service_status_dto_to_dict(self) -> None:
        """
        Tests the service_status_dto_to_dict function
        """
        service_status_dto = cluster_manager_pb2.ServiceStatusDTO(
            running=True
        )
        d = ClusterManagerUtil.service_status_dto_to_dict(service_status_dto)
        assert d["running"] is True

    def test_logs_dto_to_dict(self) -> None:
        """
        Tests the logs_dto_to_dict function
        """
        logs_dto = cluster_manager_pb2.LogsDTO(logs=["log1", "log2"])
        d = ClusterManagerUtil.logs_dto_to_dict(logs_dto)
        assert d["logs"] == ["log1", "log2"]

    def test_get_num_clients_dto_to_dict(self) -> None:
        """
        Tests the get_num_clients_dto_to_dict function
        """
        get_num_clients_dto = cluster_manager_pb2.GetNumClientsDTO(
            num_clients=10, client_process_active=True, producer_active=True,
            clients_time_step_len_seconds=5, producer_time_step_len_seconds=6
        )
        d = ClusterManagerUtil.get_num_clients_dto_to_dict(get_num_clients_dto)
        assert d["num_clients"] == 10
        assert d["client_process_active"] is True
        assert d["producer_active"] is True
        assert d["clients_time_step_len_seconds"] == 5
        assert d["producer_time_step_len_seconds"] == 6

    def test_client_managers_info_dto_to_dict(self) -> None:
        """
        Tests the client_managers_info_dto_to_dict function
        """
        status = cluster_manager_pb2.GetNumClientsDTO(num_clients=5, client_process_active=True)
        dto = cluster_manager_pb2.ClientManagersInfoDTO(
            ips=["192.168.1.1"], ports=[5000], emulationName="test_em", executionId=1,
            clientManagersRunning=[True], clientManagersStatuses=[status]
        )
        d = ClusterManagerUtil.client_managers_info_dto_to_dict(dto)
        assert d["ips"] == ["192.168.1.1"]
        assert d["emulationName"] == "test_em"
        assert d["clientManagersStatuses"][0]["num_clients"] == 5

    def test_traffic_manager_info_dto_to_dict(self) -> None:
        """
        Tests the traffic_manager_info_dto_to_dict function
        """
        dto = cluster_manager_pb2.TrafficManagerInfoDTO(running=True, script="test.sh")
        d = ClusterManagerUtil.traffic_manager_info_dto_to_dict(dto)
        assert d["running"] is True
        assert d["script"] == "test.sh"

    def test_traffic_managers_info_dto_to_dict(self) -> None:
        """
        Tests the traffic_managers_info_dto_to_dict function
        """
        status = cluster_manager_pb2.TrafficManagerInfoDTO(running=True, script="test.sh")
        dto = cluster_manager_pb2.TrafficManagersInfoDTO(
            ips=["192.168.1.1"], ports=[5000], trafficManagersRunning=[True],
            trafficManagersStatuses=[status], emulationName="test_em", executionId=1
        )
        d = ClusterManagerUtil.traffic_managers_info_dto_to_dict(dto)
        assert d["ips"] == ["192.168.1.1"]
        assert d["trafficManagersStatuses"][0]["running"] is True
        assert d["emulationName"] == "test_em"

    def test_docker_stats_monitor_status_dto_to_dict(self) -> None:
        """
        Tests the docker_stats_monitor_status_dto_to_dict function
        """
        dto = cluster_manager_pb2.DockerStatsMonitorStatusDTO(
            num_monitors=2, emulations=["em1", "em2"], emulation_executions=[1, 2]
        )
        d = ClusterManagerUtil.docker_stats_monitor_status_dto_to_dict(dto)
        assert d["num_monitors"] == 2
        assert d["emulations"] == ["em1", "em2"]
        assert d["emulation_executions"] == [1, 2]

    def test_elk_status_dto_to_dict(self) -> None:
        """
        Tests the elk_status_dto_to_dict function
        """
        dto = cluster_manager_pb2.ElkStatusDTO(
            elasticRunning=True, kibanaRunning=True, logstashRunning=True
        )
        d = ClusterManagerUtil.elk_status_dto_to_dict(dto)
        assert d["elasticRunning"] is True
        assert d["kibanaRunning"] is True
        assert d["logstashRunning"] is True

    def test_snort_ids_status_dto_to_dict(self) -> None:
        """
        Tests the snort_ids_status_dto_to_dict function
        """
        dto = cluster_manager_pb2.SnortIdsStatusDTO(
            snort_ids_running=True, monitor_running=True
        )
        d = ClusterManagerUtil.snort_ids_status_dto_to_dict(dto)
        assert d["snort_ids_running"] is True
        assert d["monitor_running"] is True

    def test_ossec_ids_status_dto_to_dict(self) -> None:
        """
        Tests the ossec_ids_status_dto_to_dict function
        """
        dto = cluster_manager_pb2.OSSECIdsStatusDTO(
            ossec_ids_running=True, monitor_running=True
        )
        d = ClusterManagerUtil.ossec_ids_status_dto_to_dict(dto)
        assert d["ossec_ids_running"] is True
        assert d["monitor_running"] is True

    def test_kafka_status_dto_to_dict(self) -> None:
        """
        Tests the kafka_status_dto_to_dict function
        """
        dto = cluster_manager_pb2.KafkaStatusDTO(
            running=True, topics=["topic1"]
        )
        d = ClusterManagerUtil.kafka_status_dto_to_dict(dto)
        assert d["running"] is True
        assert d["topics"] == ["topic1"]

    def test_ryu_manager_status_dto_to_dict(self) -> None:
        """
        Tests the ryu_manager_status_dto_to_dict function
        """
        dto = cluster_manager_pb2.RyuManagerStatusDTO(
            ryu_running=True, monitor_running=True, port=8080, web_port=8081,
            controller="ryu", kafka_ip="127.0.0.1", kafka_port=9092, time_step_len=15
        )
        d = ClusterManagerUtil.ryu_manager_status_dto_to_dict(dto)
        assert d["ryu_running"] is True
        assert d["monitor_running"] is True
        assert d["port"] == 8080
        assert d["web_port"] == 8081
        assert d["controller"] == "ryu"
        assert d["kafka_ip"] == "127.0.0.1"
        assert d["kafka_port"] == 9092
        assert d["time_step_len"] == 15

    def test_host_manager_status_dto_to_dict(self) -> None:
        """
        Tests the host_manager_status_dto_to_dict function
        """
        dto = cluster_manager_pb2.HostManagerStatusDTO(
            monitor_running=True, filebeat_running=True, packetbeat_running=True,
            metricbeat_running=True, heartbeat_running=True
        )
        d = ClusterManagerUtil.host_manager_status_dto_to_dict(dto)
        assert d["monitor_running"] is True
        assert d["filebeat_running"] is True
        assert d["packetbeat_running"] is True
        assert d["metricbeat_running"] is True
        assert d["heartbeat_running"] is True

    def test_snort_ids_monitor_thread_statuses_dto_to_dict(self) -> None:
        """
        Tests the snort_ids_monitor_thread_statuses_dto_to_dict function
        """
        status = cluster_manager_pb2.SnortIdsStatusDTO(snort_ids_running=True, monitor_running=True)
        dto = cluster_manager_pb2.SnortIdsMonitorThreadStatusesDTO(snortIDSStatuses=[status])
        d = ClusterManagerUtil.snort_ids_monitor_thread_statuses_dto_to_dict(dto)
        assert d["snortIDSStatuses"][0]["snort_ids_running"] is True

    def test_ossec_ids_monitor_thread_statuses_dto_to_dict(self) -> None:
        """
        Tests the ossec_ids_monitor_thread_statuses_dto_to_dict function
        """
        status = cluster_manager_pb2.OSSECIdsStatusDTO(ossec_ids_running=True, monitor_running=True)
        dto = cluster_manager_pb2.OSSECIdsMonitorThreadStatusesDTO(ossecIDSStatuses=[status])
        d = ClusterManagerUtil.ossec_ids_monitor_thread_statuses_dto_to_dict(dto)
        assert d["ossecIDSStatuses"][0]["ossec_ids_running"] is True
