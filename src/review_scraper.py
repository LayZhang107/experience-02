"""合规的公开评论采集器；不绕过访问限制。"""
import argparse, csv, random, re, urllib.robotparser
from pathlib import Path
from urllib.request import Request, urlopen
from html.parser import HTMLParser

class ReviewParser(HTMLParser):
 def __init__(self): super().__init__(); self.in_review=False; self.buf=[]; self.reviews=[]
 def handle_starttag(self,tag,attrs):
  d=dict(attrs); cls=(d.get("class") or "").lower();
  if tag in ("article","div","li") and any(x in cls for x in ("review","comment")): self.in_review=True; self.buf=[]
 def handle_endtag(self,tag):
  if self.in_review and tag in ("article","div","li"):
   t=" ".join("".join(self.buf).split())
   if len(t)>=8: self.reviews.append(t)
   self.in_review=False
 def handle_data(self,data):
  if self.in_review: self.buf.append(data)

def generate(n,seed):
 random.seed(seed); brands=["QuietWave","SonicLeaf","AeroTune","NebuSound"]; templates=["通勤时降噪很安静，佩戴舒服。","音质清晰但偶尔断连，价格有点贵。","续航不错，适合旅行，收纳也方便。","通话有杂音，麦克风表现一般。","外观好看，性价比不错。","夹耳疼，戴久了不舒服。","还行，没有明显问题。"]
 return [{"review_id":f"sim-{i+1:03d}","brand":random.choice(brands),"review_text":random.choice(templates),"source_type":"simulated"} for i in range(n)]

def main():
 ap=argparse.ArgumentParser(); ap.add_argument("--url"); ap.add_argument("--output",required=True); ap.add_argument("--generate",type=int); ap.add_argument("--seed",type=int,default=20261112); a=ap.parse_args()
 if a.generate:
  rows=generate(a.generate,a.seed)
 else:
  if not a.url: raise SystemExit("请提供 --url 或 --generate")
  rp=urllib.robotparser.RobotFileParser(); rp.set_url(a.url.rstrip("/")+"/robots.txt")
  try: rp.read()
  except Exception: pass
  if not rp.can_fetch("consumer-insight-skill/0.2",a.url): raise SystemExit("robots.txt 不允许采集")
  req=Request(a.url,headers={"User-Agent":"consumer-insight-skill/0.2 (educational; contact unavailable)"})
  with urlopen(req,timeout=15) as res: html=res.read().decode("utf-8","ignore")
  p=ReviewParser(); p.feed(html); rows=[{"review_id":f"web-{i+1:03d}","review_text":t,"source_type":"public_html","source_url":a.url} for i,t in enumerate(dict.fromkeys(p.reviews))]
  if not rows: raise SystemExit("未在公开 HTML 找到评论；可改用 --generate")
 Path(a.output).parent.mkdir(parents=True,exist_ok=True)
 with open(a.output,"w",encoding="utf-8-sig",newline="") as f:
  w=csv.DictWriter(f,fieldnames=sorted({k for r in rows for k in r})); w.writeheader(); w.writerows(rows)
 print(f"wrote {len(rows)} rows to {a.output}")
if __name__=="__main__": main()
