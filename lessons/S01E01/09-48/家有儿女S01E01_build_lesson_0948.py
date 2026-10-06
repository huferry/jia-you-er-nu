# -*- coding: utf-8 -*-
import os, html
from pypinyin import pinyin, Style

TITLE = "家有儿女 09:48.30 - 10:08.96"
OUT = "家有儿女S01E01_clip_09-48_lesson"
S = [
 ('09:48.30', '咱们生活在一块', "We'll all be living together,"),
 ('09:50.06', '你不许欺负人家', "so you are NOT allowed to bully her."),
 ('09:51.24', '不欺负人家', "Won't bully her."),
 ('09:54.02', '我也不欺负她', "I won't bully her either."),
 ('09:55.72', '真乖', "So well-behaved!"),
 ('09:56.90', '你瞧小雨多乖', "Look how good Xiaoyu is!"),
 ('09:58.44', '可以奖你一片火腿肠', "That deserves a slice of sausage!"),
 ('10:01.22', '别去了', "Never mind — stay put."),
 ('10:03.26', '回来了', "They're back!"),
 ('10:06.50', '小雪呢', "Where's Xiaoxue?"),
 ('10:08.48', '来了', "She's here!"),
 ('10:08.96', '小雪来', "Xiaoxue's here!"),
]
# (sentence_index, char_position) -> pinyin override
OVERRIDE = {
 (1, 3): 'xū',   # 许 in 不许: xǔ is 3rd tone, no sandhi needed; but pypinyin may read 不许 as bù xǔ correctly
}
VOCAB = [
 ('咱们', 'zánmen', 'HSK3', 'We/us (inclusive) — includes the listener, unlike 我们 which can exclude them. 咱们生活在一块 = we (all of us together) will live in one place. In Beijing colloquial speech 咱 alone can mean I/me or we.'),
 ('欺负', 'qīfu', 'HSK4', 'To bully, pick on, take advantage of. 不许欺负人家 = not allowed to bully her. 人家 here refers to a third person (Xiaoxue). Common collocations: 欺负弱小, 被人欺负.'),
 ('不许', 'bù xǔ', 'HSK4', 'Not allowed to, must not. Stronger and more authoritative than 不要 or 别. Pattern: 不许 + verb. Typical parent-to-child command. Cf. 禁止 (forbidden, formal/written).'),
 ('奖', 'jiǎng', 'HSK4', 'To reward; a reward/prize. 奖你一片火腿肠 = reward you with a slice of sausage. Colloquial: 奖励 is the more formal word. The joke here is the absurdly humble reward (cheap sausage) for such earnest behavior.'),
 ('火腿肠', 'huǒtuǐ cháng', 'colloquial', 'Processed ham sausage — the cheap, ubiquitous snack stick sold at every corner shop. In Chinese family comedies, offering 火腿肠 as a "prize" is a running joke about the gap between a child\'s eagerness and the parent\'s stinginess/humor.'),
 ('别…了', 'bié … le', 'grammar', 'Stop/don\'t (do something). 别去了 = don\'t bother going / stop (about to go). The 了 signals a change of plan or that the action is no longer needed. Contrast: 别去 (simple prohibition) vs 别去了 (canceling an action already in progress or about to start).'),
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
