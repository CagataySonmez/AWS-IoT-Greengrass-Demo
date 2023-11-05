import sys
import time
import traceback

from awsiot.greengrasscoreipc.clientv2 import GreengrassCoreIPCClientV2

CLIENT_DEVICE_EVENT_TOPIC = 'event/clients/+/alert'
TIMEOUT = 10


def on_event_message(event):
    try:
        message = str(event.binary_message.message, 'utf-8')
        print('Received new event from IoT Client: %s' % message)
    except:
        traceback.print_exc()


try:
    ipc_client = GreengrassCoreIPCClientV2()

    # SubscribeToTopic returns a tuple with the response and the operation.
    _, operation = ipc_client.subscribe_to_topic(
        topic=CLIENT_DEVICE_EVENT_TOPIC, on_stream_event=on_event_message)
    print('Successfully subscribed to topic: %s' %
          CLIENT_DEVICE_EVENT_TOPIC)

    # Keep the main thread alive, or the process will exit.
    try:
        while True:
            time.sleep(10)
    except InterruptedError:
        print('Subscribe interrupted.')

    operation.close()
except Exception:
    print('Exception occurred when using IPC.', file=sys.stderr)
    traceback.print_exc()
    exit(1)
