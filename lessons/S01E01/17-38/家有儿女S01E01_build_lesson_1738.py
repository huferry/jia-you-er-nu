# -*- coding: utf-8 -*-
import os, html
from pypinyin import pinyin, Style

TITLE = "家有儿女 17:38.00 - 17:57.00"
OUT = "家有儿女S01E01_clip_17-38_lesson"
S = [
 ('17:38.00', '我知道', "I know."),
 ('17:39.00', '你已经做得很好了', "You've already done very well."),
 ('17:41.00', '我是说', "What I mean is—"),
 ('17:42.00', '咱们肯定能做得更好', "We can definitely do even better."),
 ('17:45.00', '爱心 耐心', "Love and patience."),
 ('17:46.00', '宽大为怀嘛', "Be magnanimous, right?"),
 ('17:49.00', '行行行', "Okay, okay, okay."),
 ('17:50.00', '你先出去吧', "You go out first."),
 ('17:51.00', '我给她收拾收拾', "I'll tidy up for her."),
 ('17:52.00', '我怕你啊', "You scare me, you know that?"),
 ('17:54.00', '别假的', "Don't be fake about it."),
 ('17:57.00', '娶了你是我最大的福分', "Marrying you is my greatest blessing."),
]
# (sentence_index, char_k_position) -> pinyin override
OVERRIDE = {
 # 为 in "宽大为怀嘛": 为 = wéi (to be/act), not wèi (for the sake of)
 # 宽(0)大(1)为(2)怀(3)嘛(4)
 (5, 2): 'wéi',
 # 行行行: all three = xíng (OK/alright), not háng (trade/row)
 (6, 0): 'xíng',
 (6, 1): 'xíng',
 (6, 2): 'xíng',
 # 分 in "娶了你是我最大的福分": 分 = fèn (lot/blessing), not fēn (minute/divide)
 # 娶(0)了(1)你(2)是(3)我(4)最(5)大(6)的(7)福(8)分(9)
 (11, 9): 'fèn',
}
VOCAB = [
 ('耐心', 'nài xīn', 'HSK3', 'Patience (noun); patient (adjective). 爱心耐心 = love and patience — 夏东海\'s mantra for blending the family. 耐心 as adj.: 要耐心 (you need to be patient). As noun: 有耐心 (to have patience), 失去耐心 (lose patience). The repetition of 耐心 at 19:13 echoes this earlier scene and ties the episode together.'),
 ('宽大为怀', 'kuān dà wéi huái', 'HSK6/idiom', 'To be magnanimous, to treat others with generosity and forgiveness. Chengyu: 宽大 = broad/lenient, 为 = to be (wéi), 怀 = heart/mind. Used here as 夏东海\'s parenting philosophy — be big-hearted toward Xiaoxue. Note 为 is wéi (linking verb "to be"), not wèi (for the sake of).'),
 ('收拾', 'shōu shi', 'HSK4', 'To tidy up, to put in order; also colloquially: to deal with someone / to fix someone. 我给她收拾收拾 = I\'ll tidy up (her room) for her. The reduplication 收拾收拾 softens and casualizes the action. Watch the double meaning: in other contexts 收拾你 = I\'ll sort you out (a threat). Here it\'s gentle.'),
 ('福分', 'fú fen', 'HSK5+', 'One\'s lot of blessings; good fortune (as predestined). 娶了你是我最大的福分 = marrying you is my greatest blessing. 分 (fèn) here = one\'s allotted portion/fate, NOT fēn (minute). Compare 福气 (good fortune, luck) — similar but 福分 has a stronger sense of destiny/fate. A heartfelt, slightly literary expression.'),
 ('肯定', 'kěn dìng', 'HSK4', 'Definitely, certainly (adverb); to affirm (verb); affirmative (adj.). 咱们肯定能做得更好 = we can definitely do even better. As a verb: 我肯定这件事 = I confirm this matter. Very common spoken intensifier. Compare 一定 (yīdìng) — also "definitely/must", but 肯定 is more conversational and confident.'),
 ('做得', 'zuò de', 'grammar', 'Degree complement with 得. 做得很好 = did it very well; 做得更好 = do it even better. Pattern: V + 得 + degree. 得 here is a complement marker (not 的 or 地). Contrast: 做好 (accomplish it / do it well — result), vs 做得好 (do it well — manner/degree). Very productive pattern: 说得清楚, 跑得快, 睡得香.'),
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
