#!/usr/bin/env python3
import scapy.all as scapy
import ipaddress
import re

# Patrón para validar una dirección de red IPv4 en notación CIDR
ip_add_range_pattern = re.compile("^(?:[0-9]{1,3}\.){3}[0-9]{1,3}/[0-9]+$")

# Obtener la red a escanear
while True:
    ip_add_range_entered = input("\nIngrese la dirección IP y rango CIDR a escanear (ej. 192.168.1.0/24): ")
    if ip_add_range_pattern.search(ip_add_range_entered):
        print(f"{ip_add_range_entered} es un rango válido.")
        break

# Generar la lista de todas las IPs en el rango
network = ipaddress.ip_network(ip_add_range_entered, strict=False)
all_ips = {str(ip) for ip in network.hosts()}  # Conjunto de todas las IPs posibles

# Escaneo ARP en la red
answered, unanswered = scapy.arping(ip_add_range_entered, verbose=False)

# Obtener solo las IPs activas
active_ips = {rcv.psrc for snd, rcv in answered}  # Conjunto de IPs que respondieron

# Calcular las IPs libres
free_ips = all_ips - active_ips

# Imprimir las IPs libres
if free_ips:
    print("\n📌 Direcciones IP disponibles en la red:")
    for ip in sorted(free_ips):
        print(ip)
else:
    print("\n✅ No hay IPs libres en este rango, todas están en uso.")