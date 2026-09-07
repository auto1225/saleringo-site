/* 고객사 로그인으로 가는 문.
 *
 * 왜 이 화면이 따로 필요한가.
 *
 * 이 제품은 업체마다 자기 주소를 씁니다. 헤리티크 제주는
 * heritique.saleringo.com, 송정 새봄 한의원은 saebom.saleringo.com 입니다.
 * 로그인 화면도 그 주소 안에 있고, 거기서 업체 이름과 색이 나옵니다.
 * 그래서 "모두가 쓰는 로그인 주소" 라는 것이 없습니다.
 *
 * 그런데 판매 사이트에는 로그인 단추가 아예 없었습니다. 요금을 내고
 * 쓰시는 사장님이 이 사이트에 오면 들어갈 문이 없었다는 뜻입니다.
 * 주소를 외우고 계신 분만 들어갔습니다.
 *
 * 이 파일이 하는 일은 하나입니다. 사장님이 쓰시는 주소를 받아서 그
 * 주소의 로그인 화면으로 보내 드립니다. 비밀번호는 여기서 받지 않습니다 —
 * 그건 사장님 주소의 로그인 화면이 받습니다. 이 사이트는 비밀번호를
 * 만지지 않습니다.
 */
(function () {
  'use strict';

  var form = document.querySelector('[data-workspace-login]');
  if (!form) return;

  var KO = (document.documentElement.lang || 'ko').slice(0, 2) !== 'en';
  var BASE = 'saleringo.com';
  var KEY = 'sr_workspace';

  var T = KO
    ? {
        empty: '주소를 넣어 주세요. 개통 안내 메일에 적혀 있습니다.',
        bad: '주소에 쓸 수 없는 글자가 있습니다. 영문 소문자·숫자·붙임표(-)만 됩니다.',
        going: '여는 중…'
      }
    : {
        empty: 'Enter your address. It is in your welcome email.',
        bad: 'That address has characters it cannot have — lowercase letters, digits and hyphens only.',
        going: 'Opening…'
      };

  var input = form.querySelector('[data-ws-input]');
  var out = form.querySelector('[data-ws-preview]');
  var err = form.querySelector('[data-ws-error]');
  var go = form.querySelector('[data-ws-go]');

  /* 사장님은 주소를 여러 모양으로 적으십니다. 주소창에서 통째로 복사해
     오시기도 하고("https://saebom.saleringo.com/login"), 이름만 적기도
     하십니다("saebom"). 어느 쪽이든 같은 곳으로 가야 합니다. */
  function normalize(raw) {
    var v = String(raw == null ? '' : raw).trim().toLowerCase();
    v = v.replace(/^https?:\/\//, '').replace(/^www\./, '');
    v = v.split('/')[0].split('?')[0].split('#')[0];
    v = v.replace(/\.$/, '');
    if (v === BASE) return { kind: 'apex' };
    if (v.slice(-(BASE.length + 1)) === '.' + BASE) {
      v = v.slice(0, -(BASE.length + 1));
    } else if (v.indexOf('.') > 0) {
      /* 자기 도메인을 쓰시는 업체(방식 B). 그대로 그 도메인으로 보냅니다. */
      return /^[a-z0-9][a-z0-9.-]{1,60}[a-z0-9]$/.test(v)
        ? { kind: 'domain', host: v }
        : { kind: 'bad' };
    }
    if (!v) return { kind: 'empty' };
    if (!/^[a-z0-9](?:[a-z0-9-]{0,30}[a-z0-9])?$/.test(v)) return { kind: 'bad' };
    return { kind: 'sub', sub: v, host: v + '.' + BASE };
  }

  function preview() {
    if (!out) return;
    var r = normalize(input.value);
    if (r.kind === 'sub' || r.kind === 'domain') {
      out.textContent = r.host + '/login';
      out.hidden = false;
    } else {
      out.hidden = true;
    }
    if (err) err.textContent = '';
  }

  /* 지난번에 쓰신 주소를 기억해 둡니다. 매번 적게 하면 결국 아무도 안 씁니다.
     저장소가 막혀 있어도 화면은 그대로 돌아가야 합니다. */
  try {
    var saved = window.localStorage.getItem(KEY);
    if (saved && !input.value) { input.value = saved; }
  } catch (e) { /* 저장소가 막힌 브라우저 */ }
  preview();

  input.addEventListener('input', preview);

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var r = normalize(input.value);
    if (r.kind === 'empty' || r.kind === 'apex') {
      if (err) err.textContent = T.empty;
      input.focus();
      return;
    }
    if (r.kind === 'bad') {
      if (err) err.textContent = T.bad;
      input.focus();
      input.select();
      return;
    }
    try { window.localStorage.setItem(KEY, r.sub || r.host); } catch (e2) { /* 무시 */ }
    if (go) { go.disabled = true; go.textContent = T.going; }
    window.location.href = 'https://' + r.host + '/login';
  });
})();
