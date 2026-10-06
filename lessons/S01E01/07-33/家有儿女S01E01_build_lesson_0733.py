# -*- coding: utf-8 -*-
import os, html
from pypinyin import pinyin, Style

TITLE = "家有儿女 07:33.50 - 08:02.00"
OUT = "家有儿女_clip_07-33_lesson"
S = [
 ('07:33.50', '什么不会的 我对你们两个人', "What do you mean 'won't'? You two —"),
 ('07:36.00', '我一点都不信任', "I don't trust you one bit."),
 ('07:39.50', '荔枝呀', 'Lychees!'),
 ('07:40.50', '去去去 一边站着', 'Shoo, stand aside.'),
 ('07:43.50', '跟你们有什么关系呀', "What's it got to do with you?"),
 ('07:48.00', '刘星啊 你帮我看看', 'Liu Xing, have a look for me —'),
 ('07:49.50', '姐姐这屋还缺点什么呀', "what else is your sister's room missing?"),
 ('07:51.50', '一盒奶糖', 'A box of milk candy.'),
 ('07:53.50', '你想吃奶糖了吧你', "You just want some milk candy yourself, don't you."),
 ('07:57.00', '老妈 我和小雨呢 为了这次小雪来', 'Mom, Xiaoyu and I — for Xiaoxue coming —'),
 ('07:59.50', '编排了一个小节目 我们给你演演', 'put together a little show. Let us perform it for you.'),
 ('08:02.00', '行啊 来来来', 'Sure, go on, go on.'),
]
OVERRIDE = {
 (5, 7): 'kan',
 (6, 1): 'jie',
 (10, 13): 'yan',
}
VOCAB = [
 ('信任', 'xìnrèn', 'HSK4', "'To trust' (someone's character/reliability). 我对你们…不信任 = 'I have no trust in you'. Compare 相信 (to believe — what someone says)."),
 ('一点都不', 'yìdiǎn dōu bù', 'grammar', "'Not … at all': 一点(儿) + 都/也 + 不/没 + verb/adj. 我一点都不信任 = I don't trust (you) one bit. Same pattern as 一点…都没有."),
 ('荔枝', 'lìzhī', 'noun', "'Lychee' — a southern Chinese fruit, a bit of a treat in Beijing. 荔枝呀! = 'Ooh, lychees!' (the kids spotting them)."),
 ('一边站着', 'yìbiān zhànzhe', 'colloq.', "'Stand aside / out of the way'. 一边 = to one side; 着 marks staying in that position. Often with 去: 一边去! = 'Go away!'"),
 ('跟…有什么关系', 'gēn … yǒu shénme guānxi', 'grammar', "'What does it have to do with …?' — a rhetorical brush-off meaning 'none of your business'. 关系 (HSK3) = connection, relationship."),
 ('缺', 'quē', 'HSK4', "'To lack, be short of': 还缺点什么 = 'still missing something'. 缺钱 (short of money), 缺人 (short-staffed). Related: 缺点 (shortcoming) — not the same thing as 缺 + 点 here!"),
 ('盒', 'hé', 'HSK3', 'Measure word for boxes: 一盒奶糖 = a box of milk candy, 一盒饼干. Also a noun: 盒子 (box).'),
 ('…了吧你', '…le ba nǐ', 'grammar', "Teasing tag: statement + 吧 + 你 at the end = 'You do, don't you!' Repeating the subject at the end (你想吃奶糖了吧你) is very colloquial Beijing speech."),
 ('编排', 'biānpái', 'HSK6', "'To arrange, put together (a performance)': 编排节目 = choreograph/write a show. (Also, colloquially, 'to make up stories about someone'.)"),
 ('节目', 'jiémù', 'HSK3', "'Program, show, act' — TV programs, or a performance at a party. 小节目 = a little skit. Measure word 个."),
 ('演演', 'yǎnyan', 'grammar', "Reduplicated verb = 'do it a bit, have a go': 给你演演 = 'perform it for you'. Second syllable goes toneless, like 看看 (kànkan)."),
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
