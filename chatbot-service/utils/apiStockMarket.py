import requests

def get_stock_price(ticker: str):
    url = "https://api.marketstack.com/v1/eod?access_key=99978ab1738b4603c6f851606baa03f3"

    querystring = {"symbols":ticker}

    response = requests.get(url, params=querystring)
    
    try:
        json_response = response.json()
        
        if "data" in json_response and len(json_response["data"]) > 0:
            # Get the most recent stock data (first item in data array)
            stock_data = json_response["data"][0]
            
            return {
                "symbol": stock_data["symbol"],
                "date": stock_data["date"],
                "open": stock_data["open"],
                "high": stock_data["high"],
                "low": stock_data["low"],
                "close": stock_data["close"],
                "volume": stock_data["volume"]
            }
        else:
            return {"error": f"No stock data found for {ticker}"}
    except Exception as e:
        return {"error": str(e)}


