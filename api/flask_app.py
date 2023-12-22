from flask import Flask, request
from flipside import Flipside
import requests
import datetime
import os

flipside = Flipside(os.environ["FLIPSIDE_KEY"], "https://api-v2.flipsidecrypto.xyz")

app = Flask(__name__)

@app.route("/data/transactions")
def getTransactionData():
    sql = """SELECT DATE(block_timestamp) AS transaction_date, COUNT(DATE(block_timestamp)) AS transaction_count FROM optimism.core.fact_transactions WHERE block_timestamp > DATEADD(year, -1, GETDATE()) GROUP BY DATE(block_timestamp) ORDER BY DATE(block_timestamp) ASC"""
    query_result_set = flipside.query(sql)
    return query_result_set.rows

@app.route("/data/ethereum")
def getEthereumMarketData():
    days = request.args.get("days", default=365)
    interval = request.args.get("interval", default="")
    params = {"vs_currency": "usd", "days": days}
    if len(interval) != 0:
        params["interval"] = interval
    data = requests.get("https://api.coingecko.com/api/v3/coins/ethereum/market_chart", params=params).json()
    result = {}
    if len(data["prices"]) > 0:
        result["date"] = datetime.datetime.fromtimestamp(data["prices"][0][0]/1000)
    result["data"] = []
    for i in range(len(data["prices"])):
        result["data"].append({"timestamp": datetime.datetime.fromtimestamp(data["prices"][i][0]/1000), "price": data["prices"][i][1], "market_cap": data["market_caps"][i][1], "total_volume": data["total_volumes"][i][1]})
    return result

if __name__ == "__main__":
    app.run(debug=True)
