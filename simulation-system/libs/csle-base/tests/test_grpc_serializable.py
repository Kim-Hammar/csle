"""
Unit tests for the GRPCSerializable abstract base class.
"""
from abc import ABC
import inspect

from csle_base.grpc_serializable import GRPCSerializable


class ConcreteGRPCSerializable(GRPCSerializable):
    """
    Concrete implementation of GRPCSerializable for testing purposes.
    """

    def __init__(self, data: str) -> None:
        """
        Initializes the object.

        :param data: the data string
        """
        self.data = data

    def to_grpc_object(self) -> str:
        """
        Converts to a grpc serializable version.

        :return: a grpc serializable version of the object
        """
        return f"grpc:{self.data}"

    @staticmethod
    def from_grpc_object(obj: str) -> "ConcreteGRPCSerializable":
        """
        Instantiate the object from a GRPC object.

        :param obj: the object to instantiate from
        :return: the instantiated grpc object
        """
        if obj.startswith("grpc:"):
            data = obj[5:]
        else:
            data = obj
        return ConcreteGRPCSerializable(data=data)


class TestGRPCSerializableSuite:
    """
    Test suite for the GRPCSerializable abstract base class.
    """

    def test_is_abstract_class(self) -> None:
        """
        Tests that GRPCSerializable is an abstract base class.

        :return: None
        """
        assert inspect.isabstract(GRPCSerializable)
        assert issubclass(GRPCSerializable, ABC)

    def test_has_abstract_to_grpc_object(self) -> None:
        """
        Tests that to_grpc_object is an abstract method.

        :return: None
        """
        assert hasattr(GRPCSerializable, 'to_grpc_object')
        assert getattr(GRPCSerializable.to_grpc_object, '__isabstractmethod__', False)

    def test_has_abstract_from_grpc_object(self) -> None:
        """
        Tests that from_grpc_object is an abstract method.

        :return: None
        """
        assert hasattr(GRPCSerializable, 'from_grpc_object')
        assert getattr(GRPCSerializable.from_grpc_object, '__isabstractmethod__', False)

    def test_concrete_implementation_to_grpc_object(self) -> None:
        """
        Tests to_grpc_object on concrete implementation.

        :return: None
        """
        obj = ConcreteGRPCSerializable(data="test_data")
        grpc_obj = obj.to_grpc_object()
        assert grpc_obj == "grpc:test_data"

    def test_concrete_implementation_from_grpc_object(self) -> None:
        """
        Tests from_grpc_object on concrete implementation.

        :return: None
        """
        grpc_obj = "grpc:restored_data"
        obj = ConcreteGRPCSerializable.from_grpc_object(grpc_obj)
        assert obj.data == "restored_data"

    def test_roundtrip_grpc(self) -> None:
        """
        Tests roundtrip conversion through gRPC serialization.

        :return: None
        """
        original = ConcreteGRPCSerializable(data="roundtrip_test")
        grpc_obj = original.to_grpc_object()
        restored = ConcreteGRPCSerializable.from_grpc_object(grpc_obj)
        assert restored.data == original.data

    def test_concrete_is_subclass(self) -> None:
        """
        Tests that concrete implementation is a subclass of GRPCSerializable.

        :return: None
        """
        assert issubclass(ConcreteGRPCSerializable, GRPCSerializable)

    def test_concrete_is_instance(self) -> None:
        """
        Tests that concrete instance is an instance of GRPCSerializable.

        :return: None
        """
        obj = ConcreteGRPCSerializable(data="instance_test")
        assert isinstance(obj, GRPCSerializable)

    def test_from_grpc_object_handles_raw_data(self) -> None:
        """
        Tests from_grpc_object handles data without prefix.

        :return: None
        """
        obj = ConcreteGRPCSerializable.from_grpc_object("raw_data")
        assert obj.data == "raw_data"

    def test_empty_data(self) -> None:
        """
        Tests serialization with empty data.

        :return: None
        """
        obj = ConcreteGRPCSerializable(data="")
        grpc_obj = obj.to_grpc_object()
        assert grpc_obj == "grpc:"
        restored = ConcreteGRPCSerializable.from_grpc_object(grpc_obj)
        assert restored.data == ""
