import json
from collections import Counter
from urllib.parse import urlparse
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
with open(ROOT/"data"/"search_results.json",encoding="utf-8") as f: apps=json.load(f)
domains=Counter(); urls=Counter()
for app in apps:
    for item in app.get("results",[]):
        url=item.get("url","")
        host=urlparse(url).netloc.lower().removeprefix("www.")
        if host: domains[host]+=1; urls[url]+=1
print("Applications:",len(apps))
print("Total results:",sum(len(a.get("results",[])) for a in apps))
print("Unique URLs:",len(urls))
print("Duplicate URL entries:",sum(n-1 for n in urls.values()))
print("\nTop 25 domains")
for host,count in domains.most_common(25): print(f"{count:3} | {host}")
print("\nApplications with fewer than five results")
for app in apps:
    if len(app.get("results",[]))<5: print(app.get("app"),len(app.get("results",[])))
