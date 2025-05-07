import ipaddress

def compute_host_number(ip_str: str, mask_str: str) -> int:
    """
    Для заданных строковых представлений IP‑адреса и маски сети
    возвращает номер узла (host ID) в этой сети.
    """
    network = ipaddress.IPv4Network(f"{ip_str}/{mask_str}", strict=False)
    ip = int(ipaddress.IPv4Address(ip_str))
    mask = int(network.netmask)
    host_id = ip & (~mask & 0xFFFFFFFF)
    return host_id