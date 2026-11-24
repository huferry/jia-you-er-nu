# -*- coding: utf-8 -*-
import os, html
from pypinyin import pinyin, Style

TITLE = "家有儿女 20:45.00 - 21:17.00"
OUT = "家有儿女S01E01_clip_20-45_lesson"
S = [
 ('20:45.00', '妹妹', "Hey, sis."),
 ('20:46.00', '我发现你对小雪真有耐心', "I've noticed you're really patient with Xiaoxue."),
 ('20:48.00', '我真佩服', "I truly admire you."),
 ('20:50.00', '爱心 耐心 宽大为怀', "Big heart, patience, generous in spirit."),
 ('20:53.00', '你急 我都不急', "You might be anxious — I'm not anxious at all."),
 ('20:56.00', '我怎么可能急呢', "How could I possibly be anxious?"),
 ('21:00.00', '介绍一下', "Let me make an introduction."),
 ('21:02.00', '这位', "This is…"),
 ('21:08.00', '干什么呢你', "What are you doing?"),
 ('21:11.00', '这位是我的男朋友', "This is my boyfriend."),
 ('21:13.00', '狂野男孩', "Wild Boy."),
 ('21:15.00', '哈 我的爱心', "Ha — my love!"),
]
OVERRIDE = {
 # 的 in 我的爱心 (line 11): neutral tone 'de' — pypinyin handles this correctly
 # No overrides needed
}
VOCAB = [
 ('耐心', 'nài xīn', 'HSK4', 'Patient; patience. 耐 = endure; 心 = heart/mind. 对小雪真有耐心 = truly patient with Xiaoxue. Used as adjective (耐心的人 = a patient person) or noun (有耐心 = have patience). The word appears three times in this episode — a running theme for dealing with Xiaoxue.'),
 ('佩服', 'pèi fú', 'HSK4', 'To admire, have deep respect for. 我真佩服 = I truly admire you. Stronger than 尊重 (respect). Often used sincerely or ironically. 佩服佩服 (repeated) = genuine admiration or mock admiration depending on tone. Here it is 刘美\'s sister complimenting her calm demeanor.'),
 ('宽大为怀', 'kuān dà wéi huái', 'chengyu', 'To be magnanimous / generous in spirit. Four-character idiom: 宽大 = broad/generous; 为怀 = to hold in one\'s heart/mind. Used to praise someone\'s large-hearted tolerance. 刘美 lists 爱心·耐心·宽大为怀 as her personal virtues when dealing with her new stepdaughter.'),
 ('急', 'jí', 'HSK3', 'Anxious, in a hurry, urgent. 你急我都不急 = you may be anxious — I\'m not at all. 急 can be a stative verb (be anxious) or adjective (urgent). Common expressions: 着急 (feel anxious/worried); 急忙 (hurriedly); 急事 (urgent matter). Contrast: 急 (internal anxiety) vs 忙 (busy with tasks).'),
 ('介绍', 'jiè shào', 'HSK3', 'To introduce; introduction. 介绍一下 = let me make an introduction / allow me to introduce. The 一下 softens it into a casual, brief action. 自我介绍 = self-introduction; 介绍信 = letter of introduction. Xiaoxue uses this phrase before revealing her surprise boyfriend.'),
 ('男朋友', 'nán péng you', 'HSK3', 'Boyfriend. 男 = male; 朋友 = friend. The reveal is played for maximum shock: Xiaoxue introduces 狂野男孩 (Wild Boy) to her new blended family without warning. His name alone is a declaration of his personality.'),
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
