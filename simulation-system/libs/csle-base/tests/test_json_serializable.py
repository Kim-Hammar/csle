"""
Unit tests for the JSONSerializable abstract base class.
"""
import json
import os
import tempfile
from typing import Any, Dict

from csle_base.json_serializable import JSONSerializable


class ConcreteJSONSerializable(JSONSerializable):
    """
    Concrete implementation of JSONSerializable for testing purposes.
    """

    def __init__(self, name: str, value: int) -> None:
        """
        Initializes the object.

        :param name: a name string
        :param value: an integer value
        """
        self.name = name
        self.value = value

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "ConcreteJSONSerializable":
        """
        Converts a dict representation to an instance.

        :param d: the dict to convert
        :return: the converted instance
        """
        return ConcreteJSONSerializable(name=d["name"], value=d["value"])

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the object to a dict representation.

        :return: a dict representation of the object
        """
        return {"name": self.name, "value": self.value}

    @staticmethod
    def from_json_file(json_file_path: str) -> "ConcreteJSONSerializable":
        """
        Reads a json file and converts it to an object.

        :param json_file_path: the json file path
        :return: the object
        """
        with open(json_file_path, 'r') as f:
            d = json.load(f)
        return ConcreteJSONSerializable.from_dict(d)


class TestJSONSerializableSuite:
    """
    Test suite for the JSONSerializable abstract base class.

    Uses ConcreteJSONSerializable as a concrete implementation for testing.
    """

    def test_to_dict(self) -> None:
        """
        Tests the to_dict method.

        :return: None
        """
        obj = ConcreteJSONSerializable(name="test", value=42)
        d = obj.to_dict()
        assert d == {"name": "test", "value": 42}

    def test_from_dict(self) -> None:
        """
        Tests the from_dict static method.

        :return: None
        """
        d = {"name": "example", "value": 100}
        obj = ConcreteJSONSerializable.from_dict(d)
        assert obj.name == "example"
        assert obj.value == 100

    def test_to_json_str(self) -> None:
        """
        Tests the to_json_str method.

        :return: None
        """
        obj = ConcreteJSONSerializable(name="json_test", value=123)
        json_str = obj.to_json_str()
        parsed = json.loads(json_str)
        assert parsed["name"] == "json_test"
        assert parsed["value"] == 123

    def test_to_json_str_is_valid_json(self) -> None:
        """
        Tests that to_json_str produces valid JSON.

        :return: None
        """
        obj = ConcreteJSONSerializable(name="valid", value=999)
        json_str = obj.to_json_str()
        # Should not raise an exception
        json.loads(json_str)

    def test_to_json_str_is_sorted(self) -> None:
        """
        Tests that to_json_str produces sorted keys.

        :return: None
        """
        obj = ConcreteJSONSerializable(name="sorted", value=1)
        json_str = obj.to_json_str()
        # "name" comes before "value" alphabetically
        name_pos = json_str.find('"name"')
        value_pos = json_str.find('"value"')
        assert name_pos < value_pos

    def test_to_json_file(self) -> None:
        """
        Tests the to_json_file method.

        :return: None
        """
        obj = ConcreteJSONSerializable(name="file_test", value=456)
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_path = f.name

        try:
            obj.to_json_file(temp_path)
            with open(temp_path, 'r') as f:
                content = f.read()
            parsed = json.loads(content)
            assert parsed["name"] == "file_test"
            assert parsed["value"] == 456
        finally:
            os.unlink(temp_path)

    def test_from_json_file(self) -> None:
        """
        Tests the from_json_file static method.

        :return: None
        """
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump({"name": "from_file", "value": 789}, f)
            temp_path = f.name

        try:
            obj = ConcreteJSONSerializable.from_json_file(temp_path)
            assert obj.name == "from_file"
            assert obj.value == 789
        finally:
            os.unlink(temp_path)

    def test_roundtrip_dict(self) -> None:
        """
        Tests roundtrip conversion through dict.

        :return: None
        """
        original = ConcreteJSONSerializable(name="roundtrip", value=111)
        d = original.to_dict()
        restored = ConcreteJSONSerializable.from_dict(d)
        assert restored.name == original.name
        assert restored.value == original.value

    def test_roundtrip_json_str(self) -> None:
        """
        Tests roundtrip conversion through JSON string.

        :return: None
        """
        original = ConcreteJSONSerializable(name="json_roundtrip", value=222)
        json_str = original.to_json_str()
        d = json.loads(json_str)
        restored = ConcreteJSONSerializable.from_dict(d)
        assert restored.name == original.name
        assert restored.value == original.value

    def test_roundtrip_json_file(self) -> None:
        """
        Tests roundtrip conversion through JSON file.

        :return: None
        """
        original = ConcreteJSONSerializable(name="file_roundtrip", value=333)
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_path = f.name

        try:
            original.to_json_file(temp_path)
            restored = ConcreteJSONSerializable.from_json_file(temp_path)
            assert restored.name == original.name
            assert restored.value == original.value
        finally:
            os.unlink(temp_path)

    def test_equality_same_values(self) -> None:
        """
        Tests equality comparison with same values.

        :return: None
        """
        obj1 = ConcreteJSONSerializable(name="equal", value=100)
        obj2 = ConcreteJSONSerializable(name="equal", value=100)
        assert obj1 == obj2

    def test_equality_different_values(self) -> None:
        """
        Tests equality comparison with different values.

        :return: None
        """
        obj1 = ConcreteJSONSerializable(name="one", value=1)
        obj2 = ConcreteJSONSerializable(name="two", value=2)
        assert obj1 != obj2

    def test_equality_different_name(self) -> None:
        """
        Tests equality comparison with different name but same value.

        :return: None
        """
        obj1 = ConcreteJSONSerializable(name="alpha", value=100)
        obj2 = ConcreteJSONSerializable(name="beta", value=100)
        assert obj1 != obj2

    def test_equality_different_value(self) -> None:
        """
        Tests equality comparison with same name but different value.

        :return: None
        """
        obj1 = ConcreteJSONSerializable(name="same", value=1)
        obj2 = ConcreteJSONSerializable(name="same", value=2)
        assert obj1 != obj2

    def test_equality_with_non_serializable(self) -> None:
        """
        Tests equality comparison with non-JSONSerializable object.

        :return: None
        """
        obj = ConcreteJSONSerializable(name="test", value=42)
        assert obj != "not a serializable"
        assert obj != 42
        assert obj != {"name": "test", "value": 42}

    def test_equality_reflexive(self) -> None:
        """
        Tests that equality is reflexive (obj == obj).

        :return: None
        """
        obj = ConcreteJSONSerializable(name="reflexive", value=50)
        assert obj == obj

    def test_json_str_with_special_characters(self) -> None:
        """
        Tests to_json_str with special characters in name.

        :return: None
        """
        obj = ConcreteJSONSerializable(name="special \"chars\" \n\t", value=1)
        json_str = obj.to_json_str()
        parsed = json.loads(json_str)
        assert parsed["name"] == "special \"chars\" \n\t"
