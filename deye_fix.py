import json
import time
import random
from datetime import datetime
from urllib.request import Request, urlopen
import hashlib

import math

from awscrt import mqtt, mqtt5
from awsiot import mqtt5_client_builder

def error_handle(imei, error):
    t = time.gmtime()
    data_timestamp = "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}Z".format(
        t[0], t[1], t[2], t[3], t[4], t[5])

    TOPICERROR = f"GOSOLR/ERRORS/{imei}"

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

    error_000_nlp = [
        "There is a general error on this Brain",
        "A general error on this Brain has been identified",
        "This Brain is exhibited erroneous behaviour",
        "An anomalous trend was detected on this Brain",
        "This Brain has restarted due to a system error"
    ]
    m_key_000 = [
        "E52-P-K",
        "E48-P-P",
        "E52-L-P"
    ]
    m_key_001 = [
        "E47-D-D",
        "E47-D-E",
        "E50-K-P"
    ]
    m_key_002 = [
        "S02-A-B",
        "S01-A-A",
        "S02-B-G"
    ]
    error_019_nlp = [
        "There is a fault on the inverter main board",
        "The RS485 Meter Port appears to be faulty"
    ]
    m_key_019 = [
        "E14-W-E",
        "E69-P-R"
    ]

    error_001_nlp = [
        "The registers reported corrupted values",
        "The registers could not be read properly",
        "There appears to be a fault on the communication line",
        "An error occurred when reading the registers",
        "It looks like there is a fault in the communication protocol",
        "Pins are misaligned between the Brain and inverter",
        "The communication cable is likely twisted"
    ]
    error_002_nlp = [
        "There is an inconsistency in system settings",
        "This Brain is not registered correctly",
        "The plant could not be found on Dynamo"
    ]

    # Assign nlp_response only if error is "0"
    if error == "0":
        error_type = "000"
        nlp_response = random.choice(error_000_nlp)
        matched_key = random.choice(m_key_000)
    else:
        if error == "1":
            error_type = "001"
            nlp_response = random.choice(error_001_nlp)
            matched_key = random.choice(m_key_001)
        else:
            if error == "2":
                error_type = "002"
                nlp_response = random.choice(error_002_nlp)
                matched_key = random.choice(m_key_002)
            else:
                if error == "19":
                    error_type = "019"
                    nlp_response = random.choice(error_019_nlp)
                    matched_key = random.choice(m_key_019)
                else:
                    error_type = "100"
                    nlp_response = "NA"
                    matched_key = "NA"
    

    payload_data = {
        "error": {
            "flag": error_type,
            "nlp": nlp_response,
            "m_key": matched_key
        },
        "timeStr": data_timestamp,
        "dataTimestamp": data_timestamp,
    }

    res = mqtt_connection.publish(
        topic=TOPICERROR,
        payload=json.dumps(payload_data),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )

    while not res[0].done():
        time.sleep(0.1)

def run_data_deye3p(imei, inverter_serial):
    t = time.gmtime()
    data_timestamp = "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}Z".format(
        t[0], t[1], t[2], t[3], t[4], t[5])

    print(f"{data_timestamp}: DATA for IMEI {imei}")

    TOPICDATA = f"GOSOLR/BRAIN/{imei}/DATA"
    TOKEN = "238c59c51665df09c9bc72daaa9c48074003939bac857a109f0b767b9d4e8622"
    KEY = "28c595aa93939bab9d"
    URL_BASE = "https://gsm.gosolr.co.za"
    SERIAL_NUMBER = inverter_serial

    req = Request(f"{URL_BASE}/solarman/device/sn/{SERIAL_NUMBER}")
    req.add_header("Authorization", f"Bearer {TOKEN}")
    req.add_header("x-api-key", KEY)
    content = urlopen(req).read()

    raw_data = content.decode("utf-8")
    raw_dict = json.loads(raw_data)

    # Check if the status "failed" and print out the error message
    if raw_dict.get("status") == "failed":
        err_msg = raw_dict.get("message", "<no message provided>")
        print(f"⚠️ API reported failure: {err_msg}")
        return

    json_data = raw_dict.get("data").get("data")

    fac = "registerReadError"
    inverterID = "registerReadError"
    uPv1 = "registerReadError"
    uPv2 = "registerReadError"
    iPv1 = "registerReadError"
    iPv2 = "registerReadError"
    iAc1 = "registerReadError"
    uAc1 = "registerReadError"
    SoC = "registerReadError"
    inverterTemperature = "registerReadError"
    batteryVoltage = "registerReadError"
    batteryCurrent = "registerReadError"
    batteryTodayChargeEnergy = "registerReadError"
    batteryTodayDischargeEnergy = "registerReadError"
    gridPurchasedTodayEnergy = "registerReadError"
    pSUM = "registerReadError"
    homeLoadTodayEnergy = "registerReadError"
    bypassLoadPower = "registerReadError"
    bypassAcCurrent = "registerReadError"
    bypassAcVoltage = "registerReadError"
    familyLoadPower = "registerReadError"
    eToday = "registerReadError"
    gridTiePower = "registerReadError"
    gridPower = "registerReadError"

    # print(json.dumps(json_data, indent=2, sort_keys=True))
    bypassAcVoltage = 0
    bypassAcCurrent = 0
    if isinstance(json_data, dict):
        for key, value in json_data.items():
            if isinstance(value, list):
                for entry in value:
                    if "key" in entry:
                        if entry["name"] == "Grid Frequency":
                            fac = entry["value"]
                        if entry["name"] == "SN":
                            inverterID = entry["value"]
                        if entry["name"] == "DC Voltage PV1":
                            uPv1 = entry["value"]
                        if entry["name"] == "DC Voltage PV2":
                            uPv2 = entry["value"]
                        if entry["name"] == "DC Current PV1":
                            iPv1 = entry["value"]
                        if entry["name"] == "DC Current PV2":
                            iPv2 = entry["value"]
                        if entry["name"] == "AC Voltage R/U/A":
                            uAc1 = entry["value"]
                        if entry["name"] == "AC Voltage S/V/B":
                            uAc2 = entry["value"]
                        if entry["name"] == "AC Voltage T/W/C":
                            uAc3 = entry["value"]
                        if entry["name"] == "AC Current R/U/A":
                            iAc1 = entry["value"]
                        if entry["name"] == "AC Current S/V/B":
                            iAc2 = entry["value"]
                        if entry["name"] == "AC Current T/W/C":
                            iAc3 = entry["value"]
                        if entry["name"] == "SoC":
                            SoC = entry["value"]
                        if entry["name"] == "AC Temperature":
                            inverterTemperature = entry["value"]
                        if entry["name"] == "Battery Voltage":
                            batteryVoltage = entry["value"]
                        if entry["name"] == "Battery Current":
                            batteryCurrent = entry["value"]
                        if entry["name"] == "Daily Charging Energy":
                            batteryTodayChargeEnergy = entry["value"]
                        if entry["name"] == "Daily Discharging Energy":
                            batteryTodayDischargeEnergy = entry["value"]
                        if entry["key"] == "E_B_D":
                            gridPurchasedTodayEnergy = entry["value"]
                        if entry["key"] == "E_S_D":
                            gridSoldTodayEnergy = entry["value"]
                        if entry["key"] == "Et_ge0":
                            pSUM = entry["value"]
                        if entry["key"] == "Etdy_use1":
                            homeLoadTodayEnergy = entry["value"]
                        if entry["key"] == "E_Puse_t1":
                            bypassLoadPower = entry["value"]
                        if entry["key"] == "G_C_L1":
                            bypassAcCurrent = entry["value"]
                        if entry["key"] == "G_V_L1":
                            bypassAcVoltage = entry["value"]
                        if entry["key"] == "E_Puse_t1":
                            familyLoadPower = entry["value"]
                        if entry["key"] == "Etdy_ge1":
                            eToday = entry["value"]
    else:
        print("Unexpected JSON structure:", raw_dict)

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

    res = mqtt_connection.publish(
        topic=TOPICDATA,
        payload=json.dumps(
            {
                "inverterID": inverterID,
                "eToday": eToday,
                "fac": fac,
                "uPv1": uPv1,
                "uPv2": uPv2,
                "iPv1": iPv1,
                "iPv2": iPv2,
                "uAc1": uAc1,
                "iAc1": iAc1,
                "uAc2": uAc2,
                "iAc2": iAc2,
                "uAc3": uAc3,
                "iAc3": iAc3,
                "inverterTemperature": inverterTemperature,
                "batteryVoltage": batteryVoltage,
                "batteryCurrent": batteryCurrent,
                "SoC": SoC,
                "batteryTodayChargeEnergy": batteryTodayChargeEnergy,
                "batteryTodayDischargeEnergy": batteryTodayDischargeEnergy,
                "bypassAcVoltage": bypassAcVoltage,
                "bypassAcCurrent": bypassAcCurrent,
                "gridPurchasedTodayEnergy": gridPurchasedTodayEnergy,
                "gridSoldTodayEnergy": gridSoldTodayEnergy,
                "familyLoadPower": familyLoadPower,
                "bypassLoadPower": bypassLoadPower,
                "pSUM": pSUM,
                "homeLoadTodayEnergy": homeLoadTodayEnergy,
                "timeStr": data_timestamp,
                "dataTimestamp": data_timestamp,
            }
        ),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )

    while not res[0].done():
        time.sleep(0.1)

    return familyLoadPower


def run_data(imei, inverter_serial):
    t = time.gmtime()
    data_timestamp = "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}Z".format(
        t[0], t[1], t[2], t[3], t[4], t[5])

    print(f"{data_timestamp}: DATA for IMEI {imei}")

    TOPICDATA = f"GOSOLR/BRAIN/{imei}/DATA"
    TOPICKEYMETRICS = f"GOSOLR/BRAIN/{imei}/KEY-METRICS"
    TOKEN = "238c59c51665df09c9bc72daaa9c48074003939bac857a109f0b767b9d4e8622"
    KEY = "28c595aa93939bab9d"
    URL_BASE = "https://gsm.gosolr.co.za"
    SERIAL_NUMBER = inverter_serial

    req = Request(f"{URL_BASE}/solarman/device/sn/{SERIAL_NUMBER}")
    req.add_header("Authorization", f"Bearer {TOKEN}")
    req.add_header("x-api-key", KEY)
    content = urlopen(req).read()

    raw_data = content.decode("utf-8")
    raw_dict = json.loads(raw_data)

    # Check if the status "failed" and print out the error message
    if raw_dict.get("status") == "failed":
        err_msg = raw_dict.get("message", "<no message provided>")
        print(f"⚠️ API reported failure: {err_msg}")
        return

    json_data = raw_dict.get("data").get("data")

    fac = "registerReadError"
    inverterID = "registerReadError"
    uPv1 = "registerReadError"
    uPv2 = "registerReadError"
    iPv1 = "registerReadError"
    iPv2 = "registerReadError"
    iAc1 = "registerReadError"
    uAc1 = "registerReadError"
    SoC = "registerReadError"
    inverterTemperature = "registerReadError"
    batteryVoltage = "registerReadError"
    batteryCurrent = "registerReadError"
    batteryTodayChargeEnergy = "registerReadError"
    batteryTodayDischargeEnergy = "registerReadError"
    gridPurchasedTodayEnergy = "registerReadError"
    pSUM = "registerReadError"
    homeLoadTodayEnergy = "registerReadError"
    bypassLoadPower = "registerReadError"
    bypassAcCurrent = "registerReadError"
    bypassAcVoltage = "registerReadError"
    familyLoadPower = "registerReadError"
    eToday = "registerReadError"
    gridTiePower = "registerReadError"
    gridPower = "registerReadError"

    # print(json.dumps(json_data, indent=2, sort_keys=True))
    bypassAcVoltage = 0
    bypassAcCurrent = 0
    if isinstance(json_data, dict):
        for key, value in json_data.items():
            if isinstance(value, list):
                for entry in value:
                    if "key" in entry:
                        # print(entry["key"])
                        # print(entry["value"])
                        # print(entry["name"])
                        # print(entry["unit"])
                        if entry["name"] == "Grid Frequency":
                            fac = entry["value"]
                        if entry["name"] == "SN":
                            inverterID = entry["value"]
                        if entry["name"] == "DC Voltage PV1":
                            uPv1 = entry["value"]
                        if entry["name"] == "DC Voltage PV2":
                            uPv2 = entry["value"]
                        if entry["name"] == "DC Current PV1":
                            iPv1 = entry["value"]
                        if entry["name"] == "DC Current PV2":
                            iPv2 = entry["value"]
                        if entry["name"] == "AC Current R/U/A":
                            iAc1 = entry["value"]
                        if entry["name"] == "AC Voltage R/U/A":
                            uAc1 = entry["value"]
                        if entry["name"] == "SoC":
                            SoC = entry["value"]
                        if entry["name"] == "AC Temperature":
                            inverterTemperature = entry["value"]
                        if entry["name"] == "Battery Voltage":
                            batteryVoltage = entry["value"]
                        if entry["name"] == "Battery Current":
                            batteryCurrent = entry["value"]
                        if entry["name"] == "Daily Charging Energy":
                            batteryTodayChargeEnergy = entry["value"]
                        if entry["name"] == "Daily Discharging Energy":
                            batteryTodayDischargeEnergy = entry["value"]
                        if entry["key"] == "Etdy_pu1":
                            gridPurchasedTodayEnergy = entry["value"]
                        if entry["key"] == "Et_ge0":
                            pSUM = entry["value"]
                        if entry["key"] == "Etdy_use1":
                            homeLoadTodayEnergy = entry["value"]
                        if entry["key"] == "E_Puse_t1":
                            bypassLoadPower = entry["value"]
                        if entry["key"] == "G_C_LN":
                            bypassAcCurrent = entry["value"]
                        if entry["key"] == "G_V_LN":
                            bypassAcVoltage = entry["value"]
                        if entry["key"] == "E_Puse_t1":
                            familyLoadPower = entry["value"]
                        if entry["key"] == "Etdy_ge1":
                            eToday = entry["value"]
                        if entry["key"] == "G_T_P":  # E_CT_P
                            gridTiePower = entry["value"]
                        if entry["key"] == "PG_Pt1":  # E_CT_P
                            gridPower = entry["value"]
    else:
        print("Unexpected JSON structure:", raw_dict)

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

    res = mqtt_connection.publish(
        topic=TOPICDATA,
        payload=json.dumps(
            {
                "inverterID": inverterID,
                "eToday": eToday,
                "fac": fac,
                "uPv1": uPv1,
                "uPv2": uPv2,
                "iPv1": iPv1,
                "iPv2": iPv2,
                "uAc1": uAc1,
                "iAc1": iAc1,
                "inverterTemperature": inverterTemperature,
                "batteryVoltage": batteryVoltage,
                "batteryCurrent": batteryCurrent,
                "SoC": SoC,
                "batteryTodayChargeEnergy": batteryTodayChargeEnergy,
                "batteryTodayDischargeEnergy": batteryTodayDischargeEnergy,
                "bypassAcVoltage": bypassAcVoltage,
                "bypassAcCurrent": bypassAcCurrent,
                "gridPurchasedTodayEnergy": gridPurchasedTodayEnergy,
                "gridSoldTodayEnergy": 0,
                "familyLoadPower": familyLoadPower,
                "bypassLoadPower": bypassLoadPower,
                "pSUM": pSUM,
                "homeLoadTodayEnergy": homeLoadTodayEnergy,
                "gridTiePower": gridTiePower,
                "gridPower": gridPower,
                "timeStr": data_timestamp,
                "dataTimestamp": data_timestamp,
            }
        ),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )

    res = mqtt_connection.publish(
        topic=TOPICKEYMETRICS,
        payload=json.dumps(
            {"fields": {"psum": pSUM, "homeloadtodayenergy": homeLoadTodayEnergy, "soc": SoC, "etoday": eToday,
                        "fac": fac, "bypassloadpower": bypassLoadPower}, "timeStr": data_timestamp, "dataTimestamp": data_timestamp}
        ),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )

    if (inverterID == "registerReadError"):
        error_handle(imei,"1")

    while not res[0].done():
        time.sleep(0.1)


MQTT_BROKER_ENDPOINT = "a2z4csjj2fxwmw-ats.iot.eu-west-1.amazonaws.com"
CLIENT_ID = "hardware-pi"

IOT_CERTIFICATE = """-----BEGIN CERTIFICATE-----
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

IOT_PRIVATE_KEY = """-----BEGIN RSA PRIVATE KEY-----
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

try:
    run_data(imei="868373070931227", inverter_serial="2209158492")
except:
    print("error")
    error_handle(imei="868373070931227", error="2")

try:
    run_data(imei="868373070931565", inverter_serial="2501124292")
except:
    print("error")
    error_handle(imei="868373070931565", error="2")

try:
    run_data(imei="868373070931102", inverter_serial="2206276178")
except:
    print("error")
    error_handle(imei="868373070931102", error="19")

try:
    run_data(imei="868373070933603", inverter_serial="2304288455")
except:
    print("error")
    error_handle(imei="868373070933603", error="2")

try:
    run_data(imei="868373070932639", inverter_serial="2303266007")
except:
    print("error")
    error_handle(imei="868373070932639", error="2")

try:
    run_data(imei="868373070931664", inverter_serial="2211238422")
except:
    print("error")
    error_handle(imei="868373070931664", error="2")

try:
    run_data(imei="868373070933363", inverter_serial="2209257308")
except:
    print("error")
    error_handle(imei="868373070933363", error="2")

try:
    run_data(imei="868373070931177", inverter_serial="2211166414")
except:
    print("error")
    error_handle(imei="868373070931177", error="2")

try:
    run_data(imei="868373070933116", inverter_serial="2304256477")
except:
    print("error")
    error_handle(imei="868373070933116", error="0")

try:
    run_data(imei="868373070932720", inverter_serial="2303200214")
except:
    print("error")
    error_handle(imei="868373070932720", error="0")

try:
    run_data(imei="868373070931524", inverter_serial="2208068231")
except:
    print("error")
    error_handle(imei="868373070931524", error="0")

try:
    run_data(imei="868373070930849", inverter_serial="2303250346")
except:
    print("error")
    error_handle(imei="868373070930849", error="0")

try:
    run_data(imei="868373070933843", inverter_serial="2106294063")
except:
    print("error")
    error_handle(imei="868373070933843", error="0")

try:
    run_data(imei="868373070932522", inverter_serial="2306090282")
except:
    print("error")
    error_handle(imei="868373070932522", error="0")

try:
    run_data(imei="868373070931292", inverter_serial="2305066035")
except:
    print("error")
    error_handle(imei="868373070931292", error="0")

try:
    run_data(imei="868373070933041", inverter_serial="2304260750")
except:
    print("error")
    error_handle(imei="868373070933041", error="0")

try:
    run_data(imei="868373070930112", inverter_serial="2208182472")
except:
    print("error")
    error_handle(imei="868373070930112", error="0")

try:
    run_data(imei="868373070930385", inverter_serial="2211017640")
except:
    print("error")
    error_handle(imei="868373070930385", error="0")

try:
    run_data(imei="868373070935210", inverter_serial="2304254298")
except:
    print("error")
    error_handle(imei="868373070935210", error="0")

try:
    run_data(imei="868373070917051", inverter_serial="2304156386")
except:
    print("error")
    error_handle(imei="868373070917051", error="0")

try:
    run_data(imei="868373070928538", inverter_serial="2107179045")
except:
    print("error")
    error_handle(imei="868373070928538", error="0")

try:
    run_data(imei="868373070936259", inverter_serial="2210159573")
except:
    print("error")
    error_handle(imei="868373070936259", error="0")

try:
    run_data(imei="868373070935921", inverter_serial="2208278932")
except:
    print("error")
    error_handle(imei="868373070935921", error="0")

try:
    run_data(imei="868373070927647", inverter_serial="2304158510")
except:
    print("error")
    error_handle(imei="868373070927647", error="0")

try:
    run_data(imei="868373070920980", inverter_serial="2306200231")
except:
    print("error")
    error_handle(imei="868373070920980", error="0")

try:
    run_data(imei="868373070915899", inverter_serial="2306178933")
except:
    print("error")
    error_handle(imei="868373070915899", error="0")

try:
    run_data(imei="868373070931433", inverter_serial="2211236035")
except:
    print("error")
    error_handle(imei="868373070931433", error="0")

try:
    run_data(imei="868373070916327", inverter_serial="2211127492")
except:
    print("error")
    error_handle(imei="868373070916327", error="0")

try:
    run_data(imei="868373070916061", inverter_serial="2210145607")
except:
    print("error")
    error_handle(imei="868373070916061", error="0")

try:
    run_data(imei="868373070931276", inverter_serial="2107054365")
except:
    print("error")
    error_handle(imei="868373070931276", error="0")

try:
    run_data(imei="868373070930823", inverter_serial="2305066101")
except:
    print("error")
    error_handle(imei="868373070930823", error="0")

try:
    run_data(imei="868373070932761", inverter_serial="2303078668")
except:
    print("error")
    error_handle(imei="868373070932761", error="0")

try:
    run_data(imei="868373070931508", inverter_serial="2208266617")
except:
    print("error")
    error_handle(imei="868373070931508", error="0")

try:
    run_data(imei="868373070926797", inverter_serial="2209233278")
except:
    print("error")
    error_handle(imei="868373070926797", error="0")

try:
    run_data(imei="868373070931441", inverter_serial="2107319089")
except:
    print("error")
    error_handle(imei="868373070931441", error="0")

try:
    run_data(imei="868373070931060", inverter_serial="2506022293")
except:
    print("error")
    error_handle(imei="868373070931060", error="0")

try:
    run_data(imei="868373070927167", inverter_serial="2506025130")
except:
    print("error")
    error_handle(imei="868373070927167", error="0")

try:
    run_data(imei="868373070931540", inverter_serial="2304198322")
except:
    print("error")
    error_handle(imei="868373070931540", error="0")

try:
    run_data(imei="868373070909520", inverter_serial="2501123222")
except:
    print("error")
    error_handle(imei="868373070909520", error="0")

try:
    run_data(imei="866069069856381", inverter_serial="2303046167")
except:
    print("error")
    error_handle(imei="866069069856381", error="0")

try:
    run_data(imei="868373070931326", inverter_serial="2212022364")
except:
    print("error")
    error_handle(imei="868373070931326", error="0")

try:
    run_data(imei="868373070926763", inverter_serial="2208068775")
except:
    print("error")
    error_handle(imei="868373070926763", error="0")

try:
    run_data(imei="868373070930765", inverter_serial="2303068686")
except:
    print("error")
    error_handle(imei="868373070930765", error="0")

try:
    run_data(imei="868373070917184", inverter_serial="2501154134")
except:
    print("error")
    error_handle(imei="868373070917184", error="0")

try:
    run_data(imei="868373070932126", inverter_serial="2501141654")
except:
    print("error")
    error_handle(imei="868373070932126", error="0")

try:
    run_data(imei="868373070928991", inverter_serial="2305116451")
except:
    print("error")
    error_handle(imei="868373070928991", error="0")

try:
    run_data(imei="868373070930088", inverter_serial="2303148004")
except:
    print("error")
    error_handle(imei="868373070930088", error="0")

try:
    run_data(imei="868373070934791", inverter_serial="2211222039")
except:
    print("error")
    error_handle(imei="868373070934791", error="0")

try:
    run_data(imei="868373070932001", inverter_serial="2211282010")
except:
    print("error")
    error_handle(imei="868373070932001", error="0")

try:
    run_data(imei="868373070932233", inverter_serial="2304046516")
except:
    print("error")
    error_handle(imei="868373070932233", error="0")

try:
    run_data(imei="868373070930096", inverter_serial="2501124132")
except:
    print("error")
    error_handle(imei="868373070930096", error="0")

try:
    run_data(imei="868373070929502", inverter_serial="2305126005")
except:
    print("error")
    error_handle(imei="868373070929502", error="0")

try:
    run_data(imei="868373072915657", inverter_serial="2305268422")
except:
    print("error")
    error_handle(imei="868373072915657", error="0")

try:
    run_data(imei="868373070919529", inverter_serial="2303018106")
except:
    print("error")
    error_handle(imei="868373070919529", error="0")

try:
    run_data(imei="868373070931060", inverter_serial="2506022293")
except:
    print("error")
    error_handle(imei="868373070931060", error="0")

try:
    run_data(imei="868373070927167", inverter_serial="2506025130")
except:
    print("error")
    error_handle(imei="868373070927167", error="0")

try:
    run_data(imei="868373070920113", inverter_serial="2506022294")
except:
    print("error")
    error_handle(imei="868373070920113", error="0")

try:
    run_data(imei="868373070917051", inverter_serial="2304156386")
except:
    print("error")
    error_handle(imei="868373070917051", error="0")

try:
    run_data(imei="868373072913561", inverter_serial="2211219272")
except:
    print("error")
    error_handle(imei="868373072913561", error="0")
    
try:
    run_data(imei="868373070936325", inverter_serial="2304261091")
except:
    print("error")
    error_handle(imei="868373070936325", error="0")

print()

# time.sleep(5)
