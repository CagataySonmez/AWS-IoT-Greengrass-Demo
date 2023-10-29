from datetime import datetime
import time
import traceback
import json
import botocore
import sys
import os

import awsiot.greengrasscoreipc
import awsiot.greengrasscoreipc.client as client
from awsiot.greengrasscoreipc.model import (
    IoTCoreMessage,
    QOS,
    SubscribeToIoTCoreRequest,
    PublishToIoTCoreRequest
)

TIMEOUT = 10
REQUEST_TOPIC = sys.argv[1]
RESPONSE_TOPIC = sys.argv[2]
THING_NAME = os.getenv('AWS_IOT_THING_NAME')

ipc_client = awsiot.greengrasscoreipc.connect()


def respond(event):
    # Dummy response message
    response_message = {
        "timestamp": int(round(time.time() * 1000)),
        "response": "Hello from the Green Grass Core Device!"
    }

    # Publish to our topic
    response = PublishToIoTCoreRequest()
    response.topic_name = RESPONSE_TOPIC
    response.payload = bytes(json.dumps(response_message), "utf-8")
    response.qos = QOS.AT_MOST_ONCE
    response_op = ipc_client.new_publish_to_iot_core()
    response_op.activate(response)


class StreamHandler(client.SubscribeToIoTCoreStreamHandler):
    def __init__(self):
        super().__init__()

    def on_stream_event(self, event: IoTCoreMessage) -> None:
        try:
            respond(event)
        except:
            traceback.print_exc()

    def on_stream_error(self, error: Exception) -> bool:
        # Handle error.
        return True  # Return True to close stream, False to keep stream open.

    def on_stream_closed(self) -> None:
        # Handle close.
        pass

# Setup the MQTT Subscription
request = SubscribeToIoTCoreRequest()
request.topic_name = REQUEST_TOPIC
request.qos = QOS.AT_MOST_ONCE
handler = StreamHandler()
operation = ipc_client.new_subscribe_to_iot_core(handler)
future = operation.activate(request)
future.result(TIMEOUT)

# Keep the main thread alive, or the process will exit.
while True:
    time.sleep(10)

# To stop subscribing, close the operation stream.
operation.close()