# -*- coding: utf-8 -*-
import os, html
from pypinyin import pinyin, Style

TITLE = "家有儿女 17:12.00 - 17:35.00"
OUT = "家有儿女S01E01_clip_17-12_lesson"
S = [
 ('17:12.00', '起码她没跑回爷爷家去', "At least she didn't run back to grandpa's."),
 ('17:16.00', '跑回爷爷家', "Run back to grandpa's—"),
 ('17:17.00', '凭什么呀', "On what grounds?!"),
 ('17:18.00', '我又没招她', "It's not like I did anything to her."),
 ('17:21.00', '这孩子是怕受委屈', "This kid is afraid of being wronged."),
 ('17:23.00', '先发制人', "She strikes first to gain the upper hand."),
 ('17:26.00', '这么多年来', "All these years—"),
 ('17:27.00', '我确实也没怎么管她', "I really haven't looked after her much."),
 ('17:29.00', '孩子挺可怜的', "The poor kid."),
 ('17:30.00', '又刚来', "And she just got here."),
 ('17:31.00', '咱多给她点时间', "Let's give her a little more time."),
 ('17:35.00', '谁招她了', "Who did anything to her?"),
]
# (sentence_index, char_k_position) -> pinyin override
OVERRIDE = {
 # 爷爷: pypinyin gives yé yé correctly; no override needed
 # 给 in "咱多给她点时间": 给 = gěi (give), pypinyin should handle correctly
}
VOCAB = [
 ('起码', 'qǐ mǎ', 'HSK4', 'At least, at the minimum. 起码她没跑回爷爷家去 = at least she didn\'t run off to grandpa\'s. Useful for drawing a minimal positive conclusion from a bad situation. Compare 至少 (zhì shǎo) — same meaning, slightly more formal. 起码 is very natural in spoken Mandarin.'),
 ('凭什么', 'píng shén me', 'colloquial', 'On what grounds? Why should (I/she/he)? Expresses indignation — the speaker finds something unjustified. 凭 = based on, relying on. 凭什么呀 = what right does she have?! / why on earth would she?! Very common in spoken Chinese to push back against something you feel is unwarranted.'),
 ('委屈', 'wěi qu', 'HSK5', 'To feel wronged, aggrieved; a grievance. 受委屈 = to suffer a grievance / to be wronged. 这孩子是怕受委屈 = this child is afraid of being hurt/slighted. As a verb: 委屈你了 = I\'ve put you in a difficult position / sorry for making things hard for you. Very common in family and emotional contexts.'),
 ('先发制人', 'xiān fā zhì rén', 'HSK6/idiom', 'Strike first to gain the upper hand; preemptive action. Chengyu: 先 = first, 发 = launch, 制 = control, 人 = others. Originally a military/strategy term. Here 夏东海 uses it to psychologically explain Xiaoxue\'s hostile behavior: she attacks first so she can\'t be hurt first.'),
 ('管', 'guǎn', 'HSK3', 'To look after, to be in charge of, to manage, to care for. 没怎么管她 = didn\'t really look after her / didn\'t manage her well. 管 has a range: 管孩子 (discipline/raise a child), 管事 (handle affairs), 不管 (regardless of / to not care). Here carries a note of parental guilt.'),
 ('可怜', 'kě lián', 'HSK4', 'Pitiful, poor (evoking sympathy). 孩子挺可怜的 = the kid is quite pitiful / the poor thing. 挺…的 is a mild intensifier: pretty, rather. 可怜 can be used sympathetically (poor child) or condescendingly. Here 夏东海 says it with genuine empathy about Xiaoxue\'s difficult situation growing up without close parental oversight.'),
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
