// models/stockData.js
const mongoose = require('mongoose');

const stockDataSchema = new mongoose.Schema({
  ticker: String,
  date: Date,
  open: Number,
  high: Number,
  low: Number,
  close: Number,
  volume: Number,
  adjClose: Number,
});

const StockData = mongoose.model('StockData', stockDataSchema);

module.exports = StockData;