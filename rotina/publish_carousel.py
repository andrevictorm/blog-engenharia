#!/usr/bin/env python3
"""Publica um carrossel no Instagram pela API oficial da Meta (Graph API).

Uso:
  python publish_carousel.py post.json --dry-run   # só valida, não publica
  python publish_carousel.py post.json             # publica de verdade

Variáveis de ambiente (NUNCA coloque o token no código nem no chat):
  IG_ACCESS_TOKEN             token de acesso
  IG_BUSINESS_ACCOUNT_ID      ID da conta profissional do Instagram
  GRAPH_VERSION               opcional; confira a versão atual na documentação da Meta
"""
import json, os, sys, time
import requests

GRAPH = os.environ.get("GRAPH_VERSION", "v23.0")
BASE = f"https://graph.facebook.com/{GRAPH}"


def fail(msg):
    print(f"ERRO: {msg}", file=sys.stderr)
    sys.exit(1)


def api(method, path, token, **params):
    params["access_token"] = token
    fn = requests.post if method == "POST" else requests.get
    kw = {"data": params} if method == "POST" else {"params": params}
    r = fn(f"{BASE}/{path}", timeout=60, **kw)
    try:
        data = r.json()
    except ValueError:
        fail(f"resposta inválida da API ({r.status_code})")
    if r.status_code >= 400 or "error" in data:
        err = data.get("error", {})
        fail(f"{err.get('message', data)} (código {err.get('code')})")
    return data


def wait_ready(container_id, token, timeout=120):
    start = time.time()
    while time.time() - start < timeout:
        status = api("GET", container_id, token, fields="status_code")["status_code"]
        if status == "FINISHED":
            return
        if status in ("ERROR", "EXPIRED"):
            fail(f"contêiner {container_id} terminou com status {status}")
        time.sleep(3)
    fail(f"tempo esgotado aguardando o contêiner {container_id}")


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    dry = "--dry-run" in sys.argv
    if not args:
        fail("informe o arquivo post.json")
    post = json.load(open(args[0], encoding="utf-8"))
    urls, caption = post["image_urls"], post["caption"]
    if not 2 <= len(urls) <= 10:
        fail("um carrossel precisa de 2 a 10 imagens")
    if not all(u.lower().endswith((".jpg", ".jpeg")) for u in urls):
        fail("a API do Instagram aceita imagens JPEG; use as imagens .jpg")

    token = os.environ.get("IG_ACCESS_TOKEN")
    ig_id = os.environ.get("IG_BUSINESS_ACCOUNT_ID")
    if not token or not ig_id:
        fail("defina IG_ACCESS_TOKEN e IG_BUSINESS_ACCOUNT_ID")

    print(f"{len(urls)} imagens; legenda com {len(caption)} caracteres")
    if dry:
        print("dry-run: nada foi enviado.")
        return

    children = []
    for i, url in enumerate(urls, 1):
        cid = api("POST", f"{ig_id}/media", token, image_url=url, is_carousel_item="true")["id"]
        wait_ready(cid, token)
        children.append(cid)
        print(f"  imagem {i}/{len(urls)} pronta")

    parent = api("POST", f"{ig_id}/media", token, media_type="CAROUSEL",
                 children=",".join(children), caption=caption)["id"]
    wait_ready(parent, token)
    media = api("POST", f"{ig_id}/media_publish", token, creation_id=parent)["id"]
    print(f"Publicado! ID da mídia: {media}")


if __name__ == "__main__":
    main()
