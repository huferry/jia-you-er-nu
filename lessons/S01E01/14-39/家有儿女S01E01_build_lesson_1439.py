# -*- coding: utf-8 -*-
import os, html
from pypinyin import pinyin, Style

TITLE = "家有儿女 14:39.00 - 15:28.00"
OUT = "家有儿女S01E01_clip_14-39_lesson"
S = [
 ('14:39.00', '鸡蛋打得有点多', "The eggs — there are a few too many."),
 ('14:40.00', '太偏心了', "That's so unfair / showing favoritism!"),
 ('14:41.00', '那是我小时候', "That was when I was little."),
 ('14:45.00', '咱们好像有好长时间', "It seems like we've had such a long time"),
 ('14:47.00', '没住在一起了吧', "not living together, hasn't it."),
 ('15:05.00', '不高兴了吧', "You're unhappy, aren't you."),
 ('15:07.00', '我一看就是好委屈', "I can see at a glance — you feel really aggrieved."),
 ('15:10.00', '有什么委屈你趁着都说出来', "Whatever grievances you have, go ahead and get them all out."),
 ('15:16.00', '还有什么可说的呀', "What else is there to say?"),
 ('15:21.00', '我想哭', "I want to cry."),
 ('15:26.00', '我替她向你道歉', "I'll apologize to you on her behalf."),
 ('15:28.00', '就不哭了吧', "Then you won't cry anymore, right?"),
]
OVERRIDE = {
 # 长 in 好长时间: cháng (long, in time duration), pypinyin may give zhǎng (to grow)
 (3, 6): 'cháng',
 # 着 in 趁着: zhe (aspect/progressive particle), pypinyin may give zháo
 (7, 7): 'zhe',
}
VOCAB = [
 ('偏心', 'piān xīn', 'HSK4+', 'Favoritism, partiality, to favor one person over another. 太偏心了 = that\'s such favoritism! Here the younger boy complains that the soup was made especially for Xiaoxue (too many eggs = made with extra care). 偏 = biased, tilted; 心 = heart. Collocations: 偏心眼儿 (colloquial: playing favorites); 一碗水端平 (hold the bowl level = treat everyone equally — the ideal).'),
 ('委屈', 'wěi qu', 'HSK4', 'To feel wronged, aggrieved; a sense of grievance/injustice. Both noun and verb. 好委屈 = feeling very wronged. 说出委屈 = voice one\'s grievances. Key nuance: 委屈 implies the person has been treated unfairly and is suppressing hurt feelings — not just sadness but specifically the feeling of injustice. Very commonly used in family/relationship contexts.'),
 ('趁着', 'chèn zhe', 'HSK4+', 'Taking advantage of (an opportunity/condition); while (something is the case). 趁着 + situation + action. 有什么委屈你趁着都说出来 = while you have the chance, get all your grievances out. 趁热打铁 = strike while the iron is hot (idiom). 趁 alone is used the same way: 趁机 = take the opportunity; 趁早 = the sooner the better.'),
 ('道歉', 'dào qiàn', 'HSK4', 'To apologize. 我替她向你道歉 = I\'ll apologize to you on her behalf. Pattern: 向 + person + 道歉. 替 = on behalf of. Compare: 对不起 (sorry — informal, immediate); 道歉 is more formal and deliberate. 请求原谅 (to ask for forgiveness — even more formal). 刘美 offers this as a way to defuse Xiaoxue\'s emotional state — a pragmatic rather than sincere apology.'),
 ('好像', 'hǎo xiàng', 'HSK3', 'It seems like, as if, apparently. 咱们好像有好长时间没住在一起了 = it seems like we haven\'t lived together for such a long time. Used to express uncertainty or approximation. Compare: 似乎 (sìhū — more literary); 看起来 (looks like — based on visual observation); 好像 is the most colloquial and versatile.'),
 ('一看就', 'yī kàn jiù', 'grammar', 'As soon as one looks, it\'s immediately clear. Pattern: 一 + V + 就 + result. 我一看就知道 = I knew the moment I looked. 一 + verb signals the trigger; 就 signals the immediate consequence. This pattern expresses that something is immediately obvious. Here: 我一看就是好委屈 = one look and I can tell she\'s feeling very aggrieved.'),
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
