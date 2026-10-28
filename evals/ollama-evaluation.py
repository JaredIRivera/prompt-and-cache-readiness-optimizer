"""Compare original and skill-generated prompts using local Ollama."""
import datetime
import json
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODEL = "gemma4:12b"
source = json.loads((ROOT / "evals/skill-evaluation-results.json").read_text(encoding="utf-8"))
cases = source["cases"]
JSON_MODE = "--json-mode" in sys.argv

def generate(prompt):
    payload = {"model":MODEL,"prompt":prompt,"stream":False,"think":False,"keep_alive":"10m","options":{"temperature":0,"seed":42,"num_ctx":4096,"num_predict":256}}
    if JSON_MODE: payload["format"]="json"
    request = urllib.request.Request("http://127.0.0.1:11434/api/generate",data=json.dumps(payload).encode(),headers={"Content-Type":"application/json"})
    started=time.monotonic()
    with urllib.request.urlopen(request,timeout=300) as response:
        result=json.load(response)
    result["wall_seconds"]=round(time.monotonic()-started,3)
    return {key:result.get(key) for key in ("model","response","done","done_reason","prompt_eval_count","prompt_eval_duration","eval_count","eval_duration","load_duration","total_duration","wall_seconds")}

if __name__=="__main__":
    data={"started_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"model":MODEL,"json_mode":JSON_MODE,"options":{"temperature":0,"seed":42,"num_ctx":4096,"num_predict":256},"source":"skill-evaluation-results.json","warmup":None,"results":[]}
    data["warmup"]=generate('Return only the JSON object {"ready":true}.' if JSON_MODE else "Return the word READY.")
    for i,case in enumerate(cases):
        for arm in (("original","rewritten") if i%2==0 else ("rewritten","original")):
            prompt=case["original"] if arm=="original" else case["rewrite_result"]["answer"]
            try:
                result=generate(prompt)
                try: result["passed"]=json.dumps(json.loads(result["response"]),sort_keys=True)==json.dumps(case["expected"],sort_keys=True)
                except (ValueError,TypeError):result["passed"]=False
            except Exception as exc: result={"error":type(exc).__name__,"passed":False}
            result.update({"id":case["id"],"arm":arm,"prompt":prompt,"expected":case["expected"]})
            data["results"].append(result)
            target="ollama-json-evaluation-results.json" if JSON_MODE else "ollama-evaluation-results.json"
            (ROOT/"evals"/target).write_text(json.dumps(data,indent=2),encoding="utf-8")
            print(len(data["results"]),case["id"],arm,"PASS" if result["passed"] else "FAIL",flush=True)
