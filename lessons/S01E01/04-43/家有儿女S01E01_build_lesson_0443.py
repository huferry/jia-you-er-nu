# -*- coding: utf-8 -*-
import os, html, re, subprocess
from pypinyin import pinyin, Style

TITLE = "家有儿女 04:43.40 - 05:06.88"
OUT = "家有儿女_clip_04-43_lesson"
S = [
 ("04:43.40", "蚊子一闻", "The mosquito takes one sniff —"),
 ("04:44.60", "这儿的血甜 我来咬他吧", "\"This one's blood is sweet — I'll bite him!\""),
 ("04:48.16", "就吃你的血了 对不对", "\"So I'll just feed on your blood, right?\""),
 ("04:50.40", "快去吧 换衣服啊", "Go on now, go change your clothes."),
 ("04:51.52", "换完衣服该上学了啊", "Once you've changed, it's time for school."),
 ("04:52.88", "我不想上学 我想睡觉", "I don't want to go to school. I want to sleep."),
 ("04:55.88", "别胡说 为什么", "Don't talk nonsense. Why?"),
 ("04:57.88", "我时差还没倒过来呢", "I still haven't gotten over my jet lag."),
 ("04:59.88", "谁又在这瞎说八道啊", "Who's talking utter nonsense again?"),
 ("05:02.88", "你从美国都回来一百八十天了", "You've been back from America for a hundred and eighty days already."),
 ("05:04.88", "人八十天把地球都环游一周了", "In eighty days a person can go all the way around the globe,"),
 ("05:06.88", "你还没倒过时差来", "and you still haven't gotten over your jet lag?"),
]
OVERRIDE = {(7, 2): "chā", (7, 5): "dǎo", (7, 6): "guò", (11, 3): "dǎo", (11, 6): "chā"}
VOCAB = [
 ("闻", "wén", "HSK5", "'To smell' (verb): 闻一闻 = 'take a sniff'. Not to be confused with 嗅 (literary) or 香/臭 (adjectives for the smell itself). 蚊子一闻 = 'the moment the mosquito smells it' — 一…就… pattern implied."),
 ("换", "huàn", "HSK3", "'To change / swap'. 换衣服 = change clothes; also 换钱, 换工作, 换个方式. Different from 变 (to become) — 换 replaces one thing with another."),
 ("胡说", "húshuō", "HSK5", "'To talk nonsense'. 别胡说 is a stock scolding phrase; 胡 (recklessly) also forms 胡闹, 胡来."),
 ("时差", "shíchā", "HSK6", "'Time difference / jet lag'. 倒时差 (dǎo shíchā) is the spoken phrase for adjusting to jet lag; 倒 here means 'to shift/switch', hence 倒过来 'switch over'. Reading dǎo, not dào."),
 ("瞎说八道", "xiā shuō bā dào", "idiom", "'To talk utter nonsense'. 瞎 (blind, aimlessly) + 说 + 八道 (filler intensifier). More emphatic than 胡说; usually said in irritation."),
 ("环游", "huányóu", "HSK6", "'To travel around (the world)'. 环游世界 / 环游地球. Formal-ish verb; the joke here alludes to a famous 'around the world in 80 days' story."),
 ("地球", "dìqiú", "HSK4", "'The Earth, the globe'. 地球村 = global village; 保护地球 = protect the Earth. Compare 世界 (world, in the human/political sense)."),
 ("一百八十天了", "yì bǎi bā shí tiān le", "grammar", "都…了 pattern: 你从美国都回来一百八十天了 = 'you've already been back for 180 days'. 都 + duration + 了 stresses that a lot of time has passed, hinting at impatience."),
 ("还没…", "hái méi …", "grammar", "'Still hasn't yet': 你还没倒过时差来. 还没 + verb + (complement) signals an expected event hasn't happened; 过来 marks 'switching back to normal'."),
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
    if i == 6: body.append('<div style="page-break-before:always"></div>')
    body.append(sent_html(i, ts, t, en))
body.append('<h2 style="page-break-before:always">HSK 3+ Vocabulary</h2><div class="sub">Words from the text above that are HSK level 3 or higher (levels approximate).</div>')
body.append('<table class="vt"><tr><th>Word</th><th>Pinyin</th><th>Explanation</th></tr>')
for w, p, lv, ex in VOCAB:
    body.append(f'<tr><td><span class="vh">{w}</span><br>{lv}</td><td class="vp">{p}</td><td>{html.escape(ex)}</td></tr>')
body.append('</table>')
body.append('<div class="txt"><h2>Text Only</h2>' + "".join(sent_html(i, ts, t, en, plain=True) for i, (ts, t, en) in enumerate(S)) + '</div>')
open(os.path.join(os.path.dirname(os.path.abspath(__file__)), OUT + ".html"), "w", encoding="utf-8").write(f'<!doctype html><html><head><meta charset="utf-8"><title>{TITLE}</title><style>{css}</style></head><body>{"".join(body)}</body></html>')
