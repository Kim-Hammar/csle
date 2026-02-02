"""
Unit tests for the KafkaSerializable abstract base class.
"""
from abc import ABC
import inspect

from csle_base.kafka_serializable import KafkaSerializable


class ConcreteKafkaSerializable(KafkaSerializable):
    """
    Concrete implementation of KafkaSerializable for testing purposes.
    """

    def __init__(self, metric: float, count: int) -> None:
        """
        Initializes the object.

        :param metric: a metric value
        :param count: a count value
        """
        self.metric = metric
        self.count = count

    def to_kafka_record(self, ip: str) -> str:
        """
        Converts the DTO into a kafka record.

        :param ip: the ip to add to the record
        :return: a comma-separated string representing the kafka record
        """
        return f"{ip},{self.metric},{self.count}"

    @staticmethod
    def from_kafka_record(record: str) -> "ConcreteKafkaSerializable":
        """
        Converts a kafka record to a DTO.

        :param record: the kafka record to convert
        :return: the DTO
        """
        parts = record.split(",")
        # Skip ip (parts[0]), parse metric and count
        metric = float(parts[1])
        count = int(parts[2])
        return ConcreteKafkaSerializable(metric=metric, count=count)


class TestKafkaSerializableSuite:
    """
    Test suite for the KafkaSerializable abstract base class.
    """

    def test_is_abstract_class(self) -> None:
        """
        Tests that KafkaSerializable is an abstract base class.

        :return: None
        """
        assert inspect.isabstract(KafkaSerializable)
        assert issubclass(KafkaSerializable, ABC)

    def test_has_abstract_to_kafka_record(self) -> None:
        """
        Tests that to_kafka_record is an abstract method.

        :return: None
        """
        assert hasattr(KafkaSerializable, 'to_kafka_record')
        assert getattr(KafkaSerializable.to_kafka_record, '__isabstractmethod__', False)

    def test_has_abstract_from_kafka_record(self) -> None:
        """
        Tests that from_kafka_record is an abstract method.

        :return: None
        """
        assert hasattr(KafkaSerializable, 'from_kafka_record')
        assert getattr(KafkaSerializable.from_kafka_record, '__isabstractmethod__', False)

    def test_concrete_implementation_to_kafka_record(self) -> None:
        """
        Tests to_kafka_record on concrete implementation.

        :return: None
        """
        obj = ConcreteKafkaSerializable(metric=3.14, count=100)
        record = obj.to_kafka_record(ip="192.168.1.1")
        assert record == "192.168.1.1,3.14,100"

    def test_concrete_implementation_from_kafka_record(self) -> None:
        """
        Tests from_kafka_record on concrete implementation.

        :return: None
        """
        record = "10.0.0.1,2.718,50"
        obj = ConcreteKafkaSerializable.from_kafka_record(record)
        assert abs(obj.metric - 2.718) < 0.001
        assert obj.count == 50

    def test_roundtrip_kafka(self) -> None:
        """
        Tests roundtrip conversion through Kafka serialization.

        :return: None
        """
        original = ConcreteKafkaSerializable(metric=1.5, count=42)
        record = original.to_kafka_record(ip="127.0.0.1")
        restored = ConcreteKafkaSerializable.from_kafka_record(record)
        assert abs(restored.metric - original.metric) < 0.001
        assert restored.count == original.count

    def test_concrete_is_subclass(self) -> None:
        """
        Tests that concrete implementation is a subclass of KafkaSerializable.

        :return: None
        """
        assert issubclass(ConcreteKafkaSerializable, KafkaSerializable)

    def test_concrete_is_instance(self) -> None:
        """
        Tests that concrete instance is an instance of KafkaSerializable.

        :return: None
        """
        obj = ConcreteKafkaSerializable(metric=1.0, count=1)
        assert isinstance(obj, KafkaSerializable)

    def test_different_ip_addresses(self) -> None:
        """
        Tests to_kafka_record with different IP addresses.

        :return: None
        """
        obj = ConcreteKafkaSerializable(metric=5.0, count=10)

        record1 = obj.to_kafka_record(ip="192.168.0.1")
        assert record1.startswith("192.168.0.1,")

        record2 = obj.to_kafka_record(ip="10.0.0.1")
        assert record2.startswith("10.0.0.1,")

    def test_zero_values(self) -> None:
        """
        Tests serialization with zero values.

        :return: None
        """
        obj = ConcreteKafkaSerializable(metric=0.0, count=0)
        record = obj.to_kafka_record(ip="0.0.0.0")
        assert record == "0.0.0.0,0.0,0"

    def test_negative_values(self) -> None:
        """
        Tests serialization with negative values.

        :return: None
        """
        obj = ConcreteKafkaSerializable(metric=-1.5, count=-10)
        record = obj.to_kafka_record(ip="127.0.0.1")
        restored = ConcreteKafkaSerializable.from_kafka_record(record)
        assert abs(restored.metric - (-1.5)) < 0.001
        assert restored.count == -10

    def test_large_values(self) -> None:
        """
        Tests serialization with large values.

        :return: None
        """
        obj = ConcreteKafkaSerializable(metric=1e10, count=1000000)
        record = obj.to_kafka_record(ip="255.255.255.255")
        restored = ConcreteKafkaSerializable.from_kafka_record(record)
        assert abs(restored.metric - 1e10) < 1e5
        assert restored.count == 1000000
