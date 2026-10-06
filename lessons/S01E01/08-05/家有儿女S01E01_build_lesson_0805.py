# -*- coding: utf-8 -*-
import os, html
from pypinyin import pinyin, Style

TITLE = "家有儿女 08:05.00 - 08:27.50"
OUT = "家有儿女_clip_08-05_lesson"
S = [
 ('08:05.00', '预备开始', 'Ready — go!'),
 ('08:06.40', '小雪 小雪 小雪', 'Xiaoxue, Xiaoxue, Xiaoxue!'),
 ('08:08.16', '欢迎 欢迎 欢迎', 'Welcome, welcome, welcome!'),
 ('08:11.60', '停停停', 'Stop, stop, stop!'),
 ('08:15.00', '就你们俩这么闹', 'The racket you two are making —'),
 ('08:16.50', '非得把姐姐吓着不可', "you're bound to scare your sister half to death."),
 ('08:18.50', '而且你们这节目我告诉你啊', "And this show of yours, I'm telling you —"),
 ('08:19.50', '吃完饭不许演啊', 'no performing it right after dinner,'),
 ('08:21.50', '非得阑尾炎不行', "or somebody's sure to get appendicitis."),
 ('08:24.00', '妈 我饿了', "Mom, I'm hungry."),
 ('08:25.44', '妈 我也饿了', "Mom, I'm hungry too."),
 ('08:27.50', '妈妈准备了一桌丰盛的晚餐', "Mom's made a whole table of delicious food,"),
]
OVERRIDE = {
 (5, 4): 'jie',
 (5, 6): 'zháo',
 (11, 1): 'ma',
}
VOCAB = [
 ('预备', 'yùbèi', 'HSK6', "'Get ready': 预备 — 开始! = 'Ready — go!' (the classic start command, like 预备 — 跑!). Close to 准备 but sounds more like a formal countdown."),
 ('闹', 'nào', 'HSK4', "'To make a racket, horse around'. 这么闹 = carry on like this. Also 闹钟 (alarm clock), 热闹 (lively)."),
 ('非得…不可', 'fēiděi … bùkě', 'grammar', "'Will definitely / is bound to…' (an inevitable, usually bad result): 非得把姐姐吓着不可 = it's bound to scare her. The next line has the variant 非得…不行. 得 is děi."),
 ('吓着', 'xiàzháo', 'HSK5 (吓)', "'To give someone a fright'. 着 is zháo here — a result complement meaning 'actually affected' (also 睡着 shuìzháo, 找着). 把X吓着 = scare X."),
 ('而且', 'érqiě', 'HSK3', "'And also, moreover' — adds a further point. Often paired: 不但…而且… (not only… but also…)."),
 ('不许', 'bùxǔ', 'HSK4', "'Not allowed to' — a blunt parental ban: 吃完饭不许演. Stronger than 不要 or 别."),
 ('阑尾炎', 'lánwěiyán', 'noun', "'Appendicitis'. Old folk belief: running and jumping right after a meal can bring it on — that's the joke. 炎 = inflammation (as in 肺炎 pneumonia)."),
 ('丰盛', 'fēngshèng', 'HSK6', "'Rich, sumptuous' — almost always about a meal: 丰盛的晚餐/午餐. Compare 丰富 (abundant, rich — of content, experience, etc.)."),
 ('晚餐', 'wǎncān', 'HSK4', "'Dinner' — slightly more formal than 晚饭. 一桌…晚餐 = a whole tableful of dinner (桌 used as a measure word)."),
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
