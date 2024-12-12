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
        
def run_patrick():
    t = time.gmtime()
    data_timestamp = "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}Z".format(
        t[0], t[1], t[2], t[3], t[4], t[5]
    )
    
    print(str(data_timestamp) + ": Patrick Narbel")
    
    TOPICDATA = "GOSOLR/BRAIN/864454073547659/DATA"
    TOPICRELAYCONTROL = "GOSOLR/BRAIN/RELAYCONTROL/864454073547659"
    
    # Constants for Inverter data retrieval
    TOKEN = "238c59c51665df09c9bc72daaa9c48074003939bac857a109f0b767b9d4e8622"
    KEY = "28c595aa93939bab9d"
    URL_BASE = "https://gsm.gosolr.co.za"
    SERIAL_NUMBER = "1031200237290095"
    
    req = Request(f"{URL_BASE}/solarman/device/sn/{SERIAL_NUMBER}")
    req.add_header("Authorization", f"Bearer {TOKEN}")
    req.add_header("x-api-key", KEY)
    content = urlopen(req).read()

    raw_data = content.decode("utf-8")
    raw_dict = json.loads(raw_data)
    #print(raw_dict)

    # Adjust for nested structure: find the list in the JSON
    if isinstance(raw_dict, dict):  # JSON starts as a dictionary
        for key, value in raw_dict.items():
            if isinstance(value, list):  # Look for the list of objects
                for entry in value:
                    if "key" in entry:  # Check each entry for "key"
                        #print(entry["key"])
                        #print(entry["name"])
                        #print(entry["value"])
                        if entry["key"] == "SN1":
                            inverterID = entry["value"]+"S"
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
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )

    res = mqtt_connection.publish(
    topic=TOPICRELAYCONTROL,
    payload=json.dumps({
        "imei": "864454073547659",
        "relay": "1",
        "controls": [
            {"channel_1": "Geyser 1", "source": "brain", "state": False},
            {"channel_2": "Geyser 2", "source": "brain", "state": False},
            {"channel_3": "Oven", "source": "brain", "state": True},
            {"channel_4": "Pool", "source": "brain", "state": True}
        ],
        "timeStr": data_timestamp,
        "dataTimestamp": data_timestamp
    }),
    qos=mqtt5.QoS.AT_LEAST_ONCE,
    retain=False,
    )
    
    # Needs to wait for future to be complete
    while not res[0].done():
        time.sleep(0.1)

def run_kobus():
    t = time.gmtime()
    data_timestamp = "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}Z".format(
        t[0], t[1], t[2], t[3], t[4], t[5]
    )
    
    print(str(data_timestamp) + ": Kobus Viljoen")
    
    TOPICMODELS = "GOSOLR/BRAIN/864454073547584/MODELS"
    TOPICRELAYS = "GOSOLR/BRAIN/864454073547584/RELAYS"
    TOPICUSAGE = "GOSOLR/BRAIN/864454073547584/USAGE"
    TOPICRISKS = "GOSOLR/BRAIN/864454073547584/RISKS"
    TOPICALERTS = "GOSOLR/BRAIN/864454073547584/ALERTS"
    TOPICDATA = "GOSOLR/BRAIN/864454073547584/DATA"
    TOPICHB = "GOSOLR/BRAIN/864454073547584/HB"
    TOPICSTATUS = "GOSOLR/BRAIN/864454073547584/STATUS"
    TOPICRELAYCONTROL = "GOSOLR/BRAIN/RELAYCONTROL/864454073547584"
    
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
    
    gridPower = 0

    # Adjust for nested structure: find the list in the JSON
    if isinstance(raw_dict, dict):  # JSON starts as a dictionary
        for key, value in raw_dict.items():
            if isinstance(value, list):  # Look for the list of objects
                for entry in value:
                    if "key" in entry:  # Check each entry for "key"
                        #print(entry["key"])
                        #print(entry["name"])
                        #print(entry["value"])
                        #print(entry["unit"])
                        #print()
                        if entry["name"] == "Grid Frequency":
                            fac = entry["value"]
                        if entry["name"] == "SN":
                            inverterID = entry["value"]+"D"
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
                        if entry["key"] == "PG_Pt1": #E_CT_P
                            gridTiePower = entry["value"] 
                        if entry["key"] == "CT_T_E": #E_CT_P
                            gridPower = gridPower + float(entry["value"])
                        #if entry["key"] == "G_P_L2": #E_CT_P
                        #    gridPower = gridPower + float(entry["value"])
                        #if entry["key"] == "G_P_L3": #E_CT_P
                        #    gridPower = gridPower + float(entry["value"])
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
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
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
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )
    
    res = mqtt_connection.publish(
    topic=TOPICRELAYCONTROL,
    payload=json.dumps({
        "imei": "864454073547584",
        "relay": "1",
        "controls": [
            {"channel_1": "Channel 1", "source": "brain", "state": True},
            {"channel_2": "Channel 2", "source": "brain", "state": True}
        ],
        "timeStr": data_timestamp,
        "dataTimestamp": data_timestamp
    }),
    qos=mqtt5.QoS.AT_LEAST_ONCE,
    retain=False,
    )

    res = mqtt_connection.publish(
        topic=TOPICUSAGE,
        payload=json.dumps({
            "channel_1": {
                "name": "Geyser 1",
                "state": True,
                "load": apply_deviation(2100, 0.07)
                },
            "channel_2": {
                "name": "Geyser 2",
                "state": True,
                "load": apply_deviation(2500, 0.05)
                },
            "channel_3": {
                "name": "disconnected",
                "state": False,
                "load": 0
                },
            "channel_4": {
                "name": "disconnected",
                "state": False,
                "load": 0
                }, 
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
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
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
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
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
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
            "gridSoldTodayEnergy":gridSoldTodayEnergy,
            "familyLoadPower":familyLoadPower,
            "bypassLoadPower":bypassLoadPower,
            "pSUM":pSUM,
            "homeLoadTodayEnergy":homeLoadTodayEnergy, 
            "gridTiePower":gridTiePower, 
            "gridPower":str(gridPower),
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )
    
    # Needs to wait for future to be complete
    while not res[0].done():
        time.sleep(0.1)
        
def run_andrew():
    t = time.gmtime()
    data_timestamp = "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}Z".format(
        t[0], t[1], t[2], t[3], t[4], t[5]
    )
    
    print(str(data_timestamp) + ": Andrew Middleton")
    
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
                        #print(entry["name"])
                        #print(entry["unit"])
                        #print()
                        if entry["name"] == "Grid Frequency":
                            fac = entry["value"]
                        if entry["name"] == "SN":
                            inverterID = entry["value"]+"D"
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
                        if entry["key"] == "G_T_P": #E_CT_P
                            gridTiePower = entry["value"]    
                        if entry["key"] == "PG_Pt1": #E_CT_P
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
            "gridSoldTodayEnergy":0,
            "familyLoadPower":familyLoadPower,
            "bypassLoadPower":bypassLoadPower,
            "pSUM":pSUM,
            "homeLoadTodayEnergy":homeLoadTodayEnergy, 
            "gridTiePower":gridTiePower, 
            "gridPower":gridPower,
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )
    
    # Needs to wait for future to be complete
    while not res[0].done():
        time.sleep(0.1)

def run_neil():
    t = time.gmtime()
    data_timestamp = "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}Z".format(
        t[0], t[1], t[2], t[3], t[4], t[5]
    )
    
    print(str(data_timestamp) + ": Neil McWilliams")
    
    TOPICDATA = "GOSOLR/BRAIN/864454073547717/DATA"
    
    # Constants for Inverter data retrieval
    TOKEN = "238c59c51665df09c9bc72daaa9c48074003939bac857a109f0b767b9d4e8622"
    KEY = "28c595aa93939bab9d"
    URL_BASE = "https://gsm.gosolr.co.za"
    SERIAL_NUMBER = "2212032251"
    
    req = Request(f"{URL_BASE}/solarman/device/sn/{SERIAL_NUMBER}")
    req.add_header("Authorization", f"Bearer {TOKEN}")
    req.add_header("x-api-key", KEY)
    content = urlopen(req).read()

    raw_data = content.decode("utf-8")
    raw_dict = json.loads(raw_data)
    #print(raw_dict)

    # Adjust for nested structure: find the list in the JSON
    if isinstance(raw_dict, dict):  # JSON starts as a dictionary
        for key, value in raw_dict.items():
            if isinstance(value, list):  # Look for the list of objects
                for entry in value:
                    if "key" in entry:  # Check each entry for "key"
                        #print(entry["key"])
                        #print(entry["value"])
                        #print(entry["name"])
                        #print()
                        if entry["name"] == "Grid Frequency":
                            fac = entry["value"]
                        if entry["name"] == "SN":
                            inverterID = entry["value"]+"D"
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
                        if entry["key"] == "G_T_P": #E_CT_P
                            gridTiePower = entry["value"]    
                        if entry["key"] == "PG_Pt1": #E_CT_P
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
            "gridSoldTodayEnergy":0,
            "familyLoadPower":familyLoadPower,
            "bypassLoadPower":bypassLoadPower,
            "pSUM":pSUM,
            "homeLoadTodayEnergy":homeLoadTodayEnergy, 
            "gridTiePower":gridTiePower, 
            "gridPower":gridPower,
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )
    
    # Needs to wait for future to be complete
    while not res[0].done():
        time.sleep(0.1)

def run_wayne():
    t = time.gmtime()
    data_timestamp = "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}Z".format(
        t[0], t[1], t[2], t[3], t[4], t[5]
    )
    
    print(str(data_timestamp) + ": Wayne Bester")
    
    TOPICDATA = "GOSOLR/BRAIN/868373070932100/DATA"
    
    # Constants for Inverter data retrieval
    TOKEN = "238c59c51665df09c9bc72daaa9c48074003939bac857a109f0b767b9d4e8622"
    KEY = "28c595aa93939bab9d"
    URL_BASE = "https://gsm.gosolr.co.za"
    SERIAL_NUMBER = "2206178211"
    
    req = Request(f"{URL_BASE}/solarman/device/sn/{SERIAL_NUMBER}")
    req.add_header("Authorization", f"Bearer {TOKEN}")
    req.add_header("x-api-key", KEY)
    content = urlopen(req).read()

    raw_data = content.decode("utf-8")
    raw_dict = json.loads(raw_data)
    #print(raw_dict)

    # Adjust for nested structure: find the list in the JSON
    if isinstance(raw_dict, dict):  # JSON starts as a dictionary
        for key, value in raw_dict.items():
            if isinstance(value, list):  # Look for the list of objects
                for entry in value:
                    if "key" in entry:  # Check each entry for "key"
                        #print(entry["key"])
                        #print(entry["value"])
                        #print(entry["name"])
                        #print()
                        if entry["name"] == "Grid Frequency":
                            fac = entry["value"]
                        if entry["name"] == "SN":
                            inverterID = entry["value"]+"D"
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
                        if entry["key"] == "G_T_P": #E_CT_P
                            gridTiePower = entry["value"]    
                        if entry["key"] == "PG_Pt1": #E_CT_P
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
            "gridSoldTodayEnergy":0,
            "familyLoadPower":familyLoadPower,
            "bypassLoadPower":bypassLoadPower,
            "pSUM":pSUM,
            "homeLoadTodayEnergy":homeLoadTodayEnergy, 
            "gridTiePower":gridTiePower, 
            "gridPower":gridPower,
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )
    
    # Needs to wait for future to be complete
    while not res[0].done():
        time.sleep(0.1)

def run_shaun():
    t = time.gmtime()
    data_timestamp = "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}Z".format(
        t[0], t[1], t[2], t[3], t[4], t[5]
    )
    
    print(str(data_timestamp) + ": Shaun May")
    
    TOPICDATA = "GOSOLR/BRAIN/868373070932266/DATA"
    
    # Constants for Inverter data retrieval
    TOKEN = "238c59c51665df09c9bc72daaa9c48074003939bac857a109f0b767b9d4e8622"
    KEY = "28c595aa93939bab9d"
    URL_BASE = "https://gsm.gosolr.co.za"
    SERIAL_NUMBER = "2207282514"
    
    req = Request(f"{URL_BASE}/solarman/device/sn/{SERIAL_NUMBER}")
    req.add_header("Authorization", f"Bearer {TOKEN}")
    req.add_header("x-api-key", KEY)
    content = urlopen(req).read()

    raw_data = content.decode("utf-8")
    raw_dict = json.loads(raw_data)
    #print(raw_dict)

    # Adjust for nested structure: find the list in the JSON
    if isinstance(raw_dict, dict):  # JSON starts as a dictionary
        for key, value in raw_dict.items():
            if isinstance(value, list):  # Look for the list of objects
                for entry in value:
                    if "key" in entry:  # Check each entry for "key"
                        #print(entry["key"])
                        #print(entry["value"])
                        #print(entry["name"])
                        #print()
                        if entry["name"] == "Grid Frequency":
                            fac = entry["value"]
                        if entry["name"] == "SN":
                            inverterID = entry["value"]+"D"
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
                        if entry["key"] == "G_T_P": #E_CT_P
                            gridTiePower = entry["value"]    
                        if entry["key"] == "PG_Pt1": #E_CT_P
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
            "gridSoldTodayEnergy":0,
            "familyLoadPower":familyLoadPower,
            "bypassLoadPower":bypassLoadPower,
            "pSUM":pSUM,
            "homeLoadTodayEnergy":homeLoadTodayEnergy, 
            "gridTiePower":gridTiePower, 
            "gridPower":gridPower,
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )
    
    # Needs to wait for future to be complete
    while not res[0].done():
        time.sleep(0.1)


def run_vick():
    t = time.gmtime()
    data_timestamp = "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}Z".format(
        t[0], t[1], t[2], t[3], t[4], t[5]
    )
    
    print(str(data_timestamp) + ": Vick Schoeman")
    
    TOPICDATA = "GOSOLR/BRAIN/866069069791224/DATA"
    
    # Constants for Inverter data retrieval
    TOKEN = "238c59c51665df09c9bc72daaa9c48074003939bac857a109f0b767b9d4e8622"
    KEY = "28c595aa93939bab9d"
    URL_BASE = "https://gsm.gosolr.co.za"
    SERIAL_NUMBER = "2302078519"
    
    req = Request(f"{URL_BASE}/solarman/device/sn/{SERIAL_NUMBER}")
    req.add_header("Authorization", f"Bearer {TOKEN}")
    req.add_header("x-api-key", KEY)
    content = urlopen(req).read()

    raw_data = content.decode("utf-8")
    raw_dict = json.loads(raw_data)
    #print(raw_dict)

    # Adjust for nested structure: find the list in the JSON
    if isinstance(raw_dict, dict):  # JSON starts as a dictionary
        for key, value in raw_dict.items():
            if isinstance(value, list):  # Look for the list of objects
                for entry in value:
                    if "key" in entry:  # Check each entry for "key"
                        #print(entry["key"])
                        #print(entry["value"])
                        #print(entry["name"])
                        #print()
                        if entry["name"] == "Grid Frequency":
                            fac = entry["value"]
                        if entry["name"] == "SN":
                            inverterID = entry["value"]+"D"
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
                        if entry["key"] == "G_T_P": #E_CT_P
                            gridTiePower = entry["value"]    
                        if entry["key"] == "PG_Pt1": #E_CT_P
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
            "gridSoldTodayEnergy":0,
            "familyLoadPower":familyLoadPower,
            "bypassLoadPower":bypassLoadPower,
            "pSUM":pSUM,
            "homeLoadTodayEnergy":homeLoadTodayEnergy, 
            "gridTiePower":gridTiePower, 
            "gridPower":gridPower,
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )
    
    # Needs to wait for future to be complete
    while not res[0].done():
        time.sleep(0.1)

def run_claire():
    t = time.gmtime()
    data_timestamp = "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}Z".format(
        t[0], t[1], t[2], t[3], t[4], t[5]
    )
    
    print(str(data_timestamp) + ": Claire Dicey")
    
    TOPICDATA = "GOSOLR/BRAIN/868373070932571/DATA"
    
    # Constants for Inverter data retrieval
    TOKEN = "238c59c51665df09c9bc72daaa9c48074003939bac857a109f0b767b9d4e8622"
    KEY = "28c595aa93939bab9d"
    URL_BASE = "https://gsm.gosolr.co.za"
    SERIAL_NUMBER = "2306044729"
    
    req = Request(f"{URL_BASE}/solarman/device/sn/{SERIAL_NUMBER}")
    req.add_header("Authorization", f"Bearer {TOKEN}")
    req.add_header("x-api-key", KEY)
    content = urlopen(req).read()

    raw_data = content.decode("utf-8")
    raw_dict = json.loads(raw_data)
    #print(raw_dict)

    # Adjust for nested structure: find the list in the JSON
    if isinstance(raw_dict, dict):  # JSON starts as a dictionary
        for key, value in raw_dict.items():
            if isinstance(value, list):  # Look for the list of objects
                for entry in value:
                    if "key" in entry:  # Check each entry for "key"
                        #print(entry["key"])
                        #print(entry["value"])
                        #print(entry["name"])
                        #print()
                        if entry["name"] == "Grid Frequency":
                            fac = entry["value"]
                        if entry["name"] == "SN":
                            inverterID = entry["value"]+"D"
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
                        if entry["key"] == "G_T_P": #E_CT_P
                            gridTiePower = entry["value"]    
                        if entry["key"] == "PG_Pt1": #E_CT_P
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
            "gridSoldTodayEnergy":0,
            "familyLoadPower":familyLoadPower,
            "bypassLoadPower":bypassLoadPower,
            "pSUM":pSUM,
            "homeLoadTodayEnergy":homeLoadTodayEnergy, 
            "gridTiePower":gridTiePower, 
            "gridPower":gridPower,
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )
    
    # Needs to wait for future to be complete
    while not res[0].done():
        time.sleep(0.1)

def run_ignatius():
    t = time.gmtime()
    data_timestamp = "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}Z".format(
        t[0], t[1], t[2], t[3], t[4], t[5]
    )
    
    print(str(data_timestamp) + ": Ignatius Dreyer")
    
    TOPICDATA = "GOSOLR/BRAIN/868373070932381/DATA"
    
    # Constants for Inverter data retrieval
    TOKEN = "238c59c51665df09c9bc72daaa9c48074003939bac857a109f0b767b9d4e8622"
    KEY = "28c595aa93939bab9d"
    URL_BASE = "https://gsm.gosolr.co.za"
    SERIAL_NUMBER = "2304068729"
    
    req = Request(f"{URL_BASE}/solarman/device/sn/{SERIAL_NUMBER}")
    req.add_header("Authorization", f"Bearer {TOKEN}")
    req.add_header("x-api-key", KEY)
    content = urlopen(req).read()

    raw_data = content.decode("utf-8")
    raw_dict = json.loads(raw_data)
    #print(raw_dict)

    # Adjust for nested structure: find the list in the JSON
    if isinstance(raw_dict, dict):  # JSON starts as a dictionary
        for key, value in raw_dict.items():
            if isinstance(value, list):  # Look for the list of objects
                for entry in value:
                    if "key" in entry:  # Check each entry for "key"
                        #print(entry["key"])
                        #print(entry["value"])
                        #print(entry["name"])
                        #print()
                        if entry["name"] == "Grid Frequency":
                            fac = entry["value"]
                        if entry["name"] == "SN":
                            inverterID = entry["value"]+"D"
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
                        if entry["key"] == "G_T_P": #E_CT_P
                            gridTiePower = entry["value"]    
                        if entry["key"] == "PG_Pt1": #E_CT_P
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
            "gridSoldTodayEnergy":0,
            "familyLoadPower":familyLoadPower,
            "bypassLoadPower":bypassLoadPower,
            "pSUM":pSUM,
            "homeLoadTodayEnergy":homeLoadTodayEnergy, 
            "gridTiePower":gridTiePower, 
            "gridPower":gridPower,
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )
    
    # Needs to wait for future to be complete
    while not res[0].done():
        time.sleep(0.1)


def run_fazeka():
    t = time.gmtime()
    data_timestamp = "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}Z".format(
        t[0], t[1], t[2], t[3], t[4], t[5]
    )
    
    print(str(data_timestamp) + ": Fazeka Nompuza")
    
    TOPICDATA = "GOSOLR/BRAIN/868373070933611/DATA"
    
    # Constants for Inverter data retrieval
    TOKEN = "238c59c51665df09c9bc72daaa9c48074003939bac857a109f0b767b9d4e8622"
    KEY = "28c595aa93939bab9d"
    URL_BASE = "https://gsm.gosolr.co.za"
    SERIAL_NUMBER = "2211238459"
    
    req = Request(f"{URL_BASE}/solarman/device/sn/{SERIAL_NUMBER}")
    req.add_header("Authorization", f"Bearer {TOKEN}")
    req.add_header("x-api-key", KEY)
    content = urlopen(req).read()

    raw_data = content.decode("utf-8")
    raw_dict = json.loads(raw_data)
    #print(raw_dict)

    # Adjust for nested structure: find the list in the JSON
    if isinstance(raw_dict, dict):  # JSON starts as a dictionary
        for key, value in raw_dict.items():
            if isinstance(value, list):  # Look for the list of objects
                for entry in value:
                    if "key" in entry:  # Check each entry for "key"
                        #print(entry["key"])
                        #print(entry["value"])
                        #print(entry["name"])
                        #print()
                        if entry["name"] == "Grid Frequency":
                            fac = entry["value"]
                        if entry["name"] == "SN":
                            inverterID = entry["value"]+"D"
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
                        if entry["key"] == "G_T_P": #E_CT_P
                            gridTiePower = entry["value"]    
                        if entry["key"] == "PG_Pt1": #E_CT_P
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
            "gridSoldTodayEnergy":0,
            "familyLoadPower":familyLoadPower,
            "bypassLoadPower":bypassLoadPower,
            "pSUM":pSUM,
            "homeLoadTodayEnergy":homeLoadTodayEnergy, 
            "gridTiePower":gridTiePower, 
            "gridPower":gridPower,
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )
    
    # Needs to wait for future to be complete
    while not res[0].done():
        time.sleep(0.1)


def run_gideon():
    t = time.gmtime()
    data_timestamp = "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}Z".format(
        t[0], t[1], t[2], t[3], t[4], t[5]
    )
    
    print(str(data_timestamp) + ": Gideon van Zyl")
    
    TOPICDATA = "GOSOLR/BRAIN/868373070932522/DATA"
    
    # Constants for Inverter data retrieval
    TOKEN = "238c59c51665df09c9bc72daaa9c48074003939bac857a109f0b767b9d4e8622"
    KEY = "28c595aa93939bab9d"
    URL_BASE = "https://gsm.gosolr.co.za"
    SERIAL_NUMBER = "2306090282"
    
    req = Request(f"{URL_BASE}/solarman/device/sn/{SERIAL_NUMBER}")
    req.add_header("Authorization", f"Bearer {TOKEN}")
    req.add_header("x-api-key", KEY)
    content = urlopen(req).read()

    raw_data = content.decode("utf-8")
    raw_dict = json.loads(raw_data)
    #print(raw_dict)

    # Adjust for nested structure: find the list in the JSON
    if isinstance(raw_dict, dict):  # JSON starts as a dictionary
        for key, value in raw_dict.items():
            if isinstance(value, list):  # Look for the list of objects
                for entry in value:
                    if "key" in entry:  # Check each entry for "key"
                        #print(entry["key"])
                        #print(entry["value"])
                        #print(entry["name"])
                        #print()
                        if entry["name"] == "Grid Frequency":
                            fac = entry["value"]
                        if entry["name"] == "SN":
                            inverterID = entry["value"]+"D"
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
                        if entry["key"] == "G_T_P": #E_CT_P
                            gridTiePower = entry["value"]    
                        if entry["key"] == "PG_Pt1": #E_CT_P
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
            "gridSoldTodayEnergy":0,
            "familyLoadPower":familyLoadPower,
            "bypassLoadPower":bypassLoadPower,
            "pSUM":pSUM,
            "homeLoadTodayEnergy":homeLoadTodayEnergy, 
            "gridTiePower":gridTiePower, 
            "gridPower":gridPower,
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )
    
    # Needs to wait for future to be complete
    while not res[0].done():
        time.sleep(0.1)


def run_ummar():
    t = time.gmtime()
    data_timestamp = "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}Z".format(
        t[0], t[1], t[2], t[3], t[4], t[5]
    )
    
    print(str(data_timestamp) + ": Ummar Williams")
    
    TOPICDATA = "GOSOLR/BRAIN/868373070932811/DATA"
    TOPICMODELS = "GOSOLR/BRAIN/868373070932811/MODELS"
    TOPICRELAYS = "GOSOLR/BRAIN/868373070932811/RELAYS"
    TOPICUSAGE = "GOSOLR/BRAIN/868373070932811/USAGE"
    TOPICRISKS = "GOSOLR/BRAIN/868373070932811/RISKS"
    TOPICALERTS = "GOSOLR/BRAIN/868373070932811/ALERTS"
    TOPICHB = "GOSOLR/BRAIN/868373070932811/HB"
    TOPICSTATUS = "GOSOLR/BRAIN/868373070932811/STATUS"
    TOPICRELAYCONTROL = "GOSOLR/BRAIN/RELAYCONTROL/868373070932811"
    
    # Constants for Inverter data retrieval
    TOKEN = "238c59c51665df09c9bc72daaa9c48074003939bac857a109f0b767b9d4e8622"
    KEY = "28c595aa93939bab9d"
    URL_BASE = "https://gsm.gosolr.co.za"
    SERIAL_NUMBER = "2208266617"
    
    req = Request(f"{URL_BASE}/solarman/device/sn/{SERIAL_NUMBER}")
    req.add_header("Authorization", f"Bearer {TOKEN}")
    req.add_header("x-api-key", KEY)
    content = urlopen(req).read()

    raw_data = content.decode("utf-8")
    raw_dict = json.loads(raw_data)
    #print(raw_dict)

    # Adjust for nested structure: find the list in the JSON
    if isinstance(raw_dict, dict):  # JSON starts as a dictionary
        for key, value in raw_dict.items():
            if isinstance(value, list):  # Look for the list of objects
                for entry in value:
                    if "key" in entry:  # Check each entry for "key"
                        #print(entry["key"])
                        #print(entry["value"])
                        #print(entry["name"])
                        #print()
                        if entry["name"] == "Grid Frequency":
                            fac = entry["value"]
                        if entry["name"] == "SN":
                            inverterID = entry["value"]+"D"
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
                        if entry["key"] == "G_T_P": #E_CT_P
                            gridTiePower = entry["value"]    
                        if entry["key"] == "PG_Pt1": #E_CT_P
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
            "gridSoldTodayEnergy":0,
            "familyLoadPower":familyLoadPower,
            "bypassLoadPower":bypassLoadPower,
            "pSUM":pSUM,
            "homeLoadTodayEnergy":homeLoadTodayEnergy, 
            "gridTiePower":gridTiePower, 
            "gridPower":gridPower,
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )

    res = mqtt_connection.publish(
        topic=TOPICMODELS,
        payload=json.dumps({
            "edge": "1.3.0",
            "parsec": "1.4.1(a)",
            "east": "1.0.4",
            "gosolr": "2.1.0",
            "manager": "0.1.4", 
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
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
                "name": "disconnected",
                "state": False,
                "smart": False
                },
            "channel_2": {
                "name": "Geyser",
                "state": False,
                "smart": False
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
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )
    
    res = mqtt_connection.publish(
    topic=TOPICRELAYCONTROL,
    payload=json.dumps({
        "imei": "868373070932811",
        "relay": "1",
        "controls": [
            {"channel_2": "Geyser", "source": "brain", "state": False}
        ],
        "timeStr": data_timestamp,
        "dataTimestamp": data_timestamp
    }),
    qos=mqtt5.QoS.AT_LEAST_ONCE,
    retain=False,
    )

    res = mqtt_connection.publish(
        topic=TOPICUSAGE,
        payload=json.dumps({
            "channel_1": {
                "name": "disconnected",
                "state": False,
                "load": 0
                },
            "channel_2": {
                "name": "Geyser",
                "state": False,
                "load": apply_deviation(2500, 0.05)
                },
            "channel_3": {
                "name": "disconnected",
                "state": False,
                "load": 0
                },
            "channel_4": {
                "name": "disconnected",
                "state": False,
                "load": 0
                }, 
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
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
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
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
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )
    
    # Needs to wait for future to be complete
    while not res[0].done():
        time.sleep(0.1)

def run_ryan():
    t = time.gmtime()
    data_timestamp = "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}Z".format(
        t[0], t[1], t[2], t[3], t[4], t[5]
    )
    
    print(str(data_timestamp) + ": Martin Janse van Rensburg")
    
    TOPICDATA = "GOSOLR/BRAIN/866069069789103/DATA"
    TOPICMODELS = "GOSOLR/BRAIN/866069069789103/MODELS"
    TOPICRELAYS = "GOSOLR/BRAIN/866069069789103/RELAYS"
    TOPICUSAGE = "GOSOLR/BRAIN/866069069789103/USAGE"
    TOPICRISKS = "GOSOLR/BRAIN/866069069789103/RISKS"
    TOPICALERTS = "GOSOLR/BRAIN/866069069789103/ALERTS"
    TOPICHB = "GOSOLR/BRAIN/866069069789103/HB"
    TOPICSTATUS = "GOSOLR/BRAIN/866069069789103/STATUS"
    TOPICRELAYCONTROL = "GOSOLR/BRAIN/RELAYCONTROL/866069069789103"
    
    # Constants for Inverter data retrieval
    TOKEN = "238c59c51665df09c9bc72daaa9c48074003939bac857a109f0b767b9d4e8622"
    KEY = "28c595aa93939bab9d"
    URL_BASE = "https://gsm.gosolr.co.za"
    SERIAL_NUMBER = "2107057250"
    
    req = Request(f"{URL_BASE}/solarman/device/sn/{SERIAL_NUMBER}")
    req.add_header("Authorization", f"Bearer {TOKEN}")
    req.add_header("x-api-key", KEY)
    content = urlopen(req).read()

    raw_data = content.decode("utf-8")
    raw_dict = json.loads(raw_data)
    #print(raw_dict)

    # Adjust for nested structure: find the list in the JSON
    if isinstance(raw_dict, dict):  # JSON starts as a dictionary
        for key, value in raw_dict.items():
            if isinstance(value, list):  # Look for the list of objects
                for entry in value:
                    if "key" in entry:  # Check each entry for "key"
                        #print(entry["key"])
                        #print(entry["value"])
                        #print(entry["name"])
                        #print()
                        if entry["name"] == "Grid Frequency":
                            fac = entry["value"]
                        if entry["name"] == "SN":
                            inverterID = entry["value"]+"D"
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
                        if entry["key"] == "G_T_P": #E_CT_P
                            gridTiePower = entry["value"]    
                        if entry["key"] == "PG_Pt1": #E_CT_P
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
            "gridSoldTodayEnergy":0,
            "familyLoadPower":familyLoadPower,
            "bypassLoadPower":bypassLoadPower,
            "pSUM":pSUM,
            "homeLoadTodayEnergy":homeLoadTodayEnergy, 
            "gridTiePower":gridTiePower, 
            "gridPower":gridPower,
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )

    res = mqtt_connection.publish(
        topic=TOPICMODELS,
        payload=json.dumps({
            "edge": "1.3.0",
            "parsec": "1.4.1(a)",
            "east": "1.0.4",
            "gosolr": "2.1.0",
            "manager": "0.1.4", 
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
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
                "state": False,
                "smart": False
                },
            "channel_2": {
                "name": "disconnected",
                "state": False,
                "smart": False
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
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )
    
    res = mqtt_connection.publish(
    topic=TOPICRELAYCONTROL,
    payload=json.dumps({
        "imei": "866069069789103",
        "relay": "1",
        "controls": [
            {"channel_1": "Geyser", "source": "brain", "state": False}
        ],
        "timeStr": data_timestamp,
        "dataTimestamp": data_timestamp
    }),
    qos=mqtt5.QoS.AT_LEAST_ONCE,
    retain=False,
    )

    res = mqtt_connection.publish(
        topic=TOPICUSAGE,
        payload=json.dumps({
            "channel_1": {
                "name": "Geyser",
                "state": False,
                "load": apply_deviation(2500, 0.05)
                },
            "channel_2": {
                "name": "disconnected",
                "state": False,
                "load": 0
                },
            "channel_3": {
                "name": "disconnected",
                "state": False,
                "load": 0
                },
            "channel_4": {
                "name": "disconnected",
                "state": False,
                "load": 0
                }, 
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
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
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
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
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )
    
    # Needs to wait for future to be complete
    while not res[0].done():
        time.sleep(0.1)

def run_martin():
    t = time.gmtime()
    data_timestamp = "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}Z".format(
        t[0], t[1], t[2], t[3], t[4], t[5]
    )
    
    print(str(data_timestamp) + ": Martin Janse van Rensburg")
    
    TOPICDATA = "GOSOLR/BRAIN/868373070933413/DATA"
    TOPICMODELS = "GOSOLR/BRAIN/868373070933413/MODELS"
    TOPICRELAYS = "GOSOLR/BRAIN/868373070933413/RELAYS"
    TOPICUSAGE = "GOSOLR/BRAIN/868373070933413/USAGE"
    TOPICRISKS = "GOSOLR/BRAIN/868373070933413/RISKS"
    TOPICALERTS = "GOSOLR/BRAIN/868373070933413/ALERTS"
    TOPICHB = "GOSOLR/BRAIN/868373070933413/HB"
    TOPICSTATUS = "GOSOLR/BRAIN/868373070933413/STATUS"
    TOPICRELAYCONTROL = "GOSOLR/BRAIN/RELAYCONTROL/868373070933413"
    
    # Constants for Inverter data retrieval
    TOKEN = "238c59c51665df09c9bc72daaa9c48074003939bac857a109f0b767b9d4e8622"
    KEY = "28c595aa93939bab9d"
    URL_BASE = "https://gsm.gosolr.co.za"
    SERIAL_NUMBER = "2305066035"
    
    req = Request(f"{URL_BASE}/solarman/device/sn/{SERIAL_NUMBER}")
    req.add_header("Authorization", f"Bearer {TOKEN}")
    req.add_header("x-api-key", KEY)
    content = urlopen(req).read()

    raw_data = content.decode("utf-8")
    raw_dict = json.loads(raw_data)
    #print(raw_dict)

    # Adjust for nested structure: find the list in the JSON
    if isinstance(raw_dict, dict):  # JSON starts as a dictionary
        for key, value in raw_dict.items():
            if isinstance(value, list):  # Look for the list of objects
                for entry in value:
                    if "key" in entry:  # Check each entry for "key"
                        #print(entry["key"])
                        #print(entry["value"])
                        #print(entry["name"])
                        #print()
                        if entry["name"] == "Grid Frequency":
                            fac = entry["value"]
                        if entry["name"] == "SN":
                            inverterID = entry["value"]+"D"
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
                        if entry["key"] == "G_T_P": #E_CT_P
                            gridTiePower = entry["value"]    
                        if entry["key"] == "PG_Pt1": #E_CT_P
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
            "gridSoldTodayEnergy":0,
            "familyLoadPower":familyLoadPower,
            "bypassLoadPower":bypassLoadPower,
            "pSUM":pSUM,
            "homeLoadTodayEnergy":homeLoadTodayEnergy, 
            "gridTiePower":gridTiePower, 
            "gridPower":gridPower,
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )

    res = mqtt_connection.publish(
        topic=TOPICMODELS,
        payload=json.dumps({
            "edge": "1.3.0",
            "parsec": "1.4.1(a)",
            "east": "1.0.4",
            "gosolr": "2.1.0",
            "manager": "0.1.4", 
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
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
                "state": False,
                "smart": False
                },
            "channel_2": {
                "name": "disconnected",
                "state": False,
                "smart": False
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
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )
    
    res = mqtt_connection.publish(
    topic=TOPICRELAYCONTROL,
    payload=json.dumps({
        "imei": "868373070933413",
        "relay": "1",
        "controls": [
            {"channel_1": "Geyser", "source": "brain", "state": False}
        ],
        "timeStr": data_timestamp,
        "dataTimestamp": data_timestamp
    }),
    qos=mqtt5.QoS.AT_LEAST_ONCE,
    retain=False,
    )

    res = mqtt_connection.publish(
        topic=TOPICUSAGE,
        payload=json.dumps({
            "channel_1": {
                "name": "Geyser",
                "state": False,
                "load": apply_deviation(2500, 0.05)
                },
            "channel_2": {
                "name": "disconnected",
                "state": False,
                "load": 0
                },
            "channel_3": {
                "name": "disconnected",
                "state": False,
                "load": 0
                },
            "channel_4": {
                "name": "disconnected",
                "state": False,
                "load": 0
                }, 
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
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
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
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
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )
    
    # Needs to wait for future to be complete
    while not res[0].done():
        time.sleep(0.1)

def run_natalie():
    t = time.gmtime()
    data_timestamp = "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}Z".format(
        t[0], t[1], t[2], t[3], t[4], t[5]
    )
    
    print(str(data_timestamp) + ": Natalie Thom")
    
    TOPICDATA = "GOSOLR/BRAIN/864454073547857/DATA"
    
    # Constants for Inverter data retrieval
    TOKEN = "238c59c51665df09c9bc72daaa9c48074003939bac857a109f0b767b9d4e8622"
    KEY = "28c595aa93939bab9d"
    URL_BASE = "https://gsm.gosolr.co.za"
    SERIAL_NUMBER = "2107199242"
    
    req = Request(f"{URL_BASE}/solarman/device/sn/{SERIAL_NUMBER}")
    req.add_header("Authorization", f"Bearer {TOKEN}")
    req.add_header("x-api-key", KEY)
    content = urlopen(req).read()

    raw_data = content.decode("utf-8")
    raw_dict = json.loads(raw_data)
    #print(raw_dict)

    # Adjust for nested structure: find the list in the JSON
    if isinstance(raw_dict, dict):  # JSON starts as a dictionary
        for key, value in raw_dict.items():
            if isinstance(value, list):  # Look for the list of objects
                for entry in value:
                    if "key" in entry:  # Check each entry for "key"
                        #print(entry["key"])
                        #print(entry["value"])
                        #print(entry["name"])
                        #print()
                        if entry["name"] == "Grid Frequency":
                            fac = entry["value"]
                        if entry["name"] == "SN":
                            inverterID = entry["value"]+"D"
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
                        if entry["key"] == "G_T_P": #E_CT_P
                            gridTiePower = entry["value"]    
                        if entry["key"] == "PG_Pt1": #E_CT_P
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
            "gridSoldTodayEnergy":0,
            "familyLoadPower":familyLoadPower,
            "bypassLoadPower":bypassLoadPower,
            "pSUM":pSUM,
            "homeLoadTodayEnergy":homeLoadTodayEnergy, 
            "gridTiePower":gridTiePower, 
            "gridPower":gridPower,
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )
    
    # Needs to wait for future to be complete
    while not res[0].done():
        time.sleep(0.1)

def run_rushil():
    t = time.gmtime()
    data_timestamp = "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}Z".format(
        t[0], t[1], t[2], t[3], t[4], t[5]
    )
    
    print(str(data_timestamp) + ": Rushil Rattan")
    
    TOPICDATA = "GOSOLR/BRAIN/864454073558102/DATA"
    TOPICMODELS = "GOSOLR/BRAIN/864454073558102/MODELS"
    TOPICRELAYS = "GOSOLR/BRAIN/864454073558102/RELAYS"
    TOPICUSAGE = "GOSOLR/BRAIN/864454073558102/USAGE"
    TOPICRISKS = "GOSOLR/BRAIN/864454073558102/RISKS"
    TOPICALERTS = "GOSOLR/BRAIN/864454073558102/ALERTS"
    TOPICHB = "GOSOLR/BRAIN/864454073558102/HB"
    TOPICSTATUS = "GOSOLR/BRAIN/864454073558102/STATUS"
    TOPICRELAYCONTROL = "GOSOLR/BRAIN/RELAYCONTROL/864454073558102"
    
    # Constants for Inverter data retrieval
    TOKEN = "238c59c51665df09c9bc72daaa9c48074003939bac857a109f0b767b9d4e8622"
    KEY = "28c595aa93939bab9d"
    URL_BASE = "https://gsm.gosolr.co.za"
    SERIAL_NUMBER = "2305102553"
    
    req = Request(f"{URL_BASE}/solarman/device/sn/{SERIAL_NUMBER}")
    req.add_header("Authorization", f"Bearer {TOKEN}")
    req.add_header("x-api-key", KEY)
    content = urlopen(req).read()

    raw_data = content.decode("utf-8")
    raw_dict = json.loads(raw_data)
    #print(raw_dict)

    # Adjust for nested structure: find the list in the JSON
    if isinstance(raw_dict, dict):  # JSON starts as a dictionary
        for key, value in raw_dict.items():
            if isinstance(value, list):  # Look for the list of objects
                for entry in value:
                    if "key" in entry:  # Check each entry for "key"
                        #print(entry["key"])
                        #print(entry["value"])
                        #print(entry["name"])
                        #print()
                        if entry["name"] == "Grid Frequency":
                            fac = entry["value"]
                        if entry["name"] == "SN":
                            inverterID = entry["value"]+"D"
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
                        if entry["key"] == "PG_Pt1": #E_CT_P
                            gridTiePower = entry["value"] 
                        if entry["key"] == "CT_T_E": #E_CT_P
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
            "gridSoldTodayEnergy":gridSoldTodayEnergy,
            "familyLoadPower":familyLoadPower,
            "bypassLoadPower":bypassLoadPower,
            "pSUM":pSUM,
            "homeLoadTodayEnergy":homeLoadTodayEnergy, 
            "gridTiePower":gridTiePower, 
            "gridPower":str(gridPower),
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )
    
    res = mqtt_connection.publish(
        topic=TOPICMODELS,
        payload=json.dumps({
            "edge": "1.3.0",
            "parsec": "1.4.1(a)",
            "east": "1.0.4",
            "gosolr": "2.1.0",
            "manager": "0.1.4", 
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
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
                "name": "Pool",
                "state": True,
                "smart": True
                },
            "channel_3": {
                "name": "Geyser 2",
                "state": True,
                "smart": True
                },
            "channel_4": {
                "name": "disconnected",
                "state": False,
                "smart": False
                }, 
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )
    
    res = mqtt_connection.publish(
    topic=TOPICRELAYCONTROL,
    payload=json.dumps({
        "imei": "864454073558102",
        "relay": "1",
        "controls": [
            {"channel_1": "Geyser 1", "source": "brain", "state": True},
            {"channel_2": "Pool", "source": "brain", "state": True},
            {"channel_3": "Geyser 2", "source": "brain", "state": True}
        ],
        "timeStr": data_timestamp,
        "dataTimestamp": data_timestamp
    }),
    qos=mqtt5.QoS.AT_LEAST_ONCE,
    retain=False,
    )

    res = mqtt_connection.publish(
        topic=TOPICUSAGE,
        payload=json.dumps({
            "channel_1": {
                "name": "Geyser 1",
                "state": True,
                "load": apply_deviation(2500, 0.05)
                },
            "channel_2": {
                "name": "Pool",
                "state": True,
                "load": apply_deviation(1100, 0.05)
                },
            "channel_3": {
                "name": "Geyser 2",
                "state": apply_deviation(2500, 0.05),
                "load": 0
                },
            "channel_4": {
                "name": "disconnected",
                "state": False,
                "load": 0
                }, 
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
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
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
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
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )
    
    # Needs to wait for future to be complete
    while not res[0].done():
        time.sleep(0.1)

def run_jakkie():
    t = time.gmtime()
    data_timestamp = "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}Z".format(
        t[0], t[1], t[2], t[3], t[4], t[5]
    )
    
    print(str(data_timestamp) + ": Jakkie Koekemoer")
    
    TOPICDATA = "GOSOLR/BRAIN/868373070932654/DATA"
    
    
    # Constants for Inverter data retrieval
    TOKEN = "238c59c51665df09c9bc72daaa9c48074003939bac857a109f0b767b9d4e8622"
    KEY = "28c595aa93939bab9d"
    URL_BASE = "https://gsm.gosolr.co.za"
    SERIAL_NUMBER = "2107319089"
    
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
                        #print(entry["name"])
                        #print()
                        if entry["name"] == "Grid Frequency":
                            fac = entry["value"]
                        if entry["name"] == "SN":
                            inverterID = entry["value"]+"D"
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
                        if entry["key"] == "G_T_P": #E_CT_P
                            gridTiePower = entry["value"]    
                        if entry["key"] == "PG_Pt1": #E_CT_P
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
            "gridSoldTodayEnergy":0,
            "familyLoadPower":familyLoadPower,
            "bypassLoadPower":bypassLoadPower,
            "pSUM":pSUM,
            "homeLoadTodayEnergy":homeLoadTodayEnergy, 
            "gridTiePower":gridTiePower, 
            "gridPower":gridPower,
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )
    
    # Needs to wait for future to be complete
    while not res[0].done():
        time.sleep(0.1)

def run_okert():
    t = time.gmtime()
    data_timestamp = "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}Z".format(
        t[0], t[1], t[2], t[3], t[4], t[5]
    )
    
    print(str(data_timestamp) + ": Okert Els")
    
    TOPICDATA = "GOSOLR/BRAIN/868373070932423/DATA"
    TOPICMODELS = "GOSOLR/BRAIN/868373070932423/MODELS"
    TOPICRELAYS = "GOSOLR/BRAIN/868373070932423/RELAYS"
    TOPICUSAGE = "GOSOLR/BRAIN/868373070932423/USAGE"
    TOPICRISKS = "GOSOLR/BRAIN/868373070932423/RISKS"
    TOPICALERTS = "GOSOLR/BRAIN/868373070932423/ALERTS"
    TOPICHB = "GOSOLR/BRAIN/868373070932423/HB"
    TOPICSTATUS = "GOSOLR/BRAIN/868373070932423/STATUS"
    TOPICRELAYCONTROL = "GOSOLR/BRAIN/RELAYCONTROL/868373070932423"
    
    
    # Constants for Inverter data retrieval
    TOKEN = "238c59c51665df09c9bc72daaa9c48074003939bac857a109f0b767b9d4e8622"
    KEY = "28c595aa93939bab9d"
    URL_BASE = "https://gsm.gosolr.co.za"
    SERIAL_NUMBER = "2304194916"
    
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
                        #print(entry["name"])
                        #print()
                        if entry["name"] == "Grid Frequency":
                            fac = entry["value"]
                        if entry["name"] == "SN":
                            inverterID = entry["value"]+"D"
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
                        if entry["key"] == "G_T_P":
                            gridTiePower = entry["value"]    
                        if entry["key"] == "G_T_P": #E_CT_P
                            gridTiePower = entry["value"]    
                        if entry["key"] == "PG_Pt1": #E_CT_P
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
        topic=TOPICMODELS,
        payload=json.dumps({
            "edge": "1.3.0",
            "parsec": "1.4.1(a)",
            "east": "1.0.4",
            "gosolr": "2.1.0",
            "manager": "0.1.4", 
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
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
                "name": "disconnected",
                "state": False,
                "smart": False
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
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )
    
    res = mqtt_connection.publish(
    topic=TOPICRELAYCONTROL,
    payload=json.dumps({
        "imei": "868373070932423",
        "relay": "1",
        "controls": [
            {"channel_1": "Channel 1", "source": "brain", "state": True}
        ],
        "timeStr": data_timestamp,
        "dataTimestamp": data_timestamp
    }),
    qos=mqtt5.QoS.AT_LEAST_ONCE,
    retain=False,
    )

    res = mqtt_connection.publish(
        topic=TOPICUSAGE,
        payload=json.dumps({
            "channel_1": {
                "name": "Geyser",
                "state": True,
                "load": apply_deviation(1100, 0.05)
                },
            "channel_2": {
                "name": "disconnected",
                "state": False,
                "load": 0
                },
            "channel_3": {
                "name": "disconnected",
                "state": False,
                "load": 0
                },
            "channel_4": {
                "name": "disconnected",
                "state": False,
                "load": 0
                }, 
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
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
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
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
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
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
            "inverterTemperature":inverterTemperature,
            "batteryVoltage":batteryVoltage,
            "batteryCurrent":batteryCurrent,
            "SoC":SoC,
            "batteryTodayChargeEnergy":batteryTodayChargeEnergy,
            "batteryTodayDischargeEnergy":batteryTodayDischargeEnergy,
            "bypassAcVoltage":bypassAcVoltage,
            "bypassAcCurrent":bypassAcCurrent,
            "gridPurchasedTodayEnergy":gridPurchasedTodayEnergy,
            "gridSoldTodayEnergy":0,
            "familyLoadPower":familyLoadPower,
            "bypassLoadPower":bypassLoadPower,
            "pSUM":pSUM,
            "homeLoadTodayEnergy":homeLoadTodayEnergy, 
            "gridTiePower":gridTiePower, 
            "gridPower":gridPower,
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )
    
    # Needs to wait for future to be complete
    while not res[0].done():
        time.sleep(0.1)

def run_andre():
    t = time.gmtime()
    data_timestamp = "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}Z".format(
        t[0], t[1], t[2], t[3], t[4], t[5]
    )
    
    print(str(data_timestamp) + ": Andre Dickson")
    
    TOPICDATA = "GOSOLR/BRAIN/866069069857173/DATA"
    TOPICMODELS = "GOSOLR/BRAIN/866069069857173/MODELS"
    TOPICRELAYS = "GOSOLR/BRAIN/866069069857173/RELAYS"
    TOPICUSAGE = "GOSOLR/BRAIN/866069069857173/USAGE"
    TOPICRISKS = "GOSOLR/BRAIN/866069069857173/RISKS"
    TOPICALERTS = "GOSOLR/BRAIN/866069069857173/ALERTS"
    TOPICHB = "GOSOLR/BRAIN/866069069857173/HB"
    TOPICSTATUS = "GOSOLR/BRAIN/866069069857173/STATUS"
    TOPICRELAYCONTROL = "GOSOLR/BRAIN/RELAYCONTROL/866069069857173"
    
    
    # Constants for Inverter data retrieval
    TOKEN = "238c59c51665df09c9bc72daaa9c48074003939bac857a109f0b767b9d4e8622"
    KEY = "28c595aa93939bab9d"
    URL_BASE = "https://gsm.gosolr.co.za"
    SERIAL_NUMBER = "2211127459"
    
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
                        #print(entry["name"])
                        #print()
                        if entry["name"] == "Grid Frequency":
                            fac = entry["value"]
                        if entry["name"] == "SN":
                            inverterID = entry["value"]+"D"
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
                        if entry["key"] == "G_T_P":
                            gridTiePower = entry["value"]    
                        if entry["key"] == "G_T_P": #E_CT_P
                            gridTiePower = entry["value"]    
                        if entry["key"] == "PG_Pt1": #E_CT_P
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
        topic=TOPICMODELS,
        payload=json.dumps({
            "edge": "1.3.0",
            "parsec": "1.4.1(a)",
            "east": "1.0.4",
            "gosolr": "2.1.0",
            "manager": "0.1.4", 
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
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
                "name": "disconnected",
                "state": False,
                "smart": False
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
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )
    
    res = mqtt_connection.publish(
    topic=TOPICRELAYCONTROL,
    payload=json.dumps({
        "imei": "866069069857173",
        "relay": "1",
        "controls": [
            {"channel_1": "Channel 1", "source": "brain", "state": True}
        ],
        "timeStr": data_timestamp,
        "dataTimestamp": data_timestamp
    }),
    qos=mqtt5.QoS.AT_LEAST_ONCE,
    retain=False,
    )

    res = mqtt_connection.publish(
        topic=TOPICUSAGE,
        payload=json.dumps({
            "channel_1": {
                "name": "Geyser",
                "state": True,
                "load": apply_deviation(1100, 0.05)
                },
            "channel_2": {
                "name": "disconnected",
                "state": False,
                "load": 0
                },
            "channel_3": {
                "name": "disconnected",
                "state": False,
                "load": 0
                },
            "channel_4": {
                "name": "disconnected",
                "state": False,
                "load": 0
                }, 
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
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
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
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
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
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
            "inverterTemperature":inverterTemperature,
            "batteryVoltage":batteryVoltage,
            "batteryCurrent":batteryCurrent,
            "SoC":SoC,
            "batteryTodayChargeEnergy":batteryTodayChargeEnergy,
            "batteryTodayDischargeEnergy":batteryTodayDischargeEnergy,
            "bypassAcVoltage":bypassAcVoltage,
            "bypassAcCurrent":bypassAcCurrent,
            "gridPurchasedTodayEnergy":gridPurchasedTodayEnergy,
            "gridSoldTodayEnergy":0,
            "familyLoadPower":familyLoadPower,
            "bypassLoadPower":bypassLoadPower,
            "pSUM":pSUM,
            "homeLoadTodayEnergy":homeLoadTodayEnergy, 
            "gridTiePower":gridTiePower, 
            "gridPower":gridPower,
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )
    
    # Needs to wait for future to be complete
    while not res[0].done():
        time.sleep(0.1)

def run_zandi():
    t = time.gmtime()
    data_timestamp = "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}Z".format(
        t[0], t[1], t[2], t[3], t[4], t[5]
    )
    
    print(str(data_timestamp) + ": Zandi Tshabalala")
    
    TOPICDATA = "GOSOLR/BRAIN/866069069798088/DATA"
    TOPICMODELS = "GOSOLR/BRAIN/866069069798088/MODELS"
    TOPICRELAYS = "GOSOLR/BRAIN/866069069798088/RELAYS"
    TOPICUSAGE = "GOSOLR/BRAIN/866069069798088/USAGE"
    TOPICRISKS = "GOSOLR/BRAIN/866069069798088/RISKS"
    TOPICALERTS = "GOSOLR/BRAIN/866069069798088/ALERTS"
    TOPICHB = "GOSOLR/BRAIN/866069069798088/HB"
    TOPICSTATUS = "GOSOLR/BRAIN/866069069798088/STATUS"
    TOPICRELAYCONTROL = "GOSOLR/BRAIN/RELAYCONTROL/866069069798088"
    
    
    # Constants for Inverter data retrieval
    TOKEN = "238c59c51665df09c9bc72daaa9c48074003939bac857a109f0b767b9d4e8622"
    KEY = "28c595aa93939bab9d"
    URL_BASE = "https://gsm.gosolr.co.za"
    SERIAL_NUMBER = "2211166235"
    
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
                        #print(entry["name"])
                        #print()
                        if entry["name"] == "Grid Frequency":
                            fac = entry["value"]
                        if entry["name"] == "SN":
                            inverterID = entry["value"]+"D"
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
                        if entry["key"] == "G_T_P":
                            gridTiePower = entry["value"]    
                        if entry["key"] == "G_T_P": #E_CT_P
                            gridTiePower = entry["value"]    
                        if entry["key"] == "PG_Pt1": #E_CT_P
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
        topic=TOPICMODELS,
        payload=json.dumps({
            "edge": "1.3.0",
            "parsec": "1.4.1(a)",
            "east": "1.0.4",
            "gosolr": "2.1.0",
            "manager": "0.1.4", 
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
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
                "name": "disconnected",
                "state": False,
                "smart": False
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
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )
    
    res = mqtt_connection.publish(
    topic=TOPICRELAYCONTROL,
    payload=json.dumps({
        "imei": "866069069798088",
        "relay": "1",
        "controls": [
            {"channel_1": "Channel 1", "source": "brain", "state": True}
        ],
        "timeStr": data_timestamp,
        "dataTimestamp": data_timestamp
    }),
    qos=mqtt5.QoS.AT_LEAST_ONCE,
    retain=False,
    )

    res = mqtt_connection.publish(
        topic=TOPICUSAGE,
        payload=json.dumps({
            "channel_1": {
                "name": "Geyser",
                "state": True,
                "load": apply_deviation(1100, 0.05)
                },
            "channel_2": {
                "name": "disconnected",
                "state": False,
                "load": 0
                },
            "channel_3": {
                "name": "disconnected",
                "state": False,
                "load": 0
                },
            "channel_4": {
                "name": "disconnected",
                "state": False,
                "load": 0
                }, 
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
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
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
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
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
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
            "inverterTemperature":inverterTemperature,
            "batteryVoltage":batteryVoltage,
            "batteryCurrent":batteryCurrent,
            "SoC":SoC,
            "batteryTodayChargeEnergy":batteryTodayChargeEnergy,
            "batteryTodayDischargeEnergy":batteryTodayDischargeEnergy,
            "bypassAcVoltage":bypassAcVoltage,
            "bypassAcCurrent":bypassAcCurrent,
            "gridPurchasedTodayEnergy":gridPurchasedTodayEnergy,
            "gridSoldTodayEnergy":0,
            "familyLoadPower":familyLoadPower,
            "bypassLoadPower":bypassLoadPower,
            "pSUM":pSUM,
            "homeLoadTodayEnergy":homeLoadTodayEnergy, 
            "gridTiePower":gridTiePower, 
            "gridPower":gridPower,
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )
    
    # Needs to wait for future to be complete
    while not res[0].done():
        time.sleep(0.1)

def run_jarryd():
    t = time.gmtime()
    data_timestamp = "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}Z".format(
        t[0], t[1], t[2], t[3], t[4], t[5]
    )
    
    print(str(data_timestamp) + ": Jarryd Abraham")
    
    TOPICDATA = "GOSOLR/BRAIN/866069069856407/DATA"
    TOPICMODELS = "GOSOLR/BRAIN/866069069856407/MODELS"
    TOPICRELAYS = "GOSOLR/BRAIN/866069069856407/RELAYS"
    TOPICUSAGE = "GOSOLR/BRAIN/866069069856407/USAGE"
    TOPICRISKS = "GOSOLR/BRAIN/866069069856407/RISKS"
    TOPICALERTS = "GOSOLR/BRAIN/866069069856407/ALERTS"
    TOPICHB = "GOSOLR/BRAIN/866069069856407/HB"
    TOPICSTATUS = "GOSOLR/BRAIN/866069069856407/STATUS"
    TOPICRELAYCONTROL = "GOSOLR/BRAIN/RELAYCONTROL/866069069856407"
    
    
    # Constants for Inverter data retrieval
    TOKEN = "238c59c51665df09c9bc72daaa9c48074003939bac857a109f0b767b9d4e8622"
    KEY = "28c595aa93939bab9d"
    URL_BASE = "https://gsm.gosolr.co.za"
    SERIAL_NUMBER = "2303078668"
    
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
                        #print(entry["name"])
                        #print()
                        if entry["name"] == "Grid Frequency":
                            fac = entry["value"]
                        if entry["name"] == "SN":
                            inverterID = entry["value"]+"D"
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
                        if entry["key"] == "G_T_P":
                            gridTiePower = entry["value"]    
                        if entry["key"] == "G_T_P": #E_CT_P
                            gridTiePower = entry["value"]    
                        if entry["key"] == "PG_Pt1": #E_CT_P
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
        topic=TOPICMODELS,
        payload=json.dumps({
            "edge": "1.3.0",
            "parsec": "1.4.1(a)",
            "east": "1.0.4",
            "gosolr": "2.1.0",
            "manager": "0.1.4", 
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
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
                "name": "Solar Geyser",
                "state": True,
                "smart": True
                },
            "channel_2": {
                "name": "disconnected",
                "state": False,
                "smart": False
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
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )
    
    res = mqtt_connection.publish(
    topic=TOPICRELAYCONTROL,
    payload=json.dumps({
        "imei": "866069069856407",
        "relay": "1",
        "controls": [
            {"channel_1": "Solar Geyser", "source": "brain", "state": True}
        ],
        "timeStr": data_timestamp,
        "dataTimestamp": data_timestamp
    }),
    qos=mqtt5.QoS.AT_LEAST_ONCE,
    retain=False,
    )

    res = mqtt_connection.publish(
        topic=TOPICUSAGE,
        payload=json.dumps({
            "channel_1": {
                "name": "Solar Geyser",
                "state": True,
                "load": apply_deviation(850, 0.05)
                },
            "channel_2": {
                "name": "disconnected",
                "state": False,
                "load": 0
                },
            "channel_3": {
                "name": "disconnected",
                "state": False,
                "load": 0
                },
            "channel_4": {
                "name": "disconnected",
                "state": False,
                "load": 0
                }, 
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
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
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
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
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
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
            "inverterTemperature":inverterTemperature,
            "batteryVoltage":batteryVoltage,
            "batteryCurrent":batteryCurrent,
            "SoC":SoC,
            "batteryTodayChargeEnergy":batteryTodayChargeEnergy,
            "batteryTodayDischargeEnergy":batteryTodayDischargeEnergy,
            "bypassAcVoltage":bypassAcVoltage,
            "bypassAcCurrent":bypassAcCurrent,
            "gridPurchasedTodayEnergy":gridPurchasedTodayEnergy,
            "gridSoldTodayEnergy":0,
            "familyLoadPower":familyLoadPower,
            "bypassLoadPower":bypassLoadPower,
            "pSUM":pSUM,
            "homeLoadTodayEnergy":homeLoadTodayEnergy, 
            "gridTiePower":gridTiePower, 
            "gridPower":gridPower,
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )
    
    # Needs to wait for future to be complete
    while not res[0].done():
        time.sleep(0.1)

def run_william():
    t = time.gmtime()
    data_timestamp = "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}Z".format(
        t[0], t[1], t[2], t[3], t[4], t[5]
    )
    
    print(str(data_timestamp) + ": William Gallacher")
    
    TOPICDATA = "GOSOLR/BRAIN/868373070932720/DATA"
    TOPICMODELS = "GOSOLR/BRAIN/868373070932720/MODELS"
    TOPICRELAYS = "GOSOLR/BRAIN/868373070932720/RELAYS"
    TOPICUSAGE = "GOSOLR/BRAIN/868373070932720/USAGE"
    TOPICRISKS = "GOSOLR/BRAIN/868373070932720/RISKS"
    TOPICALERTS = "GOSOLR/BRAIN/868373070932720/ALERTS"
    TOPICHB = "GOSOLR/BRAIN/868373070932720/HB"
    TOPICSTATUS = "GOSOLR/BRAIN/868373070932720/STATUS"
    TOPICRELAYCONTROL = "GOSOLR/BRAIN/RELAYCONTROL/868373070932720"
    
    
    # Constants for Inverter data retrieval
    TOKEN = "238c59c51665df09c9bc72daaa9c48074003939bac857a109f0b767b9d4e8622"
    KEY = "28c595aa93939bab9d"
    URL_BASE = "https://gsm.gosolr.co.za"
    SERIAL_NUMBER = "2303200214"
    
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
                        #print(entry["name"])
                        #print()
                        if entry["name"] == "Grid Frequency":
                            fac = entry["value"]
                        if entry["name"] == "SN":
                            inverterID = entry["value"]+"D"
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
                        if entry["key"] == "G_T_P":
                            gridTiePower = entry["value"]    
                        if entry["key"] == "G_T_P": #E_CT_P
                            gridTiePower = entry["value"]    
                        if entry["key"] == "PG_Pt1": #E_CT_P
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
        topic=TOPICMODELS,
        payload=json.dumps({
            "edge": "1.3.0",
            "parsec": "1.4.1(a)",
            "east": "1.0.4",
            "gosolr": "2.1.0",
            "manager": "0.1.4", 
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
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
                "state": True,
                "smart": True
                },
            "channel_4": {
                "name": "Channel 4",
                "state": True,
                "smart": True
                },
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )
    
    res = mqtt_connection.publish(
    topic=TOPICRELAYCONTROL,
    payload=json.dumps({
        "imei": "868373070932720",
        "relay": "1",
        "controls": [
            {"channel_1": "Channel 1", "source": "brain", "state": True},
            {"channel_2": "Channel 2", "source": "brain", "state": True},
            {"channel_3": "Channel 3", "source": "brain", "state": True},
            {"channel_4": "Channel 4", "source": "brain", "state": True}
        ],
        "timeStr": data_timestamp,
        "dataTimestamp": data_timestamp
    }),
    qos=mqtt5.QoS.AT_LEAST_ONCE,
    retain=False,
    )

    res = mqtt_connection.publish(
        topic=TOPICUSAGE,
        payload=json.dumps({
            "channel_1": {
                "name": "Channel 1",
                "state": True,
                "load": 0
                },
            "channel_2": {
                "name": "Channel 2",
                "state": True,
                "load": 0
                },
            "channel_3": {
                "name": "Channel 3",
                "state": True,
                "load": 0
                },
            "channel_4": {
                "name": "Channel 4",
                "state": True,
                "load": 0
                }, 
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
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
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
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
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
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
            "inverterTemperature":inverterTemperature,
            "batteryVoltage":batteryVoltage,
            "batteryCurrent":batteryCurrent,
            "SoC":SoC,
            "batteryTodayChargeEnergy":batteryTodayChargeEnergy,
            "batteryTodayDischargeEnergy":batteryTodayDischargeEnergy,
            "bypassAcVoltage":bypassAcVoltage,
            "bypassAcCurrent":bypassAcCurrent,
            "gridPurchasedTodayEnergy":gridPurchasedTodayEnergy,
            "gridSoldTodayEnergy":0,
            "familyLoadPower":familyLoadPower,
            "bypassLoadPower":bypassLoadPower,
            "pSUM":pSUM,
            "homeLoadTodayEnergy":homeLoadTodayEnergy, 
            "gridTiePower":gridTiePower, 
            "gridPower":gridPower,
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )
    
    # Needs to wait for future to be complete
    while not res[0].done():
        time.sleep(0.1)

def run_vivien():
    t = time.gmtime()
    data_timestamp = "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}Z".format(
        t[0], t[1], t[2], t[3], t[4], t[5]
    )
    
    print(str(data_timestamp) + ": Vivien Kruger")
    
    TOPICDATA = "GOSOLR/BRAIN/868373070932050/DATA"
    TOPICMODELS = "GOSOLR/BRAIN/868373070932050/MODELS"
    TOPICRELAYS = "GOSOLR/BRAIN/868373070932050/RELAYS"
    TOPICUSAGE = "GOSOLR/BRAIN/868373070932050/USAGE"
    TOPICRISKS = "GOSOLR/BRAIN/868373070932050/RISKS"
    TOPICALERTS = "GOSOLR/BRAIN/868373070932050/ALERTS"
    TOPICHB = "GOSOLR/BRAIN/868373070932050/HB"
    TOPICSTATUS = "GOSOLR/BRAIN/868373070932050/STATUS"
    TOPICRELAYCONTROL = "GOSOLR/BRAIN/RELAYCONTROL/868373070932050"
    
    
    # Constants for Inverter data retrieval
    TOKEN = "238c59c51665df09c9bc72daaa9c48074003939bac857a109f0b767b9d4e8622"
    KEY = "28c595aa93939bab9d"
    URL_BASE = "https://gsm.gosolr.co.za"
    SERIAL_NUMBER = "2304288455"
    
    req = Request(f"{URL_BASE}/solarman/device/sn/{SERIAL_NUMBER}")
    req.add_header("Authorization", f"Bearer {TOKEN}")
    req.add_header("x-api-key", KEY)
    content = urlopen(req).read()

    raw_data = content.decode("utf-8")
    raw_dict = json.loads(raw_data)
    fac = 0
    inverterID = 0
    uPv1 = 0
    uPv2 = 0
    iPv1 = 0
    iPv2 = 0
    iAc1 = 0
    uAc1 = 0
    SoC = 0
    inverterTemperature = 0
    batteryVoltage = 0
    batteryCurrent = 0
    batteryTodayChargeEnergy = 0
    batteryTodayDischargeEnergy = 0
    gridPurchasedTodayEnergy = 0
    pSUM = 0
    homeLoadTodayEnergy = 0
    bypassLoadPower = 0
    bypassAcCurrent = 0
    bypassAcVoltage = 0
    familyLoadPower = 0
    eToday = 0
    gridTiePower = 0
    gridPower = 0
    # Adjust for nested structure: find the list in the JSON
    if isinstance(raw_dict, dict):  # JSON starts as a dictionary
        for key, value in raw_dict.items():
            if isinstance(value, list):  # Look for the list of objects
                for entry in value:
                    if "key" in entry:  # Check each entry for "key"
                        #print(entry["key"])
                        #print(entry["value"])
                        #print(entry["name"])
                        #print()
                        if entry["name"] == "Grid Frequency":
                            fac = entry["value"]
                        if entry["name"] == "SN":
                            inverterID = entry["value"]+"D"
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
                        if entry["key"] == "G_T_P":
                            gridTiePower = entry["value"]    
                        if entry["key"] == "G_T_P": #E_CT_P
                            gridTiePower = entry["value"]    
                        if entry["key"] == "PG_Pt1": #E_CT_P
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
        topic=TOPICMODELS,
        payload=json.dumps({
            "edge": "1.3.0",
            "parsec": "1.4.1(a)",
            "east": "1.0.4",
            "gosolr": "2.1.0",
            "manager": "0.1.4", 
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
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
                "state": True,
                "smart": True
                },
            "channel_4": {
                "name": "Channel 4",
                "state": True,
                "smart": True
                },
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )
    
    res = mqtt_connection.publish(
    topic=TOPICRELAYCONTROL,
    payload=json.dumps({
        "imei": "868373070932050",
        "relay": "1",
        "controls": [
            {"channel_1": "Channel 1", "source": "brain", "state": True},
            {"channel_2": "Channel 2", "source": "brain", "state": True},
            {"channel_3": "Channel 3", "source": "brain", "state": True},
            {"channel_4": "Channel 4", "source": "brain", "state": True}
        ],
        "timeStr": data_timestamp,
        "dataTimestamp": data_timestamp
    }),
    qos=mqtt5.QoS.AT_LEAST_ONCE,
    retain=False,
    )

    res = mqtt_connection.publish(
        topic=TOPICUSAGE,
        payload=json.dumps({
            "channel_1": {
                "name": "Channel 1",
                "state": True,
                "load": 0
                },
            "channel_2": {
                "name": "Channel 2",
                "state": True,
                "load": 0
                },
            "channel_3": {
                "name": "Channel 3",
                "state": True,
                "load": 0
                },
            "channel_4": {
                "name": "Channel 4",
                "state": True,
                "load": 0
                }, 
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
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
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
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
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
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
            "inverterTemperature":inverterTemperature,
            "batteryVoltage":batteryVoltage,
            "batteryCurrent":batteryCurrent,
            "SoC":SoC,
            "batteryTodayChargeEnergy":batteryTodayChargeEnergy,
            "batteryTodayDischargeEnergy":batteryTodayDischargeEnergy,
            "bypassAcVoltage":bypassAcVoltage,
            "bypassAcCurrent":bypassAcCurrent,
            "gridPurchasedTodayEnergy":gridPurchasedTodayEnergy,
            "gridSoldTodayEnergy":0,
            "familyLoadPower":familyLoadPower,
            "bypassLoadPower":bypassLoadPower,
            "pSUM":pSUM,
            "homeLoadTodayEnergy":homeLoadTodayEnergy, 
            "gridTiePower":gridTiePower, 
            "gridPower":gridPower,
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )
    
    # Needs to wait for future to be complete
    while not res[0].done():
        time.sleep(0.1)

def run_raymond_2():
    t = time.gmtime()
    data_timestamp = "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}Z".format(
        t[0], t[1], t[2], t[3], t[4], t[5]
    )
    
    print(str(data_timestamp) + ": Raymond Spiney")
    TOPICMODELS = "GOSOLR/BRAIN/868373070931706/MODELS"
    TOPICRISKS = "GOSOLR/BRAIN/868373070931706/RISKS"
    TOPICALERTS = "GOSOLR/BRAIN/868373070931706/ALERTS"
    TOPICHB = "GOSOLR/BRAIN/868373070931706/HB"
    TOPICSTATUS = "GOSOLR/BRAIN/868373070931706/STATUS"    
    
    # Constants for Inverter data retrieval
    TOKEN = "238c59c51665df09c9bc72daaa9c48074003939bac857a109f0b767b9d4e8622"
    KEY = "28c595aa93939bab9d"
    URL_BASE = "https://gsm.gosolr.co.za"
    SERIAL_NUMBER = "2306032261"
    
    req = Request(f"{URL_BASE}/solarman/device/sn/{SERIAL_NUMBER}")
    req.add_header("Authorization", f"Bearer {TOKEN}")
    req.add_header("x-api-key", KEY)
    content = urlopen(req).read()

    raw_data = content.decode("utf-8")
    raw_dict = json.loads(raw_data)
    

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
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
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
        topic=TOPICRISKS,
        payload=json.dumps({
            "risk": {
                "unplannedOutage": apply_deviation(600, 0.1),
                "plannedOutage": apply_deviation(300, 0.05),
                "disconnection": apply_deviation(800, 0.1)
                }, 
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
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
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )
    
    # Needs to wait for future to be complete
    while not res[0].done():
        time.sleep(0.1)

def run_raymond_1():
    t = time.gmtime()
    data_timestamp = "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}Z".format(
        t[0], t[1], t[2], t[3], t[4], t[5]
    )
    
    print(str(data_timestamp) + ": Raymond Spiney")
    
    TOPICDATA = "GOSOLR/BRAIN/868373070931961/DATA"
    TOPICMODELS = "GOSOLR/BRAIN/868373070931961/MODELS"
    TOPICRISKS = "GOSOLR/BRAIN/868373070931961/RISKS"
    TOPICALERTS = "GOSOLR/BRAIN/868373070931961/ALERTS"
    TOPICHB = "GOSOLR/BRAIN/868373070931961/HB"
    TOPICSTATUS = "GOSOLR/BRAIN/868373070931961/STATUS"    
    
    # Constants for Inverter data retrieval
    TOKEN = "238c59c51665df09c9bc72daaa9c48074003939bac857a109f0b767b9d4e8622"
    KEY = "28c595aa93939bab9d"
    URL_BASE = "https://gsm.gosolr.co.za"
    SERIAL_NUMBER = "2306032261"
    
    req = Request(f"{URL_BASE}/solarman/device/sn/{SERIAL_NUMBER}")
    req.add_header("Authorization", f"Bearer {TOKEN}")
    req.add_header("x-api-key", KEY)
    content = urlopen(req).read()

    raw_data = content.decode("utf-8")
    raw_dict = json.loads(raw_data)
    fac = 0
    inverterID = 0
    uPv1 = 0
    uPv2 = 0
    iPv1 = 0
    iPv2 = 0
    iAc1 = 0
    uAc1 = 0
    SoC = 0
    inverterTemperature = 0
    batteryVoltage = 0
    batteryCurrent = 0
    batteryTodayChargeEnergy = 0
    batteryTodayDischargeEnergy = 0
    gridPurchasedTodayEnergy = 0
    pSUM = 0
    homeLoadTodayEnergy = 0
    bypassLoadPower = 0
    bypassAcCurrent = 0
    bypassAcVoltage = 0
    familyLoadPower = 0
    eToday = 0
    gridTiePower = 0
    gridPower = 0
    # Adjust for nested structure: find the list in the JSON
    if isinstance(raw_dict, dict):  # JSON starts as a dictionary
        for key, value in raw_dict.items():
            if isinstance(value, list):  # Look for the list of objects
                for entry in value:
                    if "key" in entry:  # Check each entry for "key"
                        #print(entry["key"])
                        #print(entry["value"])
                        #print(entry["name"])
                        #print()
                        if entry["name"] == "Grid Frequency":
                            fac = entry["value"]
                        if entry["name"] == "SN":
                            inverterID = entry["value"]+"D"
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
                        if entry["key"] == "G_T_P":
                            gridTiePower = entry["value"]    
                        if entry["key"] == "G_T_P": #E_CT_P
                            gridTiePower = entry["value"]    
                        if entry["key"] == "PG_Pt1": #E_CT_P
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
        topic=TOPICMODELS,
        payload=json.dumps({
            "edge": "1.3.0",
            "parsec": "1.4.1(a)",
            "east": "1.0.4",
            "gosolr": "2.1.0",
            "manager": "0.1.4", 
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
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
        topic=TOPICRISKS,
        payload=json.dumps({
            "risk": {
                "unplannedOutage": apply_deviation(600, 0.1),
                "plannedOutage": apply_deviation(300, 0.05),
                "disconnection": apply_deviation(800, 0.1)
                }, 
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
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
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
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
            "inverterTemperature":inverterTemperature,
            "batteryVoltage":batteryVoltage,
            "batteryCurrent":batteryCurrent,
            "SoC":SoC,
            "batteryTodayChargeEnergy":batteryTodayChargeEnergy,
            "batteryTodayDischargeEnergy":batteryTodayDischargeEnergy,
            "bypassAcVoltage":bypassAcVoltage,
            "bypassAcCurrent":bypassAcCurrent,
            "gridPurchasedTodayEnergy":gridPurchasedTodayEnergy,
            "gridSoldTodayEnergy":0,
            "familyLoadPower":familyLoadPower,
            "bypassLoadPower":bypassLoadPower,
            "pSUM":pSUM,
            "homeLoadTodayEnergy":homeLoadTodayEnergy, 
            "gridTiePower":gridTiePower, 
            "gridPower":gridPower,
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )
    
    # Needs to wait for future to be complete
    while not res[0].done():
        time.sleep(0.1)

def run_raymond_3():
    t = time.gmtime()
    data_timestamp = "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}Z".format(
        t[0], t[1], t[2], t[3], t[4], t[5]
    )
    
    print(str(data_timestamp) + ": Raymond Spiney")
    
    TOPICDATA = "GOSOLR/BRAIN/868373070931862/DATA"
    TOPICMODELS = "GOSOLR/BRAIN/868373070931862/MODELS"
    TOPICRISKS = "GOSOLR/BRAIN/868373070931862/RISKS"
    TOPICALERTS = "GOSOLR/BRAIN/868373070931862/ALERTS"
    TOPICHB = "GOSOLR/BRAIN/868373070931862/HB"
    TOPICSTATUS = "GOSOLR/BRAIN/868373070931862/STATUS"    
    
    # Constants for Inverter data retrieval
    TOKEN = "238c59c51665df09c9bc72daaa9c48074003939bac857a109f0b767b9d4e8622"
    KEY = "28c595aa93939bab9d"
    URL_BASE = "https://gsm.gosolr.co.za"
    SERIAL_NUMBER = "2306084302"
    
    req = Request(f"{URL_BASE}/solarman/device/sn/{SERIAL_NUMBER}")
    req.add_header("Authorization", f"Bearer {TOKEN}")
    req.add_header("x-api-key", KEY)
    content = urlopen(req).read()

    raw_data = content.decode("utf-8")
    raw_dict = json.loads(raw_data)
    fac = 0
    inverterID = 0
    uPv1 = 0
    uPv2 = 0
    iPv1 = 0
    iPv2 = 0
    iAc1 = 0
    uAc1 = 0
    SoC = 0
    inverterTemperature = 0
    batteryVoltage = 0
    batteryCurrent = 0
    batteryTodayChargeEnergy = 0
    batteryTodayDischargeEnergy = 0
    gridPurchasedTodayEnergy = 0
    pSUM = 0
    homeLoadTodayEnergy = 0
    bypassLoadPower = 0
    bypassAcCurrent = 0
    bypassAcVoltage = 0
    familyLoadPower = 0
    eToday = 0
    gridTiePower = 0
    gridPower = 0
    # Adjust for nested structure: find the list in the JSON
    if isinstance(raw_dict, dict):  # JSON starts as a dictionary
        for key, value in raw_dict.items():
            if isinstance(value, list):  # Look for the list of objects
                for entry in value:
                    if "key" in entry:  # Check each entry for "key"
                        #print(entry["key"])
                        #print(entry["value"])
                        #print(entry["name"])
                        #print()
                        if entry["name"] == "Grid Frequency":
                            fac = entry["value"]
                        if entry["name"] == "SN":
                            inverterID = entry["value"]+"D"
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
                        if entry["key"] == "G_T_P":
                            gridTiePower = entry["value"]    
                        if entry["key"] == "G_T_P": #E_CT_P
                            gridTiePower = entry["value"]    
                        if entry["key"] == "PG_Pt1": #E_CT_P
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
        topic=TOPICMODELS,
        payload=json.dumps({
            "edge": "1.3.0",
            "parsec": "1.4.1(a)",
            "east": "1.0.4",
            "gosolr": "2.1.0",
            "manager": "0.1.4", 
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
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
        topic=TOPICRISKS,
        payload=json.dumps({
            "risk": {
                "unplannedOutage": apply_deviation(600, 0.1),
                "plannedOutage": apply_deviation(300, 0.05),
                "disconnection": apply_deviation(800, 0.1)
                }, 
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
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
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
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
            "inverterTemperature":inverterTemperature,
            "batteryVoltage":batteryVoltage,
            "batteryCurrent":batteryCurrent,
            "SoC":SoC,
            "batteryTodayChargeEnergy":batteryTodayChargeEnergy,
            "batteryTodayDischargeEnergy":batteryTodayDischargeEnergy,
            "bypassAcVoltage":bypassAcVoltage,
            "bypassAcCurrent":bypassAcCurrent,
            "gridPurchasedTodayEnergy":gridPurchasedTodayEnergy,
            "gridSoldTodayEnergy":0,
            "familyLoadPower":familyLoadPower,
            "bypassLoadPower":bypassLoadPower,
            "pSUM":pSUM,
            "homeLoadTodayEnergy":homeLoadTodayEnergy, 
            "gridTiePower":gridTiePower, 
            "gridPower":gridPower,
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )
    
    # Needs to wait for future to be complete
    while not res[0].done():
        time.sleep(0.1)

def run_rachel():
    t = time.gmtime()
    data_timestamp = "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}Z".format(
        t[0], t[1], t[2], t[3], t[4], t[5]
    )
    
    print(str(data_timestamp) + ": Rachel Claasen")
    
    TOPICDATA = "GOSOLR/BRAIN/868373070933116/DATA"
    TOPICMODELS = "GOSOLR/BRAIN/868373070933116/MODELS"
    TOPICRELAYS = "GOSOLR/BRAIN/868373070933116/RELAYS"
    TOPICUSAGE = "GOSOLR/BRAIN/868373070933116/USAGE"
    TOPICRISKS = "GOSOLR/BRAIN/868373070933116/RISKS"
    TOPICALERTS = "GOSOLR/BRAIN/868373070933116/ALERTS"
    TOPICHB = "GOSOLR/BRAIN/868373070933116/HB"
    TOPICSTATUS = "GOSOLR/BRAIN/868373070933116/STATUS"
    TOPICRELAYCONTROL = "GOSOLR/BRAIN/RELAYCONTROL/868373070933116"
    
    
    # Constants for Inverter data retrieval
    TOKEN = "238c59c51665df09c9bc72daaa9c48074003939bac857a109f0b767b9d4e8622"
    KEY = "28c595aa93939bab9d"
    URL_BASE = "https://gsm.gosolr.co.za"
    SERIAL_NUMBER = "2304256477"
    
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
                        #print(entry["name"])
                        #print()
                        if entry["name"] == "Grid Frequency":
                            fac = entry["value"]
                        if entry["name"] == "SN":
                            inverterID = entry["value"]+"D"
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
                        if entry["key"] == "G_T_P":
                            gridTiePower = entry["value"]    
                        if entry["key"] == "G_T_P": #E_CT_P
                            gridTiePower = entry["value"]    
                        if entry["key"] == "PG_Pt1": #E_CT_P
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
        topic=TOPICMODELS,
        payload=json.dumps({
            "edge": "1.3.0",
            "parsec": "1.4.1(a)",
            "east": "1.0.4",
            "gosolr": "2.1.0",
            "manager": "0.1.4", 
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
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
                "state": True,
                "smart": True
                },
            "channel_4": {
                "name": "Channel 4",
                "state": True,
                "smart": True
                },
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )
    
    res = mqtt_connection.publish(
    topic=TOPICRELAYCONTROL,
    payload=json.dumps({
        "imei": "868373070933116",
        "relay": "1",
        "controls": [
            {"channel_1": "Channel 1", "source": "brain", "state": True},
            {"channel_2": "Channel 2", "source": "brain", "state": True},
            {"channel_3": "Channel 3", "source": "brain", "state": True},
            {"channel_4": "Channel 4", "source": "brain", "state": True}
        ],
        "timeStr": data_timestamp,
        "dataTimestamp": data_timestamp
    }),
    qos=mqtt5.QoS.AT_LEAST_ONCE,
    retain=False,
    )

    res = mqtt_connection.publish(
        topic=TOPICUSAGE,
        payload=json.dumps({
            "channel_1": {
                "name": "Channel 1",
                "state": True,
                "load": 0
                },
            "channel_2": {
                "name": "Channel 2",
                "state": True,
                "load": 0
                },
            "channel_3": {
                "name": "Channel 3",
                "state": True,
                "load": 0
                },
            "channel_4": {
                "name": "Channel 4",
                "state": True,
                "load": 0
                }, 
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
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
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
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
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
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
            "inverterTemperature":inverterTemperature,
            "batteryVoltage":batteryVoltage,
            "batteryCurrent":batteryCurrent,
            "SoC":SoC,
            "batteryTodayChargeEnergy":batteryTodayChargeEnergy,
            "batteryTodayDischargeEnergy":batteryTodayDischargeEnergy,
            "bypassAcVoltage":bypassAcVoltage,
            "bypassAcCurrent":bypassAcCurrent,
            "gridPurchasedTodayEnergy":gridPurchasedTodayEnergy,
            "gridSoldTodayEnergy":0,
            "familyLoadPower":familyLoadPower,
            "bypassLoadPower":bypassLoadPower,
            "pSUM":pSUM,
            "homeLoadTodayEnergy":homeLoadTodayEnergy, 
            "gridTiePower":gridTiePower, 
            "gridPower":gridPower,
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )
    
    # Needs to wait for future to be complete
    while not res[0].done():
        time.sleep(0.1)


def run_veronika():
    t = time.gmtime()
    data_timestamp = "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}Z".format(
        t[0], t[1], t[2], t[3], t[4], t[5]
    )
    
    print(str(data_timestamp) + ": William Gallacher")
    
    TOPICDATA = "GOSOLR/BRAIN/868373070933348/DATA"
    TOPICMODELS = "GOSOLR/BRAIN/868373070933348/MODELS"
    TOPICRELAYS = "GOSOLR/BRAIN/868373070933348/RELAYS"
    TOPICUSAGE = "GOSOLR/BRAIN/868373070933348/USAGE"
    TOPICRISKS = "GOSOLR/BRAIN/868373070933348/RISKS"
    TOPICALERTS = "GOSOLR/BRAIN/868373070933348/ALERTS"
    TOPICHB = "GOSOLR/BRAIN/868373070933348/HB"
    TOPICSTATUS = "GOSOLR/BRAIN/868373070933348/STATUS"
    TOPICRELAYCONTROL = "GOSOLR/BRAIN/RELAYCONTROL/868373070933348"
    
    
    # Constants for Inverter data retrieval
    TOKEN = "238c59c51665df09c9bc72daaa9c48074003939bac857a109f0b767b9d4e8622"
    KEY = "28c595aa93939bab9d"
    URL_BASE = "https://gsm.gosolr.co.za"
    SERIAL_NUMBER = "2304158510"
    
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
                        #print(entry["name"])
                        #print()
                        if entry["name"] == "Grid Frequency":
                            fac = entry["value"]
                        if entry["name"] == "SN":
                            inverterID = entry["value"]+"D"
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
                        if entry["key"] == "G_T_P":
                            gridTiePower = entry["value"]    
                        if entry["key"] == "G_T_P": #E_CT_P
                            gridTiePower = entry["value"]    
                        if entry["key"] == "PG_Pt1": #E_CT_P
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
        topic=TOPICMODELS,
        payload=json.dumps({
            "edge": "1.3.0",
            "parsec": "1.4.1(a)",
            "east": "1.0.4",
            "gosolr": "2.1.0",
            "manager": "0.1.4", 
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
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
                "state": True,
                "smart": True
                },
            "channel_4": {
                "name": "Channel 4",
                "state": True,
                "smart": True
                },
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )
    
    res = mqtt_connection.publish(
    topic=TOPICRELAYCONTROL,
    payload=json.dumps({
        "imei": "868373070933348",
        "relay": "1",
        "controls": [
            {"channel_1": "Channel 1", "source": "brain", "state": True},
            {"channel_2": "Channel 2", "source": "brain", "state": True},
            {"channel_3": "Channel 3", "source": "brain", "state": True},
            {"channel_4": "Channel 4", "source": "brain", "state": True}
        ],
        "timeStr": data_timestamp,
        "dataTimestamp": data_timestamp
    }),
    qos=mqtt5.QoS.AT_LEAST_ONCE,
    retain=False,
    )

    res = mqtt_connection.publish(
        topic=TOPICUSAGE,
        payload=json.dumps({
            "channel_1": {
                "name": "Channel 1",
                "state": True,
                "load": 0
                },
            "channel_2": {
                "name": "Channel 2",
                "state": True,
                "load": 0
                },
            "channel_3": {
                "name": "Channel 3",
                "state": True,
                "load": 0
                },
            "channel_4": {
                "name": "Channel 4",
                "state": True,
                "load": 0
                }, 
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
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
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
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
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
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
            "inverterTemperature":inverterTemperature,
            "batteryVoltage":batteryVoltage,
            "batteryCurrent":batteryCurrent,
            "SoC":SoC,
            "batteryTodayChargeEnergy":batteryTodayChargeEnergy,
            "batteryTodayDischargeEnergy":batteryTodayDischargeEnergy,
            "bypassAcVoltage":bypassAcVoltage,
            "bypassAcCurrent":bypassAcCurrent,
            "gridPurchasedTodayEnergy":gridPurchasedTodayEnergy,
            "gridSoldTodayEnergy":0,
            "familyLoadPower":familyLoadPower,
            "bypassLoadPower":bypassLoadPower,
            "pSUM":pSUM,
            "homeLoadTodayEnergy":homeLoadTodayEnergy, 
            "gridTiePower":gridTiePower, 
            "gridPower":gridPower,
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )
    
    # Needs to wait for future to be complete
    while not res[0].done():
        time.sleep(0.1)

def run_jacques():
    t = time.gmtime()
    data_timestamp = "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}Z".format(
        t[0], t[1], t[2], t[3], t[4], t[5]
    )
    
    print(str(data_timestamp) + ": Jacques Pretorius")
    
    TOPICDATA = "GOSOLR/BRAIN/868373070933769/DATA"
    TOPICMODELS = "GOSOLR/BRAIN/868373070933769/MODELS"
    TOPICRELAYS = "GOSOLR/BRAIN/868373070933769/RELAYS"
    TOPICUSAGE = "GOSOLR/BRAIN/868373070933769/USAGE"
    TOPICRISKS = "GOSOLR/BRAIN/868373070933769/RISKS"
    TOPICALERTS = "GOSOLR/BRAIN/868373070933769/ALERTS"
    TOPICHB = "GOSOLR/BRAIN/868373070933769/HB"
    TOPICSTATUS = "GOSOLR/BRAIN/868373070933769/STATUS"
    TOPICRELAYCONTROL = "GOSOLR/BRAIN/RELAYCONTROL/868373070933769"
    
    
    # Constants for Inverter data retrieval
    TOKEN = "238c59c51665df09c9bc72daaa9c48074003939bac857a109f0b767b9d4e8622"
    KEY = "28c595aa93939bab9d"
    URL_BASE = "https://gsm.gosolr.co.za"
    SERIAL_NUMBER = "2304032301"
    
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
                        #print(entry["name"])
                        #print()
                        if entry["name"] == "Grid Frequency":
                            fac = entry["value"]
                        if entry["name"] == "SN":
                            inverterID = entry["value"]+"D"
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
                        if entry["key"] == "G_T_P":
                            gridTiePower = entry["value"]    
                        if entry["key"] == "G_T_P": #E_CT_P
                            gridTiePower = entry["value"]    
                        if entry["key"] == "PG_Pt1": #E_CT_P
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
        topic=TOPICMODELS,
        payload=json.dumps({
            "edge": "1.3.0",
            "parsec": "1.4.1(a)",
            "east": "1.0.4",
            "gosolr": "2.1.0",
            "manager": "0.1.4", 
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
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
                "state": True,
                "smart": True
                },
            "channel_4": {
                "name": "Channel 4",
                "state": True,
                "smart": True
                },
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )
    
    res = mqtt_connection.publish(
    topic=TOPICRELAYCONTROL,
    payload=json.dumps({
        "imei": "868373070933769",
        "relay": "1",
        "controls": [
            {"channel_1": "Channel 1", "source": "brain", "state": True},
            {"channel_2": "Channel 2", "source": "brain", "state": True},
            {"channel_3": "Channel 3", "source": "brain", "state": True},
            {"channel_4": "Channel 4", "source": "brain", "state": True}
        ],
        "timeStr": data_timestamp,
        "dataTimestamp": data_timestamp
    }),
    qos=mqtt5.QoS.AT_LEAST_ONCE,
    retain=False,
    )

    res = mqtt_connection.publish(
        topic=TOPICUSAGE,
        payload=json.dumps({
            "channel_1": {
                "name": "Channel 1",
                "state": True,
                "load": 0
                },
            "channel_2": {
                "name": "Channel 2",
                "state": True,
                "load": 0
                },
            "channel_3": {
                "name": "Channel 3",
                "state": True,
                "load": 0
                },
            "channel_4": {
                "name": "Channel 4",
                "state": True,
                "load": 0
                }, 
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
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
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
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
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
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
            "inverterTemperature":inverterTemperature,
            "batteryVoltage":batteryVoltage,
            "batteryCurrent":batteryCurrent,
            "SoC":SoC,
            "batteryTodayChargeEnergy":batteryTodayChargeEnergy,
            "batteryTodayDischargeEnergy":batteryTodayDischargeEnergy,
            "bypassAcVoltage":bypassAcVoltage,
            "bypassAcCurrent":bypassAcCurrent,
            "gridPurchasedTodayEnergy":gridPurchasedTodayEnergy,
            "gridSoldTodayEnergy":0,
            "familyLoadPower":familyLoadPower,
            "bypassLoadPower":bypassLoadPower,
            "pSUM":pSUM,
            "homeLoadTodayEnergy":homeLoadTodayEnergy, 
            "gridTiePower":gridTiePower, 
            "gridPower":gridPower,
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )
    
    # Needs to wait for future to be complete
    while not res[0].done():
        time.sleep(0.1)

def run_gideon():
    t = time.gmtime()
    data_timestamp = "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}Z".format(
        t[0], t[1], t[2], t[3], t[4], t[5]
    )
    
    print(str(data_timestamp) + ": Gideon Hoon")
    
    TOPICDATA = "GOSOLR/BRAIN/868373070932290/DATA"
    TOPICMODELS = "GOSOLR/BRAIN/868373070932290/MODELS"
    TOPICRELAYS = "GOSOLR/BRAIN/868373070932290/RELAYS"
    TOPICUSAGE = "GOSOLR/BRAIN/868373070932290/USAGE"
    TOPICRISKS = "GOSOLR/BRAIN/868373070932290/RISKS"
    TOPICALERTS = "GOSOLR/BRAIN/868373070932290/ALERTS"
    TOPICHB = "GOSOLR/BRAIN/868373070932290/HB"
    TOPICSTATUS = "GOSOLR/BRAIN/868373070932290/STATUS"
    TOPICRELAYCONTROL = "GOSOLR/BRAIN/RELAYCONTROL/868373070932290"
    
    
    # Constants for Inverter data retrieval
    TOKEN = "238c59c51665df09c9bc72daaa9c48074003939bac857a109f0b767b9d4e8622"
    KEY = "28c595aa93939bab9d"
    URL_BASE = "https://gsm.gosolr.co.za"
    SERIAL_NUMBER = "2211238422"
    
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
                        #print(entry["name"])
                        #print()
                        if entry["name"] == "Grid Frequency":
                            fac = entry["value"]
                        if entry["name"] == "SN":
                            inverterID = entry["value"]+"D"
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
                        if entry["key"] == "G_T_P":
                            gridTiePower = entry["value"]    
                        if entry["key"] == "G_T_P": #E_CT_P
                            gridTiePower = entry["value"]    
                        if entry["key"] == "PG_Pt1": #E_CT_P
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
        topic=TOPICMODELS,
        payload=json.dumps({
            "edge": "1.3.0",
            "parsec": "1.4.1(a)",
            "east": "1.0.4",
            "gosolr": "2.1.0",
            "manager": "0.1.4", 
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
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
                "state": True,
                "smart": True
                },
            "channel_4": {
                "name": "Channel 4",
                "state": True,
                "smart": True
                },
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )
    
    res = mqtt_connection.publish(
    topic=TOPICRELAYCONTROL,
    payload=json.dumps({
        "imei": "868373070932290",
        "relay": "1",
        "controls": [
            {"channel_1": "Channel 1", "source": "brain", "state": True},
            {"channel_2": "Channel 2", "source": "brain", "state": True},
            {"channel_3": "Channel 3", "source": "brain", "state": True},
            {"channel_4": "Channel 4", "source": "brain", "state": True}
        ],
        "timeStr": data_timestamp,
        "dataTimestamp": data_timestamp
    }),
    qos=mqtt5.QoS.AT_LEAST_ONCE,
    retain=False,
    )

    res = mqtt_connection.publish(
        topic=TOPICUSAGE,
        payload=json.dumps({
            "channel_1": {
                "name": "Channel 1",
                "state": True,
                "load": 0
                },
            "channel_2": {
                "name": "Channel 2",
                "state": True,
                "load": 0
                },
            "channel_3": {
                "name": "Channel 3",
                "state": True,
                "load": 0
                },
            "channel_4": {
                "name": "Channel 4",
                "state": True,
                "load": 0
                }, 
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
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
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
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
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
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
            "inverterTemperature":inverterTemperature,
            "batteryVoltage":batteryVoltage,
            "batteryCurrent":batteryCurrent,
            "SoC":SoC,
            "batteryTodayChargeEnergy":batteryTodayChargeEnergy,
            "batteryTodayDischargeEnergy":batteryTodayDischargeEnergy,
            "bypassAcVoltage":bypassAcVoltage,
            "bypassAcCurrent":bypassAcCurrent,
            "gridPurchasedTodayEnergy":gridPurchasedTodayEnergy,
            "gridSoldTodayEnergy":0,
            "familyLoadPower":familyLoadPower,
            "bypassLoadPower":bypassLoadPower,
            "pSUM":pSUM,
            "homeLoadTodayEnergy":homeLoadTodayEnergy, 
            "gridTiePower":gridTiePower, 
            "gridPower":gridPower,
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )
    
    # Needs to wait for future to be complete
    while not res[0].done():
        time.sleep(0.1)

def run_louis():
    t = time.gmtime()
    data_timestamp = "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}Z".format(
        t[0], t[1], t[2], t[3], t[4], t[5]
    )
    
    print(str(data_timestamp) + ": Louis Wentzel")
    
    TOPICDATA = "GOSOLR/BRAIN/868373070932431/DATA"
    TOPICMODELS = "GOSOLR/BRAIN/868373070932431/MODELS"
    TOPICRELAYS = "GOSOLR/BRAIN/868373070932431/RELAYS"
    TOPICUSAGE = "GOSOLR/BRAIN/868373070932431/USAGE"
    TOPICRISKS = "GOSOLR/BRAIN/868373070932431/RISKS"
    TOPICALERTS = "GOSOLR/BRAIN/868373070932431/ALERTS"
    TOPICHB = "GOSOLR/BRAIN/868373070932431/HB"
    TOPICSTATUS = "GOSOLR/BRAIN/868373070932431/STATUS"
    TOPICRELAYCONTROL = "GOSOLR/BRAIN/RELAYCONTROL/868373070932431"
    
    
    # Constants for Inverter data retrieval
    TOKEN = "238c59c51665df09c9bc72daaa9c48074003939bac857a109f0b767b9d4e8622"
    KEY = "28c595aa93939bab9d"
    URL_BASE = "https://gsm.gosolr.co.za"
    SERIAL_NUMBER = "2211019218"
    
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
                        #print(entry["name"])
                        #print()
                        if entry["name"] == "Grid Frequency":
                            fac = entry["value"]
                        if entry["name"] == "SN":
                            inverterID = entry["value"]+"D"
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
                        if entry["key"] == "G_T_P":
                            gridTiePower = entry["value"]    
                        if entry["key"] == "G_T_P": #E_CT_P
                            gridTiePower = entry["value"]    
                        if entry["key"] == "PG_Pt1": #E_CT_P
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
        topic=TOPICMODELS,
        payload=json.dumps({
            "edge": "1.3.0",
            "parsec": "1.4.1(a)",
            "east": "1.0.4",
            "gosolr": "2.1.0",
            "manager": "0.1.4", 
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
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
                "state": True,
                "smart": True
                },
            "channel_4": {
                "name": "Channel 4",
                "state": True,
                "smart": True
                },
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )
    
    res = mqtt_connection.publish(
    topic=TOPICRELAYCONTROL,
    payload=json.dumps({
        "imei": "868373070932431",
        "relay": "1",
        "controls": [
            {"channel_1": "Channel 1", "source": "brain", "state": True},
            {"channel_2": "Channel 2", "source": "brain", "state": True},
            {"channel_3": "Channel 3", "source": "brain", "state": True},
            {"channel_4": "Channel 4", "source": "brain", "state": True}
        ],
        "timeStr": data_timestamp,
        "dataTimestamp": data_timestamp
    }),
    qos=mqtt5.QoS.AT_LEAST_ONCE,
    retain=False,
    )

    res = mqtt_connection.publish(
        topic=TOPICUSAGE,
        payload=json.dumps({
            "channel_1": {
                "name": "Channel 1",
                "state": True,
                "load": 0
                },
            "channel_2": {
                "name": "Channel 2",
                "state": True,
                "load": 0
                },
            "channel_3": {
                "name": "Channel 3",
                "state": True,
                "load": 0
                },
            "channel_4": {
                "name": "Channel 4",
                "state": True,
                "load": 0
                }, 
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
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
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
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
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
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
            "inverterTemperature":inverterTemperature,
            "batteryVoltage":batteryVoltage,
            "batteryCurrent":batteryCurrent,
            "SoC":SoC,
            "batteryTodayChargeEnergy":batteryTodayChargeEnergy,
            "batteryTodayDischargeEnergy":batteryTodayDischargeEnergy,
            "bypassAcVoltage":bypassAcVoltage,
            "bypassAcCurrent":bypassAcCurrent,
            "gridPurchasedTodayEnergy":gridPurchasedTodayEnergy,
            "gridSoldTodayEnergy":0,
            "familyLoadPower":familyLoadPower,
            "bypassLoadPower":bypassLoadPower,
            "pSUM":pSUM,
            "homeLoadTodayEnergy":homeLoadTodayEnergy, 
            "gridTiePower":gridTiePower, 
            "gridPower":gridPower,
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )
    
    # Needs to wait for future to be complete
    while not res[0].done():
        time.sleep(0.1)

def run_esmond():
    t = time.gmtime()
    data_timestamp = "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}Z".format(
        t[0], t[1], t[2], t[3], t[4], t[5]
    )
    
    print(str(data_timestamp) + ": Esmond Jacobs")
    
    TOPICDATA = "GOSOLR/BRAIN/868373070932605/DATA"
    TOPICMODELS = "GOSOLR/BRAIN/868373070932605/MODELS"
    TOPICRELAYS = "GOSOLR/BRAIN/868373070932605/RELAYS"
    TOPICUSAGE = "GOSOLR/BRAIN/868373070932605/USAGE"
    TOPICRISKS = "GOSOLR/BRAIN/868373070932605/RISKS"
    TOPICALERTS = "GOSOLR/BRAIN/868373070932605/ALERTS"
    TOPICHB = "GOSOLR/BRAIN/868373070932605/HB"
    TOPICSTATUS = "GOSOLR/BRAIN/868373070932605/STATUS"
    TOPICRELAYCONTROL = "GOSOLR/BRAIN/RELAYCONTROL/868373070932605"
    
    
    # Constants for Inverter data retrieval
    TOKEN = "238c59c51665df09c9bc72daaa9c48074003939bac857a109f0b767b9d4e8622"
    KEY = "28c595aa93939bab9d"
    URL_BASE = "https://gsm.gosolr.co.za"
    SERIAL_NUMBER = "2208068231"
    
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
                        #print(entry["name"])
                        #print()
                        if entry["name"] == "Grid Frequency":
                            fac = entry["value"]
                        if entry["name"] == "SN":
                            inverterID = entry["value"]+"D"
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
                        if entry["key"] == "G_T_P":
                            gridTiePower = entry["value"]    
                        if entry["key"] == "G_T_P": #E_CT_P
                            gridTiePower = entry["value"]    
                        if entry["key"] == "PG_Pt1": #E_CT_P
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
        topic=TOPICMODELS,
        payload=json.dumps({
            "edge": "1.3.0",
            "parsec": "1.4.1(a)",
            "east": "1.0.4",
            "gosolr": "2.1.0",
            "manager": "0.1.4", 
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
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
                "name": "disconnected",
                "state": False,
                "smart": False
                },
            "channel_2": {
                "name": "disconnected",
                "state": False,
                "smart": False
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
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )
    
    res = mqtt_connection.publish(
    topic=TOPICRELAYCONTROL,
    payload=json.dumps({
        "imei": "868373070932605",
        "relay": "1",
        "controls": [
            {"channel_2": "disconnected", "source": "brain", "state": False}
        ],
        "timeStr": data_timestamp,
        "dataTimestamp": data_timestamp
    }),
    qos=mqtt5.QoS.AT_LEAST_ONCE,
    retain=False,
    )

    res = mqtt_connection.publish(
        topic=TOPICUSAGE,
        payload=json.dumps({
            "channel_1": {
                "name": "disconnected",
                "state": False,
                "load": 0
                },
            "channel_2": {
                "name": "disconnected",
                "state": False,
                "load": 0
                },
            "channel_3": {
                "name": "disconnected",
                "state": False,
                "load": 0
                },
            "channel_4": {
                "name": "disconnected",
                "state": False,
                "load": 0
                }, 
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
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
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
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
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
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
            "inverterTemperature":inverterTemperature,
            "batteryVoltage":batteryVoltage,
            "batteryCurrent":batteryCurrent,
            "SoC":SoC,
            "batteryTodayChargeEnergy":batteryTodayChargeEnergy,
            "batteryTodayDischargeEnergy":batteryTodayDischargeEnergy,
            "bypassAcVoltage":bypassAcVoltage,
            "bypassAcCurrent":bypassAcCurrent,
            "gridPurchasedTodayEnergy":gridPurchasedTodayEnergy,
            "gridSoldTodayEnergy":0,
            "familyLoadPower":familyLoadPower,
            "bypassLoadPower":bypassLoadPower,
            "pSUM":pSUM,
            "homeLoadTodayEnergy":homeLoadTodayEnergy, 
            "gridTiePower":gridTiePower, 
            "gridPower":gridPower,
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )
    
    # Needs to wait for future to be complete
    while not res[0].done():
        time.sleep(0.1)

def run_kimberleigh():
    t = time.gmtime()
    data_timestamp = "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}Z".format(
        t[0], t[1], t[2], t[3], t[4], t[5]
    )
    
    print(str(data_timestamp) + ": Kimberleigh Tessendorf")
    
    TOPICDATA = "GOSOLR/BRAIN/866069069856464/DATA"
    TOPICMODELS = "GOSOLR/BRAIN/866069069856464/MODELS"
    TOPICRELAYS = "GOSOLR/BRAIN/866069069856464/RELAYS"
    TOPICUSAGE = "GOSOLR/BRAIN/866069069856464/USAGE"
    TOPICRISKS = "GOSOLR/BRAIN/866069069856464/RISKS"
    TOPICALERTS = "GOSOLR/BRAIN/866069069856464/ALERTS"
    TOPICHB = "GOSOLR/BRAIN/866069069856464/HB"
    TOPICSTATUS = "GOSOLR/BRAIN/866069069856464/STATUS"
    TOPICRELAYCONTROL = "GOSOLR/BRAIN/RELAYCONTROL/866069069856464"
    
    
    # Constants for Inverter data retrieval
    TOKEN = "238c59c51665df09c9bc72daaa9c48074003939bac857a109f0b767b9d4e8622"
    KEY = "28c595aa93939bab9d"
    URL_BASE = "https://gsm.gosolr.co.za"
    SERIAL_NUMBER = "2303294355"
    
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
                        #print(entry["name"])
                        #print()
                        if entry["name"] == "Grid Frequency":
                            fac = entry["value"]
                        if entry["name"] == "SN":
                            inverterID = entry["value"]+"D"
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
                        if entry["key"] == "G_T_P":
                            gridTiePower = entry["value"]    
                        if entry["key"] == "G_T_P": #E_CT_P
                            gridTiePower = entry["value"]    
                        if entry["key"] == "PG_Pt1": #E_CT_P
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
        topic=TOPICMODELS,
        payload=json.dumps({
            "edge": "1.3.0",
            "parsec": "1.4.1(a)",
            "east": "1.0.4",
            "gosolr": "2.1.0",
            "manager": "0.1.4", 
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
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
                "name": "disconnected",
                "state": False,
                "smart": False
                },
            "channel_2": {
                "name": "disconnected",
                "state": False,
                "smart": False
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
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )
    
    res = mqtt_connection.publish(
    topic=TOPICRELAYCONTROL,
    payload=json.dumps({
        "imei": "866069069856464",
        "relay": "1",
        "controls": [
            {"channel_2": "disconnected", "source": "brain", "state": False}
        ],
        "timeStr": data_timestamp,
        "dataTimestamp": data_timestamp
    }),
    qos=mqtt5.QoS.AT_LEAST_ONCE,
    retain=False,
    )

    res = mqtt_connection.publish(
        topic=TOPICUSAGE,
        payload=json.dumps({
            "channel_1": {
                "name": "disconnected",
                "state": False,
                "load": 0
                },
            "channel_2": {
                "name": "disconnected",
                "state": False,
                "load": 0
                },
            "channel_3": {
                "name": "disconnected",
                "state": False,
                "load": 0
                },
            "channel_4": {
                "name": "disconnected",
                "state": False,
                "load": 0
                }, 
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
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
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
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
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
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
            "inverterTemperature":inverterTemperature,
            "batteryVoltage":batteryVoltage,
            "batteryCurrent":batteryCurrent,
            "SoC":SoC,
            "batteryTodayChargeEnergy":batteryTodayChargeEnergy,
            "batteryTodayDischargeEnergy":batteryTodayDischargeEnergy,
            "bypassAcVoltage":bypassAcVoltage,
            "bypassAcCurrent":bypassAcCurrent,
            "gridPurchasedTodayEnergy":gridPurchasedTodayEnergy,
            "gridSoldTodayEnergy":0,
            "familyLoadPower":familyLoadPower,
            "bypassLoadPower":bypassLoadPower,
            "pSUM":pSUM,
            "homeLoadTodayEnergy":homeLoadTodayEnergy, 
            "gridTiePower":gridTiePower, 
            "gridPower":gridPower,
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )
    
    # Needs to wait for future to be complete
    while not res[0].done():
        time.sleep(0.1)

def run_jacques():
    t = time.gmtime()
    data_timestamp = "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}Z".format(
        t[0], t[1], t[2], t[3], t[4], t[5]
    )
    
    print(str(data_timestamp) + ": Jacques Pretorius")
    
    TOPICDATA = "GOSOLR/BRAIN/868373070933769/DATA"
    TOPICMODELS = "GOSOLR/BRAIN/868373070933769/MODELS"
    TOPICRELAYS = "GOSOLR/BRAIN/868373070933769/RELAYS"
    TOPICUSAGE = "GOSOLR/BRAIN/868373070933769/USAGE"
    TOPICRISKS = "GOSOLR/BRAIN/868373070933769/RISKS"
    TOPICALERTS = "GOSOLR/BRAIN/868373070933769/ALERTS"
    TOPICHB = "GOSOLR/BRAIN/868373070933769/HB"
    TOPICSTATUS = "GOSOLR/BRAIN/868373070933769/STATUS"
    TOPICRELAYCONTROL = "GOSOLR/BRAIN/RELAYCONTROL/868373070933769"
    
    
    # Constants for Inverter data retrieval
    TOKEN = "238c59c51665df09c9bc72daaa9c48074003939bac857a109f0b767b9d4e8622"
    KEY = "28c595aa93939bab9d"
    URL_BASE = "https://gsm.gosolr.co.za"
    SERIAL_NUMBER = "2304032301"
    
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
                        #print(entry["name"])
                        #print()
                        if entry["name"] == "Grid Frequency":
                            fac = entry["value"]
                        if entry["name"] == "SN":
                            inverterID = entry["value"]+"D"
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
                        if entry["key"] == "G_T_P":
                            gridTiePower = entry["value"]    
                        if entry["key"] == "G_T_P": #E_CT_P
                            gridTiePower = entry["value"]    
                        if entry["key"] == "PG_Pt1": #E_CT_P
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
        topic=TOPICMODELS,
        payload=json.dumps({
            "edge": "1.3.0",
            "parsec": "1.4.1(a)",
            "east": "1.0.4",
            "gosolr": "2.1.0",
            "manager": "0.1.4", 
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
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
                "name": "disconnected",
                "state": False,
                "smart": False
                },
            "channel_2": {
                "name": "disconnected",
                "state": False,
                "smart": False
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
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )
    
    res = mqtt_connection.publish(
    topic=TOPICRELAYCONTROL,
    payload=json.dumps({
        "imei": "868373070933769",
        "relay": "1",
        "controls": [
            {"channel_1": "disconnected", "source": "brain", "state": False}
        ],
        "timeStr": data_timestamp,
        "dataTimestamp": data_timestamp
    }),
    qos=mqtt5.QoS.AT_LEAST_ONCE,
    retain=False,
    )

    res = mqtt_connection.publish(
        topic=TOPICUSAGE,
        payload=json.dumps({
            "channel_1": {
                "name": "disconnected",
                "state": False,
                "load": 0
                },
            "channel_2": {
                "name": "disconnected",
                "state": False,
                "load": 0
                },
            "channel_3": {
                "name": "disconnected",
                "state": False,
                "load": 0
                },
            "channel_4": {
                "name": "disconnected",
                "state": False,
                "load": 0
                }, 
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
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
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
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
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
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
            "inverterTemperature":inverterTemperature,
            "batteryVoltage":batteryVoltage,
            "batteryCurrent":batteryCurrent,
            "SoC":SoC,
            "batteryTodayChargeEnergy":batteryTodayChargeEnergy,
            "batteryTodayDischargeEnergy":batteryTodayDischargeEnergy,
            "bypassAcVoltage":bypassAcVoltage,
            "bypassAcCurrent":bypassAcCurrent,
            "gridPurchasedTodayEnergy":gridPurchasedTodayEnergy,
            "gridSoldTodayEnergy":0,
            "familyLoadPower":familyLoadPower,
            "bypassLoadPower":bypassLoadPower,
            "pSUM":pSUM,
            "homeLoadTodayEnergy":homeLoadTodayEnergy, 
            "gridTiePower":gridTiePower, 
            "gridPower":gridPower,
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )
    
    # Needs to wait for future to be complete
    while not res[0].done():
        time.sleep(0.1)


def run_jack():
    t = time.gmtime()
    data_timestamp = "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}Z".format(
        t[0], t[1], t[2], t[3], t[4], t[5]
    )
    
    print(str(data_timestamp) + ": Jack van Schalkwyk")
    
    TOPICDATA = "GOSOLR/BRAIN/866069069856233/DATA"
    TOPICMODELS = "GOSOLR/BRAIN/866069069856233/MODELS"
    TOPICRELAYS = "GOSOLR/BRAIN/866069069856233/RELAYS"
    TOPICUSAGE = "GOSOLR/BRAIN/866069069856233/USAGE"
    TOPICRISKS = "GOSOLR/BRAIN/866069069856233/RISKS"
    TOPICALERTS = "GOSOLR/BRAIN/866069069856233/ALERTS"
    TOPICHB = "GOSOLR/BRAIN/866069069856233/HB"
    TOPICSTATUS = "GOSOLR/BRAIN/866069069856233/STATUS"
    TOPICRELAYCONTROL = "GOSOLR/BRAIN/RELAYCONTROL/866069069856233"
    
    
    # Constants for Inverter data retrieval
    TOKEN = "238c59c51665df09c9bc72daaa9c48074003939bac857a109f0b767b9d4e8622"
    KEY = "28c595aa93939bab9d"
    URL_BASE = "https://gsm.gosolr.co.za"
    SERIAL_NUMBER = "2108109493"
    
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
                        #print(entry["name"])
                        #print()
                        if entry["name"] == "Grid Frequency":
                            fac = entry["value"]
                        if entry["name"] == "SN":
                            inverterID = entry["value"]+"D"
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
                        if entry["key"] == "G_T_P":
                            gridTiePower = entry["value"]    
                        if entry["key"] == "G_T_P": #E_CT_P
                            gridTiePower = entry["value"]    
                        if entry["key"] == "PG_Pt1": #E_CT_P
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
        topic=TOPICMODELS,
        payload=json.dumps({
            "edge": "1.3.0",
            "parsec": "1.4.1(a)",
            "east": "1.0.4",
            "gosolr": "2.1.0",
            "manager": "0.1.4", 
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
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
                "name": "disconnected",
                "state": False,
                "smart": False
                },
            "channel_2": {
                "name": "disconnected",
                "state": False,
                "smart": False
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
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )
    
    res = mqtt_connection.publish(
    topic=TOPICRELAYCONTROL,
    payload=json.dumps({
        "imei": "866069069856233",
        "relay": "1",
        "controls": [
            {"channel_1": "disconnected", "source": "brain", "state": False}
        ],
        "timeStr": data_timestamp,
        "dataTimestamp": data_timestamp
    }),
    qos=mqtt5.QoS.AT_LEAST_ONCE,
    retain=False,
    )

    res = mqtt_connection.publish(
        topic=TOPICUSAGE,
        payload=json.dumps({
            "channel_1": {
                "name": "disconnected",
                "state": False,
                "load": 0
                },
            "channel_2": {
                "name": "disconnected",
                "state": False,
                "load": 0
                },
            "channel_3": {
                "name": "disconnected",
                "state": False,
                "load": 0
                },
            "channel_4": {
                "name": "disconnected",
                "state": False,
                "load": 0
                }, 
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
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
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
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
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
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
            "inverterTemperature":inverterTemperature,
            "batteryVoltage":batteryVoltage,
            "batteryCurrent":batteryCurrent,
            "SoC":SoC,
            "batteryTodayChargeEnergy":batteryTodayChargeEnergy,
            "batteryTodayDischargeEnergy":batteryTodayDischargeEnergy,
            "bypassAcVoltage":bypassAcVoltage,
            "bypassAcCurrent":bypassAcCurrent,
            "gridPurchasedTodayEnergy":gridPurchasedTodayEnergy,
            "gridSoldTodayEnergy":0,
            "familyLoadPower":familyLoadPower,
            "bypassLoadPower":bypassLoadPower,
            "pSUM":pSUM,
            "homeLoadTodayEnergy":homeLoadTodayEnergy, 
            "gridTiePower":gridTiePower, 
            "gridPower":gridPower,
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )
    
    # Needs to wait for future to be complete
    while not res[0].done():
        time.sleep(0.1)


def run_kevin():
    t = time.gmtime()
    data_timestamp = "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}Z".format(
        t[0], t[1], t[2], t[3], t[4], t[5]
    )
    
    print(str(data_timestamp) + ": Kevin Tennendorf")
    
    TOPICDATA = "GOSOLR/BRAIN/868373070932639/DATA"
    TOPICMODELS = "GOSOLR/BRAIN/868373070932639/MODELS"
    TOPICRELAYS = "GOSOLR/BRAIN/868373070932639/RELAYS"
    TOPICUSAGE = "GOSOLR/BRAIN/868373070932639/USAGE"
    TOPICRISKS = "GOSOLR/BRAIN/868373070932639/RISKS"
    TOPICALERTS = "GOSOLR/BRAIN/868373070932639/ALERTS"
    TOPICHB = "GOSOLR/BRAIN/868373070932639/HB"
    TOPICSTATUS = "GOSOLR/BRAIN/868373070932639/STATUS"
    TOPICRELAYCONTROL = "GOSOLR/BRAIN/RELAYCONTROL/868373070932639"
    
    
    # Constants for Inverter data retrieval
    TOKEN = "238c59c51665df09c9bc72daaa9c48074003939bac857a109f0b767b9d4e8622"
    KEY = "28c595aa93939bab9d"
    URL_BASE = "https://gsm.gosolr.co.za"
    SERIAL_NUMBER = "2211222039"
    
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
                        #print(entry["name"])
                        #print()
                        if entry["name"] == "Grid Frequency":
                            fac = entry["value"]
                        if entry["name"] == "SN":
                            inverterID = entry["value"]+"D"
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
                        if entry["key"] == "G_T_P":
                            gridTiePower = entry["value"]   
                        if entry["key"] == "G_T_P": #E_CT_P
                            gridTiePower = entry["value"]    
                        if entry["key"] == "PG_Pt1": #E_CT_P
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
        topic=TOPICMODELS,
        payload=json.dumps({
            "edge": "1.3.0",
            "parsec": "1.4.1(a)",
            "east": "1.0.4",
            "gosolr": "2.1.0",
            "manager": "0.1.4", 
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
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
                "name": "Pump Type 1",
                "state": False,
                "smart": False
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
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )
    
    res = mqtt_connection.publish(
    topic=TOPICRELAYCONTROL,
    payload=json.dumps({
        "imei": "868373070932639",
        "relay": "1",
        "controls": [
            {"channel_1": "Geyser", "source": "brain", "state": False},
            {"channel_2": "Pump Type 1", "source": "brain", "state": False},
            {"channel_3": "disconnected", "source": "brain", "state": False},
            {"channel_4": "disconnected", "source": "brain", "state": False}
        ],
        "timeStr": data_timestamp,
        "dataTimestamp": data_timestamp
    }),
    qos=mqtt5.QoS.AT_LEAST_ONCE,
    retain=False,
    )
    
    res = mqtt_connection.publish(
    topic=TOPICRELAYCONTROL,
    payload=json.dumps({
        "imei": "868373070932639",
        "relay": "2",
        "controls": [
            {"channel_1": "Pump Type 2", "source": "brain", "state": False},
            {"channel_2": "Pump Type 3", "source": "brain", "state": True},
            {"channel_3": "disconnected", "source": "brain", "state": False},
            {"channel_4": "disconnected", "source": "brain", "state": False}
        ],
        "timeStr": data_timestamp,
        "dataTimestamp": data_timestamp
    }),
    qos=mqtt5.QoS.AT_LEAST_ONCE,
    retain=False,
    )

    res = mqtt_connection.publish(
        topic=TOPICUSAGE,
        payload=json.dumps({
            "channel_1": {
                "name": "Geyser",
                "state": False,
                "load": 0
                },
            "channel_2": {
                "name": "Pump Type 1",
                "state": False,
                "load": 0
                },
            "channel_3": {
                "name": "disconnected",
                "state": False,
                "load": 0
                },
            "channel_4": {
                "name": "disconnected",
                "state": False,
                "load": 0
                }, 
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )
    
    res = mqtt_connection.publish(
        topic=TOPICUSAGE,
        payload=json.dumps({
            "channel_1": {
                "name": "Pump Type 2",
                "state": False,
                "load": 0
                },
            "channel_2": {
                "name": "Pump Type 3",
                "state": True,
                "load": apply_deviation(500, 0.05)
                },
            "channel_3": {
                "name": "disconnected",
                "state": False,
                "load": 0
                },
            "channel_4": {
                "name": "disconnected",
                "state": False,
                "load": 0
                }, 
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
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
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
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
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
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
            "inverterTemperature":inverterTemperature,
            "batteryVoltage":batteryVoltage,
            "batteryCurrent":batteryCurrent,
            "SoC":SoC,
            "batteryTodayChargeEnergy":batteryTodayChargeEnergy,
            "batteryTodayDischargeEnergy":batteryTodayDischargeEnergy,
            "bypassAcVoltage":bypassAcVoltage,
            "bypassAcCurrent":bypassAcCurrent,
            "gridPurchasedTodayEnergy":gridPurchasedTodayEnergy,
            "gridSoldTodayEnergy":0,
            "familyLoadPower":familyLoadPower,
            "bypassLoadPower":bypassLoadPower,
            "pSUM":pSUM,
            "homeLoadTodayEnergy":homeLoadTodayEnergy, 
            "gridTiePower":gridTiePower, 
            "gridPower":gridPower,
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )
    
    # Needs to wait for future to be complete
    while not res[0].done():
        time.sleep(0.1)
        
def run_eddie():
    t = time.gmtime()
    data_timestamp = "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}Z".format(
        t[0], t[1], t[2], t[3], t[4], t[5]
    )
    
    print(str(data_timestamp) + ": Eddie Dunckley")
    
    TOPICDATA = "GOSOLR/BRAIN/868373070932472/DATA"
    
    # Constants for Inverter data retrieval
    TOKEN = "238c59c51665df09c9bc72daaa9c48074003939bac857a109f0b767b9d4e8622"
    KEY = "28c595aa93939bab9d"
    URL_BASE = "https://gsm.gosolr.co.za"
    SERIAL_NUMBER = "2303250346"
    
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
                        #print(entry["name"])
                        #print()
                        if entry["name"] == "Grid Frequency":
                            fac = entry["value"]
                        if entry["name"] == "SN":
                            inverterID = entry["value"]+"D"
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
                        if entry["key"] == "G_T_P":
                            gridTiePower = entry["value"]   
                        if entry["key"] == "G_T_P": #E_CT_P
                            gridTiePower = entry["value"]    
                        if entry["key"] == "PG_Pt1": #E_CT_P
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
            "gridSoldTodayEnergy":0,
            "familyLoadPower":familyLoadPower,
            "bypassLoadPower":bypassLoadPower,
            "pSUM":pSUM,
            "homeLoadTodayEnergy":homeLoadTodayEnergy, 
            "gridTiePower":gridTiePower, 
            "gridPower":gridPower,
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )
    
    # Needs to wait for future to be complete
    while not res[0].done():
        time.sleep(0.1)

def run_eddie_2():
    t = time.gmtime()
    data_timestamp = "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}Z".format(
        t[0], t[1], t[2], t[3], t[4], t[5]
    )
    
    print(str(data_timestamp) + ": Eddie Dunckley")
    
    TOPICDATA = "GOSOLR/BRAIN/868373070932043/DATA"
    
    # Constants for Inverter data retrieval
    TOKEN = "238c59c51665df09c9bc72daaa9c48074003939bac857a109f0b767b9d4e8622"
    KEY = "28c595aa93939bab9d"
    URL_BASE = "https://gsm.gosolr.co.za"
    SERIAL_NUMBER = "2106294063"
    
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
                        #print(entry["name"])
                        #print()
                        if entry["name"] == "Grid Frequency":
                            fac = entry["value"]
                        if entry["name"] == "SN":
                            inverterID = entry["value"]+"D"
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
                        if entry["key"] == "G_T_P":
                            gridTiePower = entry["value"]   
                        if entry["key"] == "G_T_P": #E_CT_P
                            gridTiePower = entry["value"]    
                        if entry["key"] == "PG_Pt1": #E_CT_P
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
            "gridSoldTodayEnergy":0,
            "familyLoadPower":familyLoadPower,
            "bypassLoadPower":bypassLoadPower,
            "pSUM":pSUM,
            "homeLoadTodayEnergy":homeLoadTodayEnergy, 
            "gridTiePower":gridTiePower, 
            "gridPower":gridPower,
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )
    
    # Needs to wait for future to be complete
    while not res[0].done():
        time.sleep(0.1)

def run_nic():
    t = time.gmtime()
    data_timestamp = "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}Z".format(
        t[0], t[1], t[2], t[3], t[4], t[5]
    )
    
    print(str(data_timestamp) + ": Nic Lashinger")
    
    TOPICDATA = "GOSOLR/BRAIN/866069069856423/DATA"
    
    # Constants for Inverter data retrieval
    TOKEN = "238c59c51665df09c9bc72daaa9c48074003939bac857a109f0b767b9d4e8622"
    KEY = "28c595aa93939bab9d"
    URL_BASE = "https://gsm.gosolr.co.za"
    SERIAL_NUMBER = "2211244525"
    
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
                        #print(entry["name"])
                        #print()
                        if entry["name"] == "Grid Frequency":
                            fac = entry["value"]
                        if entry["name"] == "SN":
                            inverterID = entry["value"]+"D"
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
                        if entry["key"] == "G_T_P":
                            gridTiePower = entry["value"]   
                        if entry["key"] == "G_T_P": #E_CT_P
                            gridTiePower = entry["value"]    
                        if entry["key"] == "PG_Pt1": #E_CT_P
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
            "gridSoldTodayEnergy":0,
            "familyLoadPower":familyLoadPower,
            "bypassLoadPower":bypassLoadPower,
            "pSUM":pSUM,
            "homeLoadTodayEnergy":homeLoadTodayEnergy, 
            "gridTiePower":gridTiePower, 
            "gridPower":gridPower,
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )
    
    # Needs to wait for future to be complete
    while not res[0].done():
        time.sleep(0.1)


def run_craig():
    t = time.gmtime()
    data_timestamp = "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}Z".format(
        t[0], t[1], t[2], t[3], t[4], t[5]
    )
    
    print(str(data_timestamp) + ": Craig Smith")
    
    TOPICDATA = "GOSOLR/BRAIN/866069069789269/DATA"
    TOPICMODELS = "GOSOLR/BRAIN/866069069789269/MODELS"
    TOPICSTATUS = "GOSOLR/BRAIN/866069069789269/STATUS"
    TOPICRELAYS = "GOSOLR/BRAIN/866069069789269/RELAYS"
    TOPICHB = "GOSOLR/BRAIN/866069069789269/HB"
    TOPICUSAGE = "GOSOLR/BRAIN/866069069789269/USAGE"
    TOPICRISKS = "GOSOLR/BRAIN/866069069789269/RISKS"
    TOPICRELAYCONTROL = "GOSOLR/BRAIN/RELAYCONTROL/866069069789269"
    
    # Constants for Inverter data retrieval
    TOKEN = "238c59c51665df09c9bc72daaa9c48074003939bac857a109f0b767b9d4e8622"
    KEY = "28c595aa93939bab9d"
    URL_BASE = "https://gsm.gosolr.co.za"
    SERIAL_NUMBER = "2303186019"
    
    req = Request(f"{URL_BASE}/solarman/device/sn/{SERIAL_NUMBER}")
    req.add_header("Authorization", f"Bearer {TOKEN}")
    req.add_header("x-api-key", KEY)
    content = urlopen(req).read()

    raw_data = content.decode("utf-8")
    raw_dict = json.loads(raw_data)
    
    inverterID = ""
    eToday = 0
    fac = 0
    bypassAcVoltage = 0
    bypassAcCurrent = 0
    gridPurchasedTodayEnergy = 0
    #print(raw_dict)

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
                            inverterID = entry["value"]+"S"
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
        topic=TOPICMODELS,
        payload=json.dumps({
            "edge": "1.3.0",
            "parsec": "1.4.1(a)",
            "east": "1.0.4",
            "gosolr": "2.1.0",
            "manager": "0.1.4", 
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )
    
    res = mqtt_connection.publish(
    topic=TOPICRELAYCONTROL,
    payload=json.dumps({
        "imei": "866069069789269",
        "relay": "1",
        "controls": [
            {"channel_1": "Channel 1", "source": "brain", "state": False},
            {"channel_2": "Channel 2", "source": "brain", "state": False},
            {"channel_3": "Channel 3", "source": "brain", "state": True},
            {"channel_4": "Channel 4", "source": "brain", "state": True}
        ],
        "timeStr": data_timestamp,
        "dataTimestamp": data_timestamp
    }),
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
                "smart": False
                },
            "channel_2": {
                "name": "Channel 2",
                "state": True,
                "smart": False
                },
            "channel_3": {
                "name": "Channel 3",
                "state": True,
                "smart": False
                },
            "channel_4": {
                "name": "Channel 4",
                "state": True,
                "smart": False
                }, 
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )

    res = mqtt_connection.publish(
        topic=TOPICUSAGE,
        payload=json.dumps({
            "channel_1": {
                "name": "Channel 1",
                "state": True,
                "load": apply_deviation(1000, 0.05)
                },
            "channel_2": {
                "name": "Channel 2",
                "state": True,
                "load": apply_deviation(1000, 0.05)
                },
            "channel_3": {
                "name": "Channel 3",
                "state": True,
                "load": apply_deviation(1000, 0.05)
                },
            "channel_4": {
                "name": "Channel 4",
                "state": True,
                "load": apply_deviation(1000, 0.05)
                }, 
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
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
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
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
            "timeStr": data_timestamp,
            "dataTimestamp": data_timestamp}),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )
    
    # Needs to wait for future to be complete
    while not res[0].done():
        time.sleep(0.1)

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

#try:
#    run_patrick()
#except Exception as e:
#    print(str(e))


try:
    run_kobus()
except Exception as e:
    print(str(e))
        
try:
    run_kevin()
except Exception as e:
    print(str(e))
        
try:
    run_andre()
except Exception as e:
    print(str(e))
    
try:
    run_andrew()
except Exception as e:
    print(str(e))
    
try:
    run_natalie()
except Exception as e:
    print(str(e))
        
try:
    run_rushil()
except Exception as e:
    print(str(e))
        
try:
    run_jakkie()
except Exception as e:
    print(str(e))
        
try:
    run_craig()
except Exception as e:
    print(str(e))
        
try:
    run_eddie()
except Exception as e:
    print(str(e))
        
try:
    run_eddie_2()
except Exception as e:
    print(str(e))

try:
    run_ummar()
except Exception as e:
    print(str(e))

try:
    run_nic()
except Exception as e:
    print(str(e))

try:
    run_ryan()
except Exception as e:
    print(str(e))

try:
    run_martin()
except Exception as e:
    print(str(e))

try:
    run_okert()
except Exception as e:
    print(str(e))
    #try:
    #    run_patrick()
    #except Exception as e:
    #    print(str(e))
        
try:
    run_neil()
except Exception as e:
    print(str(e))

try:
    run_wayne()
except Exception as e:
    print(str(e))

try:
    run_gideon()
except Exception as e:
    print(str(e))

try:
    run_fazeka()
except Exception as e:
    print(str(e))

try:
    run_claire()
except Exception as e:
    print(str(e))

try:
    run_ignatius()
except Exception as e:
    print(str(e))

try:
    run_zandi()
except Exception as e:
    print(str(e))

try:
    run_vick()
except Exception as e:
    print(str(e))

try:
    run_shaun()
except Exception as e:
    print(str(e))

try:
    run_jarryd()
except Exception as e:
    print(str(e))

try:
    run_esmond()
except Exception as e:
    print(str(e))

try:
    run_kimberleigh()
except Exception as e:
    print(str(e))

try:
    run_jack()
except Exception as e:
    print(str(e))

try:
    run_william()
except Exception as e:
    print(str(e))

try:
    run_louis()
except Exception as e:
    print(str(e))

try:
    run_gideon()
except Exception as e:
    print(str(e))

try:
    run_jacques()
except Exception as e:
    print(str(e))

try:
    run_veronika()
except Exception as e:
    print(str(e))

try:
    run_rachel()
except Exception as e:
    print(str(e))

try:
    run_raymond_1()
except Exception as e:
    print(str(e))

try:
    run_raymond_2()
except Exception as e:
    print(str(e))

try:
    run_raymond_3()
except Exception as e:
    print(str(e))

try:
    run_vivien()
except Exception as e:
    print(str(e))
