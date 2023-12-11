import yfinance as yf
import matplotlib.pyplot as plt
import seaborn as sns
import mplfinance as mpf


def plot_close_price_history(ticker_symbol, start_date, end_date):
    """
    This is a function that displays the closing price history of the tickers user inputs with the start date and end date the user inputs,
    it gets the data from yahoo finance (yf) and displays the graph by getting help from matplotlib
    """
    data = yf.Ticker(ticker_symbol).history(
        start=start_date, end=end_date
    )  # historical stock data for the given ticker_symbol from Yahoo Finance in the specified timeframe
    plt.figure(figsize=(14, 7))  # figure size
    plt.plot(data["Close"])  # Plot the closing prices from the fetched data
    plt.title(f"Close Price History of {ticker_symbol}")
    plt.xlabel("Date")
    plt.ylabel("Close Price")  # neccesary axis names and titel for the graph


def plot_daily_return_histogram(ticker_symbol, start_date, end_date):
    """
    A function to plot a histogram of daily returns for a given stock
    """
    data = yf.Ticker(ticker_symbol).history(
        start=start_date, end=end_date
    )  # historical stock data for the given ticker_symbol from Yahoo Finance in the specified timeframe
    data["Daily Return"] = data[
        "Close"
    ].pct_change()  # Calculates the daily percentage change in closing price/stores it in a new column called 'Daily Return'
    plt.figure(figsize=(14, 7))
    sns.histplot(
        data["Daily Return"].dropna(), bins=100, color="purple"
    )  # Use Seaborn to plot a histogram of Daily Return column, exclude Na values. The histogram has 100 bins/ is colored purple.
    plt.title(f"Histogram of Daily Returns for {ticker_symbol}")


def plot_volume_chart(ticker_symbol, start_date, end_date):
    """
    A function to plot a volume chart for a given stock
    """
    data = yf.Ticker(ticker_symbol).history(start=start_date, end=end_date)
    plt.figure(figsize=(14, 7))
    plt.bar(
        data.index, data["Volume"], color="blue"
    )  # Plot a bar chart of the volume column representing the stock's trading volume.
    plt.title(f"Volume Chart for {ticker_symbol}")
    plt.xlabel("Date")
    plt.ylabel("Volume")


def plot_candlestick_chart(ticker_symbol, start_date, end_date):
    """
    A function to plot a candlestick chart for a given stock
    """
    data = yf.Ticker(ticker_symbol).history(start=start_date, end=end_date)
    mpf.plot(
        data,
        type="candle",
        style="charles",
        title=f"Candlestick Chart for {ticker_symbol}",
        volume=True,
        figsize=(14, 7),
    )
    # Use mplfinance to plot a type: candlestick chart. The chart includes volume data/uses style charles


def plot_price_comparison(tickers, start_date, end_date):
    """
    A function to plot a price comparison chart for multiple stocks
    """
    data = yf.download(tickers, start=start_date, end=end_date)["Close"]
    plt.figure(figsize=(14, 7))
    data.plot()  # Plot the closing prices of the stocks for comparison.
    plt.title("Closing Prices Comparison")
    plt.ylabel("Price ($)")
    plt.xlabel("Date")
