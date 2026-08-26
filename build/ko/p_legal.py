# -*- coding: utf-8 -*-
"""개인정보처리방침 · 이용약관 · 보안.

These are not translations. The English versions answer to GDPR, to the FCA
and to the FTC; none of those govern a Korean 사업자, and a Korean owner
reading "your GDPR rights" learns nothing about their own obligations.

So these three are written to the law that actually applies:

  · 개인정보 보호법 - the 처리방침 must state 목적, 항목, 보유기간, 위탁,
    제3자 제공, 국외이전, 파기, 안전성 확보조치, and name a 개인정보
    보호책임자. All of those are here, including the uncomfortable one:
    the model that generates the reply runs outside Korea, so 국외이전 is
    disclosed rather than buried.
  · 통신비밀보호법 - recording a call is lawful for a party to it, but the
    caller is told at the start regardless, because that is what a business
    would want its own customers to be told.
  · 정보통신망법 - marketing messages need separate consent, so consent to
    be answered is not treated as consent to be marketed to.

The honesty that the English pages carry carries over: these are written by
the company, and legal review is stated as pending rather than implied to
have happened.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
os.chdir(os.path.dirname(os.path.dirname(HERE)))
from shell import page, NAV, FOOT

NB = '&nbsp;'
UPDATED = '2026년 8월 24일'

CSS = """
  .hero{display:block;padding:150px 0 56px;}
  .doc{max-width:none;}
  /* Clause blocks are separated by a rule with real space on both sides of
     it. The first version had them share an edge - padding inside, border on
     top - which reads as one continuous slab and, more practically, means two
     boxes literally touching, which is the shape a layout fault takes. */
  .docsec{padding-bottom:34px;margin-bottom:34px;border-bottom:1px solid #E3E7EE;}
  .docsec:last-child{padding-bottom:0;margin-bottom:0;border-bottom:0;}
  .docsec h2{font-size:var(--fs-h2s);color:var(--l-ink);letter-spacing:-.02em;}
  .docsec h3{margin-top:26px;font-size:var(--fs-lead);color:var(--l-ink);}
  .docsec p{margin-top:14px;font-size:var(--fs-body);line-height:1.85;color:var(--l-tx2);}
  .docsec ul{margin-top:16px;display:grid;gap:12px;}
  .docsec li{list-style:none;padding-left:24px;position:relative;
    font-size:var(--fs-body);line-height:1.8;color:var(--l-tx2);}
  .docsec li::before{content:"";position:absolute;left:2px;top:.72em;width:8px;height:8px;
    border-radius:50%;border:1.5px solid var(--teal);}
  .docsec li b,.docsec p b{color:var(--l-ink);}
  .dtable{width:100%;margin-top:20px;border-collapse:collapse;}
  .dtable th,.dtable td{padding:14px 12px;text-align:left;font-size:var(--fs-sm);
    line-height:1.7;border-bottom:1px solid #E3E7EE;vertical-align:top;color:var(--l-tx2);}
  .dtable th{color:var(--l-ink);font-weight:600;}
  .dtwrap{overflow-x:auto;}
  @media (max-width:700px){.dtable{min-width:600px;}}
  /* The admissions - no certification yet, no legal review yet - are not
     warnings in a yellow box. Putting them in one says "this is the bit you
     may skip". They are part of the argument, so they are set as prose, and
     the only mark they carry is that the sentence that admits it is bold. */
  .caution{margin-top:22px;}
  .caution b{display:block;color:var(--l-ink);font-size:var(--fs-body);}
  .caution p{margin-top:10px;}
  .updated{margin-top:18px;font-size:var(--fs-sm);color:rgba(255,255,255,.6);}
"""


def doc(slug, kicker, h1, sub, sections, title, desc, crumb):
    body = ['<header class="hero nophoto sec-dark bg-aurora">',
            '  <div class="scrim" aria-hidden="true"></div>',
            '  ' + NAV,
            '  <div class="wrap hero-inner">',
            '    <span class="eyebrow"><i></i>%s</span>' % kicker,
            '    <h1 style="margin-top:24px;">%s</h1>' % h1,
            '    <p class="sub">%s</p>' % sub,
            '    <p class="updated">최종 개정일 %s</p>' % UPDATED,
            '  </div>',
            '</header>', '', '<main>', '',
            '<section class="t-md sec-light bg-paper"><div class="wrap doc">']
    for h, inner in sections:
        body.append('<div class="docsec reveal"><h2>%s</h2>%s</div>' % (h, inner))
    body += ['</div></section>', '', FOOT, '</main>']
    page(slug, title, desc, '\n'.join(body), css=CSS, grade='trust',
         crumbs=[('홈', 'index.html'), (crumb, slug)])


# ── 개인정보처리방침 ────────────────────────────────────────────────────────
PRIVACY = [
('1. 이 방침이 다루는 것',
 '<p>정직한마케팅 주식회사(이하 &ldquo;회사&rdquo;)는 Saleringo 서비스를 제공하면서 두 가지 종류의 '
 '개인정보를 다룹니다. 하나는 <b>서비스를 이용하는 사업자</b>의 정보이고, 다른 하나는 그 사업자에게 '
 '<b>연락한 고객</b>의 정보입니다.</p>'
 '<p>두 번째 정보에서 회사는 <b>수탁자</b>입니다. 즉 그 정보의 개인정보처리자는 서비스를 이용하는 '
 '사업자이고, 회사는 그 사업자의 지시에 따라 처리할 뿐입니다. 걸려 온 전화의 주인은 회사가 아니라 '
 '그 가게입니다. 이 구분이 이 문서 전체의 전제입니다.</p>'),

('2. 수집하는 항목과 목적',
 '<div class="dtwrap"><table class="dtable">'
 '<thead><tr><th>구분</th><th>항목</th><th>목적</th><th>보유기간</th></tr></thead><tbody>'
 '<tr><td>서비스 이용 사업자</td><td>상호, 사업자등록번호, 담당자 성명 · 이메일 · 연락처, 결제 정보</td>'
 '<td>계약 체결과 이행, 요금 청구, 세금계산서 발행, 고객 지원</td>'
 '<td>계약 종료 후 5년(전자상거래법상 거래기록)</td></tr>'
 '<tr><td>도입 문의</td><td>이메일, 상호, 연락처, 업종, 문의 내용</td>'
 '<td>문의 응대와 견적 안내</td><td>문의일로부터 1년, 또는 삭제 요청 시 즉시</td></tr>'
 '<tr><td>사업자의 고객(수탁 처리)</td><td>성명, 연락처, 문의 내용, 통화 녹음과 전사 기록, 예약 정보</td>'
 '<td>사업자를 대신한 문의 응대와 예약 처리</td><td>사업자가 정한 기간, 미지정 시 24개월</td></tr>'
 '<tr><td>자동 수집</td><td>접속 IP, 브라우저 정보, 방문 기록</td>'
 '<td>서비스 안정성 확보와 부정 이용 방지</td><td>3개월</td></tr>'
 '</tbody></table></div>'
 '<p>주민등록번호는 수집하지 않습니다. 건강정보 같은 민감정보도 서비스 이용 사업자가 '
 '직접 입력하지 않는 한 회사가 따로 수집하지 않습니다. '
 '다만 고객이 통화 중에 스스로 말한 내용은 녹음에 남을 수 있습니다. '
 '그 부분은 아래 3항에서 따로 다룹니다.</p>'),

('3. 통화 녹음에 관하여',
 '<p>AI 전화 응대는 통화를 녹음하고 전사합니다. 무엇을 어떻게 답했는지 확인할 수 없는 자동 응대는 '
 '쓸 수 없다고 보기 때문입니다.</p>'
 '<ul>'
 '<li><b>통화 시작 시 안내합니다.</b> 걸어 온 분에게 녹음된다는 사실을 먼저 알립니다. '
 '「통신비밀보호법」상 대화의 당사자가 하는 녹음은 적법하지만, 그것과 별개로 알리는 것이 맞다고 봅니다.</li>'
 '<li><b>원치 않으면 녹음 없이 진행할 수 있습니다.</b> 사업자 설정에서 녹음을 끄고 요약만 남길 수 있습니다.</li>'
 '<li><b>녹음 파일은 사업자의 것입니다.</b> 언제든 내려받을 수 있고, 삭제를 요청하면 삭제합니다.</li>'
 '<li><b>회사 직원이 임의로 듣지 않습니다.</b> 장애 조사 등 필요한 경우에 한해, 접근 기록을 남기고 '
 '최소한의 범위에서만 접근합니다.</li>'
 '</ul>'),

('4. 처리 위탁과 국외 이전',
 '<p>서비스 제공을 위해 아래 업체에 개인정보 처리를 위탁하고 있으며, 일부는 국외에 있습니다. '
 '이 부분을 흐리게 적는 것이 흔하지만, 그러면 사업자가 자신의 처리방침을 제대로 쓸 수 없습니다.</p>'
 '<div class="dtwrap"><table class="dtable">'
 '<thead><tr><th>수탁업체</th><th>위탁 업무</th><th>이전되는 항목</th><th>보관 국가</th></tr></thead><tbody>'
 '<tr><td>Anthropic, PBC</td><td>응대 문장 생성</td><td>대화 내용(연락처 등 식별정보는 가림 처리 후 전송)</td><td>미국</td></tr>'
 '<tr><td>Vercel, Inc.</td><td>웹 서비스 호스팅</td><td>접속 기록</td><td>미국 · 대한민국</td></tr>'
 '<tr><td>결제대행사</td><td>카드 결제와 정기 결제</td><td>결제 수단 정보</td><td>대한민국</td></tr>'
 '<tr><td>통신사업자</td><td>전화 회선과 문자 발송</td><td>발신 · 수신 번호, 통화 시각</td><td>대한민국</td></tr>'
 '</tbody></table></div>'
 '<p>국외 이전에 동의하지 않으실 경우 해당 기능(AI 응대 생성)을 제공할 수 없으며, 이는 서비스의 '
 '핵심 기능이므로 사실상 이용이 어렵습니다. 그 점을 계약 전에 먼저 말씀드립니다.</p>'
 '<p><b>학습에 사용하지 않습니다.</b> 사업자의 데이터와 그 고객의 대화 내용을 회사나 수탁업체의 '
 '모델 학습에 사용하지 않으며, 이는 계약서에 명시합니다.</p>'),

('5. 제3자 제공',
 '<p>회사는 개인정보를 제3자에게 제공하지 않습니다. 판매하지 않고, 광고 목적으로 넘기지 않습니다. '
 '다만 다음의 경우는 예외입니다.</p>'
 '<ul>'
 '<li>정보주체가 별도로 동의한 경우</li>'
 '<li>법령에 근거하여 수사기관이 적법한 절차로 요구하는 경우. 이 경우 법이 금지하지 않는 한 '
 '해당 사업자에게 그 사실을 알립니다.</li>'
 '</ul>'),

('6. 정보주체의 권리',
 '<p>「개인정보 보호법」 제35조 내지 제37조에 따라 열람, 정정 · 삭제, 처리정지를 요구하실 수 있습니다. '
 '아래 이메일로 요청하시면 <b>10일 이내</b>에 처리하고 결과를 알려 드립니다.</p>'
 '<ul>'
 '<li><b>사업자의 고객이신 경우</b>, 요청은 원칙적으로 그 사업자(가게)에게 하셔야 합니다. '
 '회사는 수탁자이므로 사업자의 지시 없이 임의로 삭제하거나 열람시켜 드릴 수 없습니다. '
 '다만 어느 사업자에게 연락해야 하는지는 안내해 드립니다.</li>'
 '<li><b>서비스 이용 사업자이신 경우</b>, 계정 화면에서 직접 전체 내보내기와 삭제가 가능합니다.</li>'
 '</ul>'
 '<p>또한 「개인정보 보호법」 제37조의2에 따라, 사람의 개입 없이 내려진 결정은 '
 '설명을 요구하거나 거부하실 수 있습니다. '
 'Saleringo의 응대는 예약을 잡고 안내하는 데에 그칩니다. '
 '권리나 의무에 중대한 영향을 미치는 결정은 하지 않도록 만들어 두었습니다. '
 '그래도 설명을 요구하시면 그 응대의 근거를 그대로 보여 드립니다.</p>'),

('7. 파기',
 '<p>보유기간이 지나거나 처리 목적이 달성되면 지체 없이 파기합니다. 전자적 파일은 복구할 수 없는 '
 '방법으로 삭제하고, 출력물이 있는 경우 분쇄합니다. 백업본은 최대 30일 이내에 순차적으로 '
 '덮어쓰기 됩니다.</p>'),

('8. 안전성 확보 조치',
 '<ul>'
 '<li>전송 구간 암호화(TLS 1.2 이상)와 저장 시 암호화</li>'
 '<li>업무 담당자 최소화와 접근권한 분리, 접근 기록 보관</li>'
 '<li>관리자 계정 다중 인증</li>'
 '<li>침입 차단과 접속 기록 위 · 변조 방지</li>'
 '<li>개인정보 취급자 대상 정기 교육</li>'
 '</ul>'
 '<div class="caution"><b>아직 하지 않은 것도 적어 둡니다.</b>'
 '<p>회사는 현재 ISMS-P 인증이나 ISO 27001 인증을 보유하고 있지 않습니다. 신생 회사이기 때문입니다. '
 '인증이 없다는 사실을 밝히지 않고 &ldquo;국제 표준에 준하는 보안&rdquo;이라고만 적는 것은 '
 '거짓말에 가깝다고 봅니다. 인증을 취득하면 이 문단을 취득 사실로 바꾸겠습니다. '
 '그때까지는 무엇을 하고 있는지를 위 목록으로 판단해 주십시오.</p></div>'),

('9. 개인정보 보호책임자와 문의',
 '<p>개인정보 처리에 관한 문의, 불만, 피해구제는 아래로 연락해 주십시오. 사람이 답합니다.</p>'
 '<ul>'
 '<li><b>개인정보 보호책임자</b> &mdash; 정직한마케팅 주식회사 대표</li>'
 '<li><b>이메일</b> &mdash; hello@saleringo.com</li>'
 '<li><b>전화</b> &mdash; +82 70-5277-0820</li>'
 '</ul>'
 '<p>회사의 처리에 만족하지 못하실 경우 아래 기관에 도움을 요청하실 수 있습니다.</p>'
 '<ul>'
 '<li>개인정보분쟁조정위원회 (국번 없이 1833-6972)</li>'
 '<li>개인정보침해 신고센터 (국번 없이 118)</li>'
 '<li>대검찰청 사이버수사과 (국번 없이 1301) · 경찰청 사이버수사국 (국번 없이 182)</li>'
 '</ul>'),

('10. 개정',
 '<p>이 방침을 변경할 때에는 시행 <b>30일 전</b>에 서비스 화면과 이메일로 알려 드립니다. '
 '이용자에게 불리한 변경은 소급하지 않으며, 변경 전에 발생한 일에는 변경 전 방침이 적용됩니다. '
 '중대한 변경에 동의하지 않으시면 위약금 없이 해지하실 수 있습니다.</p>'),
]

# ── 이용약관 ──────────────────────────────────────────────────────────────
TERMS = [
('제1조 (목적과 적용)',
 '<p>이 약관은 정직한마케팅 주식회사(이하 &ldquo;회사&rdquo;)가 제공하는 Saleringo 서비스의 이용에 '
 '관한 회사와 이용자 사이의 권리 · 의무를 정합니다. 이 서비스는 사업자를 대상으로 하며, '
 '「약관의 규제에 관한 법률」에 따라 이 약관 중 이용자에게 부당하게 불리한 조항은 효력이 없습니다.</p>'
 '<div class="caution"><b>이 약관을 읽기 전에 먼저 밝힙니다.</b>'
 '<p>이 약관은 현재 회사가 직접 작성한 것이며, 법률 전문가의 검토를 마치지 않았습니다. '
 '검토를 마치는 대로 개정하고 그 사실을 이 자리에 적겠습니다. '
 '검토 여부를 밝히지 않은 채 완성된 문서처럼 보이게 하는 것보다, 지금 상태를 말씀드리는 편이 '
 '낫다고 판단했습니다. 계약 전에 사업자께서 직접 검토하시기를 권해 드립니다.</p></div>'),

('제2조 (서비스의 내용)',
 '<p>회사는 이용자를 대신하여 전화, 웹사이트 채팅, 메신저로 들어오는 문의에 응답하고, '
 '그 내용을 고객관리 시스템에 기록합니다. 무엇까지 답할지는 이용자가 '
 '등록한 요금표와 영업시간, 그리고 금지 사항이 정합니다.</p>'
 '<p>회사는 이용자가 등록하지 않은 정보를 근거로 응답하지 않도록 서비스를 설계합니다. '
 '다만 인공지능의 특성상 오류가 완전히 없을 수는 없고, 그 책임 범위는 제7조에서 정합니다.</p>'),

('제3조 (계약의 체결)',
 '<p>이용계약은 이용자가 신청하고 회사가 승낙함으로써 성립합니다. 회사는 다음의 경우 승낙을 '
 '거절하거나 계약을 해지할 수 있습니다.</p>'
 '<ul>'
 '<li>법령에 위반되는 목적으로 서비스를 이용하려는 경우</li>'
 '<li>타인을 기망하거나 사람인 것처럼 가장하도록 요구하는 경우</li>'
 '<li>수신자의 동의 없는 광고성 정보 발송에 이용하려는 경우</li>'
 '<li>사실과 다른 정보를 등록하여 고객에게 잘못된 안내가 나가도록 하는 경우</li>'
 '</ul>'),

('제4조 (요금과 결제)',
 '<ul>'
 '<li>요금은 요금 페이지에 게시된 금액에 따르며, 게시된 금액은 <b>부가가치세 별도</b>입니다.</li>'
 '<li>월 정액 요금은 선불, 통화료 등 사용량 기반 요금은 사용한 달의 다음 달에 후불로 청구합니다.</li>'
 '<li>회사는 전자세금계산서를 발행합니다.</li>'
 '<li>요금을 인상할 경우 시행 30일 전에 알리며, 인상에 동의하지 않으면 해지할 수 있습니다. '
 '이미 결제한 기간에는 인상 전 요금이 적용됩니다.</li>'
 '<li>이용자는 월 사용 한도를 설정할 수 있으며, 한도에 도달하면 회사는 추가 사용을 정지하고 '
 '이를 알립니다.</li>'
 '</ul>'),

('제5조 (해지와 환불)',
 '<ul>'
 '<li>이용자는 언제든지 해지할 수 있으며, 위약금이 없습니다.</li>'
 '<li>월 정액 요금은 해지 신청일부터 그 달 남은 날수만큼 <b>날짜로 계산해 환불</b>합니다. '
 '이미 사용한 통화료 등 사용량 요금은 환불 대상이 아닙니다.</li>'
 '<li>회사의 귀책으로 서비스를 이용하지 못한 시간에 대해서는 해당 기간의 요금을 환불하거나 '
 '다음 달 요금에서 차감합니다.</li>'
 '<li>해지 시 회사는 이용자의 전체 데이터를 내려받을 수 있는 파일로 제공하며, '
 '수령 후 회사 보유분을 파기합니다.</li>'
 '</ul>'),

('제6조 (이용자의 의무)',
 '<ul>'
 '<li>이용자는 등록하는 요금, 영업시간, 서비스 내용이 사실과 일치하도록 관리하여야 합니다. '
 '잘못 등록된 정보 때문에 고객에게 틀린 안내가 나간 경우, 그 책임은 이용자에게 있습니다.</li>'
 '<li>이용자는 자신의 고객에 대한 개인정보처리자로서의 의무를 부담합니다. 회사는 수탁자로서 '
 '이용자의 지시 범위 안에서만 처리합니다.</li>'
 '<li>이용자는 「정보통신망법」에 따른 광고성 정보 전송 규정을 준수하여야 하며, 회사의 서비스를 '
 '수신 동의 없는 광고 발송에 사용하여서는 안 됩니다.</li>'
 '</ul>'),

('제7조 (책임의 범위)',
 '<p>회사는 서비스가 정상적으로 동작하도록 상당한 주의를 다합니다. 그럼에도 인공지능이 생성한 '
 '응답에 오류가 있을 수 있으며, 이에 대한 회사의 책임은 다음과 같이 정합니다.</p>'
 '<ul>'
 '<li>회사의 고의 또는 중대한 과실로 인한 손해에 대해서는 법이 정하는 바에 따라 배상합니다. '
 '이 부분은 어떤 경우에도 배제하지 않습니다.</li>'
 '<li>그 밖의 손해에 대한 회사의 배상 책임은 <b>해당 사고가 발생한 달로부터 직전 3개월간 '
 '이용자가 회사에 지급한 요금의 합계</b>를 한도로 합니다.</li>'
 '<li>회사는 이용자가 등록한 정보 자체의 오류, 이용자의 고객이 제공한 정보의 허위, '
 '천재지변 및 통신사업자의 장애로 인한 손해에 대해서는 책임지지 않습니다.</li>'
 '</ul>'
 '<p>회사는 서비스 가동률에 관한 별도의 보장(SLA)을 아직 제공하지 않습니다. '
 '제공하지 않는 것을 제공하는 것처럼 적지 않기 위해 명시합니다.</p>'),

('제8조 (지식재산과 데이터)',
 '<p>이용자가 등록한 자료와 서비스 이용 과정에서 생성된 기록(고객 정보, 통화 녹음, 상담 내역)의 '
 '권리는 <b>이용자에게 있습니다.</b> 회사는 서비스 제공에 필요한 범위에서만 이를 처리하며, '
 '모델 학습에 사용하지 않습니다.</p>'
 '<p>회사가 제공하는 소프트웨어와 화면 구성, 문서에 관한 권리는 회사에 있습니다.</p>'),

('제9조 (약관의 변경)',
 '<p>회사는 이 약관을 변경할 수 있으며, 변경 시 시행일 <b>30일 전</b>에 서비스 화면과 이메일로 '
 '알립니다. 이용자에게 불리한 변경에 동의하지 않는 경우 시행일 전까지 해지할 수 있으며, '
 '변경된 약관은 소급하여 적용되지 않습니다.</p>'),

('제10조 (준거법과 관할)',
 '<p>이 약관과 서비스 이용에는 <b>대한민국 법</b>이 적용됩니다. 분쟁이 발생한 경우 '
 '「민사소송법」에 따른 관할 법원에 제기합니다. 회사는 이용자에게 불리한 전속관할 조항을 두지 '
 '않습니다.</p>'
 '<p>소송 이전에, 먼저 hello@saleringo.com 으로 연락 주시기를 부탁드립니다. '
 '대부분의 문제는 그 편이 빠릅니다.</p>'),
]

# ── 보안 ──────────────────────────────────────────────────────────────────
SECURITY = [
('무엇을 지켜야 하는가',
 '<p>Saleringo가 다루는 것은 사업자의 매출 자료와, 그 사업자에게 연락한 사람들의 개인정보입니다. '
 '치과라면 누가 어떤 치료를 물었는지가 남고, 요양기관이라면 어느 가족이 어떤 상황인지가 남습니다. '
 '이것은 유출되면 사과로 끝나지 않는 종류의 자료입니다.</p>'
 '<p>그래서 이 페이지는 &ldquo;안전합니다&rdquo;라고 쓰는 대신, 실제로 무엇을 하고 있고 '
 '무엇을 아직 하지 않았는지를 그대로 적습니다.</p>'),

('하고 있는 것',
 '<ul>'
 '<li><b>전송 구간 암호화</b> &mdash; 브라우저와 서버, 서버와 수탁업체 사이 통신에 TLS 1.2 이상을 사용합니다.</li>'
 '<li><b>저장 시 암호화</b> &mdash; 데이터베이스와 녹음 파일 저장소를 암호화합니다.</li>'
 '<li><b>사업자 간 데이터 분리</b> &mdash; 모든 조회에 사업자 식별자가 강제로 붙습니다. '
 '다른 가게의 자료가 조회되는 경로 자체를 만들지 않습니다.</li>'
 '<li><b>접근 최소화와 기록</b> &mdash; 회사 직원이 사업자 데이터에 접근하려면 사유를 남겨야 하고, '
 '접근 기록이 보관됩니다. 이 기록은 요청하시면 보여 드립니다.</li>'
 '<li><b>관리자 계정 다중 인증</b> &mdash; 회사 내부 관리 도구는 비밀번호만으로 접속할 수 없습니다.</li>'
 '<li><b>학습 목적 사용 금지</b> &mdash; 계약서에 명시합니다. 수탁업체와의 계약에도 같은 조건을 겁니다.</li>'
 '<li><b>전체 내보내기</b> &mdash; 언제든 전부 내려받을 수 있습니다. 나가는 길을 막지 않는 것도 보안입니다.</li>'
 '</ul>'),

('아직 하지 않은 것',
 '<div class="caution"><b>인증을 보유하고 있지 않습니다.</b>'
 '<p>ISMS-P, ISO 27001, SOC 2 중 어느 것도 아직 없습니다. 회사가 신생이고, 인증은 '
 '운영 이력이 쌓여야 받을 수 있기 때문입니다. 진행 상황이 생기면 이 자리에 날짜와 함께 적겠습니다.</p>'
 '<p>지금 시점에서 사업자께서 하실 수 있는 확인은 세 가지라고 봅니다. '
 '첫째, 위 목록의 항목을 계약서에 넣어 달라고 요구하십시오. 저희는 넣어 드립니다. '
 '둘째, 접근 기록을 실제로 보여 달라고 하십시오. 보여 드립니다. '
 '셋째, 전체 내보내기를 계약 초기에 한 번 실행해 보십시오. 나갈 수 있는지를 미리 확인해 두는 것이 '
 '가장 확실한 검증입니다.</p></div>'
 '<p>가동률 보장(SLA)도 아직 제공하지 않습니다. 제공할 수 있게 되면 수치와 함께 공개하겠습니다.</p>'),

('사고가 났을 때',
 '<p>개인정보 유출이 확인되면 「개인정보 보호법」 제34조에 따라 <b>72시간 이내</b>에 '
 '해당 사업자에게 알립니다. '
 '법령이 정한 경우에는 개인정보보호위원회 또는 한국인터넷진흥원에도 신고합니다.</p>'
 '<p>통지에는 무엇이 언제 유출되었는지, 원인이 무엇인지, 어떤 조치를 했는지를 아는 범위에서 '
 '그대로 적습니다. 조사 중이라 모르는 부분은 모른다고 적고, 알게 되는 대로 추가로 알립니다.</p>'),

('취약점을 발견하셨다면',
 '<p>hello@saleringo.com 으로 알려 주십시오. 영업일 기준 <b>2일 이내</b>에 사람이 회신합니다. '
 '선의로 신고해 주신 분께 법적 조치를 취하지 않습니다.</p>'
 '<p>다만 실제 사업자의 데이터를 열람하거나 서비스를 중단시키는 방식의 시험은 삼가 주시기 바랍니다. '
 '그 자료는 저희 것이 아니라 그 가게와 그 가게 손님의 것입니다.</p>'),
]

doc('privacy.html', '개인정보처리방침',
    '무엇을 받아 두고,<br>어디에 두고, 언제 지우는가.',
    '「개인정보 보호법」에 따라 회사가 처리하는 개인정보의 항목과 목적, 보유기간, 위탁과 국외 이전, '
    '그리고 정보주체의 권리를 적었습니다. 통화 녹음에 관한 항목을 별도로 두었습니다.',
    PRIVACY,
    '개인정보처리방침 &mdash; Saleringo',
    'Saleringo가 수집하는 개인정보의 항목, 목적, 보유기간, 처리위탁과 국외 이전, 통화 녹음 처리 방식, '
    '정보주체의 권리 행사 방법을 「개인정보 보호법」에 따라 공개합니다.',
    '개인정보처리방침')

doc('terms.html', '이용약관',
    '읽고 결정하실 수 있도록<br>짧게 적었습니다.',
    '요금과 해지, 데이터의 소유, 책임의 범위. 계약서를 읽는 데 변호사가 필요하지 않아야 한다고 봅니다. '
    '아직 법률 검토를 마치지 않았다는 사실도 아래에 그대로 적어 두었습니다.',
    TERMS,
    '이용약관 &mdash; Saleringo',
    'Saleringo 서비스 이용약관. 요금과 부가세, 해지와 일할 환불, 데이터 소유권, 책임 한도, '
    '준거법을 대한민국 법 기준으로 정리했습니다.',
    '이용약관')

doc('security.html', '보안',
    '하고 있는 것과<br>아직 하지 않은 것.',
    '치과라면 누가 어떤 치료를 물었는지가, 요양기관이라면 어느 가족이 어떤 상황인지가 남습니다. '
    '그래서 &ldquo;안전합니다&rdquo; 대신 실제로 무엇을 하고 있는지를 적습니다.',
    SECURITY,
    '보안 &mdash; Saleringo가 데이터를 다루는 방식',
    '암호화, 사업자 간 데이터 분리, 접근 기록, 학습 목적 사용 금지, 전체 내보내기. '
    '아직 보유하지 않은 인증과 SLA도 함께 밝힙니다.',
    '보안')

print('wrote ko/privacy.html, ko/terms.html, ko/security.html')
