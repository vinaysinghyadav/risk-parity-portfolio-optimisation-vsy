# Risk Parity Portfolio Optimization

This Streamlit app helps you calculate and visualize the **Risk Parity Portfolio** for a given set of assets. It allows you to input stock tickers, select a data period, and calculate portfolio weights, returns, and investment allocations. You can also visualize the risk-return tradeoff of different portfolios, optimized based on risk parity principles.

## Made by Vinay Singh Yadav

## Features

- **Risk Parity Weights**: Calculates portfolio weights based on the risk parity principle, ensuring that each asset contributes equally to the portfolio's risk.
- **Simulated Portfolios**: Simulates thousands of portfolio combinations to find the optimal portfolio for the selected assets.
- **Investment Allocation**: Shows how much to invest in each asset based on the calculated risk parity weights and the entered principal amount.
- **Interactive Visuals**: Displays a risk-return tradeoff graph. You can hover over any point to see the return and volatility (risk) for that portfolio.
- **Sharpe Ratio**: Calculates and displays the Sharpe ratio for the risk parity portfolio to evaluate its risk-adjusted return.

## Installation

### Prerequisites

- Python 3.x
- Install the necessary Python libraries by running the following:

```bash
pip install streamlit yfinance pandas numpy matplotlib plotly
```


## Running the App

1. Clone this repository or download the script to your local machine.
2. Open a terminal/command prompt and navigate to the directory where the script is saved.
3. Run the following command to start the Streamlit app:

```bash
streamlit run risk_parity_app.py
```
## Usage

- **Stock Tickers**: Enter a list of stock tickers (separated by commas) that you want to include in your portfolio.
- **Data Period**: Choose how much historical data to use for calculating returns. Options include:
  - 1 month
  - 3 months
  - 6 months
  - 1 year
- **Principal Amount**: Enter the amount of money you want to invest in the portfolio (e.g., $10,000).

The app will display the Risk Parity Weights, optimal portfolio performance, and investment allocation for each asset in your portfolio.


## Example

- Input stock tickers like `MSFT`, `AAPL`, `LLY`, `CVX`, `BHP`.
- Choose a data period (e.g., `1y` for 1 year).
- Enter a principal amount (e.g., `$10,000`).
- View the risk parity portfolio weights, optimal portfolio performance, and how to allocate your principal across the assets.

## Technologies Used

- **Streamlit**: For building the web app interface.
- **yfinance**: For fetching historical stock price data.
- **Pandas**: For data manipulation and calculations.
- **NumPy**: For numerical operations like matrix manipulation.
- **Matplotlib**: For plotting static graphs.
- **Plotly**: For creating interactive visualizations of portfolios.

## Contributing

Feel free to fork this repository, make changes, and create a pull request. Contributions are welcome!

## License

This project is licensed under the MIT License - see the LICENSE file for details.



