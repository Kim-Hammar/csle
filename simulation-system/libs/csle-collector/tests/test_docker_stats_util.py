from csle_collector.docker_stats_manager.docker_stats_util import DockerStatsUtil
from csle_collector.docker_stats_manager.docker_stats_manager_pb2 import DockerStatsMonitorDTO
import csle_collector.constants.constants as constants


class TestDockerStatsUtilSuite:
    """
    Test suite for DockerStatsUtil
    """

    def test_calculate_cpu_percent(self) -> None:
        """
        Tests the calculate_cpu_percent function
        """
        stats_dict = {
            constants.DOCKER_STATS.CPU_STATS: {
                constants.DOCKER_STATS.CPU_USAGE: {
                    constants.DOCKER_STATS.TOTAL_USAGE: 1000,
                    constants.DOCKER_STATS.PERCPU_USAGE: [500, 500]
                },
                constants.DOCKER_STATS.SYSTEM_CPU_USAGE: 5000
            },
            constants.DOCKER_STATS.PRECPU_STATS: {
                constants.DOCKER_STATS.CPU_USAGE: {
                    constants.DOCKER_STATS.TOTAL_USAGE: 500
                },
                constants.DOCKER_STATS.SYSTEM_CPU_USAGE: 4000
            }
        }
        cpu_percent = DockerStatsUtil.calculate_cpu_percent(stats_dict)
        assert cpu_percent == 100.0

    def test_calculate_cpu_percent2(self) -> None:
        """
        Tests the calculate_cpu_percent2 function
        """
        stats_dict = {
            constants.DOCKER_STATS.CPU_STATS: {
                constants.DOCKER_STATS.CPU_USAGE: {
                    constants.DOCKER_STATS.TOTAL_USAGE: 1000,
                    constants.DOCKER_STATS.PERCPU_USAGE: [500, 500]
                },
                constants.DOCKER_STATS.SYSTEM_CPU_USAGE: 5000,
                constants.DOCKER_STATS.ONLINE_CPUS: 2
            }
        }
        previous_cpu = 500.0
        previous_system = 4000.0
        cpu_percent, cpu_system, cpu_total = DockerStatsUtil.calculate_cpu_percent2(
            stats_dict, previous_cpu, previous_system)
        assert cpu_percent == 100.0
        assert cpu_system == 5000.0
        assert cpu_total == 1000.0

    def test_calculate_blkio_mb(self) -> None:
        """
        Tests the calculate_blkio_mb function
        """
        stats_dict = {
            constants.DOCKER_STATS.BLKIO_STATS: {
                constants.DOCKER_STATS.IO_SERVICE_BYTES_RECURSIVE: [
                    {constants.DOCKER_STATS.OP: constants.DOCKER_STATS.READ, constants.DOCKER_STATS.VALUE: 1000000},
                    {constants.DOCKER_STATS.OP: constants.DOCKER_STATS.WRITE, constants.DOCKER_STATS.VALUE: 2000000}
                ]
            }
        }
        r, w = DockerStatsUtil.calculate_blkio_mb(stats_dict)
        assert r == 1.0
        assert w == 2.0

    def test_calculate_network_mb(self) -> None:
        """
        Tests the calculate_network_mb function
        """
        stats_dict = {
            constants.DOCKER_STATS.NETWORKS: {
                "eth0": {
                    constants.DOCKER_STATS.RX_BYTES: 1000000,
                    constants.DOCKER_STATS.TX_BYTES: 2000000
                },
                "eth1": {
                    constants.DOCKER_STATS.RX_BYTES: 500000,
                    constants.DOCKER_STATS.TX_BYTES: 500000
                }
            }
        }
        r, t = DockerStatsUtil.calculate_network_mb(stats_dict)
        assert r == 1.5
        assert t == 2.5

    def test_graceful_chain_get(self) -> None:
        """
        Tests the graceful_chain_get function
        """
        d = {"a": {"b": {"c": 1}}}
        assert DockerStatsUtil.graceful_chain_get(d, "a", "b", "c") == 1
        assert DockerStatsUtil.graceful_chain_get(d, "a", "x") is None
        assert DockerStatsUtil.graceful_chain_get(d, "a", "x", default=0) == 0

    def test_docker_stats_monitor_dto_to_dict(self) -> None:
        """
        Tests the docker_stats_monitor_dto_to_dict function
        """
        dto = DockerStatsMonitorDTO()
        dto.num_monitors = 2
        dto.emulations.extend(["em1", "em2"])
        dto.emulation_executions.extend([1, 2])
        
        d = DockerStatsUtil.docker_stats_monitor_dto_to_dict(dto)
        assert d["num_monitors"] == 2
        assert d["emulations"] == ["em1", "em2"]
        assert d["emulation_executions"] == [1, 2]

    def test_docker_stats_monitor_dto_from_dict(self) -> None:
        """
        Tests the docker_stats_monitor_dto_from_dict function
        """
        d = {
            "num_monitors": 3,
            "emulations": ["em1", "em2", "em3"],
            "emulation_executions": [1, 2, 3]
        }
        dto = DockerStatsUtil.docker_stats_monitor_dto_from_dict(d)
        assert dto.num_monitors == 3
        assert list(dto.emulations) == ["em1", "em2", "em3"]
        assert list(dto.emulation_executions) == [1, 2, 3]

    def test_docker_stats_monitor_dto_empty(self) -> None:
        """
        Tests the docker_stats_monitor_dto_empty function
        """
        dto = DockerStatsUtil.docker_stats_monitor_dto_empty()
        assert dto.num_monitors == 0
