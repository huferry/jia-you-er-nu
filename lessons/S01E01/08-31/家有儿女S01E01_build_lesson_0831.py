# -*- coding: utf-8 -*-
import os, html
from pypinyin import pinyin, Style

TITLE = "家有儿女 08:31.50 - 09:21.50"
OUT = "家有儿女_clip_08-31_lesson"
S = [
 ('08:31.50', '但是得等姐姐来了以后才能吃', "but we have to wait till your sister's here before we eat."),
 ('08:34.50', '现在不能吃', 'No eating yet.'),
 ('08:36.00', '小雪姐姐我好想啊', 'Sister Xiaoxue, I miss you so~'),
 ('08:39.20', '我也好想你啊姐姐', 'I miss you so much too, sister~'),
 ('08:41.40', '你快回来 别让我肚子叫起来', "Hurry back, don't let my tummy start to rumble~"),
 ('09:05.50', '怎么还不回来呀 会不会出什么事呀', "Why aren't they back yet? Could something have happened?"),
 ('09:10.00', '他们下馆子去了吧 要不咱们先吃吧', "They've probably gone out to eat. Why don't we just start?"),
 ('09:12.50', '凉了都', "It's all getting cold."),
 ('09:14.00', '去去去 这不可能', 'Oh, go on — no way.'),
 ('09:16.40', '要是他们半道上饿得受不了了呢', 'What if they got too hungry to bear on the way?'),
 ('09:19.40', '就像我们俩似的', 'Just like the two of us.'),
 ('09:21.50', '你们俩谁饿得受不了了', "Which of you two can't bear it?"),
]
OVERRIDE = {
 (0, 2): 'děi',
 (0, 5): 'jie',
 (2, 3): 'jie',
 (3, 7): 'jie',
 (4, 7): 'dù',
 (9, 8): 'de',
 (11, 5): 'de',
}
VOCAB = [
 ('等…以后才…', 'děng … yǐhòu cái …', 'grammar', "'Not until … can …': 得等姐姐来了以后才能吃 = we can only eat once she arrives. 才 marks 'only then (and later than you'd like)'. 得 = děi (must)."),
 ('肚子', 'dùzi', 'HSK4', "'Belly, tummy' (dù, 4th tone). 肚子叫 = stomach rumbling; 肚子疼 = stomachache. Careful: dǔzi (3rd tone) means tripe (food)! The line parodies the pop song 《你快回来》."),
 ('出事', 'chūshì', 'HSK5', "'Something (bad) happens, have an accident'. 会不会出什么事 = could something have happened? Neutral alternatives: 发生 (happen), 出问题 (go wrong)."),
 ('下馆子', 'xià guǎnzi', 'idiom', "'Eat out at a restaurant' (colloquial). 馆子 = eatery. Neutral equivalent: 去饭店吃饭 / 在外面吃."),
 ('要不', 'yàobù', 'HSK5', "'How about… / Otherwise': 要不咱们先吃吧 = how about we eat first? Suggests an alternative plan; same as 要不然 / 不如."),
 ('凉了都', 'liáng le dōu', 'grammar', "= 都凉了 'it's all gone cold'. Moving 都 to the end is an afterthought word order typical of casual Beijing speech."),
 ('半道上', 'bàndào shang', 'colloq.', "'Halfway, on the way' = 半路上. 半道上饿得受不了 = got starving partway there."),
 ('受不了', 'shòu bu liǎo', 'HSK5', "'Can't stand / can't bear it' — potential complement. 了 is liǎo here, not le. Adj + 得 + 受不了 = so … you can't stand it: 饿得受不了 (starving), 热得受不了."),
 ('像…似的', 'xiàng … shìde', 'grammar', "'Just like …': 就像我们俩似的 = just like us two. 似的 is pronounced shìde (not sìde) in this pattern; the same as 像…一样."),
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
