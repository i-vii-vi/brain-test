import json
import time
from datetime import datetime

from urllib.request import Request, urlopen

# Constants for Inverter data retrieval
TOKEN = "238c59c51665df09c9bc72daaa9c48074003939bac857a109f0b767b9d4e8622"
KEY = "28c595aa93939bab9d"
URL_BASE = "https://gsm.gosolr.co.za"
SERIAL_NUMBER = "2202269098"

from awscrt import mqtt, mqtt5
from awsiot import mqtt5_client_builder

import random

def multiplug(device_id):
    TOPICMODELS = f"GOSOLR/MULTIPLUG/{device_id}/MODELS"
    TOPICRELAYS = f"GOSOLR/MULTIPLUG/{device_id}/RELAYS"
    TOPICUSAGE = f"GOSOLR/MULTIPLUG/{device_id}/USAGE"
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
        topic=TOPICMODELS,
        payload=json.dumps({
            "brain": "1.5.8",
            "plugs": "1.6.4",
            "interface": "0.4.25", 
            "timeStr": datetime.now().isoformat(),
            "dataTimestamp": datetime.now().isoformat()}),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )

    res = mqtt_connection.publish(
        topic=TOPICRELAYS,
        payload=json.dumps({
            "channel_1": {
                "name": "Television/Monitor",
                "state": True,
                "smart": True
                },
            "channel_2": {
                "name": "3D Printer 1",
                "state": True,
                "smart": True
                },
            "channel_3": {
                "name": "3D Printer 2",
                "state": True,
                "smart": True
                },
            "channel_4": {
                "name": "3D Printer 3",
                "state": True,
                "smart": True
                }, 
            "timeStr": datetime.now().isoformat(),
            "dataTimestamp": datetime.now().isoformat()}),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )

    res = mqtt_connection.publish(
        topic=TOPICUSAGE,
        payload=json.dumps({
            "channel_1": {
                "name": "Television/Monitor",
                "load": apply_deviation(120, 0.02)
                },
            "channel_2": {
                "name": "3D Printer 1",
                "load": apply_deviation(300, 0.05)
                },
            "channel_3": {
                "name": "3D Printer 2",
                "load": apply_deviation(400, 0.05)
                },
            "channel_4": {
                "name": "3D Printer 3",
                "load": apply_deviation(3000, 0.05)
                }, 
            "timeStr": datetime.now().isoformat(),
            "dataTimestamp": datetime.now().isoformat()}),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )
    # Needs to wait for future to be complete
    while not res[0].done():
        time.sleep(0.1)

def lightswitch(device_id):
    TOPICMODELS = f"GOSOLR/LIGHTSWITCH/{device_id}/MODELS"
    TOPICRELAYS = f"GOSOLR/LIGHTSWITCH/{device_id}/RELAYS"
    TOPICUSAGE = f"GOSOLR/LIGHTSWITCH/{device_id}/USAGE"
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
        topic=TOPICMODELS,
        payload=json.dumps({
            "brain": "1.5.8",
            "plugs": "1.6.6",
            "interface": "0.0.6", 
            "timeStr": datetime.now().isoformat(),
            "dataTimestamp": datetime.now().isoformat()}),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )

    res = mqtt_connection.publish(
        topic=TOPICRELAYS,
        payload=json.dumps({
            "channel_1": {
                "name": "Switch 1",
                "state": True,
                "smart": True
                },
            "channel_2": {
                "name": "Switch 2",
                "state": True,
                "smart": True
                }, 
            "timeStr": datetime.now().isoformat(),
            "dataTimestamp": datetime.now().isoformat()}),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )

    res = mqtt_connection.publish(
        topic=TOPICUSAGE,
        payload=json.dumps({
            "channel_1": {
                "name": "Switch 1",
                "load": apply_deviation(50, 0.02)
                },
            "channel_2": {
                "name": "Switch 2",
                "load": apply_deviation(30, 0.05)
                }, 
            "timeStr": datetime.now().isoformat(),
            "dataTimestamp": datetime.now().isoformat()}),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )
    # Needs to wait for future to be complete
    while not res[0].done():
        time.sleep(0.1)


def run_device(device_id):
    TOPICMODELS = f"GOSOLR/BRAIN/{device_id}/MODELS"
    TOPICRELAYS = f"GOSOLR/BRAIN/{device_id}/RELAYS"
    TOPICUSAGE = f"GOSOLR/BRAIN/{device_id}/USAGE"
    TOPICRISKS = f"GOSOLR/BRAIN/{device_id}/RISKS"
    TOPICALERTS = f"GOSOLR/BRAIN/{device_id}/ALERTS"
    TOPICDATA = f"GOSOLR/BRAIN/{device_id}/DATA"
    TOPICHB = f"GOSOLR/BRAIN/{device_id}/HB"
    TOPICSTATUS = f"GOSOLR/BRAIN/{device_id}/STATUS"

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
        topic=TOPICMODELS,
        payload=json.dumps({
            "edge": "1.3.0",
            "parsec": "1.4.1(a)",
            "east": "1.0.4",
            "gosolr": "2.1.0",
            "manager": "0.1.4", 
            "timeStr": datetime.now().isoformat(),
            "dataTimestamp": datetime.now().isoformat()}),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )

    res = mqtt_connection.publish(
        topic=TOPICSTATUS,
        payload=json.dumps({
            "connected": True}),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )

    res = mqtt_connection.publish(
        topic=TOPICHB,
        payload=json.dumps({
            "version":"0.7.1(a)",
            "files":[{"name":"capacity.json","md5":"72f2994f1ca6e64a5e5ecd67a2122c2a"},{"name":"coefficients.json","md5":"32bbe29d9f03a93a854415cfb1db1dde"},{"name":"gosolr.py","md5":"a41ac8bbcdbc90008645cbf6e8e96f6b"},{"name":"inv_def.json","md5":"38ad22a7f96a07b0c39ff1b107aeea24"}]}),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )

    res = mqtt_connection.publish(
        topic=TOPICRELAYS,
        payload=json.dumps({
            "channel_1": {
                "name": "Channel 1",
                "state": True,
                "smart": True
                },
            "channel_2": {
                "name": "Channel 2",
                "state": True,
                "smart": True
                },
            "channel_3": {
                "name": "Channel 3",
                "state": False,
                "smart": False
                },
            "channel_4": {
                "name": "Channel 4",
                "state": False,
                "smart": False
                }, 
            "timeStr": datetime.now().isoformat(),
            "dataTimestamp": datetime.now().isoformat()}),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )

    res = mqtt_connection.publish(
        topic=TOPICUSAGE,
        payload=json.dumps({
            "channel_1": {
                "name": "Channel 1",
                "load": apply_deviation(1400, 0.05)
                },
            "channel_2": {
                "name": "Channel 2",
                "load": apply_deviation(1100, 0.05)
                },
            "channel_3": {
                "name": "Channel 3",
                "load": apply_deviation(200, 0.05)
                },
            "channel_4": {
                "name": "Channel 4",
                "load": apply_deviation(300, 0.05)
                }, 
            "timeStr": datetime.now().isoformat(),
            "dataTimestamp": datetime.now().isoformat()}),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )

    res = mqtt_connection.publish(
        topic=TOPICRISKS,
        payload=json.dumps({
            "risk": {
                "unplannedOutage": apply_deviation(200, 0.1),
                "plannedOutage": apply_deviation(100, 0.05),
                "disconnection": apply_deviation(10, 0.1)
                }, 
            "timeStr": datetime.now().isoformat(),
            "dataTimestamp": datetime.now().isoformat()}),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )

    res = mqtt_connection.publish(
        topic=TOPICALERTS,
        payload=json.dumps({
            "alert_1": 0,
            "alert_2": 0,
            "alert_3": 0,
            "alert_4": 0,
            "alert_5": 0,
            "alert_6": 0,
            "alert_7": 0,
            "alert_8": 0, 
            "timeStr": datetime.now().isoformat(),
            "dataTimestamp": datetime.now().isoformat()}),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )

    res = mqtt_connection.publish(
        topic=TOPICDATA,
        payload=json.dumps({
            "inverterID":"",
            "eToday":0,
            "fac":0,
            "uPv1":0,
            "uPv2":0,
            "iPv1":0,
            "iPv2":0,
            "uAc1":0,
            "iAc1":0,
            "inverterTemperature":0,
            "batteryVoltage":0,
            "batteryCurrent":0,
            "SoC":30,
            "batteryTodayChargeEnergy":0,
            "batteryTodayDischargeEnergy":0,
            "bypassAcVoltage":0,
            "bypassAcCurrent":0,
            "gridPurchasedTodayEnergy":0,
            "familyLoadPower":0,
            "bypassLoadPower":0,
            "pSUM":0,
            "homeLoadTodayEnergy":0, 
            "timeStr": datetime.now().isoformat(),
            "dataTimestamp": datetime.now().isoformat()}),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )

    # Needs to wait for future to be complete
    while not res[0].done():
        time.sleep(0.1)


def run_kobus():
    TOPICMODELS = "GOSOLR/BRAIN/864454073547584/MODELS"
    TOPICRELAYS = "GOSOLR/BRAIN/864454073547584/RELAYS"
    TOPICUSAGE = "GOSOLR/BRAIN/864454073547584/USAGE"
    TOPICRISKS = "GOSOLR/BRAIN/864454073547584/RISKS"
    TOPICALERTS = "GOSOLR/BRAIN/864454073547584/ALERTS"
    TOPICDATA = "GOSOLR/BRAIN/864454073547584/DATA"
    TOPICHB = "GOSOLR/BRAIN/864454073547584/HB"
    TOPICSTATUS = "GOSOLR/BRAIN/864454073547584/STATUS"

    # Constants for Inverter data retrieval
    TOKEN = "238c59c51665df09c9bc72daaa9c48074003939bac857a109f0b767b9d4e8622"
    KEY = "28c595aa93939bab9d"
    URL_BASE = "https://gsm.gosolr.co.za"
    SERIAL_NUMBER = "2202269098"
    
    req = Request(f"{URL_BASE}/solarman/device/sn/{SERIAL_NUMBER}")
    req.add_header("Authorization", f"Bearer {TOKEN}")
    req.add_header("x-api-key", KEY)
    content = urlopen(req).read()

    raw_data = content.decode("utf-8")
    raw_dict = json.loads(raw_data)

    # Adjust for nested structure: find the list in the JSON
    if isinstance(raw_dict, dict):  # JSON starts as a dictionary
        for key, value in raw_dict.items():
            if isinstance(value, list):  # Look for the list of objects
                for entry in value:
                    if "key" in entry:  # Check each entry for "key"
                        #print(entry["key"])
                        #print(entry["value"])
                        #print(entry["unit"])
                        if entry["key"] == "PG_F1":
                            fac = entry["value"]
                        if entry["key"] == "SN1":
                            inverterID = entry["value"]
                        if entry["key"] == "DV1":
                            uPv1 = entry["value"]
                        if entry["key"] == "DV2":
                            uPv2 = entry["value"]
                        if entry["key"] == "DC1":
                            iPv1 = entry["value"]
                        if entry["key"] == "DC2":
                            iPv2 = entry["value"]
                        if entry["key"] == "AV1":
                            uAc1 = entry["value"]
                        if entry["key"] == "AV2":
                            uAc2 = entry["value"]
                        if entry["key"] == "AV3":
                            uAc3 = entry["value"]
                        if entry["key"] == "AC1":
                            iAc1 = entry["value"]
                        if entry["key"] == "AC2":
                            iAc2 = entry["value"]
                        if entry["key"] == "AC3":
                            iAc3 = entry["value"]
                        if entry["key"] == "BMS_SOC":
                            SoC = entry["value"]
                        if entry["key"] == "B_T1":
                            inverterTemperature = entry["value"]
                        if entry["key"] == "B_V1":
                            batteryVoltage = entry["value"]
                        if entry["key"] == "B_C1":
                            batteryCurrent = entry["value"]
                        if entry["key"] == "Etdy_cg1":
                            batteryTodayChargeEnergy = entry["value"]
                        if entry["key"] == "Etdy_dcg1":
                            batteryTodayDischargeEnergy = entry["value"]
                        if entry["key"] == "E_B_D":
                            gridPurchasedTodayEnergy = entry["value"]
                        if entry["key"] == "Et_ge0":
                            pSUM = entry["value"]
                        if entry["key"] == "Etdy_ge1":
                            homeLoadTodayEnergy = entry["value"]
                        if entry["key"] == "G_V_L1":
                            bypassAcVoltage = entry["value"]    
                        if entry["key"] == "G_C_L1":
                            bypassAcCurrent = entry["value"]    
                        if entry["key"] == "E_Puse_t1":
                            familyLoadPower = entry["value"]         
                        if entry["key"] == "E_Suse_t1":
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
        topic=TOPICMODELS,
        payload=json.dumps({
            "edge": "1.3.0",
            "parsec": "1.4.1(a)",
            "east": "1.0.4",
            "gosolr": "2.1.0",
            "manager": "0.1.4", 
            "timeStr": datetime.now().isoformat(),
            "dataTimestamp": datetime.now().isoformat()}),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )

    res = mqtt_connection.publish(
        topic=TOPICSTATUS,
        payload=json.dumps({
            "connected": True}),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )

    res = mqtt_connection.publish(
        topic=TOPICHB,
        payload=json.dumps({
            "version":"0.7.1(a)",
            "files":[{"name":"capacity.json","md5":"72f2994f1ca6e64a5e5ecd67a2122c2a"},{"name":"coefficients.json","md5":"32bbe29d9f03a93a854415cfb1db1dde"},{"name":"gosolr.py","md5":"a41ac8bbcdbc90008645cbf6e8e96f6b"},{"name":"inv_def.json","md5":"38ad22a7f96a07b0c39ff1b107aeea24"}]}),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )

    res = mqtt_connection.publish(
        topic=TOPICRELAYS,
        payload=json.dumps({
            "channel_1": {
                "name": "Geyser 1",
                "state": True,
                "smart": True
                },
            "channel_2": {
                "name": "Geyser 2",
                "state": True,
                "smart": True
                },
            "channel_3": {
                "name": "disconnected",
                "state": False,
                "smart": False
                },
            "channel_4": {
                "name": "disconnected",
                "state": False,
                "smart": False
                }, 
            "timeStr": datetime.now().isoformat(),
            "dataTimestamp": datetime.now().isoformat()}),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )

    res = mqtt_connection.publish(
        topic=TOPICUSAGE,
        payload=json.dumps({
            "channel_1": {
                "name": "Geyser 1",
                "state": true,
                "load": apply_deviation(1100, 0.05)
                },
            "channel_2": {
                "name": "Geyser 2",
                "state": true,
                "load": apply_deviation(1200, 0.05)
                },
            "channel_3": {
                "name": "disconnected",
                "state": false,
                "load": 0
                },
            "channel_4": {
                "name": "disconnected",
                "state": false,
                "load": 0
                }, 
            "timeStr": datetime.now().isoformat(),
            "dataTimestamp": datetime.now().isoformat()}),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )

    res = mqtt_connection.publish(
        topic=TOPICRISKS,
        payload=json.dumps({
            "risk": {
                "unplannedOutage": apply_deviation(200, 0.1),
                "plannedOutage": apply_deviation(100, 0.05),
                "disconnection": apply_deviation(10, 0.1)
                }, 
            "timeStr": datetime.now().isoformat(),
            "dataTimestamp": datetime.now().isoformat()}),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )

    res = mqtt_connection.publish(
        topic=TOPICALERTS,
        payload=json.dumps({
            "alert_1": 0,
            "alert_2": 0,
            "alert_3": 0,
            "alert_4": 0,
            "alert_5": 0,
            "alert_6": 0,
            "alert_7": 0,
            "alert_8": 0, 
            "timeStr": datetime.now().isoformat(),
            "dataTimestamp": datetime.now().isoformat()}),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )

    res = mqtt_connection.publish(
        topic=TOPICDATA,
        payload=json.dumps({
            "inverterID":inverterID,
            "eToday":eToday,
            "fac":fac,
            "uPv1":uPv1,
            "uPv2":uPv2,
            "iPv1":iPv1,
            "iPv2":iPv2,
            "uAc1":uAc1,
            "iAc1":iAc1,
            "uAc2":uAc2,
            "iAc2":iAc2,
            "uAc3":uAc3,
            "iAc3":iAc3,
            "inverterTemperature":inverterTemperature,
            "batteryVoltage":batteryVoltage,
            "batteryCurrent":batteryCurrent,
            "SoC":SoC,
            "batteryTodayChargeEnergy":batteryTodayChargeEnergy,
            "batteryTodayDischargeEnergy":batteryTodayDischargeEnergy,
            "bypassAcVoltage":bypassAcVoltage,
            "bypassAcCurrent":bypassAcCurrent,
            "gridPurchasedTodayEnergy":gridPurchasedTodayEnergy,
            "familyLoadPower":familyLoadPower,
            "bypassLoadPower":float(bypassAcVoltage)*float(bypassAcCurrent),
            "pSUM":pSUM,
            "homeLoadTodayEnergy":homeLoadTodayEnergy, 
            "timeStr": datetime.now().isoformat(),
            "dataTimestamp": datetime.now().isoformat()}),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )
    
    # Needs to wait for future to be complete
    while not res[0].done():
        time.sleep(0.1)

def run_andrew():
    TOPICDATA = "GOSOLR/BRAIN/864454073547824/DATA"
    
    # Constants for Inverter data retrieval
    TOKEN = "238c59c51665df09c9bc72daaa9c48074003939bac857a109f0b767b9d4e8622"
    KEY = "28c595aa93939bab9d"
    URL_BASE = "https://gsm.gosolr.co.za"
    SERIAL_NUMBER = "2108049103"
    
    req = Request(f"{URL_BASE}/solarman/device/sn/{SERIAL_NUMBER}")
    req.add_header("Authorization", f"Bearer {TOKEN}")
    req.add_header("x-api-key", KEY)
    content = urlopen(req).read()

    raw_data = content.decode("utf-8")
    raw_dict = json.loads(raw_data)

    # Adjust for nested structure: find the list in the JSON
    if isinstance(raw_dict, dict):  # JSON starts as a dictionary
        for key, value in raw_dict.items():
            if isinstance(value, list):  # Look for the list of objects
                for entry in value:
                    if "key" in entry:  # Check each entry for "key"
                        #print(entry["key"])
                        #print(entry["value"])
                        #print(entry["unit"])
                        if entry["key"] == "PG_F1":
                            fac = entry["value"]
                        if entry["key"] == "SN1":
                            inverterID = entry["value"]
                        if entry["key"] == "DV1":
                            uPv1 = entry["value"]
                        if entry["key"] == "DV2":
                            uPv2 = entry["value"]
                        if entry["key"] == "DC1":
                            iPv1 = entry["value"]
                        if entry["key"] == "DC2":
                            iPv2 = entry["value"]
                        if entry["key"] == "AV1":
                            uAc1 = entry["value"]
                        if entry["key"] == "AC1":
                            iAc1 = entry["value"]
                        if entry["key"] == "B_left_cap1":
                            SoC = entry["value"]
                        if entry["key"] == "B_T1":
                            inverterTemperature = entry["value"]
                        if entry["key"] == "B_V1":
                            batteryVoltage = entry["value"]
                        if entry["key"] == "B_C1":
                            batteryCurrent = entry["value"]
                        if entry["key"] == "Etdy_cg1":
                            batteryTodayChargeEnergy = entry["value"]
                        if entry["key"] == "Etdy_dcg1":
                            batteryTodayDischargeEnergy = entry["value"]
                        if entry["key"] == "EG_Etdy_ge1":
                            gridPurchasedTodayEnergy = entry["value"]
                        if entry["key"] == "Et_ge0":
                            pSUM = entry["value"]
                        if entry["key"] == "Etdy_ge1":
                            homeLoadTodayEnergy = entry["value"]
                        if entry["key"] == "G_V_LN":
                            bypassAcVoltage = entry["value"]    
                        if entry["key"] == "G_C_LN":
                            bypassAcCurrent = entry["value"]    
                        if entry["key"] == "E_Puse_t1":
                            familyLoadPower = entry["value"]         
                        if entry["key"] == "Etdy_use1":
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
        payload=json.dumps({
            "inverterID":inverterID,
            "eToday":eToday,
            "fac":fac,
            "uPv1":uPv1,
            "uPv2":uPv2,
            "iPv1":iPv1,
            "iPv2":iPv2,
            "uAc1":uAc1,
            "iAc1":iAc1,
            "inverterTemperature":inverterTemperature,
            "batteryVoltage":batteryVoltage,
            "batteryCurrent":batteryCurrent,
            "SoC":SoC,
            "batteryTodayChargeEnergy":batteryTodayChargeEnergy,
            "batteryTodayDischargeEnergy":batteryTodayDischargeEnergy,
            "bypassAcVoltage":bypassAcVoltage,
            "bypassAcCurrent":bypassAcCurrent,
            "gridPurchasedTodayEnergy":gridPurchasedTodayEnergy,
            "familyLoadPower":familyLoadPower,
            "bypassLoadPower":float(bypassAcVoltage)*float(bypassAcCurrent),
            "pSUM":pSUM,
            "homeLoadTodayEnergy":homeLoadTodayEnergy, 
            "timeStr": datetime.now().isoformat(),
            "dataTimestamp": datetime.now().isoformat()}),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )
    
    # Needs to wait for future to be complete
    while not res[0].done():
        time.sleep(0.1)

def run_craig():
    TOPICMODELS = "GOSOLR/BRAIN/866069069789269/MODELS"
    TOPICRELAYS = "GOSOLR/BRAIN/866069069789269/RELAYS"
    TOPICUSAGE = "GOSOLR/BRAIN/866069069789269/USAGE"
    TOPICRISKS = "GOSOLR/BRAIN/866069069789269/RISKS"
    TOPICALERTS = "GOSOLR/BRAIN/866069069789269/ALERTS"
    TOPICDATA = "GOSOLR/BRAIN/866069069789269/DATA"
    TOPICHB = "GOSOLR/BRAIN/866069069789269/HB"
    TOPICSTATUS = "GOSOLR/BRAIN/866069069789269/STATUS"

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
        topic=TOPICMODELS,
        payload=json.dumps({
            "edge": "1.3.0",
            "parsec": "1.4.1(a)",
            "east": "1.0.4",
            "gosolr": "2.1.0",
            "manager": "0.1.4", 
            "timeStr": datetime.now().isoformat(),
            "dataTimestamp": datetime.now().isoformat()}),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )

    res = mqtt_connection.publish(
        topic=TOPICSTATUS,
        payload=json.dumps({
            "connected": True}),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )

    res = mqtt_connection.publish(
        topic=TOPICHB,
        payload=json.dumps({
            "version":"0.7.1(a)",
            "files":[{"name":"capacity.json","md5":"72f2994f1ca6e64a5e5ecd67a2122c2a"},{"name":"coefficients.json","md5":"32bbe29d9f03a93a854415cfb1db1dde"},{"name":"gosolr.py","md5":"a41ac8bbcdbc90008645cbf6e8e96f6b"},{"name":"inv_def.json","md5":"38ad22a7f96a07b0c39ff1b107aeea24"}]}),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )

    res = mqtt_connection.publish(
        topic=TOPICRELAYS,
        payload=json.dumps({
            "channel_1": {
                "name": "Channel 1",
                "state": True,
                "smart": True
                },
            "channel_2": {
                "name": "Channel 2",
                "state": True,
                "smart": True
                },
            "channel_3": {
                "name": "Channel 3",
                "state": False,
                "smart": False
                },
            "channel_4": {
                "name": "Channel 4",
                "state": False,
                "smart": False
                }, 
            "timeStr": datetime.now().isoformat(),
            "dataTimestamp": datetime.now().isoformat()}),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )

    res = mqtt_connection.publish(
        topic=TOPICUSAGE,
        payload=json.dumps({
            "channel_1": {
                "name": "Channel 1",
                "load": apply_deviation(1400, 0.05)
                },
            "channel_2": {
                "name": "Channel 2",
                "load": apply_deviation(1100, 0.05)
                },
            "channel_3": {
                "name": "Channel 3",
                "load": apply_deviation(200, 0.05)
                },
            "channel_4": {
                "name": "Channel 4",
                "load": apply_deviation(300, 0.05)
                }, 
            "timeStr": datetime.now().isoformat(),
            "dataTimestamp": datetime.now().isoformat()}),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )

    res = mqtt_connection.publish(
        topic=TOPICRISKS,
        payload=json.dumps({
            "risk": {
                "unplannedOutage": apply_deviation(200, 0.1),
                "plannedOutage": apply_deviation(100, 0.05),
                "disconnection": apply_deviation(10, 0.1)
                }, 
            "timeStr": datetime.now().isoformat(),
            "dataTimestamp": datetime.now().isoformat()}),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )

    res = mqtt_connection.publish(
        topic=TOPICALERTS,
        payload=json.dumps({
            "alert_1": 0,
            "alert_2": 0,
            "alert_3": 0,
            "alert_4": 0,
            "alert_5": 0,
            "alert_6": 0,
            "alert_7": 0,
            "alert_8": 0, 
            "timeStr": datetime.now().isoformat(),
            "dataTimestamp": datetime.now().isoformat()}),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )

    res = mqtt_connection.publish(
        topic=TOPICDATA,
        payload=json.dumps({
            "inverterID":"",
            "eToday":0,
            "fac":0,
            "uPv1":0,
            "uPv2":0,
            "iPv1":0,
            "iPv2":0,
            "uAc1":0,
            "iAc1":0,
            "inverterTemperature":0,
            "batteryVoltage":0,
            "batteryCurrent":0,
            "SoC":30,
            "batteryTodayChargeEnergy":0,
            "batteryTodayDischargeEnergy":0,
            "bypassAcVoltage":0,
            "bypassAcCurrent":0,
            "gridPurchasedTodayEnergy":0,
            "familyLoadPower":0,
            "bypassLoadPower":0,
            "pSUM":0,
            "homeLoadTodayEnergy":0, 
            "timeStr": datetime.now().isoformat(),
            "dataTimestamp": datetime.now().isoformat()}),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )
    
    # Needs to wait for future to be complete
    while not res[0].done():
        time.sleep(0.1)
        
def run_rushil():
    TOPICMODELS = "GOSOLR/BRAIN/864454073558102/MODELS"
    TOPICRELAYS = "GOSOLR/BRAIN/864454073558102/RELAYS"
    TOPICUSAGE = "GOSOLR/BRAIN/864454073558102/USAGE"
    TOPICRISKS = "GOSOLR/BRAIN/864454073558102/RISKS"
    TOPICALERTS = "GOSOLR/BRAIN/864454073558102/ALERTS"

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
        topic=TOPICMODELS,
        payload=json.dumps({
            "edge": "1.3.0",
            "parsec": "1.4.1(a)",
            "east": "1.0.4",
            "gosolr": "2.1.0",
            "manager": "0.1.4", 
            "timeStr": datetime.now().isoformat(),
            "dataTimestamp": datetime.now().isoformat()}),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )

    res = mqtt_connection.publish(
        topic=TOPICRELAYS,
        payload=json.dumps({
            "channel_1": {
                "name": "Geyser 1",
                "state": True,
                "smart": True
                },
            "channel_2": {
                "name": "Swimming Pool",
                "state": True,
                "smart": True
                },
            "channel_3": {
                "name": "Geyser 2",
                "state": False,
                "smart": False
                },
            "channel_4": {
                "name": "disconnected",
                "state": False,
                "smart": False
                }, 
            "timeStr": datetime.now().isoformat(),
            "dataTimestamp": datetime.now().isoformat()}),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )

    res = mqtt_connection.publish(
        topic=TOPICUSAGE,
        payload=json.dumps({
            "channel_1": {
                "name": "Geyser 1",
                "load": apply_deviation(1100, 0.05)
                },
            "channel_2": {
                "name": "Swimming Pool",
                "load": apply_deviation(200, 0.05)
                },
            "channel_3": {
                "name": "Geyser 2",
                "load": apply_deviation(1200, 0.06)
                },
            "channel_4": {
                "name": "disconnected",
                "load": 0
                }, 
            "timeStr": datetime.now().isoformat(),
            "dataTimestamp": datetime.now().isoformat()}),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )

    res = mqtt_connection.publish(
        topic=TOPICRISKS,
        payload=json.dumps({
            "risk": {
                "unplannedOutage": apply_deviation(200, 0.1),
                "plannedOutage": apply_deviation(100, 0.05),
                "disconnection": apply_deviation(10, 0.1)
                }, 
            "timeStr": datetime.now().isoformat(),
            "dataTimestamp": datetime.now().isoformat()}),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )

    res = mqtt_connection.publish(
        topic=TOPICALERTS,
        payload=json.dumps({
            "alert_1": 0,
            "alert_2": 0,
            "alert_3": 0,
            "alert_4": 0,
            "alert_5": 0,
            "alert_6": 0,
            "alert_7": 0,
            "alert_8": 0, 
            "timeStr": datetime.now().isoformat(),
            "dataTimestamp": datetime.now().isoformat()}),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )
    
    # Needs to wait for future to be complete
    while not res[0].done():
        time.sleep(0.1)

def run_andre():
    TOPICMODELS = "GOSOLR/BRAIN/866069069791083/MODELS"
    TOPICRELAYS = "GOSOLR/BRAIN/866069069791083/RELAYS"
    TOPICUSAGE = "GOSOLR/BRAIN/866069069791083/USAGE"
    TOPICRISKS = "GOSOLR/BRAIN/866069069791083/RISKS"
    TOPICALERTS = "GOSOLR/BRAIN/866069069791083/ALERTS"
    TOPICHB = "GOSOLR/BRAIN/866069069791083/HB"
    TOPICSTATUS = "GOSOLR/BRAIN/866069069791083/STATUS"

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
        topic=TOPICMODELS,
        payload=json.dumps({
            "edge": "1.3.0",
            "parsec": "1.4.1(a)",
            "east": "1.0.4",
            "gosolr": "2.1.0",
            "manager": "0.1.4", 
            "timeStr": datetime.now().isoformat(),
            "dataTimestamp": datetime.now().isoformat()}),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )
    
    res = mqtt_connection.publish(
        topic=TOPICSTATUS,
        payload=json.dumps({
            "connected": True}),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )

    res = mqtt_connection.publish(
        topic=TOPICHB,
        payload=json.dumps({
            "version":"0.7.1(a)",
            "files":[{"name":"capacity.json","md5":"72f2994f1ca6e64a5e5ecd67a2122c2a"},{"name":"coefficients.json","md5":"32bbe29d9f03a93a854415cfb1db1dde"},{"name":"gosolr.py","md5":"a41ac8bbcdbc90008645cbf6e8e96f6b"},{"name":"inv_def.json","md5":"38ad22a7f96a07b0c39ff1b107aeea24"}]}),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )

    res = mqtt_connection.publish(
        topic=TOPICRELAYS,
        payload=json.dumps({
            "channel_1": {
                "name": "Geyser",
                "state": True,
                "smart": True
                },
            "channel_2": {
                "name": "Channel 2",
                "state": False,
                "smart": False
                },
            "channel_3": {
                "name": "Channel 3",
                "state": False,
                "smart": False
                },
            "channel_4": {
                "name": "Channel 4",
                "state": False,
                "smart": False
                }, 
            "timeStr": datetime.now().isoformat(),
            "dataTimestamp": datetime.now().isoformat()}),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )

    res = mqtt_connection.publish(
        topic=TOPICUSAGE,
        payload=json.dumps({
            "channel_1": {
                "name": "Geyser",
                "load": apply_deviation(2500, 0.05)
                },
            "channel_2": {
                "name": "Channel 2",
                "load": apply_deviation(100, 0.05)
                },
            "channel_3": {
                "name": "Channel 3",
                "load": 0
                },
            "channel_4": {
                "name": "Channel 4",
                "load": 0
                }, 
            "timeStr": datetime.now().isoformat(),
            "dataTimestamp": datetime.now().isoformat()}),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )

    res = mqtt_connection.publish(
        topic=TOPICRISKS,
        payload=json.dumps({
            "risk": {
                "unplannedOutage": apply_deviation(500, 0.1),
                "plannedOutage": apply_deviation(100, 0.05),
                "disconnection": apply_deviation(10, 0.1)
                }, 
            "timeStr": datetime.now().isoformat(),
            "dataTimestamp": datetime.now().isoformat()}),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )

    res = mqtt_connection.publish(
        topic=TOPICALERTS,
        payload=json.dumps({
            "alert_1": 0,
            "alert_2": 0,
            "alert_3": 0,
            "alert_4": 0,
            "alert_5": 0,
            "alert_6": "Learning | Device distinction error",
            "alert_7": 0,
            "alert_8": 0, 
            "timeStr": datetime.now().isoformat(),
            "dataTimestamp": datetime.now().isoformat()}),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )
      
    # Needs to wait for future to be complete
    while not res[0].done():
        time.sleep(0.1)  
    
def get_inverter_data():
    req = Request(f"{URL_BASE}/solarman/device/sn/{SERIAL_NUMBER}")
    req.add_header("Authorization", f"Bearer {TOKEN}")
    req.add_header("x-api-key", KEY)
    content = urlopen(req).read()

    raw_data = content.decode("utf-8")

    raw_dict = json.loads(raw_data)

    print(json.dumps(raw_dict, indent=2))

    # data = json.loads(content.decode("utf-8")).get("response", {}).get("data")

    # response = {"datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    # variables = [
    #     "eToday", "fac", "pac", "pacPec", "iPv1", "iPv2", "iPv3", "iPv4",
    #     "iPv5", "iPv6", "iPv7", "iPv8", "uPv1", "uPv2", "uPv3", "uPv4",
    #     "uPv5", "uPv6", "uPv7", "uPv8", "iAc1", "iAc2", "iAc3", "uAc1",
    #     "uAc2", "uAc3", "inverterTemperature", "batteryLaTemp", "batteryVoltage",
    #     "bstteryCurrent", "batteryCapacitySoc", "batteryTodayChargeEnergy",
    #     "batteryTodayDischargeEnergy", "gridPurchasedTodayEnergy", "familyLoadPower",
    #     "bypassLoadPower", "psum", "homeLoadTodayEnergy", "storageBatteryVoltage",
    #     "storageBatteryCurrent"
    # ]

    # for v in variables:
    #     response[v] = data.get(v)

    # print(json.dumps(response, indent=2))
    # if response.get("storageBatteryVoltage") and response.get("storageBatteryCurrent"):
    #     efficiency = (
    #         (response["storageBatteryVoltage"] * response["storageBatteryCurrent"]
    #         - response["batteryVoltage"] * response.get("bstteryCurrent", 0))
    #         / (response["storageBatteryVoltage"] * response["storageBatteryCurrent"])
    #     )
    #     print(efficiency)

    # return response



def apply_deviation(load, deviation_percent):
    deviation_factor = random.uniform(1 - deviation_percent, 1 + deviation_percent)
    adjusted_load = round(load * deviation_factor)  # Round off the adjusted load
    return adjusted_load / 1000  # Convert to kilowatts (kW)

MQTT_BROKER_ENDPOINT = "a1xz7n0flroqhn-ats.iot.eu-west-1.amazonaws.com"

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
MIIEowIBAAKCAQEAqEAdhltg+h2VlkyJh2c6lWl5b8ODIO6Q/eeM7J+bFsvbdJM1
fP5VVIXDsOTaUDI88nYJh1JoxNt6YW7tQrUTi4Gs5KKcLwQf64V6sha59QGigkM/
aB2HU+zBAfJG3rjE3S5EF0OvlXUFhV9oqzbGgpgB674nAxLzbWJDNG4ViyLmmR8r
2RerTYdCGjO4lM2nyBWDaINeuvrwD/4W5vrJijBt0zpviEzeXKlPFCP1Fh3WR/Mn
qbGWQ+6DWdWjCimRqMmw28hS4mgVLg4C72Tt1luUKcmR3+Lcgv2tuRa0+UenxSJm
aWi4cNDVfeyFQ8Q2Noistc5w9MTGJY+76Jq7oQIDAQABAoIBAFfdS83rkKRtqL3Z
8IR+u1BlyZ49OxCKpbuDHcxAuaxY/51Md0V0SLmgNYb+rKfu5Hc2f1llBwOvHqUd
WdhZWgCj0td/uBKxk73aci3owmoZ1XUzizxjF1YTsOPEU5Bia6SaUcLYfSyO9Tgm
kDHBpD91BKPJJPRtBCUeiLwrtSJ4WWpxpaF7fdbZK/36uUU/n9eEQnIo39qirXE3
JIXkOXbXqEjyxqprZhc8Y7JAUZ061TnPWS4GsXO0pNa2ItQP0+4+h96KJzF8m1mu
gnJo8q8fNwU+p1wGKpFWB59zN5iT2Z7GukrUkaBPID4inJ2/pVLa1OmTTv6CRcme
6bKutbECgYEA2mLf+BPEb8O/LXGJM2qNhfhs2lUkSas3QN39Zf23uHcfKPAdwSCG
Rz8Cj/ZVUrzhqYFU/pKUxtCx3ZGMSJRMMSvQQI3lkwBtiKH8Bpmh2qL1tZR85ftF
7Pt5K+bdE/mGj0M7M8M7vFLq5x/iPPu/+pWxF6AXFg2t1HKeeV7/680CgYEAxTql
BKs4JTkcUhcaBXfa+wTv/yTVqUWwyh3Htgb1iOUK6u3gC2TpE4wBoq407jLBSp+V
VZP32yNlRj8LmFzY1i8et7ykAKdrgwm73Gs4C5AxyShEaqXtbC2oLdsHuPsuQ3mP
dydJm2cGDZ+61w4gpgilrZnW+dRq8uWGGa2DQyUCgYAYuNa346z6JgOvZkns2yQY
RW41LSxFdq9zlW3JLPauWDXb0YrcwQzSZeypVW6FRkKZiL2RcBCNjTSFa6Og18Dk
VBxoImgZwxOjQwsfyCaNdKMyIhQdiNt6n2ExOhpO15GHCEpcar6JbC2RaoeW9bze
5jE9Bm92nKfQBAWyobGBBQKBgCM12QgAWUGr9HZjUW3we9OcigwO02Yo3ur2bhT9
IRCTc2OFnB3sof+vWwtj9mcgAIoF+28Pv4wLwaTM1JEa4ks6lk1PDChhuzvlnPg4
3ASUdY7n9W7kuII7lG67T6GilhvNs+MdzHJF7jq4bW6/QuzhVlKryElJtt4uQ8aJ
x4lRAoGBAJQiv1iFQgxmeqNkWNifsmeXBCcN/+SggcTCXcsFcIFudG26PDsExwcO
lrUfqsNR6D5i9/NhGp0y6MsTUaIgBv9vHOeUcB2QgqhBMgiNbDjMXPiz9Ozeupi2
T1LZSwV+EZ+1QF1C170iSwGMYLSnjvwkHrBa4HuLNVkxnBvbL8kO
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


CLIENT_ID = "brain-learning"

try:
    run_kobus()
except Exception as e:
    print(str(e))
time.sleep(5)
try:
    run_rushil()
except Exception as e:
    print(str(e))
time.sleep(5)
try:
    run_andre()
except Exception as e:
    print(str(e))
time.sleep(5)
try:
    run_craig()
except Exception as e:
    print(str(e))
time.sleep(5)
try:
    run_craig()
except Exception as e:
    print(str(e))
time.sleep(5)
try:
    run_device("866069069856407")
    run_device("866069069798088")
    run_device("866069069792180")
except Exception as e:
    print(str(e))
try:
    multiplug("1200250000000001938475")
    #multiplug("1200250000000001945852")
    #multiplug("1200250000000001947589")
except Exception as e:
    print(str(e))
try:
    lightswitch("152430000201")
except Exception as e:
    print(str(e))
# Pause for 2 minutes (120 seconds)
#time.sleep(105)


# Disconnect
# disconnect_future = mqtt_connection.disconnect()
# disconnect_future.result()
