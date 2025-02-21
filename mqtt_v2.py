import json
import time
from datetime import datetime

from urllib.request import Request, urlopen


        
def run_patrick():
    t = time.gmtime()
    data_timestamp = "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}Z".format(
        t[0], t[1], t[2], t[3], t[4], t[5]
    )
    
    hours = t.tm_hour
    minutes = t.tm_min
    seconds = t.tm_sec

    channel_1_status = True
    channel_1_status = True
    channel_1_status = True
    channel_1_status = True

    print(str(data_timestamp) + ": Patrick Narbel")
    
    TOPICRELAYCONTROL = "GOSOLR/BRAIN/RELAYCONTROL/864454073547659"

    # The Oven is always ON
    default_controls = [
        {"channel_3": "Oven", "state": True}  # Oven ON always
    ]

    # 07:05 SAST (05:05 GMT) → Turn ON Pool Pump
    if hours == 5 and minutes == 5:
        res = mqtt_connection.publish(
            topic=TOPICRELAYCONTROL,
            payload=json.dumps({
                "imei": "864454073547659",
                "relay": "1",
                "source": "brain",
                "controls": default_controls + [
                    {"channel_4": "Pool", "state": True}  # Pool Pump ON
                ],
                "timeStr": data_timestamp,
                "dataTimestamp": data_timestamp
            }),
            qos=mqtt5.QoS.AT_LEAST_ONCE,
            retain=False,
        )
 # 09:35 SAST (07:35 GMT) → Keep Pool ON + Turn ON Geyser 1
    elif hours == 7 and minutes == 35:
        res = mqtt_connection.publish(
            topic=TOPICRELAYCONTROL,
            payload=json.dumps({
                "imei": "868373070933652",
                "relay": "1",
                "source": "brain",
                "controls": default_controls + [
                    {"channel_1": "Geyser1", "state": True},  # Geyser 1 ON
                    {"channel_4": "Pool", "state": True}  # Keep Pool Pump ON
                ],
                "timeStr": data_timestamp,
                "dataTimestamp": data_timestamp
            }),
            qos=mqtt5.QoS.AT_LEAST_ONCE,
            retain=False,
        )

    # 11:55 SAST (09:55 GMT) → Turn OFF Geyser 1, Keep Pool Pump ON
    elif hours == 9 and minutes == 55:
        res = mqtt_connection.publish(
            topic=TOPICRELAYCONTROL,
            payload=json.dumps({
                "imei": "868373070933652",
                "relay": "1",
                "source": "brain",
                "controls": default_controls + [
                    {"channel_1": "Geyser1", "state": False},  # Geyser 1 OFF
                    {"channel_4": "Pool", "state": True}  # Keep Pool Pump ON
                ],
                "timeStr": data_timestamp,
                "dataTimestamp": data_timestamp
            }),
            qos=mqtt5.QoS.AT_LEAST_ONCE,
            retain=False,
        )

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

try:
    run_patrick()
except Exception as e:
    print(str(e))
