# -*- coding: utf-8 -*-
import os, html
from pypinyin import pinyin, Style

TITLE = "家有儿女 11:40.00 - 12:07.00"
OUT = "家有儿女S01E01_clip_11-40_lesson"
S = [
 ('11:40.00', '孩子们开饭了', "Kids, dinner's ready!"),
 ('11:42.00', '爸爸饿了', "Daddy's hungry."),
 ('11:43.00', '怎么还站这呢', "Why are you still standing around?"),
 ('11:46.00', '你坐这', "You sit here."),
 ('11:47.00', '我就在你旁边', "I'll be right beside you."),
 ('11:50.00', '小雨 你坐这', "Xiaoyu, you sit here."),
 ('11:51.00', '你坐那', "You sit there."),
 ('12:01.00', '看 大虾', "Look — big shrimp!"),
 ('12:03.00', '多吃点', "Eat more!"),
 ('12:04.00', '但正确的健康观念', "But the correct health concept —"),
 ('12:06.00', '是让人少吃点', "is to eat a little less."),
 ('12:08.00', '你这不是今天第一天来吗', "Isn't today your first day here?"),
]
# (sentence_index, char_k_position) -> pinyin override
OVERRIDE = {
 # 这/那 as proximal/distal demonstratives; in Beijing colloquial 这 → zhè, 那 → nà — pypinyin handles
 # 还 in 怎么还站这呢: hái (still) vs huán (return) — context = still, hái; pypinyin usually correct
}
VOCAB = [
 ('开饭', 'kāi fàn', 'HSK3+', 'Dinner/meal is ready; to start eating. 开饭了 = it\'s time to eat! (literally "the meal opens"). Common household announcement. Compare: 吃饭了 (let\'s eat / time to eat — can be used similarly); 开饭 is slightly more formal/announcement-like. 饭 here = meal (not specifically rice).'),
 ('旁边', 'páng biān', 'HSK3', 'Beside, next to, by the side of. 在你旁边 = beside you / next to you. Positional noun — used after 在: 在桌子旁边 (by the table). Compare: 旁边 (beside), 附近 (nearby/in the vicinity), 身边 (at one\'s side — more intimate). 我就在你旁边 = I\'ll be right next to you (就 adds reassurance).'),
 ('大虾', 'dà xiā', 'everyday', 'Large shrimp, prawns. 虾 = shrimp/prawn in general; 大虾 = big ones (a treat). Note: 大虾 is also a humorous internet slang term for "expert/guru" (大侠 homophone joke), but here it\'s literal food. The father is trying to make Xiaoxue feel welcome with a nice spread.'),
 ('健康观念', 'jiàn kāng guān niàn', 'HSK4+', 'Health concept/philosophy; view on health. 健康 = health/healthy; 观念 = concept, idea, mindset. 正确的健康观念 = the correct health philosophy. Xiaoxue deflects the stepmother\'s hospitality with a "health" lecture — a character moment showing her prickliness. 观念 collocates: 传统观念 (traditional values), 更新观念 (update one\'s thinking).'),
 ('少吃点', 'shǎo chī diǎn', 'grammar pattern', 'Eat a little less. Pattern: 少/多 + V + 点 = V a little less/more. 多吃点 (eat more) vs 少吃点 (eat less). 点 softens the imperative. This pattern is ubiquitous: 多喝水 (drink more water), 少说废话 (talk less nonsense), 多注意 (pay more attention). Xiaoxue counters 多吃点 with this correction.'),
 ('第一天', 'dì yī tiān', 'HSK3', 'The first day. 你这不是今天第一天来吗 = isn\'t today your first day (here)?  The "不是…吗" structure is a rhetorical question implying "it obviously is": 不是…吗 = isn\'t it the case that…? Used to gently challenge or express mild surprise. Compare: 是不是…? (a yes/no question); 不是…吗 carries more rhetorical weight.'),
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
