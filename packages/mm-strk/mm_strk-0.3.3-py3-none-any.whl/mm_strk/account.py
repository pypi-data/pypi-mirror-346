import re

from starknet_py.hash.address import is_checksum_address

# Maximum allowable value for a StarkNet address (251 bits)
MAX_STARKNET_ADDRESS = 2**251


def is_valid_address(address: str) -> bool:
    """
    Check if the address is a valid StarkNet address.

    A valid address:
    - Starts with '0x'
    - Followed by 1 to 64 hex characters (0-9, a-f, A-F)
    - Represents a number less than 2**251
    - Uses either minimal hex form (no leading zeros) or full 64-char padded form with correct checksum
    """
    # Basic checks
    if not isinstance(address, str) or not address.startswith("0x"):
        return False

    hex_part = address[2:]
    if len(hex_part) < 1 or len(hex_part) > 64:
        return False
    if not re.fullmatch(r"[0-9a-fA-F]+", hex_part):
        return False

    # Convert to integer
    try:
        value = int(hex_part, 16)
    except ValueError:
        return False

    # Range check
    if value >= MAX_STARKNET_ADDRESS:
        return False

    # Minimal hex form (e.g., '0x123')
    minimal = hex(value)[2:]
    if hex_part.lower() == minimal:
        return True

    # Full 64-char padded form with checksum (checksummed address)
    return bool(len(hex_part) == 64 and is_checksum_address(address))
