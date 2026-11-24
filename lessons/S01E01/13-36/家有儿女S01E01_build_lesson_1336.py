# -*- coding: utf-8 -*-
import os, html
from pypinyin import pinyin, Style

TITLE = "家有儿女 13:36.00 - 13:57.00"
OUT = "家有儿女S01E01_clip_13-36_lesson"
S = [
 ('13:36.00', '你看看人家小雪', "Look at Xiaoxue over there!"),
 ('13:37.00', '人家座位特别棒', "Her posture is exceptionally good!"),
 ('13:40.00', '北京市的座位比赛', "In the Beijing posture competition"),
 ('13:42.00', '都得过特等奖', "she's won the top prize every time."),
 ('13:45.00', '今后在这个家里', "From now on, in this home,"),
 ('13:46.00', '我的独立人格', "my independent personhood"),
 ('13:47.00', '必须得到尊重', "must be respected."),
 ('13:49.00', '我有权在衣食住行', "I have the right, in all matters of food, clothing, shelter, and travel,"),
 ('13:51.00', '各方面', "in every aspect,"),
 ('13:52.00', '保持自己的个性', "to maintain my own individuality."),
 ('13:54.00', '不容质疑', "This is beyond question."),
 ('13:57.00', '不许随便动我的东西', "No one is allowed to casually touch my things."),
]
OVERRIDE = {
 # 得 in 都得过: děi (must/have to), pypinyin defaults to dé
 (3, 1): 'děi',
 # 得 in 必须得到: dé (obtain), pypinyin should handle but verify
 # 得到 — pypinyin usually gives dé correctly in this context; no override needed
}
VOCAB = [
 ('座位', 'zuò wèi', 'HSK3', 'Seat, posture (here used colloquially for 坐姿 sitting posture). Standard meaning: a seat (on a bus, in a theater). Dad is using it humorously/loosely to mean 坐姿 (sitting posture/bearing). 比赛 = competition. 特等奖 = top/special prize (特等 = special grade, above 一等奖).'),
 ('独立人格', 'dú lì rén gé', 'HSK5+', 'Independent personhood / autonomous personality. 独立 = independent (HSK4); 人格 = character, personhood, dignity. A formal/legal-sounding phrase — Xiaoxue is reading out a quasi-legal declaration of rights, which is the comedy here. Collocations: 尊重人格 (respect personhood), 人格尊严 (personal dignity).'),
 ('衣食住行', 'yī shí zhù xíng', 'idiom', 'Food, clothing, shelter, and transportation — the four necessities of life. A fixed four-character idiom (成语). Covers all basic aspects of daily living. Commonly used in political speeches and everyday contexts: 老百姓的衣食住行 = the basic needs of ordinary people.'),
 ('保持', 'bǎo chí', 'HSK4', 'To maintain, keep, preserve. 保持个性 = maintain one\'s individuality. 保持沉默 = maintain silence (appears later in the episode). 保持联系 = keep in touch. Verb + object structure: 保持 + noun/state.'),
 ('不容质疑', 'bù róng zhì yí', 'idiom', 'Beyond question, indisputable, brooking no doubt. 不容 = not tolerating/allowing; 质疑 = to question, to doubt. A formal, emphatic phrase. Used in written language and formal speeches. Xiaoxue using it at the dinner table to announce her household rules is deliberately over-the-top and comedic.'),
 ('随便', 'suí biàn', 'HSK3', 'Casually, randomly, arbitrarily; to do as one pleases. 不许随便动 = not allowed to casually touch. As an adjective: 随便 = casual, informal (你随便 = whatever you like / up to you). As an adverb modifying verbs: 不要随便说话 = don\'t just say anything without thinking.'),
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
