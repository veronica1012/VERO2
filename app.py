from flask import Flask, Response
import requests
import json
import logging

app = Flask(__name__)



logging.basicConfig(level=logging.DEBUG)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


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


