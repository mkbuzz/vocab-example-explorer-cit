from pathlib import Path
import json, re

path = Path('index.html')
s = path.read_text(encoding='utf-8')
MARKER = '/* PLACEHOLDER_CHIPS_V1 */'
if MARKER in s:
    print('Placeholder chips already applied.')
    raise SystemExit(0)

# Restore A/B placeholders in the Japanese meanings for expression patterns.
jp = {
    'think-as':'AをBと考える',
    'signs-has':'AがBしたという兆候がある',
    'so-many-from-that':'Bから非常に多くのAを[動]しているため～',
    'cannot-quickly-enough':'Bするのに十分な速さでAできない',
    'become-interested':'AがBに興味を持つようになる',
    'source-of':'Bの供給源としてのA',
    'make-money':'AがBを[動]して多くのお金を稼ぐ',
    'these-include':'これらのAにはBが含まれる',
    'enable-a-to-b':'AがBできるようにする',
    'estimate-that':'AがBと推定する',
    'mainly-due':'Aは主にBが原因である',
    'greatly-reduced':'AがBを大幅に減らした',
    'plenty':'BにはAがたくさんある',
    'more-than-doubled':'Aは2倍以上になった',
    'largely-because':'Aは主にBだからである',
    'serious-problems':'Aは深刻な問題を引き起こす可能性がある',
    'another-way':'Aするもう一つの方法はBである',
    'give-chance':'AにBする機会を与える',
    'future-with':'Aのある未来を期待する',
}

m = re.search(r'const ITEMS = (\[.*?\]);\nconst STORAGE_KEY', s, re.S)
if not m:
    raise RuntimeError('Could not find ITEMS data')
items = json.loads(m.group(1))
for item in items:
    if item['id'] in jp:
        item['jpMeaning'] = jp[item['id']]
new_items = json.dumps(items, ensure_ascii=False, separators=(',', ':'))
s = s[:m.start(1)] + new_items + s[m.end(1):]

css = r'''
/* PLACEHOLDER_CHIPS_V1 */
.slot-chip{display:inline-flex;align-items:center;justify-content:center;min-width:1.55em;height:1.55em;padding:0 .38em;border-radius:999px;font-weight:850;font-size:.78em;line-height:1;vertical-align:.12em;border:1px solid transparent;box-shadow:inset 0 0 0 1px rgba(255,255,255,.35)}
.slot-a{background:#e8f1ff;border-color:#bfd0ec;color:#3e5f8c}
.slot-b{background:#f3eafb;border-color:#d5c1e8;color:#76548f}
.vocab-item .slot-chip{font-size:.72em;margin:0 .05em}
.flash-front .slot-chip{font-size:.58em;vertical-align:.18em}
.flash-back-title .slot-chip{font-size:.68em}
.related-chip .slot-chip{font-size:.72em}
.meaning-row .slot-chip{font-size:.76em}
'''
s = s.replace('</style>', css + '\n</style>', 1)

# Helper for rendering A/B placeholders as colored chips.
helper = r'''
function renderSlots(text){
  return String(text||"").replace(/\b([AB])\b/g,(m,x)=>`<span class="slot-chip slot-${x.toLowerCase()}">${x}</span>`);
}

'''
anchor = 'let flashFlipped=false;\n'
if anchor not in s:
    raise RuntimeError('Could not find flashcard helper anchor')
s = s.replace(anchor, helper + anchor, 1)

# Vocabulary list: render chips in expression names.
s = s.replace('b.innerHTML=`<span class="status ${s}">${markSymbol(s)}</span><span>${item.term}</span>`;',
              'b.innerHTML=`<span class="status ${s}">${markSymbol(s)}</span><span>${item.pos==="exp"?renderSlots(item.term):item.term}</span>`;', 1)

# Flashcard related expressions.
s = s.replace('${item.related.map(x=>`<span class="related-chip">${x}</span>`).join("")}',
              '${item.related.map(x=>`<span class="related-chip">${item.pos==="exp"?renderSlots(x):x}</span>`).join("")}', 1)

# Front and back titles.
s = s.replace('<div class="word-line"><h1>${item.term}</h1><span class="pos">${item.pos}</span></div>',
              '<div class="word-line"><h1>${item.pos==="exp"?renderSlots(item.term):item.term}</h1><span class="pos">${item.pos}</span></div>', 1)
s = s.replace('<div class="flash-back-title"><strong>${item.term}</strong></div>',
              '<div class="flash-back-title"><strong>${item.pos==="exp"?renderSlots(item.term):item.term}</strong></div>', 1)

# English and Japanese meanings on the back.
s = s.replace('<div class="meaning-row"><span class="pos">${item.pos}</span><span>${item.enMeaning}</span></div>',
              '<div class="meaning-row"><span class="pos">${item.pos}</span><span>${item.pos==="exp"?renderSlots(item.enMeaning):item.enMeaning}</span></div>', 1)
s = s.replace('<div class="meaning-row jp"><span class="pos">${item.jpPos}</span><span>${item.jpMeaning}</span></div>',
              '<div class="meaning-row jp"><span class="pos">${item.jpPos}</span><span>${item.pos==="exp"?renderSlots(item.jpMeaning):item.jpMeaning}</span></div>', 1)

path.write_text(s, encoding='utf-8')
print('Placeholder chips applied.')
