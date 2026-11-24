# -*- coding: utf-8 -*-
import os, html
from pypinyin import pinyin, Style

TITLE = "家有儿女 S01E02 02:34.16 - 03:14.60"
OUT = "家有儿女S01E02_clip_02-34_lesson"
S = [
 ('02:34.16', '你凭什么干涉我的社交', "What gives you the right to interfere in my social life?"),
 ('02:36.68', '社交', "Social life?!"),
 ('02:40.20', '你这么小的年纪', "At your age —"),
 ('02:42.08', '你懂什么叫社交', "What do you know about social life?"),
 ('02:44.08', '我是怕你犯错误', "I'm just afraid you'll make a mistake."),
 ('02:47.92', '您不犯错误', "You don't make mistakes?"),
 ('02:49.84', '那你还离婚', "Then how come you got divorced?"),
 ('02:53.32', '怎么说话的', "What kind of talk is that?!"),
 ('02:55.08', '爸爸可真生气了 我告诉你', "Dad is really furious now — let me tell you!"),
 ('03:00.60', '你干嘛那么凶啊', "Why are you being so fierce?"),
 ('03:05.76', '你从来都没有关心过我', "You have never cared about me at all."),
 ('03:12.28', '你就把我扔在爷爷家不管', "You just dumped me at grandpa's and ignored me."),
]
# (sentence_index, char_k_position) -> pinyin override
OVERRIDE = {
 (0, 2): 'gàn',   # 干 in 干涉 → gān (actually gān is correct for 干涉; but 干嘛 would be gàn)
 # 干涉 = gān shè (to interfere) — gān here, NOT gàn
 # so we override back to default: no override needed for 干涉
 (8, 1): 'kě',    # 可 tone 3 — default ok
 (11, 2): 'rēng', # 扔 — default ok
}
VOCAB = [
 ('凭什么', 'píng shén me', 'colloquial', 'What right do you have? On what basis? A strong challenge phrase. 你凭什么…= "By what right do you…?" Much more confrontational than 为什么 (why). Common in arguments between equals or when someone feels unjustly restricted. Tone: indignant.'),
 ('干涉', 'gān shè', 'HSK5', 'To interfere, meddle. 干涉 implies unwanted intrusion into someone\'s affairs. Note: 干 here is gān (1st tone), not gàn (do/work). Compare: 插手 (to stick one\'s hand in), 过问 (to inquire/involve oneself). Collocations: 干涉内政, 干涉私事.'),
 ('社交', 'shè jiāo', 'HSK5', 'Social interaction, socializing. 社交生活 = social life. Used somewhat formally here — Xiaoxue uses it deliberately to sound grown-up and push back. Compare: 交际 (social dealings, more formal/business). Modern usage: 社交媒体 (social media).'),
 ('犯错误', 'fàn cuò wù', 'HSK4', 'To make a mistake, commit an error. 犯 = to commit/violate. 犯错误 is slightly more serious than 出错 (make an error) — implies moral or behavioral failing. The parent\'s anxiety here is realistic: 犯错误 echoes political-era language of "making mistakes."'),
 ('从来都没有', 'cóng lái dōu méi yǒu', 'grammar', 'Never have, not once. 从来 = from always/ever; 都 = even/all; 没有 = have not. This triple-negation structure is emphatic: 你从来都没有关心过我 = "You have NEVER once cared about me." 过 adds the experiential aspect. Contrast: 一直没有 (continuously haven\'t).'),
 ('怎么说话的', 'zěn me shuō huà de', 'colloquial', 'What kind of way is that to talk?! A rhetorical scolding formula. The 的 at the end creates an implied judgment. Used by adults when a child says something shockingly disrespectful. Equivalent register: "Watch your mouth!" Compare: 你说什么 (what did you say? — simpler surprise).'),
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
