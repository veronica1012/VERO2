from flask import Flask, Response
import requests
import json
import logging

app = Flask(__name__)



logging.basicConfig(level=logging.DEBUG)


@app.route("/")
def hello_world():
    return "<p> Tratamiento de Datos Grupo5 </p>"

@app.route("/price/<ticker>")
def price(ticker : str):   
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={ticker}&interval=5min&apikey=demo"
    r = requests.get(url)
    result =r.json()
    return result




@app.route("/moneda/<ticker>")
def moneda(ticker : str):  
    url = f"https://www.alphavantage.co/query?function=FX_INTRADAY&from_symbol={ticker}&to_symbol=USD&interval=5min&apikey=demo"
    r = requests.get(url)
    result =r.json()
    #price = result['quoteSummary']['result'][0]['price']['regularMarketPrice']['raw']
    simbolo = result['Meta Data']['2. From Symbol']
    price = result['Time Series FX (5min)']['2022-08-15 04:00:00']['1. open']
    #df=pd.DataFrame(price["2022-08-12 13:40:00"])
    return simbolo  +" precio actual "+ price



@app.route("/get-price/<ticker>")
def get_price(ticker):
    url = f"https://query2.finance.yahoo.com/v10/finance/quoteSummary/{ticker}?modules=price%2CsummaryDetail%2CpageViews%2CfinancialsTemplate"
    response = requests.get(url)
    company_info = response.json()
    app.logger.info(f"Requested ticker: {ticker}")

    if response.status_code > 400:
        app.logger.info(f"Yahoo has problem with ticker: {ticker}.")
        app.logger.info(f"Yahoo status code: {response.status_code}.")
        return Response({}, status=404, mimetype='application/json')

    app.logger.info(company_info)

    try:
        price = company_info['quoteSummary']['result'][0]['price']['regularMarketPrice']['raw']
        company_name = company_info['quoteSummary']['result'][0]['price']['longName']
        exchange = company_info['quoteSummary']['result'][0]['price']['exchangeName']
        
     
        currency = company_info['quoteSummary']['result'][0]['price']['currency']

        result = {
            "price": price,
            "name": company_name,
            "exchange": exchange,
            "currency": currency
        }
        app.logger.info(result)

        return Response(json.dumps(result), status=200, mimetype='application/json')
    except (KeyError, TypeError):
        return Response({}, status=404, mimetype='application/json')
    except Exception as e:
        app.logger.error("Exception occurred", exc_info=True)


if __name__ == '__main__':
    app.run()


