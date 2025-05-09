import pandas as pd
import numpy as np
import sys

sys.path.append("..")

from portfolio_optimizer.data_utils import data_loader
from portfolio_optimizer.calc_utils import markowitz_optimizer

from tests import HOLDER


def test_optimizer():
    # Load the dataset
    df = data_loader("./demo/example_dataset.csv")

    # run optimizer
    res = markowitz_optimizer(df)

    # Check if the result is not empty
    assert res is not None, "Optimizer result should not be None"

    # Check if weights are add up to 1
    assert (
        abs(sum(res.weights[np.argmax(res.sharpe_array), :]) - 1.0) < 1e-6
    ), "Weights should sum to 1"

    # Check if the result contains all tickers
    assert all(
        res.means.index.values == df.columns.values
    ), "Result should contain all tickers"
