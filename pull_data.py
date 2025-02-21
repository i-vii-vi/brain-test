from datetime import datetime
import json
import time
from typing import Dict, List, Tuple
from urllib.request import Request, urlopen
from awscrt import mqtt, mqtt5
from awsiot import mqtt5_client_builder
import os
import logging
from dataclasses import dataclass

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants for MQTT connection
MQTT_BROKER_ENDPOINT = "a1xz7n0flroqhn-ats.iot.eu-west-1.amazonaws.com"
CLIENT_ID = "brain-relays-868373070933652"
TOPICRELAYCONTROL = "GOSOLR/BRAIN/RELAYCONTROL/864454073547659"

# Certificate strings
IOT_CERTIFICATE = """-----BEGIN CERTIFICATE-----
MIIDWTCCAkGgAwIBAgIUXO6FV19qM6tVnJLOwaV2B8wgwGMwDQYJKoZIhvcNAQEL
BQAwTTFLMEkGA1UECwxCQW1hem9uIFdlYiBTZXJ2aWNlcyBPPUFtYXpvbi5jb20g
SW5jLiBMPVNlYXR0bGUgU1Q9V2FzaGluZ3RvbiBDPVVTMB4XDTI0MTExMTE1MDgz
MVoXDTQ5MTIzMTIzNTk1OVowHjEcMBoGA1UEAwwTQVdTIElvVCBDZXJ0aWZpY2F0
ZTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBAKhAHYZbYPodlZZMiYdn
OpVpeW/DgyDukP3njOyfmxbL23STNXz+VVSFw7Dk2lAyPPJ2CYdSaMTbemFu7UK1
E4uBrOSinC8EH+uFerIWufUBooJDP2gdh1PswQHyRt64xN0uRBdDr5V1BYVfaKs2
xoKYAeu+JwMS821iQzRuFYsi5pkfK9kXq02HQhozuJTNp8gVg2iDXrr68A/+Fub6
yYowbdM6b4hM3lypTxQj9RYd1kfzJ6mxlkPug1nVowopkajJsNvIUuJoFS4OAu9k
7dZblCnJkd/i3IL9rbkWtPlHp8UiZmlouHDQ1X3shUPENjaIrLXOcPTExiWPu+ia
u6ECAwEAAaNgMF4wHwYDVR0jBBgwFoAUD4KdJeLTqh2nfvT6MbuGTWuqgAwwHQYD
VR0OBBYEFDXDlanEIMDSNsGwdMwA0qHiLBAZMAwGA1UdEwEB/wQCMAAwDgYDVR0P
AQH/BAQDAgeAMA0GCSqGSIb3DQEBCwUAA4IBAQCDg+dLuupFEN7yhogmEIimZyJl
mjB1gN3JeVsTC0b/d0k69GwhTfWikmMjehhytTu0qHkSJN0KcoiYxfgPF6Md+TTl
4V/2CS+usuH1B6iv6kHS9rSMbIT1yTaU3Dzcqh0lg5aDUb6MiZDW9jVhOe75Ibj+
KsT4+9CZRGQM7UuCfEOzQ7i5lA27uxlWbtxWhrtG200wt35sN8cTKqGO+pACDGy0
Sdqn7RxKei6VU17vQ5sbquWQYbXM77ICecZ+/6NaLIpDmMlpF9Fsw2awMt5c7dCr
PRE3cOm2G+B/TWDPYvRc361sL0cGTNqcVvbW8pX7SUNch9UB+Bvfp1rOgHiY
-----END CERTIFICATE-----"""

IOT_PRIVATE_KEY = """-----BEGIN RSA PRIVATE KEY-----
MIIDWTCCAkGgAwIBAgIUXO6FV19qM6tVnJLOwaV2B8wgwGMwDQYJKoZIhvcNAQEL
BQAwTTFLMEkGA1UECwxCQW1hem9uIFdlYiBTZXJ2aWNlcyBPPUFtYXpvbi5jb20g
SW5jLiBMPVNlYXR0bGUgU1Q9V2FzaGluZ3RvbiBDPVVTMB4XDTI0MTExMTE1MDgz
MVoXDTQ5MTIzMTIzNTk1OVowHjEcMBoGA1UEAwwTQVdTIElvVCBDZXJ0aWZpY2F0
ZTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBAKhAHYZbYPodlZZMiYdn
OpVpeW/DgyDukP3njOyfmxbL23STNXz+VVSFw7Dk2lAyPPJ2CYdSaMTbemFu7UK1
E4uBrOSinC8EH+uFerIWufUBooJDP2gdh1PswQHyRt64xN0uRBdDr5V1BYVfaKs2
xoKYAeu+JwMS821iQzRuFYsi5pkfK9kXq02HQhozuJTNp8gVg2iDXrr68A/+Fub6
yYowbdM6b4hM3lypTxQj9RYd1kfzJ6mxlkPug1nVowopkajJsNvIUuJoFS4OAu9k
7dZblCnJkd/i3IL9rbkWtPlHp8UiZmlouHDQ1X3shUPENjaIrLXOcPTExiWPu+ia
u6ECAwEAAaNgMF4wHwYDVR0jBBgwFoAUD4KdJeLTqh2nfvT6MbuGTWuqgAwwHQYD
VR0OBBYEFDXDlanEIMDSNsGwdMwA0qHiLBAZMAwGA1UdEwEB/wQCMAAwDgYDVR0P
AQH/BAQDAgeAMA0GCSqGSIb3DQEBCwUAA4IBAQCDg+dLuupFEN7yhogmEIimZyJl
mjB1gN3JeVsTC0b/d0k69GwhTfWikmMjehhytTu0qHkSJN0KcoiYxfgPF6Md+TTl
4V/2CS+usuH1B6iv6kHS9rSMbIT1yTaU3Dzcqh0lg5aDUb6MiZDW9jVhOe75Ibj+
KsT4+9CZRGQM7UuCfEOzQ7i5lA27uxlWbtxWhrtG200wt35sN8cTKqGO+pACDGy0
Sdqn7RxKei6VU17vQ5sbquWQYbXM77ICecZ+/6NaLIpDmMlpF9Fsw2awMt5c7dCr
PRE3cOm2G+B/TWDPYvRc361sL0cGTNqcVvbW8pX7SUNch9UB+Bvfp1rOgHiY
-----END RSA PRIVATE KEY-----"""

AWS_ROOT_CA = """-----BEGIN CERTIFICATE-----
MIIDQTCCAimgAwIBAgITBmyfz5m/jAo54vB4ikPmljZbyjANBgkqhkiG9w0BAQsF
ADA5MQswCQYDVQQGEwJVUzEPMA0GA1UEChMGQW1hem9uMRkwFwYDVQQDExBBbWF6
b24gUm9vdCBDQSAxMB4XDTE1MDUyNjAwMDAwMFoXDTM4MDExNzAwMDAwMFowOTEL
MAkGA1UEBhMCVVMxDzANBgNVBAoTBkFtYXpvbjEZMBcGA1UEAxMQQW1hem9uIFJv
b3QgQ0EgMTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBALJ4gHHKeNXj
ca9HgFB0fW7Y14h29Jlo91ghYPl0hAEvrAIthtOgQ3pOsqTQNroBvo3bSMgHFzZM
9O6II8c+6zf1tRn4SWiw3te5djgdYZ6k/oI2peVKVuRF4fn9tBb6dNqcmzU5L/qw
IFAGbHrQgLKm+a/sRxmPUDgH3KKHOVj4utWp+UhnMJbulHheb4mjUcAwhmahRWa6
VOujw5H5SNz/0egwLX0tdHA114gk957EWW67c4cX8jJGKLhD+rcdqsq08p8kDi1L
93FcXmn/6pUCyziKrlA4b9v7LWIbxcceVOF34GfID5yHI9Y/QCB/IIDEgEw+OyQm
jgSubJrIqg0CAwEAAaNCMEAwDwYDVR0TAQH/BAUwAwEB/zAOBgNVHQ8BAf8EBAMC
AYYwHQYDVR0OBBYEFIQYzIU07LwMlJQuCFmcx7IQTgoIMA0GCSqGSIb3DQEBCwUA
A4IBAQCY8jdaQZChGsV2USggNiMOruYou6r4lK5IpDB/G/wkjUu0yKGX9rbxenDI
U5PMCCjjmCXPI6T53iHTfIUJrU6adTrCC2qJeHZERxhlbI1Bjjt/msv0tadQ1wUs
N+gDS63pYaACbvXy8MWy7Vu33PqUXHeeE6V/Uq2V8viTO96LXFvKWlJbYK8U90vv
o/ufQJVtMVT8QtPHRh8jrdkPSHCa2XV4cdFyQzR1bldZwgJcJmApzyMZFo6IQ6XU
5MsI+yMRQ+hDKXJioaldXgjUkK642M4UwtBV8ob2xJNDd2ZhwLnoQdeXeGADbkpy
rqXRfboQnoZsG4q5WTP468SQvvG5
-----END CERTIFICATE-----"""

@dataclass
class RelayConfig:
    mqtt_broker: str
    client_id: str
    topic: str
    cert: str
    key: str
    root_ca: str
    use_files: bool = False

@dataclass
class ChannelState:
    channel: str
    state: str

class RelayController:
    def __init__(self, config: RelayConfig):
        self.config = config
        self.mqtt_client = None
        self.mqtt_connection = None
        self._initialize_mqtt()

    def _initialize_mqtt(self):
        """Initialize MQTT client with credentials from either files or strings"""
        try:
            if self.config.use_files:
                with open(self.config.cert, 'r') as f:
                    cert = f.read()
                with open(self.config.key, 'r') as f:
                    key = f.read()
                with open(self.config.root_ca, 'r') as f:
                    root_ca = f.read()
            else:
                cert = self.config.cert
                key = self.config.key
                root_ca = self.config.root_ca

            self.mqtt_client = mqtt5_client_builder.mtls_from_bytes(
                endpoint=self.config.mqtt_broker,
                client_id=self.config.client_id,
                cert_bytes=cert.encode(),
                pri_key_bytes=key.encode(),
                ca_bytes=root_ca.encode(),
                clean_session=True,
                keep_alive_secs=30,
            )
            self.mqtt_connection = self.mqtt_client.new_connection()
        except Exception as e:
            logger.error(f"Failed to initialize MQTT client: {e}")
            raise

    def connect(self):
        """Establish MQTT connection with error handling"""
        try:
            if not self.mqtt_connection:
                self._initialize_mqtt()
            connect_future = self.mqtt_connection.connect()
            connect_future.result(timeout=5.0)  # Wait up to 5 seconds
            logger.info("Successfully connected to MQTT broker")
        except Exception as e:
            logger.error(f"Failed to connect to MQTT broker: {e}")
            raise

    def disconnect(self):
        """Safely disconnect from MQTT broker"""
        if self.mqtt_connection:
            try:
                disconnect_future = self.mqtt_connection.disconnect()
                disconnect_future.result(timeout=5.0)
                logger.info("Successfully disconnected from MQTT broker")
            except Exception as e:
                logger.error(f"Error during disconnect: {e}")

    def determine_channel_states(self, current_time: datetime) -> List[ChannelState]:
        """Determine the state of all channels based on the current time"""
        # Initialize default states
        states = {
            "Channel_1": "True",
            "Channel_2": "True",
            "Channel_3": "True",
            "Channel_4": "True"
        }
        
        # Define time ranges and their effects
        time_rules = [
            {
                "start": "06:55",
                "end": "18:05",
                "channels": {"Channel_1": "False", "Channel_2": "False", "Channel_3": "True", "Channel_4": "True"},
                "description": "Pool"
            },
            {
                "start": "09:35",
                "end": "11:50",
                "channels": {"Channel_1": "True", "Channel_2": "False", "Channel_3": "True", "Channel_4": "True"},
                "description": "Pool and geyser 1"
            },
            {
                "start": "12:35",
                "end": "13:50",
                "channels": {"Channel_1": "True", "Channel_2": "False", "Channel_3": "True", "Channel_4": "True"},
                "description": "Pool and geyser 1"
            },
            {
                "start": "13:50",
                "end": "16:10",
                "channels": {"Channel_1": "False", "Channel_2": "True", "Channel_3": "True", "Channel_4": "True"},
                "description": "Pool and geyser 1"
            },
            {
                "start": "16:10",
                "end": "18:05",
                "channels": {"Channel_1": "False", "Channel_2": "False", "Channel_3": "True", "Channel_4": "True"},
                "description": "Pool and geyser 1"
            },
            {
                "start": "18:05",
                "end": "19:30",
                "channels": {"Channel_1": "False", "Channel_2": "False", "Channel_3": "True", "Channel_4": "True"},
                "description": "Pool and geyser 1"
            }
        ]

        current_time_str = current_time.strftime("%H:%M")
        
        # Apply rules in priority order
        for rule in time_rules:
            if self._is_time_between(current_time_str, rule["start"], rule["end"]):
                for channel, state in rule["channels"].items():
                    states[channel] = state
                logger.info(f"Applied rule: {rule['description']}")

        return [ChannelState(channel=k, state=v) for k, v in states.items()]


    def _is_time_between(self, current: str, start: str, end: str) -> bool:
        """Check if current time is between start and end times"""
        current_time = datetime.strptime(current, "%H:%M").time()
        start_time = datetime.strptime(start, "%H:%M").time()
        end_time = datetime.strptime(end, "%H:%M").time()
        
        if start_time <= end_time:
            return start_time <= current_time <= end_time
        else:  # Handle overnight ranges
            return current_time >= start_time or current_time <= end_time

    def publish_states(self, states: List[ChannelState]):
        """Publish channel states to MQTT broker"""
        try:
            data_timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
            payload = {
                "imei": "864454073547659",
                "relay": "1",
                "source": "brain",
                "controls": [
                    {"channel": state.channel, "state": state.state}
                    for state in states
                ],
                "timeStr": data_timestamp,
                "dataTimestamp": data_timestamp
            }

            publish_future = self.mqtt_connection.publish(
                topic=self.config.topic,
                payload=json.dumps(payload),
                qos=mqtt5.QoS.AT_LEAST_ONCE,
                retain=False,
            )
            publish_future.result(timeout=5.0)  # Wait up to 5 seconds
            logger.info("Successfully published channel states")
        except Exception as e:
            logger.error(f"Failed to publish channel states: {e}")
            raise

def main():
    # Create configuration with hardcoded credentials
    config = RelayConfig(
        mqtt_broker=MQTT_BROKER_ENDPOINT,
        client_id=CLIENT_ID,
        topic=TOPICRELAYCONTROL,
        cert=IOT_CERTIFICATE,
        key=IOT_PRIVATE_KEY,
        root_ca=AWS_ROOT_CA,
        use_files=False  # Using string certificates instead of files
    )

    # Create the controller
    controller = RelayController(config)
    
    try:
        # Connect to MQTT broker
        controller.connect()
        
        # Get current time and check channel states
        current_time = datetime.now()
        current_time_str = current_time.strftime("%H:%M")
        logger.info(f"Checking channel states for time: {current_time_str}")
        
        # Check channels
        states = controller.determine_channel_states(current_time)
        
        # Publish the states
        controller.publish_states(states)
        
        logger.info("Successfully published channel states")
        
    except Exception as e:
        logger.error(f"Error in main execution: {e}")
    finally:
        # Always disconnect properly
        controller.disconnect()

if __name__ == "__main__":
    main()
