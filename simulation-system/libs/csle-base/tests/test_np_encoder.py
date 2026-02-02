"""
Unit tests for the NpEncoder class.
"""
import json
from typing import Any, Dict, List

import numpy as np

from csle_base.encoding.np_encoder import NpEncoder


class TestNpEncoderSuite:
    """
    Test suite for the NpEncoder class.

    The NpEncoder is a JSON encoder that handles NumPy data types.
    """

    def test_encode_numpy_int32(self) -> None:
        """
        Tests encoding of numpy int32 to JSON.

        :return: None
        """
        data: Dict[str, Any] = {"value": np.int32(42)}
        result = json.dumps(data, cls=NpEncoder)
        decoded = json.loads(result)
        assert decoded["value"] == 42
        assert isinstance(decoded["value"], int)

    def test_encode_numpy_int64(self) -> None:
        """
        Tests encoding of numpy int64 to JSON.

        :return: None
        """
        data: Dict[str, Any] = {"value": np.int64(123456789)}
        result = json.dumps(data, cls=NpEncoder)
        decoded = json.loads(result)
        assert decoded["value"] == 123456789
        assert isinstance(decoded["value"], int)

    def test_encode_numpy_float32(self) -> None:
        """
        Tests encoding of numpy float32 to JSON.

        :return: None
        """
        data: Dict[str, Any] = {"value": np.float32(3.14)}
        result = json.dumps(data, cls=NpEncoder)
        decoded = json.loads(result)
        assert abs(decoded["value"] - 3.14) < 0.001
        assert isinstance(decoded["value"], float)

    def test_encode_numpy_float64(self) -> None:
        """
        Tests encoding of numpy float64 to JSON.

        :return: None
        """
        data: Dict[str, Any] = {"value": np.float64(2.718281828)}
        result = json.dumps(data, cls=NpEncoder)
        decoded = json.loads(result)
        assert abs(decoded["value"] - 2.718281828) < 0.0001
        assert isinstance(decoded["value"], float)

    def test_encode_numpy_array_1d(self) -> None:
        """
        Tests encoding of 1D numpy array to JSON.

        :return: None
        """
        arr = np.array([1, 2, 3, 4, 5])
        data: Dict[str, Any] = {"array": arr}
        result = json.dumps(data, cls=NpEncoder)
        decoded = json.loads(result)
        assert decoded["array"] == [1, 2, 3, 4, 5]
        assert isinstance(decoded["array"], list)

    def test_encode_numpy_array_2d(self) -> None:
        """
        Tests encoding of 2D numpy array to JSON.

        :return: None
        """
        arr = np.array([[1, 2], [3, 4]])
        data: Dict[str, Any] = {"matrix": arr}
        result = json.dumps(data, cls=NpEncoder)
        decoded = json.loads(result)
        assert decoded["matrix"] == [[1, 2], [3, 4]]
        assert isinstance(decoded["matrix"], list)

    def test_encode_numpy_array_float(self) -> None:
        """
        Tests encoding of float numpy array to JSON.

        :return: None
        """
        arr = np.array([1.1, 2.2, 3.3])
        data: Dict[str, Any] = {"floats": arr}
        result = json.dumps(data, cls=NpEncoder)
        decoded = json.loads(result)
        assert len(decoded["floats"]) == 3
        assert abs(decoded["floats"][0] - 1.1) < 0.001

    def test_encode_mixed_types(self) -> None:
        """
        Tests encoding of mixed numpy and Python types to JSON.

        :return: None
        """
        data: Dict[str, Any] = {
            "int_val": np.int64(100),
            "float_val": np.float32(1.5),
            "array": np.array([1, 2, 3]),
            "python_int": 42,
            "python_str": "test"
        }
        result = json.dumps(data, cls=NpEncoder)
        decoded = json.loads(result)
        assert decoded["int_val"] == 100
        assert abs(decoded["float_val"] - 1.5) < 0.001
        assert decoded["array"] == [1, 2, 3]
        assert decoded["python_int"] == 42
        assert decoded["python_str"] == "test"

    def test_encode_empty_array(self) -> None:
        """
        Tests encoding of empty numpy array to JSON.

        :return: None
        """
        arr = np.array([])
        data: Dict[str, Any] = {"empty": arr}
        result = json.dumps(data, cls=NpEncoder)
        decoded = json.loads(result)
        assert decoded["empty"] == []

    def test_encode_nested_structure(self) -> None:
        """
        Tests encoding of nested structure with numpy types to JSON.

        :return: None
        """
        data: Dict[str, Any] = {
            "outer": {
                "inner_array": np.array([1, 2]),
                "inner_int": np.int32(5)
            }
        }
        result = json.dumps(data, cls=NpEncoder)
        decoded = json.loads(result)
        assert decoded["outer"]["inner_array"] == [1, 2]
        assert decoded["outer"]["inner_int"] == 5

    def test_encoder_default_method_directly(self) -> None:
        """
        Tests the default method of NpEncoder directly.

        :return: None
        """
        encoder = NpEncoder()
        assert encoder.default(np.int32(10)) == 10
        assert encoder.default(np.float64(3.14)) == 3.14
        assert encoder.default(np.array([1, 2, 3])) == [1, 2, 3]

    def test_encode_list_with_numpy_elements(self) -> None:
        """
        Tests encoding of Python list containing numpy elements.

        :return: None
        """
        data: Dict[str, List[Any]] = {
            "mixed_list": [np.int32(1), np.float64(2.5), np.array([3, 4])]
        }
        result = json.dumps(data, cls=NpEncoder)
        decoded = json.loads(result)
        assert decoded["mixed_list"][0] == 1
        assert abs(decoded["mixed_list"][1] - 2.5) < 0.001
        assert decoded["mixed_list"][2] == [3, 4]
