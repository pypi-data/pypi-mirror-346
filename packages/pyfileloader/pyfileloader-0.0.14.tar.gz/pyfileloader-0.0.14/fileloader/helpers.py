def detect_bom(file: str) -> str:
    """
    Sometimes byte-order mode is messy, let's try to cover those cases
    """

    # Open the file in binary mode to read raw bytes
    with open(file, "rb") as f:
        # Read the first 4 bytes of the file
        raw = f.read(4)

    # Check for the BOM
    if raw.startswith(b"\xef\xbb\xbf"):
        return "UTF-8-SIG"
    if raw.startswith(b"\xff\xfe\x00\x00") or raw.startswith(b"\x00\x00\xfe\xff"):
        return "UTF-32-SIG"
    if raw.startswith(b"\xff\xfe") or raw.startswith(b"\xfe\xff"):
        return "UTF-16-SIG"

    return "UTF-8"
