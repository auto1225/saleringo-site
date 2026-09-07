# -*- coding: utf-8 -*-
"""관리자 시스템 정적 검사 — 배포 전에 걸러야 할 것들.

    python build/admincheck.py

무엇을 보는가.
  1. 비밀이 파일에 없는가 (service_role, sb_secret, JWT, 토큰 모양의 문자열).
  2. 관리자 파일이 500줄을 넘지 않는가 (넘으면 경고).
  3. i18n 사전의 ko/en 키가 같은가, 화면 코드가 쓰는 키가 사전에 있는가.
  4. vercel.json 이 유효하고 /admin, /api/admin 재작성·헤더·includeFiles 가 있는가.
  5. 사이트맵·라우트가 admin 을 포함하지 않는가, 화면 HTML 이 en/ko 아래에 없는가.
  6. 화면 HTML 이 /assets/admin/ 자산을 ?v= 와 함께 부르고, 외부 스크립트가 없는가.
  7. JS 파일이 문법상 유효한가 (node --check), innerHTML 에 데이터가 들어가지 않는가(경고).
"""
import glob
import io
import json
import os
import re
import subprocess
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

problems = []
warns = []


def read(p):
    return io.open(p, encoding='utf-8').read()


ADMIN_FILES = (sorted(glob.glob('api/admin.js')) + sorted(glob.glob('api/_admin/**/*.*', recursive=True))
               + sorted(glob.glob('assets/admin/**/*.*', recursive=True))
               + sorted(glob.glob('supabase/admin/*.sql')))
if not ADMIN_FILES:
    problems.append(('파일', '.', '관리자 파일이 하나도 없습니다 (api/admin.js, api/_admin/, assets/admin/, supabase/admin/)'))

# ── 1. 비밀 ──────────────────────────────────────────────────────────────
#     service_role 는 SQL 의 grant 대상(역할 이름)으로 정당하게 나옵니다.
#     문제는 그 역할의 "키" 가 코드에 박히는 것이므로, 키 모양만 봅니다.
SECRET = re.compile(r'sb_secret_[A-Za-z0-9_-]{10,}|eyJ[A-Za-z0-9_-]{30,}\.[A-Za-z0-9_-]{20,}'
                    r'|sk_(live|test)_[A-Za-z0-9]{10,}|re_[A-Za-z0-9]{24,}|xox[bp]-[A-Za-z0-9-]{20,}'
                    r'|SERVICE_ROLE_KEY\s*[:=]\s*[\'"][^\'"]{10,}')
GRANT = re.compile(r'\b(grant|revoke)\b', re.I)
for fp in ADMIN_FILES + ['vercel.json']:
    for i, line in enumerate(read(fp).splitlines(), 1):
        m = SECRET.search(line)
        if m:
            problems.append(('비밀', '%s:%d' % (fp, i), m.group(0)[:24] + '…'))
        # service_role 이 grant/revoke 문 밖에서 나오면 사람이 봐야 합니다.
        if 'service_role' in line and not GRANT.search(line):
            warns.append(('service_role', '%s:%d' % (fp, i), line.strip()[:90]))

# ── 2. 크기 ──────────────────────────────────────────────────────────────
for fp in ADMIN_FILES:
    n = read(fp).count('\n') + 1
    if n > 500 and not fp.endswith('.sql'):
        warns.append(('500줄', fp, '%d줄' % n))

# ── 3. i18n ──────────────────────────────────────────────────────────────
#     사전은 `'키': ['한국어', 'English']` 한 줄에 두 언어를 같이 둡니다.
#     그래서 "한쪽만 번역된" 상태가 구조적으로 생기지 않고, 여기서는 두 칸이
#     실제로 채워졌는지와 코드가 부르는 키가 사전에 있는지만 봅니다.
DICTS = ['assets/admin/i18n-core.js', 'assets/admin/i18n-entities.js']
#     한 줄에 여러 항목이 들어 있으므로 줄머리에 고정하지 않는다.
ENTRY = re.compile(r'''(?<![A-Za-z0-9_.])'([A-Za-z0-9_.-]+)'\s*:\s*\[\s*'((?:[^'\\]|\\.)*)'\s*,\s*'((?:[^'\\]|\\.)*)'\s*\]''')
known = {}
for fp in DICTS:
    if not os.path.exists(fp):
        problems.append(('i18n', fp, '없습니다'))
        continue
    src = read(fp)
    found = ENTRY.findall(src)
    if not found:
        problems.append(('i18n', fp, "사전 항목(`'키': ['ko','en']`)을 찾지 못했습니다"))
    for key, ko, en in found:
        if key in known:
            problems.append(('i18n', fp, '중복 키: %s (앞: %s)' % (key, known[key])))
        known[key] = fp
        if not ko.strip():
            problems.append(('i18n', fp, '한국어가 비었습니다: %s' % key))
        if not en.strip():
            problems.append(('i18n', fp, '영어가 비었습니다: %s' % key))
    # 두 칸짜리가 아닌 항목(한 언어만 적은 줄)을 잡는다
    for m in re.finditer(r'''(?m)^\s*'([^']+)'\s*:\s*\[''', src):
        seg = src[m.end():src.find(']', m.end()) + 1]
        if seg.count("',") < 1 and seg.count('", ') < 1:
            problems.append(('i18n', fp, '두 언어가 아닌 항목: %s' % m.group(1)))
used = set()
for fp in glob.glob('assets/admin/**/*.js', recursive=True) + glob.glob('api/_admin/pages/*.html'):
    slug = fp.replace('\\', '/')
    if slug in DICTS or slug.endswith('/i18n.js'):
        continue  # 사전 자체와 t() 를 정의하는 파일(주석의 예시)은 건너뛴다
    src = re.sub(r'/\*[\s\S]*?\*/', ' ', read(fp))  # 주석 속 예시는 사용처가 아니다
    # 완성된 키만 본다. `t('col.' + name)` 처럼 이어 붙이는 것은 조각이라 건너뛴다
    # (enumLabel 의 첫 인자도 접두사이므로 제외).
    for m in re.finditer(r'''\b(?:t|has)\(\s*['"]([A-Za-z0-9_.-]+)['"]\s*[,)]''', src):
        used.add(m.group(1))
    for m in re.finditer(r'''data-i18n="([A-Za-z0-9_.-]+)"''', src):
        used.add(m.group(1))
for fp in glob.glob('api/_admin/pages/*.html'):
    for m in re.finditer(r'''data-i18n="([A-Za-z0-9_.-]+)"''', read(fp)):
        used.add(m.group(1))
missing = sorted(k for k in used if k not in known)
for k in missing[:30]:
    problems.append(('i18n', 'assets/admin', '사전에 없는 키 사용: %s' % k))
if len(missing) > 30:
    problems.append(('i18n', 'assets/admin', '… 외 %d개' % (len(missing) - 30)))
if known:
    print('i18n 사전 %d개 키 (%s)' % (len(known), ', '.join(os.path.basename(d) for d in DICTS)))

# ── 4. vercel.json ───────────────────────────────────────────────────────
try:
    V = json.load(io.open('vercel.json', encoding='utf-8'))
    rw = {(r.get('source'), r.get('destination')) for r in V.get('rewrites', [])}
    for src_, dst in (('/api/admin/:path*', '/api/admin?p=/:path*'), ('/admin', '/api/admin?page=index'), ('/admin/:path*', '/api/admin?page=/:path*')):
        if (src_, dst) not in rw:
            problems.append(('vercel', 'vercel.json', '재작성 없음: %s → %s' % (src_, dst)))
    fn = V.get('functions', {}).get('api/admin.js', {})
    if 'api/_admin/**' not in str(fn.get('includeFiles', '')):
        problems.append(('vercel', 'vercel.json', 'functions["api/admin.js"].includeFiles 에 api/_admin/** 가 없습니다'))
    hdr = json.dumps(V.get('headers', []))
    if 'noindex' not in hdr or '/admin' not in hdr:
        problems.append(('vercel', 'vercel.json', '/admin 경로의 X-Robots-Tag noindex 헤더가 없습니다'))
    if len(V.get('redirects', [])) < 900:
        problems.append(('vercel', 'vercel.json', 'redirects 가 %d개 — 기존 919개가 사라졌습니다' % len(V.get('redirects', []))))
except Exception as e:  # noqa
    problems.append(('vercel', 'vercel.json', 'JSON 오류: %s' % e))

# ── 5. 노출 ──────────────────────────────────────────────────────────────
if os.path.exists('sitemap.xml') and 'admin' in read('sitemap.xml'):
    problems.append(('노출', 'sitemap.xml', 'admin 이 사이트맵에 있습니다'))
for fp in glob.glob('en/admin*') + glob.glob('ko/admin*') + glob.glob('admin/*.html'):
    problems.append(('노출', fp, '관리자 화면이 정적 경로에 있습니다 (api/_admin/pages/ 에만 둘 것)'))
for fp in glob.glob('api/_admin/pages/*.html'):
    s = read(fp)
    for m in re.finditer(r'<script[^>]+src="([^"]+)"', s):
        u = m.group(1)
        if not u.startswith('/assets/admin/'):
            problems.append(('자산', fp, '외부 또는 잘못된 스크립트: %s' % u))
        elif '?v=' not in u:
            warns.append(('자산', fp, '판 번호 없는 스크립트: %s' % u))
    for m in re.finditer(r'<link[^>]+href="([^"]+)"', s):
        u = m.group(1)
        if u.startswith('/assets/admin/') and '?v=' not in u:
            warns.append(('자산', fp, '판 번호 없는 CSS: %s' % u))
        if u.startswith('http') and not u.startswith('https://fonts.g'):
            problems.append(('자산', fp, '외부 링크: %s' % u))
    if 'noindex' not in s:
        warns.append(('노출', fp, '<meta name="robots" content="noindex"> 가 없습니다'))

# ── 6. JS 문법·innerHTML ─────────────────────────────────────────────────
JS = sorted(glob.glob('api/admin.js') + glob.glob('api/_admin/*.js') + glob.glob('assets/admin/**/*.js', recursive=True))
for fp in JS:
    r = subprocess.run(['node', '--check', fp], capture_output=True, text=True)
    if r.returncode != 0:
        problems.append(('문법', fp, (r.stderr or r.stdout).strip().splitlines()[-1][:160] if (r.stderr or r.stdout).strip() else 'node --check 실패'))
    s = read(fp)
    for i, line in enumerate(s.splitlines(), 1):
        if '.innerHTML' in line and '=' in line and re.search(r'\$\{|\+\s*[a-zA-Z_]', line.split('innerHTML', 1)[1]):
            warns.append(('innerHTML', '%s:%d' % (fp, i), line.strip()[:110]))
    if 'api/' in fp.replace('\\', '/') and re.search(r'console\.log\(', s):
        warns.append(('로그', fp, 'console.log 가 남아 있습니다'))

# ── 결과 ─────────────────────────────────────────────────────────────────
for kind, fp, msg in warns:
    print('경고  %-9s %-40s %s' % (kind, fp.replace(os.sep, '/'), msg))
if not problems:
    print('관리자 정적 검사 통과 (%d 파일, 경고 %d)' % (len(ADMIN_FILES), len(warns)))
else:
    for kind, fp, msg in problems:
        print('문제  %-9s %-40s %s' % (kind, fp.replace(os.sep, '/'), msg))
    print('\n합계 %d건' % len(problems))
    sys.exit(1)
