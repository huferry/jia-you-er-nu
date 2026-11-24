# -*- coding: utf-8 -*-
import os, html
from pypinyin import pinyin, Style

TITLE = "家有儿女 16:30.00 - 17:11.00"
OUT = "家有儿女S01E01_clip_16-30_lesson"
S = [
 ('16:30.00', '妈', "Mom!"),
 ('16:32.00', '小雪她谁都不叫我', "Xiaoxue doesn't call me anything at all."),
 ('16:33.00', '平时出大门了', "Usually when she goes out the door—"),
 ('16:34.00', '连个头都不回', "She doesn't even turn her head."),
 ('16:37.00', '上哪儿去了', "Where did she go?"),
 ('16:38.00', '上哪儿了', "Where'd she go?"),
 ('16:39.00', '不知道', "Don't know."),
 ('16:40.00', '我更不知道', "I know even less."),
 ('16:41.00', '这孩子 这孩子 这孩子', "This kid… this kid… this kid…"),
 ('16:59.00', '你看看', "Take a look."),
 ('17:09.00', '没看见箱子还在', "Don't you see the suitcase is still here?"),
 ('17:11.00', '这说明啊', "That means, you see—"),
]
# (sentence_index, char_k_position) -> pinyin override
OVERRIDE = {
 # 还 in "没看见箱子还在": 还 = hái (still), k=5 (没0,看1,见2,箱3,子4,还5,在6)
 (10, 5): 'hái',
}
VOCAB = [
 ('谁都不', 'shéi dōu bù', 'grammar', 'Not … anyone; not … at all. 谁都不叫我 = doesn\'t call me anything (lit. "doesn\'t call me, whoever"). Pattern: 谁都不 + V = nobody (or not … anyone). Compare 什么都不 (nothing at all), 哪儿都不 (nowhere at all). The 都 here is a universal quantifier: it intensifies the negation.'),
 ('连…都/也…', 'lián … dōu/yě', 'HSK4', 'Even … (not). 连个头都不回 = she doesn\'t even turn her head. Pattern: 连 + NP + 都/也 + (neg.) V. Used to highlight the most obvious or minimal thing that is (or isn\'t) done. Very common in spoken Chinese to express frustration or emphasis.'),
 ('上哪儿', 'shàng nǎr', 'colloquial', 'Where to? / Where did (you/she) go? Colloquial Beijing contraction of 上哪儿去. 上 here = going to (direction verb). Common spoken pattern: 上哪儿去了 = where did you go? / where\'d she go? Also heard as 去哪儿了 in more standard speech. The repeated questions (上哪儿去了 / 上哪儿了) show the two grandmothers echoing each other in confusion.'),
 ('箱子', 'xiāng zi', 'HSK4', 'Suitcase, box, trunk. 没看见箱子还在 = don\'t you see the suitcase is still here? A key plot clue: Xiaoxue\'s suitcase being left behind means she hasn\'t run away back to grandpa\'s. 还 here = still (hái). 箱 alone = chest/box; common compounds: 行李箱 (luggage), 冰箱 (refrigerator, lit. "ice box").'),
 ('说明', 'shuō míng', 'HSK4', 'To indicate, to show, to prove; an explanation. 这说明啊 = that means / that shows. As a verb: 说明 + clause (this shows that…). As a noun: 使用说明 (user manual / instructions). Often followed by a logical conclusion — here 夏东海 is building suspense before his deduction about Xiaoxue.'),
 ('更', 'gèng', 'HSK3', 'Even more, still more. 我更不知道 = I know even less (lit. "I even more don\'t know"). Degree adverb used to escalate a comparison. Compare: 还 (hái) = still; 更 = even more so. Pattern: A + neg. V, B + 更 + neg. V = if A doesn\'t, B does so even less.'),
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
