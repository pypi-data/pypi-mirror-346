import os
import sys
import unittest

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from sega_learn.utils.dataPreprocessing import (
    Scaler,
    _find_categorical_columns,
    normalize,
    one_hot_encode,
)
from tests.utils import BaseTest


class TestScaler(BaseTest):
    """Unit test for the Scaler class in the data preprocessing module."""

    @classmethod
    def setUpClass(cls):  # NOQA D201
        print("\nTesting Scaler", end="", flush=True)

    def setUp(self):
        """Set up test data and initialize Scaler instances for testing."""
        self.data = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        self.scaler_standard = Scaler(method="standard")
        self.scaler_minmax = Scaler(method="minmax")
        self.scaler_normalize = Scaler(method="normalize")

    def test_standard_scaling(self):
        """Test standard scaling to ensure mean is 0 and standard deviation is 1."""
        self.scaler_standard.fit(self.data)
        transformed = self.scaler_standard.transform(self.data)
        self.assertTrue(np.allclose(np.mean(transformed, axis=0), 0, atol=1e-7))
        self.assertTrue(np.allclose(np.std(transformed, axis=0), 1, atol=1e-7))

    def test_standard_scaling_inverse(self):
        """Test inverse transformation of standard scaling to ensure it returns original data."""
        self.scaler_standard.fit(self.data)
        transformed = self.scaler_standard.transform(self.data)
        inverse = self.scaler_standard.inverse_transform(transformed)
        self.assertTrue(np.allclose(inverse, self.data))

    def test_minmax_scaling(self):
        """Test min-max scaling to ensure data is scaled between 0 and 1."""
        self.scaler_minmax.fit(self.data)
        transformed = self.scaler_minmax.transform(self.data)
        self.assertTrue(np.allclose(np.min(transformed, axis=0), 0, atol=1e-7))
        self.assertTrue(np.allclose(np.max(transformed, axis=0), 1, atol=1e-7))

    def test_minmax_scaling_inverse(self):
        """Test inverse transformation of min-max scaling to ensure it returns original data."""
        self.scaler_minmax.fit(self.data)
        transformed = self.scaler_minmax.transform(self.data)
        inverse = self.scaler_minmax.inverse_transform(transformed)
        self.assertTrue(np.allclose(inverse, self.data))

    def test_normalize_scaling(self):
        """Test normalization to ensure each row has a unit norm."""
        self.scaler_normalize.fit(self.data)
        transformed = self.scaler_normalize.transform(self.data)
        norms = np.linalg.norm(transformed, axis=1)
        self.assertTrue(np.allclose(norms, 1, atol=1e-7))

    def test_normalize_scaling_inverse(self):
        """Test inverse transformation of normalization to ensure it returns original data."""
        self.scaler_normalize.fit(self.data)
        transformed = self.scaler_normalize.transform(self.data)
        inverse = self.scaler_normalize.inverse_transform(transformed)
        self.assertTrue(np.allclose(inverse, self.data))

    def test_fit_transform(self):
        """Test fit_transform method for standard scaling."""
        transformed = self.scaler_standard.fit_transform(self.data)
        self.assertTrue(np.allclose(np.mean(transformed, axis=0), 0, atol=1e-7))
        self.assertTrue(np.allclose(np.std(transformed, axis=0), 1, atol=1e-7))

    def test_invalid_method(self):
        """Test that an invalid scaling method raises a ValueError."""
        with self.assertRaises(ValueError):
            Scaler(method="invalid")

    def test_transform_without_fit(self):
        """Test that calling transform without fitting raises a TypeError."""
        scaler = Scaler(method="standard")
        with self.assertRaises(TypeError):
            scaler.transform(self.data)

    def test_inverse_transform_without_fit(self):
        """Test that calling inverse_transform without fitting raises a TypeError."""
        scaler = Scaler(method="standard")
        with self.assertRaises(TypeError):
            scaler.inverse_transform(self.data)


class TestCataPreprocessingFuncs(BaseTest):
    """Unit test for categorical preprocessing functions in the data preprocessing module."""

    @classmethod
    def setUpClass(cls):  # NOQA D201
        print("\nTesting Categorical Preprocessing Functions", end="", flush=True)

    def setUp(self):
        """Set up test data for categorical preprocessing functions."""
        self.data_df = pd.DataFrame(
            {"A": ["cat", "dog", "cat"], "B": [1, 2, 3], "C": ["red", "blue", "red"]}
        )
        self.data_np = np.array(
            [["cat", 1, "red"], ["dog", 2, "blue"], ["cat", 3, "red"]], dtype=object
        )

    def test_one_hot_encode_dataframe(self):
        """Test one-hot encoding on a pandas DataFrame."""
        encoded = one_hot_encode(self.data_df, cols=[0, 2])
        self.assertIn("cat", encoded.columns)
        self.assertIn("dog", encoded.columns)
        self.assertIn("red", encoded.columns)
        self.assertIn("blue", encoded.columns)
        self.assertNotIn("A", encoded.columns)
        self.assertNotIn("C", encoded.columns)

    def test_one_hot_encode_numpy(self):
        """Test one-hot encoding on a numpy array."""
        encoded = one_hot_encode(self.data_np, cols=[0, 2])
        self.assertEqual(
            encoded.shape[1], 5
        )  # 2 original columns dropped, 4 one-hot columns added

    def test_find_categorical_columns_dataframe(self):
        """Test finding categorical columns in a pandas DataFrame."""
        categorical_cols = _find_categorical_columns(self.data_df)
        self.assertEqual(categorical_cols, [0, 2])

    def test_find_categorical_columns_numpy(self):
        """Test finding categorical columns in a numpy array."""
        categorical_cols = _find_categorical_columns(self.data_np)
        self.assertEqual(categorical_cols, [0, 2])

    def test_normalize_l2(self):
        """Test L2 normalization."""
        data = np.array([[1, 2], [3, 4]])
        normalized = normalize(data, norm="l2")
        norms = np.linalg.norm(normalized, axis=1)
        self.assertTrue(np.allclose(norms, 1, atol=1e-7))

    def test_normalize_l1(self):
        """Test L1 normalization."""
        data = np.array([[1, 2], [3, 4]])
        normalized = normalize(data, norm="l1")
        norms = np.sum(np.abs(normalized), axis=1)
        self.assertTrue(np.allclose(norms, 1, atol=1e-7))

    def test_normalize_max(self):
        """Test max normalization."""
        data = np.array([[1, 2], [3, 4]])
        normalized = normalize(data, norm="max")
        max_values = np.max(np.abs(normalized), axis=1)
        self.assertTrue(np.allclose(max_values, 1, atol=1e-7))

    def test_normalize_minmax(self):
        """Test min-max normalization."""
        data = np.array([[1, 2], [3, 4]])
        normalized = normalize(data, norm="minmax")
        self.assertTrue(np.allclose(np.min(normalized, axis=1), 0, atol=1e-7))
        self.assertTrue(np.allclose(np.max(normalized, axis=1), 1, atol=1e-7))

    def test_normalize_invalid_norm(self):
        """Test that an invalid normalization method raises a ValueError."""
        data = np.array([[1, 2], [3, 4]])
        with self.assertRaises(ValueError):
            normalize(data, norm="invalid")


if __name__ == "__main__":
    unittest.main()
