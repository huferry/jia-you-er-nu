# -*- coding: utf-8 -*-
import os, html
from pypinyin import pinyin, Style

TITLE = "家有儿女 S01E02 01:04.00 - 02:33.52"
OUT = "家有儿女S01E02_clip_01-04_lesson"
S = [
 ('01:04.00', '狂野', "Wild!"),
 ('01:07.00', '骚扰你们', "Harassing you guys!"),
 ('01:57.00', '小雪', "Xiaoxue!"),
 ('01:58.00', '你怎么居然交上男朋友', "How could you actually get yourself a boyfriend?!"),
 ('02:04.00', '你还 还 还找一个', "And you even — even — even found one!"),
 ('02:06.00', '什么男朋友', "What boyfriend?"),
 ('02:16.00', '你怎么不叫我', "Why didn't you tell me?"),
 ('02:27.00', '什么狂野的新鲜新人类', "Some kind of wild, fresh new type of person?"),
 ('02:30.24', '你居然还把她带回家里来', "You actually had the nerve to bring her home!"),
 ('02:32.44', '我对你太失望了', "I'm so disappointed in you."),
]
# (sentence_index, char_k_position) -> pinyin override
OVERRIDE = {
 (0, 0): 'kuáng',  # 狂 tone 2 — default fine, no override needed; keeping as placeholder
 (1, 0): 'sāo',   # 骚 — default pypinyin should give sāo; confirming
 (3, 1): 'zěn',   # 怎 — checking
 (3, 4): 'jū',    # 居 in 居然 → jū (actually default ok)
 (7, 1): 'me',    # 么 neutral — default ok
}
VOCAB = [
 ('骚扰', 'sāo rǎo', 'HSK5+', 'To harass, disturb, pester. 骚 (sāo) suggests agitation/disturbance; 扰 (rǎo) = disturb. Here said lightly as the boys leave — either teasing or the adult shooing them off. Collocation: 性骚扰 (sexual harassment), 骚扰电话 (nuisance call).'),
 ('居然', 'jū rán', 'HSK4', 'Actually, unexpectedly — expresses surprise or indignation at something happening contrary to expectation. 你居然…！= "How could you actually…!" Stronger and more emotional than 竟然, though both overlap. Used twice in this scene for dramatic effect.'),
 ('失望', 'shī wàng', 'HSK4', 'Disappointed; to lose hope in someone. 对你太失望了 = "I\'m so very disappointed in you." Pattern: 对…失望 = disappointed in/with [person/thing]. Opposite: 满意 (satisfied), 欣慰 (relieved/pleased). The double 太…了 structure intensifies.'),
 ('新人类', 'xīn rén lèi', 'colloquial', 'New human type/generation — a 1990s–2000s term for the younger generation seen as strange or alien by parents. 狂野的新鲜新人类 is Xiaoxue\'s dad\'s mock-dramatic description. Compare: 新新人类 (even newer type), 年轻一代 (the younger generation, neutral).'),
 ('怎么…的', 'zěn me…de', 'grammar', 'How-could-you construction: 你怎么不叫我 = "How could you not tell me?" The implied accusation is stronger than a plain question. When 的 appears at the end (你怎么不叫我的), it asks for an explanation; without 的 it\'s more rhetorical/accusatory.'),
 ('把…带回来', 'bǎ…dài huí lái', 'grammar', 'Disposal construction: 把 marks the object (她) acted upon; 带回来 = bring back. 你把她带回家里来 = "You brought her back home." 把 is used when the verb has a strong effect on the object. Compare: 带她回来 (simpler, less emphatic).'),
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
    # 不 sandhi: 不 (4th) → bú before another 4th-tone syllable
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
