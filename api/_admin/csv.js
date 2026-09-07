/* admin_export 결과를 CSV 로 바꾼다.
 *
 * 엑셀이 한글을 깨뜨리지 않으려면 UTF-8 BOM 이 맨 앞에 있어야 합니다.
 * 머리글은 한국어 이름 뒤에 (키) 를 붙입니다 — 사람은 이름을 읽고,
 * 프로그램은 괄호 안의 키로 다시 맞출 수 있습니다.
 *
 * 값은 RFC 4180 대로 씁니다: 쉼표·따옴표·줄바꿈이 들어 있으면 따옴표로
 * 감싸고 안의 따옴표는 두 번 씁니다. 배열·객체는 JSON 문자열로, 날짜는
 * DB 가 준 문자열 그대로(시간대 변환은 화면의 몫).
 */

const BOM = '\uFEFF';
const CRLF = '\r\n';
const NEEDS_QUOTE = /[",\r\n]/;
const FORMULA = /^(?:[=@\t\r]|[+-](?![0-9]))/;

export function csvCell(v) {
  if (v === null || v === undefined) return '';
  let s;
  if (typeof v === 'string') s = v;
  else if (typeof v === 'number' || typeof v === 'boolean' || typeof v === 'bigint') s = String(v);
  else {
    try {
      s = JSON.stringify(v);
    } catch (e) {
      s = String(v);
    }
  }
  /* 수식 주입. 회사명에 "=cmd|…" 같은 것을 적어 두면 엑셀이 열면서 실행할
     수 있습니다. =, @, 탭, 줄바꿈으로 시작하거나 +/- 뒤에 숫자가 아닌 것이
     오면(전화번호 "+82 10…" 은 그대로) 앞에 작은따옴표를 붙여 글자로 만듭니다. */
  if (FORMULA.test(s)) s = "'" + s;
  return NEEDS_QUOTE.test(s) ? '"' + s.replace(/"/g, '""') + '"' : s;
}

/* columns: [{key, ko, en}], rows: 객체 배열(키로 찾음) 또는 배열의 배열
   (열 순서대로). columns 가 비어 있고 첫 행이 객체면 그 키를 열로 씁니다. */
export function toCsv(columns, rows) {
  const list = Array.isArray(rows) ? rows : [];
  let cols = Array.isArray(columns)
    ? columns.filter((c) => c && typeof c === 'object' && typeof c.key === 'string' && c.key)
    : [];
  if (!cols.length && list.length && list[0] && typeof list[0] === 'object' && !Array.isArray(list[0])) {
    cols = Object.keys(list[0]).map((k) => ({ key: k, ko: k }));
  }
  const head = cols.map((c) => csvCell((c.ko || c.en || c.key) + ' (' + c.key + ')'));
  const out = [head.join(',')];
  for (const row of list) {
    if (Array.isArray(row)) {
      out.push(cols.map((c, i) => csvCell(row[i])).join(','));
    } else {
      const r = row && typeof row === 'object' ? row : {};
      out.push(cols.map((c) => csvCell(r[c.key])).join(','));
    }
  }
  return BOM + out.join(CRLF) + CRLF;
}

/* 파일 이름의 날짜는 운영자가 보는 시간(Asia/Seoul)으로. 서버의 UTC 로
   쓰면 밤에 내려받은 파일이 어제 날짜를 답니다. */
export function csvFilename(entity) {
  const ent = String(entity || '').replace(/[^a-z0-9_-]/gi, '').slice(0, 40) || 'export';
  const day = new Intl.DateTimeFormat('en-CA', {
    timeZone: 'Asia/Seoul',
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
  }).format(new Date());
  return ent + '-' + day + '.csv';
}
