from ipaddress import ip_address
from urllib.parse import urlsplit


def is_local_origin(origin: str) -> bool:
    """Return True for localhost/loopback/private-network origins."""
    if not origin:
        return False

    try:
        parsed = urlsplit(origin)
    except ValueError:
        return False

    host = parsed.hostname
    if not host:
        return False

    if host == "localhost" or host.endswith(".local"):
        return True

    try:
        ip = ip_address(host)
    except ValueError:
        return False

    return ip.is_loopback or ip.is_private or ip.is_link_local
