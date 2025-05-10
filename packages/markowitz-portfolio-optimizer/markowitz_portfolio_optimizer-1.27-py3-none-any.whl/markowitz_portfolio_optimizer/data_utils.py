import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import logging

log = logging.getLogger(__name__)
log.info("Loading data_utils.py")

from scipy import optimize
from dataclasses import dataclass
from matplotlib import ticker


def data_loader(df_name: str) -> pd.DataFrame:
    """
    Processes stock price data in a DataFrame by converting dates and resampling to monthly frequency.

    Parameters:
    ----------
    df : pd.DataFrame
        A DataFrame containing stock price data. Must include a 'Date' column representing daily dates, and other columns corresponding to stock tickers with their daily prices as floats.

    Returns:
    -------
    pd.DataFrame
        A DataFrame indexed by weekly dates (using the first day of each month), where each stock column's value is the first available daily price in each month.

    Notes:
    -----
    - The function infers appropriate data types for each column.
    - The 'Date' column is converted to datetime format and set as the DataFrame index.
    - Weekly resampling is performed with the resampled period labeled and closed on the left.
    """
    df = pd.read_csv(df_name)

    log.debug(f"DataFrame shape: {df.shape}")
    log.debug(f"DataFrame columns: {df.columns}")

    df = df.dropna(axis=0, how="all")
    df = df.infer_objects()
    df["Date"] = pd.to_datetime(df["Date"])
    df.set_index("Date", drop=True, inplace=True)
    df = df.resample("W", label="left", closed="left").first()
    df = df.diff() / df.shift(1)
    df = df.dropna()
    return df


@dataclass
class OptimRes:

    log.info("Loading OptimRes class")

    weights: np.ndarray
    means: np.ndarray
    stds: np.ndarray
    sharpe_array: np.ndarray
    return_array: np.ndarray
    variance_array: np.ndarray

    def plot_efficient_horizon(self, ax) -> None:
        """
        Plots the efficient frontier along with individual asset points and the point with the maximum Sharpe ratio.
        """
        # Scatter plot for the variance and return of each optimized portfolio
        ax.plot(
            self.variance_array,
            self.return_array,
            "--",
            label="Efficient frontier under constraints",
        )

        # Scatter plot for the standard deviations and means of individual assets
        ax.scatter(self.stds, self.means, color="blue", label="Individual Assets")

        # Highlight the portfolio with the maximum Sharpe ratio
        max_sharpe_idx = np.argmax(self.sharpe_array)
        ax.scatter(
            self.variance_array[max_sharpe_idx],
            self.return_array[max_sharpe_idx],
            color="red",
            label="Max Sharpe Ratio",
        )
        ax.annotate(
            f"Sharpe = {max(self.sharpe_array):0.2f}",
            xy=(self.variance_array[max_sharpe_idx], self.return_array[max_sharpe_idx]),
        )

        # Add labels and legend
        ax.set_xlabel("Variance (%)")
        ax.set_ylabel("Returns (%)")
        ax.set_xlim(0, max(self.stds) * 1.1)
        ax.set_ylim(min(0, min(self.means)), max(self.means) * 1.1)
        ax.set_title("Efficient Frontier with Individual Assets")
        for i, txt in enumerate(self.means.index):
            ax.annotate(txt, (self.stds[i], self.means[i]))
        ax.legend()

    def plot_optimal_weights(self, ax) -> None:
        """
        Plots the optimal weights for the portfolio with the maximum Sharpe ratio.
        """
        # Bar plot for the optimal weights
        ax.bar(self.means.index, self.weights[np.argmax(self.sharpe_array), :])
        ax.set_ylabel("Weights")
        ax.set_title("Optimal Weights for Maximum Sharpe Ratio Portfolio")
        ax.yaxis.set_minor_locator(ticker.MultipleLocator(0.25))
