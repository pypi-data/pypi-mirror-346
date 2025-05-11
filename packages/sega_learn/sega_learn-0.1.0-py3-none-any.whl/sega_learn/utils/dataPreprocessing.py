import numpy as np
import pandas as pd


def one_hot_encode(X, cols=None):
    """One-hot encodes non-numerical columns in a DataFrame or numpy array.

    Drops the original columns after encoding.

    Args:
        X: (pandas.DataFrame or numpy.ndarray) - The data to be encoded.
        cols: (list), optional - The list of column indices to be encoded (default is None).
            If None, all non-numerical columns will be encoded.

    Returns:
        X: (pandas.DataFrame or numpy.ndarray) - The data with one-hot encoded columns.
    """
    is_dataframe = isinstance(X, pd.DataFrame)
    if not is_dataframe:
        X = pd.DataFrame(X)  # Convert to DataFrame if not already

    if cols is None:
        cols = _find_categorical_columns(X)
    if len(cols) == 0:
        return X

    new_columns = []
    for col in cols:  # For each column index
        unique_values = X.iloc[:, col].unique()  # Get the unique values in the column
        for value in unique_values:  # For each unique value, create a new binary column
            new_columns.append((X.iloc[:, col] == value).astype(int).rename(str(value)))

    X = pd.concat(
        [X.drop(X.columns[cols], axis=1)] + new_columns, axis=1
    )  # Drop the original columns and add new columns

    if not is_dataframe:
        return (
            X.values
        )  # Convert back to numpy array if it was originally a numpy array
    return X  # Else, return the DataFrame


def _find_categorical_columns(X):
    """Finds the indices of non-numerical columns in a DataFrame or numpy array.

    Args:
        X: (pandas.DataFrame or numpy.ndarray) - The data to be checked.

    Returns:
        categorical_cols: (list) - The list of indices of non-numerical columns.
    """
    if isinstance(X, np.ndarray):
        X = pd.DataFrame(X)  # Convert to DataFrame if not already

    # For each column, try to convert it to numeric
    # If it fails, it is a categorical column
    categorical_cols = []
    for i in range(X.shape[1]):
        try:
            pd.to_numeric(X.iloc[:, i])
        except ValueError:
            categorical_cols.append(i)
    return categorical_cols  # Return the list of indices of non-numerical columns


def normalize(X, norm="l2"):
    """Normalizes the input data using the specified norm.

    Args:
        X: (numpy.ndarray) - The input data to be normalized.
        norm: (str), optional - The type of norm to use for normalization (default is 'l2').
            Options:
                - 'l2': L2 normalization (Euclidean norm).
                - 'l1': L1 normalization (Manhattan norm).
                - 'max': Max normalization (divides by the maximum absolute value).
                - 'minmax': Min-max normalization (scales to [0, 1]).

    Returns:
        X: (numpy.ndarray) - The normalized data.
    """
    # Ensure the data is in the correct shape and type
    if isinstance(X, pd.DataFrame):
        X = X.values
    if isinstance(X, pd.Series):
        X = X.values.reshape(-1, 1)
    if X.ndim == 1:
        X = X.reshape(-1, 1)
    elif X.ndim > 2:
        raise ValueError("Input data must be 1D or 2D.")

    if norm == "l2":
        norms = np.linalg.norm(X, axis=1, keepdims=True)
        norms[norms == 0] = 1  # Avoid division by zero
        X = X / norms
    elif norm == "l1":
        norms = np.sum(np.abs(X), axis=1, keepdims=True)
        norms[norms == 0] = 1  # Avoid division by zero
        X = X / norms
    elif norm == "max":
        max_values = np.max(np.abs(X), axis=1, keepdims=True)
        max_values[max_values == 0] = 1  # Avoid division by zero
        X = X / max_values
    elif norm == "minmax":
        min_values = np.min(X, axis=1, keepdims=True)
        max_values = np.max(X, axis=1, keepdims=True)
        range_values = max_values - min_values
        range_values[range_values == 0] = 1  # Avoid division by zero
        X = (X - min_values) / range_values
    else:
        raise ValueError(f"Unsupported norm: {norm}")
    return X


class Scaler:
    """A class for scaling data by standardization and normalization."""

    def __init__(self, method="standard"):
        """Initializes the scaler with the specified method.

        Args:
            method: (str) - The scaling method to use. Options are 'standard', 'minmax', or 'normalize'.
        """
        if method not in ["standard", "minmax", "normalize"]:
            raise ValueError(f"Unsupported method: {method}")

        self.method = method
        self.mean = None
        self.std = None
        self.min = None
        self.max = None
        self.norm = None

    def fit(self, X):
        """Fits the scaler to the data.

        Args:
            X: (numpy.ndarray) - The data to fit the scaler to.
        """
        if self.method == "standard":
            self.mean = np.mean(X, axis=0)
            self.std = np.std(X, axis=0)
        elif self.method == "minmax":
            self.min = np.min(X, axis=0)
            self.max = np.max(X, axis=0)
        elif self.method == "normalize":
            norms = np.linalg.norm(X, axis=1)
            norms[norms == 0] = 1  # Avoid division by zero
            self.norm = norms
        else:
            raise ValueError(f"Unsupported method: {self.method}")

    def transform(self, X):
        """Transforms the data using the fitted scaler.

        Args:
            X: (numpy.ndarray) - The data to transform.

        Returns:
            X_transformed: (numpy.ndarray) - The transformed data.
        """
        if self.method == "standard":
            return (X - self.mean) / (self.std + 1e-8)
        elif self.method == "minmax":
            return (X - self.min) / (self.max - self.min + 1e-8)
        elif self.method == "normalize":
            return X / (self.norm[:, np.newaxis] + 1e-8)

    def fit_transform(self, X):
        """Fits the scaler to the data and then transforms it.

        Args:
            X: (numpy.ndarray) - The data to fit and transform.

        Returns:
            X_transformed: (numpy.ndarray) - The transformed data.
        """
        self.fit(X)
        return self.transform(X)

    def inverse_transform(self, X):
        """Inverse transforms the data using the fitted scaler.

        Args:
            X: (numpy.ndarray) - The data to inverse transform.

        Returns:
            X_inverse: (numpy.ndarray) - The inverse transformed data.
        """
        if self.method == "standard":
            return X * self.std + self.mean
        elif self.method == "minmax":
            return X * (self.max - self.min) + self.min
        elif self.method == "normalize":
            return X * (self.norm[:, np.newaxis] + 1e-8)


# TODO: Add data imputation methods/functions
