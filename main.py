from enum import Enum
from time import sleep
from watson_client import WatsonMQTTDevice, WatsonMQTTApi
import yaml
import argparse


class Method(Enum):
    PUBLISH = "publish"
    SUBSCRIBE = "subscribe"


def on_message(mqttc, obj, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))


def main():

    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "method",
        choices=[Method.PUBLISH.value, Method.SUBSCRIBE.value],
        help=f"Either {Method.PUBLISH.value} or {Method.SUBSCRIBE.value}",
    )
    args = parser.parse_args()

    # Read configuration file
    with open("config.yaml") as config_file:
        cfg = yaml.safe_load(config_file)

    # Set up publishing topic
    topic = cfg["topic"]["name"]
    format = cfg["topic"]["format"]
    topic_str = f"iot-2/evt/{topic}/fmt/{format}"
    port = 8883 if cfg["connection"]["ssl"] else 1883

    if args.method == Method.PUBLISH.value:
        # Create client
        c = WatsonMQTTDevice.from_config(cfg)
        # Connect to cloud using TLS. (1883 without TLS - not recommended)
        c.connect(port)
        for t in range(25, 29):
            print(f"publishing temperature {t}° ... ", end="")
            payload = {"temperature": t, "unit": "celsius"}
            info = c.publish(topic_str, payload)

            # Wait for publish confirmation
            info.wait_for_publish()
            print("done")

            # Add a little delay to allow for observation in dashboard
            sleep(3)
    elif args.method == Method.SUBSCRIBE.value:
        api_cfg = cfg["api"]
        c = WatsonMQTTApi(api_cfg["appId"], api_cfg["organization"], api_cfg["token"])
        c.connect()
        device_type = cfg["device"]["type"]
        device_id = cfg["device"]["id"]
        api_topic = f"iot-2/type/{device_type}/id/{device_id}/evt/{topic}/fmt/{format}"
        print(f"Subscribing to {api_topic}")
        c.client.on_message = on_message
        c.client.subscribe(api_topic, 0)
        c.client.loop_forever()
    c.disconnect()


if __name__ == "__main__":
    main()
