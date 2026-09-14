from typing import List
import pytest
import pytest_mock
import grpc
import csle_common.constants.constants as constants
from csle_common.dao.emulation_config.config import Config
from csle_common.util.grpc_auth_util import GrpcAuthServerInterceptor, GrpcAuthClientInterceptor
from csle_cluster.cluster_manager.cluster_manager_pb2 import LogsDTO, GetLogFileMsg
from csle_cluster.cluster_manager.cluster_manager_pb2_grpc import ClusterManagerStub
from csle_cluster.cluster_manager.cluster_manager import ClusterManagerServicer
import csle_cluster.cluster_manager.query_cluster_manager as query_cluster_manager


class TestClusterManagerAuthSuite:
    """
    Test suite for the authentication of the cluster manager gRPC server
    """

    @pytest.fixture(scope='module')
    def grpc_add_to_server(self):
        """
        Necessary fixture for pytest-grpc

        :return: the add_servicer_to_server function
        """
        from csle_cluster.cluster_manager.cluster_manager_pb2_grpc import add_ClusterManagerServicer_to_server
        return add_ClusterManagerServicer_to_server

    @pytest.fixture(scope='module')
    def grpc_servicer(self) -> ClusterManagerServicer:
        """
        Necessary fixture for pytest-grpc

        :return: the cluster manager servicer
        """
        return ClusterManagerServicer()

    @pytest.fixture(scope='module')
    def grpc_stub_cls(self, grpc_channel):
        """
        Necessary fixture for pytest-grpc

        :param grpc_channel: the grpc channel for testing
        :return: the stub to the service
        """
        return ClusterManagerStub

    @pytest.fixture(scope='module')
    def grpc_interceptors(self) -> List[grpc.ServerInterceptor]:
        """
        Overrides the pytest-grpc fixture so that the test server is started with the authentication
        interceptor, like the real cluster manager

        :return: the list of server interceptors
        """
        return [GrpcAuthServerInterceptor(token="test_token")]

    def test_unauthenticated_call_is_rejected(self, grpc_stub, mocker: pytest_mock.MockFixture,
                                              example_config: Config) -> None:
        """
        Tests that a call without a token, or with a wrong token, is rejected with UNAUTHENTICATED
        before reaching the servicer

        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param example_config: fixture that creates an example config
        :return: None
        """
        mocker.patch('csle_common.dao.emulation_config.config.Config.get_current_config',
                     return_value=example_config)
        exists = mocker.patch("os.path.exists", return_value=True)
        with pytest.raises(grpc.RpcError) as exc_info:
            query_cluster_manager.get_log_file(stub=grpc_stub, log_file_name="abcdef")
        assert exc_info.value.code() == grpc.StatusCode.UNAUTHENTICATED
        assert exc_info.value.details() == constants.GRPC_SERVERS.UNAUTHENTICATED_MSG
        with pytest.raises(grpc.RpcError) as exc_info:
            query_cluster_manager.get_node_status(stub=grpc_stub)
        assert exc_info.value.code() == grpc.StatusCode.UNAUTHENTICATED
        with pytest.raises(grpc.RpcError) as exc_info:
            grpc_stub.getLogFile(GetLogFileMsg(name="abcdef"),
                                 metadata=((constants.GRPC_SERVERS.AUTH_TOKEN_METADATA_KEY, "wrong_token"),))
        assert exc_info.value.code() == grpc.StatusCode.UNAUTHENTICATED
        exists.assert_not_called()

    def test_authenticated_call_is_forwarded(self, grpc_channel, grpc_stub, mocker: pytest_mock.MockFixture,
                                             example_config: Config) -> None:
        """
        Tests that a call carrying the correct token reaches the servicer, both when the metadata is passed
        explicitly and when it is attached by the client interceptor

        :param grpc_channel: the grpc channel for testing
        :param grpc_stub: the stub for the GRPC server to make the request to
        :param mocker: the mocker object to mock functions with external dependencies
        :param example_config: fixture that creates an example config
        :return: None
        """
        mocker.patch('csle_common.dao.emulation_config.config.Config.get_current_config',
                     return_value=example_config)
        mocker.patch('csle_cluster.cluster_manager.cluster_manager_util.ClusterManagerUtil.tail',
                     return_value="abcdef")
        mocker.patch("os.path.exists", return_value=True)
        mocker.patch('builtins.open', return_value=TestClusterManagerAuthSuite.with_class())
        log_file_name = f"{example_config.default_log_dir}/abcdef"
        msg = GetLogFileMsg(name=log_file_name)
        response: LogsDTO = grpc_stub.getLogFile(
            msg, metadata=((constants.GRPC_SERVERS.AUTH_TOKEN_METADATA_KEY, "test_token"),))
        assert response.logs == ['abcdef']
        authenticated_channel = grpc.intercept_channel(grpc_channel, GrpcAuthClientInterceptor(token="test_token"))
        authenticated_stub = ClusterManagerStub(authenticated_channel)
        response = query_cluster_manager.get_log_file(stub=authenticated_stub, log_file_name=log_file_name)
        assert response.logs == ['abcdef']

    @staticmethod
    def with_class():
        """
        Auxillary method for mocking a file object that supports the with statement

        :return: the mock object
        """

        class A:
            """
            Auxillary class for mocking
            """

            def __init__(self):
                pass

            def __enter__(self):
                pass

            def __exit__(self, exc_type, exc_value, traceback):
                pass

        return A()
