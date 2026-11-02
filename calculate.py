#!/usr/bin/env python3
from pathlib import Path
from collections import Counter
import json,csv
R=Path(__file__).resolve().parent
def read(name):
    with (R/name).open(encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f))
e=read("EVIDENCE_MATRIX.csv");s=read("SELECTION_REGISTER.csv");u=read("SOURCE_REGISTER.csv");c=read("FACT_CLAIM_MAP.csv");m=read("SCENARIO_MEMBERSHIP.csv")
a=json.loads((R/"RESULTS.json").read_text(encoding="utf-8"))
assert (len(e),len(s),len(u),len(c),len(m))==(180,20,31,115,41)
assert len({x["candidate_id"] for x in s})==20
assert len({(x["candidate_id"],x["criterion_id"]) for x in e})==180
assert Counter(x["decision"] for x in s)==Counter({"INCLUDED_STANDARD":13,"CONDITIONAL_LARGE_3PL":1,"REJECTED_FOR_MAIN_CORPUS":6})
assert Counter(x["evidence_grade"] for x in e)==Counter({"D":62,"E":18,"G":35,"U":55,"X":9,"B":1})
assert not {"weight_pct_draft","preliminary_raw_0_to_4","score","rank"}.intersection(e[0])
source_ids={x["source_id"] for x in u}; assert len(source_ids)==31
assert all(x["source_id"] in source_ids for x in c)
assert all(x["source_id"] in source_ids for x in e if x["evidence_grade"] in ("D","E"))
grade={(x["candidate_id"],x["criterion_id"]):x["evidence_grade"] for x in e}
decision={x["candidate_id"]:x["decision"] for x in s}
for scenario in a["scenarios"]:
    sid=scenario["id"]
    std=scenario["standard"]
    big=scenario["conditional_large_3pl"]
    assert len(std)==scenario["standard_count"] and len(big)==scenario["conditional_large_3pl_count"]
    assert all(decision[x["candidate_id"]]=="INCLUDED_STANDARD" for x in std)
    assert all(decision[x["candidate_id"]]=="CONDITIONAL_LARGE_3PL" for x in big)
    ids={x["candidate_id"] for x in std+big}
    assert ids=={x["candidate_id"] for x in m if x["scenario"]==sid}
    for x in std+big:
        for metric in x["evidence"]:assert grade[(x["candidate_id"],metric)] in ("D","E")
assert a["metadata"]["publishedScores"] is False
print("INDEX-T054 PASS: 20 offers / 180 cells / 31 sources / 115 claims / 5 unranked scenarios")
