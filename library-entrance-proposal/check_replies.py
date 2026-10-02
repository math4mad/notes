#!/usr/bin/env python3
"""check_replies.py — 图书馆入口建议 · 回音巡检。

定期扫邮箱（agently-cli），把三馆/各馆的回音写回 outreach.csv；
回音累计达阈值（默认 5）则**告警**：挂一条 iPhone 提醒 ＋ 打印哨 THRESHOLD-REACHED。

用法:
  python3 check_replies.py                 # 巡检并更新 csv（不告警）
  python3 check_replies.py --notify        # 达阈值时告警
  python3 check_replies.py --threshold 5
"""
import csv, json, os, subprocess, sys, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
CSV = os.path.join(HERE, "outreach.csv")
REMIND = os.path.expanduser("~/Programming/code-2026/Concept-Space-Sphere/bin/remind.sh")
REPLIED = ("replied", "ack", "positive", "negative")

THRESHOLD = 5
for i, a in enumerate(sys.argv):
    if a == "--threshold" and i + 1 < len(sys.argv):
        THRESHOLD = int(sys.argv[i + 1])
NOTIFY = "--notify" in sys.argv


def cli(*args):
    try:
        r = subprocess.run(["agently-cli", *args], capture_output=True, text=True, timeout=60)
        return json.loads(r.stdout)
    except Exception as e:
        return {"ok": False, "err": str(e)}


def search_from(addr):
    d = cli("message", "+search", "--from", addr, "--dir", "inbox", "--limit", "20")
    if not d.get("ok"):
        return []
    return (d.get("data") or {}).get("data") or []


def latest(msgs):
    ds = [m.get("created_at", "") for m in msgs if m.get("created_at")]
    return max(ds)[:10] if ds else ""


def main():
    rows = list(csv.DictReader(open(CSV, encoding="utf-8")))
    fields = list(rows[0].keys()) if rows else ["city", "tier", "library", "email", "sent_date", "status", "reply_date", "note"]

    total = 0
    for r in rows:
        addr = r.get("email", "").strip()
        dom = addr.split("@", 1)[1] if "@" in addr else ""
        msgs = search_from(addr) + (search_from(dom) if dom else [])
        # 去重（同 message_id）
        seen, uniq = set(), []
        for m in msgs:
            mid = m.get("message_id")
            if mid and mid not in seen:
                seen.add(mid); uniq.append(m)
        if uniq and (r.get("status") or "pending") == "pending":
            r["status"] = "replied"
            r["reply_date"] = latest(uniq)
        if (r.get("status") or "").strip() in REPLIED:
            total += 1
        r["_n"] = len(uniq)

    # 写回
    with open(CSV, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in fields})

    print(f"[{datetime.datetime.now():%F %T}] 巡检: 投递 n={len(rows)} · 有回音 {total} · 阈值 {THRESHOLD}")
    for r in rows:
        print(f"  {r.get('library',''):<10} {r.get('email',''):<24} {r.get('status',''):<9} {r.get('reply_date','')}")

    if total >= THRESHOLD:
        msg = f"图书馆入口建议：回音已达 {total}（阈值 {THRESHOLD}）——触发扩张律/统计"
        if NOTIFY:
            subprocess.run([REMIND, "add", "图书馆建议·回音达阈值", msg], timeout=60)
        print("THRESHOLD-REACHED total=%d" % total)
    else:
        print(f"below-threshold ({total}/{THRESHOLD})")


if __name__ == "__main__":
    main()
