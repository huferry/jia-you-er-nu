# -*- coding: utf-8 -*-
import os, html
from pypinyin import pinyin, Style

TITLE = "家有儿女 S01E02 20:46.24 - 21:08.24"
OUT = "家有儿女S01E02_clip_20-46_lesson"
S = [
 ('20:46.24', '你把你的鞋往哪儿甩呢你', "Where do you think you're flinging your shoes?"),
 ('20:49.24', '人是自由的', "People are free!"),
 ('20:50.24', '鞋也是自由的', "So are shoes!"),
 ('20:51.24', '不是 我说你也太过分了吧你', "No — I'm saying you've gone way too far!"),
 ('20:54.24', '出去玩也不跟家长说一声', "Going out to play without even telling the adults!"),
 ('20:56.24', '你看看现在都几点了', "Look at what time it is now!"),
 ('20:59.24', '我说你', "I'm talking to you!"),
 ('21:00.24', '还有你', "And you too!"),
 ('21:01.24', '你们俩的所作所为', "The behavior of you two —"),
 ('21:02.24', '都太过分了', "— has been completely out of line."),
 ('21:03.24', '你才过分呢', "You're the one who's out of line!"),
 ('21:07.24', '因为我们是向你学的', "Because we learned it from you!"),
]
# (sentence_index, char_k_position) -> pinyin override
OVERRIDE = {
 (0, 3): 'nǎr',   # 哪儿 → nǎr
 (0, 4): 'shuǎi', # 甩 → shuǎi
 (3, 3): 'tài',   # 太 → tài
 (3, 4): 'guò',   # 过 in 过分 → guò
 (4, 1): 'qù',    # 去 → qù
 (4, 5): 'jiā',   # 家 in 家长 → jiā
 (4, 6): 'zhǎng', # 长 in 家长 → zhǎng (elder/parent), not cháng
 (4, 7): 'shuō',  # 说 → shuō
 (8, 2): 'suǒ',   # 所 in 所作所为 → suǒ
 (8, 4): 'suǒ',   # 所 in 所作所为 (second 所) → suǒ
 (11, 3): 'xiàng', # 向 in 向你学 → xiàng (from/following)
}
VOCAB = [
 ('所作所为', 'suǒ zuò suǒ wéi', 'idiom', 'One\'s actions and conduct — everything one does. A formal 4-character phrase (chéngyǔ-style) used to judge someone\'s overall behavior. Slightly literary; in spoken Chinese it often signals serious reproach: 你们的所作所为让我很失望 = "I am very disappointed by everything you\'ve done."'),
 ('家长', 'jiā zhǎng', 'HSK3', 'Parent, guardian; head of a family. Note: 长 is zhǎng (elder/leader), NOT cháng (long). 跟家长说 = "tell the parents/adults." Collocations: 家长会 (parent-teacher meeting), 家长制 (patriarchal system). Distinct from 父母 (parents specifically).'),
 ('说一声', 'shuō yī shēng', 'phrase', '"Say something / give a heads-up." 跟家长说一声 = "let the parents know / just tell someone." 一声 (one sound/utterance) makes it casual and minimal — just a brief word, not a full report. Very common in family/social contexts.'),
 ('向…学', 'xiàng … xué', 'grammar', 'To learn from someone. 向你学 = "learned from you." 向 (towards/from) + person + 学 (learn). Common pattern: 向老师学, 向前辈学 (learn from teachers/seniors). The children use it here cheekily to deflect blame onto the adults.'),
 ('才…呢', 'cái … ne', 'grammar', 'Emphatic counter-accusation: "YOU\'RE the one who…!" 你才过分呢 = "YOU\'RE the one who\'s out of line!" The pattern 你才…呢 pushes the charge back at the accuser. Stress is on 才 (it\'s precisely YOU, not me). Very common in bickering among children and siblings.'),
 ('过分', 'guò fèn', 'HSK4', 'Excessive, going too far. Used twice in rapid succession here (lines 10 and 11) — once as accusation, once as rebuttal. The word becomes a verbal ping-pong ball in the argument. 太过分了 (too much) vs 你才过分 (you\'re the one who\'s out of line).'),
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
