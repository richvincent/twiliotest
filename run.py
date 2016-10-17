from flask import Flask, request, redirect
from blockchain import exchangerates
import twilio.twiml
import os

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def sms():
    number = request.form['From']
    message_body = request.form['Body']
    message_parts = message_body.split()
    resp = twilio.twiml.Response()
    if len(message_parts) != 2:
        message_body = "Please properly form command"
        resp.message(message_body)
        return(str(resp))

    sms_command = message_parts[0]
    sms_attribute = message_parts[1]

    if sms_command == '$btcprice':
        ticker = exchangerates.get_ticker()
        if sms_attribute in ticker:
            btc_price = ticker[sms_attribute].p15min
            spot_price = btc_price*1.125
            message_body = 'The price for 1 bitcoin in USD is {}.\
                The spot price for btc purchase is {}'.format(btc_price, spot_price)

    resp.message('Hello {}, {}'.format(number, message_body))
    return str(resp)

if __name__ == "__main__":
    # Bind to Port if defined, otherwise default to 5000
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
