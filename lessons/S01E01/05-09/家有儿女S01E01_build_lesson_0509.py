# -*- coding: utf-8 -*-
import os, html, re, subprocess
from pypinyin import pinyin, Style

TITLE = "家有儿女 05:09.00 - 05:37.00"
OUT = "家有儿女_clip_05-09_lesson"
S = [
 ("05:09.00", "我在美国都呆了七年了", "I've lived in America for seven whole years."),
 ("05:11.50", "对呀 人家七年就得倒七年的时差", "Right — seven years means seven years to get over your jet lag."),
 ("05:15.50", "爸爸什么都不懂", "Dad, you don't understand anything."),
 ("05:18.50", "老妈 老爸 老弟 Good morning", "Mom, Dad, little brother — Good morning."),
 ("05:20.50", "Good morning 刘星", "Good morning, Liu Xing."),
 ("05:21.50", "你以后少在这儿 Good morning", "Don't you \"good morning\" me around here anymore."),
 ("05:23.50", "记住了 以后当着弟弟不许老说英文", "Remember — from now on, no more speaking English in front of your little brother."),
 ("05:27.00", "就得说纯正的中文 听见没有", "You have to speak proper Chinese — do you hear me?"),
 ("05:29.00", "收到 不过我告诉你们一件事", "Got it. But let me tell you something."),
 ("05:32.00", "刚才我看见一个八条腿的家伙", "Just now I saw a thing with eight legs."),
 ("05:35.00", "横着它就进沙发底下去了", "It scuttled sideways and went right under the sofa."),
 ("05:37.00", "妈 加利福尼亚的大蜘蛛", "Mom, it's a giant California spider."),
]
OVERRIDE = {
 (1, 7): "děi", (1, 8): "dǎo", (1, 13): "chā",
 (5, 3): "shǎo",
 (6, 6): "zhe",
 (7, 1): "děi",
 (9, 12): "huo",
 (10, 1): "zhe", (10, 8): "xia",
}
VOCAB = [
 ("纯正", "chúnzhèng", "HSK6", "'Pure / authentic' (of language, flavor, etc.): 纯正的中文 = 'proper, unaccented Chinese'. Stronger than 标准 (standard) — 纯正 stresses freedom from mixing-in of other influences."),
 ("记住", "jìzhù", "HSK4", "'To remember, keep in mind' — 住 here is a resultative complement meaning 'firmly, securely'. 记住了 is a stock parental command, like 'got that?'"),
 ("不许", "bùxǔ", "HSK4", "'Not allowed to': blunter and more parental than 不可以/不能. 不许 + verb, often in commands: 不许哭, 不许说话."),
 ("当着", "dāngzhe", "grammar", "'In front of / to someone's face': 当着弟弟 = 'in front of little brother'. Opposite of 背着 (behind someone's back, without them knowing)."),
 ("听见", "tīngjiàn", "HSK3", "'To hear' — 见 is a resultative complement marking that the perception actually registered. Compare plain 听 (to listen), which doesn't guarantee anything was heard."),
 ("收到", "shōudào", "HSK4", "Literally 'received' (a signal, letter, etc.); used here colloquially as 'Roger / got it', echoing military radio-speak — similar in feel to 明白了."),
 ("家伙", "jiāhuo", "HSK5", "'Guy, fellow, thing' — casual and slightly dismissive; can refer to people, animals, or objects (as here, a bug). 伙 is toneless (neutral tone), not huǒ."),
 ("横着", "héngzhe", "grammar", "'Sideways, crosswise' — 横 (horizontal) + 着 used adverbially to describe the manner of motion. Compare 竖着 (vertically/lengthwise)."),
 ("底下", "dǐxia", "HSK3", "'Underneath, below' — colloquial equivalent of the more formal 下面. 下 is toneless here (xia, not xià): 沙发底下 = 'under the sofa'."),
]

def tokenize(text):
    tokens, i = [], 0
    while i < len(text):
        ch = text[i]
        if ch == " ":
            tokens.append((" ", "gap")); i += 1; continue
        if ch.isascii() and ch.isalpha():
            j = i
            while j < len(text) and text[j].isascii() and text[j].isalpha():
                j += 1
            tokens.append((text[i:j], "ascii")); i = j; continue
        tokens.append((ch, "han")); i += 1
    return tokens

def tone_of(p):
    for ch in p:
        if ch in "āēīōūǖ": return 1
        if ch in "áéíóúǘ": return 2
        if ch in "ǎěǐǒǔǚ": return 3
        if ch in "àèìòùǜ": return 4
    return 0

def sent_chars(i, text):
    tokens = tokenize(text)
    han_chars = [c for c, k in tokens if k == "han"]
    py = pinyin("".join(han_chars), style=Style.TONE, heteronym=False)
    out, k = [], 0
    for c, kind in tokens:
        if kind == "gap":
            out.append((None, None, "gap")); continue
        if kind == "ascii":
            out.append((c, None, "ascii")); continue
        p = OVERRIDE.get((i, k), py[k][0]); k += 1
        out.append((c, p, "han"))
    real = [j for j, (c, p, kind) in enumerate(out) if kind == "han"]
    for a, j in enumerate(real[:-1]):
        c, p, kind = out[j]
        if c == "不" and tone_of(out[real[a+1]][1]) == 4:
            out[j] = (c, "bú", "han")
    return out

def box(p):
    t = tone_of(p); return {2: "t2", 3: "t3", 4: "t4"}.get(t, "t0")

def sent_html(i, ts, text, en, plain=False):
    if plain:
        return f'<div class="pl">{html.escape(text.replace(" ", "　"))}</div>'
    cells = []
    for c, p, kind in sent_chars(i, text):
        if kind == "gap":
            cells.append('<span class="gap"></span>'); continue
        if kind == "ascii":
            cells.append(f'<span class="c"><span class="py"></span><span class="hz t0 en-word">{html.escape(c)}</span></span>'); continue
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
.en-word{font-family:"Helvetica Neue",Arial,sans-serif;font-size:15pt}
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
