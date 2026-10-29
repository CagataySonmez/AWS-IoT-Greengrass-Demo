import time
import traceback
import json
import sys

from awsiot.greengrasscoreipc.clientv2 import GreengrassCoreIPCClientV2                    # pyright: ignore[reportMissingImports]

REQUEST_TOPIC = sys.argv[1]
RESPONSE_TOPIC = sys.argv[2]

ipc_client = GreengrassCoreIPCClientV2()


def respond(event):
    # Dummy response message
    response_message = {
        "timestamp": int(round(time.time() * 1000)),
        "response": "Hello from the Green Grass Core Device!"
    }

    # Publish to our topic
    ipc_client.publish_to_iot_core(
        topic_name=RESPONSE_TOPIC,
        payload=json.dumps(response_message).encode("utf-8"),
        qos="0"
    )


def on_stream_event(event):
    try:
        respond(event)
    except Exception:
        traceback.print_exc()


def on_stream_error(error):
    # Return True to close stream, False to keep stream open.
    return True


def on_stream_closed():
    pass


operation = None

try:
    # Setup the MQTT Subscription
    _, operation = ipc_client.subscribe_to_iot_core(
        topic_name=REQUEST_TOPIC,
        qos="0",
        on_stream_event=on_stream_event,
        on_stream_error=on_stream_error,
        on_stream_closed=on_stream_closed
    )

    # Keep the main thread alive, or the process will exit.
    while True:
        time.sleep(10)

except KeyboardInterrupt:
    pass

finally:
    # Close the subscription and IPC client.
    if operation is not None:
        operation.close()

    ipc_client.close()