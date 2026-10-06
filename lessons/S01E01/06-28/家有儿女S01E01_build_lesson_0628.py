# -*- coding: utf-8 -*-
import os, html
from pypinyin import pinyin, Style

TITLE = "家有儿女 06:28.00 - 06:57.00"
OUT = "家有儿女_clip_06-28_lesson"
S = [
 ('06:28.00', '真的 我就给秃小子当过妈', "Really. I've only ever been mom to a scruffy little boy."),
 ('06:33.00', '我从来没想过要给一大闺女当妈', "I never imagined I'd be mom to a big girl."),
 ('06:36.00', '我保证啊 这种感觉一定会特别地好', "I promise you, it's going to feel wonderful."),
 ('06:40.50', '为什么', "Why's that?"),
 ('06:41.50', '因为小雪是一个特文静', 'Because Xiaoxue is a really quiet, gentle,'),
 ('06:43.50', '懂礼貌 有教养 典型的乖乖女呀', 'polite, well-brought-up — a classic good girl.'),
 ('06:47.00', '真的啊', 'Really?'),
 ('06:49.00', '你看她在学校是尖子生', "Look — at school she's a top student."),
 ('06:50.50', '正好咱们在一块', "And now that we'll all be together,"),
 ('06:52.50', '她能在刘星的眼皮底下', "right under Liu Xing's nose, she can"),
 ('06:53.50', '给刘星树立一活榜样', 'set Liu Xing a living example.'),
 ('06:57.00', '你快走吧 怎么还不走啊', "Off you go — why haven't you left yet?"),
]
OVERRIDE = {
 (2, 13): 'de',
 (5, 4): 'jiào',
 (9, 9): 'xia',
}
VOCAB = [
 ('秃小子', 'tū xiǎozi', 'colloq.', "Literally 'bald little kid' — affectionate northern slang for a (scruffy, rough-and-tumble) little boy. Contrast 闺女 in the next line: boy vs. girl. 子 is toneless (zi)."),
 ('闺女', 'guīnǚ', 'colloq.', "'Daughter / girl' — warm, colloquial northern word. 一大闺女 = 一(个)大闺女, 'a big (grown-up) girl'; the measure word 个 is often dropped after 一 in fast speech."),
 ('从来没', 'cónglái méi', 'grammar', "'Never (ever) have…': 从来 + 没/不 + verb (+过). 我从来没想过 = 'I never once thought'. 从来 is almost always used with a negative."),
 ('保证', 'bǎozhèng', 'HSK4', "'To guarantee, promise'. 我保证 is a strong spoken promise — stronger than 我答应 (I agree to). Also a noun: 质量保证 (quality guarantee)."),
 ('感觉', 'gǎnjué', 'HSK4', "As a noun 'feeling/sense' (这种感觉 = this feeling); also a verb 'to feel' (我感觉很好). Close to 觉得, but 感觉 leans more toward sensations and impressions."),
 ('文静', 'wénjìng', 'HSK6', "'Gentle and quiet' — refined, calm, not rowdy; used almost exclusively for girls/women. Contrast 安静 (quiet, of a place or a moment)."),
 ('礼貌 / 教养', 'lǐmào / jiàoyǎng', 'HSK4 / HSK6', "懂礼貌 = 'has good manners' (lit. 'understands courtesy'); 有教养 = 'well brought up, cultured'. 教 is 4th tone (jiào) here, not jiāo (to teach)."),
 ('典型', 'diǎnxíng', 'HSK5', "'Typical, classic (example)': 典型的乖乖女 = 'a textbook good girl'. More emphatic than 一般 (ordinary) — it's the perfect representative of a type."),
 ('乖乖女', 'guāiguāi nǚ', 'idiom', "'Good girl' — obedient, well-behaved daughter. 乖 = well-behaved (said of children/pets); 真乖! = 'Good boy/girl!'"),
 ('尖子生', 'jiānzishēng', 'colloq.', "'Top student' — 尖子 = the tip/the best of a group. Synonym: 优等生, 学霸 (newer slang)."),
 ('眼皮底下', 'yǎnpí dǐxia', 'idiom', "'Right under one's nose' (lit. 'under the eyelids'). 在X的眼皮底下 = right in front of X, where X can't miss it."),
 ('树立 / 榜样', 'shùlì / bǎngyàng', 'HSK6 / HSK5', "树立榜样 = 'set an example' — a fixed collocation. 树立 also goes with 形象 (image), 信心 (confidence). 活榜样 = 'a living role model'."),
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
