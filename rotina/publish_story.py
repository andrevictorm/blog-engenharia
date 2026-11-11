#!/usr/bin/env python3
"""Publica um story (imagem JPEG pública) no Instagram pela Graph API.
Uso: python publish_story.py URL_DA_IMAGEM [--dry-run]
Variáveis: IG_ACCESS_TOKEN, IG_BUSINESS_ACCOUNT_ID (nunca imprimir o token)."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from publish_carousel import api, wait_ready, fail
url = next((a for a in sys.argv[1:] if not a.startswith("--")), None)
if not url or not url.lower().endswith((".jpg", ".jpeg")): fail("informe a URL .jpg do story")
if "--dry-run" in sys.argv: print("dry-run OK:", url); sys.exit(0)
token, ig = os.environ.get("IG_ACCESS_TOKEN"), os.environ.get("IG_BUSINESS_ACCOUNT_ID")
if not token or not ig: fail("defina IG_ACCESS_TOKEN e IG_BUSINESS_ACCOUNT_ID")
cid = api("POST", f"{ig}/media", token, image_url=url, media_type="STORIES")["id"]
wait_ready(cid, token)
print("Story publicado! ID:", api("POST", f"{ig}/media_publish", token, creation_id=cid)["id"])
