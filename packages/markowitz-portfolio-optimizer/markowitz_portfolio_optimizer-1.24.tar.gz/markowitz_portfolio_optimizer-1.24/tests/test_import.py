import pandas as pd
import sys

sys.path.append("..")

from portfolio_optimizer.data_utils import data_loader


def test_data_loader():
    # Test the data_loader function
    df = data_loader("./demo/example_dataset.csv")

    # Check if the DataFrame is not empty
    assert not df.empty, "DataFrame should not be empty"

    # Check if the 'Date' column is in datetime format
    assert pd.api.types.is_datetime64_any_dtype(
        df.index
    ), "Date column should be in datetime format"

    # Check if the DataFrame has been resampled correctly
    assert df.index.freq == "W-SUN", "DataFrame should be resampled to weekly frequency"

    # Check if the DataFrame has no NaN values
    assert df.notna().all().all(), "DataFrame should not contain NaN values"
