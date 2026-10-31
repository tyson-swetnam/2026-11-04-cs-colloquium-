"""Slide 16: compute what is computable from the fetched sources (run 01_fetch_sources.py first).

1. Clef release facts from the Hugging Face model API: creation date, licence tag, base model,
   parameter count (safetensors total) -> data/processed/clef_releases.csv
2. Static read (ast, not executed) of Clef's published joint_schema_model.py: does inference call
   the backbone once with no token generation, and is every answer drawn from the caller's options?
   -> data/processed/clef_code_checks.csv
3. Better Stack's 200-comment test: overall vs per-question mean -> data/processed/betterstack_test.csv
"""

from __future__ import annotations

import ast
import json
import re
from pathlib import Path

import pandas as pd

SLIDE = Path(__file__).resolve().parents[1]
RAW = SLIDE / "data" / "raw" / "sources"
OUT = SLIDE / "data" / "processed"


def releases() -> pd.DataFrame:
    rows = []
    for name in ("hf_api_clef", "hf_api_clef_flash", "hf_api_clef_omni"):
        d = json.loads((RAW / f"{name}.json").read_text())
        tags = d.get("tags", [])
        lic = (RAW / f"{name.replace('hf_api_', 'hf_')}_license.txt")
        rows.append({
            "model": d["id"],
            "created_utc": d.get("createdAt"),
            "license_tag": next((t.split(":", 1)[1] for t in tags if t.startswith("license:")), ""),
            "license_file_is_apache2": ("Apache License" in lic.read_text() and "Version 2.0" in lic.read_text()) if lic.exists() else None,
            "base_model": next((t.split(":", 1)[1] for t in tags if t.startswith("base_model:") and t.count(":") == 1), ""),
            "params_total": d.get("safetensors", {}).get("total"),
            "params_billion": round(d.get("safetensors", {}).get("total", 0) / 1e9, 2),
            "gated": d.get("gated"),
            "private": d.get("private"),
        })
    return pd.DataFrame(rows)


def code_checks() -> pd.DataFrame:
    src = (RAW / "hf_clef_code.txt").read_text()
    tree = ast.parse(src)
    funcs = {n.name: n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)}
    calls = [n for n in ast.walk(tree) if isinstance(n, ast.Call)]
    attr_names = [c.func.attr for c in calls if isinstance(c.func, ast.Attribute)]
    fwd = ast.get_source_segment(src, funcs["forward"]) if "forward" in funcs else ""
    # ClefModel.forward is the last 'forward' defined; find it explicitly
    clef_cls = next(n for n in ast.walk(tree) if isinstance(n, ast.ClassDef) and n.name == "ClefModel")
    clef_fwd = next(n for n in clef_cls.body if isinstance(n, ast.FunctionDef) and n.name == "forward")
    clef_fwd_src = ast.get_source_segment(src, clef_fwd)
    answer_src = ast.get_source_segment(src, funcs["systemone_answer"])
    options_src = ast.get_source_segment(src, funcs["question_options"])
    serve_src = ast.get_source_segment(src, funcs["systemone"])
    checks = [
        ("no call to .generate() anywhere in the file", "generate" not in attr_names),
        ("ClefModel.forward calls the backbone text_model exactly once", clef_fwd_src.count("text_model(") == 1),
        ("backbone called with use_cache=False (no incremental decoding)", "use_cache=False" in clef_fwd_src),
        ("systemone() runs the model once per request", serve_src.count("model(collate_records") == 1),
        ("choice answer = argmax over the caller's listed options", 'options = [str(option) for option in question["criteria"]]' in answer_src and "max(options" in answer_src),
        ("noul answer = probability of 'true' (yes/no only)", 'probabilities["true"]' in answer_src and '("true", "false")' in options_src),
        ("score answer = probability-weighted mean of caller's levels", "sum(index * probabilities[level]" in answer_src),
        ("response reports output_tokens = 0", '"output_tokens": 0' in serve_src),
    ]
    return pd.DataFrame(checks, columns=["check", "passes"])


def betterstack() -> pd.DataFrame:
    t = (RAW / "betterstack.txt").read_text()
    seg = t[t.find("Question Jev Clef Winner") + len("Question Jev Clef Winner"):t.find("Clef was more accurate")]
    rows = re.findall(r"([A-Z][A-Za-z /]+?) (\d+)% (\d+)% (Jev|Clef)", seg)
    df = pd.DataFrame(rows, columns=["question", "jev_pct", "clef_pct", "winner"]).astype({"jev_pct": int, "clef_pct": int})
    df["question"] = df["question"].str.strip()
    mean = pd.DataFrame([{"question": "MEAN of 5 questions (computed)", "jev_pct": df.jev_pct.mean(), "clef_pct": df.clef_pct.mean(), "winner": ""}])
    overall = re.search(r"Jev matched the referee (\d+)% of the time and Clef matched it (\d+)%", t)
    rep = pd.DataFrame([{"question": "OVERALL as reported", "jev_pct": int(overall.group(1)), "clef_pct": int(overall.group(2)), "winner": ""}])
    referee = re.search(r"(Claude [^ ]+ [\d.]+) served as the referee", t)
    out = pd.concat([df, mean, rep], ignore_index=True)
    out["referee"] = referee.group(1) if referee else ""
    return out


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for name, df in (("clef_releases", releases()), ("clef_code_checks", code_checks()), ("betterstack_test", betterstack())):
        df.to_csv(OUT / f"{name}.csv", index=False)
        print(f"\n# {name}\n{df.to_string(index=False)}")


if __name__ == "__main__":
    main()
