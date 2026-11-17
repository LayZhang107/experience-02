import argparse, csv, json, re
from pathlib import Path

NEED_RULES={
 "降噪":["降噪","安静","隔音"],"佩戴舒适":["舒服","舒适","夹耳","硌","疼"],"续航":["续航","电量","充电"],
 "音质":["音质","低音","高音","声音"],"通话":["通话","麦克风","电话"],"连接稳定":["连接","断连","蓝牙"],
 "便携":["便携","轻","收纳"],"性价比":["性价比","便宜","贵","价格"],"外观":["外观","颜值","好看"]}
SCENARIOS={"通勤":["通勤","地铁","公交"],"学习":["学习","图书馆"],"办公":["办公","会议"],"运动":["运动","跑步"],"旅行":["旅行","飞机"],"通话":["通话","电话"],"居家":["家里","居家"]}
NEG=["差","问题","断连","漏音","夹耳","疼","不舒服","太贵","失望","杂音","坏"]
POS=["好","不错","满意","舒服","清晰","优秀","喜欢","安静","推荐"]
BARRIERS={"价格":["贵","价格","便宜"],"舒适度担忧":["夹耳","疼","不舒服"],"质量担忧":["坏","质量","故障"],"功能不足":["没有","不足","不支持"],"售后担忧":["售后","退货"]}

def first_hit(text, mapping):
 for label, words in mapping.items():
  for w in words:
   if w in text: return label
 return "unknown"

def encode(row):
 text=(row.get("review_text") or "").strip(); low=text.lower()
 evidence="unknown"
 for term in re.findall(r"[^，。！？；,.!?; ]+", text):
  if any(k in term for k in NEG+POS): evidence=term; break
 if evidence=="unknown" and text: evidence=text[:min(12,len(text))]
 neg=any(k in low for k in NEG); pos=any(k in low for k in POS)
 sentiment="mixed" if neg and pos else "negative" if neg else "positive" if pos else "neutral" if text else "unknown"
 need=first_hit(text,NEED_RULES); scenario=first_hit(text,SCENARIOS)
 pain_rules={"降噪差":["降噪差","不安静"],"漏音":["漏音"],"断连":["断连"],"夹耳疼痛":["夹耳","硌","疼"],"续航不足":["续航短","没电"],"通话杂音":["杂音","听不清"],"价格偏高":["太贵","价格高"]}
 pain="unknown" if not text else next((label for label, words in pain_rules.items() if any(word in text for word in words)), None)
 pain=pain or ("none" if not neg and text else "unknown")
 barrier="无" if text and not neg else first_hit(text,BARRIERS)
 if not text: barrier="unknown"
 confidence="high" if text and evidence!="unknown" and (need!="unknown" or sentiment in ["positive","negative"]) else "medium" if text else "low"
 return {"review_id":row.get("review_id",""),"sentiment":sentiment,"need":need,"pain_point":pain,"scenario":scenario,"purchase_barrier":barrier,"evidence":evidence,"confidence":confidence}

def main():
 ap=argparse.ArgumentParser(); ap.add_argument("--input",required=True); ap.add_argument("--output",required=True); a=ap.parse_args()
 with open(a.input,encoding="utf-8-sig",newline="") as f: rows=list(csv.DictReader(f))
 out=[encode(r) for r in rows]
 Path(a.output).parent.mkdir(parents=True,exist_ok=True); Path(a.output).write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding="utf-8")
 print(json.dumps({"records":len(out),"output":a.output},ensure_ascii=False))
if __name__=="__main__": main()
