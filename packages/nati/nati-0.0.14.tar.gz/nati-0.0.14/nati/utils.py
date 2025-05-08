import datetime
import re
from iptools import ipv4


def is_valid_ipv4(address):
    return ipv4.validate_ip(address)


def is_valid_mac(address):
    mac_regex = re.compile(r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$')
    return bool(mac_regex.match(address))


def normalize_mac(address):
    # Remove common separators and make lowercase
    cleaned = re.sub(r'[^0-9A-Fa-f]', '', address).lower()
    
    if len(cleaned) != 12 or not all(c in '0123456789abcdef' for c in cleaned):
        return None  # Not a valid MAC address

    # Insert colons every two characters
    normalized = ':'.join(cleaned[i:i+2] for i in range(0, 12, 2))
    return normalized.upper()


def normalize_mac_prefix(prefix):
    """
    Normalize MAC prefix: remove separators, uppercase, 6–9 hex digits.
    """
    cleaned = re.sub(r'[^0-9A-Fa-f]', '', prefix).upper()
    if not (6 <= len(cleaned) <= 9) or not all(c in '0123456789ABCDEF' for c in cleaned):
        return None
    return cleaned


def today():
    """Return current date in ISO format."""
    return datetime.datetime.now().date().isoformat()
