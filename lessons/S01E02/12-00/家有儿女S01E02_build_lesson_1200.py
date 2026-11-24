# -*- coding: utf-8 -*-
import os, html
from pypinyin import pinyin, Style

TITLE = "家有儿女 S01E02 12:00.04 - 12:57.96"
OUT = "家有儿女S01E02_clip_12-00_lesson"
S = [
 ('12:00.04', '可以', "Sure."),
 ('12:02.56', '我想去爷爷家住几天', "I want to go stay at Grandpa's place for a few days."),
 ('12:04.08', '可以', "Sure."),
 ('12:06.12', '我还会把狂野男孩带到家里来的', "I'll still bring Wild Boy home too, you know."),
 ('12:08.68', '可以', "Sure."),
 ('12:10.60', '你不怕我变得很坏', "Aren't you afraid I'll turn out bad?"),
 ('12:12.20', '可以', "Sure."),
 ('12:13.76', '你怎么会变得很坏呢', "How could you possibly turn out bad?"),
 ('12:15.28', '根本不可能', "Absolutely impossible."),
 ('12:24.72', '我们退后得挺好', "We handled that retreat pretty well."),
 ('12:26.24', '就是有点累', "Just a bit exhausting."),
 ('12:29.24', '你说小雪会明白我们的苦心吗', "Do you think Xiaoxue will understand our good intentions?"),
]
# (sentence_index, char_k_position) -> pinyin override
OVERRIDE = {
 (3, 4): 'zhǎng',   # 长 in 把…带到 — actually no 长 here; placeholder removed
 (9, 2): 'tuì',     # 退 is correct, no override needed; keeping dict minimal
}
# Clean override — only real heteronyms
OVERRIDE = {
}
VOCAB = [
 ('苦心', 'kǔ xīn', 'HSK5', 'Painstaking effort, good intentions born of hardship. 苦心 implies the parents worked hard and suffered to achieve a result — here their "strategic retreat." Collocation: 一片苦心 (a whole heart of good intentions), 苦心经营 (painstakingly manage). Compare: 用心 (put in effort, more neutral).'),
 ('退后', 'tuì hòu', 'HSK4+', 'To step back, give ground. Used here as a strategy (零限制 policy) — giving the daughter total freedom to win her trust. Literal: step backward. Figurative: make concessions. Opposite: 进逼 (press forward).'),
 ('变得', 'biàn de', 'grammar', 'To become (+ adjective/state). 变得很坏 = become very bad. 得 here is a structural particle linking verb to result complement. Compare: 变成 (turn into + noun). Pattern: 变得 + adj is for gradual change of state; 变成 + noun is change of category.'),
 ('根本不可能', 'gēn běn bù kě néng', 'HSK4', 'Absolutely impossible. 根本 (from the root) intensifies negation: "not possible at all." Very common spoken intensifier: 根本不知道 (have no idea), 根本不在乎 (couldn\'t care less). Stronger than 不太可能 (unlikely) or 没可能.'),
 ('没准', 'méi zhǔn', 'colloquial', 'Maybe, perhaps — spoken register, expressing uncertainty. 没准可以 = "Could be." Softer than 可能 and more colloquial than 也许. Often implies the speaker is not fully confident but cautiously optimistic. Very common in Beijing dialect.'),
 ('可以', 'kě yǐ', 'HSK2', 'OK, fine, allowed. Here used as a comic running gag: Xiaoxue tests her parents with increasingly provocative statements and they just keep saying 可以. The repetition reveals their "zero-restriction" policy has become absurd — 可以 turns from permission into comic surrender.'),
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
