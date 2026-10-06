# -*- coding: utf-8 -*-
import os, html
from pypinyin import pinyin, Style

TITLE = "家有儿女 05:40.40 - 06:24.00"
OUT = "家有儿女_clip_05-40_lesson"
S = [
 ("05:40.40", "什么加利福尼亚的大蜘蛛", "A giant California spider, what are you talking about?"),
 ("05:42.50", "那是早晨起来妈妈去买的活螃蟹", "That was a live crab Mom went out and bought first thing this morning."),
 ("05:52.00", "你跟小雪说", "You tell Xiaoxue —"),
 ("05:53.50", "就说我真心的欢迎她来", "tell her I sincerely welcome her."),
 ("05:55.50", "她来了咱们这个新家才能算完整", "Only once she's here can our new family really be complete."),
 ("06:00.00", "没问题 一定会如实转达", "No problem, I'll pass that along exactly."),
 ("06:03.00", "你还没告我呢 她爱喝什么汤", "You still haven't told me — what soup does she like?"),
 ("06:06.00", "我记得应该是西红柿鸡蛋汤", "I remember it should be tomato and egg soup."),
 ("06:11.00", "你等会 我想想还有什么事来着", "Hold on — let me think what else there was."),
 ("06:18.00", "我看看你是有点紧张了吧 紧张了", "Let me see... you're a little nervous, aren't you — nervous."),
 ("06:21.00", "去你的 我紧张什么呀我", "Get outta here, what would I have to be nervous about?"),
 ("06:24.00", "我就是有点心跳过速", "I just — my heart's racing a little, that's all."),
]
OVERRIDE = {
 (5, 8): "zhuǎn",
 (7, 2): "de",
 (8, 12): "zhe",
}
VOCAB = [
 ("真心", "zhēnxīn", "HSK5", "'Sincere, wholehearted': 真心的欢迎 = 'sincerely welcome'. Stronger than 真的 (really) — 真心 stresses that the feeling comes from the heart, not just words."),
 ("完整", "wánzhěng", "HSK4", "'Complete, whole' — nothing missing. 才能算完整 = 'can only then be called complete'. Compare 完全 (completely, an adverb) vs 完整 (an adjective describing a whole thing)."),
 ("才能", "cái néng", "grammar", "'Only then can...': …了，X才能… — the first clause states a condition, 才 marks that only once it's met does X become possible. 她来了 咱们这个新家才能算完整."),
 ("如实", "rúshí", "HSK6", "'Truthfully, as things really are': 如实转达 = 'relay exactly as said', without adding or omitting anything. Formal register, common in reporting/relaying contexts."),
 ("转达", "zhuǎndá", "HSK5", "'To pass on / relay (a message)' from one person to another. More specific than 说 — implies you're speaking on someone else's behalf. Note 转 is 3rd tone (zhuǎn), not zhuàn."),
 ("记得", "jìde", "HSK3", "'To remember, recall' — 得 here is toneless (de), not dé. Opposite: 忘记 (to forget). 我记得应该是… = 'I remember it should be...'"),
 ("紧张", "jǐnzhāng", "HSK3", "'Nervous, tense' — of a person's feelings, or of a situation (时间很紧张 = time is tight). 有点紧张了 = 'a bit nervous'."),
 ("心跳过速", "xīntiào guòsù", "idiom", "'Rapid heartbeat, tachycardia' — 心跳 (heartbeat) + 过速 (excessive speed). Literally medical-sounding, used here half-jokingly to describe nervous excitement."),
 ("去你的", "qù nǐ de", "idiom", "A mild, joking dismissal — 'get outta here', 'oh stop it' — not a literal 'go to yours'. Used to wave off a teasing remark, often between close friends or family."),
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
