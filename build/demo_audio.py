# -*- coding: utf-8 -*-
"""데모 음성 생성 — 홈의 '풀 데모'가 재생하는 통화 음성.

두 목소리(손님·AI)를 신경망 TTS(Microsoft Edge 음성)로 만든다. 사이트가
파는 실제 AI 음성이 아니라 시연용이며, 페이지는 그렇게 표시한다.
생성 결과는 assets/audio/demo/<lang>/NN-<who>.mp3 와 manifest.json(길이 포함).

    python build/demo_audio.py            # 없는 파일만 만든다
    python build/demo_audio.py --force    # 전부 다시 만든다
"""
import asyncio
import io
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "audio", "demo")

VOICES = {
    "ko": {"ai": ("ko-KR-InJoonNeural", "-3%", "-2Hz"), "user": ("ko-KR-SunHiNeural", "+4%", "+3Hz")},
    "en": {"ai": ("en-US-AndrewNeural", "-2%", "-1Hz"), "user": ("en-US-AvaNeural", "+3%", "+2Hz")},
}

# 1장 — 밤 11:42, 전화. 가상의 치과 '밝은미소치과 / Brightside Dental'.
LINES = {
    "ko": [
        ("ai",   "안녕하세요, 밝은미소치과입니다. 지금은 진료가 끝난 시간이지만, 예약과 문의는 제가 도와드릴 수 있어요. 무엇을 도와드릴까요?"),
        ("user", "저기, 앞니가 깨졌는데요… 크라운 하면 얼마나 하고, 이번 주에 볼 수 있을까요?"),
        ("ai",   "많이 놀라셨겠어요. 저희 요금표 기준으로 지르코니아 크라운은 55만원이고, 정확한 금액은 검진과 엑스레이 후에 확정됩니다. 이번 주는 목요일 오전 10시 30분과 금요일 오전 8시가 비어 있어요. 어느 쪽이 편하세요?"),
        ("user", "목요일이요."),
        ("ai",   "네, 목요일 10시 30분으로 잡아 드릴게요. 성함과 연락처를 말씀해 주시겠어요?"),
        ("user", "김지은이고요, 010-4482-5137이에요."),
        ("ai",   "김지은 님, 목요일 10시 30분 예약되었습니다. 확인 문자를 지금 보내 드리고, 처음 오시는 거라 위치와 주차 안내도 함께 넣어 드릴게요. 혹시 지금 많이 아프신가요?"),
        ("user", "조금 시린 정도예요."),
        ("ai",   "그러시면 목요일까지 찬 음식은 피해 주시고, 통증이 갑자기 심해지면 이 번호로 다시 전화 주세요. 밤에도 제가 받습니다. 목요일에 뵙겠습니다."),
        ("user", "네, 감사합니다."),
        ("ai",   "감사합니다. 편안한 밤 되세요."),
    ],
    "en": [
        ("ai",   "Thanks for calling Brightside Dental. We're closed for the night, but I can book appointments and answer questions. How can I help?"),
        ("user", "Hi — I chipped a front tooth. How much is a crown, and can anyone see me this week?"),
        ("ai",   "I'm sorry, that's never fun. From our fee schedule, a crown runs eleven hundred to sixteen hundred dollars depending on the material, and the exact figure is confirmed after an exam and X-ray. This week I have Thursday at ten thirty or Friday at eight. Which works better?"),
        ("user", "Thursday, please."),
        ("ai",   "Thursday at ten thirty it is. Can I get your name and a mobile number?"),
        ("user", "It's Jane Kim, five five five, zero one four seven."),
        ("ai",   "Thank you, Jane. You're booked for Thursday at ten thirty. I'm texting you a confirmation now, with directions and parking since it's your first visit. Is the tooth hurting right now?"),
        ("user", "It's a little sensitive, that's all."),
        ("ai",   "Then avoid very cold food until Thursday, and if the pain gets worse, call this number again — I answer at night too. We'll see you Thursday."),
        ("user", "Great, thanks."),
        ("ai",   "Thank you. Have a good night."),
    ],
}


async def make(lang, i, who, text, force):
    import edge_tts
    voice, rate, pitch = VOICES[lang][who]
    d = os.path.join(OUT, lang)
    os.makedirs(d, exist_ok=True)
    fn = "%02d-%s.mp3" % (i + 1, who)
    p = os.path.join(d, fn)
    if os.path.exists(p) and not force:
        return fn
    tts = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)
    await tts.save(p)
    return fn


def mp3_duration(path):
    try:
        from mutagen.mp3 import MP3
        return round(MP3(path).info.length, 2)
    except Exception:
        return None


async def main():
    force = "--force" in sys.argv
    manifest = {}
    for lang, lines in LINES.items():
        items = []
        for i, (who, text) in enumerate(lines):
            fn = await make(lang, i, who, text, force)
            items.append({"file": fn, "who": who, "text": text, "dur": mp3_duration(os.path.join(OUT, lang, fn))})
            print(lang, fn, items[-1]["dur"], "s")
        manifest[lang] = items
    io.open(os.path.join(OUT, "manifest.json"), "w", encoding="utf-8").write(json.dumps(manifest, ensure_ascii=False, indent=1))
    tot = {l: round(sum((x["dur"] or 0) for x in v), 1) for l, v in manifest.items()}
    print("manifest written; speech seconds:", tot)


if __name__ == "__main__":
    asyncio.run(main())
