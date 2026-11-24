# -*- coding: utf-8 -*-
import os, html
from pypinyin import pinyin, Style

TITLE = "家有儿女 S01E02 14:01.74 - 14:53.24"
OUT = "家有儿女S01E02_clip_14-01_lesson"
S = [
 ('14:01.74', '第三页', "Page three."),
 ('14:05.74', '我想有个女朋友', "I want to have a girlfriend."),
 ('14:08.36', '第四页', "Page four."),
 ('14:10.66', '送给你一朵玫瑰花', "I'll give you a rose."),
 ('14:16.74', '你现在就告诉我怎么做那道题了吧', "Tell me right now how to solve that problem, okay?"),
 ('14:19.36', '现在还不行', "Not yet."),
 ('14:22.74', '我的目标还没达到', "My goal hasn't been achieved yet."),
 ('14:25.40', '我觉得你父母人挺好的', "I think your parents are pretty nice people."),
 ('14:27.16', '你担心的事情 根本不会发生', "The thing you're worried about simply won't happen."),
 ('14:39.24', '这几天小雪 开始往乖乖女的方向发展了', "These past few days, Xiaoxue has started moving in the direction of a well-behaved girl."),
 ('14:44.24', '宽容和理解的神奇力量', "The magical power of tolerance and understanding!"),
 ('14:47.24', '这说明我们的角色多么英明', "This shows how wise our roles have been."),
]
# (sentence_index, char_k_position) -> pinyin override
OVERRIDE = {
 (9, 7): 'guāi',   # 乖 is guāi; pypinyin should get it right, but just in case
}
OVERRIDE = {
}
VOCAB = [
 ('玫瑰花', 'méi guī huā', 'HSK4', 'Rose. The book Wild Boy is reading aloud uses classic romantic lines from a novel — "送给你一朵玫瑰花" is a clichéd love declaration, which is exactly why it\'s funny here. 玫瑰 alone = rose (the plant/flower concept); 玫瑰花 = a rose (the actual flower). Collocations: 一束玫瑰花 (a bouquet of roses), 玫瑰色 (rose-colored).'),
 ('目标', 'mù biāo', 'HSK4', 'Goal, objective, target. 达到目标 = achieve one\'s goal. Here Xiaoxue means her plan — using Wild Boy as a decoy — hasn\'t fully worked yet. Collocations: 完成目标 (complete a goal), 实现目标 (realize a goal). Note: 目标 is for a concrete intended outcome; compare 理想 (ideal/dream, more abstract).'),
 ('乖乖女', 'guāi guāi nǚ', 'colloquial', 'Good girl, obedient daughter. 乖 = well-behaved, docile. Reduplication 乖乖 adds affectionate/dismissive tone. 乖乖女 = a girl who follows rules and pleases parents. Used here by the father observing a change in Xiaoxue\'s behavior — slightly patronizing but warm. Opposite: 叛逆女 (rebellious girl).'),
 ('宽容', 'kuān róng', 'HSK5', 'Tolerant, forgiving, broad-minded. 宽 = broad, 容 = contain/accept. 宽容和理解 = tolerance and understanding — the parents\' self-congratulatory slogan. Collocations: 宽容大度 (magnanimous), 对…宽容 (be tolerant toward). Compare: 包容 (encompass/forgive, slightly broader); 原谅 (forgive a specific wrong).'),
 ('英明', 'yīng míng', 'HSK5', 'Wise, brilliant (of a decision or leader). Formal/literary register — often used to praise emperors or leaders. Here used self-ironically by the father to congratulate himself, adding comic pomposity. Collocations: 英明决策 (brilliant decision), 英明领导 (wise leadership). The humor: praising your own parenting in imperial vocabulary.'),
 ('神奇', 'shén qí', 'HSK5', 'Magical, miraculous, wondrous. 神 = divine/spirit, 奇 = strange/remarkable. 神奇力量 = magical power. Used hyperbolically here — the father is delighted that giving freedom actually worked. Compare: 奇妙 (wonderfully strange, more aesthetic), 神秘 (mysterious, unknown).'),
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
    # 不 sandhi: 不 (4th) → bú before another 4th-tone syllable
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
