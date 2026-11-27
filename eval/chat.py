import argparse
import uuid

import requests

ap = argparse.ArgumentParser()
ap.add_argument("text")
ap.add_argument("--base-url", default="http://localhost:8000")
ap.add_argument("--answer", help="확인 질문에 자동으로 답할 값 (예 또는 아니오)")
ap.add_argument("--session", default=str(uuid.uuid4())[:8])
ap.add_argument("--header", action="append", default=[], help='예: --header "X-Canary: 1"')
a = ap.parse_args()
HDR = dict(h.split(": ", 1) for h in a.header)
u = a.base_url.rstrip("/") + "/chat"


def show(resp):
    if resp.status_code != 200:
        print(f"[HTTP {resp.status_code}] {resp.text[:200]}")
        raise SystemExit(1)
    r = resp.json()
    print(f"[{r['type']}] {r['text']}")
    return r


r = show(requests.post(u, json={"session_id": a.session, "text": a.text}, headers=HDR, timeout=90))
if r["type"] == "confirm":
    ans = a.answer or input("사용자 > ")
    show(requests.post(u, json={"session_id": a.session, "confirm": ans.strip() in ("예", "y", "yes", "네")},
                       headers=HDR, timeout=90))