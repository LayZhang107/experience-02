import csv
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
rows = {r["review_id"]: r["review_text"] for r in csv.DictReader((root / "data/sample/reviews_10.csv").open(encoding="utf-8-sig"))}
items = json.loads((root / "outputs/sample_insights.json").read_text(encoding="utf-8"))
required = {"review_id", "sentiment", "need", "pain_point", "scenario", "purchase_barrier", "evidence", "confidence"}
assert len(items) == 10
for item in items:
    assert set(item) == required
    assert item["evidence"] == "unknown" or item["evidence"] in rows[item["review_id"]]
print("validated 10 records and evidence traceability")
