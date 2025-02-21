import json
import time
from datetime import datetime
from urllib.request import Request, urlopen
from awscrt import mqtt, mqtt5
from awsiot import mqtt5_client_builder
import random

const char* iotCertificate = R"(
-----BEGIN CERTIFICATE-----
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
-----END CERTIFICATE-----
)";
const char* iotCertificate = R"(
-----BEGIN CERTIFICATE-----
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
-----END CERTIFICATE-----
)";
const char* awsRootCA = R"(
-----BEGIN CERTIFICATE-----
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
-----END CERTIFICATE-----
)";

def run_patrick():
    t = time.gmtime()
    data_timestamp = "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}Z".format(
        t[0], t[1], t[2], t[3], t[4], t[5]
    )

    hours = t.tm_hour
    minutes = t.tm_min
    seconds = t.tm_sec
    
    print(str(data_timestamp) + ": Patrick Narbel")
    
    TOPICRELAYCONTROL = "GOSOLR/BRAIN/868373070933652/RELAYCONTROL"

    mqtt_client = mqtt5_client_builder.mtls_from_bytes(
        endpoint=MQTT_BROKER_ENDPOINT,
        client_id=CLIENT_ID,
        cert_bytes=IOT_CERTIFICATE.encode(),
        pri_key_bytes=IOT_PRIVATE_KEY.encode(),
        ca_bytes=AWS_ROOT_CA.encode(),
        clean_session=True,
        keep_alive_secs=10,
    )
    mqtt_connection = mqtt_client.new_connection()

    connect_future = mqtt_connection.connect()
    connect_future.result()

    if (hours > 9 and hours <= 20):
        res = mqtt_connection.publish(
            topic=TOPICRELAYCONTROL,
            payload=json.dumps({
                "imei": "868373070933652",
                "relay": "1",
                "source": "brain",
                "controls": [
                    {"channel_3": "Oven", "state": True},
                    {"channel_4": "Pool", "state": True}
                ],
                "timeStr": data_timestamp,
                "dataTimestamp": data_timestamp
            }),
            qos=mqtt5.QoS.AT_LEAST_ONCE,
            retain=False,
        )
    
    if (hours == 14 and minutes >= 35 and minutes <= 59):
        res = mqtt_connection.publish(
            topic=TOPICRELAYCONTROL,
            payload=json.dumps({
                "imei": "868373070933652",
                "relay": "1",
                "source": "brain",
                "controls": [
                    {"channel_1": "Geyser1", "state": True},
                    {"channel_2": "Geyser2", "state": False},
                    {"channel_3": "Oven", "state": True},
                    {"channel_4": "Pool", "state": True}
                ],
                "timeStr": data_timestamp,
                "dataTimestamp": data_timestamp
            }),
            qos=mqtt5.QoS.AT_LEAST_ONCE,
            retain=False,
        )

    if (hours == 15 and minutes >= 30 and minutes <= 59):
        res = mqtt_connection.publish(
            topic=TOPICRELAYCONTROL,
            payload=json.dumps({
                "imei": "868373070933652",
                "relay": "1",
                "source": "brain",
                "controls": [
                    {"channel_1": "Geyser1", "state": False},
                    {"channel_2": "Geyser2", "state": True},
                    {"channel_3": "Oven", "state": True},
                    {"channel_4": "Pool", "state": True}
                ],
                "timeStr": data_timestamp,
                "dataTimestamp": data_timestamp
            }),
            qos=mqtt5.QoS.AT_LEAST_ONCE,
            retain=False,
        )

    if (hours == 16 and minutes >= 0 and minutes <= 45):
        res = mqtt_connection.publish(
            topic=TOPICRELAYCONTROL,
            payload=json.dumps({
                "imei": "868373070933652",
                "relay": "1",
                "source": "brain",
                "controls": [
                    {"channel_1": "Geyser1", "state": True},
                    {"channel_2": "Geyser2", "state": True},
                    {"channel_3": "Oven", "state": True},
                    {"channel_4": "Pool", "state": True}
                ],
                "timeStr": data_timestamp,
                "dataTimestamp": data_timestamp
            }),
            qos=mqtt5.QoS.AT_LEAST_ONCE,
            retain=False,
        )
