const express = require('express');
const app = express();
const path = require('path');

// Function to fetch stock data
const fetchStockData = (req, res) => {
  console.log('Request started');
  const ticker = req.query.ticker;
  const startDate = req.query.startDate;
  const endDate = req.query.endDate;

  if (!ticker) {
    console.log('Invalid request');
    return res.status(400).send('Ticker symbol is required');
  }

  let url;
  if (startDate && endDate) {
    url = `http://localhost:5000/stock-data-historic?ticker=${ticker}&startDate=${startDate}&endDate=${endDate}`;
  } else {
    url = `http://localhost:5000/stock-data-actual?ticker=${ticker}`;
  }

  fetch(url)
    .then(response => response.json())
    .then(data => {
      console.log('Response received:', data);
      res.send(data);
    })
    .catch(error => {
      console.error('Error:', error);
      res.status(500).send('Error fetching stock data');
    });
};


// Route to fetch stock data
app.get('/fetch-stock-data', fetchStockData);

app.listen(3000, () => {
  console.log('Server is running on port 3000');
});