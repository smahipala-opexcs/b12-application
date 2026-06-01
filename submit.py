import json
import hmac
import hashlib
import requests
from datetime import datetime, timezone
import os

SIGNING_SECRET = os.environ["SIGNING_SECRET"]
ENDPOINT = "https://b12.io/apply/submission"

payload = {
    "action_run_link": os.environ["ACTION_RUN_LINK"],
    "email": os.environ["EMAIL"],
    "name": os.environ["NAME"],
    "repository_link": os.environ["REPOSITORY_LINK"],
    "resume_link": os.environ["RESUME_LINK"],
    "timestamp": datetime.now(timezone.utc)
        .isoformat(timespec="milliseconds")
        .replace("+00:00", "Z")
}

body = json.dumps(
    payload,
    sort_keys=True,
    separators=(",", ":"),
    ensure_ascii=False
).encode("utf-8")

signature = hmac.new(
    SIGNING_SECRET.encode("utf-8"),
    body,
    hashlib.sha256
).hexdigest()

headers = {
    "Content-Type": "application/json",
    "X-Signature-256": f"sha256={signature}"
}

response = requests.post(ENDPOINT, data=body, headers=headers, timeout=30)
response.raise_for_status()

result = response.json()
print("Receipt:", result["receipt"])