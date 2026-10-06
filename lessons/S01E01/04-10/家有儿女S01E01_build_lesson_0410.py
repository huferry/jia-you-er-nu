# -*- coding: utf-8 -*-
import os, html, re, subprocess
from pypinyin import pinyin, Style

TITLE = "家有儿女 04:10.28 - 04:41.32"
OUT = "家有儿女_clip_04-10_lesson"
S = [
 ("04:10.28", "妈 我的手被虫子给咬了", "Mom, my hand got bitten by a bug!"),
 ("04:16.48", "哟 怎么回事呀", "Oh, what happened?"),
 ("04:18.68", "蚊子咬的吧 妈给挠挠啊", "A mosquito bite, probably. Let Mom scratch it for you."),
 ("04:21.88", "可怜了", "Poor thing."),
 ("04:23.12", "为什么蚊子只咬我不咬刘星", "Why do mosquitoes only bite me and not Liu Xing?"),
 ("04:25.56", "是不是这不是我的家啊", "Is it because this isn't my home?"),
 ("04:27.80", "别胡说 这怎么不是你的家呀", "Don't talk nonsense — how could this not be your home?"),
 ("04:30.16", "这就是你的家啊", "This is your home."),
 ("04:31.60", "你看爸爸妈妈不都在呢吗 对不对", "Look, Mom and Dad are both right here, aren't we? Right?"),
 ("04:35.68", "你知道为什么蚊子咬你不咬刘星吗", "Do you know why mosquitoes bite you and not Liu Xing?"),
 ("04:38.60", "因为你的血呀是甜的", "Because your blood is sweet."),
 ("04:41.32", "刘星的血呀是臭的", "Liu Xing's blood is stinky."),
]
# (sentence_index, char_position) -> pinyin override
OVERRIDE = {}
VOCAB = [
 ("被", "bèi", "HSK3", "Passive marker: 我的手被虫子咬了 = 'my hand was bitten by a bug'. Pattern: Receiver + 被 + (Agent) + Verb + result. Here 给 is added before the verb for colloquial emphasis (被…给咬了)."),
 ("蚊子", "wénzi", "HSK6", "'Mosquito'. Common collocations: 蚊子叮 / 被蚊子咬. Note 叮 (dīng) is the usual verb in writing; 咬 is the everyday spoken choice."),
 ("挠", "náo", "beyond HSK", "'To scratch (an itch) lightly'. 挠痒痒 = scratch an itch. Not the same as 抓 (grab/claw) — 挠 is gentle and soothing, which is why a parent says 给挠挠."),
 ("可怜", "kělián", "HSK5", "'Pitiful, poor thing'. As a sympathetic exclamation, 可怜了 / 真可怜 comforts a child. Can also mean 'to pity' as a verb: 可怜他."),
 ("胡说", "húshuō", "HSK5", "'To talk nonsense'. 别胡说 is a stock scolding phrase; 胡 (recklessly) + verb forms 胡说八道, 胡闹, 胡来."),
 ("不都…吗", "bù dōu … ma", "grammar", "Rhetorical question: 爸爸妈妈不都在呢吗 = 'aren't Mom and Dad both here?' Using 不 + 都 + 吗 expects a 'yes' and reassures. 呢 adds a gentle, explanatory tone."),
 ("甜", "tián", "HSK4", "'Sweet'. Used for taste (甜的血), also figuratively: 嘴甜 'sweet-talking', 笑得很甜 'a sweet smile'. Opposite: 苦."),
 ("臭", "chòu", "HSK5", "'Stinky, smelly'. Opposite of 香 (fragrant). Also figurative: 臭脾气 'bad temper'. Here it's the playful counterpart to 甜."),
 ("血", "xuè", "HSK5", "'Blood'. Formal reading xuè; spoken Mandarin (esp. Beijing) often says xiě, e.g. 流血 liú xiě. Both accepted."),
 ("只…不…", "zhǐ … bù …", "grammar", "'Only (does A), not (B)': 蚊子只咬我不咬刘星. 只 limits the action to one target, then 不 contrasts with the excluded one."),
]

def strip(s): return s
def tone_of(p):
    for ch in p:
        if ch in "āēīōūǖ": return 1
        if ch in "áéíóúǘ": return 2
        if ch in "ǎěǐǒǔǚ": return 3
        if ch in "àèìòùǜ": return 4
    return 0
def retone_bu(p):
    return p.replace("ù", "ú")  # bù -> bú
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
