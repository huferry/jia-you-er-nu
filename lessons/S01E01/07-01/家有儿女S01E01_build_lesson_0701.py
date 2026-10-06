# -*- coding: utf-8 -*-
import os, html
from pypinyin import pinyin, Style

TITLE = "家有儿女 07:01.50 - 07:31.50"
OUT = "家有儿女_clip_07-01_lesson"
S = [
 ('07:01.50', '我特高兴', "I'm so happy."),
 ('07:02.00', '那是 二十一世纪的城市女性', 'Of course — for a 21st-century city woman,'),
 ('07:05.50', '一个人要有仨孩子的概率', 'the odds of one person having three kids'),
 ('07:07.50', '跟中头奖差不多', 'are about the same as hitting the jackpot.'),
 ('07:14.50', '我还真有点中头奖的感觉', "I really do feel a bit like I've hit the jackpot."),
 ('07:18.00', '都没这么欢迎过我', "Nobody's ever welcomed me like this."),
 ('07:20.00', '哎呀 她的床比我的舒服多了', 'Wow, her bed is way more comfortable than mine.'),
 ('07:22.50', '对 太舒服了', 'Yeah, so comfy.'),
 ('07:25.50', '干吗呢你们俩', 'What are you two up to?'),
 ('07:26.50', '去去去 你把姐姐床都给弄乱了', "Shoo! You've gone and messed up your sister's bed."),
 ('07:31.00', '哎呀 不会', "Aw, we won't (do anything)."),
 ('07:31.50', '我也不会的', "I won't either."),
]
OVERRIDE = {
 (3, 1): 'zhòng',
 (4, 5): 'zhòng',
 (6, 1): 'ya',
 (6, 9): 'fu',
 (7, 3): 'fu',
 (9, 6): 'jie',
 (10, 1): 'ya',
}
VOCAB = [
 ('那是', 'nà shì', 'colloq.', "'Of course! / Naturally!' — a spoken interjection of agreement, often a bit smug: 'well, obviously'. Not the literal 'that is' here."),
 ('世纪', 'shìjì', 'HSK4', "'Century'. 二十一世纪 = 21st century. Compare 年代 (decade, e.g. 八十年代 = the '80s)."),
 ('城市', 'chéngshì', 'HSK3', "'City'. 城市女性 = urban women. Opposite: 农村 (countryside)."),
 ('仨', 'sā', 'colloq.', "'Three (of something)' = 三个, northern colloquial. Like 俩 (liǎ = 两个), it already contains the measure word, so never say ×仨个."),
 ('概率', 'gàilǜ', 'HSK6', "'Probability, odds'. 率 is lǜ here (as in 效率 xiàolǜ), not shuài. A semi-technical word used humorously in this line."),
 ('中头奖', 'zhòng tóujiǎng', 'idiom', "'Win the top prize / hit the jackpot'. 中 is 4th tone (zhòng) = to hit a target, as in 中奖 (win a prize), 猜中 (guess right) — not zhōng (middle)."),
 ('差不多', 'chàbuduō', 'HSK4', "'About the same, almost'. A跟B差不多 = A is about the same as B. 不 is light/neutral here."),
 ('比…多了', 'bǐ … duō le', 'grammar', "Comparison 'much more…': A比B + adj + 多了. 她的床比我的舒服多了 = her bed is much more comfortable than mine. You can't use 很 here (×比我的很舒服)."),
 ('舒服', 'shūfu', 'HSK3', "'Comfortable' — 服 is toneless (fu). Also 'feeling well': 我不舒服 = I'm not feeling well."),
 ('弄乱', 'nòngluàn', 'HSK5 (弄)', "'To mess up' — 弄 (do/make, vague all-purpose verb) + 乱 (messy) as result. Pattern 把X(都)给弄乱了 = 'went and messed X up' (给 adds a sense of unwanted outcome)."),
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
