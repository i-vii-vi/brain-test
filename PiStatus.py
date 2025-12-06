import json
import random
from awscrt import mqtt5
from awsiot import mqtt5_client_builder

# --- Configuration ---
ENDPOINT = "a1xz7n0flroqhn-ats.iot.eu-west-1.amazonaws.com"
CLIENT_ID = "pi-handler"

CERTIFICATE = """-----BEGIN CERTIFICATE-----
MIIDWjCCAkKgAwIBAgIVAN3hA6bQwNzDzCV1VQrecjQ/1DgUMA0GCSqGSIb3DQEB
CwUAME0xSzBJBgNVBAsMQkFtYXpvbiBXZWIgU2VydmljZXMgTz1BbWF6b24uY29t
IEluYy4gTD1TZWF0dGxlIFNUPVdhc2hpbmd0b24gQz1VUzAeFw0yNDA3MDMwNzE1
NTZaFw00OTEyMzEyMzU5NTlaMB4xHDAaBgNVBAMME0FXUyBJb1QgQ2VydGlmaWNh
dGUwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQDzGNz3gbuaxCXbWMGU
9V2tzciMcNONUxtJmb0L28a0o3uc0+xY1OcE2JoRDBgF3QAe234tVbt2v4U8cgg2
aoze/nSJQBKyER/3UNb9EaXgCcEvuYvlx2EW58OkV1dRCzpRP/urx48hpzdrxktv
NOiNzQNv5Vc+Fayw0mLy5SQXceWl8+5yG1vvvQqPNmnRXuR9y3Tw18vLJebJ45nA
La3HKR3tsBu1i3dHdABhFDDUe96DCz0jZjYo2+Xylb29JYfG+6SZTDumlXD/8tZ5
9XCGque2K4KCaGG/2TH4J6qTTtCXTiBWLX4dXF4gfOHEcU7lQ2nHE2Hzn7w8XYav
LYS/AgMBAAGjYDBeMB8GA1UdIwQYMBaAFMigx/zlVeGsGaESmCyJzgFJ0YgUMB0G
A1UdDgQWBBQeab6F82iLG3ot6GhDbxBcwopD7zAMBgNVHRMBAf8EAjAAMA4GA1Ud
DwEB/wQEAwIHgDANBgkqhkiG9w0BAQsFAAOCAQEALG342QeII9XyGcKYhuvl0U8F
XairHL3l7zmw2yRNX2NO7GFGYJXau494Jjy2SeHJxus8tBqN82DT8TEUxjCUXrxE
SMwWUqPCdCBh8Lbon3d/CPM7fybbCWmBh+rqZT3eEASzQZszs/FBhkQbyTR5MAPU
BjrMlpxlLltoIdnKrRYACbz/OLXIREUgkUYINThUN2ndYjvYAUkCZHNnilEoboM5
XxxqXDZoG7E7NJd9Hmoq2GHxQCVzHM13fpDBslWgot+lCqyW3nL6/cDKAIlLFPdq
qz8NakHrkP9vJf37Y95xhZixaLbM63Z85b/LNboLJYlqA7++Gp47GUGcMbWfiQ==
-----END CERTIFICATE-----"""

PRIVATE_KEY = """-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEA8xjc94G7msQl21jBlPVdrc3IjHDTjVMbSZm9C9vGtKN7nNPs
WNTnBNiaEQwYBd0AHtt+LVW7dr+FPHIINmqM3v50iUASshEf91DW/RGl4AnBL7mL
5cdhFufDpFdXUQs6UT/7q8ePIac3a8ZLbzTojc0Db+VXPhWssNJi8uUkF3HlpfPu
chtb770KjzZp0V7kfct08NfLyyXmyeOZwC2txykd7bAbtYt3R3QAYRQw1Hvegws9
I2Y2KNvl8pW9vSWHxvukmUw7ppVw//LWefVwhqrntiuCgmhhv9kx+Ceqk07Ql04g
Vi1+HVxeIHzhxHFO5UNpxxNh85+8PF2Gry2EvwIDAQABAoIBAQDZA2QXS+g3VE1b
UBOYL6aORrt2rC4e5obgoG8ETBFKJvtt2D4QWxdU2yxGdZ5odY7q/RTZ0cQFURnX
CRFNyraxR0SvVdSaw/DebntN9dg3dV3RhfleiiuhMAsWBaZ8QeKwr8ay5fZfm5A9
FQs4XmoQVGlyFbFZSi4ct+P/ZBFhHt3t4aNTs7aksj7CazS64QenDcIwlFUVmf/i
RZzL91k023/OV+ISB3nd7jaNUd5yLGtoo4YGSAKSgJm8sJee2u7b51lulNE9eV8c
0XMHL/yj+nhc+YT/qL+4UdNXYORSYG4672gwN2FJeEJjNvwXWZOMcRJ7qke3hssM
lyf/ac4hAoGBAPxoJ5Ge8j1ja9uGt423vJq+BuelYi2vKSGmRHzAK3arv1mGln5r
GtMQR/PcuXlscsPms8wzS1Er6fZCmn1YMMyPpm01HoY6O2sfEcbyc4C+7Q8gQ0DE
iudHn3hmetHFhLChpb25neee3oACCpdHlQV2QV9Vos5STPgs0ca2cffxAoGBAPaO
x/osX0Ie50N/8YLUyszhKUnBIxfu7jSkzq9+6XK1H7OH3vlTPLTxJ/6xHanUE5BN
so/llNQGj+S3Xtzku4rQG/1UnhPJx1+VblOFPIwxp5/wtTJqzW07nGlRYu8Yy16H
yj+HZcWC+FFVUOcwSqsmzCwE26F4qYCzGYYxRHevAoGBANZd7x0yDTIt+jCbndDy
t3AE7ABY6aU7GofFmm0JGODUxNLYB4Cenk2bikCGuc9yV5YhnZpUBieOUEoiDutd
tzRE3GfrsVz2n/g+ju6Ug5xYiyVJlVSwl/gNUFcFUlJOmn8ZCpazynQo7XdyRGRv
GxVkdejt5jOsmko8Zn2J/glBAoGAFf1T/o74i/gfnhiKHKYH1E/8k7RjAd5wZkeQ
m3xRK8bVpfhnPYtb7bNYYtG/GIdumz8ivsy2Alb3fGmST1cjFtVKucRTOOaVHoRA
S7ilVseS8KPSNUXrPmPDpmz4yuRGNw8bTaEwxXXR2ccnKQdYkX0rVn20bOlLDMxs
aVh5h8cCgYAMWztXLaT+MeIIQ9Z6lbNS+UbNWS9hAlSlafyGAj6DmE51SRf4P+gM
xquDk3tnHvZRIcHxHSSi9JCzuteiVJlDWHndxw9MUdNt8edjxhrck5MopswDwOzt
ARknSgsIyHeBiBICjXABMGLqSnbjKibSrwWTooBhSZYlqdB2NmyLOQ==
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


# -------------------------------
#   Random IP Generation Helpers
# -------------------------------
def random_ip(prefix, used_ips):
    """Generate a unique random IP with the given prefix."""
    while True:
        last_octet = random.randint(1, 254)
        ip = f"{prefix}{last_octet}"
        if ip not in used_ips:
            used_ips.add(ip)
            return ip


# Linux process names (realistic common daemons & services)
LINUX_PROCESSES = [
    "systemd", "systemd-journald", "systemd-logind", "dbus-daemon",
    "NetworkManager", "sshd", "cron", "rsyslogd", "udevd", "containerd",
    "dockerd", "apparmor", "avahi-daemon", "cupsd", "nginx", "apache2",
    "mysqld", "redis-server", "bash", "python3", "kworker/0:1", "kworker/1:0",
    "Xorg", "gnome-shell", "pulseaudio"
]


def random_process_list():
    """Generate a random list of Linux-like processes."""
    count = random.randint(5, 20)
    processes = []

    for _ in range(count):
        name = random.choice(LINUX_PROCESSES)
        pid = random.randint(100, 5000)
        cpu = round(random.uniform(0.0, 15.0), 1)
        mem = round(random.uniform(0.0, 5.0), 1)

        processes.append({
            "pid": pid,
            "name": name,
            "cpu": cpu,
            "mem": mem
        })

    return processes


def generate_metrics():
    """Generate realistic system metrics."""
    # Memory (64GB system)
    mem_total = 64
    mem_used = round(random.uniform(4, 60), 1)
    mem_used_pct = round((mem_used / mem_total) * 100, 1)

    # CPU usage
    cpu = round(random.uniform(1, 98), 1)

    # Network throughput (1–950 Mbps)
    net_in = round(random.uniform(1, 950), 1)
    net_out = round(random.uniform(1, 950), 1)

    return {
        "memory_used_gb": mem_used,
        "memory_total_gb": mem_total,
        "memory_used_percent": mem_used_pct,
        "cpu_usage_percent": cpu,
        "net_in_mbps": net_in,
        "net_out_mbps": net_out,
        "processes": random_process_list()
    }


# Topic → IP prefix mappings (matches your old manual IPs)
topic_ip_map = {
    "PI/CPT-HW/0/C": "147.55.3.",
    "PI/CPT-HW/1/C": "147.55.4.",
    "PI/CPT-HW/1/N/A": "147.55.4.",
    "PI/CPT-HW/1/N/B": "147.55.4.",
    "PI/CPT-HW/1/N/C": "147.55.4.",
    "PI/CPT-HW/1/N/D": "147.55.4.",
    "PI/CPT-HW/1/N/E": "147.55.4.",
    "PI/CPT-HW/1/N/F": "147.55.4.",
    "PI/CPT-HW/1/N/G": "147.55.4.",
    "PI/CPT-HW/1/N/H": "147.55.4.",
    "PI/CPT-HW/1/N/I": "147.55.4.",
    "PI/CPT-HW/1/N/J": "147.55.4.",
    "PI/CPT-HW/1/N/K": "147.55.4.",
    "PI/CPT-HW/1/N/L": "147.55.4.",

    "PI/CPT-HW/2/C": "147.55.5.",
    "PI/CPT-HW/2/N/M": "147.55.5.",
    "PI/CPT-HW/2/N/N": "147.55.5.",
    "PI/CPT-HW/2/N/O": "147.55.5.",
    "PI/CPT-HW/2/N/P": "147.55.5.",
    "PI/CPT-HW/2/N/Q": "147.55.5.",
    "PI/CPT-HW/2/N/R": "147.55.5.",
    "PI/CPT-HW/2/N/S": "147.55.5.",

    "PI/CPT-WQ/3/C": "118.124.0.",
    "PI/CPT-WQ/3/N/T": "118.124.0.",
    "PI/CPT-WQ/3/N/U": "118.124.0.",
    "PI/CPT-WQ/3/N/V": "118.124.0.",

    "PI/ISR-TA/4/C": "36.131.8.",
    "PI/ISR-TA/4/N/W": "36.131.8.",
    "PI/ISR-TA/4/N/X": "36.131.8.",
    "PI/ISR-TA/4/N/Y": "36.131.8.",

    "PI/CPT-PN/5/C": "192.168.1.",
}


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


def main():
    print("Connecting to AWS IoT Core...")
    mqtt_connection.connect().result()
    print("✅ Connected")

    used_ips = set()

    # Publish all topics with enriched payloads
    for topic, prefix in topic_ip_map.items():
        ip = random_ip(prefix, used_ips)
        metrics = generate_metrics()

        payload = json.dumps({
            "ip": ip,
            **metrics
        })

        mqtt_connection.publish(
            topic=topic,
            payload=payload,
            qos=mqtt5.QoS.AT_LEAST_ONCE,
            retain=False
        )

        print(f"Published {ip} → {topic}")

    print("All enriched system payloads sent.")


if __name__ == "__main__":
    main()
