import json

import paho.mqtt.client as mqtt


class ConnectURLMixin:
    def connect(self, port=8883):
        """
        Connects the client using the pre set parameters.
        :param port: Override the default port 8883
        :return: 0 if the connection was successful
        """
        return self.client.connect(self.get_connect_url(), port)

    def get_connect_url(self) -> str:
        return f"{self.organization}.messaging.internetofthings.ibmcloud.com"


class WatsonMQTTApi(ConnectURLMixin):
    appId: str
    organization: str
    token: str
    client: mqtt.Client

    def __init__(self, appId, organization, token):
        self.appId = appId
        self.organization = organization
        self.token = token
        self.client = mqtt.Client(self.get_client_id())
        self.client.username_pw_set(self.get_user_name(), token)
        self.client.tls_set()

    def get_user_name(self):
        return f"a-{self.organization}-{self.appId}"

    def get_client_id(self):
        return f"a:{self.organization}:{self.appId}"


class WatsonMQTTDevice(ConnectURLMixin):
    """
    Creates a paho.mqtt.client from IBM Watson IOT device properties.
    """

    device_id: str
    organization: str
    device_type: str
    __auth_type: str
    token: str
    client = None
    supported_auth_types = [
        "use-token-auth",
    ]

    def __init__(
        self,
        device_id,
        organization,
        device_type,
        auth_type,
        token,
        use_ssl=True,
    ):
        """
        Sets up the paho-mqtt client for use with Watson
        :param device_id: Device-ID
        :param organization: Organization
        :param device_type: Device type or category
        :param auth_type: Auth type: Must be use-token-auth
        :param token: The secret token for authentication
        :param use_ssl: Set to false if the connection should not be encrypted
        """
        self.device_id = device_id
        self.organization = organization
        self.device_type = device_type
        self.token = token
        self.auth_type = auth_type
        self.client = mqtt.Client(self.get_client_id())
        self.client.username_pw_set(self.auth_type, self.token)
        if use_ssl:
            self.client.tls_set()

    @classmethod
    def from_config(cls, cfg: dict):
        return WatsonMQTTDevice(
            cfg["device"]["id"],
            cfg["device"]["organization"],
            cfg["device"]["type"],
            cfg["device"]["username"],
            cfg["device"]["token"],
        )

    @property
    def auth_type(self):
        return self.__auth_type

    @auth_type.setter
    def auth_type(self, auth_type):
        if auth_type not in self.supported_auth_types:
            supported_auth_types_str = ", ".join(self.supported_auth_types)
            raise AttributeError(
                f"Auth type {auth_type} unsupported: "
                f"use one of these: {supported_auth_types_str}"
            )
        self.__auth_type = auth_type

    def get_client_id(self):
        """
        Formats the device string as expected by watson IOT
        :return: A string in the form d:organization:device_type:device_id
        """
        return f"d:{self.organization}:{self.device_type}:{self.device_id}"

    def publish(self, topic: str, payload: dict) -> mqtt.MQTTMessageInfo:
        """
        Publishes the payload under the specified topic
        :param topic: Topic to publish the payload to. For example
            /iot-2/evt/status/fmt/json
        :param payload: A dict object containing the message data.
            Must be convertible to JSON.
        :return: MQTTMessageInfo for publish status inspection
        """
        return self.client.publish(topic, json.dumps(payload))

    def disconnect(self) -> None:
        """
        Disconnects the client
        """
        # Assert all messages are sent
        self.client.loop()

        # Disconnect the client
        self.client.disconnect()
