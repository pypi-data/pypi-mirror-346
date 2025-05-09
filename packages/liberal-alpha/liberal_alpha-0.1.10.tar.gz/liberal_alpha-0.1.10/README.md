# Liberal Alpha SDK Usage Example

## 1️⃣ Initialize the SDK

You can initialize the SDK with default parameters:

```python
from liberal_alpha.client import LiberalAlphaClient

private_key = "YOUR_PRIVATE_KEY"
# If wallet address is not provided, you can derive it from your private key:
wallet = get_wallet_address(private_key)

    client = LiberalAlphaClient(
        host="127.0.0.1",#optional
        port=8128,#optional
        api_key="api-key",#optional
        private_key=private_key #optional
    )
Send a JSON object via gRPC:
JSON_Object = {
    "Price": 100000,
    "Volume": 50,
    "Volume_USD": 5000000,
}

client.send_data("BTC_SOURCE1", JSON_Object, record_id="1")
3️⃣ Send Alpha Signal
Send an alpha signal:
alpha_data = {
    "signal": "buy",
    "confidence": 0.85
}

client.send_alpha("Alpha_ID", alpha_data, record_id="1")
4️⃣ Subscribe to Data
To subscribe to real-time data, use the subscribe_data method. Note that your API key, private key, wallet, and base URL are already set during initialization. You only need to specify the record to subscribe to and (optionally) provide an on_message callback for custom message handling. For example:
# Define a callback function to handle received messages
def on_message(message):
    print("Received message:", message)

# Subscribe to data from record_id 1:
client.subscribe_data(record_id=1, max_reconnect=5, on_message=on_message)

Ensure that your API Key, private key, and wallet address are correct, and that you have subscribed to the data you wish to receive via the website's subscribe channel.

Fetch My Records
To fetch the records associated with your account, use the my_records() method. This method makes an HTTP GET request to the backend endpoint /api/records using your API key for authentication, and returns the records in JSON format.

records = liberal.my_records()
print("My Records:", records)

Fetch My Subscriptions
To fetch your subscription information, use the my_subscriptions() method. This method sends an HTTP GET request to the backend endpoint /api/subscriptions with your API key for authentication, and returns the subscription details in JSON format.

subscriptions = liberal.my_subscriptions()
print("My Subscriptions:", subscriptions)
