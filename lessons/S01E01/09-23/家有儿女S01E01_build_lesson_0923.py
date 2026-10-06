# -*- coding: utf-8 -*-
import os, html
from pypinyin import pinyin, Style

TITLE = "家有儿女 09:23.10 - 09:43.64"
OUT = "家有儿女S01E01_clip_09-23_lesson"
S = [
 ('09:23.10', '谁去给我喝杯水', "Whoever can't bear it, go get yourself a glass of water."),
 ('09:24.22', '饿了给水喝', 'Hungry, and all you get is water?'),
 ('09:26.82', '那叫后妈', "That's what a stepmother would do!"),
 ('09:28.04', '你闭嘴吧', 'Oh, shut up.'),
 ('09:29.76', '趁着姐姐没来', "Before your sister gets here,"),
 ('09:32.72', '我再嘱咐你两句', 'let me give you a couple more reminders.'),
 ('09:33.88', '你给我记住了', "You'd better remember this."),
 ('09:35.84', '记不住了', "Can't remember."),
 ('09:37.76', '我已经脑供血不足了', "My brain's already running low on blood flow."),
 ('09:40.52', '你闭嘴', 'Shut up.'),
 ('09:41.40', '你听清楚了啊', 'Now listen up carefully.'),
 ('09:43.64', '小雪姐姐可是一个文静的乖乖女', 'Sister Xiaoxue is a quiet, well-behaved girl.'),
]
# (sentence_index, char_position) -> pinyin override
OVERRIDE = {}
VOCAB = [
 ('后妈', 'hòumā', 'colloquial', '饿了给水喝，那叫后妈 = "giving water when hungry — that\'s what a stepmother would do." In Chinese folk culture 后妈 (stepmother) is the archetype of heartless caregiving. Used here as a biting hyperbole, not a literal accusation.'),
 ('趁着', 'chènzhe', 'HSK5', 'To seize/take advantage of a time or situation. Pattern: 趁着 + condition + action. 趁着姐姐没来 = while sister hasn\'t arrived yet. Related idiom: 趁热打铁 (strike while the iron is hot).'),
 ('嘱咐', 'zhǔfù', 'HSK5', 'To give earnest, repeated instructions. More heartfelt than 告诉 — implies the speaker really cares. Common: 临走前嘱咐 (give instructions just before leaving). 再嘱咐你两句 = let me remind you of a couple more things.'),
 ('脑供血不足', 'nǎo gōng xuè bù zú', 'idiom', 'Literally "insufficient blood supply to the brain" — a real medical term (cerebral ischemia). Used here as comic self-deprecation: 我已经脑供血不足了 = my brain is already oxygen-starved, don\'t expect me to remember things.'),
 ('文静', 'wénjìng', 'HSK5', 'Quiet, gentle, refined (of character). Almost always applied to girls/women. Contrast with 活泼 (lively, outgoing). In Chinese parenting rhetoric, 文静 is high praise for a daughter.'),
 ('乖乖女', 'guāiguāi nǚ', 'colloquial', 'A well-behaved, obedient "good girl". 乖 (guāi) means docile and compliant; doubling it adds an affectionate, cutesy tone. Boy equivalent: 乖宝宝. A 乖乖女 causes no trouble and does what she\'s told — which is exactly what the mom is preparing 小雨 to expect.'),
]

def tone_of(p):
    for ch in p:
        if ch in "āēīōūǖ": return 1
        if ch in "áéíóúǘ": return 2
        if ch in "ǎěǐǒǔǚ": return 3
        if ch in "àèìòùǜ": return 4
    return 0

def sent_chars(i, text):
    py = pinyin(text.replace(" ", ""), style=Style.TONE, heteronym=False)
    out, k = [], 0
    for pos, ch in enumerate(text):
        if ch == " ":
            out.append((None, None)); continue
        p = OVERRIDE.get((i, k), py[k][0]); k += 1
        out.append((ch, p))
    # 不 sandhi
    real = [j for j, (c, _) in enumerate(out) if c]
    for a, j in enumerate(real[:-1]):
        c, p = out[j]
        if c == "不" and tone_of(out[real[a+1]][1]) == 4:
            out[j] = (c, "bú")
    return out

def box(p):
    t = tone_of(p); return {2: "t2", 3: "t3", 4: "t4"}.get(t, "t0")

def sent_html(i, ts, text, en, plain=False):
    if plain:
        return f'<div class="pl">{html.escape(text.replace(" ", "　"))}</div>'
    cells = []
    for c, p in sent_chars(i, text):
        if c is None: cells.append('<span class="gap"></span>'); continue
        cells.append(f'<span class="c"><span class="py">{p}</span><span class="hz {box(p)}">{c}</span></span>')
    return f'<div class="s"><div class="ts">[{ts}]</div><div class="row">{"".join(cells)}</div><div class="en">{html.escape(en)}</div></div>'

css = """
@page { size: A4; margin: 14mm; }
body { font-family: "STHeiti","Heiti SC","Hiragino Sans GB",sans-serif; color:#111; margin:0; }
h1 { font-size:20pt; margin:0 0 2pt; } .sub{color:#555;font-size:9.5pt;margin-bottom:6pt}
.legend{font-size:9.5pt;margin-bottom:10pt;display:flex;gap:12pt;align-items:center}
.sw{display:inline-block;width:14pt;height:14pt;line-height:14pt;text-align:center;font-size:10pt;box-sizing:border-box}
.ts{font-size:8.5pt;color:#777;margin-top:7pt}
.s{page-break-inside:avoid;break-inside:avoid}
.vt tr{page-break-inside:avoid;break-inside:avoid}
.row{display:flex;flex-wrap:wrap;align-items:flex-end}
.c{display:inline-flex;flex-direction:column;align-items:center;margin:0 1.5pt}
.py{font-size:8.5pt;color:#333;height:11pt} .hz{font-size:19pt;line-height:24pt;padding:0 2pt;border:2px solid transparent;box-sizing:border-box}
.gap{display:inline-block;width:10pt}
.t2{border-color:#0047d6}.t3{border-color:#0f8a1f}.t4{border-color:#d21414}
.en{font-style:italic;font-size:10.5pt;color:#333;margin-top:2pt}
h2{font-size:15pt;margin:0 0 4pt}
.vt{width:100%;border-collapse:collapse;margin-top:6pt}
.vt th{text-align:left;font-size:9.5pt;border-bottom:1.5px solid #333;padding:4pt}
.vt td{vertical-align:top;padding:6pt 4pt;border-bottom:1px solid #ccc;font-size:9.5pt}
.vh{font-size:16pt}.vp{font-size:11.5pt}
.txt h2{page-break-before:always}
.pl{font-size:19pt;line-height:1.2;padding:5pt 0;border-bottom:1px solid #ddd;margin:0}
"""
legend = ('<div class="legend"><span>Tone colors:</span><span>1st / neutral (no box)</span>'
 '<span><span class="sw t2" style="border:2px solid #0047d6">二</span> 2nd</span>'
 '<span><span class="sw" style="border:2px solid #0f8a1f">三</span> 3rd</span>'
 '<span><span class="sw" style="border:2px solid #d21414">四</span> 4th</span></div>')
body = [f'<h1>{TITLE}</h1><div class="sub">Chinese text with per-character pinyin, English translation, and timestamps</div>', legend]
for i, (ts, t, en) in enumerate(S):
    if i == 6:
        body.append('<div style="page-break-before:always"></div>')
    body.append(sent_html(i, ts, t, en))
body.append('<h2 style="page-break-before:always">HSK 3+ Vocabulary</h2><div class="sub">Words from the text above that are HSK level 3 or higher (levels approximate).</div>')
body.append('<table class="vt"><tr><th>Word</th><th>Pinyin</th><th>Explanation</th></tr>')
for w, p, lv, ex in VOCAB:
    body.append(f'<tr><td><span class="vh">{w}</span><br>{lv}</td><td class="vp">{p}</td><td>{html.escape(ex)}</td></tr>')
body.append('</table>')
body.append('<div class="txt"><h2>Text Only</h2>' + "".join(sent_html(i, ts, t, en, plain=True) for i, (ts, t, en) in enumerate(S)) + '</div>')
open(os.path.join(os.path.dirname(os.path.abspath(__file__)), OUT + ".html"), "w", encoding="utf-8").write(f'<!doctype html><html><head><meta charset="utf-8"><title>{TITLE}</title><style>{css}</style></head><body>{"".join(body)}</body></html>')
