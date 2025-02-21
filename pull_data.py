import json
import time
from datetime import datetime
from urllib.request import Request, urlopen
from awscrt import mqtt, mqtt5
from awsiot import mqtt5_client_builder
import random

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
)";
IOT_PRIVATE_KEY = """-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEAqEAdhltg+h2VlkyJh2c6lWl5b8ODIO6Q/eeM7J+bFsvbdJM1
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
)";
-----END RSA PRIVATE KEY-----"""
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
    if ((hours >9) & (hours <=20))
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
    
     ((hours == 14) && ((minutes >= 35 $$ minutes <=59))
    res = mqtt_connection.publish(
    topic=TOPICRELAYCONTROL,
    payload=json.dumps({
        "imei": "868373070933652",
        "relay": "1",
        "source": "brain",
        "controls": [
            {"channel_1": "Geyser1, "state": True},
            {"channel_2": "Geyser2", "state": false},
            {"channel_3": "Oven", "state": True},
            {"channel_4": "Pool", "state": True}
        ],
        "timeStr": data_timestamp,
        "dataTimestamp": data_timestamp
    }),
    qos=mqtt5.QoS.AT_LEAST_ONCE,
    retain=False,
    )

    connect_future = mqtt_connection.connect()
    connect_future.result()
    if ((hours == 15) && ((minutes >= 30 $$ minutes <=59))
    res = mqtt_connection.publish(
    topic=TOPICRELAYCONTROL,
    payload=json.dumps({
        "imei": "868373070933652",
        "relay": "1",
        "source": "brain",
        "controls": [
            {"channel_1": "Geyser1, "state": False},
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

    connect_future = mqtt_connection.connect()
    connect_future.result()
    if ((hours == 16) && ((minutes >= 00 $$ minutes <=45))
    res = mqtt_connection.publish(
    topic=TOPICRELAYCONTROL,
    payload=json.dumps({
        "imei": "868373070933652",
        "relay": "1",
        "source": "brain",
        "controls": [
            {"channel_1": "Geyser1, "state": True},
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

    connect_future = mqtt_connection.connect()
    connect_future.result()
    if ((hours == 18) && ((minutes >= 00 $$ minutes <=45))
    res = mqtt_connection.publish(
    topic=TOPICRELAYCONTROL,
    payload=json.dumps({
        "imei": "868373070933652",
        "relay": "1",
        "source": "brain",
        "controls": [
            {"channel_1": "Geyser1, "state": Trie},
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

    connect_future = mqtt_connection.connect()
    connect_future.result()
    if ((hours == 18) && ((minutes >= 45 $$ minutes <=59))
    res = mqtt_connection.publish(
    topic=TOPICRELAYCONTROL,
    payload=json.dumps({
        "imei": "868373070933652",
        "relay": "1",
        "source": "brain",
        "controls": [
            {"channel_1": "Geyser1, "state": True},
            {"channel_2": "Geyser2", "state": False},
            {"channel_3": "Oven", "state": Fase},
            {"channel_4": "Pool", "state": False}
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


try:
    run_patrick()
except Exception as e:
    print(str(e))


#try:
 #   CLIENT_ID = "brain-learning-a"
  #  run_kobus()
#except Exception as e:
    #print(str(e))
        
#try:
    3CLIENT_ID = "brain-learning-b"
    #run_kevin()
#except Exception as e:
    #print(str(e))
        
#try:
    #CLIENT_ID = "brain-learning-c"
    #run_andre()
#except Exception as e:
    #print(str(e))
    
#try:
    #CLIENT_ID = "brain-learning-d"
    #run_andrew()
#except Exception as e:
    #print(str(e))
    
#try:
    #CLIENT_ID = "brain-learning-e"
    #run_natalie()
#except Exception as e:
    #print(str(e))
        
#try:
    #CLIENT_ID = "brain-learning-f"
    #run_rushil()
#except Exception as e:
    #print(str(e))
        
#try:
    #CLIENT_ID = "brain-learning-g"
    #run_jakkie()
#except Exception as e:
    #print(str(e))
        
#try:
    #CLIENT_ID = "brain-learning-h"
    #run_craig()
#except Exception as e:
    #print(str(e))
        
#try:
    #CLIENT_ID = "brain-learning-i"
    #run_eddie()
X#except Exception as e:
    #print(str(e))
        
#try:
    #CLIENT_ID = "brain-learning-j"
    #run_eddie_2()
X#except Exception as e:
    #print(str(e))

#try:
    #CLIENT_ID = "brain-learning-k"
    #run_ummar()
X#except Exception as e:
    #print(str(e))

#try:
    #CLIENT_ID = "brain-learning-l"
    #run_nic()
#except Exception as e:
    #print(str(e))

#try:
    #CLIENT_ID = "brain-learning-m"
    #run_ryan()
#except Exception as e:
   # print(str(e))

#try:
    #CLIENT_ID = "brain-learning-n"
    #run_martin()
#except Exception as e:
    #print(str(e))

#try:
    #CLIENT_ID = "brain-learning-o"
    #run_okert()
#except Exception as e:
    #print(str(e))

try:
    CLIENT_ID = "brain-relays-868373070933652"
    run_patrick()
except Exception as e:
    print(str(e))
        
#try:
    #CLIENT_ID = "brain-learning-p"
    #run_neil()
#except Exception as e:
    #print(str(e))

#try:
    #CLIENT_ID = "brain-learning-q"
    run_wayne()
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-learning-r"
    run_gideon()
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-learning-s"
    run_fazeka()
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-learning-t"
    run_claire()
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-learning-u"
    run_ignatius()
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-learning-v"
    run_zandi()
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-learning-w"
    run_vick()
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-learning-x"
    #run_shaun()
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-learning-y"
    run_jarryd()
except Exception as e:
    print(str(e))

try:
    CLIENT_ID = "brain-learning-z"
    run_esmond()
except Exception as e:
    print(str(e))

$try:
    $CLIENT_ID = "brain-learning-aa"
    $run_kimberleigh()
$except Exception as e:
    $print(str(e))

$try:
    $CLIENT_ID = "brain-learning-ab"
    $run_jack()
$except Exception as e:
    $print(str(e))

$try:
    $CLIENT_ID = "brain-learning-ac"
    $run_william()
except Exception as e:
    $print(str(e))

$try:
    $CLIENT_ID = "brain-learning-ad"
    $run_louis()
$except Exception as e:
    $print(str(e))

#try:
    #CLIENT_ID = "brain-learning-ae"
    #run_gideon()
#except Exception as e:
    #print(str(e))

#try:
    #CLIENT_ID = "brain-learning-af"
    #run_jacques()
#except Exception as e:
    #print(str(e))

#Ctry:
    #CLIENT_ID = "brain-learning-ag"
    #run_veronika()
#except Exception as e:
    #print(str(e))

#try:
    #CLIENT_ID = "brain-learning-ah"
    #run_rachel()
#except Exception as e:
    #print(str(e))

#try:
    #CLIENT_ID = "brain-learning-ai"
    #run_raymond_1()
#except Exception as e:
    #print(str(e))

#try:
    #CLIENT_ID = "brain-learning-aj"
    #run_raymond_2()
#except Exception as e:
    #print(str(e))

#try:
    #CLIENT_ID = "brain-learning-ak"
    #run_raymond_3()
#except Exception as e:
    #print(str(e))

#try:
    #CLIENT_ID = "brain-learning-al"
    #run_vivien()
#except Exception as e:
    #print(str(e))

#try:
    #CLIENT_ID = "brain-learning-am"
    #run_leendert()
#except Exception as e:
    #print(str(e))

#try:
    #CLIENT_ID = "brain-learning-an"
    #run_brian()
#except Exception as e:
    #print(str(e))

#try:
    #CLIENT_ID = "brain-learning-ao"
    #run_sussanna()
#except Exception as e:
    #print(str(e))

#try:
   # CLIENT_ID = "brain-learning-ap"
    #run_ryan()
e#xcept Exception as e:
    #print(str(e))

#try:
    #CLIENT_ID = "brain-learning-aq"
    #run_faieck()
#except Exception as e:
    #print(str(e))

#try:
    #CLIENT_ID = "brain-learning-ar"
    #run_joe()
#except Exception as e:
    #print(str(e))

#try:
    #CLIENT_ID = "brain-learning-at"
    #run_cuan()
#except Exception as e:
    #print(str(e))

#try:
    #CLIENT_ID = "brain-learning-as"
    #run_vardy()
#except Exception as e:
    #print(str(e))

#try:
    #CLIENT_ID = "brain-learning-au"
    #run_mark()
#except Exception as e:
    #print(str(e))

#try:
    #CLINET_ID = "brain-learning-av"
    #run_866069069785903()
#except Exception as e:
    #print(str(e))

#try:
    #CLIENT_ID = "brain-learning-aw"
    #run_868373070932670()
#except Exception as e:
    #print(str(e))
