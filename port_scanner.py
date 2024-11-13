import socket
from common_ports import ports_and_services

def get_open_ports(target, port_range, verbose=False):
    open_ports = []
    try:
        # Verificar si el objetivo es una dirección IP
        if target.replace('.', '').isdigit():
            ip_address = target
            socket.inet_aton(ip_address)  # Valida la dirección IP
        else:
            # Intentar resolver el hostname del objetivo
            ip_address = socket.gethostbyname(target)
    except socket.gaierror:
        # Manejar hostnames o IPs no válidas
        return "Error: Invalid hostname" if not target.replace('.', '').isdigit() else "Error: Invalid IP address"

    # Escanear los puertos en el rango especificado
    for port in range(port_range[0], port_range[1] + 1):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)  # Tiempo de espera para escaneo más rápido
            if s.connect_ex((ip_address, port)) == 0:
                open_ports.append(port)

    if verbose:
        # Formatear la salida en modo detallado (verbose)
        service_lines = [
            f"{port:<7} {ports_and_services.get(port, 'unknown')}" for port in open_ports
        ]
        hostname = target if target != ip_address else None
        title = f"Open ports for {hostname} ({ip_address})" if hostname else f"Open ports for {ip_address}"
        return f"{title}\nPORT     SERVICE\n" + "\n".join(service_lines)
    else:
        # Retornar lista de puertos abiertos
        return open_ports
