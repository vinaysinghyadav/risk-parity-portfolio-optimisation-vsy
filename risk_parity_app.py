import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from PIL import Image

# Title and Description
st.title("Risk Parity Portfolio Optimization")
st.write("""
This app helps you calculate the Risk Parity Portfolio for a given set of assets. 
You can input your stock tickers (separated by commas), select how much historical data to use, and calculate portfolio weights, returns, and allocation.
""")
st.write('<p style="color:blue;">Made by Vinay Singh Yadav</p>', unsafe_allow_html=True)

# Add Streamlit logo in sidebar with smaller size
st.sidebar.image("https://streamlit.io/images/brand/streamlit-mark-color.png", width=150)

# Sidebar Inputs
st.sidebar.header("Portfolio Settings")
tickers_input = st.sidebar.text_input("Enter Stock Tickers (comma separated)", "MSFT, AAPL, LLY, CVX, BHP")

# Convert the input string to a list of tickers
tickers = [ticker.strip() for ticker in tickers_input.split(",")]

# Custom data period selection (months)
data_period = st.sidebar.selectbox("Select Data Period", ["1mo", "3mo", "6mo", "1y"], index=0)

# Principal amount input
principal_amount = st.sidebar.number_input("Enter Your Principal Amount ($)", min_value=1, value=10000)

# Function to fetch stock data
def fetch_data(tickers, period):
    stock_data = {}
    for ticker in tickers:
        try:
            # Fetching stock data for the selected period
            stock_data[ticker] = yf.download(ticker, period=period)['Close']  # Use 'Close' prices
            if stock_data[ticker].empty:
                st.warning(f"No data found for {ticker}")
            else:
                st.success(f"Successfully fetched data for {ticker}")
        except Exception as e:
            st.error(f"Error fetching data for {ticker}: {e}")
    
    # Check if any data is available
    if stock_data:
        st.success("Data fetched successfully for all tickers.")
        
        # Align data by date (index) to ensure all dataframes have the same dates
        aligned_data = pd.concat(stock_data, axis=1)
        
        # Remove rows with missing data (if any)
        aligned_data = aligned_data.dropna()
        
        return aligned_data
    else:
        st.error("No data available. Please check tickers or connection.")
        return pd.DataFrame()  # Return empty DataFrame if no data

# Function to calculate risk parity portfolio weights
def calculate_risk_parity_weights(cov_matrix):
    inv_volatility = 1 / np.sqrt(np.diag(cov_matrix))
    inv_volatility /= np.sum(inv_volatility)  # Normalize to sum to 1
    return inv_volatility

# Function to calculate portfolio return and risk
def calculate_portfolio_performance(weights, mean_returns, cov_matrix):
    port_return = np.sum(mean_returns * weights)
    port_volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
    return port_return, port_volatility

# Function to simulate portfolios for optimization
def simulate_portfolios(mean_returns, cov_matrix, num_portfolios=10000):
    results = np.zeros((3, num_portfolios))
    for i in range(num_portfolios):
        weights = np.random.random(len(mean_returns))
        weights /= np.sum(weights)
        
        portfolio_return, portfolio_volatility = calculate_portfolio_performance(weights, mean_returns, cov_matrix)
        results[0, i] = portfolio_return
        results[1, i] = portfolio_volatility
        results[2, i] = np.sum(weights)  # This is for weight sum, just for checking
    return results

# Fetch the data and show it
data = fetch_data(tickers, data_period)

# If data is available, proceed with portfolio calculations
if not data.empty:
    st.write("### Fetched Stock Price Data")
    st.dataframe(data)
    
    # Calculate mean returns and covariance matrix
    mean_returns = data.pct_change().mean()
    cov_matrix = data.pct_change().cov()

    # Calculate risk parity weights
    risk_parity_weights = calculate_risk_parity_weights(cov_matrix)
    st.write(f"### Risk Parity Portfolio Weights:")
    st.write(risk_parity_weights)

    # Simulate portfolios to find optimal portfolio
    results = simulate_portfolios(mean_returns, cov_matrix)
    
    # Extract optimal portfolio based on max return for given risk
    max_return_idx = np.argmax(results[0])
    optimal_portfolio = results[:, max_return_idx]
    
    # Display optimal portfolio data
    st.write("### Optimal Portfolio:")
    st.write(f"Return: {optimal_portfolio[0]:.2%}")
    st.write(f"Volatility: {optimal_portfolio[1]:.2%}")
    
    # Display the amount to invest in each asset based on the principal
    st.write("### Investment Allocation based on Your Principal Amount")
    allocation = risk_parity_weights * principal_amount
    allocation_df = pd.DataFrame(allocation, index=data.columns, columns=["Investment ($)"])
    st.dataframe(allocation_df)

    # Plotting the risk-return tradeoff with Plotly
    fig = go.Figure()

    # Scatter plot of all portfolios
    fig.add_trace(go.Scatter(
        x=results[1, :],
        y=results[0, :],
        mode='markers',
        marker=dict(
            size=5,
            color=results[0, :]/results[1, :],  # Color by Sharpe Ratio
            colorscale='Viridis',
            colorbar=dict(title="Sharpe Ratio")
        ),
        text=[f"Return: {r:.2%}, Risk: {vol:.2%}" for r, vol in zip(results[0, :], results[1, :])],
        hoverinfo='text'
    ))

    # Scatter plot of the optimal portfolio
    fig.add_trace(go.Scatter(
        x=[optimal_portfolio[1]],
        y=[optimal_portfolio[0]],
        mode='markers',
        marker=dict(
            size=12,
            color='red',
            symbol='star',
            line=dict(width=2, color='black')
        ),
        name="Optimal Portfolio",
        text=[f"Return: {optimal_portfolio[0]:.2%}, Volatility: {optimal_portfolio[1]:.2%}"],
        hoverinfo='text'
    ))

    # Layout configuration
    fig.update_layout(
        title="Simulated Portfolio Optimization",
        xaxis_title="Risk (Volatility)",
        yaxis_title="Return",
        template="plotly_dark",
        showlegend=True
    )

    # Show the Plotly graph in the Streamlit app
    st.plotly_chart(fig)
