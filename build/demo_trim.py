# -*- coding: utf-8 -*-
"""데모 음성의 꼬리 무음을 잘라 낸다 (edge-tts 가 문장 끝에 1~2초 무음을 붙인다).

뒤집어서 앞쪽(=원래 꼬리) 무음을 0.3초만 남기고 잘라 낸 뒤 다시 뒤집는다 (중간 쉼은 건드리지 않음). 32kbps mono 로 다시 인코딩.
이미 다듬은 파일은 건너뛴다(<file>.trim 표식). 실행: python build/demo_trim.py [slug ...]
끝나면 python build/demo_build.py 로 JSON 의 dur 을 갱신할 것."""
import glob
import io
import os
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)


def ffmpeg():
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        return None


def main():
    ff = ffmpeg()
    if not ff:
        print("ffmpeg 없음"); sys.exit(1)
    only = [a for a in sys.argv[1:] if not a.startswith("-")]
    files = sorted(glob.glob("assets/audio/demo/*/*/*.mp3"))
    if only:
        files = [f for f in files if f.replace("\\", "/").split("/")[3] in only]
    n = 0; skipped = 0; failed = 0
    for f in files:
        mark = f + ".trim"
        if os.path.exists(mark) and os.path.getmtime(mark) >= os.path.getmtime(f):
            skipped += 1; continue
        tmp = f + ".tmp.mp3"
        r = subprocess.run([ff, "-y", "-loglevel", "error", "-i", f,
                            "-af", "areverse,silenceremove=start_periods=1:start_silence=0.3:start_threshold=-45dB,areverse",
                            "-ac", "1", "-b:a", "32k", "-ar", "24000", tmp])
        if r.returncode == 0 and os.path.exists(tmp) and os.path.getsize(tmp) > 800:
            os.replace(tmp, f); io.open(mark, "w").write("1"); n += 1
        else:
            failed += 1
            if os.path.exists(tmp): os.remove(tmp)
    print("trimmed=%d skipped=%d failed=%d" % (n, skipped, failed))


if __name__ == "__main__":
    main()
