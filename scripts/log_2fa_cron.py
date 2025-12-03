#!/usr/bin/env python3
import os
import datetime
import base64
import pyotp

SEED_FILE = '/data/seed.txt'
LOG_FILE = '/cron/last_code.txt'

try:
    with open(SEED_FILE, 'r') as f:
        hex_seed = f.read().strip()
except FileNotFoundError:
    print("Seed not found", file=sys.stderr)
    exit(1)

# Convert hex seed to base32
seed_bytes = bytes.fromhex(hex_seed)
base32_seed = base64.b32encode(seed_bytes).decode('utf-8')

# Generate TOTP code
totp = pyotp.TOTP(base32_seed)
code = totp.now()

# Get current UTC timestamp
timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

# Append to log file
with open(LOG_FILE, 'a') as f:
    f.write(f"{timestamp} - 2FA Code: {code}\n")
