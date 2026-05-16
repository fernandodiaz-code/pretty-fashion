import os
import subprocess
import tempfile


PRINTER_NAME = "XPrinter-RAW"
CUT_COMMAND = b"\x1D\x56\x00"


def print_raw(payload):
    data = payload if isinstance(payload, bytes) else payload.encode("utf-8")
    data += CUT_COMMAND

    temp_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".bin") as temp_file:
            temp_file.write(data)
            temp_path = temp_file.name

        subprocess.run(
            ["lp", "-d", PRINTER_NAME, "-o", "raw", temp_path],
            check=True,
            capture_output=True,
            text=True,
        )
    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)
