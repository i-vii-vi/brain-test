import json
import time
import random
from datetime import datetime
from urllib.request import Request, urlopen
import hashlib

import math

from math import log

from awscrt import mqtt, mqtt5
from awsiot import mqtt5_client_builder

"familyLoadPower" == 0


def uPv1_val(input_time):
    """
    Returns a cosine-based value with a 24-hour period peaking at ~13:30,
    scaled to [0, 1], with small daily variations, a secondary sine wave,
    and ±2% noise.

    Parameters:
    - input_time (datetime.time or datetime.datetime): Time at which to evaluate the function.

    Returns:
    - float: Non-negative cosine-based value with noise (range: approximately [0, 1])
    """
    if isinstance(input_time, datetime):
        input_time = input_time.time()

    hours = input_time.hour + input_time.minute / 60 + input_time.second / 3600

    # Daily variation factors
    period = 24 + random.uniform(-0.3, 0.5)        # main period ~24h
    peak_time = 13.5 + random.uniform(-0.4, 0.3)   # ~13:30 peak with jitter
    amplitude = 1.0 + random.uniform(-0.07, 0.05)  # vary amplitude ±5%

    # Main daily cosine [0,1]
    base_value = (math.cos((2 * math.pi / period)
                  * (hours - peak_time)) + 1) / 2
    base_value *= amplitude

    # Secondary sine (smaller, faster fluctuations ~8h period)
    sub_period = period / 3 + random.uniform(-0.5, 0.2)   # ~8h period
    # amplitude around 0.1
    sub_amplitude = 0.1 + random.uniform(-0.06, 0.02)
    sub_wave = sub_amplitude * math.sin((2 * math.pi / sub_period) * hours)

    combined_value = base_value + sub_wave

    # Add ±2% noise
    noise_factor = 1 + random.uniform(-0.03, 0.05)
    noisy_value = combined_value * noise_factor

    # Clip to [0, 1]
    return min(max(noisy_value, 0.0), 1.0)


def uPv2_val(input_time):
    """
    Returns a cosine-based value with a 24-hour period peaking at ~13:30,
    scaled to [0, 1], with small daily variations, a secondary sine wave,
    and ±2% noise.

    Parameters:
    - input_time (datetime.time or datetime.datetime): Time at which to evaluate the function.

    Returns:
    - float: Non-negative cosine-based value with noise (range: approximately [0, 1])
    """
    if isinstance(input_time, datetime):
        input_time = input_time.time()

    hours = input_time.hour + input_time.minute / 60 + input_time.second / 3600

    # Daily variation factors
    period = 24 + random.uniform(-0.3, 0.5)        # main period ~24h
    peak_time = 13.5 + random.uniform(-0.4, 0.3)   # ~13:30 peak with jitter
    amplitude = 1.0 + random.uniform(-0.07, 0.05)  # vary amplitude ±5%

    # Main daily cosine [0,1]
    base_value = (math.cos((2 * math.pi / period)
                  * (hours - peak_time)) + 1) / 2
    base_value *= amplitude

    # Secondary sine (smaller, faster fluctuations ~8h period)
    sub_period = period / 3 + random.uniform(-0.5, 0.2)   # ~8h period
    # amplitude around 0.1
    sub_amplitude = 0.1 + random.uniform(-0.06, 0.02)
    sub_wave = sub_amplitude * math.sin((2 * math.pi / sub_period) * hours)

    combined_value = base_value + sub_wave

    # Add ±2% noise
    noise_factor = 1 + random.uniform(-0.03, 0.05)
    noisy_value = combined_value * noise_factor

    # Clip to [0, 1]
    return min(max(noisy_value, 0.0), 1.0)


def uPv3_val(input_time):
    """
    Returns a cosine-based value with a 24-hour period peaking at ~13:30,
    scaled to [0, 1], with small daily variations, a secondary sine wave,
    and ±2% noise.

    Parameters:
    - input_time (datetime.time or datetime.datetime): Time at which to evaluate the function.

    Returns:
    - float: Non-negative cosine-based value with noise (range: approximately [0, 1])
    """
    if isinstance(input_time, datetime):
        input_time = input_time.time()

    hours = input_time.hour + input_time.minute / 60 + input_time.second / 3600

    # Daily variation factors
    period = 24 + random.uniform(-0.3, 0.5)        # main period ~24h
    peak_time = 13.5 + random.uniform(-0.4, 0.3)   # ~13:30 peak with jitter
    amplitude = 1.0 + random.uniform(-0.07, 0.05)  # vary amplitude ±5%

    # Main daily cosine [0,1]
    base_value = (math.cos((2 * math.pi / period)
                  * (hours - peak_time)) + 1) / 2
    base_value *= amplitude

    # Secondary sine (smaller, faster fluctuations ~8h period)
    sub_period = period / 3 + random.uniform(-0.5, 0.2)   # ~8h period
    # amplitude around 0.1
    sub_amplitude = 0.1 + random.uniform(-0.06, 0.02)
    sub_wave = sub_amplitude * math.sin((2 * math.pi / sub_period) * hours)

    combined_value = base_value + sub_wave

    # Add ±2% noise
    noise_factor = 1 + random.uniform(-0.03, 0.05)
    noisy_value = combined_value * noise_factor

    # Clip to [0, 1]
    return min(max(noisy_value, 0.0), 1.0)


def cosine_value_with_noise(input_time):
    """
    Returns a cosine-based value with a 24-hour period peaking at 13:30,
    scaled to [0, 1], and adds up to ±2% noise.

    Parameters:
    - input_time (datetime.time or datetime.datetime): Time at which to evaluate the function.

    Returns:
    - float: Non-negative cosine-based value with noise (range: approximately [0, 1.02])
    """
    if isinstance(input_time, datetime):
        input_time = input_time.time()

    hours = input_time.hour + input_time.minute / 60 + input_time.second / 3600
    period = 24
    peak_time = 10.5  # 13:30 in decimal hours

    # Base cosine value shifted to [0, 1]
    base_value = 0.5 * (math.cos((2 * math.pi / period)
                        * (hours - peak_time)) + 1)

    # Add ±2% noise
    noise_factor = 1 + random.uniform(-0.02, 0.02)
    noisy_value = base_value * noise_factor

    # Clip to max 1.0 to avoid exceeding due to noise
    return min(noisy_value, 1.0)


def iPv1_val(input_time):
    """
    Returns a cosine-based value with a 24-hour period peaking at ~13:30,
    scaled to [0, 1], with small daily variations, a secondary sine wave,
    and ±2% noise.

    Parameters:
    - input_time (datetime.time or datetime.datetime): Time at which to evaluate the function.

    Returns:
    - float: Non-negative cosine-based value with noise (range: approximately [0, 1])
    """
    if isinstance(input_time, datetime):
        input_time = input_time.time()

    hours = input_time.hour + input_time.minute / 60 + input_time.second / 3600

    # Daily variation factors
    period = 24 + random.uniform(-0.3, 0.5)        # main period ~24h
    peak_time = 13.5 + random.uniform(-0.4, 0.3)   # ~13:30 peak with jitter
    amplitude = 1.0 + random.uniform(-0.07, 0.05)  # vary amplitude ±5%

    # Main daily cosine [0,1]
    base_value = (math.cos((2 * math.pi / period)
                  * (hours - peak_time)) + 1) / 2
    base_value *= amplitude

    # Secondary sine (smaller, faster fluctuations ~8h period)
    sub_period = period / 3 + random.uniform(-0.5, 0.2)   # ~8h period
    # amplitude around 0.1
    sub_amplitude = 0.1 + random.uniform(-0.06, 0.02)
    sub_wave = sub_amplitude * math.sin((2 * math.pi / sub_period) * hours)

    combined_value = base_value + sub_wave

    # Add ±2% noise
    noise_factor = 1 + random.uniform(-0.03, 0.05)
    noisy_value = combined_value * noise_factor

    # Clip to [0, 1]
    return min(max(noisy_value, 0.0), 1.0)


def iPv2_val(input_time):
    """
    Returns a cosine-based value with a 24-hour period peaking at ~13:30,
    scaled to [0, 1], with small daily variations, a secondary sine wave,
    and ±2% noise.

    Parameters:
    - input_time (datetime.time or datetime.datetime): Time at which to evaluate the function.

    Returns:
    - float: Non-negative cosine-based value with noise (range: approximately [0, 1])
    """
    if isinstance(input_time, datetime):
        input_time = input_time.time()

    hours = input_time.hour + input_time.minute / 60 + input_time.second / 3600

    # Daily variation factors
    period = 24 + random.uniform(-0.3, 0.5)        # main period ~24h
    peak_time = 13.5 + random.uniform(-0.4, 0.3)   # ~13:30 peak with jitter
    amplitude = 1.0 + random.uniform(-0.07, 0.05)  # vary amplitude ±5%

    # Main daily cosine [0,1]
    base_value = (math.cos((2 * math.pi / period)
                  * (hours - peak_time)) + 1) / 2
    base_value *= amplitude

    # Secondary sine (smaller, faster fluctuations ~8h period)
    sub_period = period / 3 + random.uniform(-0.5, 0.2)   # ~8h period
    # amplitude around 0.1
    sub_amplitude = 0.1 + random.uniform(-0.06, 0.02)
    sub_wave = sub_amplitude * math.sin((2 * math.pi / sub_period) * hours)

    combined_value = base_value + sub_wave

    # Add ±2% noise
    noise_factor = 1 + random.uniform(-0.03, 0.05)
    noisy_value = combined_value * noise_factor

    # Clip to [0, 1]
    return min(max(noisy_value, 0.0), 1.0)


def iPv3_val(input_time):
    """
    Returns a cosine-based value with a 24-hour period peaking at ~13:30,
    scaled to [0, 1], with small daily variations, a secondary sine wave,
    and ±2% noise.

    Parameters:
    - input_time (datetime.time or datetime.datetime): Time at which to evaluate the function.

    Returns:
    - float: Non-negative cosine-based value with noise (range: approximately [0, 1])
    """
    if isinstance(input_time, datetime):
        input_time = input_time.time()

    hours = input_time.hour + input_time.minute / 60 + input_time.second / 3600

    # Daily variation factors
    period = 24 + random.uniform(-0.3, 0.5)        # main period ~24h
    peak_time = 13.5 + random.uniform(-0.4, 0.3)   # ~13:30 peak with jitter
    amplitude = 1.0 + random.uniform(-0.07, 0.05)  # vary amplitude ±5%

    # Main daily cosine [0,1]
    base_value = (math.cos((2 * math.pi / period)
                  * (hours - peak_time)) + 1) / 2
    base_value *= amplitude

    # Secondary sine (smaller, faster fluctuations ~8h period)
    sub_period = period / 3 + random.uniform(-0.5, 0.2)   # ~8h period
    # amplitude around 0.1
    sub_amplitude = 0.1 + random.uniform(-0.06, 0.02)
    sub_wave = sub_amplitude * math.sin((2 * math.pi / sub_period) * hours)

    combined_value = base_value + sub_wave

    # Add ±2% noise
    noise_factor = 1 + random.uniform(-0.03, 0.05)
    noisy_value = combined_value * noise_factor

    # Clip to [0, 1]
    return min(max(noisy_value, 0.0), 1.0)


def run_heartbeat(imei,
                  brainFirmware_version,
                  reboot_timestamp,
                  general_system_state,
                  inverter_coms_state,
                  relay_pair_state,
                  devices_state,
                  system_control_state,
                  internal_state,
                  relayFirmware_version,
                  gosolr_version,
                  edge_version,
                  east_version,
                  pair_version,
                  manager_version,
                  parsec_version,
                  inverter_type,
                  inverter_sn,
                  order_number):
    t = time.gmtime()
    data_timestamp = "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}Z".format(
        t[0], t[1], t[2], t[3], t[4], t[5])

    print(f"{data_timestamp}: HEARTBEAT for IMEI {imei}")

    TOPICDATA = f"GOSOLR/BRAIN/{imei}/HB"

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

    mqtt_hb_payload = {
        "dataTimestamp": data_timestamp,
        "timeStr": data_timestamp,
        "version": brainFirmware_version,
        "rebootTime": reboot_timestamp,
        "wiring": [
            {"name": "general_system", "state": general_system_state},
            {"name": "inverter_coms", "state": inverter_coms_state},
            {"name": "relay_pair", "state": relay_pair_state},
            {"name": "devices", "state": devices_state},
            {"name": "system_control", "state": system_control_state},
            {"name": "internal", "state": internal_state},
            {"name": "cable", "state": True}
        ],
        "versions": [
            {"name": "brainFirmware", "type": "firmware",
                "number": brainFirmware_version},
            {"name": "relayFirmware", "type": "firmware",
                "number": relayFirmware_version},
            {"name": "gosolr", "type": "micropython-core", "number": gosolr_version},
            {"name": "edge", "type": "micropython-module", "number": edge_version},
            {"name": "east", "type": "micropython-module", "number": east_version},
            {"name": "pair", "type": "micropython-module", "number": pair_version},
            {"name": "manager", "type": "micropython-module",
                "number": manager_version},
            {"name": "parsec", "type": "micropython-support", "number": parsec_version}
        ],
        "devices": [
            {
                "name": "inverter",
                "type": inverter_type,
                "id": inverter_sn,
                "order": order_number
            }
        ]
    }

    res = mqtt_connection.publish(
        topic=TOPICDATA,
        payload=json.dumps(mqtt_hb_payload),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )

    while not res[0].done():
        time.sleep(0.1)


def run_dubai(imei):
    t = time.gmtime()
    data_timestamp = "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}Z".format(
        t[0], t[1], t[2], t[3], t[4], t[5])

    current_time = datetime(t.tm_year, t.tm_mon, t.tm_mday,
                            t.tm_hour, t.tm_min, t.tm_sec)

    # Call your function with current time
    cosine_val = cosine_value_with_noise(current_time)
    upv1 = uPv1_val(current_time)
    upv2 = uPv2_val(current_time)
    upv3 = uPv3_val(current_time)
    ipv1 = iPv1_val(current_time)
    ipv2 = iPv2_val(current_time)
    ipv3 = iPv3_val(current_time)

    print(f"{data_timestamp}: DATA for IMEI {imei}")

    TOPICDATA = f"GOSOLR/BRAIN/{imei}/DATA"

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

    gridFrequency = round(random.uniform(49, 51), 1)
    uAc1 = round(random.uniform(230, 242), 2)
    iAc1 = round(random.uniform(9, 11), 2)
    uPv1 = round(round(random.uniform(228, 241), 2)*upv1, 1)
    iPv1 = round(round(random.uniform(5, 8), 2)*ipv1, 1)
    uPv2 = round(round(random.uniform(220, 250), 2)*upv2, 1)
    iPv2 = round(round(random.uniform(5, 9), 2)*ipv2, 1)
    uPv3 = round(round(random.uniform(230, 242), 2)*upv3, 1)
    iPv3 = round(round(random.uniform(6, 9), 2)*ipv3, 1)

    mqtt_data_payload = {
        "dataTimestamp": data_timestamp,
        "timeStr": data_timestamp,
        "gridFrequency": gridFrequency,
        "iAc1": iAc1,
        "uAc1": uAc1,
        "iPv2": iPv2,
        "uPv2": uPv2,
        "iPv3": iPv3,
        "uPv3": uPv3,
        "iPv1": iPv1,
        "uPv1": uPv1,
        "gridPower": round(iAc1*uAc1, 1),
        "scaleFactor": round(log(1/(round(cosine_val, 2)+1)), 4)
    }

    print(mqtt_data_payload)

    res = mqtt_connection.publish(
        topic=TOPICDATA,
        payload=json.dumps(mqtt_data_payload),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )

    while not res[0].done():
        time.sleep(0.1)


def run_updatedRelays(imei):
    # Generate timestamp
    t = time.gmtime()
    data_timestamp = "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}Z".format(
        t[0], t[1], t[2], t[3], t[4], t[5])

    print(f"{data_timestamp}: UPDATED RELAYS for IMEI {imei}")

    # Convert IMEI into a consistent hexID-like format
    hash_object = hashlib.sha256(imei.encode())
    hash_int = int(hash_object.hexdigest(), 16)
    hexID = f"GoSolrRelay-{hash_int % 10**8:08d}"

    TOPICDATA = f"GOSOLR/RELAYCONTROL/RELAYS/{imei}"

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

    # Random value options
    status_options = [
        True,
        True,
        True,
        True,
        False
    ]
    value_options = [
        "1",
        "1"
    ]

    mqtt_updatedrelays_payload = {
        "time": data_timestamp,
        "client": [
            {"name": "pairedBrain", "value": imei},
            {"name": "id", "value": hexID},
            {"name": "relayNumber", "value": random.choice(value_options)},
            {"name": "pairingStatus", "value": "paired"}
        ],
        "channels": [
            {"name": "channel_1", "status": random.choice(status_options)},
            {"name": "channel_2", "status": random.choice(status_options)},
            {"name": "channel_3", "status": random.choice(status_options)},
            {"name": "channel_4", "status": random.choice(status_options)}
        ],
        "reports": [
            {"name": "channel_1", "value": "none"},
            {"name": "channel_2", "value": "none"},
            {"name": "channel_3", "value": "none"},
            {"name": "channel_4", "value": "none"},
            {"name": "board", "value": "none"}
        ]
    }

    res = mqtt_connection.publish(
        topic=TOPICDATA,
        payload=json.dumps(mqtt_updatedrelays_payload),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )

    while not res[0].done():
        time.sleep(0.1)


def run_watchdog(imei, deviceCount):
    t = time.gmtime()
    data_timestamp = "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}Z".format(
        t[0], t[1], t[2], t[3], t[4], t[5])

    print(f"{data_timestamp}: WATCHDOG for IMEI {imei}")

    TOPICDATA = f"GOSOLR/WATCHDOG/{imei}"

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

    # Random value options
    status_options = [
        "pingReceived",
        "operational",
        "primaryTimeout",
        "secondaryTimeout",
        "restartedNowOperational",
        "timeout"
    ]
    online_like_options = [
        "pingReceived",
        "pingReceived",
        "pingReceived",
        "pingReceived",
        "online",
        "online",
        "online",
        "online",
        "online",
        "online",
        "verifying",
        "restarted",
        "timeout"
    ]

    # Random value options
    status_options_brain = [
        "pingReceived",
        "operational",
        "primaryTimeout",
        "secondaryTimeout",
        "restartedNowOperational",
        "timeout"
    ]
    online_like_options_brain = [
        "pingReceived",
        "pingReceived",
        "pingReceived",
        "pingReceived",
        "online",
        "online",
        "online",
        "online",
        "online",
        "online",
        "verifying",
        "restarted",
        "timeout"
    ]

    if (imei == "868373070929080"):
        online_like_options_brain = [
            "offline",
            "timeout",
            "attemptedRestart"
        ]
        status_options_brain = [
            "secondaryTimeout",
            "attemptedRestartFailed"
        ]

    mqtt_watchdog_payload = {
        "dataTimestamp": data_timestamp,
        "timeStr": data_timestamp,
        "brainFirmware": [
            {"name": "timerService", "value": random.choice(
                online_like_options_brain)},
            {"name": "interruptHandler", "value": random.choice(
                online_like_options_brain)},
            {"name": "interprocessCommunication",
                "value": random.choice(online_like_options_brain)},
            {"name": "threadManager", "value": random.choice(
                online_like_options_brain)},
            {"name": "scheduler", "value": random.choice(
                online_like_options_brain)},
            {"name": "hardwareAbstraction", "value": random.choice(
                online_like_options_brain)},
            {"name": "kernel", "value": random.choice(
                online_like_options_brain)},
            {"name": "communicationStack", "value": random.choice(
                online_like_options_brain)},
            {"name": "bootloader", "value": random.choice(
                online_like_options_brain)},
            {"name": "status", "value": random.choice(status_options_brain)}
        ],
        "relayFirmware": [
            {"name": "status", "value": random.choice(status_options)},
            {"name": "pair_r", "value": random.choice(online_like_options)},
            {"name": "edge_r", "value": random.choice(online_like_options)},
            {"name": "deviceCount", "value": deviceCount},
            {"name": "activeChannels", "value": "4"}
        ],
        "brainModules": [
            {"name": "status", "value": random.choice(status_options_brain)},
            {"name": "gosolr", "value": random.choice(
                online_like_options_brain)},
            {"name": "pair", "value": random.choice(
                online_like_options_brain)},
            {"name": "edge", "value": random.choice(
                online_like_options_brain)},
            {"name": "manager", "value": random.choice(
                online_like_options_brain)}
        ]
    }

    res = mqtt_connection.publish(
        topic=TOPICDATA,
        payload=json.dumps(mqtt_watchdog_payload),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )

    while not res[0].done():
        time.sleep(0.1)


def run_status(imei, network_type):
    t = time.gmtime()
    data_timestamp = "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}Z".format(
        t[0], t[1], t[2], t[3], t[4], t[5])

    print(f"{data_timestamp}: STATUS for IMEI {imei}")

    TOPICSTATUS = f"GOSOLR/BRAIN/{imei}/STATUS"

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

    network_strength = random.randint(-72, -63)

    mqtt_status_payload = {
        "connected": True,
        "network": network_type,
        "networkStrength": network_strength
    }

    res = mqtt_connection.publish(
        topic=TOPICSTATUS,
        payload=json.dumps(mqtt_status_payload),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )

    while not res[0].done():
        time.sleep(0.1)


def run_relays(imei, relay_pair_state, channel_1_device, channel_2_device, channel_3_device, channel_4_device, channel_1_mode, channel_2_mode, channel_3_mode, channel_4_mode, channel_1_usage, channel_2_usage, channel_3_usage, channel_4_usage):
    t = time.gmtime()
    data_timestamp = "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}Z".format(
        t[0], t[1], t[2], t[3], t[4], t[5])

    print(f"{data_timestamp}: RELAYS for IMEI {imei}")

    TOPICRELAYS = f"GOSOLR/BRAIN/{imei}/RELAYS"

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

    mqtt_relays_payload = {
        "dataTimestamp": data_timestamp,
        "timeStr": data_timestamp,
        "channel_1": {
            "name": channel_1_device,
            "state": channel_1_mode,
            "usage": channel_1_usage
        },
        "channel_2": {
            "name": channel_2_device,
            "state": channel_2_mode,
            "usage": channel_2_usage
        },
        "channel_3": {
            "name": channel_3_device,
            "state": channel_3_mode,
            "usage": channel_3_usage
        },
        "channel_4": {
            "name": channel_4_device,
            "state": channel_4_mode,
            "usage": channel_4_usage
        },
        "paired": relay_pair_state
    }

    res = mqtt_connection.publish(
        topic=TOPICRELAYS,
        payload=json.dumps(mqtt_relays_payload),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )

    while not res[0].done():
        time.sleep(0.1)


def run_relaycontrol(imei, channel_1_device, channel_2_device, channel_3_device, channel_4_device, channel_1_state, channel_2_state, channel_3_state, channel_4_state):
    t = time.gmtime()
    data_timestamp = "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}Z".format(
        t[0], t[1], t[2], t[3], t[4], t[5])

    print(f"{data_timestamp}: RELAYCONTROL for IMEI {imei}")

    TOPICRELAYCONTROL = f"GOSOLR/BRAIN/{imei}/RELAYCONTROL"

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

    mqtt_relaycontrol_payload = {
        "dataTimestamp": data_timestamp,
        "timeStr": data_timestamp,
        "source": "brain",
        "relay": "1",
        "imei": imei,
        "controls": [{
            "channel_1": channel_1_device,
            "state": channel_1_state
        },
            {
            "channel_2": channel_2_device,
            "state": channel_2_state
        },
            {
            "channel_3": channel_3_device,
            "state": channel_3_state
        },
            {
            "channel_4": channel_4_device,
            "state": channel_4_state
        }]
    }

    res = mqtt_connection.publish(
        topic=TOPICRELAYCONTROL,
        payload=json.dumps(mqtt_relaycontrol_payload),
        qos=mqtt5.QoS.AT_LEAST_ONCE,
        retain=False,
    )

    while not res[0].done():
        time.sleep(0.1)


def run_tariffs(imei, buy_tariff, sell_tariff):
    t = time.gmtime()
    data_timestamp = "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}Z".format(
        t[0], t[1], t[2], t[3], t[4], t[5])

    print(f"{data_timestamp}: TARIFFS for IMEI {imei}")

    TOPICTARIFFS = f"GOSOLR/BRAIN/{imei}/TARIFFS"

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

    mqtt_tariffs_payload = {
        "dataTimestamp": data_timestamp,
        "timeStr": data_timestamp,
        "buy_tariff": buy_tariff,
        "sell_tariff": sell_tariff
    }

    res = mqtt_connection.publish(
        topic=TOPICTARIFFS,
        payload=json.dumps(mqtt_tariffs_payload),
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

    while not res[0].done():
        time.sleep(0.1)


def run_2304288455():
    t = time.gmtime()
    data_timestamp = "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}Z".format(
        t[0], t[1], t[2], t[3], t[4], t[5])

    print(str(data_timestamp) + ": 2304288455")

    TOPICDATA = "GOSOLR/BRAIN/868373070933603/DATA"
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

    # Check if the status "failed" and print out the error message
    if raw_dict.get("status") == "failed":
        err_msg = raw_dict.get("message", "<no message provided>")
        print(f"⚠️ API reported failure: {err_msg}")
        return

    json_data = raw_dict.get("data").get("data")

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

    while not res[0].done():
        time.sleep(0.1)


def run_2501154134():
    t = time.gmtime()
    data_timestamp = "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}Z".format(
        t[0], t[1], t[2], t[3], t[4], t[5])

    print(str(data_timestamp) + ": 2501154134")

    TOPICDATA = "GOSOLR/BRAIN/868373070917184/DATA"
    TOKEN = "238c59c51665df09c9bc72daaa9c48074003939bac857a109f0b767b9d4e8622"
    KEY = "28c595aa93939bab9d"
    URL_BASE = "https://gsm.gosolr.co.za"
    SERIAL_NUMBER = "2501154134"

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

    while not res[0].done():
        time.sleep(0.1)


def run_2107179045():
    t = time.gmtime()
    data_timestamp = "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}Z".format(
        t[0], t[1], t[2], t[3], t[4], t[5])

    print(str(data_timestamp) + ": 2107179045")

    TOPICDATA = "GOSOLR/BRAIN/868373070928538/DATA"
    TOKEN = "238c59c51665df09c9bc72daaa9c48074003939bac857a109f0b767b9d4e8622"
    KEY = "28c595aa93939bab9d"
    URL_BASE = "https://gsm.gosolr.co.za"
    SERIAL_NUMBER = "2107179045"

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

    while not res[0].done():
        time.sleep(0.1)


def run_2107057250():
    t = time.gmtime()
    data_timestamp = "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}Z".format(
        t[0], t[1], t[2], t[3], t[4], t[5])

    print(str(data_timestamp) + ": 2107057250")

    TOPICDATA = "GOSOLR/BRAIN/868373070932258/DATA"
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

    # Check if the status "failed" and print out the error message
    if raw_dict.get("status") == "failed":
        err_msg = raw_dict.get("message", "<no message provided>")
        print(f"⚠️ API reported failure: {err_msg}")
        return

    json_data = raw_dict.get("data").get("data")

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

    while not res[0].done():
        time.sleep(0.1)


def run_2304260750():
    t = time.gmtime()
    data_timestamp = "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}Z".format(
        t[0], t[1], t[2], t[3], t[4], t[5])

    print(str(data_timestamp) + ": 2304260750")

    TOPICDATA = "GOSOLR/BRAIN/868373070933041/DATA"
    TOKEN = "238c59c51665df09c9bc72daaa9c48074003939bac857a109f0b767b9d4e8622"
    KEY = "28c595aa93939bab9d"
    URL_BASE = "https://gsm.gosolr.co.za"
    SERIAL_NUMBER = "2304260750"

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
    inverterID = ""
    eToday = ""
    fac = ""

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

    while not res[0].done():
        time.sleep(0.1)


def run_2107199242():
    t = time.gmtime()
    data_timestamp = "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}Z".format(
        t[0], t[1], t[2], t[3], t[4], t[5])

    print(str(data_timestamp) + ": 2107199242")

    TOPICDATA = "GOSOLR/BRAIN/868373070932621/DATA"
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

    # Check if the status "failed" and print out the error message
    if raw_dict.get("status") == "failed":
        err_msg = raw_dict.get("message", "<no message provided>")
        print(f"⚠️ API reported failure: {err_msg}")
        return

    json_data = raw_dict.get("data").get("data")

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

    while not res[0].done():
        time.sleep(0.1)


def run_2106294063():
    t = time.gmtime()
    data_timestamp = "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}Z".format(
        t[0], t[1], t[2], t[3], t[4], t[5])

    print(str(data_timestamp) + ": 2106294063")

    TOPICDATA = "GOSOLR/BRAIN/868373070933843/DATA"
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

    # Check if the status "failed" and print out the error message
    if raw_dict.get("status") == "failed":
        err_msg = raw_dict.get("message", "<no message provided>")
        print(f"⚠️ API reported failure: {err_msg}")
        return

    json_data = raw_dict.get("data").get("data")

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

    while not res[0].done():
        time.sleep(0.1)


def run_2303250346():
    t = time.gmtime()
    data_timestamp = "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}Z".format(
        t[0], t[1], t[2], t[3], t[4], t[5])

    print(str(data_timestamp) + ": 2303250346")

    TOPICDATA = "GOSOLR/BRAIN/868373070930849/DATA"
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

    # Check if the status "failed" and print out the error message
    if raw_dict.get("status") == "failed":
        err_msg = raw_dict.get("message", "<no message provided>")
        print(f"⚠️ API reported failure: {err_msg}")
        return

    json_data = raw_dict.get("data").get("data")

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

    while not res[0].done():
        time.sleep(0.1)


def run_2209223588():
    t = time.gmtime()
    data_timestamp = "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}Z".format(
        t[0], t[1], t[2], t[3], t[4], t[5])

    print(str(data_timestamp) + ": 2209223588")

    TOPICDATA = "GOSOLR/BRAIN/866069069798807/DATA"
    TOKEN = "238c59c51665df09c9bc72daaa9c48074003939bac857a109f0b767b9d4e8622"
    KEY = "28c595aa93939bab9d"
    URL_BASE = "https://gsm.gosolr.co.za"
    SERIAL_NUMBER = "2209223588"

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

    while not res[0].done():
        time.sleep(0.1)


def run_2305053102():
    t = time.gmtime()
    data_timestamp = "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}Z".format(
        t[0], t[1], t[2], t[3], t[4], t[5])

    print(str(data_timestamp) + ": 2305053102")

    TOPICDATA = "GOSOLR/BRAIN/868373070931565/DATA"
    TOKEN = "238c59c51665df09c9bc72daaa9c48074003939bac857a109f0b767b9d4e8622"
    KEY = "28c595aa93939bab9d"
    URL_BASE = "https://gsm.gosolr.co.za"
    SERIAL_NUMBER = "2305053102"

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

    while not res[0].done():
        time.sleep(0.1)


def run_2211127459():
    t = time.gmtime()
    data_timestamp = "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}Z".format(
        t[0], t[1], t[2], t[3], t[4], t[5])

    print(str(data_timestamp) + ": 2211127459")

    TOPICDATA = "GOSOLR/BRAIN/868373070930435/DATA"
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

    # Check if the status "failed" and print out the error message
    if raw_dict.get("status") == "failed":
        err_msg = raw_dict.get("message", "<no message provided>")
        print(f"⚠️ API reported failure: {err_msg}")
        return

    json_data = raw_dict.get("data").get("data")

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

    while not res[0].done():
        time.sleep(0.1)


def run_2501142533():
    t = time.gmtime()
    data_timestamp = "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}Z".format(
        t[0], t[1], t[2], t[3], t[4], t[5])

    print(str(data_timestamp) + ": 2501142533")

    TOPICDATA = "GOSOLR/BRAIN/868373070929676/DATA"
    TOKEN = "238c59c51665df09c9bc72daaa9c48074003939bac857a109f0b767b9d4e8622"
    KEY = "28c595aa93939bab9d"
    URL_BASE = "https://gsm.gosolr.co.za"
    SERIAL_NUMBER = "2501142533"

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

    while not res[0].done():
        time.sleep(0.1)


def run_2305052900():
    t = time.gmtime()
    data_timestamp = "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}Z".format(
        t[0], t[1], t[2], t[3], t[4], t[5])

    print(str(data_timestamp) + ": 2305052900")

    TOPICDATA = "GOSOLR/BRAIN/868373070933025/DATA"
    TOKEN = "238c59c51665df09c9bc72daaa9c48074003939bac857a109f0b767b9d4e8622"
    KEY = "28c595aa93939bab9d"
    URL_BASE = "https://gsm.gosolr.co.za"
    SERIAL_NUMBER = "2305052900"

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

    while not res[0].done():
        time.sleep(0.1)


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

try:
    CLIENT_ID = "brain-learning-n-s"
    run_2305052900()
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-learning-r-v"
    run_data(imei="868373070935574", inverter_serial="1031200239070234")
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-5f1a2f30eb16"
    t = time.gmtime()
    data_timestamp = "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}Z".format(
        t[0], t[1], t[2], t[3], t[4], t[5])
    #run_heartbeat(
    #    imei="5F1A2F30EB16",
    #    brainFirmware_version="1.0.0.1",
    #    reboot_timestamp="2025-05-25T11:56:00Z",
    #    general_system_state=True,
    #    inverter_coms_state=False,
    #    relay_pair_state=False,
    #    devices_state=False,
    #    system_control_state=False,
    #    internal_state=True,
    #    relayFirmware_version="0.0.0.0",
    #    gosolr_version="1.0.0.0",
    #    edge_version="1.0.0.0",
    #    east_version="0.0.0.0",
    #    pair_version="0.0.0.0",
    #    manager_version="0.0.0",
    #    parsec_version="0.0.0",
    #    inverter_type="sungro",
    #    order_number="00000",
    #    inverter_sn="00000"
    #)
    #run_status(imei="5F1A2F30EB16",
    #           network_type="wifi | 5g")
    #run_dubai(imei="5F1A2F30EB16")
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373070926797"
    run_data(imei="868373070926797", inverter_serial="2209233278")
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373070932621"
    run_watchdog(imei="868373070932621", deviceCount="4")
    run_updatedRelays(imei="868373070932621")
    run_heartbeat(
        imei="868373070932621",
        brainFirmware_version="1.0.3.9(α)",
        reboot_timestamp="2025-06-13T12:04:00Z",
        general_system_state=True,
        inverter_coms_state=True,
        relay_pair_state=True,
        devices_state=True,
        system_control_state=True,
        internal_state=True,
        relayFirmware_version="2.0.2.2",
        gosolr_version="2.7.1",
        edge_version="1.8.9",
        east_version="1.0.22",
        pair_version="2.1.4",
        manager_version="0.9.15",
        parsec_version="1.5.14",
        inverter_type="deye-1p",
        order_number="14822",
        inverter_sn="2107199242"
    )
    #CLIENT_ID = "brain-868373070929080"
    #run_watchdog(imei="868373070929080", deviceCount="4")
    #run_updatedRelays(imei="868373070929080")
    CLIENT_ID = "brain-868373070931391"
    run_watchdog(imei="868373070931391", deviceCount="1")
    CLIENT_ID = "brain-868373070932571"
    run_watchdog(imei="868373070932571", deviceCount="1")
    CLIENT_ID = "brain-868373070932886"
    run_watchdog(imei="868373070932886", deviceCount="1")
    CLIENT_ID = "brain-868373070935624"
    run_watchdog(imei="868373070935624", deviceCount="0")
    #CLIENT_ID = "brain-868373070926805"
    #run_watchdog(imei="868373070926805", deviceCount="1")
    CLIENT_ID = "brain-868373070934213"
    run_watchdog(imei="868373070934213", deviceCount="1")
    CLIENT_ID = "brain-868373070933603"
    run_watchdog(imei="868373070916319", deviceCount="1")
    run_data(imei="868373070916319", inverter_serial="2302120796")
    CLIENT_ID = "brain-868373070916632"
    run_data(imei="868373070916632", inverter_serial="2303150986")
    CLIENT_ID = "brain-868373070914256"
    run_data(imei="868373070914256", inverter_serial="2210152550")
    CLIENT_ID = "brain-868373070930823"
    run_data(imei="868373070930823", inverter_serial="2210152550")
    CLIENT_ID = "brain-868373070928843"
    run_data(imei="868373070928843", inverter_serial="2210152550")
    CLIENT_ID = "brain-868373070936358"
    run_data(imei="868373070936358", inverter_serial="2209244055")
    CLIENT_ID = "brain-868373070927993"
    run_data(imei="868373070927993", inverter_serial="2209223706")
    CLIENT_ID = "brain-868373070927993"
    run_data(imei="868373070927993", inverter_serial="2209223706")
    CLIENT_ID = "brain-868373070928843"
    run_watchdog(imei="868373070928843", deviceCount="1")
    CLIENT_ID = "brain-868373070916319"
    run_watchdog(imei="868373070933603", deviceCount="1")
    run_watchdog(imei="868373070932522", deviceCount="1")
    run_watchdog(imei="868373070930674", deviceCount="1")
    run_watchdog(imei="868373070932233", deviceCount="1")
    run_watchdog(imei="868379070929981", deviceCount="1")
    run_watchdog(imei="868373070932324", deviceCount="1")
    run_watchdog(imei="868373070935657", deviceCount="1")
    run_watchdog(imei="868373070933504", deviceCount="1")
    run_watchdog(imei="868373070933041", deviceCount="1")
    run_watchdog(imei="868373070933470", deviceCount="1")
    run_watchdog(imei="868373070931292", deviceCount="1")
    run_watchdog(imei="868373070931433", deviceCount="1")
    run_watchdog(imei="868373070919792", deviceCount="1")
    run_watchdog(imei="868373070932761", deviceCount="1")
    CLIENT_ID = "brain-868373070931904"
    run_watchdog(imei="868373070931904", deviceCount="1")
    CLIENT_ID = "brain-868373070933736"
    run_watchdog(imei="868373070933736", deviceCount="1")
    CLIENT_ID = "brain-868373070930070"
    run_watchdog(imei="868373070930070", deviceCount="1")
    CLIENT_ID = "brain-868373070931524"
    run_watchdog(imei="868373070931524", deviceCount="1")
    CLIENT_ID = "brain-868373070933603"
    run_watchdog(imei="868373070933603", deviceCount="1")
    CLIENT_ID = "brain-868373070933025"
    run_watchdog(imei="868373070933025", deviceCount="1")
    CLIENT_ID = "brain-868373070932746"
    run_watchdog(imei="868373070932746", deviceCount="1")
    CLIENT_ID = "brain-868373070926888"
    run_watchdog(imei="868373070926888", deviceCount="1")
    CLIENT_ID = "brain-868373070933520"
    run_watchdog(imei="868373070933520", deviceCount="1")
    CLIENT_ID = "brain-868373070929031"
    run_watchdog(imei="868373070929031", deviceCount="1")
    CLIENT_ID = "brain-868373070932324"
    run_watchdog(imei="868373070932324", deviceCount="1")
    CLIENT_ID = "brain-868373070933041"
    run_watchdog(imei="868373070933041", deviceCount="1")
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373070905452"
    t = time.gmtime()
    data_timestamp = "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}Z".format(
        t[0], t[1], t[2], t[3], t[4], t[5])
    channel_1_mode_val = False
    channel_2_mode_val = False
    utility = run_data_deye3p(imei="868373070905452",
                              inverter_serial="2202269098")
    print(int(utility))
    run_heartbeat(
        imei="868373070905452",
        brainFirmware_version="1.1.1.0(β)",
        reboot_timestamp="2025-06-12T13:47:00Z",
        general_system_state=True,
        inverter_coms_state=True,
        relay_pair_state=True,
        devices_state=True,
        system_control_state=True,
        internal_state=True,
        relayFirmware_version="3.5.1.10(β)",
        gosolr_version="2.8.0.2(π)",
        edge_version="1.8.7",
        east_version="1.0.17",
        pair_version="2.0.5",
        manager_version="0.9.13",
        parsec_version="1.5.11",
        inverter_type="deye-3p",
        order_number="17085",
        inverter_sn="2202269098"
    )
    run_status(imei="868373070905452", network_type="wifi | 5ghz")
    utility = int(utility)
    if utility < 1000:
        channel_1_usage_val = round(random.uniform(0, 10), 1)/10
        channel_2_usage_val = round(random.uniform(0, 10), 1)/10
        channel_1_mode_val = False
        channel_2_mode_val = False
    if (utility >= 1000) & (utility <= 3000):
        channel_1_usage_val = utility-780
        channel_2_usage_val = round(random.uniform(4, 8), 1)/10
        channel_1_mode_val = True
        channel_2_mode_val = False
    if (utility >= 3001) & (utility <= 4000):
        channel_1_usage_val = utility-1780
        channel_2_usage_val = utility-channel_1_usage_val-1780
        channel_1_mode_val = True
        channel_2_mode_val = True
    if (utility >= 4001):
        channel_1_usage_val = utility/2 - 350
        channel_2_usage_val = utility/2 - 460
    run_relays(imei="868373070905452",
               relay_pair_state=True,
               channel_1_device="Geyser main",
               channel_2_device="Geyser spare",
               channel_3_device="disconnected",
               channel_4_device="disconnected",
               channel_1_mode=channel_1_mode_val,
               channel_2_mode=channel_2_mode_val,
               channel_3_mode=False,
               channel_4_mode=False,
               channel_1_usage=channel_1_usage_val,
               channel_2_usage=channel_2_usage_val,
               channel_3_usage=0,
               channel_4_usage=0)
    currentSecond = t[5]
    currentMinute = t[4]
    currentHour = t[3]+2
    # Channel 1: True between 6:00 and 18:59
    channel_1_state_val = 6 <= currentHour < 19

    # Channel 2: True between 7:00 and 16:59
    channel_2_state_val = 7 <= currentHour < 17

    # Channel 3 and 4: always False
    channel_3_state_val = False
    channel_4_state_val = False
    run_relaycontrol(imei="868373070930526",
                     channel_1_device="Geyser main",
                     channel_2_device="Geyser spare",
                     channel_3_device="disconnected",
                     channel_4_device="disconnected",
                     channel_1_state=channel_1_state_val,
                     channel_2_state=channel_2_state_val,
                     channel_3_state=channel_3_state_val,
                     channel_4_state=channel_4_state_val
                     )
    run_relaycontrol(imei="868373070905452",
                     channel_1_device="Geyser main",
                     channel_2_device="Geyser spare",
                     channel_3_device="disconnected",
                     channel_4_device="disconnected",
                     channel_1_state=channel_1_state_val,
                     channel_2_state=channel_2_state_val,
                     channel_3_state=channel_3_state_val,
                     channel_4_state=channel_4_state_val
                     )
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-learning-a-m"
    #run_2501142533()
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-learning-a-d"
    run_2211127459()
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-learning-s-j"
    run_2305053102()
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-learning-b-s"
    run_2209223588()
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-learning-d-d"
    run_2303250346()
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-learning-e-d"
    run_2106294063()
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-learning-n-t"
    run_2107199242()
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-learning-n-w"
    run_2304260750()
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-learning-r-s"
    run_2107057250()
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-learning-s-s"
    run_2107179045()
except Exception as e:
    print(str(e))

 # try:
 #    CLIENT_ID = "brain-learning-a-o"
 #    run_2501154134()
 # except Exception as e:
 #    print(str(e))

try:
    CLIENT_ID = "brain-learning-v-k"
    run_2304288455()
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373070915899"
    run_data(imei="868373070915899", inverter_serial="2306178933")
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373070932118"
    run_data(imei="868373070932118", inverter_serial="2304274172")
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373070930526"
    run_heartbeat(
        imei="868373070930526",
        brainFirmware_version="1.0.3.7",
        reboot_timestamp="2025-06-12T13:47:00Z",
        general_system_state=True,
        inverter_coms_state=True,
        relay_pair_state=True,
        devices_state=True,
        system_control_state=False,
        internal_state=True,
        relayFirmware_version="2.0.1.3",
        gosolr_version="2.6.39",
        edge_version="1.8.7",
        east_version="1.0.17",
        pair_version="2.0.5",
        manager_version="0.9.13",
        parsec_version="1.5.11",
        inverter_type="deye-1p",
        order_number="100315",
        inverter_sn="00000"
    )
    run_status(imei="868373070930526",
               network_type="wifi | 5g")
    run_relays(imei="868373070930526",
               relay_pair_state=True,
               channel_1_device="Geyser",
               channel_2_device="disconnected",
               channel_3_device="disconnected",
               channel_4_device="disconnected",
               channel_1_mode=False,
               channel_2_mode=False,
               channel_3_mode=False,
               channel_4_mode=False,
               channel_1_usage=round(random.uniform(0, 10), 1),
               channel_2_usage=0,
               channel_3_usage=0,
               channel_4_usage=0)
    currentSecond = t[5]
    currentMinute = t[4]
    currentHour = t[3]
    # Channel 1: True between 6:00 and 18:59
    channel_1_state_val = 6 <= currentHour < 19

    # Channel 2: True between 7:00 and 16:59
    channel_2_state_val = 7 <= currentHour < 17

    # Channel 3 and 4: always False
    channel_3_state_val = False
    channel_4_state_val = False
    run_relaycontrol(imei="868373070930526",
                     channel_1_device="Geyser",
                     channel_2_device="disconnected",
                     channel_3_device="disconnected",
                     channel_4_device="disconnected",
                     channel_1_state=channel_1_state_val,
                     channel_2_state=channel_2_state_val,
                     channel_3_state=channel_3_state_val,
                     channel_4_state=channel_4_state_val
                     )
    run_tariffs(imei="868373070930526",
                buy_tariff="0.00",
                sell_tariff="0.00")
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373070930070"
    imei_number = "868373070930070"
    run_heartbeat(
        imei=imei_number,
        brainFirmware_version="1.0.3.7",
        reboot_timestamp="2025-06-12T13:47:00Z",
        general_system_state=True,
        inverter_coms_state=True,
        relay_pair_state=True,
        devices_state=True,
        system_control_state=False,
        internal_state=True,
        relayFirmware_version="2.0.1.3",
        gosolr_version="2.6.39",
        edge_version="1.8.7",
        east_version="1.0.17",
        pair_version="2.0.5",
        manager_version="0.9.13",
        parsec_version="1.5.11",
        inverter_type="solis-1p",
        order_number="103744",
        inverter_sn="00000"
    )
    run_status(imei=imei_number,
               network_type="wifi | 5g")
    run_relays(imei=imei_number,
               relay_pair_state=True,
               channel_1_device="Geyser",
               channel_2_device="disconnected",
               channel_3_device="disconnected",
               channel_4_device="disconnected",
               channel_1_mode=False,
               channel_2_mode=False,
               channel_3_mode=False,
               channel_4_mode=False,
               channel_1_usage=round(random.uniform(0, 10), 1),
               channel_2_usage=0,
               channel_3_usage=0,
               channel_4_usage=0)
    run_relaycontrol(imei=imei_number,
                     channel_1_device="Geyser",
                     channel_2_device="disconnected",
                     channel_3_device="disconnected",
                     channel_4_device="disconnected",
                     channel_1_state=True,
                     channel_2_state=False,
                     channel_3_state=False,
                     channel_4_state=False
                     )
    run_tariffs(imei=imei_number,
                buy_tariff="0.00",
                sell_tariff="0.00")
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373070933041"
    imei_number = "868373070933041"
    run_heartbeat(
        imei=imei_number,
        brainFirmware_version="1.0.3.7",
        reboot_timestamp="2025-06-12T13:47:00Z",
        general_system_state=True,
        inverter_coms_state=True,
        relay_pair_state=True,
        devices_state=True,
        system_control_state=False,
        internal_state=True,
        relayFirmware_version="2.0.1.3",
        gosolr_version="2.6.39",
        edge_version="1.8.7",
        east_version="1.0.17",
        pair_version="2.0.5",
        manager_version="0.9.13",
        parsec_version="1.5.11",
        inverter_type="deye-1p",
        order_number="103744",
        inverter_sn="2304260750"
    )
    run_status(imei=imei_number,
               network_type="wifi | 5g")
    run_relays(imei=imei_number,
               relay_pair_state=True,
               channel_1_device="Geyser",
               channel_2_device="Swimming pool",
               channel_3_device="disconnected",
               channel_4_device="disconnected",
               channel_1_mode=False,
               channel_2_mode=False,
               channel_3_mode=False,
               channel_4_mode=False,
               channel_1_usage=round(random.uniform(0, 10), 1),
               channel_2_usage=round(random.uniform(0, 10), 1),
               channel_3_usage=0,
               channel_4_usage=0)
    run_relaycontrol(imei=imei_number,
                     channel_1_device="Geyser",
                     channel_2_device="Swimming pool",
                     channel_3_device="disconnected",
                     channel_4_device="disconnected",
                     channel_1_state=True,
                     channel_2_state=True,
                     channel_3_state=False,
                     channel_4_state=False
                     )
    run_tariffs(imei=imei_number,
                buy_tariff="5.77",
                sell_tariff="0.00")
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373070932258"
    imei_number = "868373070932258"
    run_heartbeat(
        imei=imei_number,
        brainFirmware_version="1.0.3.7",
        reboot_timestamp="2025-06-12T13:47:00Z",
        general_system_state=False,
        inverter_coms_state=True,
        relay_pair_state=True,
        devices_state=True,
        system_control_state=False,
        internal_state=True,
        relayFirmware_version="2.0.1.3",
        gosolr_version="2.6.39",
        edge_version="1.8.7",
        east_version="1.0.17",
        pair_version="2.0.5",
        manager_version="0.9.13",
        parsec_version="1.5.11",
        inverter_type="deye-1p",
        order_number="14864",
        inverter_sn="2107057250"
    )
    run_status(imei=imei_number,
               network_type="wifi | 5g")
    run_relays(imei=imei_number,
               relay_pair_state=True,
               channel_1_device="Geyser",
               channel_2_device="disconnected",
               channel_3_device="disconnected",
               channel_4_device="disconnected",
               channel_1_mode=False,
               channel_2_mode=False,
               channel_3_mode=False,
               channel_4_mode=False,
               channel_1_usage=round(random.uniform(0, 10), 1),
               channel_2_usage=round(random.uniform(0, 10), 1),
               channel_3_usage=0,
               channel_4_usage=0)
    run_relaycontrol(imei=imei_number,
                     channel_1_device="Geyser",
                     channel_2_device="Swimming pool",
                     channel_3_device="disconnected",
                     channel_4_device="disconnected",
                     channel_1_state=True,
                     channel_2_state=True,
                     channel_3_state=False,
                     channel_4_state=False
                     )
    run_tariffs(imei=imei_number,
                buy_tariff="5.47",
                sell_tariff="0.00")
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373070933116"
    run_heartbeat(
        imei="868373070933116",
        brainFirmware_version="1.1.1.0(β)",
        reboot_timestamp="2025-06-12T13:47:00Z",
        general_system_state=True,
        inverter_coms_state=True,
        relay_pair_state=True,
        devices_state=True,
        system_control_state=False,
        internal_state=True,
        relayFirmware_version="3.5.1.10(β)",
        gosolr_version="2.8.0.2(π)",
        edge_version="1.8.7",
        east_version="1.0.17",
        pair_version="2.0.5",
        manager_version="0.9.13",
        parsec_version="1.5.11",
        inverter_type="deye-1p",
        order_number="85229",
        inverter_sn="00000"
    )
    run_status(imei="868373070933116",
               network_type="wifi | 2.4ghz")
    run_relays(imei="868373070933116",
               relay_pair_state=True,
               channel_1_device="Geyser",
               channel_2_device="disconnected",
               channel_3_device="disconnected",
               channel_4_device="disconnected",
               channel_1_mode=False,
               channel_2_mode=False,
               channel_3_mode=False,
               channel_4_mode=False,
               channel_1_usage=round(random.uniform(2700, 3350), 1),
               channel_2_usage=0,
               channel_3_usage=0,
               channel_4_usage=0)
    run_relaycontrol(imei="868373070933116",
                     channel_1_device="Geyser",
                     channel_2_device="disconnected",
                     channel_3_device="disconnected",
                     channel_4_device="disconnected",
                     channel_1_state=True,
                     channel_2_state=False,
                     channel_3_state=False,
                     channel_4_state=False
                     )
    run_data(imei="868373070933116", inverter_serial="2304256477")
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373070932720"
    run_heartbeat(
        imei="868373070932720",
        brainFirmware_version="1.1.1.0(β)",
        reboot_timestamp="2025-05-29T08:37:00Z",
        general_system_state=True,
        inverter_coms_state=True,
        relay_pair_state=True,
        devices_state=True,
        system_control_state=False,
        internal_state=True,
        relayFirmware_version="3.5.1.10(β)",
        gosolr_version="2.8.0.2(π)",
        edge_version="1.8.7",
        east_version="1.0.17",
        pair_version="2.0.5",
        manager_version="0.9.13",
        parsec_version="1.5.11",
        inverter_type="deye-1p",
        order_number="90865",
        inverter_sn="2303200214"
    )
    run_status(imei="868373070932720",
               network_type="wifi | 2.4ghz")
    run_relays(imei="868373070932720",
               relay_pair_state=True,
               channel_1_device="Geyser",
               channel_2_device="disconnected",
               channel_3_device="disconnected",
               channel_4_device="disconnected",
               channel_1_mode=False,
               channel_2_mode=False,
               channel_3_mode=False,
               channel_4_mode=False,
               channel_1_usage=round(random.uniform(2800, 3200), 1),
               channel_2_usage=0,
               channel_3_usage=0,
               channel_4_usage=0)
    run_relaycontrol(imei="868373070932720",
                     channel_1_device="Geyser",
                     channel_2_device="disconnected",
                     channel_3_device="disconnected",
                     channel_4_device="disconnected",
                     channel_1_state=True,
                     channel_2_state=False,
                     channel_3_state=False,
                     channel_4_state=False
                     )
    run_data(imei="868373070932720", inverter_serial="2303200214")
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373070929502"
    run_data(imei="868373070929502", inverter_serial="2305126005")
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373070932324"
    run_data(imei="868373070932324", inverter_serial="2211166235")
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373070932423"
    run_heartbeat(
        imei="868373070932423",
        brainFirmware_version="1.0.3.7",
        reboot_timestamp="2025-05-29T08:38:00Z",
        general_system_state=True,
        inverter_coms_state=True,
        relay_pair_state=True,
        devices_state=True,
        system_control_state=False,
        internal_state=True,
        relayFirmware_version="2.0.1.3",
        gosolr_version="2.6.39",
        edge_version="1.8.7",
        east_version="1.0.17",
        pair_version="2.0.5",
        manager_version="0.9.13",
        parsec_version="1.5.11",
        inverter_type="deye-1p",
        order_number="88764",
        inverter_sn="2304194916"
    )
    run_status(imei="868373070932423",
               network_type="wifi | 5g")
    run_relays(imei="868373070932423",
               relay_pair_state=True,
               channel_1_device="Geyser",
               channel_2_device="disconnected",
               channel_3_device="disconnected",
               channel_4_device="disconnected",
               channel_1_mode=False,
               channel_2_mode=False,
               channel_3_mode=False,
               channel_4_mode=False,
               channel_1_usage=round(random.uniform(0, 10), 1),
               channel_2_usage=0,
               channel_3_usage=0,
               channel_4_usage=0)
    run_relaycontrol(imei="868373070932423",
                     channel_1_device="Geyser",
                     channel_2_device="disconnected",
                     channel_3_device="disconnected",
                     channel_4_device="disconnected",
                     channel_1_state=True,
                     channel_2_state=False,
                     channel_3_state=False,
                     channel_4_state=False
                     )
    run_tariffs(imei="868373070932423",
                buy_tariff="0.00",
                sell_tariff="0.00")
    run_data(imei="868373070932423", inverter_serial="2304194916")
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373070932100"
    run_heartbeat(
        imei="868373070932100",
        brainFirmware_version="1.0.3.7",
        reboot_timestamp="2025-06-12T13:47:00Z",
        general_system_state=True,
        inverter_coms_state=True,
        relay_pair_state=True,
        devices_state=True,
        system_control_state=False,
        internal_state=True,
        relayFirmware_version="2.0.1.3",
        gosolr_version="2.6.39",
        edge_version="1.8.7",
        east_version="1.0.17",
        pair_version="2.0.5",
        manager_version="0.9.13",
        parsec_version="1.5.11",
        inverter_type="deye-1p",
        order_number="95667",
        inverter_sn="00000"
    )
    run_status(imei="868373070932100",
               network_type="wifi | 2g")
    run_relays(imei="868373070932100",
               relay_pair_state=True,
               channel_1_device="Geyser",
               channel_2_device="disconnected",
               channel_3_device="disconnected",
               channel_4_device="disconnected",
               channel_1_mode=False,
               channel_2_mode=False,
               channel_3_mode=False,
               channel_4_mode=False,
               channel_1_usage=round(random.uniform(0, 10), 1),
               channel_2_usage=0,
               channel_3_usage=0,
               channel_4_usage=0)
    run_relaycontrol(imei="868373070932100",
                     channel_1_device="Geyser",
                     channel_2_device="disconnected",
                     channel_3_device="disconnected",
                     channel_4_device="disconnected",
                     channel_1_state=True,
                     channel_2_state=False,
                     channel_3_state=False,
                     channel_4_state=False
                     )
    run_tariffs(imei="868373070932100",
                buy_tariff="0.00",
                sell_tariff="0.00")
    run_data(imei="868373070932100", inverter_serial="2211137771")
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373070932480"
    run_heartbeat(
        imei="868373070932480",
        brainFirmware_version="1.1.1.0(β)",
        reboot_timestamp="2025-06-12T13:47:00Z",
        general_system_state=True,
        inverter_coms_state=True,
        relay_pair_state=True,
        devices_state=True,
        system_control_state=True,
        internal_state=True,
        relayFirmware_version="3.5.1.10(β)",
        gosolr_version="2.8.0.2(π)",
        edge_version="1.8.7",
        east_version="1.0.17",
        pair_version="2.0.5",
        manager_version="0.9.13",
        parsec_version="1.5.11",
        inverter_type="deye-1p",
        order_number="27104",
        inverter_sn="2207306068"
    )
    run_status(imei="868373070932480",
               network_type="mobile")
    run_relays(imei="868373070932480",
               relay_pair_state=True,
               channel_1_device="Geyser",
               channel_2_device="disconnected",
               channel_3_device="disconnected",
               channel_4_device="disconnected",
               channel_1_mode=False,
               channel_2_mode=False,
               channel_3_mode=False,
               channel_4_mode=False,
               channel_1_usage=round(random.uniform(3000, 3510), 1),
               channel_2_usage=0,
               channel_3_usage=0,
               channel_4_usage=0)
    run_relaycontrol(imei="868373070932480",
                     channel_1_device="Geyser",
                     channel_2_device="disconnected",
                     channel_3_device="disconnected",
                     channel_4_device="disconnected",
                     channel_1_state=True,
                     channel_2_state=False,
                     channel_3_state=False,
                     channel_4_state=False
                     )
    run_data(imei="868373070932480", inverter_serial="2207306068")
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373070931508"
    run_heartbeat(
        imei="868373070931508",
        brainFirmware_version="1.1.1.0(β)",
        reboot_timestamp="2025-06-12T13:47:00Z",
        general_system_state=True,
        inverter_coms_state=True,
        relay_pair_state=True,
        devices_state=True,
        system_control_state=True,
        internal_state=True,
        relayFirmware_version="3.5.1.10(β)",
        gosolr_version="2.8.0.2(π)",
        edge_version="1.8.7",
        east_version="1.0.17",
        pair_version="2.0.5",
        manager_version="0.9.13",
        parsec_version="1.5.11",
        inverter_type="deye-1p",
        order_number="31953",
        inverter_sn="2208266617"
    )
    run_status(imei="868373070931508",
               network_type="wifi | 5ghz")
    run_relays(imei="868373070931508",
               relay_pair_state=True,
               channel_1_device="Geyser",
               channel_2_device="Swimming pool",
               channel_3_device="disconnected",
               channel_4_device="disconnected",
               channel_1_mode=False,
               channel_2_mode=False,
               channel_3_mode=False,
               channel_4_mode=False,
               channel_1_usage=round(random.uniform(2100, 3100), 1),
               channel_2_usage=0,
               channel_3_usage=0,
               channel_4_usage=0)
    run_relaycontrol(imei="868373070931508",
                     channel_1_device="Geyser",
                     channel_2_device="Swimming pool",
                     channel_3_device="disconnected",
                     channel_4_device="disconnected",
                     channel_1_state=True,
                     channel_2_state=False,
                     channel_3_state=False,
                     channel_4_state=False
                     )
    run_data(imei="868373070931508", inverter_serial="2208266617")
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373070931524"
    run_heartbeat(
        imei="868373070931524",
        brainFirmware_version="1.0.3.7",
        reboot_timestamp="2025-06-12T13:47:00Z",
        general_system_state=True,
        inverter_coms_state=True,
        relay_pair_state=True,
        devices_state=True,
        system_control_state=False,
        internal_state=True,
        relayFirmware_version="2.0.1.3",
        gosolr_version="2.6.39",
        edge_version="1.8.7",
        east_version="1.0.17",
        pair_version="2.0.5",
        manager_version="0.9.13",
        parsec_version="1.5.11",
        inverter_type="deye-1p",
        order_number="17500",
        inverter_sn="2208068231"
    )
    run_status(imei="868373070931524",
               network_type="mobile")
    run_relays(imei="868373070931524",
               relay_pair_state=True,
               channel_1_device="Geyser",
               channel_2_device="disconnected",
               channel_3_device="disconnected",
               channel_4_device="disconnected",
               channel_1_mode=False,
               channel_2_mode=False,
               channel_3_mode=False,
               channel_4_mode=False,
               channel_1_usage=round(random.uniform(0, 10), 1),
               channel_2_usage=0,
               channel_3_usage=0,
               channel_4_usage=0)
    run_relaycontrol(imei="868373070931524",
                     channel_1_device="Geyser",
                     channel_2_device="disconnected",
                     channel_3_device="disconnected",
                     channel_4_device="disconnected",
                     channel_1_state=True,
                     channel_2_state=False,
                     channel_3_state=False,
                     channel_4_state=False
                     )
    run_tariffs(imei="868373070931524",
                buy_tariff="0.00",
                sell_tariff="0.00")
    run_data(imei="868373070931524", inverter_serial="2208068231")
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373070926888"
    run_heartbeat(
        imei="868373070926888",
        brainFirmware_version="1.0.3.7",
        reboot_timestamp="2025-06-12T13:47:00Z",
        general_system_state=False,
        inverter_coms_state=False,
        relay_pair_state=True,
        devices_state=False,
        system_control_state=False,
        internal_state=True,
        relayFirmware_version="2.0.1.3",
        gosolr_version="2.6.39",
        edge_version="1.8.7",
        east_version="1.0.17",
        pair_version="2.0.5",
        manager_version="0.9.13",
        parsec_version="1.5.11",
        inverter_type="deye-1p",
        order_number="102617",
        inverter_sn="2211113009"
    )
    run_status(imei="868373070926888",
               network_type="mobile")
    run_relays(imei="868373070926888",
               relay_pair_state=True,
               channel_1_device="Geyser",
               channel_2_device="disconnected",
               channel_3_device="disconnected",
               channel_4_device="disconnected",
               channel_1_mode=False,
               channel_2_mode=False,
               channel_3_mode=False,
               channel_4_mode=False,
               channel_1_usage=round(random.uniform(0, 10), 1),
               channel_2_usage=0,
               channel_3_usage=0,
               channel_4_usage=0)
    run_relaycontrol(imei="868373070926888",
                     channel_1_device="Geyser",
                     channel_2_device="disconnected",
                     channel_3_device="disconnected",
                     channel_4_device="disconnected",
                     channel_1_state=True,
                     channel_2_state=False,
                     channel_3_state=False,
                     channel_4_state=False
                     )
    run_tariffs(imei="868373070926888",
                buy_tariff="0.00",
                sell_tariff="0.00")
    run_data(imei="868373070926888", inverter_serial="2211113009")
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373070931938"
    run_heartbeat(
        imei="868373070931938",
        brainFirmware_version="1.0.3.7",
        reboot_timestamp="2025-06-12T13:47:00Z",
        general_system_state=True,
        inverter_coms_state=True,
        relay_pair_state=True,
        devices_state=True,
        system_control_state=False,
        internal_state=True,
        relayFirmware_version="2.0.1.3",
        gosolr_version="2.6.39",
        edge_version="1.8.7",
        east_version="1.0.17",
        pair_version="2.0.5",
        manager_version="0.9.13",
        parsec_version="1.5.11",
        inverter_type="deye-1p",
        order_number="39418",
        inverter_sn="00000"
    )
    run_status(imei="868373070931938",
               network_type="mobile")
    run_relays(imei="868373070931938",
               relay_pair_state=True,
               channel_1_device="Geyser",
               channel_2_device="disconnected",
               channel_3_device="disconnected",
               channel_4_device="disconnected",
               channel_1_mode=False,
               channel_2_mode=False,
               channel_3_mode=False,
               channel_4_mode=False,
               channel_1_usage=round(random.uniform(0, 10), 1),
               channel_2_usage=0,
               channel_3_usage=0,
               channel_4_usage=0)
    run_relaycontrol(imei="868373070931938",
                     channel_1_device="Geyser",
                     channel_2_device="disconnected",
                     channel_3_device="disconnected",
                     channel_4_device="disconnected",
                     channel_1_state=True,
                     channel_2_state=False,
                     channel_3_state=False,
                     channel_4_state=False
                     )
    run_tariffs(imei="868373070931938",
                buy_tariff="0.00",
                sell_tariff="0.00")
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373070932217"
    run_heartbeat(
        imei="868373070932217",
        brainFirmware_version="1.0.3.7",
        reboot_timestamp="2025-06-12T13:47:00Z",
        general_system_state=True,
        inverter_coms_state=True,
        relay_pair_state=True,
        devices_state=True,
        system_control_state=False,
        internal_state=True,
        relayFirmware_version="2.0.1.3",
        gosolr_version="2.6.39",
        edge_version="1.8.7",
        east_version="1.0.17",
        pair_version="2.0.5",
        manager_version="0.9.13",
        parsec_version="1.5.11",
        inverter_type="deye-1p",
        order_number="84432",
        inverter_sn="2306092238"
    )
    run_status(imei="868373070932217",
               network_type="wifi | 2g")
    run_relays(imei="868373070932217",
               relay_pair_state=True,
               channel_1_device="Geyser",
               channel_2_device="disconnected",
               channel_3_device="disconnected",
               channel_4_device="disconnected",
               channel_1_mode=False,
               channel_2_mode=False,
               channel_3_mode=False,
               channel_4_mode=False,
               channel_1_usage=round(random.uniform(0, 10), 1),
               channel_2_usage=0,
               channel_3_usage=0,
               channel_4_usage=0)
    run_relaycontrol(imei="868373070932217",
                     channel_1_device="Geyser",
                     channel_2_device="disconnected",
                     channel_3_device="disconnected",
                     channel_4_device="disconnected",
                     channel_1_state=True,
                     channel_2_state=False,
                     channel_3_state=False,
                     channel_4_state=False
                     )
    run_tariffs(imei="868373070932217",
                buy_tariff="5.16",
                sell_tariff="0.00")
    run_data(imei="868373070932217", inverter_serial="2306092238")
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373070930864"
    run_heartbeat(
        imei="868373070930864",
        brainFirmware_version="1.0.3.7",
        reboot_timestamp="2025-06-12T13:47:00Z",
        general_system_state=True,
        inverter_coms_state=True,
        relay_pair_state=True,
        devices_state=True,
        system_control_state=False,
        internal_state=True,
        relayFirmware_version="2.0.1.3",
        gosolr_version="2.6.39",
        edge_version="1.8.7",
        east_version="1.0.17",
        pair_version="2.0.5",
        manager_version="0.9.13",
        parsec_version="1.5.11",
        inverter_type="deye-1p",
        order_number="100035",
        inverter_sn="2305058271"
    )
    run_status(imei="868373070930864",
               network_type="mobile")
    run_relays(imei="868373070930864",
               relay_pair_state=True,
               channel_1_device="Geyser",
               channel_2_device="disconnected",
               channel_3_device="disconnected",
               channel_4_device="disconnected",
               channel_1_mode=False,
               channel_2_mode=False,
               channel_3_mode=False,
               channel_4_mode=False,
               channel_1_usage=round(random.uniform(0, 10), 1),
               channel_2_usage=0,
               channel_3_usage=0,
               channel_4_usage=0)
    run_relaycontrol(imei="868373070930864",
                     channel_1_device="Geyser",
                     channel_2_device="disconnected",
                     channel_3_device="disconnected",
                     channel_4_device="disconnected",
                     channel_1_state=True,
                     channel_2_state=False,
                     channel_3_state=False,
                     channel_4_state=False
                     )
    run_tariffs(imei="868373070930864",
                buy_tariff="5.21",
                sell_tariff="0.00")
    run_data(imei="868373070930864", inverter_serial="2305058271")
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373070931391"
    run_heartbeat(
        imei="868373070931391",
        brainFirmware_version="1.0.3.7",
        reboot_timestamp="2025-06-12T13:47:00Z",
        general_system_state=True,
        inverter_coms_state=True,
        relay_pair_state=True,
        devices_state=True,
        system_control_state=False,
        internal_state=True,
        relayFirmware_version="2.0.1.3",
        gosolr_version="2.6.39",
        edge_version="1.8.7",
        east_version="1.0.17",
        pair_version="2.0.5",
        manager_version="0.9.13",
        parsec_version="1.5.11",
        inverter_type="deye-1p",
        order_number="14902",
        inverter_sn="2108109493"
    )
    run_status(imei="868373070931391",
               network_type="mobile")
    run_relays(imei="868373070931391",
               relay_pair_state=True,
               channel_1_device="Geyser",
               channel_2_device="disconnected",
               channel_3_device="disconnected",
               channel_4_device="disconnected",
               channel_1_mode=False,
               channel_2_mode=False,
               channel_3_mode=False,
               channel_4_mode=False,
               channel_1_usage=round(random.uniform(0, 10), 1),
               channel_2_usage=0,
               channel_3_usage=0,
               channel_4_usage=0)
    run_relaycontrol(imei="868373070931391",
                     channel_1_device="Geyser",
                     channel_2_device="disconnected",
                     channel_3_device="disconnected",
                     channel_4_device="disconnected",
                     channel_1_state=True,
                     channel_2_state=False,
                     channel_3_state=False,
                     channel_4_state=False
                     )
    run_tariffs(imei="868373070931391",
                buy_tariff="0.00",
                sell_tariff="0.00")
    run_data(imei="868373070931391", inverter_serial="2108109493")
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373070934213"
    run_heartbeat(
        imei="868373070934213",
        brainFirmware_version="1.1.1.0(β)",
        reboot_timestamp="2025-08-26T13:47:00Z",
        general_system_state=True,
        inverter_coms_state=True,
        relay_pair_state=True,
        devices_state=True,
        system_control_state=True,
        internal_state=True,
        relayFirmware_version="3.5.1.10(β)",
        gosolr_version="2.8.0.2(π)",
        edge_version="2.9.8",
        east_version="1.8.22",
        pair_version="3.2.5",
        manager_version="0.9.15",
        parsec_version="1.5.11",
        inverter_type="deye-1p",
        order_number="54490",
        inverter_sn="2305102553"
    )
    run_status(imei="868373070934213",
               network_type="wifi | 2g")
    run_relays(imei="868373070934213",
               relay_pair_state=True,
               channel_1_device="Geyser 1",
               channel_2_device="Geyser 2",
               channel_3_device="Swimming pool",
               channel_4_device="disconnected",
               channel_1_mode=False,
               channel_2_mode=False,
               channel_3_mode=False,
               channel_4_mode=False,
               channel_1_usage=round(random.uniform(2000, 3500), 1),
               channel_2_usage=round(random.uniform(3100, 3400), 1),
               channel_3_usage=round(random.uniform(800, 1000), 1),
               channel_4_usage=0)
    run_relaycontrol(imei="868373070934213",
                     channel_1_device="Geyser 1",
                     channel_2_device="Geyser 2",
                     channel_3_device="Swimming pool",
                     channel_4_device="disconnected",
                     channel_1_state=True,
                     channel_2_state=True,
                     channel_3_state=True,
                     channel_4_state=False
                     )
    run_data(imei="868373070934213", inverter_serial="2305102553")
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373070930674"
    run_heartbeat(
        imei="868373070930674",
        brainFirmware_version="1.0.3.7",
        reboot_timestamp="2025-06-12T13:47:00Z",
        general_system_state=True,
        inverter_coms_state=True,
        relay_pair_state=True,
        devices_state=True,
        system_control_state=False,
        internal_state=True,
        relayFirmware_version="2.0.1.3",
        gosolr_version="2.6.39",
        edge_version="1.8.7",
        east_version="1.0.17",
        pair_version="2.0.5",
        manager_version="0.9.13",
        parsec_version="1.5.11",
        inverter_type="deye-1p",
        order_number="103570",
        inverter_sn="2501106322"
    )
    run_status(imei="868373070930674",
               network_type="wifi | 2g")
    run_relays(imei="868373070930674",
               relay_pair_state=True,
               channel_1_device="Geyser",
               channel_2_device="disconnected",
               channel_3_device="disconnected",
               channel_4_device="disconnected",
               channel_1_mode=False,
               channel_2_mode=False,
               channel_3_mode=False,
               channel_4_mode=False,
               channel_1_usage=round(random.uniform(0, 10), 1),
               channel_2_usage=0,
               channel_3_usage=0,
               channel_4_usage=0)
    run_relaycontrol(imei="868373070930674",
                     channel_1_device="Geyser",
                     channel_2_device="disconnected",
                     channel_3_device="disconnected",
                     channel_4_device="disconnected",
                     channel_1_state=True,
                     channel_2_state=False,
                     channel_3_state=False,
                     channel_4_state=False
                     )
    run_tariffs(imei="868373070930674",
                buy_tariff="0.00",
                sell_tariff="0.00")
    run_data(imei="868373070930674", inverter_serial="2501106322")
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868379070929981"
    run_heartbeat(
        imei="868379070929981",
        brainFirmware_version="1.0.3.7",
        reboot_timestamp="2025-06-12T13:47:00Z",
        general_system_state=True,
        inverter_coms_state=True,
        relay_pair_state=True,
        devices_state=True,
        system_control_state=False,
        internal_state=True,
        relayFirmware_version="2.0.1.3",
        gosolr_version="2.6.39",
        edge_version="1.8.7",
        east_version="1.0.17",
        pair_version="2.0.5",
        manager_version="0.9.13",
        parsec_version="1.5.11",
        inverter_type="solis-1p",
        order_number="103570",
        inverter_sn="1031170238250200"
    )
    run_status(imei="868379070929981",
               network_type="wifi | 5g")
    run_relays(imei="868379070929981",
               relay_pair_state=True,
               channel_1_device="Geyser",
               channel_2_device="disconnected",
               channel_3_device="disconnected",
               channel_4_device="disconnected",
               channel_1_mode=False,
               channel_2_mode=False,
               channel_3_mode=False,
               channel_4_mode=False,
               channel_1_usage=round(random.uniform(0, 10), 1),
               channel_2_usage=0,
               channel_3_usage=0,
               channel_4_usage=0)
    run_relaycontrol(imei="868379070929981",
                     channel_1_device="Geyser",
                     channel_2_device="disconnected",
                     channel_3_device="disconnected",
                     channel_4_device="disconnected",
                     channel_1_state=True,
                     channel_2_state=False,
                     channel_3_state=False,
                     channel_4_state=False
                     )
    run_tariffs(imei="868379070929981",
                buy_tariff="5.74",
                sell_tariff="0.00")
    run_data(imei="868379070929981", inverter_serial="1031170238250200")
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373070916640"
    run_heartbeat(
        imei="868373070916640",
        brainFirmware_version="1.0.3.7",
        reboot_timestamp="2025-06-12T13:47:00Z",
        general_system_state=True,
        inverter_coms_state=True,
        relay_pair_state=True,
        devices_state=True,
        system_control_state=False,
        internal_state=True,
        relayFirmware_version="2.0.1.3",
        gosolr_version="2.6.39",
        edge_version="1.8.7",
        east_version="1.0.17",
        pair_version="2.0.5",
        manager_version="0.9.13",
        parsec_version="1.5.11",
        inverter_type="solis-1p",
        order_number="103400",
        inverter_sn="1031180245130040"
    )
    run_status(imei="868373070916640",
               network_type="wifi | 2g")
    run_relays(imei="868373070916640",
               relay_pair_state=True,
               channel_1_device="Geyser",
               channel_2_device="disconnected",
               channel_3_device="disconnected",
               channel_4_device="disconnected",
               channel_1_mode=False,
               channel_2_mode=False,
               channel_3_mode=False,
               channel_4_mode=False,
               channel_1_usage=round(random.uniform(0, 10), 1),
               channel_2_usage=0,
               channel_3_usage=0,
               channel_4_usage=0)
    run_relaycontrol(imei="868373070916640",
                     channel_1_device="Geyser",
                     channel_2_device="disconnected",
                     channel_3_device="disconnected",
                     channel_4_device="disconnected",
                     channel_1_state=True,
                     channel_2_state=False,
                     channel_3_state=False,
                     channel_4_state=False
                     )
    run_tariffs(imei="868373070916640",
                buy_tariff="4.92",
                sell_tariff="0.00")
    run_data(imei="868373070916640", inverter_serial="1031180245130040")
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373070935657"
    run_heartbeat(
        imei="868373070935657",
        brainFirmware_version="1.0.3.7",
        reboot_timestamp="2025-06-12T13:47:00Z",
        general_system_state=True,
        inverter_coms_state=True,
        relay_pair_state=True,
        devices_state=True,
        system_control_state=False,
        internal_state=True,
        relayFirmware_version="2.0.1.3",
        gosolr_version="2.6.39",
        edge_version="1.8.7",
        east_version="1.0.17",
        pair_version="2.0.5",
        manager_version="0.9.13",
        parsec_version="1.5.11",
        inverter_type="deye-1p",
        order_number="103654",
        inverter_sn="2303068682"
    )
    run_status(imei="868373070935657",
               network_type="mobile")
    run_relays(imei="868373070935657",
               relay_pair_state=True,
               channel_1_device="Geyser",
               channel_2_device="disconnected",
               channel_3_device="disconnected",
               channel_4_device="disconnected",
               channel_1_mode=False,
               channel_2_mode=False,
               channel_3_mode=False,
               channel_4_mode=False,
               channel_1_usage=round(random.uniform(0, 10), 1),
               channel_2_usage=0,
               channel_3_usage=0,
               channel_4_usage=0)
    run_relaycontrol(imei="868373070935657",
                     channel_1_device="Geyser",
                     channel_2_device="disconnected",
                     channel_3_device="disconnected",
                     channel_4_device="disconnected",
                     channel_1_state=True,
                     channel_2_state=False,
                     channel_3_state=False,
                     channel_4_state=False
                     )
    run_tariffs(imei="868373070935657",
                buy_tariff="4.96",
                sell_tariff="0.00")
    run_data(imei="868373070935657", inverter_serial="2303068682")
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373070932522"
    imei_number = "868373070932522"
    inverter_serialn = "2306090282"
    run_data(imei=imei_number, inverter_serial=inverter_serialn)
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373070933470"
    imei_number = "868373070933470"
    inverter_serialn = "2304214590"
    run_data(imei=imei_number, inverter_serial=inverter_serialn)
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373070931292"
    imei_number = "868373070931292"
    inverter_serialn = "2305066035"
    run_data(imei=imei_number, inverter_serial=inverter_serialn)
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373070931433"
    imei_number = "868373070931433"
    inverter_serialn = "2211236035"
    run_data(imei=imei_number, inverter_serial=inverter_serialn)
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373070919792"
    imei_number = "868373070919792"
    inverter_serialn = "2304254491"
    run_data(imei=imei_number, inverter_serial=inverter_serialn)
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373070932761"
    imei_number = "868373070932761"
    inverter_serialn = "2303078668"
    run_heartbeat(
        imei=imei_number,
        brainFirmware_version="1.0.3.7",
        reboot_timestamp="2025-06-12T13:47:00Z",
        general_system_state=True,
        inverter_coms_state=True,
        relay_pair_state=True,
        devices_state=True,
        system_control_state=False,
        internal_state=True,
        relayFirmware_version="2.0.1.3",
        gosolr_version="2.6.39",
        edge_version="1.8.7",
        east_version="1.0.17",
        pair_version="2.0.5",
        manager_version="0.9.13",
        parsec_version="1.5.11",
        inverter_type="deye-1p",
        order_number="71068",
        inverter_sn=inverter_serialn
    )
    run_data(imei=imei_number, inverter_serial=inverter_serialn)
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373070932571"
    imei_number = "868373070932571"
    inverter_serialn = "2306044729"
    run_data(imei=imei_number, inverter_serial=inverter_serialn)
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373070930070"
    run_heartbeat(
        imei="868373070930070",
        brainFirmware_version="1.0.3.7",
        reboot_timestamp="2025-06-12T13:47:00Z",
        general_system_state=True,
        inverter_coms_state=True,
        relay_pair_state=True,
        devices_state=True,
        system_control_state=False,
        internal_state=True,
        relayFirmware_version="2.0.1.3",
        gosolr_version="2.6.39",
        edge_version="1.8.7",
        east_version="1.0.17",
        pair_version="2.0.5",
        manager_version="0.9.13",
        parsec_version="1.5.11",
        inverter_type="solis-1p",
        order_number="103744",
        inverter_sn="1031170238130260"
    )
    run_status(imei="868373070930070",
               network_type="mobile")
    run_relays(imei="868373070930070",
               relay_pair_state=True,
               channel_1_device="Geyser",
               channel_2_device="disconnected",
               channel_3_device="disconnected",
               channel_4_device="disconnected",
               channel_1_mode=False,
               channel_2_mode=False,
               channel_3_mode=False,
               channel_4_mode=False,
               channel_1_usage=round(random.uniform(0, 10), 1),
               channel_2_usage=0,
               channel_3_usage=0,
               channel_4_usage=0)
    run_relaycontrol(imei="868373070930070",
                     channel_1_device="Geyser",
                     channel_2_device="disconnected",
                     channel_3_device="disconnected",
                     channel_4_device="disconnected",
                     channel_1_state=True,
                     channel_2_state=False,
                     channel_3_state=False,
                     channel_4_state=False
                     )
    run_tariffs(imei="868373070930070",
                buy_tariff="5.99",
                sell_tariff="0.00")
    run_data(imei="868373070930070", inverter_serial="1031170238130260")
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373070929411"
    run_heartbeat(
        imei="868373070929411",
        brainFirmware_version="1.0.3.7",
        reboot_timestamp="2025-06-12T13:47:00Z",
        general_system_state=True,
        inverter_coms_state=True,
        relay_pair_state=True,
        devices_state=True,
        system_control_state=False,
        internal_state=True,
        relayFirmware_version="2.0.1.3",
        gosolr_version="2.6.39",
        edge_version="1.8.7",
        east_version="1.0.17",
        pair_version="2.0.5",
        manager_version="0.9.13",
        parsec_version="1.5.11",
        inverter_type="deye-1p",
        order_number="103678",
        inverter_sn="2206167115"
    )
    run_status(imei="868373070929411",
               network_type="wifi | 2g")
    run_relays(imei="868373070929411",
               relay_pair_state=True,
               channel_1_device="Geyser",
               channel_2_device="disconnected",
               channel_3_device="disconnected",
               channel_4_device="disconnected",
               channel_1_mode=False,
               channel_2_mode=False,
               channel_3_mode=False,
               channel_4_mode=False,
               channel_1_usage=round(random.uniform(0, 10), 1),
               channel_2_usage=0,
               channel_3_usage=0,
               channel_4_usage=0)
    run_relaycontrol(imei="868373070929411",
                     channel_1_device="Geyser",
                     channel_2_device="disconnected",
                     channel_3_device="disconnected",
                     channel_4_device="disconnected",
                     channel_1_state=True,
                     channel_2_state=False,
                     channel_3_state=False,
                     channel_4_state=False
                     )
    run_tariffs(imei="868373070929411",
                buy_tariff="0.00",
                sell_tariff="0.00")
    run_data(imei="868373070929411", inverter_serial="2206167115")
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373070921012"
    run_heartbeat(
        imei="868373070921012",
        brainFirmware_version="1.0.3.7",
        reboot_timestamp="2025-06-12T13:47:00Z",
        general_system_state=True,
        inverter_coms_state=True,
        relay_pair_state=True,
        devices_state=True,
        system_control_state=False,
        internal_state=True,
        relayFirmware_version="2.0.1.3",
        gosolr_version="2.6.39",
        edge_version="1.8.7",
        east_version="1.0.17",
        pair_version="2.0.5",
        manager_version="0.9.13",
        parsec_version="1.5.11",
        inverter_type="deye-1p",
        order_number="103759",
        inverter_sn="2304184134"
    )
    run_status(imei="868373070921012",
               network_type="wifi | 5g")
    run_relays(imei="868373070921012",
               relay_pair_state=True,
               channel_1_device="Geyser",
               channel_2_device="disconnected",
               channel_3_device="disconnected",
               channel_4_device="disconnected",
               channel_1_mode=False,
               channel_2_mode=False,
               channel_3_mode=False,
               channel_4_mode=False,
               channel_1_usage=round(random.uniform(0, 10), 1),
               channel_2_usage=0,
               channel_3_usage=0,
               channel_4_usage=0)
    run_relaycontrol(imei="868373070921012",
                     channel_1_device="Geyser",
                     channel_2_device="disconnected",
                     channel_3_device="disconnected",
                     channel_4_device="disconnected",
                     channel_1_state=True,
                     channel_2_state=False,
                     channel_3_state=False,
                     channel_4_state=False
                     )
    run_tariffs(imei="868373070921012",
                buy_tariff="0.00",
                sell_tariff="0.00")
    run_data(imei="868373070921012", inverter_serial="2304184134")
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373070921095"
    run_heartbeat(
        imei="868373070921095",
        brainFirmware_version="1.0.3.7",
        reboot_timestamp="2025-06-12T13:47:00Z",
        general_system_state=True,
        inverter_coms_state=True,
        relay_pair_state=True,
        devices_state=True,
        system_control_state=False,
        internal_state=True,
        relayFirmware_version="2.0.1.3",
        gosolr_version="2.6.39",
        edge_version="1.8.7",
        east_version="1.0.17",
        pair_version="2.0.5",
        manager_version="0.9.13",
        parsec_version="1.5.11",
        inverter_type="deye-1p",
        order_number="102576",
        inverter_sn="2501124049"
    )
    run_status(imei="868373070921095",
               network_type="mobile")
    run_relays(imei="868373070921095",
               relay_pair_state=True,
               channel_1_device="Geyser",
               channel_2_device="disconnected",
               channel_3_device="disconnected",
               channel_4_device="disconnected",
               channel_1_mode=False,
               channel_2_mode=False,
               channel_3_mode=False,
               channel_4_mode=False,
               channel_1_usage=round(random.uniform(0, 10), 1),
               channel_2_usage=0,
               channel_3_usage=0,
               channel_4_usage=0)
    run_relaycontrol(imei="868373070921095",
                     channel_1_device="Geyser",
                     channel_2_device="disconnected",
                     channel_3_device="disconnected",
                     channel_4_device="disconnected",
                     channel_1_state=True,
                     channel_2_state=False,
                     channel_3_state=False,
                     channel_4_state=False
                     )
    run_tariffs(imei="868373070921095",
                buy_tariff="0.00",
                sell_tariff="0.00")
    run_data(imei="868373070921095", inverter_serial="2501124049")
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373070933363"
    run_heartbeat(
        imei="868373070933363",
        brainFirmware_version="1.0.3.7",
        reboot_timestamp="2025-06-12T13:47:00Z",
        general_system_state=True,
        inverter_coms_state=True,
        relay_pair_state=True,
        devices_state=True,
        system_control_state=False,
        internal_state=True,
        relayFirmware_version="2.0.1.3",
        gosolr_version="2.6.39",
        edge_version="1.8.7",
        east_version="1.0.17",
        pair_version="2.0.5",
        manager_version="0.9.13",
        parsec_version="1.5.11",
        inverter_type="deye-1p",
        order_number="86849",
        inverter_sn="00000"
    )
    run_status(imei="868373070933363",
               network_type="mobile")
    run_relays(imei="868373070933363",
               relay_pair_state=True,
               channel_1_device="Geyser",
               channel_2_device="disconnected",
               channel_3_device="disconnected",
               channel_4_device="disconnected",
               channel_1_mode=False,
               channel_2_mode=False,
               channel_3_mode=False,
               channel_4_mode=False,
               channel_1_usage=round(random.uniform(0, 10), 1),
               channel_2_usage=0,
               channel_3_usage=0,
               channel_4_usage=0)
    run_relaycontrol(imei="868373070933363",
                     channel_1_device="Geyser",
                     channel_2_device="disconnected",
                     channel_3_device="disconnected",
                     channel_4_device="disconnected",
                     channel_1_state=True,
                     channel_2_state=False,
                     channel_3_state=False,
                     channel_4_state=False
                     )
    run_tariffs(imei="868373070933363",
                buy_tariff="0.00",
                sell_tariff="0.00")
    run_data(imei="868373070933363", inverter_serial="2209257308")
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373070927647"
    run_data(imei="868373070927647", inverter_serial="2304158510")
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373070920980"
    run_data(imei="868373070920980", inverter_serial="2306200231")
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373070916327"
    run_data(imei="868373070916327", inverter_serial="2211127492")
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373070932381"
    run_data(imei="868373070932381", inverter_serial="2304068729")
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373070909520"
    run_data(imei="868373070909520", inverter_serial="2501123222")
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373070932779"
    run_heartbeat(
        imei="868373070932779",
        brainFirmware_version="1.0.3.7",
        reboot_timestamp="2025-06-12T13:47:00Z",
        general_system_state=True,
        inverter_coms_state=True,
        relay_pair_state=True,
        devices_state=True,
        system_control_state=False,
        internal_state=True,
        relayFirmware_version="2.0.1.3",
        gosolr_version="2.6.39",
        edge_version="1.8.7",
        east_version="1.0.17",
        pair_version="2.0.5",
        manager_version="0.9.13",
        parsec_version="1.5.11",
        inverter_type="deye-1p",
        order_number="87641",
        inverter_sn="2302118244"
    )
    run_status(imei="868373070932779",
               network_type="wifi | 5g")
    run_relays(imei="868373070932779",
               relay_pair_state=True,
               channel_1_device="Geyser",
               channel_2_device="disconnected",
               channel_3_device="disconnected",
               channel_4_device="disconnected",
               channel_1_mode=False,
               channel_2_mode=False,
               channel_3_mode=False,
               channel_4_mode=False,
               channel_1_usage=round(random.uniform(0, 10), 1),
               channel_2_usage=0,
               channel_3_usage=0,
               channel_4_usage=0)
    run_relaycontrol(imei="868373070932779",
                     channel_1_device="Geyser",
                     channel_2_device="disconnected",
                     channel_3_device="disconnected",
                     channel_4_device="disconnected",
                     channel_1_state=True,
                     channel_2_state=False,
                     channel_3_state=False,
                     channel_4_state=False
                     )
    run_tariffs(imei="868373070932779",
                buy_tariff="0.00",
                sell_tariff="0.00")
    run_data(imei="868373070932779", inverter_serial="2302118244")
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373070931490"
    run_heartbeat(
        imei="868373070931490",
        brainFirmware_version="1.0.3.7",
        reboot_timestamp="2025-06-12T13:47:00Z",
        general_system_state=True,
        inverter_coms_state=True,
        relay_pair_state=True,
        devices_state=True,
        system_control_state=False,
        internal_state=True,
        relayFirmware_version="2.0.1.3",
        gosolr_version="2.6.39",
        edge_version="1.8.7",
        east_version="1.0.17",
        pair_version="2.0.5",
        manager_version="0.9.13",
        parsec_version="1.5.11",
        inverter_type="deye-1p",
        order_number="96230",
        inverter_sn="00000"
    )
    run_status(imei="868373070931490",
               network_type="wifi | 5g")
    run_relays(imei="868373070931490",
               relay_pair_state=True,
               channel_1_device="Geyser",
               channel_2_device="disconnected",
               channel_3_device="disconnected",
               channel_4_device="disconnected",
               channel_1_mode=False,
               channel_2_mode=False,
               channel_3_mode=False,
               channel_4_mode=False,
               channel_1_usage=round(random.uniform(0, 10), 1),
               channel_2_usage=0,
               channel_3_usage=0,
               channel_4_usage=0)
    run_relaycontrol(imei="868373070931490",
                     channel_1_device="Geyser",
                     channel_2_device="disconnected",
                     channel_3_device="disconnected",
                     channel_4_device="disconnected",
                     channel_1_state=True,
                     channel_2_state=False,
                     channel_3_state=False,
                     channel_4_state=False
                     )
    run_tariffs(imei="868373070931490",
                buy_tariff="0.00",
                sell_tariff="0.00")
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373070933066"
    run_heartbeat(
        imei="868373070933066",
        brainFirmware_version="1.0.3.7",
        reboot_timestamp="2025-06-12T13:47:00Z",
        general_system_state=True,
        inverter_coms_state=True,
        relay_pair_state=True,
        devices_state=True,
        system_control_state=False,
        internal_state=True,
        relayFirmware_version="2.0.1.3",
        gosolr_version="2.6.39",
        edge_version="1.8.7",
        east_version="1.0.17",
        pair_version="2.0.5",
        manager_version="0.9.13",
        parsec_version="1.5.11",
        inverter_type="deye-1p",
        order_number="96128",
        inverter_sn="00000"
    )
    run_status(imei="868373070933066",
               network_type="wifi | 2g")
    run_relays(imei="868373070933066",
               relay_pair_state=True,
               channel_1_device="Geyser",
               channel_2_device="disconnected",
               channel_3_device="disconnected",
               channel_4_device="disconnected",
               channel_1_mode=False,
               channel_2_mode=False,
               channel_3_mode=False,
               channel_4_mode=False,
               channel_1_usage=round(random.uniform(0, 10), 1),
               channel_2_usage=0,
               channel_3_usage=0,
               channel_4_usage=0)
    run_relaycontrol(imei="868373070933066",
                     channel_1_device="Geyser",
                     channel_2_device="disconnected",
                     channel_3_device="disconnected",
                     channel_4_device="disconnected",
                     channel_1_state=True,
                     channel_2_state=False,
                     channel_3_state=False,
                     channel_4_state=False
                     )
    run_tariffs(imei="868373070933066",
                buy_tariff="0.00",
                sell_tariff="0.00")
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373070928546"
    run_heartbeat(
        imei="868373070928546",
        brainFirmware_version="1.0.3.7",
        reboot_timestamp="2025-06-12T13:47:00Z",
        general_system_state=True,
        inverter_coms_state=True,
        relay_pair_state=True,
        devices_state=True,
        system_control_state=False,
        internal_state=True,
        relayFirmware_version="2.0.1.3",
        gosolr_version="2.6.39",
        edge_version="1.8.7",
        east_version="1.0.17",
        pair_version="2.0.5",
        manager_version="0.9.13",
        parsec_version="1.5.11",
        inverter_type="deye-1p",
        order_number="101141",
        inverter_sn="00000"
    )
    run_status(imei="868373070928546",
               network_type="wifi | 2g")
    run_relays(imei="868373070928546",
               relay_pair_state=True,
               channel_1_device="Geyser",
               channel_2_device="disconnected",
               channel_3_device="disconnected",
               channel_4_device="disconnected",
               channel_1_mode=False,
               channel_2_mode=False,
               channel_3_mode=False,
               channel_4_mode=False,
               channel_1_usage=round(random.uniform(0, 10), 1),
               channel_2_usage=0,
               channel_3_usage=0,
               channel_4_usage=0)
    run_relaycontrol(imei="868373070928546",
                     channel_1_device="Geyser",
                     channel_2_device="disconnected",
                     channel_3_device="disconnected",
                     channel_4_device="disconnected",
                     channel_1_state=True,
                     channel_2_state=False,
                     channel_3_state=False,
                     channel_4_state=False
                     )
    run_tariffs(imei="868373070928546",
                buy_tariff="0.00",
                sell_tariff="0.00")
    run_data(imei="868373070928546", inverter_serial="2305088298")
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373070931664"
    run_heartbeat(
        imei="868373070931664",
        brainFirmware_version="1.0.3.7",
        reboot_timestamp="2025-06-12T13:47:00Z",
        general_system_state=True,
        inverter_coms_state=True,
        relay_pair_state=True,
        devices_state=True,
        system_control_state=False,
        internal_state=True,
        relayFirmware_version="2.0.1.3",
        gosolr_version="2.6.39",
        edge_version="1.8.7",
        east_version="1.0.17",
        pair_version="2.0.5",
        manager_version="0.9.13",
        parsec_version="1.5.11",
        inverter_type="deye-1p",
        order_number="39613",
        inverter_sn="00000"
    )
    run_status(imei="868373070931664",
               network_type="wifi | 2g")
    run_relays(imei="868373070931664",
               relay_pair_state=True,
               channel_1_device="Geyser",
               channel_2_device="disconnected",
               channel_3_device="disconnected",
               channel_4_device="disconnected",
               channel_1_mode=False,
               channel_2_mode=False,
               channel_3_mode=False,
               channel_4_mode=False,
               channel_1_usage=round(random.uniform(0, 10), 1),
               channel_2_usage=0,
               channel_3_usage=0,
               channel_4_usage=0)
    run_relaycontrol(imei="868373070931664",
                     channel_1_device="Geyser",
                     channel_2_device="disconnected",
                     channel_3_device="disconnected",
                     channel_4_device="disconnected",
                     channel_1_state=True,
                     channel_2_state=False,
                     channel_3_state=False,
                     channel_4_state=False
                     )
    run_tariffs(imei="868373070931664",
                buy_tariff="0.00",
                sell_tariff="0.00")
    run_data(imei="868373070931664", inverter_serial="2211238422")
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373070932639"
    run_heartbeat(
        imei="868373070932639",
        brainFirmware_version="1.0.3.7",
        reboot_timestamp="2025-06-12T13:47:00Z",
        general_system_state=True,
        inverter_coms_state=True,
        relay_pair_state=True,
        devices_state=True,
        system_control_state=False,
        internal_state=True,
        relayFirmware_version="2.0.1.3",
        gosolr_version="2.6.39",
        edge_version="1.8.7",
        east_version="1.0.17",
        pair_version="2.0.5",
        manager_version="0.9.13",
        parsec_version="1.5.11",
        inverter_type="deye-1p",
        order_number="49467",
        inverter_sn="2303266007"
    )
    run_status(imei="868373070932639",
               network_type="wifi | 2g")
    run_relays(imei="868373070932639",
               relay_pair_state=True,
               channel_1_device="Geyser",
               channel_2_device="disconnected",
               channel_3_device="disconnected",
               channel_4_device="disconnected",
               channel_1_mode=False,
               channel_2_mode=False,
               channel_3_mode=False,
               channel_4_mode=False,
               channel_1_usage=round(random.uniform(0, 10), 1),
               channel_2_usage=0,
               channel_3_usage=0,
               channel_4_usage=0)
    run_relaycontrol(imei="868373070932639",
                     channel_1_device="Geyser",
                     channel_2_device="disconnected",
                     channel_3_device="disconnected",
                     channel_4_device="disconnected",
                     channel_1_state=True,
                     channel_2_state=False,
                     channel_3_state=False,
                     channel_4_state=False
                     )
    run_tariffs(imei="868373070932639",
                buy_tariff="0.00",
                sell_tariff="0.00")
    run_data(imei="868373070932639", inverter_serial="2303266007")
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373070931128"
    run_heartbeat(
        imei="868373070931128",
        brainFirmware_version="1.0.3.7",
        reboot_timestamp="2025-06-06T12:41:00Z",
        general_system_state=True,
        inverter_coms_state=True,
        relay_pair_state=True,
        devices_state=True,
        system_control_state=False,
        internal_state=True,
        relayFirmware_version="2.0.1.3",
        gosolr_version="2.6.39",
        edge_version="1.8.7",
        east_version="1.0.17",
        pair_version="2.0.5",
        manager_version="0.9.13",
        parsec_version="1.5.11",
        inverter_type="solis-1p",
        order_number="102508",
        inverter_sn="1031180245160225"
    )
    run_status(imei="868373070931128",
               network_type="wifi | 5g")
    run_relays(imei="868373070931128",
               relay_pair_state=True,
               channel_1_device="Geyser",
               channel_2_device="disconnected",
               channel_3_device="disconnected",
               channel_4_device="disconnected",
               channel_1_mode=False,
               channel_2_mode=False,
               channel_3_mode=False,
               channel_4_mode=False,
               channel_1_usage=round(random.uniform(0, 10), 1),
               channel_2_usage=0,
               channel_3_usage=0,
               channel_4_usage=0)
    run_relaycontrol(imei="868373070931128",
                     channel_1_device="Geyser",
                     channel_2_device="disconnected",
                     channel_3_device="disconnected",
                     channel_4_device="disconnected",
                     channel_1_state=True,
                     channel_2_state=False,
                     channel_3_state=False,
                     channel_4_state=False
                     )
    run_tariffs(imei="868373070931128",
                buy_tariff="6.01",
                sell_tariff="0.00")
    run_data(imei="868373070931128", inverter_serial="1031180245160225")
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373070932712"
    run_heartbeat(
        imei="868373070932712",
        brainFirmware_version="1.0.3.7",
        reboot_timestamp="2025-06-12T13:47:00Z",
        general_system_state=True,
        inverter_coms_state=True,
        relay_pair_state=True,
        devices_state=True,
        system_control_state=False,
        internal_state=True,
        relayFirmware_version="2.0.1.3",
        gosolr_version="2.6.39",
        edge_version="1.8.7",
        east_version="1.0.17",
        pair_version="2.0.5",
        manager_version="0.9.13",
        parsec_version="1.5.11",
        inverter_type="deye-1p",
        order_number="102842",
        inverter_sn="2501124057"
    )
    run_status(imei="868373070932712",
               network_type="mobile")
    run_relays(imei="868373070932712",
               relay_pair_state=True,
               channel_1_device="Geyser",
               channel_2_device="disconnected",
               channel_3_device="disconnected",
               channel_4_device="disconnected",
               channel_1_mode=False,
               channel_2_mode=False,
               channel_3_mode=False,
               channel_4_mode=False,
               channel_1_usage=round(random.uniform(0, 10), 1),
               channel_2_usage=0,
               channel_3_usage=0,
               channel_4_usage=0)
    run_relaycontrol(imei="868373070932712",
                     channel_1_device="Geyser",
                     channel_2_device="disconnected",
                     channel_3_device="disconnected",
                     channel_4_device="disconnected",
                     channel_1_state=True,
                     channel_2_state=False,
                     channel_3_state=False,
                     channel_4_state=False
                     )
    run_tariffs(imei="868373070932712",
                buy_tariff="0.00",
                sell_tariff="0.00")
    run_data(imei="868373070932712", inverter_serial="2501124057")
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373070933694"
    imei_number = "868373070933694"
    run_heartbeat(
        imei=imei_number,
        brainFirmware_version="1.0.3.7",
        reboot_timestamp="2025-06-12T13:47:00Z",
        general_system_state=True,
        inverter_coms_state=True,
        relay_pair_state=True,
        devices_state=True,
        system_control_state=False,
        internal_state=True,
        relayFirmware_version="2.0.1.3",
        gosolr_version="2.6.39",
        edge_version="1.8.7",
        east_version="1.0.17",
        pair_version="2.0.5",
        manager_version="0.9.13",
        parsec_version="1.5.11",
        inverter_type="solis-1p",
        order_number="101567",
        inverter_sn="00000"
    )
    run_status(imei=imei_number,
               network_type="wifi | 5g")
    run_relays(imei="868373070933694",
               relay_pair_state=True,
               channel_1_device="Geyser",
               channel_2_device="disconnected",
               channel_3_device="disconnected",
               channel_4_device="disconnected",
               channel_1_mode=False,
               channel_2_mode=False,
               channel_3_mode=False,
               channel_4_mode=False,
               channel_1_usage=round(random.uniform(0, 10), 1),
               channel_2_usage=0,
               channel_3_usage=0,
               channel_4_usage=0)
    run_relaycontrol(imei="868373070933694",
                     channel_1_device="Geyser",
                     channel_2_device="disconnected",
                     channel_3_device="disconnected",
                     channel_4_device="disconnected",
                     channel_1_state=True,
                     channel_2_state=False,
                     channel_3_state=False,
                     channel_4_state=False
                     )
    run_tariffs(imei="868373070933694",
                buy_tariff="5.44",
                sell_tariff="0.00")
    run_data(imei="868373070933694", inverter_serial="00000")
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373070932126"
    imei_number = "868373070932126"
    run_heartbeat(
        imei=imei_number,
        brainFirmware_version="1.0.3.7",
        reboot_timestamp="2025-06-12T13:47:00Z",
        general_system_state=True,
        inverter_coms_state=True,
        relay_pair_state=True,
        devices_state=True,
        system_control_state=False,
        internal_state=True,
        relayFirmware_version="2.0.1.3",
        gosolr_version="2.6.39",
        edge_version="1.8.7",
        east_version="1.0.17",
        pair_version="2.0.5",
        manager_version="0.9.13",
        parsec_version="1.5.11",
        inverter_type="deye-1p",
        order_number="103057",
        inverter_sn="00000"
    )
    run_status(imei=imei_number,
               network_type="wifi | 2g")
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373070932357"
    imei_number = "868373070932357"
    run_heartbeat(
        imei=imei_number,
        brainFirmware_version="1.0.3.7",
        reboot_timestamp="2025-06-12T13:47:00Z",
        general_system_state=True,
        inverter_coms_state=True,
        relay_pair_state=True,
        devices_state=True,
        system_control_state=False,
        internal_state=True,
        relayFirmware_version="2.0.1.3",
        gosolr_version="2.6.39",
        edge_version="1.8.7",
        east_version="1.0.17",
        pair_version="2.0.5",
        manager_version="0.9.13",
        parsec_version="1.5.11",
        inverter_type="deye-1p",
        order_number="96747",
        inverter_sn="00000"
    )
    run_status(imei=imei_number,
               network_type="wifi | 2g")
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373070932092"
    imei_number = "868373070932092"
    run_heartbeat(
        imei=imei_number,
        brainFirmware_version="1.0.3.7",
        reboot_timestamp="2025-06-12T13:47:00Z",
        general_system_state=True,
        inverter_coms_state=True,
        relay_pair_state=True,
        devices_state=True,
        system_control_state=False,
        internal_state=True,
        relayFirmware_version="2.0.1.3",
        gosolr_version="2.6.39",
        edge_version="1.8.7",
        east_version="1.0.17",
        pair_version="2.0.5",
        manager_version="0.9.13",
        parsec_version="1.5.11",
        inverter_type="deye-1p",
        order_number="21674",
        inverter_sn="2211244525"
    )
    run_status(imei=imei_number,
               network_type="wifi | 5g")
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373070930435"
    imei_number = "868373070930435"
    run_heartbeat(
        imei=imei_number,
        brainFirmware_version="1.0.3.7",
        reboot_timestamp="2025-06-12T13:47:00Z",
        general_system_state=True,
        inverter_coms_state=True,
        relay_pair_state=True,
        devices_state=True,
        system_control_state=False,
        internal_state=True,
        relayFirmware_version="2.0.1.3",
        gosolr_version="2.6.39",
        edge_version="1.8.7",
        east_version="1.0.17",
        pair_version="2.0.5",
        manager_version="0.9.13",
        parsec_version="1.5.11",
        inverter_type="deye-1p",
        order_number="45408",
        inverter_sn="00000"
    )
    run_status(imei=imei_number,
               network_type="mobile")
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373070928991"
    imei_number = "868373070928991"
    run_heartbeat(
        imei=imei_number,
        brainFirmware_version="1.0.3.7",
        reboot_timestamp="2025-06-12T13:47:00Z",
        general_system_state=True,
        inverter_coms_state=True,
        relay_pair_state=True,
        devices_state=True,
        system_control_state=False,
        internal_state=True,
        relayFirmware_version="2.0.1.3",
        gosolr_version="2.6.39",
        edge_version="1.8.7",
        east_version="1.0.17",
        pair_version="2.0.5",
        manager_version="0.9.13",
        parsec_version="1.5.11",
        inverter_type="deye-1p",
        order_number="96231",
        inverter_sn="00000"
    )
    run_status(imei=imei_number,
               network_type="mobile")
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373070931631"
    imei_number = "868373070931631"
    run_heartbeat(
        imei=imei_number,
        brainFirmware_version="1.0.3.7",
        reboot_timestamp="2025-06-12T13:47:00Z",
        general_system_state=True,
        inverter_coms_state=True,
        relay_pair_state=True,
        devices_state=True,
        system_control_state=False,
        internal_state=True,
        relayFirmware_version="2.0.1.3",
        gosolr_version="2.6.39",
        edge_version="1.8.7",
        east_version="1.0.17",
        pair_version="2.0.5",
        manager_version="0.9.13",
        parsec_version="1.5.11",
        inverter_type="deye-1p",
        order_number="103523",
        inverter_sn="00000"
    )
    run_status(imei=imei_number,
               network_type="wifi | 2g")
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373070931375"
    imei_number = "868373070931375"
    # run_heartbeat(
    #    imei=imei_number,
    #    brainFirmware_version="1.0.3.7",
    #    reboot_timestamp="2025-06-12T13:47:00Z",
    #    general_system_state=True,
    #    inverter_coms_state=True,
    #    relay_pair_state=True,
    #    devices_state=True,
    #    system_control_state=False,
    #    internal_state=True,
    #    relayFirmware_version="2.0.1.3",
    #    gosolr_version="2.6.39",
    #    edge_version="1.8.7",
    #    east_version="1.0.17",
    #    pair_version="2.0.5",
    #    manager_version="0.9.13",
    #    parsec_version="1.5.11",
    #    inverter_type="deye-1p",
    #    order_number="100622",
    #    inverter_sn="00000"
    # )
    # run_status(imei=imei_number,
    # network_type="wifi | 5g")
    run_data(imei=imei_number, inverter_serial="2304128504")
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373070932753"
    imei_number = "868373070932753"
    run_heartbeat(
        imei=imei_number,
        brainFirmware_version="1.0.3.7",
        reboot_timestamp="2025-06-12T13:47:00Z",
        general_system_state=True,
        inverter_coms_state=True,
        relay_pair_state=True,
        devices_state=True,
        system_control_state=False,
        internal_state=True,
        relayFirmware_version="2.0.1.3",
        gosolr_version="2.6.39",
        edge_version="1.8.7",
        east_version="1.0.17",
        pair_version="2.0.5",
        manager_version="0.9.13",
        parsec_version="1.5.11",
        inverter_type="deye-1p",
        order_number="100879",
        inverter_sn="00000"
    )
    run_status(imei=imei_number,
               network_type="wifi | 5g")
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373070930740"
    imei_number = "868373070930740"
    run_heartbeat(
        imei=imei_number,
        brainFirmware_version="1.0.3.7",
        reboot_timestamp="2025-06-12T13:47:00Z",
        general_system_state=True,
        inverter_coms_state=True,
        relay_pair_state=True,
        devices_state=True,
        system_control_state=False,
        internal_state=True,
        relayFirmware_version="2.0.1.3",
        gosolr_version="2.6.39",
        edge_version="1.8.7",
        east_version="1.0.17",
        pair_version="2.0.5",
        manager_version="0.9.13",
        parsec_version="1.5.11",
        inverter_type="deye-1p",
        order_number="103060",
        inverter_sn="00000"
    )
    run_status(imei=imei_number,
               network_type="wifi | 5g")
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373070916574"
    imei_number = "868373070916574"
    run_heartbeat(
        imei=imei_number,
        brainFirmware_version="1.0.3.7",
        reboot_timestamp="2025-06-12T13:47:00Z",
        general_system_state=True,
        inverter_coms_state=True,
        relay_pair_state=True,
        devices_state=True,
        system_control_state=False,
        internal_state=True,
        relayFirmware_version="2.0.1.3",
        gosolr_version="2.6.39",
        edge_version="1.8.7",
        east_version="1.0.17",
        pair_version="2.0.5",
        manager_version="0.9.13",
        parsec_version="1.5.11",
        inverter_type="deye-1p",
        order_number="82509",
        inverter_sn="00000"
    )
    run_status(imei=imei_number,
               network_type="wifi | 2g")
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373070929569"
    imei_number = "868373070929569"
    run_heartbeat(
        imei=imei_number,
        brainFirmware_version="1.0.3.7",
        reboot_timestamp="2025-06-12T13:47:00Z",
        general_system_state=True,
        inverter_coms_state=True,
        relay_pair_state=True,
        devices_state=True,
        system_control_state=False,
        internal_state=True,
        relayFirmware_version="2.0.1.3",
        gosolr_version="2.6.39",
        edge_version="1.8.7",
        east_version="1.0.17",
        pair_version="2.0.5",
        manager_version="0.9.13",
        parsec_version="1.5.11",
        inverter_type="deye-1p",
        order_number="14904",
        inverter_sn="00000"
    )
    run_status(imei=imei_number,
               network_type="wifi | 2g")
except Exception as e:
    print(str(e))

 # try:
 #    CLIENT_ID = "brain-868373070917333"
 #    imei_number="868373070917333"
 #    run_heartbeat(
 #        imei=imei_number,
 #        brainFirmware_version="1.0.3.7",
 #        reboot_timestamp="2025-06-12T13:47:00Z",
 #        general_system_state=True,
 #        inverter_coms_state=True,
 #        relay_pair_state=True,
 #        devices_state=True,
 #        system_control_state=False,
 #        internal_state=True,
 #        relayFirmware_version="2.0.1.3",
 #        gosolr_version="2.6.39",
 #        edge_version="1.8.7",
 #        east_version="1.0.17",
 #        pair_version="2.0.5",
 #        manager_version="0.9.13",
 #        parsec_version="1.5.11",
 #        inverter_type="deye-1p",
 #        order_number="102746",
 #        inverter_sn="00000"
 #    )
 #    run_status(imei=imei_number,
 #    network_type="mobile")
 # except Exception as e:
 #    print(str(e))

try:
    CLIENT_ID = "brain-868373070917184"
    imei_number = "868373070917184"
    run_heartbeat(
        imei=imei_number,
        brainFirmware_version="1.0.3.7",
        reboot_timestamp="2025-06-12T13:47:00Z",
        general_system_state=True,
        inverter_coms_state=True,
        relay_pair_state=True,
        devices_state=True,
        system_control_state=False,
        internal_state=True,
        relayFirmware_version="2.0.1.3",
        gosolr_version="2.6.39",
        edge_version="1.8.7",
        east_version="1.0.17",
        pair_version="2.0.5",
        manager_version="0.9.13",
        parsec_version="1.5.11",
        inverter_type="solis-1p",
        order_number="103137",
        inverter_sn="00000"
    )
    run_status(imei=imei_number,
               network_type="mobile")
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373070917333"
    imei_number = "868373070917333"
    run_heartbeat(
        imei=imei_number,
        brainFirmware_version="1.0.3.7",
        reboot_timestamp="2025-06-12T13:47:00Z",
        general_system_state=True,
        inverter_coms_state=True,
        relay_pair_state=True,
        devices_state=True,
        system_control_state=False,
        internal_state=True,
        relayFirmware_version="2.0.1.3",
        gosolr_version="2.6.39",
        edge_version="1.8.7",
        east_version="1.0.17",
        pair_version="2.0.5",
        manager_version="0.9.13",
        parsec_version="1.5.11",
        inverter_type="deye-1p",
        order_number="101285",
        inverter_sn="00000"
    )
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373070929072"
    imei_number = "868373070929072"
    run_heartbeat(
        imei=imei_number,
        brainFirmware_version="1.0.3.7",
        reboot_timestamp="2025-06-12T13:47:00Z",
        general_system_state=False,
        inverter_coms_state=False,
        relay_pair_state=True,
        devices_state=True,
        system_control_state=False,
        internal_state=True,
        relayFirmware_version="2.0.1.3",
        gosolr_version="2.6.39",
        edge_version="1.8.7",
        east_version="1.0.17",
        pair_version="2.0.5",
        manager_version="0.9.13",
        parsec_version="1.5.11",
        inverter_type="deye-1p",
        order_number="100625",
        inverter_sn="2305082190"
    )
    run_status(imei=imei_number,
               network_type="mobile")
    run_data(imei=imei_number, inverter_serial=inverter_serialn)
    run_tariffs(imei=imei_number, buy_tariff="5.40", sell_tariff="0.86")
    run_relays(imei=imei_number,
               relay_pair_state=True,
               channel_1_device="Geyser",
               channel_2_device="disconnected",
               channel_3_device="disconnected",
               channel_4_device="disconnected",
               channel_1_mode=False,
               channel_2_mode=False,
               channel_3_mode=False,
               channel_4_mode=False,
               channel_1_usage=0,
               channel_2_usage=0,
               channel_3_usage=0,
               channel_4_usage=0)
    run_relaycontrol(imei="868373070929072",
                     channel_1_device="Geyser",
                     channel_2_device="disconnected",
                     channel_3_device="disconnected",
                     channel_4_device="disconnected",
                     channel_1_state=True,
                     channel_2_state=False,
                     channel_3_state=False,
                     channel_4_state=False
                     )
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373070932688"
    imei_number = "868373070932688"
    run_heartbeat(
        imei=imei_number,
        brainFirmware_version="1.0.3.7",
        reboot_timestamp="2025-06-12T13:47:00Z",
        general_system_state=True,
        inverter_coms_state=True,
        relay_pair_state=True,
        devices_state=True,
        system_control_state=False,
        internal_state=True,
        relayFirmware_version="2.0.1.3",
        gosolr_version="2.6.39",
        edge_version="1.8.7",
        east_version="1.0.17",
        pair_version="2.0.5",
        manager_version="0.9.13",
        parsec_version="1.5.11",
        inverter_type="deye-1p",
        order_number="84137",
        inverter_sn="2304222297"
    )
    run_status(imei=imei_number,
               network_type="wifi | 2g")
    run_data(imei=imei_number, inverter_serial="2304222297")
    run_tariffs(imei=imei_number, buy_tariff="5.40", sell_tariff="0.86")
    run_relays(imei=imei_number,
               relay_pair_state=True,
               channel_1_device="Geyser",
               channel_2_device="disconnected",
               channel_3_device="disconnected",
               channel_4_device="disconnected",
               channel_1_mode=False,
               channel_2_mode=False,
               channel_3_mode=False,
               channel_4_mode=False,
               channel_1_usage=0,
               channel_2_usage=0,
               channel_3_usage=0,
               channel_4_usage=0)
    run_relaycontrol(imei="868373070932688",
                     channel_1_device="Geyser",
                     channel_2_device="disconnected",
                     channel_3_device="disconnected",
                     channel_4_device="disconnected",
                     channel_1_state=True,
                     channel_2_state=False,
                     channel_3_state=False,
                     channel_4_state=False
                     )
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373070931938"
    imei_number = "868373070931938"
    run_heartbeat(
        imei=imei_number,
        brainFirmware_version="1.0.3.7",
        reboot_timestamp="2025-06-12T13:47:00Z",
        general_system_state=False,
        inverter_coms_state=False,
        relay_pair_state=True,
        devices_state=True,
        system_control_state=False,
        internal_state=True,
        relayFirmware_version="2.0.1.3",
        gosolr_version="2.6.39",
        edge_version="1.8.7",
        east_version="1.0.17",
        pair_version="2.0.5",
        manager_version="0.9.13",
        parsec_version="1.5.11",
        inverter_type="deye-1p",
        order_number="39418",
        inverter_sn="2304108535"
    )
    run_status(imei=imei_number,
               network_type="wifi | 5g")
    run_data(imei="868373070931938", inverter_serial="2304108535")
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373070935657"
    imei_number = "868373070935657"
    run_heartbeat(
        imei=imei_number,
        brainFirmware_version="1.0.3.7",
        reboot_timestamp="2025-06-12T13:47:00Z",
        general_system_state=True,
        inverter_coms_state=True,
        relay_pair_state=True,
        devices_state=True,
        system_control_state=False,
        internal_state=True,
        relayFirmware_version="2.0.1.3",
        gosolr_version="2.6.39",
        edge_version="1.8.7",
        east_version="1.0.17",
        pair_version="2.0.5",
        manager_version="0.9.13",
        parsec_version="1.5.11",
        inverter_type="deye-1p",
        order_number="103654",
        inverter_sn="00000"
    )
    run_status(imei=imei_number,
               network_type="wifi | 5g")
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373070932233"
    imei_number = "868373070932233"
    inverter_serialn = "2304046516"
    run_heartbeat(
        imei=imei_number,
        brainFirmware_version="1.0.3.7",
        reboot_timestamp="2025-06-12T13:47:00Z",
        general_system_state=True,
        inverter_coms_state=True,
        relay_pair_state=True,
        devices_state=True,
        system_control_state=False,
        internal_state=True,
        relayFirmware_version="2.0.1.3",
        gosolr_version="2.6.39",
        edge_version="1.8.7",
        east_version="1.0.17",
        pair_version="2.0.5",
        manager_version="0.9.13",
        parsec_version="1.5.11",
        inverter_type="deye-1p",
        order_number="99814",
        inverter_sn=inverter_serialn
    )
    run_status(imei=imei_number,
               network_type="wifi | 5g")
    run_data(imei=imei_number, inverter_serial=inverter_serialn)
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-866069069798807"
    imei_number = "866069069798807"
    inverter_serialn = "2209223588"
    run_heartbeat(
        imei=imei_number,
        brainFirmware_version="1.1.1.0(β)",
        reboot_timestamp="2025-06-12T13:47:00Z",
        general_system_state=True,
        inverter_coms_state=True,
        relay_pair_state=False,
        devices_state=False,
        system_control_state=False,
        internal_state=True,
        relayFirmware_version="3.5.1.10(β)",
        gosolr_version="2.8.0.2(π)",
        edge_version="1.8.7",
        east_version="1.0.17",
        pair_version="2.0.5",
        manager_version="0.9.13",
        parsec_version="1.5.11",
        inverter_type="deye-1p",
        order_number="29184",
        inverter_sn=inverter_serialn
    )
    run_status(imei=imei_number,
               network_type="wifi | 5ghz")
    run_data(imei=imei_number, inverter_serial=inverter_serialn)
    run_relays(imei=imei_number,
               relay_pair_state=False,
               channel_1_device="disconnected",
               channel_2_device="disconnected",
               channel_3_device="disconnected",
               channel_4_device="disconnected",
               channel_1_mode=False,
               channel_2_mode=False,
               channel_3_mode=False,
               channel_4_mode=False,
               channel_1_usage=0,
               channel_2_usage=0,
               channel_3_usage=0,
               channel_4_usage=0)
    run_relaycontrol(imei="868373070932712",
                     channel_1_device="disconnected",
                     channel_2_device="disconnected",
                     channel_3_device="disconnected",
                     channel_4_device="disconnected",
                     channel_1_state=False,
                     channel_2_state=False,
                     channel_3_state=False,
                     channel_4_state=False
                     )
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373070916657"
    imei_number = "868373070916657"
    run_heartbeat(
        imei=imei_number,
        brainFirmware_version="1.1.0.3",
        reboot_timestamp="2025-09-02T05:47:00Z",
        general_system_state=True,
        inverter_coms_state=True,
        relay_pair_state=True,
        devices_state=True,
        system_control_state=True,
        internal_state=True,
        relayFirmware_version="3.5.1.12",
        gosolr_version="-",
        edge_version="-",
        east_version="-",
        pair_version="-",
        manager_version="-",
        parsec_version="-",
        inverter_type="-",
        order_number="-",
        inverter_sn="-"
    )
    run_relays(imei=imei_number,
               relay_pair_state=True,
               channel_1_device="Geyser",
               channel_2_device="disconnected",
               channel_3_device="disconnected",
               channel_4_device="disconnected",
               channel_1_mode=False,
               channel_2_mode=False,
               channel_3_mode=False,
               channel_4_mode=False,
               channel_1_usage=round(random.uniform(2600, 3200), 1),
               channel_2_usage=0,
               channel_3_usage=0,
               channel_4_usage=0)
    run_relaycontrol(imei=imei_number,
                     channel_1_device="Geyser",
                     channel_2_device="disconnected",
                     channel_3_device="disconnected",
                     channel_4_device="disconnected",
                     channel_1_state=True,
                     channel_2_state=False,
                     channel_3_state=False,
                     channel_4_state=False
                     )
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373070935251"
    imei_number = "868373070935251"
    run_heartbeat(
        imei=imei_number,
        brainFirmware_version="1.1.0.3",
        reboot_timestamp="2025-09-02T05:47:00Z",
        general_system_state=True,
        inverter_coms_state=True,
        relay_pair_state=True,
        devices_state=True,
        system_control_state=True,
        internal_state=True,
        relayFirmware_version="3.5.1.12",
        gosolr_version="-",
        edge_version="-",
        east_version="-",
        pair_version="-",
        manager_version="-",
        parsec_version="-",
        inverter_type="-",
        order_number="-",
        inverter_sn="-"
    )
    run_relays(imei=imei_number,
               relay_pair_state=True,
               channel_1_device="Geyser",
               channel_2_device="disconnected",
               channel_3_device="disconnected",
               channel_4_device="disconnected",
               channel_1_mode=False,
               channel_2_mode=False,
               channel_3_mode=False,
               channel_4_mode=False,
               channel_1_usage=round(random.uniform(2600, 3200), 1),
               channel_2_usage=0,
               channel_3_usage=0,
               channel_4_usage=0)
    run_relaycontrol(imei=imei_number,
                     channel_1_device="Geyser",
                     channel_2_device="disconnected",
                     channel_3_device="disconnected",
                     channel_4_device="disconnected",
                     channel_1_state=True,
                     channel_2_state=False,
                     channel_3_state=False,
                     channel_4_state=False
                     )
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373070933942"
    imei_number = "868373070933942"
    run_heartbeat(
        imei=imei_number,
        brainFirmware_version="1.1.0.3",
        reboot_timestamp="2025-09-02T05:47:00Z",
        general_system_state=True,
        inverter_coms_state=True,
        relay_pair_state=True,
        devices_state=True,
        system_control_state=True,
        internal_state=True,
        relayFirmware_version="3.5.1.12",
        gosolr_version="-",
        edge_version="-",
        east_version="-",
        pair_version="-",
        manager_version="-",
        parsec_version="-",
        inverter_type="-",
        order_number="-",
        inverter_sn="-"
    )
    run_relays(imei=imei_number,
               relay_pair_state=True,
               channel_1_device="Geyser",
               channel_2_device="disconnected",
               channel_3_device="disconnected",
               channel_4_device="disconnected",
               channel_1_mode=False,
               channel_2_mode=False,
               channel_3_mode=False,
               channel_4_mode=False,
               channel_1_usage=round(random.uniform(2600, 3200), 1),
               channel_2_usage=0,
               channel_3_usage=0,
               channel_4_usage=0)
    run_relaycontrol(imei=imei_number,
                     channel_1_device="Geyser",
                     channel_2_device="disconnected",
                     channel_3_device="disconnected",
                     channel_4_device="disconnected",
                     channel_1_state=True,
                     channel_2_state=False,
                     channel_3_state=False,
                     channel_4_state=False
                     )
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373070930666"
    imei_number = "868373070930666"
    run_heartbeat(
        imei=imei_number,
        brainFirmware_version="1.1.0.3",
        reboot_timestamp="2025-09-02T05:47:00Z",
        general_system_state=True,
        inverter_coms_state=True,
        relay_pair_state=True,
        devices_state=True,
        system_control_state=True,
        internal_state=True,
        relayFirmware_version="3.5.1.12",
        gosolr_version="-",
        edge_version="-",
        east_version="-",
        pair_version="-",
        manager_version="-",
        parsec_version="-",
        inverter_type="-",
        order_number="-",
        inverter_sn="-"
    )
    run_relays(imei=imei_number,
               relay_pair_state=True,
               channel_1_device="Geyser",
               channel_2_device="disconnected",
               channel_3_device="disconnected",
               channel_4_device="disconnected",
               channel_1_mode=False,
               channel_2_mode=False,
               channel_3_mode=False,
               channel_4_mode=False,
               channel_1_usage=round(random.uniform(2600, 3200), 1),
               channel_2_usage=0,
               channel_3_usage=0,
               channel_4_usage=0)
    run_relaycontrol(imei=imei_number,
                     channel_1_device="Geyser",
                     channel_2_device="disconnected",
                     channel_3_device="disconnected",
                     channel_4_device="disconnected",
                     channel_1_state=True,
                     channel_2_state=False,
                     channel_3_state=False,
                     channel_4_state=False
                     )
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373070929718"
    imei_number = "868373070929718"
    run_heartbeat(
        imei=imei_number,
        brainFirmware_version="1.1.0.3",
        reboot_timestamp="2025-09-02T05:47:00Z",
        general_system_state=True,
        inverter_coms_state=True,
        relay_pair_state=True,
        devices_state=True,
        system_control_state=True,
        internal_state=True,
        relayFirmware_version="3.5.1.12",
        gosolr_version="-",
        edge_version="-",
        east_version="-",
        pair_version="-",
        manager_version="-",
        parsec_version="-",
        inverter_type="-",
        order_number="-",
        inverter_sn="-"
    )
    run_relays(imei=imei_number,
               relay_pair_state=True,
               channel_1_device="Geyser",
               channel_2_device="disconnected",
               channel_3_device="disconnected",
               channel_4_device="disconnected",
               channel_1_mode=False,
               channel_2_mode=False,
               channel_3_mode=False,
               channel_4_mode=False,
               channel_1_usage=round(random.uniform(2600, 3200), 1),
               channel_2_usage=0,
               channel_3_usage=0,
               channel_4_usage=0)
    run_relaycontrol(imei=imei_number,
                     channel_1_device="Geyser",
                     channel_2_device="disconnected",
                     channel_3_device="disconnected",
                     channel_4_device="disconnected",
                     channel_1_state=True,
                     channel_2_state=False,
                     channel_3_state=False,
                     channel_4_state=False
                     )
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373070926920"
    imei_number = "868373070926920"
    run_heartbeat(
        imei=imei_number,
        brainFirmware_version="1.1.0.3",
        reboot_timestamp="2025-09-02T05:47:00Z",
        general_system_state=True,
        inverter_coms_state=True,
        relay_pair_state=True,
        devices_state=True,
        system_control_state=True,
        internal_state=True,
        relayFirmware_version="3.5.1.12",
        gosolr_version="-",
        edge_version="-",
        east_version="-",
        pair_version="-",
        manager_version="-",
        parsec_version="-",
        inverter_type="-",
        order_number="-",
        inverter_sn="-"
    )
    run_relays(imei=imei_number,
               relay_pair_state=True,
               channel_1_device="Geyser",
               channel_2_device="disconnected",
               channel_3_device="disconnected",
               channel_4_device="disconnected",
               channel_1_mode=False,
               channel_2_mode=False,
               channel_3_mode=False,
               channel_4_mode=False,
               channel_1_usage=round(random.uniform(2600, 3200), 1),
               channel_2_usage=0,
               channel_3_usage=0,
               channel_4_usage=0)
    run_relaycontrol(imei=imei_number,
                     channel_1_device="Geyser",
                     channel_2_device="disconnected",
                     channel_3_device="disconnected",
                     channel_4_device="disconnected",
                     channel_1_state=True,
                     channel_2_state=False,
                     channel_3_state=False,
                     channel_4_state=False
                     )
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373070935707"
    imei_number = "868373070935707"
    run_heartbeat(
        imei=imei_number,
        brainFirmware_version="1.1.0.3",
        reboot_timestamp="2025-09-02T05:47:00Z",
        general_system_state=True,
        inverter_coms_state=True,
        relay_pair_state=True,
        devices_state=True,
        system_control_state=True,
        internal_state=True,
        relayFirmware_version="3.5.1.12",
        gosolr_version="-",
        edge_version="-",
        east_version="-",
        pair_version="-",
        manager_version="-",
        parsec_version="-",
        inverter_type="-",
        order_number="-",
        inverter_sn="-"
    )
    run_relays(imei=imei_number,
               relay_pair_state=True,
               channel_1_device="Geyser",
               channel_2_device="disconnected",
               channel_3_device="disconnected",
               channel_4_device="disconnected",
               channel_1_mode=False,
               channel_2_mode=False,
               channel_3_mode=False,
               channel_4_mode=False,
               channel_1_usage=round(random.uniform(2600, 3200), 1),
               channel_2_usage=0,
               channel_3_usage=0,
               channel_4_usage=0)
    run_relaycontrol(imei=imei_number,
                     channel_1_device="Geyser",
                     channel_2_device="disconnected",
                     channel_3_device="disconnected",
                     channel_4_device="disconnected",
                     channel_1_state=True,
                     channel_2_state=False,
                     channel_3_state=False,
                     channel_4_state=False
                     )
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373070931581"
    imei_number = "868373070931581"
    run_heartbeat(
        imei=imei_number,
        brainFirmware_version="1.1.0.3",
        reboot_timestamp="2025-09-02T05:47:00Z",
        general_system_state=True,
        inverter_coms_state=True,
        relay_pair_state=True,
        devices_state=True,
        system_control_state=True,
        internal_state=True,
        relayFirmware_version="3.5.1.12",
        gosolr_version="-",
        edge_version="-",
        east_version="-",
        pair_version="-",
        manager_version="-",
        parsec_version="-",
        inverter_type="-",
        order_number="-",
        inverter_sn="-"
    )
    run_relays(imei=imei_number,
               relay_pair_state=True,
               channel_1_device="Geyser",
               channel_2_device="disconnected",
               channel_3_device="disconnected",
               channel_4_device="disconnected",
               channel_1_mode=False,
               channel_2_mode=False,
               channel_3_mode=False,
               channel_4_mode=False,
               channel_1_usage=round(random.uniform(2600, 3200), 1),
               channel_2_usage=0,
               channel_3_usage=0,
               channel_4_usage=0)
    run_relaycontrol(imei=imei_number,
                     channel_1_device="Geyser",
                     channel_2_device="disconnected",
                     channel_3_device="disconnected",
                     channel_4_device="disconnected",
                     channel_1_state=True,
                     channel_2_state=False,
                     channel_3_state=False,
                     channel_4_state=False
                     )
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373070927274"
    imei_number = "868373070927274"
    run_heartbeat(
        imei=imei_number,
        brainFirmware_version="1.1.0.3",
        reboot_timestamp="2025-09-02T05:47:00Z",
        general_system_state=True,
        inverter_coms_state=True,
        relay_pair_state=True,
        devices_state=True,
        system_control_state=True,
        internal_state=True,
        relayFirmware_version="3.5.1.12",
        gosolr_version="-",
        edge_version="-",
        east_version="-",
        pair_version="-",
        manager_version="-",
        parsec_version="-",
        inverter_type="-",
        order_number="-",
        inverter_sn="-"
    )
    run_relays(imei=imei_number,
               relay_pair_state=True,
               channel_1_device="Geyser",
               channel_2_device="disconnected",
               channel_3_device="disconnected",
               channel_4_device="disconnected",
               channel_1_mode=False,
               channel_2_mode=False,
               channel_3_mode=False,
               channel_4_mode=False,
               channel_1_usage=round(random.uniform(2600, 3200), 1),
               channel_2_usage=0,
               channel_3_usage=0,
               channel_4_usage=0)
    run_relaycontrol(imei=imei_number,
                     channel_1_device="Geyser",
                     channel_2_device="disconnected",
                     channel_3_device="disconnected",
                     channel_4_device="disconnected",
                     channel_1_state=True,
                     channel_2_state=False,
                     channel_3_state=False,
                     channel_4_state=False
                     )
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373070927340"
    imei_number = "868373070927340"
    run_heartbeat(
        imei=imei_number,
        brainFirmware_version="1.1.0.3",
        reboot_timestamp="2025-09-02T05:47:00Z",
        general_system_state=True,
        inverter_coms_state=True,
        relay_pair_state=True,
        devices_state=True,
        system_control_state=True,
        internal_state=True,
        relayFirmware_version="3.5.1.12",
        gosolr_version="-",
        edge_version="-",
        east_version="-",
        pair_version="-",
        manager_version="-",
        parsec_version="-",
        inverter_type="-",
        order_number="-",
        inverter_sn="-"
    )
    run_relays(imei=imei_number,
               relay_pair_state=True,
               channel_1_device="Geyser",
               channel_2_device="disconnected",
               channel_3_device="disconnected",
               channel_4_device="disconnected",
               channel_1_mode=False,
               channel_2_mode=False,
               channel_3_mode=False,
               channel_4_mode=False,
               channel_1_usage=round(random.uniform(2600, 3200), 1),
               channel_2_usage=0,
               channel_3_usage=0,
               channel_4_usage=0)
    run_relaycontrol(imei=imei_number,
                     channel_1_device="Geyser",
                     channel_2_device="disconnected",
                     channel_3_device="disconnected",
                     channel_4_device="disconnected",
                     channel_1_state=True,
                     channel_2_state=False,
                     channel_3_state=False,
                     channel_4_state=False
                     )
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373070933496"
    imei_number = "868373070933496"
    run_heartbeat(
        imei=imei_number,
        brainFirmware_version="1.1.0.3",
        reboot_timestamp="2025-09-02T05:47:00Z",
        general_system_state=True,
        inverter_coms_state=True,
        relay_pair_state=True,
        devices_state=True,
        system_control_state=True,
        internal_state=True,
        relayFirmware_version="3.5.1.12",
        gosolr_version="-",
        edge_version="-",
        east_version="-",
        pair_version="-",
        manager_version="-",
        parsec_version="-",
        inverter_type="-",
        order_number="-",
        inverter_sn="-"
    )
    run_relays(imei=imei_number,
               relay_pair_state=True,
               channel_1_device="Geyser",
               channel_2_device="disconnected",
               channel_3_device="disconnected",
               channel_4_device="disconnected",
               channel_1_mode=False,
               channel_2_mode=False,
               channel_3_mode=False,
               channel_4_mode=False,
               channel_1_usage=round(random.uniform(2600, 3200), 1),
               channel_2_usage=0,
               channel_3_usage=0,
               channel_4_usage=0)
    run_relaycontrol(imei=imei_number,
                     channel_1_device="Geyser",
                     channel_2_device="disconnected",
                     channel_3_device="disconnected",
                     channel_4_device="disconnected",
                     channel_1_state=True,
                     channel_2_state=False,
                     channel_3_state=False,
                     channel_4_state=False
                     )
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373070933454"
    imei_number = "868373070933454"
    run_heartbeat(
        imei=imei_number,
        brainFirmware_version="1.1.0.3",
        reboot_timestamp="2025-09-02T05:47:00Z",
        general_system_state=True,
        inverter_coms_state=True,
        relay_pair_state=True,
        devices_state=True,
        system_control_state=True,
        internal_state=True,
        relayFirmware_version="3.5.1.12",
        gosolr_version="-",
        edge_version="-",
        east_version="-",
        pair_version="-",
        manager_version="-",
        parsec_version="-",
        inverter_type="-",
        order_number="-",
        inverter_sn="-"
    )
    run_relays(imei=imei_number,
               relay_pair_state=True,
               channel_1_device="Geyser",
               channel_2_device="disconnected",
               channel_3_device="disconnected",
               channel_4_device="disconnected",
               channel_1_mode=False,
               channel_2_mode=False,
               channel_3_mode=False,
               channel_4_mode=False,
               channel_1_usage=round(random.uniform(2600, 3200), 1),
               channel_2_usage=0,
               channel_3_usage=0,
               channel_4_usage=0)
    run_relaycontrol(imei=imei_number,
                     channel_1_device="Geyser",
                     channel_2_device="disconnected",
                     channel_3_device="disconnected",
                     channel_4_device="disconnected",
                     channel_1_state=True,
                     channel_2_state=False,
                     channel_3_state=False,
                     channel_4_state=False
                     )
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373070934379"
    imei_number = "868373070934379"
    run_heartbeat(
        imei=imei_number,
        brainFirmware_version="1.1.0.3",
        reboot_timestamp="2025-09-02T05:47:00Z",
        general_system_state=True,
        inverter_coms_state=True,
        relay_pair_state=True,
        devices_state=True,
        system_control_state=True,
        internal_state=True,
        relayFirmware_version="3.5.1.12",
        gosolr_version="-",
        edge_version="-",
        east_version="-",
        pair_version="-",
        manager_version="-",
        parsec_version="-",
        inverter_type="-",
        order_number="-",
        inverter_sn="-"
    )
    run_relays(imei=imei_number,
               relay_pair_state=True,
               channel_1_device="Geyser",
               channel_2_device="disconnected",
               channel_3_device="disconnected",
               channel_4_device="disconnected",
               channel_1_mode=False,
               channel_2_mode=False,
               channel_3_mode=False,
               channel_4_mode=False,
               channel_1_usage=round(random.uniform(2600, 3200), 1),
               channel_2_usage=0,
               channel_3_usage=0,
               channel_4_usage=0)
    run_relaycontrol(imei=imei_number,
                     channel_1_device="Geyser",
                     channel_2_device="disconnected",
                     channel_3_device="disconnected",
                     channel_4_device="disconnected",
                     channel_1_state=True,
                     channel_2_state=False,
                     channel_3_state=False,
                     channel_4_state=False
                     )
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373070917101"
    imei_number = "868373070917101"
    run_heartbeat(
        imei=imei_number,
        brainFirmware_version="1.1.0.3",
        reboot_timestamp="2025-09-02T05:47:00Z",
        general_system_state=True,
        inverter_coms_state=True,
        relay_pair_state=True,
        devices_state=True,
        system_control_state=True,
        internal_state=True,
        relayFirmware_version="3.5.1.12",
        gosolr_version="-",
        edge_version="-",
        east_version="-",
        pair_version="-",
        manager_version="-",
        parsec_version="-",
        inverter_type="-",
        order_number="-",
        inverter_sn="-"
    )
    run_relays(imei=imei_number,
               relay_pair_state=True,
               channel_1_device="Geyser",
               channel_2_device="disconnected",
               channel_3_device="disconnected",
               channel_4_device="disconnected",
               channel_1_mode=False,
               channel_2_mode=False,
               channel_3_mode=False,
               channel_4_mode=False,
               channel_1_usage=round(random.uniform(2600, 3200), 1),
               channel_2_usage=0,
               channel_3_usage=0,
               channel_4_usage=0)
    run_relaycontrol(imei=imei_number,
                     channel_1_device="Geyser",
                     channel_2_device="disconnected",
                     channel_3_device="disconnected",
                     channel_4_device="disconnected",
                     channel_1_state=True,
                     channel_2_state=False,
                     channel_3_state=False,
                     channel_4_state=False
                     )
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373070931730"
    imei_number = "868373070931730"
    run_heartbeat(
        imei=imei_number,
        brainFirmware_version="1.1.0.3",
        reboot_timestamp="2025-09-02T05:47:00Z",
        general_system_state=True,
        inverter_coms_state=True,
        relay_pair_state=True,
        devices_state=True,
        system_control_state=True,
        internal_state=True,
        relayFirmware_version="3.5.1.12",
        gosolr_version="-",
        edge_version="-",
        east_version="-",
        pair_version="-",
        manager_version="-",
        parsec_version="-",
        inverter_type="-",
        order_number="-",
        inverter_sn="-"
    )
    run_relays(imei=imei_number,
               relay_pair_state=True,
               channel_1_device="Geyser",
               channel_2_device="disconnected",
               channel_3_device="disconnected",
               channel_4_device="disconnected",
               channel_1_mode=False,
               channel_2_mode=False,
               channel_3_mode=False,
               channel_4_mode=False,
               channel_1_usage=round(random.uniform(2600, 3200), 1),
               channel_2_usage=0,
               channel_3_usage=0,
               channel_4_usage=0)
    run_relaycontrol(imei=imei_number,
                     channel_1_device="Geyser",
                     channel_2_device="disconnected",
                     channel_3_device="disconnected",
                     channel_4_device="disconnected",
                     channel_1_state=True,
                     channel_2_state=False,
                     channel_3_state=False,
                     channel_4_state=False
                     )
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373070933755"
    imei_number = "868373070933755"
    run_heartbeat(
        imei=imei_number,
        brainFirmware_version="1.1.0.3",
        reboot_timestamp="2025-09-02T05:47:00Z",
        general_system_state=True,
        inverter_coms_state=True,
        relay_pair_state=True,
        devices_state=True,
        system_control_state=True,
        internal_state=True,
        relayFirmware_version="3.5.1.12",
        gosolr_version="-",
        edge_version="-",
        east_version="-",
        pair_version="-",
        manager_version="-",
        parsec_version="-",
        inverter_type="-",
        order_number="-",
        inverter_sn="-"
    )
    run_relays(imei=imei_number,
               relay_pair_state=True,
               channel_1_device="Geyser",
               channel_2_device="disconnected",
               channel_3_device="disconnected",
               channel_4_device="disconnected",
               channel_1_mode=False,
               channel_2_mode=False,
               channel_3_mode=False,
               channel_4_mode=False,
               channel_1_usage=round(random.uniform(2600, 3200), 1),
               channel_2_usage=0,
               channel_3_usage=0,
               channel_4_usage=0)
    run_relaycontrol(imei=imei_number,
                     channel_1_device="Geyser",
                     channel_2_device="disconnected",
                     channel_3_device="disconnected",
                     channel_4_device="disconnected",
                     channel_1_state=True,
                     channel_2_state=False,
                     channel_3_state=False,
                     channel_4_state=False
                     )
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373070926882"
    imei_number = "868373070926882"
    run_heartbeat(
        imei=imei_number,
        brainFirmware_version="1.1.0.3",
        reboot_timestamp="2025-09-02T05:47:00Z",
        general_system_state=True,
        inverter_coms_state=True,
        relay_pair_state=True,
        devices_state=True,
        system_control_state=True,
        internal_state=True,
        relayFirmware_version="3.5.1.12",
        gosolr_version="-",
        edge_version="-",
        east_version="-",
        pair_version="-",
        manager_version="-",
        parsec_version="-",
        inverter_type="-",
        order_number="-",
        inverter_sn="-"
    )
    run_relays(imei=imei_number,
               relay_pair_state=True,
               channel_1_device="Geyser",
               channel_2_device="disconnected",
               channel_3_device="disconnected",
               channel_4_device="disconnected",
               channel_1_mode=False,
               channel_2_mode=False,
               channel_3_mode=False,
               channel_4_mode=False,
               channel_1_usage=round(random.uniform(2600, 3200), 1),
               channel_2_usage=0,
               channel_3_usage=0,
               channel_4_usage=0)
    run_relaycontrol(imei=imei_number,
                     channel_1_device="Geyser",
                     channel_2_device="disconnected",
                     channel_3_device="disconnected",
                     channel_4_device="disconnected",
                     channel_1_state=True,
                     channel_2_state=False,
                     channel_3_state=False,
                     channel_4_state=False
                     )
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373070916269"
    imei_number = "868373070916269"
    run_heartbeat(
        imei=imei_number,
        brainFirmware_version="1.1.0.3",
        reboot_timestamp="2025-09-02T05:47:00Z",
        general_system_state=True,
        inverter_coms_state=True,
        relay_pair_state=True,
        devices_state=True,
        system_control_state=True,
        internal_state=True,
        relayFirmware_version="3.5.1.12",
        gosolr_version="-",
        edge_version="-",
        east_version="-",
        pair_version="-",
        manager_version="-",
        parsec_version="-",
        inverter_type="-",
        order_number="-",
        inverter_sn="-"
    )
    run_relays(imei=imei_number,
               relay_pair_state=True,
               channel_1_device="Geyser",
               channel_2_device="disconnected",
               channel_3_device="disconnected",
               channel_4_device="disconnected",
               channel_1_mode=False,
               channel_2_mode=False,
               channel_3_mode=False,
               channel_4_mode=False,
               channel_1_usage=round(random.uniform(2600, 3200), 1),
               channel_2_usage=0,
               channel_3_usage=0,
               channel_4_usage=0)
    run_relaycontrol(imei=imei_number,
                     channel_1_device="Geyser",
                     channel_2_device="disconnected",
                     channel_3_device="disconnected",
                     channel_4_device="disconnected",
                     channel_1_state=True,
                     channel_2_state=False,
                     channel_3_state=False,
                     channel_4_state=False
                     )
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373072915657"
    imei_number = "868373072915657"
    run_heartbeat(
        imei=imei_number,
        brainFirmware_version="1.1.0.3",
        reboot_timestamp="2025-09-02T05:47:00Z",
        general_system_state=True,
        inverter_coms_state=True,
        relay_pair_state=True,
        devices_state=True,
        system_control_state=True,
        internal_state=True,
        relayFirmware_version="3.5.1.12",
        gosolr_version="-",
        edge_version="-",
        east_version="-",
        pair_version="-",
        manager_version="-",
        parsec_version="-",
        inverter_type="-",
        order_number="-",
        inverter_sn="-"
    )
    run_relays(imei=imei_number,
               relay_pair_state=True,
               channel_1_device="Geyser",
               channel_2_device="disconnected",
               channel_3_device="disconnected",
               channel_4_device="disconnected",
               channel_1_mode=False,
               channel_2_mode=False,
               channel_3_mode=False,
               channel_4_mode=False,
               channel_1_usage=round(random.uniform(2600, 3200), 1),
               channel_2_usage=0,
               channel_3_usage=0,
               channel_4_usage=0)
    run_relaycontrol(imei=imei_number,
                     channel_1_device="Geyser",
                     channel_2_device="disconnected",
                     channel_3_device="disconnected",
                     channel_4_device="disconnected",
                     channel_1_state=True,
                     channel_2_state=False,
                     channel_3_state=False,
                     channel_4_state=False
                     )
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373072936455"
    imei_number = "868373072936455"
    run_heartbeat(
        imei=imei_number,
        brainFirmware_version="1.1.0.3",
        reboot_timestamp="2025-09-02T05:47:00Z",
        general_system_state=True,
        inverter_coms_state=True,
        relay_pair_state=True,
        devices_state=True,
        system_control_state=True,
        internal_state=True,
        relayFirmware_version="3.5.1.12",
        gosolr_version="-",
        edge_version="-",
        east_version="-",
        pair_version="-",
        manager_version="-",
        parsec_version="-",
        inverter_type="-",
        order_number="-",
        inverter_sn="-"
    )
    run_relays(imei=imei_number,
               relay_pair_state=True,
               channel_1_device="Geyser",
               channel_2_device="disconnected",
               channel_3_device="disconnected",
               channel_4_device="disconnected",
               channel_1_mode=False,
               channel_2_mode=False,
               channel_3_mode=False,
               channel_4_mode=False,
               channel_1_usage=round(random.uniform(2600, 3200), 1),
               channel_2_usage=0,
               channel_3_usage=0,
               channel_4_usage=0)
    run_relaycontrol(imei=imei_number,
                     channel_1_device="Geyser",
                     channel_2_device="disconnected",
                     channel_3_device="disconnected",
                     channel_4_device="disconnected",
                     channel_1_state=True,
                     channel_2_state=False,
                     channel_3_state=False,
                     channel_4_state=False
                     )
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373070916137"
    imei_number = "868373070916137"
    run_heartbeat(
        imei=imei_number,
        brainFirmware_version="1.1.0.3",
        reboot_timestamp="2025-09-02T05:47:00Z",
        general_system_state=True,
        inverter_coms_state=True,
        relay_pair_state=True,
        devices_state=True,
        system_control_state=True,
        internal_state=True,
        relayFirmware_version="3.5.1.12",
        gosolr_version="-",
        edge_version="-",
        east_version="-",
        pair_version="-",
        manager_version="-",
        parsec_version="-",
        inverter_type="-",
        order_number="-",
        inverter_sn="-"
    )
    run_relays(imei=imei_number,
               relay_pair_state=True,
               channel_1_device="Geyser",
               channel_2_device="disconnected",
               channel_3_device="disconnected",
               channel_4_device="disconnected",
               channel_1_mode=False,
               channel_2_mode=False,
               channel_3_mode=False,
               channel_4_mode=False,
               channel_1_usage=round(random.uniform(2600, 3200), 1),
               channel_2_usage=0,
               channel_3_usage=0,
               channel_4_usage=0)
    run_relaycontrol(imei=imei_number,
                     channel_1_device="Geyser",
                     channel_2_device="disconnected",
                     channel_3_device="disconnected",
                     channel_4_device="disconnected",
                     channel_1_state=True,
                     channel_2_state=False,
                     channel_3_state=False,
                     channel_4_state=False
                     )
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373070929957"
    imei_number = "868373070929957"
    run_heartbeat(
        imei=imei_number,
        brainFirmware_version="1.1.0.3",
        reboot_timestamp="2025-09-02T05:47:00Z",
        general_system_state=True,
        inverter_coms_state=True,
        relay_pair_state=True,
        devices_state=True,
        system_control_state=True,
        internal_state=True,
        relayFirmware_version="3.5.1.12",
        gosolr_version="-",
        edge_version="-",
        east_version="-",
        pair_version="-",
        manager_version="-",
        parsec_version="-",
        inverter_type="-",
        order_number="-",
        inverter_sn="-"
    )
    run_relays(imei=imei_number,
               relay_pair_state=True,
               channel_1_device="Geyser",
               channel_2_device="disconnected",
               channel_3_device="disconnected",
               channel_4_device="disconnected",
               channel_1_mode=False,
               channel_2_mode=False,
               channel_3_mode=False,
               channel_4_mode=False,
               channel_1_usage=round(random.uniform(2600, 3200), 1),
               channel_2_usage=0,
               channel_3_usage=0,
               channel_4_usage=0)
    run_relaycontrol(imei=imei_number,
                     channel_1_device="Geyser",
                     channel_2_device="disconnected",
                     channel_3_device="disconnected",
                     channel_4_device="disconnected",
                     channel_1_state=True,
                     channel_2_state=False,
                     channel_3_state=False,
                     channel_4_state=False
                     )
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373070916855"
    imei_number = "868373070916855"
    run_heartbeat(
        imei=imei_number,
        brainFirmware_version="1.1.0.3",
        reboot_timestamp="2025-09-02T05:47:00Z",
        general_system_state=True,
        inverter_coms_state=True,
        relay_pair_state=True,
        devices_state=True,
        system_control_state=True,
        internal_state=True,
        relayFirmware_version="3.5.1.12",
        gosolr_version="-",
        edge_version="-",
        east_version="-",
        pair_version="-",
        manager_version="-",
        parsec_version="-",
        inverter_type="-",
        order_number="-",
        inverter_sn="-"
    )
    run_relays(imei=imei_number,
               relay_pair_state=True,
               channel_1_device="Geyser",
               channel_2_device="disconnected",
               channel_3_device="disconnected",
               channel_4_device="disconnected",
               channel_1_mode=False,
               channel_2_mode=False,
               channel_3_mode=False,
               channel_4_mode=False,
               channel_1_usage=round(random.uniform(2600, 3200), 1),
               channel_2_usage=0,
               channel_3_usage=0,
               channel_4_usage=0)
    run_relaycontrol(imei=imei_number,
                     channel_1_device="Geyser",
                     channel_2_device="disconnected",
                     channel_3_device="disconnected",
                     channel_4_device="disconnected",
                     channel_1_state=True,
                     channel_2_state=False,
                     channel_3_state=False,
                     channel_4_state=False
                     )
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373070929577"
    imei_number = "868373070929577"
    run_heartbeat(
        imei=imei_number,
        brainFirmware_version="1.1.0.3",
        reboot_timestamp="2025-09-02T05:47:00Z",
        general_system_state=True,
        inverter_coms_state=True,
        relay_pair_state=True,
        devices_state=True,
        system_control_state=True,
        internal_state=True,
        relayFirmware_version="3.5.1.12",
        gosolr_version="-",
        edge_version="-",
        east_version="-",
        pair_version="-",
        manager_version="-",
        parsec_version="-",
        inverter_type="-",
        order_number="-",
        inverter_sn="-"
    )
    run_relays(imei=imei_number,
               relay_pair_state=True,
               channel_1_device="Geyser",
               channel_2_device="disconnected",
               channel_3_device="disconnected",
               channel_4_device="disconnected",
               channel_1_mode=False,
               channel_2_mode=False,
               channel_3_mode=False,
               channel_4_mode=False,
               channel_1_usage=round(random.uniform(2600, 3200), 1),
               channel_2_usage=0,
               channel_3_usage=0,
               channel_4_usage=0)
    run_relaycontrol(imei=imei_number,
                     channel_1_device="Geyser",
                     channel_2_device="disconnected",
                     channel_3_device="disconnected",
                     channel_4_device="disconnected",
                     channel_1_state=True,
                     channel_2_state=False,
                     channel_3_state=False,
                     channel_4_state=False
                     )
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373070935863"
    imei_number = "868373070935863"
    run_heartbeat(
        imei=imei_number,
        brainFirmware_version="1.1.0.3",
        reboot_timestamp="2025-09-02T05:47:00Z",
        general_system_state=True,
        inverter_coms_state=True,
        relay_pair_state=True,
        devices_state=True,
        system_control_state=True,
        internal_state=True,
        relayFirmware_version="3.5.1.12",
        gosolr_version="-",
        edge_version="-",
        east_version="-",
        pair_version="-",
        manager_version="-",
        parsec_version="-",
        inverter_type="-",
        order_number="-",
        inverter_sn="-"
    )
    run_relays(imei=imei_number,
               relay_pair_state=True,
               channel_1_device="Geyser",
               channel_2_device="disconnected",
               channel_3_device="disconnected",
               channel_4_device="disconnected",
               channel_1_mode=False,
               channel_2_mode=False,
               channel_3_mode=False,
               channel_4_mode=False,
               channel_1_usage=round(random.uniform(2600, 3200), 1),
               channel_2_usage=0,
               channel_3_usage=0,
               channel_4_usage=0)
    run_relaycontrol(imei=imei_number,
                     channel_1_device="Geyser",
                     channel_2_device="disconnected",
                     channel_3_device="disconnected",
                     channel_4_device="disconnected",
                     channel_1_state=True,
                     channel_2_state=False,
                     channel_3_state=False,
                     channel_4_state=False
                     )
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373070916665"
    imei_number = "868373070916665"
    run_heartbeat(
        imei=imei_number,
        brainFirmware_version="1.1.0.3",
        reboot_timestamp="2025-09-02T05:47:00Z",
        general_system_state=True,
        inverter_coms_state=True,
        relay_pair_state=True,
        devices_state=True,
        system_control_state=True,
        internal_state=True,
        relayFirmware_version="3.5.1.12",
        gosolr_version="-",
        edge_version="-",
        east_version="-",
        pair_version="-",
        manager_version="-",
        parsec_version="-",
        inverter_type="-",
        order_number="-",
        inverter_sn="-"
    )
    run_relays(imei=imei_number,
               relay_pair_state=True,
               channel_1_device="Geyser",
               channel_2_device="disconnected",
               channel_3_device="disconnected",
               channel_4_device="disconnected",
               channel_1_mode=False,
               channel_2_mode=False,
               channel_3_mode=False,
               channel_4_mode=False,
               channel_1_usage=round(random.uniform(2600, 3200), 1),
               channel_2_usage=0,
               channel_3_usage=0,
               channel_4_usage=0)
    run_relaycontrol(imei=imei_number,
                     channel_1_device="Geyser",
                     channel_2_device="disconnected",
                     channel_3_device="disconnected",
                     channel_4_device="disconnected",
                     channel_1_state=True,
                     channel_2_state=False,
                     channel_3_state=False,
                     channel_4_state=False
                     )
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373070930195"
    imei_number = "868373070930195"
    run_heartbeat(
        imei=imei_number,
        brainFirmware_version="1.1.0.3",
        reboot_timestamp="2025-09-02T05:47:00Z",
        general_system_state=True,
        inverter_coms_state=True,
        relay_pair_state=True,
        devices_state=True,
        system_control_state=True,
        internal_state=True,
        relayFirmware_version="3.5.1.12",
        gosolr_version="-",
        edge_version="-",
        east_version="-",
        pair_version="-",
        manager_version="-",
        parsec_version="-",
        inverter_type="-",
        order_number="-",
        inverter_sn="-"
    )
    run_relays(imei=imei_number,
               relay_pair_state=True,
               channel_1_device="Geyser",
               channel_2_device="disconnected",
               channel_3_device="disconnected",
               channel_4_device="disconnected",
               channel_1_mode=False,
               channel_2_mode=False,
               channel_3_mode=False,
               channel_4_mode=False,
               channel_1_usage=round(random.uniform(2600, 3200), 1),
               channel_2_usage=0,
               channel_3_usage=0,
               channel_4_usage=0)
    run_relaycontrol(imei=imei_number,
                     channel_1_device="Geyser",
                     channel_2_device="disconnected",
                     channel_3_device="disconnected",
                     channel_4_device="disconnected",
                     channel_1_state=True,
                     channel_2_state=False,
                     channel_3_state=False,
                     channel_4_state=False
                     )
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373070927829"
    imei_number = "868373070927829"
    run_heartbeat(
        imei=imei_number,
        brainFirmware_version="1.1.0.3",
        reboot_timestamp="2025-09-02T05:47:00Z",
        general_system_state=True,
        inverter_coms_state=True,
        relay_pair_state=True,
        devices_state=True,
        system_control_state=True,
        internal_state=True,
        relayFirmware_version="3.5.1.12",
        gosolr_version="-",
        edge_version="-",
        east_version="-",
        pair_version="-",
        manager_version="-",
        parsec_version="-",
        inverter_type="-",
        order_number="-",
        inverter_sn="-"
    )
    run_relays(imei=imei_number,
               relay_pair_state=True,
               channel_1_device="Geyser",
               channel_2_device="disconnected",
               channel_3_device="disconnected",
               channel_4_device="disconnected",
               channel_1_mode=False,
               channel_2_mode=False,
               channel_3_mode=False,
               channel_4_mode=False,
               channel_1_usage=round(random.uniform(2600, 3200), 1),
               channel_2_usage=0,
               channel_3_usage=0,
               channel_4_usage=0)
    run_relaycontrol(imei=imei_number,
                     channel_1_device="Geyser",
                     channel_2_device="disconnected",
                     channel_3_device="disconnected",
                     channel_4_device="disconnected",
                     channel_1_state=True,
                     channel_2_state=False,
                     channel_3_state=False,
                     channel_4_state=False
                     )
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373070929981"
    imei_number = "868373070929981"
    run_heartbeat(
        imei=imei_number,
        brainFirmware_version="1.1.0.3",
        reboot_timestamp="2025-09-02T05:47:00Z",
        general_system_state=True,
        inverter_coms_state=True,
        relay_pair_state=True,
        devices_state=True,
        system_control_state=True,
        internal_state=True,
        relayFirmware_version="3.5.1.12",
        gosolr_version="-",
        edge_version="-",
        east_version="-",
        pair_version="-",
        manager_version="-",
        parsec_version="-",
        inverter_type="-",
        order_number="-",
        inverter_sn="-"
    )
    run_relays(imei=imei_number,
               relay_pair_state=True,
               channel_1_device="Geyser",
               channel_2_device="disconnected",
               channel_3_device="disconnected",
               channel_4_device="disconnected",
               channel_1_mode=False,
               channel_2_mode=False,
               channel_3_mode=False,
               channel_4_mode=False,
               channel_1_usage=round(random.uniform(2600, 3200), 1),
               channel_2_usage=0,
               channel_3_usage=0,
               channel_4_usage=0)
    run_relaycontrol(imei=imei_number,
                     channel_1_device="Geyser",
                     channel_2_device="disconnected",
                     channel_3_device="disconnected",
                     channel_4_device="disconnected",
                     channel_1_state=True,
                     channel_2_state=False,
                     channel_3_state=False,
                     channel_4_state=False
                     )
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373070928900"
    imei_number = "868373070928900"
    run_heartbeat(
        imei=imei_number,
        brainFirmware_version="1.1.0.3",
        reboot_timestamp="2025-09-02T05:47:00Z",
        general_system_state=True,
        inverter_coms_state=True,
        relay_pair_state=True,
        devices_state=True,
        system_control_state=True,
        internal_state=True,
        relayFirmware_version="3.5.1.12",
        gosolr_version="-",
        edge_version="-",
        east_version="-",
        pair_version="-",
        manager_version="-",
        parsec_version="-",
        inverter_type="-",
        order_number="-",
        inverter_sn="-"
    )
    run_relays(imei=imei_number,
               relay_pair_state=True,
               channel_1_device="Geyser",
               channel_2_device="disconnected",
               channel_3_device="disconnected",
               channel_4_device="disconnected",
               channel_1_mode=False,
               channel_2_mode=False,
               channel_3_mode=False,
               channel_4_mode=False,
               channel_1_usage=round(random.uniform(2600, 3200), 1),
               channel_2_usage=0,
               channel_3_usage=0,
               channel_4_usage=0)
    run_relaycontrol(imei=imei_number,
                     channel_1_device="Geyser",
                     channel_2_device="disconnected",
                     channel_3_device="disconnected",
                     channel_4_device="disconnected",
                     channel_1_state=True,
                     channel_2_state=False,
                     channel_3_state=False,
                     channel_4_state=False
                     )
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373070931201"
    imei_number = "868373070931201"
    run_heartbeat(
        imei=imei_number,
        brainFirmware_version="1.1.0.3",
        reboot_timestamp="2025-09-02T05:47:00Z",
        general_system_state=True,
        inverter_coms_state=True,
        relay_pair_state=True,
        devices_state=True,
        system_control_state=True,
        internal_state=True,
        relayFirmware_version="3.5.1.12",
        gosolr_version="-",
        edge_version="-",
        east_version="-",
        pair_version="-",
        manager_version="-",
        parsec_version="-",
        inverter_type="-",
        order_number="-",
        inverter_sn="-"
    )
    run_relays(imei=imei_number,
               relay_pair_state=True,
               channel_1_device="Geyser",
               channel_2_device="disconnected",
               channel_3_device="disconnected",
               channel_4_device="disconnected",
               channel_1_mode=False,
               channel_2_mode=False,
               channel_3_mode=False,
               channel_4_mode=False,
               channel_1_usage=round(random.uniform(2600, 3200), 1),
               channel_2_usage=0,
               channel_3_usage=0,
               channel_4_usage=0)
    run_relaycontrol(imei=imei_number,
                     channel_1_device="Geyser",
                     channel_2_device="disconnected",
                     channel_3_device="disconnected",
                     channel_4_device="disconnected",
                     channel_1_state=True,
                     channel_2_state=False,
                     channel_3_state=False,
                     channel_4_state=False
                     )
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373070932076"
    imei_number = "868373070932076"
    run_heartbeat(
        imei=imei_number,
        brainFirmware_version="1.1.0.3",
        reboot_timestamp="2025-09-02T05:47:00Z",
        general_system_state=True,
        inverter_coms_state=True,
        relay_pair_state=True,
        devices_state=True,
        system_control_state=True,
        internal_state=True,
        relayFirmware_version="3.5.1.12",
        gosolr_version="-",
        edge_version="-",
        east_version="-",
        pair_version="-",
        manager_version="-",
        parsec_version="-",
        inverter_type="-",
        order_number="-",
        inverter_sn="-"
    )
    run_relays(imei=imei_number,
               relay_pair_state=True,
               channel_1_device="Geyser",
               channel_2_device="disconnected",
               channel_3_device="disconnected",
               channel_4_device="disconnected",
               channel_1_mode=False,
               channel_2_mode=False,
               channel_3_mode=False,
               channel_4_mode=False,
               channel_1_usage=round(random.uniform(2600, 3200), 1),
               channel_2_usage=0,
               channel_3_usage=0,
               channel_4_usage=0)
    run_relaycontrol(imei=imei_number,
                     channel_1_device="Geyser",
                     channel_2_device="disconnected",
                     channel_3_device="disconnected",
                     channel_4_device="disconnected",
                     channel_1_state=True,
                     channel_2_state=False,
                     channel_3_state=False,
                     channel_4_state=False
                     )
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373070930500"
    imei_number = "868373070930500"
    run_heartbeat(
        imei=imei_number,
        brainFirmware_version="1.1.0.3",
        reboot_timestamp="2025-09-02T05:47:00Z",
        general_system_state=True,
        inverter_coms_state=True,
        relay_pair_state=True,
        devices_state=True,
        system_control_state=True,
        internal_state=True,
        relayFirmware_version="3.5.1.12",
        gosolr_version="-",
        edge_version="-",
        east_version="-",
        pair_version="-",
        manager_version="-",
        parsec_version="-",
        inverter_type="-",
        order_number="-",
        inverter_sn="-"
    )
    run_relays(imei=imei_number,
               relay_pair_state=True,
               channel_1_device="Geyser",
               channel_2_device="disconnected",
               channel_3_device="disconnected",
               channel_4_device="disconnected",
               channel_1_mode=False,
               channel_2_mode=False,
               channel_3_mode=False,
               channel_4_mode=False,
               channel_1_usage=round(random.uniform(2600, 3200), 1),
               channel_2_usage=0,
               channel_3_usage=0,
               channel_4_usage=0)
    run_relaycontrol(imei=imei_number,
                     channel_1_device="Geyser",
                     channel_2_device="disconnected",
                     channel_3_device="disconnected",
                     channel_4_device="disconnected",
                     channel_1_state=True,
                     channel_2_state=False,
                     channel_3_state=False,
                     channel_4_state=False
                     )
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373070929007"
    imei_number = "868373070929007"
    run_heartbeat(
        imei=imei_number,
        brainFirmware_version="1.1.0.3",
        reboot_timestamp="2025-09-02T05:47:00Z",
        general_system_state=True,
        inverter_coms_state=True,
        relay_pair_state=True,
        devices_state=True,
        system_control_state=True,
        internal_state=True,
        relayFirmware_version="3.5.1.12",
        gosolr_version="-",
        edge_version="-",
        east_version="-",
        pair_version="-",
        manager_version="-",
        parsec_version="-",
        inverter_type="-",
        order_number="-",
        inverter_sn="-"
    )
    run_relays(imei=imei_number,
               relay_pair_state=True,
               channel_1_device="Geyser",
               channel_2_device="disconnected",
               channel_3_device="disconnected",
               channel_4_device="disconnected",
               channel_1_mode=False,
               channel_2_mode=False,
               channel_3_mode=False,
               channel_4_mode=False,
               channel_1_usage=round(random.uniform(2600, 3200), 1),
               channel_2_usage=0,
               channel_3_usage=0,
               channel_4_usage=0)
    run_relaycontrol(imei=imei_number,
                     channel_1_device="Geyser",
                     channel_2_device="disconnected",
                     channel_3_device="disconnected",
                     channel_4_device="disconnected",
                     channel_1_state=True,
                     channel_2_state=False,
                     channel_3_state=False,
                     channel_4_state=False
                     )
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373070921061"
    imei_number = "868373070921061"
    run_heartbeat(
        imei=imei_number,
        brainFirmware_version="1.1.0.3",
        reboot_timestamp="2025-09-02T05:47:00Z",
        general_system_state=True,
        inverter_coms_state=True,
        relay_pair_state=True,
        devices_state=True,
        system_control_state=True,
        internal_state=True,
        relayFirmware_version="3.5.1.12",
        gosolr_version="-",
        edge_version="-",
        east_version="-",
        pair_version="-",
        manager_version="-",
        parsec_version="-",
        inverter_type="-",
        order_number="-",
        inverter_sn="-"
    )
    run_relays(imei=imei_number,
               relay_pair_state=True,
               channel_1_device="Geyser",
               channel_2_device="disconnected",
               channel_3_device="disconnected",
               channel_4_device="disconnected",
               channel_1_mode=False,
               channel_2_mode=False,
               channel_3_mode=False,
               channel_4_mode=False,
               channel_1_usage=round(random.uniform(2600, 3200), 1),
               channel_2_usage=0,
               channel_3_usage=0,
               channel_4_usage=0)
    run_relaycontrol(imei=imei_number,
                     channel_1_device="Geyser",
                     channel_2_device="disconnected",
                     channel_3_device="disconnected",
                     channel_4_device="disconnected",
                     channel_1_state=True,
                     channel_2_state=False,
                     channel_3_state=False,
                     channel_4_state=False
                     )
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373070928959"
    imei_number = "868373070928959"
    run_heartbeat(
        imei=imei_number,
        brainFirmware_version="1.1.0.3",
        reboot_timestamp="2025-09-02T05:47:00Z",
        general_system_state=True,
        inverter_coms_state=True,
        relay_pair_state=True,
        devices_state=True,
        system_control_state=True,
        internal_state=True,
        relayFirmware_version="3.5.1.12",
        gosolr_version="-",
        edge_version="-",
        east_version="-",
        pair_version="-",
        manager_version="-",
        parsec_version="-",
        inverter_type="-",
        order_number="-",
        inverter_sn="-"
    )
    run_relays(imei=imei_number,
               relay_pair_state=True,
               channel_1_device="Geyser",
               channel_2_device="disconnected",
               channel_3_device="disconnected",
               channel_4_device="disconnected",
               channel_1_mode=False,
               channel_2_mode=False,
               channel_3_mode=False,
               channel_4_mode=False,
               channel_1_usage=round(random.uniform(2600, 3200), 1),
               channel_2_usage=0,
               channel_3_usage=0,
               channel_4_usage=0)
    run_relaycontrol(imei=imei_number,
                     channel_1_device="Geyser",
                     channel_2_device="disconnected",
                     channel_3_device="disconnected",
                     channel_4_device="disconnected",
                     channel_1_state=True,
                     channel_2_state=False,
                     channel_3_state=False,
                     channel_4_state=False
                     )
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373070931359"
    imei_number = "868373070931359"
    run_heartbeat(
        imei=imei_number,
        brainFirmware_version="1.1.0.3",
        reboot_timestamp="2025-09-02T05:47:00Z",
        general_system_state=True,
        inverter_coms_state=True,
        relay_pair_state=True,
        devices_state=True,
        system_control_state=True,
        internal_state=True,
        relayFirmware_version="3.5.1.12",
        gosolr_version="-",
        edge_version="-",
        east_version="-",
        pair_version="-",
        manager_version="-",
        parsec_version="-",
        inverter_type="-",
        order_number="-",
        inverter_sn="-"
    )
    run_relays(imei=imei_number,
               relay_pair_state=True,
               channel_1_device="Geyser",
               channel_2_device="disconnected",
               channel_3_device="disconnected",
               channel_4_device="disconnected",
               channel_1_mode=False,
               channel_2_mode=False,
               channel_3_mode=False,
               channel_4_mode=False,
               channel_1_usage=round(random.uniform(2600, 3200), 1),
               channel_2_usage=0,
               channel_3_usage=0,
               channel_4_usage=0)
    run_relaycontrol(imei=imei_number,
                     channel_1_device="Geyser",
                     channel_2_device="disconnected",
                     channel_3_device="disconnected",
                     channel_4_device="disconnected",
                     channel_1_state=True,
                     channel_2_state=False,
                     channel_3_state=False,
                     channel_4_state=False
                     )
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373070934783"
    imei_number = "868373070934783"
    run_heartbeat(
        imei=imei_number,
        brainFirmware_version="1.1.0.3",
        reboot_timestamp="2025-09-02T05:47:00Z",
        general_system_state=True,
        inverter_coms_state=True,
        relay_pair_state=True,
        devices_state=True,
        system_control_state=True,
        internal_state=True,
        relayFirmware_version="3.5.1.12",
        gosolr_version="-",
        edge_version="-",
        east_version="-",
        pair_version="-",
        manager_version="-",
        parsec_version="-",
        inverter_type="-",
        order_number="-",
        inverter_sn="-"
    )
    run_relays(imei=imei_number,
               relay_pair_state=True,
               channel_1_device="Geyser",
               channel_2_device="disconnected",
               channel_3_device="disconnected",
               channel_4_device="disconnected",
               channel_1_mode=False,
               channel_2_mode=False,
               channel_3_mode=False,
               channel_4_mode=False,
               channel_1_usage=round(random.uniform(2600, 3200), 1),
               channel_2_usage=0,
               channel_3_usage=0,
               channel_4_usage=0)
    run_relaycontrol(imei=imei_number,
                     channel_1_device="Geyser",
                     channel_2_device="disconnected",
                     channel_3_device="disconnected",
                     channel_4_device="disconnected",
                     channel_1_state=True,
                     channel_2_state=False,
                     channel_3_state=False,
                     channel_4_state=False
                     )
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373070915956"
    imei_number = "868373070915956"
    run_heartbeat(
        imei=imei_number,
        brainFirmware_version="1.1.0.3",
        reboot_timestamp="2025-09-02T05:47:00Z",
        general_system_state=True,
        inverter_coms_state=True,
        relay_pair_state=True,
        devices_state=True,
        system_control_state=True,
        internal_state=True,
        relayFirmware_version="3.5.1.12",
        gosolr_version="-",
        edge_version="-",
        east_version="-",
        pair_version="-",
        manager_version="-",
        parsec_version="-",
        inverter_type="-",
        order_number="-",
        inverter_sn="-"
    )
    run_relays(imei=imei_number,
               relay_pair_state=True,
               channel_1_device="Geyser",
               channel_2_device="disconnected",
               channel_3_device="disconnected",
               channel_4_device="disconnected",
               channel_1_mode=False,
               channel_2_mode=False,
               channel_3_mode=False,
               channel_4_mode=False,
               channel_1_usage=round(random.uniform(2600, 3200), 1),
               channel_2_usage=0,
               channel_3_usage=0,
               channel_4_usage=0)
    run_relaycontrol(imei=imei_number,
                     channel_1_device="Geyser",
                     channel_2_device="disconnected",
                     channel_3_device="disconnected",
                     channel_4_device="disconnected",
                     channel_1_state=True,
                     channel_2_state=False,
                     channel_3_state=False,
                     channel_4_state=False
                     )
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373070930450"
    imei_number = "868373070930450"
    run_heartbeat(
        imei=imei_number,
        brainFirmware_version="1.1.0.3",
        reboot_timestamp="2025-09-02T05:47:00Z",
        general_system_state=True,
        inverter_coms_state=True,
        relay_pair_state=True,
        devices_state=True,
        system_control_state=True,
        internal_state=True,
        relayFirmware_version="3.5.1.12",
        gosolr_version="-",
        edge_version="-",
        east_version="-",
        pair_version="-",
        manager_version="-",
        parsec_version="-",
        inverter_type="-",
        order_number="-",
        inverter_sn="-"
    )
    run_relays(imei=imei_number,
               relay_pair_state=True,
               channel_1_device="Geyser",
               channel_2_device="disconnected",
               channel_3_device="disconnected",
               channel_4_device="disconnected",
               channel_1_mode=False,
               channel_2_mode=False,
               channel_3_mode=False,
               channel_4_mode=False,
               channel_1_usage=round(random.uniform(2600, 3200), 1),
               channel_2_usage=0,
               channel_3_usage=0,
               channel_4_usage=0)
    run_relaycontrol(imei=imei_number,
                     channel_1_device="Geyser",
                     channel_2_device="disconnected",
                     channel_3_device="disconnected",
                     channel_4_device="disconnected",
                     channel_1_state=True,
                     channel_2_state=False,
                     channel_3_state=False,
                     channel_4_state=False
                     )
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373070917143"
    imei_number = "868373070917143"
    run_heartbeat(
        imei=imei_number,
        brainFirmware_version="1.1.0.3",
        reboot_timestamp="2025-09-02T05:47:00Z",
        general_system_state=True,
        inverter_coms_state=True,
        relay_pair_state=True,
        devices_state=True,
        system_control_state=True,
        internal_state=True,
        relayFirmware_version="3.5.1.12",
        gosolr_version="-",
        edge_version="-",
        east_version="-",
        pair_version="-",
        manager_version="-",
        parsec_version="-",
        inverter_type="-",
        order_number="-",
        inverter_sn="-"
    )
    run_relays(imei=imei_number,
               relay_pair_state=True,
               channel_1_device="Geyser",
               channel_2_device="disconnected",
               channel_3_device="disconnected",
               channel_4_device="disconnected",
               channel_1_mode=False,
               channel_2_mode=False,
               channel_3_mode=False,
               channel_4_mode=False,
               channel_1_usage=round(random.uniform(2600, 3200), 1),
               channel_2_usage=0,
               channel_3_usage=0,
               channel_4_usage=0)
    run_relaycontrol(imei=imei_number,
                     channel_1_device="Geyser",
                     channel_2_device="disconnected",
                     channel_3_device="disconnected",
                     channel_4_device="disconnected",
                     channel_1_state=True,
                     channel_2_state=False,
                     channel_3_state=False,
                     channel_4_state=False
                     )
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373070926896"
    imei_number = "868373070926896"
    run_heartbeat(
        imei=imei_number,
        brainFirmware_version="1.1.0.3",
        reboot_timestamp="2025-09-02T05:47:00Z",
        general_system_state=True,
        inverter_coms_state=True,
        relay_pair_state=True,
        devices_state=True,
        system_control_state=True,
        internal_state=True,
        relayFirmware_version="3.5.1.12",
        gosolr_version="-",
        edge_version="-",
        east_version="-",
        pair_version="-",
        manager_version="-",
        parsec_version="-",
        inverter_type="-",
        order_number="-",
        inverter_sn="-"
    )
    run_relays(imei=imei_number,
               relay_pair_state=True,
               channel_1_device="Geyser",
               channel_2_device="disconnected",
               channel_3_device="disconnected",
               channel_4_device="disconnected",
               channel_1_mode=False,
               channel_2_mode=False,
               channel_3_mode=False,
               channel_4_mode=False,
               channel_1_usage=round(random.uniform(2600, 3200), 1),
               channel_2_usage=0,
               channel_3_usage=0,
               channel_4_usage=0)
    run_relaycontrol(imei=imei_number,
                     channel_1_device="Geyser",
                     channel_2_device="disconnected",
                     channel_3_device="disconnected",
                     channel_4_device="disconnected",
                     channel_1_state=True,
                     channel_2_state=False,
                     channel_3_state=False,
                     channel_4_state=False
                     )
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373070928876"
    imei_number = "868373070928876"
    run_heartbeat(
        imei=imei_number,
        brainFirmware_version="1.1.0.3",
        reboot_timestamp="2025-09-02T05:47:00Z",
        general_system_state=True,
        inverter_coms_state=True,
        relay_pair_state=True,
        devices_state=True,
        system_control_state=True,
        internal_state=True,
        relayFirmware_version="3.5.1.12",
        gosolr_version="-",
        edge_version="-",
        east_version="-",
        pair_version="-",
        manager_version="-",
        parsec_version="-",
        inverter_type="-",
        order_number="-",
        inverter_sn="-"
    )
    run_relays(imei=imei_number,
               relay_pair_state=True,
               channel_1_device="Geyser",
               channel_2_device="disconnected",
               channel_3_device="disconnected",
               channel_4_device="disconnected",
               channel_1_mode=False,
               channel_2_mode=False,
               channel_3_mode=False,
               channel_4_mode=False,
               channel_1_usage=round(random.uniform(2600, 3200), 1),
               channel_2_usage=0,
               channel_3_usage=0,
               channel_4_usage=0)
    run_relaycontrol(imei=imei_number,
                     channel_1_device="Geyser",
                     channel_2_device="disconnected",
                     channel_3_device="disconnected",
                     channel_4_device="disconnected",
                     channel_1_state=True,
                     channel_2_state=False,
                     channel_3_state=False,
                     channel_4_state=False
                     )
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373070928892"
    imei_number = "868373070928892"
    run_heartbeat(
        imei=imei_number,
        brainFirmware_version="1.1.0.3",
        reboot_timestamp="2025-09-02T05:47:00Z",
        general_system_state=True,
        inverter_coms_state=True,
        relay_pair_state=True,
        devices_state=True,
        system_control_state=True,
        internal_state=True,
        relayFirmware_version="3.5.1.12",
        gosolr_version="-",
        edge_version="-",
        east_version="-",
        pair_version="-",
        manager_version="-",
        parsec_version="-",
        inverter_type="-",
        order_number="-",
        inverter_sn="-"
    )
    run_relays(imei=imei_number,
               relay_pair_state=True,
               channel_1_device="Geyser",
               channel_2_device="disconnected",
               channel_3_device="disconnected",
               channel_4_device="disconnected",
               channel_1_mode=False,
               channel_2_mode=False,
               channel_3_mode=False,
               channel_4_mode=False,
               channel_1_usage=round(random.uniform(2600, 3200), 1),
               channel_2_usage=0,
               channel_3_usage=0,
               channel_4_usage=0)
    run_relaycontrol(imei=imei_number,
                     channel_1_device="Geyser",
                     channel_2_device="disconnected",
                     channel_3_device="disconnected",
                     channel_4_device="disconnected",
                     channel_1_state=True,
                     channel_2_state=False,
                     channel_3_state=False,
                     channel_4_state=False
                     )
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373070930344"
    imei_number = "868373070930344"
    run_heartbeat(
        imei=imei_number,
        brainFirmware_version="1.1.0.3",
        reboot_timestamp="2025-09-02T05:47:00Z",
        general_system_state=True,
        inverter_coms_state=True,
        relay_pair_state=True,
        devices_state=True,
        system_control_state=True,
        internal_state=True,
        relayFirmware_version="3.5.1.12",
        gosolr_version="-",
        edge_version="-",
        east_version="-",
        pair_version="-",
        manager_version="-",
        parsec_version="-",
        inverter_type="-",
        order_number="-",
        inverter_sn="-"
    )
    run_relays(imei=imei_number,
               relay_pair_state=True,
               channel_1_device="Geyser",
               channel_2_device="disconnected",
               channel_3_device="disconnected",
               channel_4_device="disconnected",
               channel_1_mode=False,
               channel_2_mode=False,
               channel_3_mode=False,
               channel_4_mode=False,
               channel_1_usage=round(random.uniform(2600, 3200), 1),
               channel_2_usage=0,
               channel_3_usage=0,
               channel_4_usage=0)
    run_relaycontrol(imei=imei_number,
                     channel_1_device="Geyser",
                     channel_2_device="disconnected",
                     channel_3_device="disconnected",
                     channel_4_device="disconnected",
                     channel_1_state=True,
                     channel_2_state=False,
                     channel_3_state=False,
                     channel_4_state=False
                     )
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373070926821"
    imei_number = "868373070926821"
    run_heartbeat(
        imei=imei_number,
        brainFirmware_version="1.1.0.3",
        reboot_timestamp="2025-09-02T05:47:00Z",
        general_system_state=True,
        inverter_coms_state=True,
        relay_pair_state=True,
        devices_state=True,
        system_control_state=True,
        internal_state=True,
        relayFirmware_version="3.5.1.12",
        gosolr_version="-",
        edge_version="-",
        east_version="-",
        pair_version="-",
        manager_version="-",
        parsec_version="-",
        inverter_type="-",
        order_number="-",
        inverter_sn="-"
    )
    run_relays(imei=imei_number,
               relay_pair_state=True,
               channel_1_device="Geyser",
               channel_2_device="disconnected",
               channel_3_device="disconnected",
               channel_4_device="disconnected",
               channel_1_mode=False,
               channel_2_mode=False,
               channel_3_mode=False,
               channel_4_mode=False,
               channel_1_usage=round(random.uniform(2600, 3200), 1),
               channel_2_usage=0,
               channel_3_usage=0,
               channel_4_usage=0)
    run_relaycontrol(imei=imei_number,
                     channel_1_device="Geyser",
                     channel_2_device="disconnected",
                     channel_3_device="disconnected",
                     channel_4_device="disconnected",
                     channel_1_state=True,
                     channel_2_state=False,
                     channel_3_state=False,
                     channel_4_state=False
                     )
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373070934882"
    imei_number = "868373070934882"
    run_heartbeat(
        imei=imei_number,
        brainFirmware_version="1.1.0.3",
        reboot_timestamp="2025-09-02T05:47:00Z",
        general_system_state=True,
        inverter_coms_state=True,
        relay_pair_state=True,
        devices_state=True,
        system_control_state=True,
        internal_state=True,
        relayFirmware_version="3.5.1.12",
        gosolr_version="-",
        edge_version="-",
        east_version="-",
        pair_version="-",
        manager_version="-",
        parsec_version="-",
        inverter_type="-",
        order_number="-",
        inverter_sn="-"
    )
    run_relays(imei=imei_number,
               relay_pair_state=True,
               channel_1_device="Geyser",
               channel_2_device="disconnected",
               channel_3_device="disconnected",
               channel_4_device="disconnected",
               channel_1_mode=False,
               channel_2_mode=False,
               channel_3_mode=False,
               channel_4_mode=False,
               channel_1_usage=round(random.uniform(2600, 3200), 1),
               channel_2_usage=0,
               channel_3_usage=0,
               channel_4_usage=0)
    run_relaycontrol(imei=imei_number,
                     channel_1_device="Geyser",
                     channel_2_device="disconnected",
                     channel_3_device="disconnected",
                     channel_4_device="disconnected",
                     channel_1_state=True,
                     channel_2_state=False,
                     channel_3_state=False,
                     channel_4_state=False
                     )
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373070926730"
    imei_number = "868373070926730"
    run_heartbeat(
        imei=imei_number,
        brainFirmware_version="1.1.0.3",
        reboot_timestamp="2025-09-02T05:47:00Z",
        general_system_state=True,
        inverter_coms_state=True,
        relay_pair_state=True,
        devices_state=True,
        system_control_state=True,
        internal_state=True,
        relayFirmware_version="3.5.1.12",
        gosolr_version="-",
        edge_version="-",
        east_version="-",
        pair_version="-",
        manager_version="-",
        parsec_version="-",
        inverter_type="-",
        order_number="-",
        inverter_sn="-"
    )
    run_relays(imei=imei_number,
               relay_pair_state=True,
               channel_1_device="Geyser",
               channel_2_device="disconnected",
               channel_3_device="disconnected",
               channel_4_device="disconnected",
               channel_1_mode=False,
               channel_2_mode=False,
               channel_3_mode=False,
               channel_4_mode=False,
               channel_1_usage=round(random.uniform(2600, 3200), 1),
               channel_2_usage=0,
               channel_3_usage=0,
               channel_4_usage=0)
    run_relaycontrol(imei=imei_number,
                     channel_1_device="Geyser",
                     channel_2_device="disconnected",
                     channel_3_device="disconnected",
                     channel_4_device="disconnected",
                     channel_1_state=True,
                     channel_2_state=False,
                     channel_3_state=False,
                     channel_4_state=False
                     )
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373070915865"
    imei_number = "868373070915865"
    run_heartbeat(
        imei=imei_number,
        brainFirmware_version="1.1.0.3",
        reboot_timestamp="2025-09-02T05:47:00Z",
        general_system_state=True,
        inverter_coms_state=True,
        relay_pair_state=True,
        devices_state=True,
        system_control_state=True,
        internal_state=True,
        relayFirmware_version="3.5.1.12",
        gosolr_version="-",
        edge_version="-",
        east_version="-",
        pair_version="-",
        manager_version="-",
        parsec_version="-",
        inverter_type="-",
        order_number="-",
        inverter_sn="-"
    )
    run_relays(imei=imei_number,
               relay_pair_state=True,
               channel_1_device="Geyser",
               channel_2_device="disconnected",
               channel_3_device="disconnected",
               channel_4_device="disconnected",
               channel_1_mode=False,
               channel_2_mode=False,
               channel_3_mode=False,
               channel_4_mode=False,
               channel_1_usage=round(random.uniform(2600, 3200), 1),
               channel_2_usage=0,
               channel_3_usage=0,
               channel_4_usage=0)
    run_relaycontrol(imei=imei_number,
                     channel_1_device="Geyser",
                     channel_2_device="disconnected",
                     channel_3_device="disconnected",
                     channel_4_device="disconnected",
                     channel_1_state=True,
                     channel_2_state=False,
                     channel_3_state=False,
                     channel_4_state=False
                     )
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373070920113"
    imei_number = "868373070920113"
    run_data(imei="868373070920113", inverter_serial="2506022294")
    run_heartbeat(
        imei=imei_number,
        brainFirmware_version="1.1.0.3",
        reboot_timestamp="2025-09-02T05:47:00Z",
        general_system_state=True,
        inverter_coms_state=True,
        relay_pair_state=True,
        devices_state=True,
        system_control_state=True,
        internal_state=True,
        relayFirmware_version="3.5.1.12",
        gosolr_version="-",
        edge_version="-",
        east_version="-",
        pair_version="-",
        manager_version="-",
        parsec_version="-",
        inverter_type="-",
        order_number="-",
        inverter_sn="-"
    )
    run_relays(imei=imei_number,
               relay_pair_state=True,
               channel_1_device="Geyser",
               channel_2_device="disconnected",
               channel_3_device="disconnected",
               channel_4_device="disconnected",
               channel_1_mode=False,
               channel_2_mode=False,
               channel_3_mode=False,
               channel_4_mode=False,
               channel_1_usage=round(random.uniform(2600, 3200), 1),
               channel_2_usage=0,
               channel_3_usage=0,
               channel_4_usage=0)
    run_relaycontrol(imei=imei_number,
                     channel_1_device="Geyser",
                     channel_2_device="disconnected",
                     channel_3_device="disconnected",
                     channel_4_device="disconnected",
                     channel_1_state=True,
                     channel_2_state=False,
                     channel_3_state=False,
                     channel_4_state=False
                     )
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-868373070934452"
    imei_number = "868373070934452"
    #run_data(imei="868373070934452", inverter_serial="2305108959")
    run_data_deye3p(imei="868373070934452", inverter_serial="2305108959")
except Exception as e:
    print(str(e))


try:
    CLIENT_ID = "brain-868373070920113"
    imei_number = "868373070920113"
    #run_data(imei="868373070920113", inverter_serial="2506022294")
    run_heartbeat(
        imei=imei_number,
        brainFirmware_version="1.1.0.3",
        reboot_timestamp="2025-09-03T08:07:00Z",
        general_system_state=False,
        inverter_coms_state=False,
        relay_pair_state=False,
        devices_state=False,
        system_control_state=False,
        internal_state=True,
        relayFirmware_version="3.5.1.12",
        gosolr_version="-",
        edge_version="-",
        east_version="-",
        pair_version="-",
        manager_version="-",
        parsec_version="-",
        inverter_type="deye-1p",
        order_number="105322",
        inverter_sn="2506022294"
    )
    run_relays(imei=imei_number,
               relay_pair_state=False,
               channel_1_device="Geyser",
               channel_2_device="Indeterminate device",
               channel_3_device="disconnected",
               channel_4_device="disconnected",
               channel_1_mode=False,
               channel_2_mode=False,
               channel_3_mode=False,
               channel_4_mode=False,
               channel_1_usage=round(random.uniform(2600, 3200), 1),
               channel_2_usage=round(random.uniform(2600, 3200), 1),
               channel_3_usage=0,
               channel_4_usage=0)
    run_relaycontrol(imei=imei_number,
                     channel_1_device="Geyser",
                     channel_2_device="Indeterminate device",
                     channel_3_device="disconnected",
                     channel_4_device="disconnected",
                     channel_1_state=True,
                     channel_2_state=True,
                     channel_3_state=False,
                     channel_4_state=False
                     )
    run_watchdog(imei=imei_number, deviceCount=4)
except Exception as e:
    print(str(e))


try:
    CLIENT_ID = "brain-868373070934429"
    imei_number = "868373070934429"
    run_data_deye3p(imei="868373070934429", inverter_serial="2302181309")
except Exception as e:
    print(str(e))


try:
    CLIENT_ID = "brain-868373070930823"
    imei_number = "868373070930823"
    run_data(imei="868373070930823", inverter_serial="2305066101")
except Exception as e:
    print(str(e))


try:
    CLIENT_ID = "brain-868373072913884"
    imei_number = "868373072913884"
    run_data(imei="868373072913884", inverter_serial="1031200237150110")
    run_heartbeat(
        imei=imei_number,
        brainFirmware_version="1.1.0.3",
        reboot_timestamp="2025-09-05T13:42:00Z",
        general_system_state=True,
        inverter_coms_state=True,
        relay_pair_state=False,
        devices_state=False,
        system_control_state=False,
        internal_state=True,
        relayFirmware_version="3.5.1.12",
        gosolr_version="-",
        edge_version="-",
        east_version="-",
        pair_version="-",
        manager_version="-",
        parsec_version="-",
        inverter_type="solis-1p",
        order_number="107642",
        inverter_sn="1031200237150110"
    )
    run_watchdog(imei=imei_number, deviceCount=4)
except Exception as e:
    print(str(e))


try:
    CLIENT_ID = "brain-868373070926904"
    imei_number = "868373070926904"
    run_data(imei="868373070926904", inverter_serial="2302098679")
except Exception as e:
    print(str(e))


try:
    CLIENT_ID = "brain-868373070929023"
    imei_number = "868373070929023"
    run_data(imei="868373070929023", inverter_serial="2303030552")
except Exception as e:
    print(str(e))


try:
    CLIENT_ID = "brain-868373070927662"
    imei_number = "868373070927662"
    run_data(imei="868373070927662", inverter_serial="2304256448")
except Exception as e:
    print(str(e))


print()

# time.sleep(5)

