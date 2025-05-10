import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import logging

log = logging.getLogger(__name__)
log.info("Loading calc_utils.py")

from scipy import optimize
from typing import Union
from dataclasses import dataclass
from .data_utils import OptimRes


def calculate_sharpe(
    ret: Union[float, np.ndarray], std: Union[float, np.ndarray], TBill: float
) -> Union[float, np.ndarray]:
    """
    Computes the Sharpe ratio for given returns, volatility, and risk-free rate.

    Parameters:
    ----------
    ret : float or np.ndarray
        Expected return(s) of the investment.
    std : float or np.ndarray
        Standard deviation(s) (volatility) of the investment returns.
    TBill : float
        Risk-free rate (e.g., yield on treasury bills).

    Returns:
    -------
    float or np.ndarray
        The Sharpe ratio, representing the risk-adjusted return.
    """
    log.debug(f"calculate_sharpe = {((ret - TBill) / std):.2f}")
    return (ret - TBill) / std


def minimize_variance(weights: np.ndarray, cov_matrix: np.ndarray) -> float:
    """
    Calculates the portfolio variance given asset weights and covariance matrix.

    Parameters:
    ----------
    weights : np.ndarray
        Array containing asset allocation weights.
    cov_matrix : np.ndarray
        Covariance matrix of asset returns.

    Returns:
    -------
    float
        The calculated variance of the portfolio.
    """
    variance = np.matmul(np.matmul(weights, cov_matrix), weights)
    log.debug(f"minimize_variance = {variance:.2f}")
    return variance


def weight_constraint(weights: np.ndarray) -> float:
    """
    Ensures the sum of portfolio weights equals exactly 1.

    Parameters:
    ----------
    weights : np.ndarray
        Array containing asset allocation weights.

    Returns:
    -------
    float
        The deviation from the target sum (should be 0 for a valid constraint).
    """
    log.debug(f"weight_constraint = {(np.sum(weights) - 1.0):.2f}")
    return np.sum(weights) - 1.0


def return_constraint(
    weights: np.ndarray, returns: np.ndarray, return_target: float
) -> float:
    """
    Ensures the expected portfolio return meets a specified target return.

    Parameters:
    ----------
    weights : np.ndarray
        Array containing asset allocation weights.
    returns : np.ndarray
        Array of expected returns for each asset.
    return_target : float
        The target return that the portfolio should achieve.

    Returns:
    -------
    float
        The deviation from the desired target return (should be 0 for a valid constraint).
    """
    log.debug(f"return_constraint = {(weights @ returns - return_target):.2f}")
    return weights @ returns - return_target


def markowitz_optimizer(df: pd.DataFrame, risk_free_rate: float = 3.5) -> OptimRes:
    """
    Optimizes a portfolio using the Markowitz optimization framework by finding the efficient frontier, which
    consists of portfolios that offer the highest expected return for a given level of risk.

    Parameters:
    ----------
    df : pd.DataFrame
        A DataFrame returned by the data_loader function, containing historical stock prices.

    risk_free_rate : float
        The annual risk-free rate, expressed as percentage (e.g., 3.0 for 3%). This rate is used in the calculation of the Sharpe ratio.

    Returns:
    -------
    OptimRes dataclass
        - res : optimize._optimize.OptimizeResult
            Return value from scipy optimization function
        - means : pd.Series
            The annualized mean returns for each stock, multiplied by 100 to convert to percentage form.
        - stds : pd.Series
            The annualized standard deviations for each stock, multiplied by 100 to convert to percentage form.
        - sharpe_array : List[float]
            A list of Sharpe ratios for the optimized portfolios, where each portfolio is targeted to a specific return.
        - return_array : List[float]
            A list of targeted returns for which the portfolio was optimized, expressed in percentage form.
        - variance_array : List[float]
            A list of annualized variances for each optimized portfolio, multiplied by 100 to convert to percentage form.

    Notes:
    -----
    The function performs several key operations:
    - It calculates the covariance matrix of the stock returns to understand how stocks move in relation to each other.
    - It standardizes returns and volatilities to an annual scale assuming 252 trading days, suitable for comparison and further analysis.
    - It uses a sequential quadratic programming method (SLSQP) to minimize the variance of the portfolio for a given return,
      constrained by the weights summing to 1 and achieving a specified return.
    - It iterates over a range of possible returns, optimizing the portfolio for each and calculating the corresponding Sharpe ratio.
    - The function assumes that the DataFrame's columns are well-prepared without any preprocessing required for missing data handling.

    """

    # w is for annualizing weekly returns and standard deviations
    w = 52.1429

    # Calculate covariance matrix and annualize returns and standard deviations
    cov_matrix = df.cov()
    means = df.mean().apply(lambda x: (x * w) * 100)
    stds = df.std().apply(lambda x: (x * np.sqrt(w)) * 100)

    # Initialize weights and set bounds for each weight
    lower_bound = 0.0
    upper_bound = 0.3
    weights = np.full(len(df.columns), 1 / len(df.columns))
    bounds = [(lower_bound, upper_bound)] * len(weights)

    return_array = []
    variance_array = []
    sharpe_array = []
    weights_out = []

    # Iterate through a range of possible returns
    returns_to_iterate_through = np.linspace(0, np.max(means.values), 40)

    log.debug(f"returns_to_iterate_through = {(returns_to_iterate_through)}")

    for ret in returns_to_iterate_through:
        # Define constraints for weight sum and targeted return
        cons = [
            {"type": "eq", "fun": weight_constraint},
            {"type": "eq", "fun": return_constraint, "args": (means.values, ret)},
        ]

        # Optimize the portfolio for minimum variance under the constraints
        res = optimize.minimize(
            minimize_variance,
            x0=weights,
            args=(cov_matrix,),
            method="SLSQP",
            constraints=cons,
            bounds=bounds,
        )

        if res.success:
            # Calculate Sharpe ratio and adjust variance to annualized percent form
            sharpe_ratio = calculate_sharpe(
                ret, np.sqrt(res.fun) * np.sqrt(w) * 100, risk_free_rate
            )
            sharpe_array.append(sharpe_ratio)
            return_array.append(ret)
            variance_array.append(np.sqrt(res.fun) * np.sqrt(w) * 100)
            weights_out.append(res.x)
            log.info("Optimization successful")

    log.info("Optimization returning")
    return OptimRes(
        np.array(weights_out), means, stds, sharpe_array, return_array, variance_array
    )
