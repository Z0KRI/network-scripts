#!/usr/bin/env python3
import ipaddress
import subprocess
import platform
import re
from concurrent.futures import ThreadPoolExecutor

# Patrón para validar una dirección de red IPv4 en notación CIDR
ip_add_range_pattern = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}/[0-9]+$")

# Obtener la red a escanear
while True:
    ip_add_range_entered = input("\nIngrese la dirección IP y rango CIDR a escanear (ej. 192.168.1.0/24): ")
    if ip_add_range_pattern.search(ip_add_range_entered):
        print(f"{ip_add_range_entered} es un rango válido.")
        break

# Generar la lista de todas las IPs en el rango
network = ipaddress.ip_network(ip_add_range_entered, strict=False)
all_ips = {str(ip) for ip in network.hosts()}  # Conjunto de todas las IPs posibles

# Configuración para ping según SO
is_windows = platform.system() == "Windows"
ping_cmd = ["ping", "-n", "1", "-w", "1000"] if is_windows else ["ping", "-c", "1", "-W", "1"]

# Función para hacer ping a una IP
def is_host_alive(ip):
    try:
        result = subprocess.run(ping_cmd + [ip], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return ip if result.returncode == 0 else None
    except Exception:
        return None

# Usar ThreadPoolExecutor para hacer ping en paralelo
max_threads = 50  # Ajusta según la capacidad de la red
active_ips = set()

with ThreadPoolExecutor(max_threads) as executor:
    results = executor.map(is_host_alive, all_ips)

# Filtrar IPs activas
active_ips = {ip for ip in results if ip}

# Calcular las IPs libres
free_ips = all_ips - active_ips

# Imprimir resultados
if free_ips:
    print("\n📌 Direcciones IP disponibles en la red:")
    for ip in sorted(free_ips):
        print(ip)
else:
    print("\n✅ No hay IPs libres en este rango, todas están en uso.")
