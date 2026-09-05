# -*- coding: utf-8 -*-
"""데모 음성 생성 — 모든 업종 대본의 통화 줄을 신경망 TTS(Microsoft Edge 음성)로 만든다.

시연용 합성 음성이며 페이지는 그렇게 표시한다. 결과는
assets/audio/demo/<slug>/<lang>/NN-<who>.mp3 이고, 끝나면 build/demo_build.py 가 길이를 JSON 에 붙인다.

    python build/demo_audio.py                 # 없는 파일만 만든다 (전 업종)
    python build/demo_audio.py dental salons   # 이 업종만
    python build/demo_audio.py --force         # 전부 다시

목소리: AI 는 언어마다 한 목소리(브랜드 목소리). 손님은 업종마다 남·여를 번갈아 써서 55개가 같은
사람처럼 들리지 않게 한다. 손님 쪽은 플레이어가 전화 음질 필터를 다시 입힌다.
파일 크기: Edge 는 48kbps 로 주는데, 55×2×~11 줄이면 수십 MB 라 ffmpeg 로 32kbps 로 줄인다.
"""
import asyncio
import io
import os
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "build", "demo"))
from validate import load_all  # noqa: E402

OUT = os.path.join(ROOT, "assets", "audio", "demo")

AI_VOICE = {"ko": ("ko-KR-InJoonNeural", "-3%", "-2Hz"), "en": ("en-US-AndrewNeural", "-2%", "-1Hz")}
CUSTOMER = {
    "ko": [("ko-KR-SunHiNeural", "+4%", "+3Hz"), ("ko-KR-HyunsuMultilingualNeural", "+3%", "+1Hz")],
    "en": [("en-US-AvaNeural", "+3%", "+2Hz"), ("en-US-BrianNeural", "+2%", "+0Hz"),
           ("en-US-EmmaNeural", "+3%", "+1Hz"), ("en-US-GuyNeural", "+2%", "+1Hz")],
}


def ffmpeg():
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        return None


FF = ffmpeg()


async def make(sem, slug, lang, i, who, text, voice, force):
    import edge_tts
    d = os.path.join(OUT, slug, lang)
    os.makedirs(d, exist_ok=True)
    fn = "%02d-%s.mp3" % (i + 1, who)
    p = os.path.join(d, fn)
    if os.path.exists(p) and os.path.getsize(p) > 1000 and not force:
        return fn, False
    vname, rate, pitch = voice
    async with sem:
        for attempt in range(5):
            try:
                tts = edge_tts.Communicate(text, vname, rate=rate, pitch=pitch)
                tmp = p + ".raw.mp3"
                await tts.save(tmp)
                break
            except Exception as e:
                if attempt == 4: raise
                await asyncio.sleep(3 + attempt * 4)
    if FF:
        r = subprocess.run([FF, "-y", "-loglevel", "error", "-i", tmp, "-ac", "1", "-b:a", "32k", "-ar", "24000", p])
        if r.returncode == 0 and os.path.exists(p) and os.path.getsize(p) > 1000:
            os.remove(tmp)
        else:
            os.replace(tmp, p)
    else:
        os.replace(tmp, p)
    return fn, True


async def main():
    force = "--force" in sys.argv
    customers = "--customers" in sys.argv   # 손님 대사만 다시 만든다 (목소리 배정을 바꿨을 때)
    only = [a for a in sys.argv[1:] if not a.startswith("-")]
    S = load_all()
    order = sorted(S)                       # 목소리 배정은 전체 목록의 자리로 — 일부만 다시 돌려도 같은 목소리
    slugs = [s for s in order if not only or s in only]
    sem = asyncio.Semaphore(3)
    jobs = []
    for slug in slugs:
        k = order.index(slug)
        for lang in ("ko", "en"):
            cust = CUSTOMER[lang][k % len(CUSTOMER[lang])]
            for i, ln in enumerate(S[slug][lang]["lines"]):
                voice = AI_VOICE[lang] if ln["who"] == "ai" else cust
                jobs.append(make(sem, slug, lang, i, ln["who"], ln["text"], voice, force or (customers and ln["who"] != "ai")))
    made = 0; skipped = 0; failed = 0
    for n in range(0, len(jobs), 24):
        chunk = jobs[n:n + 24]
        res = await asyncio.gather(*chunk, return_exceptions=True)
        for r in res:
            if isinstance(r, Exception): failed += 1; print("  !!", str(r)[:120])
            elif r[1]: made += 1
            else: skipped += 1
        print("  %d/%d  made=%d skipped=%d failed=%d" % (min(n + 24, len(jobs)), len(jobs), made, skipped, failed))
    print("done. slugs=%d lines=%d made=%d skipped=%d failed=%d" % (len(slugs), len(jobs), made, skipped, failed))


if __name__ == "__main__":
    asyncio.run(main())
