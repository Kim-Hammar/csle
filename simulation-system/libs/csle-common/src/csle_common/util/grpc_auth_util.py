import collections
import hmac
import logging
from typing import Any, Callable, List, Optional, Sequence, Tuple
import grpc
import csle_common.constants.constants as constants
from csle_common.dao.emulation_config.config import Config


class _AuthClientCallDetails(
        collections.namedtuple("_AuthClientCallDetails",
                               ("method", "timeout", "metadata", "credentials", "wait_for_ready", "compression")),
        grpc.ClientCallDetails):
    """
    Concrete grpc.ClientCallDetails (the base class is abstract) used to forward call details with
    the authentication metadata attached
    """
    pass


class GrpcAuthServerInterceptor(grpc.ServerInterceptor):
    """
    Server-side gRPC interceptor that rejects every request that does not carry the expected token
    in its call metadata
    """

    def __init__(self, token: str) -> None:
        """
        Initializes the interceptor

        :param token: the token that clients must present. If empty, all requests are rejected.
        """
        self.token = token
        if self.token == "":
            logging.warning("The configured gRPC authentication token is empty, all requests will be rejected")

        def abort_unauthenticated(request: Any, context: grpc.ServicerContext) -> None:
            """
            Handler that aborts the call with the UNAUTHENTICATED status code

            :param request: the gRPC request
            :param context: the gRPC context
            :return: None
            """
            context.abort(grpc.StatusCode.UNAUTHENTICATED, constants.GRPC_SERVERS.UNAUTHENTICATED_MSG)

        self.unauthenticated_handler = grpc.unary_unary_rpc_method_handler(abort_unauthenticated)

    def is_authenticated(self, metadata: Optional[Sequence[Tuple[str, Any]]]) -> bool:
        """
        Checks whether the given call metadata carries the expected token

        :param metadata: the invocation metadata of the call
        :return: True if the token is present and valid, otherwise False
        """
        if self.token == "" or metadata is None:
            return False
        for key, value in metadata:
            if key == constants.GRPC_SERVERS.AUTH_TOKEN_METADATA_KEY and isinstance(value, str) \
                    and hmac.compare_digest(value, self.token):
                return True
        return False

    def intercept_service(self, continuation: Callable[[grpc.HandlerCallDetails], Any],
                          handler_call_details: grpc.HandlerCallDetails) -> Any:
        """
        Intercepts an incoming request and forwards it to the real handler only if it is authenticated

        :param continuation: function that forwards the request to the next interceptor or the handler
        :param handler_call_details: the details of the incoming call
        :return: the RPC method handler to use for the call
        """
        if self.is_authenticated(metadata=handler_call_details.invocation_metadata):
            return continuation(handler_call_details)
        logging.warning(f"Rejected unauthenticated gRPC request to: {handler_call_details.method}")
        return self.unauthenticated_handler


class GrpcAuthClientInterceptor(grpc.UnaryUnaryClientInterceptor):
    """
    Client-side gRPC interceptor that attaches the authentication token to the metadata of every call
    """

    def __init__(self, token: str) -> None:
        """
        Initializes the interceptor

        :param token: the token to attach to outgoing calls
        """
        self.token = token

    def intercept_unary_unary(self, continuation: Callable[[grpc.ClientCallDetails, Any], Any],
                              client_call_details: grpc.ClientCallDetails, request: Any) -> Any:
        """
        Intercepts an outgoing call and adds the token to its metadata

        :param continuation: function that performs the call with the given call details
        :param client_call_details: the details of the outgoing call
        :param request: the request message
        :return: the result of the continuation
        """
        metadata: List[Tuple[str, Any]] = []
        if client_call_details.metadata is not None:
            metadata = list(client_call_details.metadata)
        metadata.append((constants.GRPC_SERVERS.AUTH_TOKEN_METADATA_KEY, self.token))
        new_details = _AuthClientCallDetails(
            method=client_call_details.method, timeout=client_call_details.timeout, metadata=metadata,
            credentials=client_call_details.credentials, wait_for_ready=client_call_details.wait_for_ready,
            compression=client_call_details.compression)
        return continuation(new_details, request)


class GrpcAuthUtil:
    """
    Utility functions for authenticated gRPC channels in CSLE
    """

    @staticmethod
    def get_cluster_manager_token() -> str:
        """
        Reads the cluster manager token from the currently loaded CSLE configuration

        :return: the token
        """
        config = Config.get_current_config()
        if config is None:
            raise ValueError("The CSLE configuration is not loaded, cannot read the cluster manager token")
        return config.cluster_manager_token

    @staticmethod
    def create_authenticated_channel(ip: str, port: int, token: Optional[str] = None) -> grpc.Channel:
        """
        Creates a gRPC channel to the cluster manager that attaches the authentication token to every call

        :param ip: the ip of the cluster manager
        :param port: the port of the cluster manager
        :param token: the token to use (if None, it is read from the currently loaded configuration)
        :return: the channel
        """
        if token is None:
            token = GrpcAuthUtil.get_cluster_manager_token()
        channel = grpc.insecure_channel(f"{ip}:{port}", options=constants.GRPC_SERVERS.GRPC_OPTIONS)
        return grpc.intercept_channel(channel, GrpcAuthClientInterceptor(token=token))
