import os

PAPERLESS_NGX_URI = os.getenv("PAPERLESS_NGX_URI", None)
PAPERLESS_NGX_TOKEN = os.getenv("PAPERLESS_NGX_TOKEN", None)

if PAPERLESS_NGX_URI is None:
    raise ValueError("PAPERLESS_NGX_URI must be set")

if PAPERLESS_NGX_TOKEN is None:
    raise ValueError("PAPERLESS_NGX_TOKEN must be set")