# -*- coding: utf-8 -*-
import os, html
from pypinyin import pinyin, Style

TITLE = "家有儿女 S01E02 12:53.32 - 13:47.24"
OUT = "家有儿女S01E02_clip_12-53_lesson"
S = [
 ('12:53.32', '那你们凭什么惩罚我呀', "Then what gives you the right to punish me?"),
 ('12:56.00', '我们凭什么不惩罚你呀', "What gives us reason NOT to punish you?"),
 ('13:00.08', '天理何在呀', "Where is the justice in this?!"),
 ('13:02.56', '你们凭什么惩罚我呀', "What right do you have to punish me?!"),
 ('13:05.40', '我们凭什么这么累呀', "What did we do to deserve being this exhausted?"),
 ('13:22.08', '她能成为我们最好的老师', "She could become our best teacher."),
 ('13:32.60', '就是相声相声的', "It's just like a crosstalk act."),
 ('13:37.24', '四十八页三到十六号', "Page forty-eight, lines three to sixteen."),
 ('13:40.00', '是啊', "That's right."),
 ('13:41.16', '那快去吧', "Then go ahead quickly."),
 ('13:42.66', '我给你们弄点水果', "I'll get you some fruit."),
 ('13:43.86', '待会给你们送进去', "I'll bring it in for you in a bit."),
]
# (sentence_index, char_k_position) -> pinyin override
OVERRIDE = {
 (2, 0): 'tiān',    # 天理何在 — 天 is correct tian1; no override needed
 (11, 0): 'dāi',   # 待 in 待会 → dāi (hang around/wait a bit), not dài
}
VOCAB = [
 ('凭什么', 'píng shén me', 'HSK4', 'On what basis? What right do you have? A sharp rhetorical challenge. 凭 = relying on, based on. 凭什么 = "based on what?" Implies the speaker finds the action unjustified. Very confrontational in tone — here used as a running joke with both sides asking it simultaneously. Compare: 有什么资格 (what qualification do you have).'),
 ('惩罚', 'chéng fá', 'HSK4', 'To punish; punishment. 惩 = penalize, 罚 = fine/penalize. Collocations: 受到惩罚 (receive punishment), 惩罚机制 (punishment mechanism). Here the whole family debates who deserves punishment, culminating in a logical standoff where nobody can justify anything.'),
 ('天理何在', 'tiān lǐ hé zài', 'idiom', 'Where is heaven\'s justice? A set phrase expressing moral outrage at an injustice. 天理 = natural moral order; 何在 = where is it (literary). Formal/dramatic register — used here by Xiaoyu for comic effect since his grievance is trivial. Compare: 说不过去 (can\'t justify this).'),
 ('相声', 'xiàng sheng', 'HSK5', 'Crosstalk comedy — a traditional Chinese two-person comedic dialogue art form (逗哏 sets up jokes, 捧哏 feeds lines). Here the adults compare their circular argument to a crosstalk routine. Collocations: 说相声 (perform crosstalk), 相声演员 (crosstalk performer). Cultural note: a quintessential Beijing entertainment form.'),
 ('待会', 'dāi huì', 'colloquial', 'In a little while, in a moment. Spoken contraction of 等一会儿. Note the pronunciation: 待 → dāi (not dài). Very common in Northern Chinese speech. Compare: 一会儿 (a moment), 过一会 (after a bit). Used here by the warm stepmother offering to bring fruit — a small but telling detail of her nurturing character.'),
 ('弄', 'nòng', 'HSK3', 'To get, fix up, deal with — a highly versatile colloquial verb. 弄点水果 = get/prepare some fruit. 弄 replaces more specific verbs (拿, 准备, 做) in casual speech. Other uses: 弄清楚 (sort out), 弄坏 (break), 弄错 (get wrong). One of the most flexible verbs in spoken Mandarin.'),
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
