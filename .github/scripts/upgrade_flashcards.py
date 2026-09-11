from pathlib import Path
import json, re

path = Path('index.html')
s = path.read_text(encoding='utf-8')
MARKER = '/* FLASHCARD_UPGRADE_V1 */'
if MARKER in s:
    print('Flashcard upgrade already applied.')
    raise SystemExit(0)

meta = {
'diverse': {'wordFamily':'(n) diversity, diversification; (v) diversify; (adj) diverse; (adv) diversely','related':['varied','various','different'],'label':'Synonyms','en':'having many different kinds','jp':'多様な, 様々な'},
'species': {'wordFamily':'','related':['kind','type','variety'],'label':'Synonyms','en':'a group of similar plants or animals','jp':'種, 生物種'},
'commercial': {'wordFamily':'(n) commerce; (adj) commercial; (adv) commercially','related':['business','for-profit','business-related'],'label':'Synonyms','en':'related to business or making money','jp':'商業の, 営利目的の'},
'quantity': {'wordFamily':'(n) quantity; (adj) quantitative; (adv) quantitatively','related':['amount','number','volume'],'label':'Synonyms','en':'an amount or number of something','jp':'量, 数量'},
'estimate': {'wordFamily':'(n) estimate, estimation; (v) estimate; (adj) estimated','related':['calculate','judge','approximate'],'label':'Synonyms','en':'to make a careful guess about an amount or number','jp':'推定する, 見積もる'},
'reduce': {'wordFamily':'(n) reduction; (v) reduce; (adj) reduced','related':['decrease','lower','cut'],'label':'Synonyms','en':'to make something smaller or less','jp':'減らす, 減少させる'},
'double': {'wordFamily':'(n) double; (v) double; (adj) double','related':['multiply by two','become twice as large'],'label':'Synonyms','en':'to become or make something twice as large','jp':'2倍になる, 2倍にする'},
'stable': {'wordFamily':'(n) stability; (adj) stable; (adv) stably','related':['steady','balanced','secure'],'label':'Synonyms','en':'not changing suddenly or easily','jp':'安定した'},
'restore': {'wordFamily':'(n) restoration; (v) restore; (adj) restored','related':['repair','recover','bring back'],'label':'Synonyms','en':'to return something to a good or earlier condition','jp':'回復させる, 元の状態に戻す'},
'survive': {'wordFamily':'(n) survival, survivor; (v) survive','related':['live','stay alive','remain'],'label':'Synonyms','en':'to continue to live or exist','jp':'生き残る, 生存する'},
'major-factor': {'wordFamily':'','related':['main cause','important factor','key factor'],'label':'Similar expressions','en':'an important cause or influence','jp':'主な要因, 大きな要因'},
'maintain': {'wordFamily':'(n) maintenance; (v) maintain','related':['keep','preserve','continue'],'label':'Synonyms','en':'to keep something at the same level or condition','jp':'維持する, 保つ'},
'communities': {'wordFamily':'(n) community; (adj) communal','related':['local areas','local groups','neighborhoods'],'label':'Synonyms','en':'groups of people living in the same area','jp':'地域社会, 地域の人々'},
'traditional': {'wordFamily':'(n) tradition; (adj) traditional; (adv) traditionally','related':['conventional','customary','long-established'],'label':'Synonyms','en':'following customs or methods used for a long time','jp':'伝統的な, 昔ながらの'},
'target': {'wordFamily':'(n) target; (v) target; (adj) targeted','related':['aim at','focus on','direct at'],'label':'Synonyms','en':'to aim something at a particular person or group','jp':'狙う, 対象にする'},
'locate': {'wordFamily':'(n) location; (v) locate; (adj) located','related':['find','identify','discover'],'label':'Synonyms','en':'to find the exact place of something','jp':'場所を突き止める, 見つける'},
'equipment': {'wordFamily':'(n) equipment; (v) equip; (adj) equipped','related':['tools','gear','machinery'],'label':'Synonyms','en':'the tools or machines needed for an activity','jp':'装置, 機器, 道具'},
'enable': {'wordFamily':'(v) enable; (adj) enabled','related':['allow','permit','make possible'],'label':'Synonyms','en':'to make it possible for someone to do something','jp':'～を可能にする'},
'publish': {'wordFamily':'(n) publication, publisher; (v) publish; (adj) published','related':['release','print','issue'],'label':'Synonyms','en':'to make a book, article, or research available to the public','jp':'発表する, 出版する'},
'journal': {'wordFamily':'(n) journal, journalism, journalist','related':['academic journal','periodical','publication'],'label':'Synonyms','en':'a magazine containing academic or professional articles','jp':'学術誌, 専門誌'},
'prediction': {'wordFamily':'(n) prediction; (v) predict; (adj) predictable; (adv) predictably','related':['forecast','expectation','projection'],'label':'Synonyms','en':'a statement about what will happen in the future','jp':'予測, 予想'},
'reproduce': {'wordFamily':'(n) reproduction; (v) reproduce; (adj) reproductive','related':['breed','have young','produce offspring'],'label':'Synonyms','en':'to produce babies or young','jp':'繁殖する, 子孫を増やす'},
'throughout-history': {'wordFamily':'','related':['over the course of history','through history'],'label':'Similar expressions','en':'during all periods of history','jp':'歴史を通じて'},
'today': {'wordFamily':'','related':['nowadays','currently','at present'],'label':'Similar expressions','en':'at the present time','jp':'今日では, 現在では'},
'however': {'wordFamily':'','related':['nevertheless','still','yet'],'label':'Similar expressions','en':'used to introduce a contrasting idea','jp':'しかし, しかしながら'},
'mid-20th': {'wordFamily':'','related':['around the middle of the 20th century','in the mid-1900s'],'label':'Similar expressions','en':'around the middle of the 20th century','jp':'20世紀半ばに'},
'response': {'wordFamily':'','related':['because of this','reacting to this','as a response'],'label':'Similar expressions','en':'as a reaction to what happened before','jp':'これを受けて'},
'result': {'wordFamily':'','related':['therefore','consequently','because of this'],'label':'Similar expressions','en':'used to introduce a result','jp':'その結果'},
'addition': {'wordFamily':'','related':['additionally','also','furthermore'],'label':'Similar expressions','en':'used to add another point','jp':'さらに'},
'in-2010': {'wordFamily':'','related':['during 2010','that year'],'label':'Similar expressions','en':'during the year 2010','jp':'2010年に'},
'particular': {'wordFamily':'','related':['especially','particularly','specifically'],'label':'Similar expressions','en':'used to focus attention on one example or point','jp':'特に'},
'without-them': {'wordFamily':'','related':['if they were not there','in their absence'],'label':'Similar expressions','en':'if those people or things were not present','jp':'それらがいなければ'},
'for-example': {'wordFamily':'','related':['for instance','such as','to give an example'],'label':'Similar expressions','en':'used to introduce an example','jp':'例えば'},
'think-as': {'wordFamily':'','related':['regard A as B','see A as B','consider A to be B'],'label':'Similar expressions','en':'to consider A to be B','jp':'AをBと考える'},
'signs-has': {'wordFamily':'','related':['there is evidence that…','evidence suggests that…'],'label':'Similar expressions','en':'there is evidence showing that something has happened','jp':'～したという兆候がある'},
'so-many-from-that': {'wordFamily':'','related':['V-ing such a large number of A from B that…'],'label':'Similar expressions','en':'doing something to so many A from B that a result follows','jp':'～から非常に多くの～を[動]しているため～'},
'cannot-quickly-enough': {'wordFamily':'','related':['cannot A fast enough to B','A too slowly to B'],'label':'Similar expressions','en':'to be unable to do A fast enough to achieve B','jp':'～するのに十分な速さで～できない'},
'become-interested': {'wordFamily':'','related':['develop an interest in','start to be interested in'],'label':'Similar expressions','en':'A starts to have an interest in B','jp':'～が～に興味を持つようになる'},
'source-of': {'wordFamily':'','related':['A as a supply of B','A as a way to obtain B'],'label':'Similar expressions','en':'A used as something that provides B','jp':'～の供給源としての～'},
'make-money': {'wordFamily':'','related':['earn a lot of money V-ing','make large profits V-ing'],'label':'Similar expressions','en':'A earns a large amount of money by doing B','jp':'～を[動]して多くのお金を稼ぐ'},
'these-include': {'wordFamily':'','related':['among these A is B','B is included in these A'],'label':'Similar expressions','en':'B is one example or member of these A','jp':'これらの～には～が含まれる'},
'enable-a-to-b': {'wordFamily':'','related':['allow A to B','make it possible for A to B'],'label':'Similar expressions','en':'to make it possible for A to do B','jp':'～が～できるようにする'},
'estimate-that': {'wordFamily':'','related':['A calculates that B','A believes approximately that B'],'label':'Similar expressions','en':'A makes a careful guess that B is true','jp':'～が～と推定する'},
'mainly-due': {'wordFamily':'','related':['A is mostly caused by B','A results mainly from B'],'label':'Similar expressions','en':'B is the main cause of A','jp':'～は主に～が原因である'},
'greatly-reduced': {'wordFamily':'','related':['A has significantly decreased B','A has sharply cut B'],'label':'Similar expressions','en':'A has made B much smaller or fewer','jp':'～が～を大幅に減らした'},
'plenty': {'wordFamily':'','related':['there are many A in B','B has lots of A'],'label':'Similar expressions','en':'B contains a large number or enough of A','jp':'～には～がたくさんある'},
'more-than-doubled': {'wordFamily':'','related':['A have increased to more than twice as much','A have risen by over 100%'],'label':'Similar expressions','en':'A have become more than twice as large or numerous','jp':'～は2倍以上になった'},
'largely-because': {'wordFamily':'','related':['A is mainly because B','A is mostly due to B'],'label':'Similar expressions','en':'B is the main reason for A','jp':'～は主に～だからである'},
'serious-problems': {'wordFamily':'','related':['A can create major problems','A can lead to serious problems'],'label':'Similar expressions','en':'A may produce important or harmful problems','jp':'～は深刻な問題を引き起こす可能性がある'},
'make-prediction': {'wordFamily':'','related':['predict','forecast','make a forecast'],'label':'Similar expressions','en':'to say what you think will happen in the future','jp':'予測する'},
'another-way': {'wordFamily':'','related':['another method of A is B','you can also A by B'],'label':'Similar expressions','en':'B is another method for doing A','jp':'～するもう一つの方法は～である'},
'give-chance': {'wordFamily':'','related':['give A an opportunity to B','allow A to B'],'label':'Similar expressions','en':'to provide A with an opportunity to do B','jp':'～に～する機会を与える'},
'future-with': {'wordFamily':'','related':['hope for a future with A','expect a future with A'],'label':'Similar expressions','en':'to feel hopeful about having A in the future','jp':'～のある未来を期待する'},
}

m = re.search(r'const ITEMS = (\[.*?\]);\nconst STORAGE_KEY', s, re.S)
if not m:
    raise RuntimeError('Could not find ITEMS data.')
items = json.loads(m.group(1))
missing = [x['id'] for x in items if x['id'] not in meta]
extra = [k for k in meta if k not in {x['id'] for x in items}]
if missing or extra:
    raise RuntimeError(f'Metadata mismatch. missing={missing}, extra={extra}')

jp_pos = {'n':'名','v':'動','adj':'形','adv':'副','phr':'句','exp':'表'}
for item in items:
    d = meta[item['id']]
    item['wordFamily'] = d['wordFamily']
    item['related'] = d['related']
    item['relatedLabel'] = d['label']
    item['enMeaning'] = d['en']
    item['jpMeaning'] = d['jp']
    item['jpPos'] = jp_pos.get(item['pos'], item['pos'])

new_items = json.dumps(items, ensure_ascii=False, separators=(',', ':'))
s = s[:m.start(1)] + new_items + s[m.end(1):]

css = r'''
/* FLASHCARD_UPGRADE_V1 */
.word-head{background:transparent;border:0;padding:0;perspective:1200px;cursor:pointer;outline:none}
.word-head:focus-visible{outline:3px solid rgba(36,87,214,.25);outline-offset:4px;border-radius:17px}
.flashcard-inner{display:grid;transform-style:preserve-3d;transition:transform .32s ease}
.word-head.flipped .flashcard-inner{transform:rotateY(180deg)}
.flash-face{grid-area:1/1;backface-visibility:hidden;-webkit-backface-visibility:hidden;border:1px solid var(--border);border-radius:16px;padding:20px;min-height:210px;box-shadow:0 2px 8px rgba(24,35,52,.04);display:flex;flex-direction:column}
.flash-front{background:linear-gradient(135deg,#fbfdff 0%,#edf4ff 100%);align-items:center;justify-content:center;text-align:center}
.flash-back{background:var(--card);transform:rotateY(180deg);justify-content:center}
.flash-front .word-line{justify-content:center;align-items:center}
.flash-front h1{font-size:clamp(2rem,9vw,3rem);margin:0;line-height:1.12}
.flip-hint{margin-top:18px;color:var(--muted);font-size:.8rem;font-weight:650}
.flash-back-title{display:flex;align-items:baseline;gap:9px;flex-wrap:wrap;margin-bottom:12px}
.flash-back-title strong{font-size:1.4rem}
.back-section{padding:8px 0;border-top:1px solid #edf0f3}
.back-section:first-of-type{border-top:0}
.back-label{font-size:.75rem;text-transform:uppercase;letter-spacing:.04em;font-weight:800;color:var(--muted);margin-bottom:5px}
.family-line{line-height:1.8}
.mini-pos{display:inline-flex;align-items:center;border-radius:999px;background:#eef1f5;color:#596472;padding:1px 6px;font-weight:750;font-size:.72rem;margin-right:3px;vertical-align:1px}
.related-list{display:flex;flex-wrap:wrap;gap:6px}
.related-chip{display:inline-flex;background:#f4f6f9;border:1px solid #e4e8ed;border-radius:999px;padding:4px 8px;font-size:.86rem;color:#46515d}
.meaning-row{display:flex;align-items:flex-start;gap:8px;margin-top:8px;font-size:1rem}
.meaning-row .pos{flex:0 0 auto;margin-top:1px}
.meaning-row.jp{color:#4f5965}
.flash-back .flip-hint{margin-top:12px;text-align:right}
@media(max-width:480px){
  .flash-face{padding:17px;min-height:220px}
  .flash-back-title strong{font-size:1.28rem}
  .back-section{padding:7px 0}
  .related-chip{font-size:.82rem}
}
'''
s = s.replace('</style>', css + '\n</style>', 1)

old_head = '''  document.getElementById("wordHead").innerHTML=\n    `<div class="word-line"><h1>${item.term}</h1><span class="pos">${item.pos}</span></div>\n     <p class="meaning-en">${item.enMeaning}</p>\n     <p class="meaning-jp">${item.jpMeaning}</p>`;'''
new_head = r'''  const familyHtml=item.wordFamily
    ? `<div class="back-section"><div class="back-label">Word family</div><div class="family-line">${formatWordFamily(item.wordFamily)}</div></div>`
    : "";
  const relatedHtml=(item.related&&item.related.length)
    ? `<div class="back-section"><div class="back-label">${item.relatedLabel||"Similar expressions"}</div><div class="related-list">${item.related.map(x=>`<span class="related-chip">${x}</span>`).join("")}</div></div>`
    : "";
  const wordHead=document.getElementById("wordHead");
  wordHead.classList.remove("flipped");
  wordHead.setAttribute("role","button");
  wordHead.setAttribute("tabindex","0");
  wordHead.setAttribute("aria-label",`Flashcard for ${item.term}. Tap or press Space to reveal the meaning.`);
  wordHead.setAttribute("aria-pressed","false");
  wordHead.innerHTML=
    `<div class="flashcard-inner">
       <section class="flash-face flash-front" aria-hidden="false">
         <div class="word-line"><h1>${item.term}</h1><span class="pos">${item.pos}</span></div>
         <div class="flip-hint">Tap to reveal meaning ↻</div>
       </section>
       <section class="flash-face flash-back" aria-hidden="true">
         <div class="flash-back-title"><strong>${item.term}</strong></div>
         ${familyHtml}
         ${relatedHtml}
         <div class="back-section">
           <div class="meaning-row"><span class="pos">${item.pos}</span><span>${item.enMeaning}</span></div>
           <div class="meaning-row jp"><span class="pos">${item.jpPos}</span><span>${item.jpMeaning}</span></div>
         </div>
         <div class="flip-hint">Tap to flip back ↻</div>
       </section>
     </div>`;
  wordHead.onclick=()=>toggleFlashcard();'''
if old_head not in s:
    raise RuntimeError('Could not find wordHead rendering block.')
s = s.replace(old_head, new_head, 1)

helpers = r'''
let flashFlipped=false;
function formatWordFamily(text){
  return String(text||"").replace(/\(([^)]+)\)/g,'<span class="mini-pos">$1</span>');
}
function setFlashcard(on){
  flashFlipped=!!on;
  const card=document.getElementById("wordHead");
  if(!card) return;
  card.classList.toggle("flipped",flashFlipped);
  card.setAttribute("aria-pressed",String(flashFlipped));
  const front=card.querySelector(".flash-front"), back=card.querySelector(".flash-back");
  if(front) front.setAttribute("aria-hidden",String(flashFlipped));
  if(back) back.setAttribute("aria-hidden",String(!flashFlipped));
}
function toggleFlashcard(){ setFlashcard(!flashFlipped); }

'''
s = s.replace('function renderCard(id){', helpers + 'function renderCard(id){\n  flashFlipped=false;', 1)

old_keys = '  if(cardOpen && e.key==="ArrowLeft"){'
new_keys = '''  if(cardOpen && (e.code==="Space" || e.key===" ")){\n    e.preventDefault();\n    toggleFlashcard();\n  }else if(cardOpen && e.key==="ArrowLeft"){'''
if old_keys not in s:
    raise RuntimeError('Could not find keyboard handler.')
s = s.replace(old_keys, new_keys, 1)

old_hint = 'Keyboard: <kbd>←</kbd>/<kbd>→</kbd> cards　<kbd>,</kbd> learned　<kbd>.</kbd> review　<kbd>B</kbd> vocabulary list　<kbd>H</kbd> home'
new_hint = 'Keyboard: <kbd>Space</kbd> flip　<kbd>←</kbd>/<kbd>→</kbd> cards　<kbd>,</kbd> learned　<kbd>.</kbd> review　<kbd>B</kbd> vocabulary list　<kbd>H</kbd> home'
if old_hint not in s:
    raise RuntimeError('Could not find desktop shortcut hint.')
s = s.replace(old_hint, new_hint, 1)

path.write_text(s, encoding='utf-8')
print('Flashcard upgrade applied successfully.')
