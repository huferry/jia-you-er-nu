# -*- coding: utf-8 -*-
import os, html
from pypinyin import pinyin, Style

TITLE = "家有儿女 S01E02 09:03.00 - 09:41.88"
OUT = "家有儿女S01E02_clip_09-03_lesson"
S = [
 ('09:03.00', '叔叔阿姨 我演得像吗', "Uncle, Auntie — was my acting convincing?"),
 ('09:05.64', '不像', "Not at all."),
 ('09:07.04', '我早就看出来了', "I saw through it right from the start."),
 ('09:08.92', '小雪怎么可能早恋呢', "How could Xia Xue possibly be in an early romance?"),
 ('09:15.24', '千万别把这事告诉夏雪啊', "Whatever you do, don't tell Xia Xue about this, okay?"),
 ('09:17.80', '不然她该不给我讲题了', "Otherwise she won't explain the problem to me anymore."),
 ('09:21.80', '我先走了', "I'll head off now."),
 ('09:28.28', '我就说嘛', "I knew it, didn't I say so?"),
 ('09:29.08', '小雪怎么可能早恋', "How could Xia Xue possibly be in a romance?"),
 ('09:31.08', '我早就知道了', "I knew all along."),
 ('09:33.84', '你什么时候早就知道的', "Since when did you 'know all along'?"),
 ('09:40.20', '我还说过你没听见', "I did say so — you just didn't hear me."),
]
# (sentence_index, char_k_position) -> pinyin override
OVERRIDE = {
 (0, 0): 'shū',   # 叔 in 叔叔 → shū
 (0, 2): 'ā',     # 阿 in 阿姨 → ā
 (3, 2): 'zěn',   # 怎 in 怎么 → zěn
 (3, 4): 'kě',    # 可 in 可能 → kě
 (3, 5): 'néng',  # 能 → néng
 (3, 6): 'zǎo',   # 早 in 早恋 → zǎo
 (3, 7): 'liàn',  # 恋 → liàn
 (4, 0): 'qiān',  # 千 in 千万 → qiān
 (4, 5): 'zhè',   # 这 → zhè
 (5, 1): 'rán',   # 然 in 不然 → rán
 (5, 3): 'gāi',   # 该 in 该…了 → gāi (would, then)
 (7, 2): 'shuō',  # 说 → shuō
 (8, 2): 'zěn',   # 怎
 (8, 4): 'kě',    # 可
 (8, 6): 'zǎo',   # 早
 (8, 7): 'liàn',  # 恋
 (10, 1): 'shén', # 什 in 什么 → shén
 (10, 5): 'zǎo',  # 早
}
VOCAB = [
 ('叔叔阿姨', 'shū shu ā yí', 'HSK3', 'Uncle and Auntie — the standard respectful address for adult friends\' parents or neighbors, regardless of actual relation. Children in China use this for any adult couple. Here the boy uses it charmingly to defuse the awkward situation with the parents.'),
 ('早就', 'zǎo jiù', 'HSK4', '"Long ago; have… for a long time already." 早就知道了 = knew long ago. 早 (early) + 就 (already/then) = even earlier than expected. The phrase implies the speaker is ahead of events. Used to show one was not deceived. Compare: 已经 (already, neutral timing).'),
 ('看出来', 'kàn chū lái', 'HSK4', 'To see through; to figure out from observation. Directional complement 出来 = "out from observation." 我早就看出来了 = I saw through it long ago. Compare: 看出 (see/detect, without the 来 that implies the realization "surfacing").'),
 ('怎么可能', 'zěn me kě néng', 'colloquial', '"How could it possibly be?" — a rhetorical exclamation of disbelief or denial. 怎么 (how) + 可能 (possible). Very common in spoken Chinese. Compare: 不可能 (impossible, a flat denial); 怎么可能 is more incredulous and conversational.'),
 ('不然', 'bù rán', 'HSK4', '"Otherwise; if not." 不然她该不给我讲题了 = otherwise she won\'t explain problems to me anymore. Functions as a connective adverb. Near-synonym: 否则 (otherwise, more formal/written). Very common in spoken Chinese for conditional warnings.'),
 ('我就说嘛', 'wǒ jiù shuō ma', 'colloquial', '"I told you so; didn\'t I say so?" — a smug retrospective claim. 就 here means "precisely/exactly." 嘛 is a particle asserting something is obvious. The father uses this to cover up that he actually did NOT know, then immediately gets called out by the mother asking "since when?"'),
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
