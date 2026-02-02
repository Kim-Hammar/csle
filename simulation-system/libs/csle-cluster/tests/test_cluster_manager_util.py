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

    def test_container_image_dto_to_dict(self) -> None:
        """
        Tests the container_image_dto_to_dict function

        :return: None
        """
        dto = cluster_manager_pb2.ContainerImageDTO(
            repoTags="csle/base:latest",
            created="2024-01-01",
            os="linux",
            architecture="amd64",
            size=1024000
        )
        d = ClusterManagerUtil.container_image_dto_to_dict(dto)
        assert d["repoTags"] == "csle/base:latest"
        assert d["created"] == "2024-01-01"
        assert d["os"] == "linux"
        assert d["architecture"] == "amd64"
        assert d["size"] == 1024000

    def test_container_images_dtos_to_dict(self) -> None:
        """
        Tests the container_images_dtos_to_dict function

        :return: None
        """
        image1 = cluster_manager_pb2.ContainerImageDTO(
            repoTags="csle/base:latest", created="2024-01-01", os="linux",
            architecture="amd64", size=1024000
        )
        image2 = cluster_manager_pb2.ContainerImageDTO(
            repoTags="csle/attacker:latest", created="2024-01-02", os="linux",
            architecture="amd64", size=2048000
        )
        dto = cluster_manager_pb2.ContainerImagesDTO(images=[image1, image2])
        d = ClusterManagerUtil.container_images_dtos_to_dict(dto)
        assert len(d["images"]) == 2
        assert d["images"][0]["repoTags"] == "csle/base:latest"
        assert d["images"][1]["repoTags"] == "csle/attacker:latest"

    def test_docker_networks_dto_to_dict(self) -> None:
        """
        Tests the docker_networks_dto_to_dict function

        :return: None
        """
        dto = cluster_manager_pb2.DockerNetworksDTO(networks=["bridge", "host", "csle_net"])
        d = ClusterManagerUtil.docker_networks_dto_to_dict(dto)
        assert d["networks"] == ["bridge", "host", "csle_net"]

    def test_running_containers_dto_to_dict(self) -> None:
        """
        Tests the running_containers_dto_to_dict function

        :return: None
        """
        container = cluster_manager_pb2.DockerContainerDTO(
            name="test_container", image="csle/base:latest", ip="192.168.1.10"
        )
        dto = cluster_manager_pb2.RunningContainersDTO(runningContainers=[container])
        d = ClusterManagerUtil.running_containers_dto_to_dict(dto)
        assert len(d["runningContainers"]) == 1
        assert d["runningContainers"][0]["name"] == "test_container"

    def test_stopped_containers_dto_to_dict(self) -> None:
        """
        Tests the stopped_containers_dto_to_dict function

        :return: None
        """
        container = cluster_manager_pb2.DockerContainerDTO(
            name="stopped_container", image="csle/base:latest", ip=""
        )
        dto = cluster_manager_pb2.StoppedContainersDTO(stoppedContainers=[container])
        d = ClusterManagerUtil.stopped_containers_dto_to_dict(dto)
        assert len(d["stoppedContainers"]) == 1
        assert d["stoppedContainers"][0]["name"] == "stopped_container"

    def test_docker_container_dto_to_dict(self) -> None:
        """
        Tests the docker_container_dto_to_dict function

        :return: None
        """
        dto = cluster_manager_pb2.DockerContainerDTO(
            name="my_container", image="csle/attacker:latest", ip="10.0.0.5"
        )
        d = ClusterManagerUtil.docker_container_dto_to_dict(dto)
        assert d["name"] == "my_container"
        assert d["image"] == "csle/attacker:latest"
        assert d["ip"] == "10.0.0.5"

    def test_running_emulations_dto_to_dict(self) -> None:
        """
        Tests the running_emulations_dto_to_dict function

        :return: None
        """
        dto = cluster_manager_pb2.RunningEmulationsDTO(
            runningEmulations=["emulation1", "emulation2"]
        )
        d = ClusterManagerUtil.running_emulations_dto_to_dict(dto)
        assert d["runningEmulations"] == ["emulation1", "emulation2"]

    def test_get_empty_kafka_dto(self) -> None:
        """
        Tests the get_empty_kafka_dto function

        :return: None
        """
        result = ClusterManagerUtil.get_empty_kafka_dto()
        assert result.running is False
        assert len(result.topics) == 0

    def test_get_empty_ryu_manager_status_dto(self) -> None:
        """
        Tests the get_empty_ryu_manager_status_dto function

        :return: None
        """
        result = ClusterManagerUtil.get_empty_ryu_manager_status_dto()
        assert result.ryu_running is False
        assert result.monitor_running is False
        assert result.port == -1
        assert result.web_port == -1

    def test_get_empty_docker_stats_monitor_status_dto(self) -> None:
        """
        Tests the get_empty_docker_stats_monitor_status_dto function

        :return: None
        """
        result = ClusterManagerUtil.get_empty_docker_stats_monitor_status_dto()
        assert result.num_monitors == 0
        assert len(result.emulations) == 0
        assert len(result.emulation_executions) == 0

    def test_get_empty_elk_status_dto(self) -> None:
        """
        Tests the get_empty_elk_status_dto function

        :return: None
        """
        result = ClusterManagerUtil.get_empty_elk_status_dto()
        assert result.elasticRunning is False
        assert result.kibanaRunning is False
        assert result.logstashRunning is False

    def test_get_empty_snort_ids_status_dto(self) -> None:
        """
        Tests the get_empty_snort_ids_status_dto function

        :return: None
        """
        result = ClusterManagerUtil.get_empty_snort_ids_status_dto()
        assert result.snort_ids_running is False
        assert result.monitor_running is False

    def test_get_empty_ossec_ids_status_dto(self) -> None:
        """
        Tests the get_empty_ossec_ids_status_dto function

        :return: None
        """
        result = ClusterManagerUtil.get_empty_ossec_ids_status_dto()
        assert result.ossec_ids_running is False
        assert result.monitor_running is False

    def test_get_empty_host_manager_status_dto(self) -> None:
        """
        Tests the get_empty_host_manager_status_dto function

        :return: None
        """
        result = ClusterManagerUtil.get_empty_host_manager_status_dto()
        assert result.monitor_running is False
        assert result.filebeat_running is False
        assert result.packetbeat_running is False
        assert result.metricbeat_running is False
        assert result.heartbeat_running is False

    def test_get_empty_kibana_tunnel_dto(self) -> None:
        """
        Tests the get_empty_kibana_tunnel_dto function

        :return: None
        """
        result = ClusterManagerUtil.get_empty_kibana_tunnel_dto()
        assert result.ip == ""
        assert result.port == 1
        assert result.emulation == ""
        assert result.ipFirstOctet == -1

    def test_get_empty_kibana_tunnels_dto(self) -> None:
        """
        Tests the get_empty_kibana_tunnels_dto function

        :return: None
        """
        result = ClusterManagerUtil.get_empty_kibana_tunnels_dto()
        assert len(result.tunnels) == 0

    def test_kibana_tunnel_dto_to_dict(self) -> None:
        """
        Tests the kibana_tunnel_dto_to_dict function

        :return: None
        """
        dto = cluster_manager_pb2.KibanaTunnelDTO(
            ip="192.168.1.100", port=5601, emulation="test_em", ipFirstOctet=1
        )
        d = ClusterManagerUtil.kibana_tunnel_dto_to_dict(dto)
        assert d["ip"] == "192.168.1.100"
        assert d["port"] == 5601
        assert d["emulation"] == "test_em"
        assert d["ipFirstOctet"] == 1

    def test_kibana_tunnels_dto_to_dict(self) -> None:
        """
        Tests the kibana_tunnels_dto_to_dict function

        :return: None
        """
        tunnel = cluster_manager_pb2.KibanaTunnelDTO(
            ip="192.168.1.100", port=5601, emulation="test_em", ipFirstOctet=1
        )
        dto = cluster_manager_pb2.KibanaTunnelsDTO(tunnels=[tunnel])
        d = ClusterManagerUtil.kibana_tunnels_dto_to_dict(dto)
        assert len(d["tunnels"]) == 1
        assert d["tunnels"][0]["ip"] == "192.168.1.100"

    def test_get_empty_ryu_tunnel_dto(self) -> None:
        """
        Tests the get_empty_ryu_tunnel_dto function

        :return: None
        """
        result = ClusterManagerUtil.get_empty_ryu_tunnel_dto()
        assert result.ip == ""
        assert result.port == 1
        assert result.emulation == ""
        assert result.ipFirstOctet == -1

    def test_get_empty_ryu_tunnels_dto(self) -> None:
        """
        Tests the get_empty_ryu_tunnels_dto function

        :return: None
        """
        result = ClusterManagerUtil.get_empty_ryu_tunnels_dto()
        assert len(result.tunnels) == 0

    def test_ryu_tunnel_dto_to_dict(self) -> None:
        """
        Tests the ryu_tunnel_dto_to_dict function

        :return: None
        """
        dto = cluster_manager_pb2.RyuTunnelDTO(
            ip="192.168.1.101", port=8080, emulation="ryu_em", ipFirstOctet=2
        )
        d = ClusterManagerUtil.ryu_tunnel_dto_to_dict(dto)
        assert d["ip"] == "192.168.1.101"
        assert d["port"] == 8080
        assert d["emulation"] == "ryu_em"
        assert d["ipFirstOctet"] == 2

    def test_ryu_tunnels_dto_to_dict(self) -> None:
        """
        Tests the ryu_tunnels_dto_to_dict function

        :return: None
        """
        tunnel = cluster_manager_pb2.RyuTunnelDTO(
            ip="192.168.1.101", port=8080, emulation="ryu_em", ipFirstOctet=2
        )
        dto = cluster_manager_pb2.RyuTunnelsDTO(tunnels=[tunnel])
        d = ClusterManagerUtil.ryu_tunnels_dto_to_dict(dto)
        assert len(d["tunnels"]) == 1
        assert d["tunnels"][0]["port"] == 8080

    def test_get_empty_five_g_core_tunnel_dto(self) -> None:
        """
        Tests the get_empty_five_g_core_tunnel_dto function

        :return: None
        """
        result = ClusterManagerUtil.get_empty_five_g_core_tunnel_dto()
        assert result.ip == ""
        assert result.port == 1
        assert result.emulation == ""
        assert result.ipFirstOctet == -1

    def test_get_empty_five_g_core_tunnels_dto(self) -> None:
        """
        Tests the get_empty_five_g_core_tunnels_dto function

        :return: None
        """
        result = ClusterManagerUtil.get_empty_five_g_core_tunnels_dto()
        assert len(result.tunnels) == 0

    def test_five_g_core_tunnel_dto_to_dict(self) -> None:
        """
        Tests the five_g_core_tunnel_dto_to_dict function

        :return: None
        """
        dto = cluster_manager_pb2.FiveGCoreTunnelDTO(
            ip="192.168.1.102", port=9999, emulation="5g_em", ipFirstOctet=3
        )
        d = ClusterManagerUtil.five_g_core_tunnel_dto_to_dict(dto)
        assert d["ip"] == "192.168.1.102"
        assert d["port"] == 9999
        assert d["emulation"] == "5g_em"
        assert d["ipFirstOctet"] == 3

    def test_five_g_core_tunnels_dto_to_dict(self) -> None:
        """
        Tests the five_g_core_tunnels_dto_to_dict function

        :return: None
        """
        tunnel = cluster_manager_pb2.FiveGCoreTunnelDTO(
            ip="192.168.1.102", port=9999, emulation="5g_em", ipFirstOctet=3
        )
        dto = cluster_manager_pb2.FiveGCoreTunnelsDTO(tunnels=[tunnel])
        d = ClusterManagerUtil.five_g_core_tunnels_dto_to_dict(dto)
        assert len(d["tunnels"]) == 1
        assert d["tunnels"][0]["emulation"] == "5g_em"

    def test_docker_stats_managers_info_dto_to_dict(self) -> None:
        """
        Tests the docker_stats_managers_info_dto_to_dict function

        :return: None
        """
        status = cluster_manager_pb2.DockerStatsMonitorStatusDTO(
            num_monitors=1, emulations=["em1"], emulation_executions=[1]
        )
        dto = cluster_manager_pb2.DockerStatsManagersInfoDTO(
            ips=["192.168.1.1"], ports=[50051], emulationName="test_em", executionId=1,
            dockerStatsManagersRunning=[True], dockerStatsManagersStatuses=[status]
        )
        d = ClusterManagerUtil.docker_stats_managers_info_dto_to_dict(dto)
        assert d["ips"] == ["192.168.1.1"]
        assert d["ports"] == [50051]
        assert d["emulationName"] == "test_em"
        assert d["executionId"] == 1
        assert d["dockerStatsManagersRunning"] == [True]

    def test_elk_managers_info_dto_to_dict(self) -> None:
        """
        Tests the elk_managers_info_dto_to_dict function

        :return: None
        """
        status = cluster_manager_pb2.ElkStatusDTO(
            elasticRunning=True, kibanaRunning=True, logstashRunning=False
        )
        dto = cluster_manager_pb2.ElkManagersInfoDTO(
            ips=["192.168.1.5"], ports=[9200], emulationName="elk_em", executionId=5,
            elkManagersRunning=[True], elkManagersStatuses=[status],
            localKibanaPort=5601
        )
        d = ClusterManagerUtil.elk_managers_info_dto_to_dict(dto)
        assert d["ips"] == ["192.168.1.5"]
        assert d["emulationName"] == "elk_em"
        assert d["localKibanaPort"] == 5601
        assert d["elkManagersStatuses"][0]["elasticRunning"] is True

    def test_snort_managers_info_dto_to_dict(self) -> None:
        """
        Tests the snort_managers_info_dto_to_dict function

        :return: None
        """
        status = cluster_manager_pb2.SnortIdsStatusDTO(
            snort_ids_running=True, monitor_running=True
        )
        dto = cluster_manager_pb2.SnortIdsManagersInfoDTO(
            ips=["192.168.1.6"], ports=[50052], emulationName="snort_em", executionId=6,
            snortIdsManagersRunning=[True], snortIdsManagersStatuses=[status]
        )
        d = ClusterManagerUtil.snort_managers_info_dto_to_dict(dto)
        assert d["ips"] == ["192.168.1.6"]
        assert d["emulationName"] == "snort_em"
        assert d["snortIdsManagersStatuses"][0]["snort_ids_running"] is True

    def test_ossec_managers_info_dto_to_dict(self) -> None:
        """
        Tests the ossec_managers_info_dto_to_dict function

        :return: None
        """
        status = cluster_manager_pb2.OSSECIdsStatusDTO(
            ossec_ids_running=True, monitor_running=False
        )
        dto = cluster_manager_pb2.OSSECIdsManagersInfoDTO(
            ips=["192.168.1.7"], ports=[50053], emulationName="ossec_em", executionId=7,
            ossecIdsManagersRunning=[True], ossecIdsManagersStatuses=[status]
        )
        d = ClusterManagerUtil.ossec_managers_info_dto_to_dict(dto)
        assert d["ips"] == ["192.168.1.7"]
        assert d["emulationName"] == "ossec_em"
        assert d["ossecIdsManagersStatuses"][0]["ossec_ids_running"] is True

    def test_kafka_managers_info_dto_to_dict(self) -> None:
        """
        Tests the kafka_managers_info_dto_to_dict function

        :return: None
        """
        status = cluster_manager_pb2.KafkaStatusDTO(
            running=True, topics=["topic1", "topic2"]
        )
        dto = cluster_manager_pb2.KafkaManagersInfoDTO(
            ips=["192.168.1.8"], ports=[9092], emulationName="kafka_em", executionId=8,
            kafkaManagersRunning=[True], kafkaManagersStatuses=[status]
        )
        d = ClusterManagerUtil.kafka_managers_info_dto_to_dict(dto)
        assert d["ips"] == ["192.168.1.8"]
        assert d["emulationName"] == "kafka_em"
        assert d["kafkaManagersStatuses"][0]["topics"] == ["topic1", "topic2"]

    def test_host_managers_info_dto_to_dict(self) -> None:
        """
        Tests the host_managers_info_dto_to_dict function

        :return: None
        """
        status = cluster_manager_pb2.HostManagerStatusDTO(
            monitor_running=True, filebeat_running=True, packetbeat_running=False,
            metricbeat_running=True, heartbeat_running=False
        )
        dto = cluster_manager_pb2.HostManagersInfoDTO(
            ips=["192.168.1.9"], ports=[50054], emulationName="host_em", executionId=9,
            hostManagersRunning=[True], hostManagersStatuses=[status]
        )
        d = ClusterManagerUtil.host_managers_info_dto_to_dict(dto)
        assert d["ips"] == ["192.168.1.9"]
        assert d["emulationName"] == "host_em"
        assert d["hostManagersStatuses"][0]["filebeat_running"] is True

    def test_ryu_managers_info_dto_to_dict(self) -> None:
        """
        Tests the ryu_managers_info_dto_to_dict function

        :return: None
        """
        status = cluster_manager_pb2.RyuManagerStatusDTO(
            ryu_running=True, monitor_running=True, port=6653, web_port=8080,
            controller="ryu", kafka_ip="192.168.1.8", kafka_port=9092, time_step_len=10
        )
        dto = cluster_manager_pb2.RyuManagersInfoDTO(
            ips=["192.168.1.10"], ports=[6653], emulationName="ryu_em", executionId=10,
            ryuManagersRunning=[True], ryuManagersStatuses=[status]
        )
        d = ClusterManagerUtil.ryu_managers_info_dto_to_dict(dto)
        assert d["ips"] == ["192.168.1.10"]
        assert d["emulationName"] == "ryu_em"
        assert d["executionId"] == 10
        assert d["ryuManagersStatuses"][0]["ryu_running"] is True
