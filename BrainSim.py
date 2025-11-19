import time
import json
from datetime import datetime, timezone
import threading
import random
import sys

from awscrt import mqtt5
from awsiot import mqtt5_client_builder

# --- Configuration ---
ENDPOINT = "a2z4csjj2fxwmw-ats.iot.eu-west-1.amazonaws.com"
CLIENT_ID = "brain-868373070929676"

CERTIFICATE = """-----BEGIN CERTIFICATE-----
MIIDWTCCAkGgAwIBAgIUeyHUgxh0ctpZ9G85ATVnhY2+yXEwDQYJKoZIhvcNAQEL
BQAwTTFLMEkGA1UECwxCQW1hem9uIFdlYiBTZXJ2aWNlcyBPPUFtYXpvbi5jb20g
SW5jLiBMPVNlYXR0bGUgU1Q9V2FzaGluZ3RvbiBDPVVTMB4XDTI1MDczMTEwNTcy
MloXDTQ5MTIzMTIzNTk1OVowHjEcMBoGA1UEAwwTQVdTIElvVCBDZXJ0aWZpY2F0
ZTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBAMKsUeBcnJVBZ/E2QO0E
4zdoK57fQwzMJjocjZXRNF2Ca3x4NggU6OqvcoC0GnHkxi0US3XZ/297xFynqzzH
dsQi9g29Tz5QfKxZvhBOl8eZweWoJNRV31wLZzaU3VnhgSJDt4TRnQ9Kb2nQ5hyj
8IPVsHyjRSc8jS0MbU6rVvA0vhbCuS0SeLkzvkNbkqEM34A4OdRCVRTIrmu5OnP0
KXQEA/YihF5oGcI8Ns1AZV6s+eGU4miSWQs+/ktU27H+7Mpg6yx8wcdjGV/EkaOi
Qo0aw5jHe8/v0qhYkrcRADtJkkVXJsulUuqQNQsfg6S62wMrUI2Eq5HOw3O72r7u
K3UCAwEAAaNgMF4wHwYDVR0jBBgwFoAUuwsszlnwg0/wKbTLU0mGGzvCGhYwHQYD
VR0OBBYEFCTb2evk2L9rxBnuuwVG1MLB4iYIMAwGA1UdEwEB/wQCMAAwDgYDVR0P
AQH/BAQDAgeAMA0GCSqGSIb3DQEBCwUAA4IBAQB4BEwH7TsfI2kQImHPGzSD7q/g
THBx9FapzL43XwhTjx8gqfL7YizvieRyYMC5x8CZn20LRr1CTTN02eIAyItaxm/V
Tx/QZcuvHEAPNNYf5ifeqQMaYi3ZQ7kef8fazsYtKIx17o4Q71A/y7BvVex1xZO0
Zk00TvoxLPOpfHqDv2G56qAIcPqUFzI+BXO4YFTyGqzM1w/1yodyG/XMZPbHSoqo
dnGrPCQD8ZAZ9/h+u76xvtmiHvetW4Rv84rXtUIL9hKtADFeCxV79Wau3pheXFsO
80bvVUawdebK1Aetww43nIyW65LYVon5aJtK2x15nWAOv3rvr93DJElxFOOe
-----END CERTIFICATE-----"""

PRIVATE_KEY = """-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEAwqxR4FyclUFn8TZA7QTjN2grnt9DDMwmOhyNldE0XYJrfHg2
CBTo6q9ygLQaceTGLRRLddn/b3vEXKerPMd2xCL2Db1PPlB8rFm+EE6Xx5nB5agk
1FXfXAtnNpTdWeGBIkO3hNGdD0pvadDmHKPwg9WwfKNFJzyNLQxtTqtW8DS+FsK5
LRJ4uTO+Q1uSoQzfgDg51EJVFMiua7k6c/QpdAQD9iKEXmgZwjw2zUBlXqz54ZTi
aJJZCz7+S1Tbsf7symDrLHzBx2MZX8SRo6JCjRrDmMd7z+/SqFiStxEAO0mSRVcm
y6VS6pA1Cx+DpLrbAytQjYSrkc7Dc7vavu4rdQIDAQABAoIBAQCDd+JXddPdTG2I
zc3tA4b7LSOASGC8rMYIKq5HhiAqImC6j2hV7uEZVOEsH/VYA1r+qJ0Jeu5xeJE0
zZrsEfyYGtA2mSmB+NMphfXAh4MjLihvEy3EJDYSsDTE/KW8BHm0DS1Lyk+aOveg
643ru587OT3V/mE+TTs+OA09uqKc1qHpCjzfuiA/0rqk0UVEA6afzUvtfHj+W6Ko
CYT69umv3aUGWHbxSeiAwr3KoDrvrrwagZimM/DqxEEmPBYiqXyYY/M3eQRQoACa
5geVFhaUt5xxqkGqiklax6SLjX5hIX2pUYKnnzsTv7UM+NgjKkHUCbXd+hkE/DiQ
hWB7XdLlAoGBAPvy4+E+Y9uKD01QmwhwVFYpHFGPBDh6bFSloe99aS6YNnNHAwIc
Vu2kCN3aW29r/w53/gYi9tq3dXXjaeO6ga1uGuIGjg+8TGoEFzXgTQUpoOdrbVmp
5XvP/YQAxpHemRlU9yMwSmrZwReH/bZlFU2dmy/pH+9UdRu3WKlkcFhHAoGBAMXN
qbMJGqCHFZ6a5EAlXfh5WIPY/AT5y5pGSh4vbjM4cg+QnV6y2k+fdoboTDdB01mW
VkwKNmXN46qBoIBkjpwn8Pzz6OyUsPsxyOlJ3ji6Sfpi1vb0L+zWw9u6xfImY34Z
eeL9Rn78Q9oSMopX7pawrDLOX/yPCcRxrJT1L7hjAoGAbYezb7ma2ddUPa1cKLgE
wgxPRlmhYRg/vjDfjGj98Aa2LTli4mkFlXwpaqFB/Nd7Y4PgyDQtEvqMsvpxj1IG
jCoAv+BPpCGdKr2qhX6EnUjyrYizWjaVEFVkhh18NfAKqMuaQQ7+WyNdYWh6cO/S
6hIpZBO6EWarHqh/f+ytNoMCgYA3UH8PQRGAKKaEFv6TbZ+st4poPIqlfZFRUCyz
6kGf8z36Wk+Xxt5D++zyZw3BOhg3alIxq31w1LXA3cUbgoNa6dR7eF3/osknRdHQ
Y0bQiE/dxDwnDTxFt/1HeiCWyeNyxP8P2hIXusXiusoFY/eljjxpbMrs3rc1hzBi
63nvzwKBgQDEf3vdJuA7V6cCRiUTt4Z6Tovn8IsQKQIVkw01reZBxwS0w+OkzxoK
yI/b/+PYsG4xa6Li5t6OmGhsb1ze+TBPWDgXO97kgQ0qjKJIo3CPNQ1CfJ0TdCAv
1eDJH1FkrJqN4LmIdJM6KFztrRaSftXXnFadedbirFh4hwWVJmWHRQ==
-----END RSA PRIVATE KEY-----"""

ROOT_CERTIFICATE = """-----BEGIN CERTIFICATE-----
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

# --- MQTT Setup ---
mqtt_client = mqtt5_client_builder.mtls_from_bytes(
    endpoint=ENDPOINT,
    cert_bytes=CERTIFICATE.encode(),
    pri_key_bytes=PRIVATE_KEY.encode(),
    ca_bytes=ROOT_CERTIFICATE.encode(),
    client_id=CLIENT_ID,
    clean_session=False,
    keep_alive_secs=60,
)
mqtt_connection = mqtt_client.new_connection()


def publish_status(imei):
    status_topic = f"GOSOLR/BRAIN/{imei}/STATUS"
    status_payload = {"connected": True, "network": {
        "band": "5ghz", "type": "wifi", "provider": "onboardModule", "source": "onboardModule"}}
    mqtt_connection.publish(
        topic=status_topic,
        payload=json.dumps(status_payload),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False
    )
    print(f"📡 Sent STATUS to {status_topic}: {status_payload}")


def publish_systemhealth(imei):
    systemhealth_topic = f"GOSOLR/BRAIN/{imei}/SYSTEM-HEALTH"
    systemhealth_payload = {"totalConsumptionPrediction": 44, "efficiency": "moderate", "water": {"device": {
        "Geyser 1": "maintained", "Geyser 2": "maintained"}}, "consumptionStatus": "stable", "chargeStatus": "charging"}
    mqtt_connection.publish(
        topic=systemhealth_topic,
        payload=json.dumps(systemhealth_payload),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False
    )
    print(
        f"📡 Sent SYSTEM-HEALTH to {systemhealth_topic}: {systemhealth_payload}")


def publish_heartbeat(imei):
    t = time.gmtime()
    data_timestamp = "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}Z".format(
        t[0], t[1], t[2], t[3], t[4], t[5])

    currentHour = t[3] + 2
    currentMinute = t[4]

    hb_topic = f"GOSOLR/BRAIN/{imei}/HB"
    hb_payload = {"version": "1.1.0.5",
                  "dataTimestamp": data_timestamp, "timeStr": data_timestamp}
    mqtt_connection.publish(
        topic=hb_topic,
        payload=json.dumps(hb_payload),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False
    )
    print(f"📡 Sent HEARTBEAT to {hb_topic}: {hb_payload}")


def publish_test():

    t = time.gmtime()
    data_timestamp = "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}Z".format(
        t[0], t[1], t[2], t[3], t[4], t[5])

    for _ in range(500):
        imei = ''.join(random.choices('0123456789ABCDEF', k=15))
        test_hb_topic = f"GOSOLR/BRAIN/{imei}/HB"
        test_hb_payload = {"version": "1.1.0.5",
                           "dataTimestamp": data_timestamp, "timeStr": data_timestamp}
        mqtt_connection.publish(
            topic=test_hb_topic,
            payload=json.dumps(test_hb_payload),
            qos=mqtt5.QoS.AT_LEAST_ONCE,
            retain=False
        )
        print(f"📡 Sent HEARTBEAT to {test_hb_topic}: {test_hb_payload}")
        time.sleep(0.1)  # optional pause between sends
        test_status_topic = f"GOSOLR/BRAIN/{imei}/STATUS"
        test_status_payload = {"connected": False, "network": {
            "band": "-", "type": "-", "provider": "-", "source": "-"}}
        mqtt_connection.publish(
            topic=test_status_topic,
            payload=json.dumps(test_status_payload),
            qos=mqtt5.QoS.AT_LEAST_ONCE,
            retain=False
        )
        print(f"📡 Sent STATUS to {test_status_topic}: {test_status_payload}")
        time.sleep(0.1)  # optional pause between sends
        test_systemhealth_topic = f"GOSOLR/BRAIN/{imei}/SYSTEM-HEALTH"
        test_systemhealth_payload = {"totalConsumptionPrediction": "-", "efficiency": "-", "water": {
            "device": {"-": "-", "-": "-"}}, "consumptionStatus": "-", "chargeStatus": "-"}
        mqtt_connection.publish(
            topic=test_systemhealth_topic,
            payload=json.dumps(test_systemhealth_payload),
            qos=mqtt5.QoS.AT_LEAST_ONCE,
            retain=False
        )
        print(
            f"📡 Sent SYSTEM-HEALTH to {test_systemhealth_topic}: {test_systemhealth_payload}")
        time.sleep(0.1)  # optional pause between sends


def publish_relays(imei):
    t = time.gmtime()
    data_timestamp = "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}Z".format(
        t[0], t[1], t[2], t[3], t[4], t[5])

    currentHour = t[3] + 2
    currentMinute = t[4]

    relays_topic = f"GOSOLR/BRAIN/{imei}/RELAYS"
    relays_payload = {"dataTimestamp": data_timestamp, "channel_2": {"name": "Swimming pool", "state": False, "usage": 790}, "channel_3": {
        "name": "Geyser 2", "state": True, "usage": 3003}, "timeStr": data_timestamp, "channel_1": {"name": "Geyser 1", "state": True, "usage": 3197}, "paired": True}
    mqtt_connection.publish(
        topic=relays_topic,
        payload=json.dumps(relays_payload),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False
    )
    print(f"📡 Sent RELAYS to {relays_topic}: {relays_payload}")


def publish_relays_2(imei):
    t = time.gmtime()
    data_timestamp = "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}Z".format(
        t[0], t[1], t[2], t[3], t[4], t[5])

    currentHour = t[3] + 2
    currentMinute = t[4]

    relays_topic = f"GOSOLR/BRAIN/{imei}/RELAYS"
    relays_payload = {"dataTimestamp": data_timestamp, "channel_2": {"name": "Geyser 2", "state": True, "usage": 2790}, "channel_3": {"name": "Swimming pool", "state": True, "usage": 690},
                      "timeStr": data_timestamp, "channel_1": {"name": "Geyser 1", "state": True, "usage": 3197}, "channel_4": {"name": "Underfloor heating", "state": False, "usage": 0}, "paired": True}
    mqtt_connection.publish(
        topic=relays_topic,
        payload=json.dumps(relays_payload),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False
    )
    print(f"📡 Sent RELAYS to {relays_topic}: {relays_payload}")


def publish_relaycontrol_2(imei):
    t = time.gmtime()
    data_timestamp = "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}Z".format(
        t[0], t[1], t[2], t[3], t[4], t[5])

    currentHour = t[3] + 2
    currentMinute = t[4]

    if (9 <= currentHour < 11) or (13 <= currentHour < 15):
        channel_1_state = True
    else:
        channel_1_state = False

    if (11 <= currentHour < 13) or (15 <= currentHour < 16):
        channel_2_state = True
    else:
        channel_2_state = False

    if (9 <= currentHour < 12) or (14 <= currentHour < 16):
        channel_3_state = True
    else:
        channel_3_state = False

    relaycontrol_topic = f"GOSOLR/BRAIN/{imei}/RELAYCONTROL"
    relaycontrol_payload = {"relay": "1", "dataTimestamp": data_timestamp, "timeStr": data_timestamp, "imei": imei, "source": "brain", "controls": [{"channel_1": "Geyser 1", "state": channel_1_state}, {
        "channel_3": "Swimming pool", "state": channel_3_state}, {"state": channel_2_state, "channel_2": "Geyser 2"}, {"state": False, "channel_4": "Underfloor heating"}], "paired": True}
    mqtt_connection.publish(
        topic=relaycontrol_topic,
        payload=json.dumps(relaycontrol_payload),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False
    )
    print(
        f"📡 Sent RELAYCONTROL to {relaycontrol_topic}: {relaycontrol_payload}")


def publish_data(imei):
    t = time.gmtime()
    data_timestamp = "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}Z".format(
        t[0], t[1], t[2], t[3], t[4], t[5])

    currentHour = t[3] + 2
    currentMinute = t[4]
    # 2501142533
    data_topic = f"GOSOLR/BRAIN/{imei}/DATA"
    data_payload = {"dataTimestamp": data_timestamp, "timeStr": data_timestamp, "inverterID": "2503250271", "fac": 49.91, "uPv1": 195.2, "uPv2": 232.2, "uPv3": 228.2, "iPv1": 1.4,
                    "iPv2": 0.6, "iPv3": 0.6, "uAc1": 223.6, "iAc1": 14.5, "inverterTemperature": 48.2, "gridPower": 150, "batteryVoltage": 52.47, "batteryCurrent": 53.5, "SoC": 99}
    mqtt_connection.publish(
        topic=data_topic,
        payload=json.dumps(data_payload),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False
    )
    print(f"📡 Sent DATA to {data_topic}: {data_payload}")


def publish_relaycontrol(imei):
    t = time.gmtime()
    data_timestamp = "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}Z".format(
        t[0], t[1], t[2], t[3], t[4], t[5])

    currentHour = t[3] + 2
    currentMinute = t[4]

    if (7 <= currentHour < 9) or (11 <= currentHour < 13) or (15 <= currentHour < 17):
        channel_1_state = True
    else:
        channel_1_state = False

    if (10 <= currentHour < 13) or (15 <= currentHour < 18):
        channel_2_state = True
    else:
        channel_2_state = False

    if (8 <= currentHour < 10) or (13 <= currentHour < 15) or (16 <= currentHour < 18):
        channel_3_state = True
    else:
        channel_3_state = False

    relaycontrol_topic = f"GOSOLR/BRAIN/{imei}/RELAYCONTROL"
    relaycontrol_payload = {"relay": "1", "dataTimestamp": data_timestamp, "timeStr": data_timestamp, "imei": "868373070929676", "source": "brain", "controls": [
        {"channel_1": "Geyser 1", "state": channel_1_state}, {"channel_3": "Geyser 2", "state": channel_3_state}, {"state": channel_2_state, "channel_2": "Swimming pool"}], "paired": True}
    mqtt_connection.publish(
        topic=relaycontrol_topic,
        payload=json.dumps(relaycontrol_payload),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False
    )
    print(
        f"📡 Sent RELAYCONTROL to {relaycontrol_topic}: {relaycontrol_payload}")


def publish_relaycontrol_lyle(imei):
    t = time.gmtime()
    data_timestamp = "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}Z".format(
        t[0], t[1], t[2], t[3], t[4], t[5])

    currentHour = t[3] + 2
    currentMinute = t[4]

    if (5 <= currentHour <= 16):
        channel_4_state = True
    else:
        channel_4_state = False

    relaycontrol_topic = f"GOSOLR/BRAIN/{imei}/RELAYCONTROL"
    relaycontrol_payload = {"relay": "1", "dataTimestamp": data_timestamp, "timeStr": data_timestamp, "imei": "868373070934429",
                            "source": "brain", "controls": [{"channel_4": "Swimming pool", "state": channel_4_state}], "paired": True}
    mqtt_connection.publish(
        topic=relaycontrol_topic,
        payload=json.dumps(relaycontrol_payload),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False
    )
    print(
        f"📡 Sent RELAYCONTROL to {relaycontrol_topic}: {relaycontrol_payload}")


def publish_relays_pool(imei):
    t = time.gmtime()
    data_timestamp = "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}Z".format(
        t[0], t[1], t[2], t[3], t[4], t[5])

    currentHour = t[3] + 2
    currentMinute = t[4]

    relays_topic = f"GOSOLR/BRAIN/{imei}/RELAYS"
    relays_payload = {"dataTimestamp": data_timestamp, "channel_1": {
        "name": "Swimming pool", "state": True, "usage": 797}, "paired": True}
    mqtt_connection.publish(
        topic=relays_topic,
        payload=json.dumps(relays_payload),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False
    )
    print(f"📡 Sent RELAYS to {relays_topic}: {relays_payload}")

    if (10 <= currentHour < 13) or (15 <= currentHour < 17):
        channel_4_state = True
    else:
        channel_4_state = False

    relaycontrol_topic = f"GOSOLR/BRAIN/{imei}/RELAYCONTROL"
    relaycontrol_payload = {"relay": "1", "dataTimestamp": data_timestamp, "timeStr": data_timestamp, "imei": imei,
                            "source": "brain", "controls": [{"channel_1": "Swimming pool", "state": channel_4_state}], "paired": True}
    mqtt_connection.publish(
        topic=relaycontrol_topic,
        payload=json.dumps(relaycontrol_payload),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False
    )
    print(
        f"📡 Sent RELAYCONTROL to {relaycontrol_topic}: {relaycontrol_payload}")


def publish_relays_geyser(imei):
    t = time.gmtime()
    data_timestamp = "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}Z".format(
        t[0], t[1], t[2], t[3], t[4], t[5])

    currentHour = t[3] + 2
    currentMinute = t[4]

    relays_topic = f"GOSOLR/BRAIN/{imei}/RELAYS"
    relays_payload = {"dataTimestamp": data_timestamp, "channel_1": {
        "name": "Geyser", "state": True, "usage": 3197}, "paired": True}
    mqtt_connection.publish(
        topic=relays_topic,
        payload=json.dumps(relays_payload),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False
    )
    print(f"📡 Sent RELAYS to {relays_topic}: {relays_payload}")

    if (3 <= currentHour <= 4) or (11 <= currentHour < 13) or (15 <= currentHour < 17):
        channel_4_state = True
    else:
        channel_4_state = False

    relaycontrol_topic = f"GOSOLR/BRAIN/{imei}/RELAYCONTROL"
    relaycontrol_payload = {"relay": "1", "dataTimestamp": data_timestamp, "timeStr": data_timestamp, "imei": imei,
                            "source": "brain", "controls": [{"channel_1": "Geyser", "state": channel_4_state}], "paired": True}
    mqtt_connection.publish(
        topic=relaycontrol_topic,
        payload=json.dumps(relaycontrol_payload),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False
    )
    print(
        f"📡 Sent RELAYCONTROL to {relaycontrol_topic}: {relaycontrol_payload}")


def publish_relays_muller(imei):
    t = time.gmtime()
    data_timestamp = "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}Z".format(
        t[0], t[1], t[2], t[3], t[4], t[5])

    currentHour = t[3] + 2
    currentMinute = t[4]

    relays_topic = f"GOSOLR/BRAIN/{imei}/RELAYS"
    relays_payload = {"dataTimestamp": data_timestamp, "channel_1": {
        "name": "Geyser", "state": True, "usage": 3197}, "channel_2": {"name": "Swimming pool", "state": True, "usage": 797}, "paired": True}
    mqtt_connection.publish(
        topic=relays_topic,
        payload=json.dumps(relays_payload),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False
    )
    print(f"📡 Sent RELAYS to {relays_topic}: {relays_payload}")

    if (3 <= currentHour <= 4) or (11 <= currentHour < 13) or (15 <= currentHour < 17):
        channel_1_state = True
    else:
        channel_1_state = False

    if (9 <= currentHour <= 11) or (14 <= currentHour < 17):
        channel_2_state = True
    else:
        channel_2_state = False

    relaycontrol_topic = f"GOSOLR/BRAIN/{imei}/RELAYCONTROL"
    relaycontrol_payload = {"relay": "1", "dataTimestamp": data_timestamp, "timeStr": data_timestamp, "imei": imei,
                            "source": "brain", "controls": [{"channel_1": "Geyser", "state": channel_1_state}, {"channel_2": "Swimming pool", "state": channel_2_state}], "paired": True}
    mqtt_connection.publish(
        topic=relaycontrol_topic,
        payload=json.dumps(relaycontrol_payload),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False
    )
    print(
        f"📡 Sent RELAYCONTROL to {relaycontrol_topic}: {relaycontrol_payload}")


def main():
    print("Connecting to AWS IoT Core...")
    mqtt_connection.connect().result()
    print("✅ Connected to AWS IoT Core")

    try:
        print("\n🔄 Publishing data cycle started...")
        imei = "868373070929676"
        publish_status(imei)
        publish_heartbeat(imei)
        publish_relays(imei)
        publish_relaycontrol(imei)
        publish_systemhealth(imei)
        # publish_data(imei)

        imei = "868373070933520"
        publish_status(imei)
        publish_heartbeat(imei)
        publish_systemhealth(imei)
        publish_relays_2(imei)
        publish_relaycontrol_2(imei)

        imei = "868373070934429"
        publish_relaycontrol_lyle(imei)

        imei = "868373072914858"
        publish_status(imei)
        publish_heartbeat(imei)
        publish_relays_geyser(imei)
        # publish_relaycontrol(imei)
        publish_systemhealth(imei)
        # publish_data(imei)

        imei = "868373072921846"
        publish_status(imei)
        publish_heartbeat(imei)
        publish_relays_geyser(imei)
        # publish_relaycontrol(imei)
        publish_systemhealth(imei)
        # publish_data(imei)868373070928215

        imei = "868373070916525"
        publish_status(imei)
        publish_heartbeat(imei)
        publish_relays_geyser(imei)
        # publish_relaycontrol(imei)
        publish_systemhealth(imei)
        # publish_data(imei)

        imei = "868373072917463"
        publish_status(imei)
        publish_heartbeat(imei)
        publish_relays_geyser(imei)
        # publish_relaycontrol(imei)
        publish_systemhealth(imei)
        # publish_data(imei)

        imei = "868373070928215"
        publish_status(imei)
        publish_heartbeat(imei)
        publish_relays_geyser(imei)
        # publish_relaycontrol(imei)
        publish_systemhealth(imei)
        # publish_data(imei)

        imei = "868373072915533"
        publish_status(imei)
        publish_heartbeat(imei)
        publish_relays_pool(imei)
        # publish_relaycontrol(imei)
        publish_systemhealth(imei)
        # publish_data(imei)

        imei = "868373070929098"
        publish_status(imei)
        publish_heartbeat(imei)
        publish_relays_muller(imei)
        # publish_relaycontrol(imei)
        publish_systemhealth(imei)
        # publish_data(imei)

        imei = "868373070935079"
        publish_status(imei)
        publish_heartbeat(imei)
        publish_systemhealth(imei)

        # publish_test()
    except KeyboardInterrupt:
        print("\n🛑 Interrupted by user. Disconnecting...")
        mqtt_connection.disconnect().result()
        print("✅ Disconnected. Exiting.")
        sys.exit(0)


if __name__ == "__main__":
    main()
