# Watson MQTT example

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

In publish mode the application connects to the IBM Watson IOT platform
using paho-mqtt and publishes sensor data in a topic.

In subscribe mode the application uses an API key to receive messages from the device
API (also using MQTT).

## Prerequisites

- [Python 3](https://www.python.org)
- [paho-mqtt](https://github.com/eclipse/paho.mqtt.python)

## Installation

Install dependencies with pip

```shell
pip install -r requirements.txt
```

For development also install development dependencies

```shell
pip install -r requirements_dev.txt
```

## Usage

1. Copy the example configuration `config-sample.yaml` to `config.yaml`
1. Create a new device in imcloud.com and enter the credentials in the configuration
   file.
1. IMPORTANT: Open the devices **status** section in the dashboard before running.
   The messages will not be visible otherwise.
1. Run the application

```shell
# (Optional) Run subscribe mode in a separate shell
python main.py subscribe

# Publish the messages
python main.py publish
```

```shell
# Sample output (publish)
publishing temperature 25° ... done
publishing temperature 26° ... done
publishing temperature 27° ... done
publishing temperature 28° ... done
```

```shell
# Sample output (subscribe)
Subscribing to iot-2/type/sensor/id/pi0-temperature/evt/status/fmt/json
<topic_string> 0 b'{"temperature": 25, "unit": "celsius"}'
<topic_string> 0 b'{"temperature": 26, "unit": "celsius"}'
<topic_string> 0 b'{"temperature": 27, "unit": "celsius"}'
<topic_string> 0 b'{"temperature": 28, "unit": "celsius"}'
```

This should result into messages being published on the broker:

![Payload published to the status topic](img/sending_data.png)

## References

- [Watson IOT Platform Documentation - Communicating with devices (MQTT)](https://www.ibm.com/docs/en/watson-iot-platform?topic=devices-communicating-mqtt)
- [Watson IOT Platform Documentation - Communicating with applications (MQTT)](https://www.ibm.com/docs/en/watson-iot-platform?topic=applications-communicating-mqtt)
- [Paho MQTT to Watson IOT (Stackoverflow)](https://stackoverflow.com/questions/46664862/python-paho-mqtt-og-ibm-watson-iot)
