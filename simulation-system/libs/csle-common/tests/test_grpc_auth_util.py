from typing import Any, List, Tuple
from collections import namedtuple
from unittest.mock import MagicMock
import pytest
import pytest_mock
import grpc
import csle_common.constants.constants as constants
from csle_common.util.grpc_auth_util import GrpcAuthServerInterceptor, GrpcAuthClientInterceptor, GrpcAuthUtil


class TestGrpcAuthUtilSuite:
    """
    Test suite for grpc_auth_util
    """

    @pytest.fixture
    def handler_call_details(self):
        """
        Fixture that creates fake grpc.HandlerCallDetails objects

        :return: a factory function
        """
        HandlerCallDetails = namedtuple("HandlerCallDetails", ["method", "invocation_metadata"])

        def create(metadata: Any) -> Any:
            return HandlerCallDetails(method="/csle.ClusterManager/getLogFile", invocation_metadata=metadata)

        return create

    @pytest.fixture
    def client_call_details(self):
        """
        Fixture that creates fake grpc.ClientCallDetails objects

        :return: a factory function
        """
        ClientCallDetails = namedtuple(
            "ClientCallDetails", ["method", "timeout", "metadata", "credentials", "wait_for_ready", "compression"])

        def create(metadata: Any) -> Any:
            return ClientCallDetails(method="/csle.ClusterManager/getLogFile", timeout=5, metadata=metadata,
                                     credentials=None, wait_for_ready=None, compression=None)

        return create

    def test_server_interceptor_is_authenticated(self) -> None:
        """
        Tests the is_authenticated function of the server interceptor

        :return: None
        """
        interceptor = GrpcAuthServerInterceptor(token="secret")
        key = constants.GRPC_SERVERS.AUTH_TOKEN_METADATA_KEY
        assert interceptor.is_authenticated(metadata=[(key, "secret")])
        assert interceptor.is_authenticated(metadata=[("other", "x"), (key, "secret")])
        assert not interceptor.is_authenticated(metadata=[(key, "wrong")])
        assert not interceptor.is_authenticated(metadata=[(key, "")])
        assert not interceptor.is_authenticated(metadata=[(key, b"secret")])
        assert not interceptor.is_authenticated(metadata=[("other", "secret")])
        assert not interceptor.is_authenticated(metadata=[])
        assert not interceptor.is_authenticated(metadata=None)

    def test_server_interceptor_empty_token_rejects_everything(self) -> None:
        """
        Tests that the server interceptor fails closed when the configured token is empty

        :return: None
        """
        interceptor = GrpcAuthServerInterceptor(token="")
        key = constants.GRPC_SERVERS.AUTH_TOKEN_METADATA_KEY
        assert not interceptor.is_authenticated(metadata=[(key, "")])
        assert not interceptor.is_authenticated(metadata=[(key, "secret")])
        assert not interceptor.is_authenticated(metadata=[])

    def test_server_interceptor_intercept_service(self, handler_call_details) -> None:
        """
        Tests the intercept_service function of the server interceptor

        :param handler_call_details: fixture for creating fake handler call details
        :return: None
        """
        interceptor = GrpcAuthServerInterceptor(token="secret")
        key = constants.GRPC_SERVERS.AUTH_TOKEN_METADATA_KEY
        real_handler = object()
        continuation = MagicMock(return_value=real_handler)

        # Authenticated call is forwarded to the real handler
        details = handler_call_details(metadata=[(key, "secret")])
        handler = interceptor.intercept_service(continuation=continuation, handler_call_details=details)
        assert handler is real_handler
        continuation.assert_called_once_with(details)

        # Unauthenticated call is not forwarded and gets a handler that aborts the call
        continuation.reset_mock()
        details = handler_call_details(metadata=[(key, "wrong")])
        handler = interceptor.intercept_service(continuation=continuation, handler_call_details=details)
        assert handler is interceptor.unauthenticated_handler
        continuation.assert_not_called()
        context = MagicMock()
        handler.unary_unary(MagicMock(), context)
        context.abort.assert_called_once_with(grpc.StatusCode.UNAUTHENTICATED,
                                              constants.GRPC_SERVERS.UNAUTHENTICATED_MSG)

        # Missing metadata
        details = handler_call_details(metadata=[])
        handler = interceptor.intercept_service(continuation=continuation, handler_call_details=details)
        assert handler is interceptor.unauthenticated_handler
        continuation.assert_not_called()

    def test_client_interceptor_adds_token(self, client_call_details) -> None:
        """
        Tests that the client interceptor attaches the token to the call metadata

        :param client_call_details: fixture for creating fake client call details
        :return: None
        """
        interceptor = GrpcAuthClientInterceptor(token="secret")
        key = constants.GRPC_SERVERS.AUTH_TOKEN_METADATA_KEY
        captured: List[Tuple[Any, Any]] = []

        def continuation(details: Any, request: Any) -> str:
            captured.append((details, request))
            return "response"

        # No pre-existing metadata
        details = client_call_details(metadata=None)
        result = interceptor.intercept_unary_unary(continuation=continuation, client_call_details=details,
                                                   request="request")
        assert result == "response"
        new_details, request = captured[-1]
        assert request == "request"
        assert new_details.metadata == [(key, "secret")]
        assert new_details.method == details.method
        assert new_details.timeout == details.timeout
        assert isinstance(new_details, grpc.ClientCallDetails)

        # Pre-existing metadata is preserved
        details = client_call_details(metadata=(("other", "x"),))
        interceptor.intercept_unary_unary(continuation=continuation, client_call_details=details, request="r")
        new_details, _ = captured[-1]
        assert new_details.metadata == [("other", "x"), (key, "secret")]

    def test_get_cluster_manager_token(self, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the get_cluster_manager_token function

        :param mocker: the pytest mocker object
        :return: None
        """
        config = MagicMock()
        config.cluster_manager_token = "secret"
        mocker.patch("csle_common.dao.emulation_config.config.Config.get_current_config", return_value=config)
        assert GrpcAuthUtil.get_cluster_manager_token() == "secret"
        mocker.patch("csle_common.dao.emulation_config.config.Config.get_current_config", return_value=None)
        with pytest.raises(ValueError):
            GrpcAuthUtil.get_cluster_manager_token()

    def test_create_authenticated_channel(self, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests the create_authenticated_channel function

        :param mocker: the pytest mocker object
        :return: None
        """
        config = MagicMock()
        config.cluster_manager_token = "secret"
        mocker.patch("csle_common.dao.emulation_config.config.Config.get_current_config", return_value=config)
        intercept_channel = mocker.patch("grpc.intercept_channel", return_value="intercepted_channel")
        insecure_channel = mocker.patch("grpc.insecure_channel", return_value="raw_channel")
        channel = GrpcAuthUtil.create_authenticated_channel(ip="127.0.0.1", port=50041)
        assert channel == "intercepted_channel"
        insecure_channel.assert_called_once_with("127.0.0.1:50041", options=constants.GRPC_SERVERS.GRPC_OPTIONS)
        raw_channel, interceptor = intercept_channel.call_args[0]
        assert raw_channel == "raw_channel"
        assert isinstance(interceptor, GrpcAuthClientInterceptor)
        assert interceptor.token == "secret"

        # Explicit token overrides the configured one
        GrpcAuthUtil.create_authenticated_channel(ip="127.0.0.1", port=50041, token="other")
        _, interceptor = intercept_channel.call_args[0]
        assert interceptor.token == "other"

    def test_end_to_end(self) -> None:
        """
        Tests the server and client interceptors together against a real in-process gRPC server

        :return: None
        """
        def echo(request: bytes, context: grpc.ServicerContext) -> bytes:
            return request

        handler = grpc.method_handlers_generic_handler(
            "test.Echo", {"echo": grpc.unary_unary_rpc_method_handler(echo)})
        server = grpc.server(futures_pool(), interceptors=[GrpcAuthServerInterceptor(token="secret")])
        server.add_generic_rpc_handlers((handler,))
        port = server.add_insecure_port("localhost:0")
        server.start()
        try:
            with grpc.insecure_channel(f"localhost:{port}") as channel:
                call = channel.unary_unary("/test.Echo/echo")
                with pytest.raises(grpc.RpcError) as exc_info:
                    call(b"hello", timeout=5)
                assert exc_info.value.code() == grpc.StatusCode.UNAUTHENTICATED
                with pytest.raises(grpc.RpcError) as exc_info:
                    call(b"hello", timeout=5, metadata=((constants.GRPC_SERVERS.AUTH_TOKEN_METADATA_KEY, "wrong"),))
                assert exc_info.value.code() == grpc.StatusCode.UNAUTHENTICATED
                assert call(b"hello", timeout=5,
                            metadata=((constants.GRPC_SERVERS.AUTH_TOKEN_METADATA_KEY, "secret"),)) == b"hello"
            with GrpcAuthUtil.create_authenticated_channel(ip="localhost", port=port, token="secret") as channel:
                assert channel.unary_unary("/test.Echo/echo")(b"hello", timeout=5) == b"hello"
            with GrpcAuthUtil.create_authenticated_channel(ip="localhost", port=port, token="wrong") as channel:
                with pytest.raises(grpc.RpcError) as exc_info:
                    channel.unary_unary("/test.Echo/echo")(b"hello", timeout=5)
                assert exc_info.value.code() == grpc.StatusCode.UNAUTHENTICATED
        finally:
            server.stop(grace=None)


def futures_pool() -> Any:
    """
    Creates a small thread pool for the in-process gRPC test server

    :return: the thread pool
    """
    from concurrent import futures
    return futures.ThreadPoolExecutor(max_workers=2)
