# -*- coding: utf-8 -*-
import os, html
from pypinyin import pinyin, Style

TITLE = "家有儿女 10:39.00 - 11:04.00"
OUT = "家有儿女S01E01_clip_10-39_lesson"
S = [
 ('10:39.00', '洗手去', "Go wash your hands."),
 ('10:42.00', '那我帮你把行李拿房间', "Let me take your luggage to the room."),
 ('10:45.00', '好 我来', "Sure — I'll do it."),
 ('10:46.00', '来来来 咱俩一块', "Come, come — let's do it together."),
 ('10:53.00', '小雨 你告诉我', "Xiaoyu, tell me —"),
 ('10:54.00', '你在这个家好吗', "Are you doing well in this family?"),
 ('10:57.00', '还行吧', "It's alright, I guess."),
 ('10:59.00', '咱爸娶了后妈以后', "Since our dad remarried —"),
 ('11:00.00', '你过得好吗', "Have you been getting on okay?"),
 ('11:02.00', '还行', "Fine."),
 ('11:03.00', '你告诉姐姐', "Tell your sister."),
 ('11:04.00', '咱们姓夏的孩子', "We kids who have the surname Xia —"),
]
# (sentence_index, char_k_position) -> pinyin override
OVERRIDE = {
 # 把 bǎ: grammatical marker (prepositional), not 把 bà (handle) — pypinyin gets this right in context
 # 好 hǎo (adj) vs hào (v, to like): all instances here are hǎo — no override needed
 # 过 guò (pass/experience) vs 过 guo (aspect marker): index 8, char 2 is aspect 过 → guo
 (8, 2): 'guò',  # 过得 — 过 here is verb "pass/live through", not aspect marker; pypinyin may default to guo
}
VOCAB = [
 ('行李', 'xíng li', 'HSK4', 'Luggage, baggage. 拿行李 = carry/take the luggage; 行李箱 = suitcase. Note the neutral tone on 李 in natural speech. Common at airports/train stations: 托运行李 (checked baggage), 随身行李 (carry-on).'),
 ('咱俩', 'zán liǎ', 'colloquial', 'The two of us (inclusive). 咱 is informal Northern/Beijing dialect for "we/us (inclusive, including the listener)". 俩 = liǎ in colloquial speech (= 两个). Compare: 我们俩 (more standard); 咱们 (all of us, inclusive). Very common in Beijing-dialect TV.'),
 ('后妈', 'hòu mā', 'HSK4+', 'Stepmother. 后 = behind/after, here meaning "replacement/subsequent". Compare: 继母 jì mǔ (formal/literary term for stepmother); 后爸 (stepfather). 娶 qǔ = to marry (used when a man marries — 娶妻, 娶了后妈).'),
 ('娶', 'qǔ', 'HSK4', 'To marry (a woman) — used for the groom\'s action. Opposite: 嫁 jià = to marry (used for the bride\'s action). Pattern: 男人娶女人，女人嫁男人. 娶了后妈以后 = after (dad) married a stepmother. Never use 娶 for the bride\'s perspective.'),
 ('过得好', 'guò de hǎo', 'HSK3+', 'To be getting on well, to live well. 过 (verb) = to live/get along; 得 (complement marker); 好 = well. Pattern: 过得好/不好/怎么样. Compare: 过得怎么样？(How are you getting on?); 日子过得不错 (life is going pretty well). 你过得好吗 is a warmer, more concerned "are you doing alright" than a casual 你好吗.'),
 ('咱们', 'zán men', 'HSK3', 'We/us — inclusive (includes the listener). Contrasts with 我们 which can be exclusive (may exclude the listener). 咱们姓夏的孩子 = we kids with the surname Xia (Xiaoxue addresses her brother, including both of them). Common in Northern Mandarin/Beijing speech; less common in Southern dialects.'),
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
