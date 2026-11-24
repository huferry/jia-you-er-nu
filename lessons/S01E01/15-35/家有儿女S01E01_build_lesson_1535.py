# -*- coding: utf-8 -*-
import os, html
from pypinyin import pinyin, Style

TITLE = "家有儿女 15:35.00 - 16:10.00"
OUT = "家有儿女S01E01_clip_15-35_lesson"
S = [
 ('15:35.00', '小雪这孩子', "That child Xiaoxue —"),
 ('15:36.00', '确实太不像话', "she really has gone too far."),
 ('15:38.00', '我一定好好教育教育她', "I'll definitely have a good talk with her."),
 ('15:45.00', '现在就去', "Go right now."),
 ('15:46.00', '去你的', "Oh, get out of here! / You wish!"),
 ('15:50.00', '我现在不能说', "I can't say anything right now."),
 ('15:51.00', '你现在更不能说了', "And you definitely can't say anything now either."),
 ('15:54.00', '你现在要一批评她', "If you criticize her right now,"),
 ('15:55.00', '她准觉得是我出的主意', "she'll definitely think it was my idea."),
 ('15:58.00', '我就是那个很毒的后妈', "That would make me the wicked stepmother."),
 ('16:02.00', '就是那没主见的爹', "And you'd be the spineless father with no mind of his own."),
 ('16:08.00', '咱们俩现在只好忍着', "The two of us have no choice but to put up with it for now."),
]
OVERRIDE = {
 # 准 in 她准觉得: zhǔn (certainly/definitely — adverbial use), pypinyin may give zhǔn
 # correctly in some versions; override to be safe
 (8, 1): 'zhǔn',
}
VOCAB = [
 ('不像话', 'bù xiàng huà', 'HSK4+', 'Outrageous, unacceptable, out of line. Literally "not like speech/words" → doesn\'t behave as one should. 太不像话了 = that\'s completely unacceptable! A common spoken exclamation expressing moral disapproval. Used by adults about children\'s behavior, or by anyone about conduct that violates social norms. Compare: 不像样 (doesn\'t look the part / shabby); 说不过去 (can\'t justify it).'),
 ('去你的', 'qù nǐ de', 'colloquial', 'Get out of here! / Oh come on! / You wish! A dismissive exclamation used to brush off an unreasonable suggestion or to tease someone. Not rude, more like rolling one\'s eyes. 刘美 says it when her husband suggests going to scold Xiaoxue immediately — she\'s dismissing his impulsive idea. Compare: 得了吧 (give me a break); 才不是呢 (no way).'),
 ('主见', 'zhǔ jiàn', 'HSK5', 'One\'s own opinion / ability to make independent decisions. 没主见 = spineless, indecisive, can\'t think for oneself. 有主见 = knows one\'s own mind, decisive. 刘美 uses it as a pointed jab: if the dad scolds Xiaoxue because 刘美 suggested it, he\'s just a puppet — 没主见的爹. This is both an accusation and a warning: she doesn\'t want to be manipulated into that role.'),
 ('后妈', 'hòu mā', 'colloquial', 'Stepmother. 后 = behind/after (in family terms: step-); 妈 = mom. 毒后妈 = wicked/cruel stepmother — a stock villain from fairy tales (like Cinderella\'s stepmother). 刘美 is acutely aware of this stereotype and is strategically managing her image with Xiaoxue. The 毒 (venomous, cruel) is what she wants to avoid being labeled as.'),
 ('忍', 'rěn', 'HSK4', 'To endure, bear, put up with, restrain oneself. 只好忍着 = can only put up with it / have no choice but to endure. 忍 is a core concept in Chinese social culture — patience and endurance are virtues. Compounds: 忍耐 (patience, endurance); 忍不住 (can\'t hold back, can\'t help but); 忍气吞声 (swallow one\'s anger — idiom for bearing humiliation in silence).'),
 ('只好', 'zhǐ hǎo', 'HSK4', 'Have no choice but to, can only. 只好 + V = the only option is to [do X]. Expresses that all other options are closed off. 咱们俩只好忍着 = the two of us can only grin and bear it. Compare: 只能 (can only — focuses on ability/possibility); 不得不 (have to, must — stronger compulsion); 只好 emphasizes reluctant acceptance of the only remaining option.'),
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
