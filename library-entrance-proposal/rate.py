#!/usr/bin/env python3
"""rate.py — 图书馆入口建议·投递成功率统计 (n 小, 只报读数, 不夸大)。"""
import csv, os, collections

HERE = os.path.dirname(os.path.abspath(__file__))
ROWS = list(csv.DictReader(open(os.path.join(HERE, "outreach.csv"), encoding="utf-8")))

def pct(n, d):
    return f"{(100.0*n/d):.1f}%" if d else "—"

sent = len(ROWS)
c = collections.Counter((r["status"] or "pending").strip() for r in ROWS)
replied = sum(c[s] for s in ("ack", "positive", "negative"))
positive = c["positive"]

print("── 图书馆入口建议 · 投递台账 ──")
for r in ROWS:
    print(f"  {r['tier']:<4} {r['library']:<10} {r['email']:<24} {r['sent_date']}  {r['status']}")
print()
print(f"投递 n        = {sent}")
print(f"回复率        = {pct(replied, sent)}   ({replied}/{sent})  [ack+positive+negative]")
print(f"正向率        = {pct(positive, sent)}   ({positive}/{sent})")
print(f"退信率        = {pct(c['bounce'], sent)}   ({c['bounce']}/{sent})")
print(f"仍 pending    = {c['pending']}")
print()
if replied == 0:
    print("→ 扩张律：尚无回音，**不扩张**（样本即结论的一部分）。")
else:
    print("→ 扩张律触发：**可扩至 1–2 线城市大馆**。")
