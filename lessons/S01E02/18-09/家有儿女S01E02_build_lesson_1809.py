# -*- coding: utf-8 -*-
import os, html
from pypinyin import pinyin, Style

TITLE = "家有儿女 S01E02 18:09.24 - 18:55.24"
OUT = "家有儿女S01E02_clip_18-09_lesson"
S = [
 ('18:09.24', '怎么着', "So what do you say?"),
 ('18:14.24', '我看由于事情非常严重', "I think, given that the matter is extremely serious,"),
 ('18:16.24', '所以还是事先确认一下为好', "it would be best to confirm something in advance."),
 ('18:19.24', '请问你家夏雨在吗', "May I ask — is Xia Yu home?"),
 ('18:22.24', '我在这呢', "I'm right here."),
 ('18:32.24', '对不起', "I'm sorry."),
 ('18:38.24', '多多 我爱你', "Duoduo, I love you!"),
 ('18:41.24', '你们都听到了吧', "You all heard that, didn't you?"),
 ('18:44.24', '她只是对我女儿进行', "She was directing at my daughter —"),
 ('18:47.24', '性骚扰', "— sexual harassment!"),
 ('18:50.24', '其实没那么严重', "Actually it's not that serious."),
 ('18:52.24', '其实我们家小雨 才七岁', "Actually, our Xiaoyu is only seven years old."),
]
# (sentence_index, char_k_position) -> pinyin override
OVERRIDE = {
 (1, 2): 'yóu',  # 由 in 由于 → yóu
 (1, 7): 'fēi',  # 非 in 非常 → fēi
 (2, 3): 'shì',  # 事 in 事先 → shì
 (2, 6): 'wéi',  # 为 in 为好 → wéi (for the purpose of)
 (5, 0): 'duì',  # 对 → duì
 (7, 2): 'dōu',  # 都 → dōu
 (8, 3): 'jǐn',  # 仅 → skip; 进 in 进行 → jìn
 (9, 0): 'xìng', # 性 in 性骚扰 → xìng
 (11, 4): 'xiǎo', # 小 → xiǎo
 (11, 6): 'cái', # 才 → cái (only/just)
}
VOCAB = [
 ('事先', 'shì xiān', 'HSK4', 'In advance, beforehand. 事先确认 = "confirm in advance." Synonym: 提前 (ahead of time, more colloquial). 事先 is slightly more formal; often used in procedures, planning, warnings: 事先说明, 事先通知.'),
 ('确认', 'què rèn', 'HSK4', 'To confirm, verify. 确认一下 = "just confirm/check." 一下 softens the request (see grammar note). Collocations: 确认信息, 确认身份, 请确认. Near-synonym 核实 (verify facts) is more investigative and formal.'),
 ('进行', 'jìn xíng', 'HSK3', 'To carry out, conduct, engage in. Used with abstract or formal activities: 进行讨论, 进行手术, 进行骚扰. It converts a noun into a verb phrase. The father uses it here satirically formally: 对…进行性骚扰 = "to conduct sexual harassment against."'),
 ('性骚扰', 'xìng sāo rǎo', 'phrase', 'Sexual harassment. The father applies this adult legal term absurdly to a 7-year-old\'s declaration of love — the comedy lies in the mismatch of register. 骚扰 alone = to harass/disturb (can be non-sexual).'),
 ('才', 'cái', 'HSK3', 'Only, merely — stresses that a quantity or age is surprisingly small. 才七岁 = "only seven years old!" Contrast 就 (already, stresses earliness): 就七岁了 = "already seven." Same character, opposite implications depending on context.'),
 ('一下', 'yī xià', 'grammar', 'Softener after a verb — reduces the formality/imposingness of a request or action. 确认一下 = "just check / take a look." Compare 确认 (blunt/abrupt) vs 确认一下 (casual, polite). Also signals a brief/single action.'),
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
