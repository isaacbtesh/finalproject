from flask import Flask, render_template, request
import matplotlib

matplotlib.use("Agg")  # Set the Matplotlib backend to 'Agg'
import matplotlib.pyplot as plt
import io
import base64
from openai import OpenAI
from config import api_gpt_key
from main import (
    plot_close_price_history,
    plot_daily_return_histogram,
    plot_price_comparison,
    plot_volume_chart,
    plot_candlestick_chart,
)

"""Import Flask class to create the app, render_template to render HTML templates,
 and request to handle request data.
Import the matplotlib library for plotting and sets the Agg backend,
which is a non-GUI backend suitable for script and server environments.
Import the pyplot module from matplotlib for plotting graphs.
Import the io module for handling byte streams/used for converting plots to images
Import the base64 module for encoding binary data to encode images
Import the OpenAI class for interacting with OpenAI's GPT-3 API.
Import api_gpt_key from a config module
Import the graph plotting functions defined in main.py
"""
app = Flask(__name__)


def get_graph():
    """Function to convert matplotlib plot to base64 encoded image for embedding in HTML"""
    img = io.BytesIO()  # Create an in-memory binary stream object img
    plt.savefig(
        img, format="png", bbox_inches="tight"
    )  # Save the matplotlib figure to the binary stream img in PNG format
    img.seek(0)  # Reset the file pointer to the beginning of the stream
    graph_url = base64.b64encode(
        img.getvalue()
    ).decode()  # Encode the image in img as a base64 string and decode it to UTF-8 format.
    return "data:image/png;base64,{}".format(
        graph_url
    )  # Return the base64 string in a format that can be embedded in HTML


# Function to fetch company information using GPT-3
def fetch_gpt_data(ticker):
    """retrieve company information using GPT-3 for a stock ticker"""
    client = OpenAI(api_key=api_gpt_key)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": f"In three bullet points tell me basic company information about {ticker}",
            }
        ],
        stream=False,
    )
    return response.choices[0].message.content


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        user_tickers = (
            request.form.get("tickers").upper().split(",")
        )  # Retrieve comma-separated list of tickers from form data, convert to uppercase, splits it into a list.
        start_date = request.form.get("start_date")
        end_date = request.form.get(
            "end_date"
        )  # Retrieve the start and end dates from the form data.
        user_tickers = [
            ticker.strip() for ticker in user_tickers
        ]  # Strip whitespace from each ticker symbol.
        selected_graphs = request.form.getlist(
            "graph_type"
        )  # Retrieve a list of selected graph types from the form data.
        all_graphs_and_responses = (
            {}
        )  # Initialize a dictionary to store graphs and GPT-3 responses.
        if (
            "price_comparison" in selected_graphs
        ):  # Check if the price comparison graph is selected
            plot_price_comparison(
                user_tickers, start_date, end_date
            )  # Plot the price comparison graph for the specified tickers and dates.
            all_graphs_and_responses["Price Comparison"] = [
                ("Price Comparison Graph", get_graph())
            ]  # Store the price comparison graph in the dictionary.
            plt.close()  # Close the matplotlib plot to free up memory.
        for ticker in user_tickers:  # Loop through each ticker symbol.
            graphs_and_responses = (
                []
            )  # Initialize a list to store graphs and responses for each ticker.
            if (
                "close_price" in selected_graphs
            ):  # Check if the close price graph is selected.
                plot_close_price_history(
                    ticker, start_date, end_date
                )  # Plot the close price history graph.
                graphs_and_responses.append(
                    ("Close Price History", get_graph())
                )  # Appends the close price history graph to the list.
            # same logic in each if
            if "daily_return" in selected_graphs:
                plot_daily_return_histogram(ticker, start_date, end_date)
                graphs_and_responses.append(("Daily Return Histogram", get_graph()))
            if "volume_chart" in selected_graphs:
                plot_volume_chart(ticker, start_date, end_date)
                graphs_and_responses.append(("Volume Chart", get_graph()))
            if "candlestick_chart" in selected_graphs:
                plot_candlestick_chart(ticker, start_date, end_date)
                graphs_and_responses.append(("Candlestick Chart", get_graph()))
            # Fetch GPT-3 response for the ticker
            gpt_response = fetch_gpt_data(
                ticker
            )  # Fetch GPT-3 response for the ticker.
            graphs_and_responses.append(
                ("GPT-3 Response", gpt_response)
            )  # Append the GPT-3 response to the list.
            all_graphs_and_responses[
                ticker
            ] = graphs_and_responses  # Store the graphs and responses for the ticker in the dictionary.
        return render_template(
            "graphs.html", all_graphs_and_responses=all_graphs_and_responses
        )
    # Render the graphs.html template with the graphs and responses.
    else:
        return render_template("index.html")


@app.errorhandler(404)
def not_found_error(error):
    return render_template("errorpage.html"), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template("errorpage.html"), 500


if __name__ == "__main__":
    app.run(debug=True)
