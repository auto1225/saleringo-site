# -*- coding: utf-8 -*-
"""업종별 데모 대본 → assets/demo/<slug>.json

build/demo/scripts_*.py 의 SCRIPTS 를 읽어 플레이어(assets/js/demofull.js)가 먹는 JSON 으로 쓴다.
음성 파일(assets/audio/demo/<slug>/<lang>/NN-<who>.mp3)이 있으면 그 길이(dur)와 파일명을 줄마다 붙인다.
음성이 아직 없으면 dur 없이 쓴다 — 플레이어는 글자 수로 길이를 어림한다.

    python build/demo_build.py            # 전부
    python build/demo_build.py dental     # 하나만
"""
import io
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "build", "demo"))
from validate import load_all  # noqa: E402

OUT = os.path.join(ROOT, "assets", "demo")
AUDIO = os.path.join(ROOT, "assets", "audio", "demo")


def mp3_duration(path):
    try:
        from mutagen.mp3 import MP3
        return round(MP3(path).info.length, 2)
    except Exception:
        return None


def build_one(slug, spec):
    out = {}
    for lang in ("ko", "en"):
        d = json.loads(json.dumps(spec[lang], ensure_ascii=False))  # deep copy
        for i, ln in enumerate(d["lines"]):
            fn = "%02d-%s.mp3" % (i + 1, ln["who"])
            p = os.path.join(AUDIO, slug, lang, fn)
            if os.path.exists(p):
                ln["file"] = fn
                dur = mp3_duration(p)
                if dur: ln["dur"] = dur
        out[lang] = d
    os.makedirs(OUT, exist_ok=True)
    io.open(os.path.join(OUT, slug + ".json"), "w", encoding="utf-8").write(json.dumps(out, ensure_ascii=False, separators=(",", ":")))
    have = sum(1 for lang in ("ko", "en") for ln in out[lang]["lines"] if ln.get("file"))
    need = sum(len(out[lang]["lines"]) for lang in ("ko", "en"))
    return have, need


def main():
    only = [a for a in sys.argv[1:] if not a.startswith("-")]
    S = load_all()
    rows = []
    for slug, spec in S.items():
        if only and slug not in only: continue
        have, need = build_one(slug, spec)
        rows.append((slug, have, need))
    for slug, have, need in rows:
        print("%-22s audio %2d/%2d" % (slug, have, need))
    print("wrote %d scripts to assets/demo/" % len(rows))


if __name__ == "__main__":
    main()
