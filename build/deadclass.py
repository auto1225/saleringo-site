# -*- coding: utf-8 -*-
"""HTML 에는 있는데 CSS 어디에도 규칙이 없는 클래스를 찾는다.

    python build/deadclass.py


사이트맵 페이지의 위아래 여백이 사라진 이유가 이것이었다.
섹션에 class="t-lg" 를 썼는데 그런 클래스가 없다. 이 사이트의 간격 토큰은
t-sm, t-md, t-xl 세 개뿐이고 t-lg 는 내가 지어낸 이름이었다.

없는 클래스는 조용히 아무 일도 하지 않는다. 오타 하나가 165개 섹션의
padding 을 0 으로 만들어도 브라우저는 아무 말도 하지 않고, 정적 검사도
링크 검사도 이것을 잡지 못한다. 그래서 따로 본다.

찾는 방법
  · 모든 .css 파일과 각 페이지의 <style> 블록에서 .클래스이름 을 모은다.
  · 모든 페이지의 class="..." 에서 쓰인 이름을 모은다.
  · 쓰였는데 규칙이 없는 것을 센다.

자바스크립트가 붙였다 뗐다 하는 표시용 클래스는 규칙이 없어도 정상이라
따로 빼 둔다.
"""
import glob
import io
import os
import re
import sys
from collections import defaultdict

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
os.chdir(r'C:\2026make\saleringo\website-global')

# 자바스크립트가 표시용으로만 쓰는 것들 - CSS 규칙이 없어도 잘못이 아니다
JS_ONLY = {
    'reveal', 'in', 'on', 'sr-force', 'srjs', 'srwrap', 'is-mid', 'cw',
    'np-here', 'grain', 'wrap', 'two', 'r',
}


def css_classes():
    have = set()
    for p in glob.glob('assets/css/*.css'):
        s = io.open(p, encoding='utf-8').read()
        have |= set(re.findall(r'\.(-?[_a-zA-Z][\w-]*)', s))
    return have


GLOBAL = css_classes()
pages = sorted(glob.glob('en/*.html') + glob.glob('en/industries/*.html') +
               glob.glob('ko/*.html') + glob.glob('ko/industries/*.html') +
               ['index.html', '404.html'])

missing = defaultdict(set)
for fp in pages:
    if not os.path.exists(fp):
        continue
    s = io.open(fp, encoding='utf-8').read()
    local = set()
    for m in re.finditer(r'<style[^>]*>(.*?)</style>', s, re.S):
        local |= set(re.findall(r'\.(-?[_a-zA-Z][\w-]*)', m.group(1)))
    known = GLOBAL | local | JS_ONLY
    used = set()
    for m in re.finditer(r'class="([^"]*)"', s):
        used |= set(m.group(1).split())
    for c in used - known:
        missing[c].add(fp.replace(os.sep, '/'))

if not missing:
    print('규칙 없는 클래스 없음')
else:
    for c in sorted(missing, key=lambda k: -len(missing[k])):
        files = sorted(missing[c])
        print('%-22s %3d개 페이지   예: %s' % (c, len(files), files[0]))
    print('\n합계 %d종, 연 %d곳' % (len(missing), sum(len(v) for v in missing.values())))
