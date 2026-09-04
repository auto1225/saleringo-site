# -*- coding: utf-8 -*-
"""영어 페이지에 그림·사진을 넣는다. 멱등: <!--illus:NAME--> … <!--/illus:NAME--> 표식 사이를 갈아 끼운다.
실행: python build/illus_en.py"""
import io
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sys.path.insert(0, os.path.join(ROOT, "build"))
import illus  # noqa: E402

PH = 'https://images.pexels.com/photos/%s/pexels-photo-%s.jpeg?auto=compress&amp;cs=tinysrgb&amp;w=720&amp;h=480&amp;fit=crop'

# 업종별 장면 사진 — 대표 사진과 겹치지 않는 두 번째 사진 (Pexels, 설명문으로 고르고 시트로 확인)
SCENE = {
    'dental': (4269501, 'Dental practice', 'A dentist attending to a patient in a modern clinic'),
    'clinics': (7446684, 'Clinic', 'A dermatologist and a smiling patient looking at a tablet together'),
    'veterinary': (22504402, 'Veterinary clinic', 'A vet examining a dog while its owner holds it'),
    'senior-care': (18459198, 'Senior care', 'A caregiver bringing tea to residents in a sunlit lounge'),
    'academies': (7156103, 'Academy', 'A tutor working with two young students at a desk'),
    'universities': (7972304, 'University', 'A student holding admission papers outside a campus building'),
    'salons': (3992879, 'Salon', 'A stylist cutting a client’s hair in a contemporary salon'),
    'fitness': (37963576, 'Gym', 'A personal trainer guiding a client through an exercise'),
    'home-services': (34734504, 'Home services', 'A technician in uniform repairing a home appliance'),
    'pest-control': (4176550, 'Pest control', 'A technician in protective gear treating a room'),
    'property-management': (7642004, 'Property management', 'Keys being handed from one person to another'),
    'real-estate': (7937328, 'Real estate', 'An agent showing an empty apartment to a couple'),
    'auto-repair': (6870321, 'Auto repair', 'A mechanic on the phone beside a car in the workshop'),
    'movers': (7464687, 'Movers', 'Two movers carrying boxes through a bright new home'),
    'self-storage': (5759037, 'Self storage', 'A corridor of steel storage units'),
    'equipment-rental': (34100276, 'Equipment rental', 'Excavators lined up in a rental yard'),
    'restaurants': (28700799, 'Restaurant', 'A reserved sign on a set restaurant table'),
    'venues': (16985130, 'Wedding & event venue', 'A banquet hall set with round tables and flowers'),
    'stays': (7820689, 'Boutique stay', 'A hand pressing the bell at a hotel reception'),
    'golf': (38890586, 'Golf club', 'Two players riding a golf cart on a sunny course'),
    'legal': (8112153, 'Law firm', 'A lawyer going through documents with two clients'),
    'public-sector': (37568243, 'Public service', 'Two staff working at a public-service desk'),
    'funeral-homes': (7317893, 'Funeral home', 'A director comforting a family at a service'),
    'ecommerce': (7289733, 'Online store', 'An owner packing an order into a box'),
    'franchise': (8475204, 'Franchise', 'Two smiling store owners in aprons behind the counter'),
}
CUSTOMER = (9052866, 'A customer making a call from the sofa in the evening')
OWNER = (13736440, 'An owner in an apron reading the morning’s records on a tablet')


def img(pid, alt):
    return '<img src="%s" alt="%s" loading="lazy" decoding="async" width="720" height="480">' % (PH % (pid, pid), alt)


def strip(slug):
    pid, name, alt = SCENE[slug]
    return ('<div class="scenestrip reveal" aria-label="The three moments in every worked example">'
            '<figure>%s<figcaption><b>After hours — the call comes in</b>The customer calls when it suits them, not when your desk is open.</figcaption></figure>'
            '<figure>%s<figcaption><b>%s — answered from your own facts</b>Prices, hours and rules you approved. Nothing invented.</figcaption></figure>'
            '<figure>%s<figcaption><b>Next morning — what is waiting</b>A booking, a quote, a record with an owner and a deadline.</figcaption></figure>'
            '</div>' % (img(CUSTOMER[0], CUSTOMER[1]), img(pid, alt), name, img(OWNER[0], OWNER[1])))


def put(path, name, before_pat, html, after=False):
    """표식이 있으면 갈아 끼우고, 없으면 before_pat 앞(또는 뒤)에 넣는다."""
    s = io.open(path, encoding="utf-8").read()
    block = '<!--illus:%s-->%s<!--/illus:%s-->' % (name, html, name)
    marked = re.compile(r'<!--illus:%s-->.*?<!--/illus:%s-->' % (name, name), re.S)
    if marked.search(s):
        new = marked.sub(lambda m: block, s, count=1)
    else:
        m = re.search(before_pat, s)
        if not m:
            print("  !! anchor missing", path, name); return
        new = s[:m.end()] + '\n' + block + '\n' + s[m.end():] if after else s[:m.start()] + block + '\n    ' + s[m.start():]
    if new != s:
        io.open(path, "w", encoding="utf-8").write(new); print("  ok", path, name)


for slug in SCENE:
    p = 'en/industries/%s.html' % slug
    s = io.open(p, encoding="utf-8").read()
    sec = s.find('id="worked-examples"')
    if sec < 0: print("  !! no worked-examples", p); continue
    m = re.compile(r'<div class="panelset exset reveal"[^>]*>').search(s, sec)
    if not m: print("  !! no panelset", p); continue
    block = '<!--illus:scene-->%s<!--/illus:scene-->' % strip(slug)
    marked = re.compile(r'<!--illus:scene-->.*?<!--/illus:scene-->', re.S)
    new = marked.sub(lambda mm: block, s, count=1) if marked.search(s) else s[:m.start()] + block + '\n    ' + s[m.start():]
    if new != s: io.open(p, "w", encoding="utf-8").write(new); print("  ok", p, "scene")

wide = lambda svg, cap='': '<div class="illwide reveal">%s</div>' % illus.figure(svg, cap)

# get-started: the first week, in three steps
put('en/get-started.html', 'flow', r'\n\s*<div class="tline">',
    wide(illus.flow3('en'), 'What the week produces: your own words in, the AI answering on every channel, and a record of everything left behind.'))
# platform: the record the fourth box writes
put('en/platform.html', 'card', r'\n\s*<div class="stackrow reveal">',
    wide(illus.card('en'), 'The fourth part writes this: a record with the source of every field, an owner and a deadline. Sample data.'))
# industries: what a pack is — fields + pipeline
put('en/industries.html', 'pack', r'\n\s*<div class="packgrid reveal">',
    '<div class="illrow reveal">%s%s</div>' % (
        illus.figure(illus.card('en'), 'The fields a pack already has — filled from the call, with the source beside each one.'),
        illus.figure(illus.pipeline('en', stages=['Inquiry', 'Booked', 'Visited', 'Treatment plan', 'Recall']), 'The pipeline a pack moves a customer along — this one is dental.')))
# webchat: the one question it will not answer
put('en/webchat.html', 'handoff', r'\n\s*<div class="wrap">(?=[^\n]*\n[^\n]*one-question|)', '', after=True) if False else None
s = io.open('en/webchat.html', encoding="utf-8").read()
i = s.find('id="one-question"')
if i > 0:
    j = s.find('</section>', i)
    seg = s[i:j]
    if '<!--illus:handoff-->' not in seg:
        # 절의 첫 문단 뒤에 넣는다
        k = seg.find('</p>')
        if k > 0:
            seg2 = seg[:k + 4] + '\n' + '<!--illus:handoff-->%s<!--/illus:handoff-->' % wide(illus.handoff('en', question='Does my insurance cover the crown?'), 'The gate every answer passes: on the approved list it answers, otherwise a person gets the whole thread.') + seg[k + 4:]
            s = s[:i] + seg2 + s[j:]
            io.open('en/webchat.html', "w", encoding="utf-8").write(s); print("  ok en/webchat.html handoff")
print("done")
