#!/usr/bin/env python3
"""IndexNow ping after a deploy.

Reads the live sitemap, compares it with the state saved from the previous
run (URL -> lastmod), and POSTs only new or changed URLs to IndexNow.
No-op when nothing changed. Safe to re-run: state is only updated after an
accepted (200/202) response, so a failed ping is retried next run.

Env: SITE_HOST (e.g. shutterkit.app), INDEXNOW_KEY, STATE_FILE (default
.indexnow/state.json), FIRST_RUN_SUBMIT_ALL (default "1"), DRY_RUN ("1" = log only).
Optional: BING_API_KEY (see Bing block at the bottom; off unless set AND uncommented).
"""
import json, os, sys, time, urllib.request, urllib.error
import xml.etree.ElementTree as ET

HOST = os.environ["SITE_HOST"]
KEY = os.environ["INDEXNOW_KEY"]
STATE = os.environ.get("STATE_FILE", ".indexnow/state.json")
SITEMAP = f"https://{HOST}/sitemap.xml"
NS = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
UA = {"User-Agent": "farspeak-indexnow/1.0"}

def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
        return r.status, r.read()

def fetch_sitemap(url, depth=0):
    _, body = get(url)
    root = ET.fromstring(body)
    out = {}
    if root.tag.endswith("sitemapindex") and depth < 2:
        for loc in root.findall("s:sitemap/s:loc", NS):
            out.update(fetch_sitemap(loc.text.strip(), depth + 1))
        return out
    for u in root.findall("s:url", NS):
        loc = u.find("s:loc", NS).text.strip()
        lm = u.find("s:lastmod", NS)
        out[loc] = lm.text.strip() if lm is not None and lm.text else ""
    return out

def main():
    # 1. Key file must be live first, or IndexNow rejects the ping (403).
    key_url = f"https://{HOST}/{KEY}.txt"
    for attempt in range(10):
        try:
            st, body = get(key_url)
            if st == 200 and body.decode().strip() == KEY:
                break
        except Exception as e:
            print(f"key file not live yet ({e}); retry {attempt+1}/10")
        time.sleep(30)
    else:
        sys.exit(f"ERROR: {key_url} not serving the key; not pinging")

    current = {u: lm for u, lm in fetch_sitemap(SITEMAP).items() if u.startswith(f"https://{HOST}/")}
    previous = None
    if os.path.exists(STATE):
        previous = json.load(open(STATE))
    if previous is None:
        changed = sorted(current) if os.environ.get("FIRST_RUN_SUBMIT_ALL", "1") == "1" else []
        print(f"no previous state; first run, submitting {len(changed)} URLs")
    else:
        changed = sorted(u for u, lm in current.items() if previous.get(u) != lm)
    removed = sorted(set(previous or {}) - set(current))
    # Removed URLs can be submitted too (IndexNow treats 404/410 as a deletion signal).
    urls = changed + removed
    print(f"sitemap URLs: {len(current)}; changed/new: {len(changed)}; removed: {len(removed)}")
    for u in urls:
        print("  ", u)

    def save():
        os.makedirs(os.path.dirname(STATE) or ".", exist_ok=True)
        json.dump(current, open(STATE, "w"), indent=1, sort_keys=True)

    if not urls:
        print("nothing changed; no ping sent")
        save(); return
    if os.environ.get("DRY_RUN") == "1":
        print("DRY_RUN=1; not sending"); return

    payload = {"host": HOST, "key": KEY, "keyLocation": key_url, "urlList": urls[:10000]}
    req = urllib.request.Request("https://api.indexnow.org/indexnow",
        data=json.dumps(payload).encode(), method="POST",
        headers={"Content-Type": "application/json; charset=utf-8", **UA})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            status = r.status
    except urllib.error.HTTPError as e:
        status = e.code
    print(f"IndexNow HTTP status: {status} (200/202 = accepted)")
    if status in (200, 202):
        save()
    else:
        # 400 bad request, 403 key not valid, 422 URLs not on host, 429 too many requests
        sys.exit(f"IndexNow rejected the ping with {status}; state not updated, will retry next run")

    # --- Optional: Bing URL Submission API (off by default) -----------------
    # Uncomment to also submit to Bing directly. Runs only if BING_API_KEY is set.
    # Bing daily quota applies (shown in Bing Webmaster Tools > URL Submission).
    # bing = os.environ.get("BING_API_KEY")
    # if bing:
    #     breq = urllib.request.Request(
    #         f"https://ssl.bing.com/webmaster/api.svc/json/SubmitUrlBatch?apikey={bing}",
    #         data=json.dumps({"siteUrl": f"https://{HOST}", "urlList": urls[:500]}).encode(),
    #         method="POST", headers={"Content-Type": "application/json; charset=utf-8"})
    #     try:
    #         with urllib.request.urlopen(breq, timeout=30) as r: bst = r.status
    #     except urllib.error.HTTPError as e: bst = e.code
    #     print(f"Bing SubmitUrlBatch HTTP status: {bst} (200 = accepted)")

if __name__ == "__main__":
    main()
