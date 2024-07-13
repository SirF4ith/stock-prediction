from flask import Flask, jsonify, request
import yfinance as yf
from datetime import datetime
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Route for fetching historical stock data
@app.route('/stock-data-historic', methods=['GET'])
def get_stock_data_historic():
    """
    Retrieves historical stock data based on the provided ticker symbol, start date, and end date.
    Parameters:
        No parameters.
    
    Returns:
        JSON response containing historical stock data if successful, with appropriate error messages and status codes if there are issues.
    """
    ticker = request.args.get('ticker')
    start_date_str = request.args.get('startDate')
    end_date_str = request.args.get('endDate')

    if not (ticker and start_date_str and end_date_str):
        return jsonify({'error': 'Ticker symbol, start date, and end date are required'}), 400

    try:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD.'}), 400

    stock = yf.Ticker(ticker)
    stock_data = stock.history(start=start_date, end=end_date)

    if stock_data.empty:
        return jsonify({'error': f"No data found for ticker '{ticker}' between {start_date_str} and {end_date_str}"}), 404
    
    stock_data_json = stock_data.reset_index().to_json(orient='records')
    return jsonify(stock_data_json)


# Route for fetching actual stock data
@app.route('/stock-data-actual', methods=['GET'])
def get_stock_data_actual():
    """
    Route for fetching the last available closing price of a stock.
    """
    ticker = request.args.get('ticker')

    if not ticker:
        return jsonify({'error': 'Ticker symbol is required'}), 400

    stock = yf.Ticker(ticker)
    stock_data = stock.history(period="1d")  # Get the latest day's data

    if stock_data.empty:
        return jsonify({'error': f"No closing price data found for ticker '{ticker}'"}), 404

    last_close_price = stock_data['Close'].iloc[-1]  # Get the last close price
    return jsonify({'ticker': ticker, 'last_close_price': last_close_price})

# Route for web scraping news

# Need to adjust the route
@app.route('/get-news', methods=['GET'])
def get_news():
    """
    Fetches news articles from a specified URL, extracts the titles and content from HTML, and returns them in a list of dictionaries.
    """
    url = request.args.get('url')
    if not url:
        url =  'https://www.economist.com/'  # Replace with the actual news website URL                                     
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract news articles from the HTML
    news_articles = []
    for article in soup.find_all('article'):
        title = article.find('h2').text
        content = article.find('div', {'class': 'content'}).text
        news_articles.append({'title': title, 'content': content})

    return jsonify(news_articles)

# Route for stock prediction
'''@app.route('/predict-stock', methods=['POST'])
def predict_stock():
    """
    A route to predict stock prices using a machine learning model or script.
    Fetches data from the request in JSON format, predicts stock prices using the model, and returns the predicted prices.
    """
    data = request.get_json()
    # Call your machine learning model or script to predict stock prices
    predicted_prices = ml_model.predict(data)
    return jsonify(predicted_prices)'''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
