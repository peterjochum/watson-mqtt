from time import sleep
from watson_client import WatsonClient
import yaml


def main():
    # Read configuration file
    with open("config.yaml") as config_file:
        cfg = yaml.safe_load(config_file)

    # Create client
    c = WatsonClient(
        cfg["device"]["id"],
        cfg["device"]["organization"],
        cfg["device"]["type"],
        cfg["device"]["auth_type"],
        cfg["device"]["token"],
    )

    # Set up publishing topic
    topic = cfg["topic"]["name"]
    format = cfg["topic"]["format"]
    topic_str = f"iot-2/evt/{topic}/fmt/{format}"

    port = 8883 if cfg["connection"]["ssl"] else 1883

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
    c.disconnect()


if __name__ == "__main__":
    main()


