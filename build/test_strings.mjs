// 화면에 나가는 문장이 실제로 어떤 문장이 되는지 본다.
//
// 라이브에 "창립 고객 할인 적용 — 처음 50개월 3% 할인" 이 나가 있었습니다.
// 한국어는 "처음 3개월 50%", 영어는 "50% off for your first 3 months" 로
// 숫자 어순이 반대인데, 자리를 순서대로 채우고 있었습니다. 영어는 맞고
// 한국어만 뒤집혔습니다. 코드에는 오류가 없었고 검사도 통과했습니다.
// 문장을 실제로 만들어 보지 않으면 잡히지 않는 종류입니다.
//
// 같은 화면에 "(6/31일)" 도 있었습니다. 6월 31일은 없는 날짜입니다.
// 뜻은 "31일 가운데 6일" 이었습니다.
//
//     node build/test_strings.mjs
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const ROOT = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const src = fs.readFileSync(path.join(ROOT, 'assets/js/checkout.js'), 'utf8');

// 문구는 한 줄에 하나씩 있습니다. 필요한 것만 이름으로 뽑습니다.
// 파일 전체를 실행하지 않으므로 브라우저도 DOM 도 필요 없습니다.
function grab(lang, key) {
  const a = src.indexOf(`    ${lang}: {`);
  if (a < 0) throw new Error(`${lang} 블록을 못 찾음`);
  const b = src.indexOf('\n    },', a);
  const block = src.slice(a, b);
  const m = block.match(new RegExp(`^\\s{6}${key}:\\s*(.+?),?\\s*$`, 'm'));
  if (!m) throw new Error(`${lang}.${key} 를 못 찾음`);
  // '…' + '…' 로 이어 붙인 문구를 하나로 만듭니다.
  const parts = [...m[1].matchAll(/'((?:[^'\\]|\\.)*)'/g)].map((x) =>
    x[1].replace(/\\'/g, "'").replace(/\\\\/g, '\\'));
  if (!parts.length) throw new Error(`${lang}.${key} 가 문자열이 아님`);
  return parts.join('');
}

// checkout.js 의 fill() 과 같은 규칙입니다.
function fill(tpl, vals) {
  return String(tpl).replace(/\{(\w+)\}/g, (m, k) =>
    Object.prototype.hasOwnProperty.call(vals, k) ? String(vals[k]) : m);
}

const CASES = [
  {
    key: 'discount',
    vals: {
      ko: { name: '창립 고객 할인', percent: 50, months: 3, after: '374,000원' },
      en: { name: 'Founding discount', percent: 50, months: 3, after: '$273.90' },
    },
    want: {
      ko: [/3개월/, /50\s?%/],
      en: [/50\s?%/, /first 3 months/],
    },
    reject: { ko: [/50개월/, /3\s?%/], en: [/first 50 months/] },
  },
  {
    key: 'firstIf',
    vals: {
      ko: { amount: '36,193원', left: 6, total: 31 },
      en: { amount: '$36.19', left: 6, total: 31 },
    },
    want: { ko: [/31일/, /6일/], en: [/\b6\b/, /\b31\b/] },
    // 6/31 은 6월 31일로 읽힙니다. 그런 날짜는 없습니다.
    reject: { ko: [/\b6\s?\/\s?31\b/], en: [/\b6\s?\/\s?31\b/] },
  },
  {
    key: 'overage',
    vals: {
      ko: { included: '2,000', rate: '90원' },
      en: { included: '2,000', rate: '$0.08' },
    },
    want: { ko: [/2,000건/, /90원/], en: [/2,000 conversations/, /\$0\.08/] },
    reject: { ko: [/90건/], en: [] },
  },
];

let bad = 0;
for (const c of CASES) {
  for (const lang of ['ko', 'en']) {
    const tpl = grab(lang, c.key);
    const out = fill(tpl, c.vals[lang]);
    const problems = [];

    if (/\{\w+\}/.test(out)) problems.push('채워지지 않은 자리가 남음');
    if (/%[sd]/.test(tpl)) problems.push('순서로 채우는 옛 자리표시자 — 어순이 다른 언어에서 뒤집힙니다');
    for (const re of c.want[lang] || []) {
      if (!re.test(out)) problems.push(`${re} 가 문장에 없음`);
    }
    for (const re of (c.reject[lang] || [])) {
      if (re.test(out)) problems.push(`${re} 가 문장에 있음 — 숫자가 자리를 바꿨습니다`);
    }

    if (problems.length) bad++;
    console.log(`${problems.length ? '!!' : '  '} ${lang} ${c.key.padEnd(9)} ${out}`);
    for (const p of problems) console.log(`      → ${p}`);
  }
}

console.log(`문장 ${CASES.length * 2}건 검사 완료.`);

// ── 전화번호 자동 하이픈 ────────────────────────────────────────────────
// 예전에는 숫자를 11자리로 잘라 3-4-4 로 밀어붙였습니다. 그래서
// 0507-1234-5678 이 050-7123-4567 이 되었습니다. 마지막 자리가 사라지고
// 앞자리가 한 칸씩 밀렸는데, 친 사람은 알아채기 어렵습니다. 접수된 번호로
// 전화를 걸면 다른 사람이 받습니다.
{
  const a = src.indexOf('function fmtPhone(v) {');
  const b = src.indexOf(String.fromCharCode(10) + '  function ', a + 10);
  const body = src.slice(a, b);
  // 함수 하나만 떼어 냅니다. 파일 전체를 실행하지 않으므로 DOM 이 필요 없습니다.
  const fmtPhone = new Function('return (' + body.replace(/^function/, 'function') + ')')();

  const CASES = [
    // [친 것,                기대,                  왜]
    ['01012345678',      '010-1234-5678', '휴대폰'],
    ['0212345678',       '02-1234-5678',  '서울 지역번호는 두 자리'],
    ['0311234567',       '031-123-4567',  '그 밖의 지역번호는 세 자리'],
    ['050712345678',     '0507-1234-5678', '안심번호는 열두 자리'],
    ['05051234567',      '0505-123-4567',  '같은 0505 라도 열한 자리가 있다'],
    ['030312345678',     '0303-1234-5678', '인터넷전화'],
    ['15881234',         '1588-1234',      '대표번호는 여덟 자리'],
    ['+82 10-1234-5678', '+82 10-1234-5678', '국제 표기는 손대지 않는다'],
    ['+1 415 555 0100',  '+1 415 555 0100',  '해외 번호도 그대로'],
  ];

  for (const [input, want, why] of CASES) {
    const got = fmtPhone(input);
    const bad2 = got !== want;
    if (bad2) bad++;
    console.log(`${bad2 ? '!!' : '  '} phone     ${input.padEnd(18)} → ${got.padEnd(18)} (${why})`);
    if (bad2) console.log(`      → ${want} 이어야 합니다`);
  }
}

console.log();
if (bad) {
  console.log(`전화번호 또는 문장 ${bad}건이 틀립니다.`);
  process.exit(1);
}
console.log('전화번호도 친 그대로 남습니다.');

