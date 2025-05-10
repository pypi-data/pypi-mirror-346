# Portfolio Optimizer

This project implements the simple Markowitz portfolio optimization model.
It is the foundation of modern portfolio theory.

The assumptions of the model are:

1. Risk of a portfolio is based on the variability of returns from said portfolio.
2. An investor is risk averse.
3. An investor prefers to increase consumption.
4. The investor's utility function is concave and increasing, due to their risk aversion and consumption preference.
5. Analysis is based on single period model of investment.
6. An investor either maximizes their portfolio return for a given level of risk or minimizes their risk for a given return.
7. An investor is rational in nature.

More information on theory and calculations can be found on:
https://en.wikipedia.org/wiki/Modern_portfolio_theory

The algorithm needs a timestamped dataset of stock prices,
which can be obtained from Yahoo Finance, Google Finance or other sources.
A sample table structure is as follows:

<div align="center">
<img src="https://github.com/SirArthur100/scientific_python/raw/main/docs/source/images/table.png" width="50%">
</div>

The algorithm will provide the efficient frontier visually:

<div align="center">
<img src="https://github.com/SirArthur100/scientific_python/raw/main/docs/source/images/illustration.png" width="50%">
</div>

and the optimal portfolio weights numerically:

<div align="center">
<img src="https://github.com/SirArthur100/scientific_python/raw/main/docs/source/images/weights.png" width="50%">
</div>

## Requirements
- numpy==1.26.3
- pandas==2.1.4
- matplotlib==3.8.1
- scipy==1.11.4

## Documentation
https://portfolio-optimizer.readthedocs.io/en/latest/

## Source
https://github.com/SirArthur100/scientific_python
