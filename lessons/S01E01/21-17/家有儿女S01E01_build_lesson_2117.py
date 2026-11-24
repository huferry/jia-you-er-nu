# -*- coding: utf-8 -*-
import os, html
from pypinyin import pinyin, Style

TITLE = "家有儿女 21:17.00 - 22:30.00"
OUT = "家有儿女S01E01_clip_21-17_lesson"
S = [
 ('21:17.00', '哈 好像一把火', "Ha — just like a blazing fire!"),
 ('21:19.00', '哈 燃烧了整个沙漠', "Ha — burning up the entire desert!"),
 ('21:25.00', '怎么都不说话了', "How come nobody's saying anything?"),
 ('21:27.00', '对我的男朋友不满意吗', "Are you not satisfied with my boyfriend?"),
 ('21:39.00', '那个 小雪', "Um… Xiaoxue."),
 ('21:41.00', '你说她是你什么人', "You said she is your — what exactly?"),
 ('22:01.00', '走 去我房间', "Come on, let's go to my room."),
 ('22:08.00', '你千万别着急', "Whatever you do, don't panic."),
 ('22:09.00', '真的一定要有耐心', "You really must have patience."),
 ('22:10.00', '不是 我不着急', "No no — I'm not panicking."),
 ('22:14.00', '吓到了', "Just… shocked."),
 ('22:29.00', '唱歌啊', "Singing!"),
]
OVERRIDE = {
 # 着 in 着急 (zháo jí): 着 here is zháo (2nd tone), not zhe/zhuó
 # 你千万别着急: 你(0)千(1)万(2)别(3)着(4)急(5) → 着 is k=4
 (7, 4): 'zháo',
 # 不是 我不着急: 不(0)是(1)我(2)不(3)着(4)急(5) → 着 is k=4
 (9, 4): 'zháo',
}
VOCAB = [
 ('燃烧', 'rán shāo', 'HSK5', 'To burn, blaze. 燃 = ignite; 烧 = burn. 燃烧了整个沙漠 = burned up the entire desert. 狂野男孩\'s dramatic love poem uses fire + desert imagery — the hallmark of a certain brand of overwrought teen romance. 燃烧 collocates with: 激情 (passion), 青春 (youth), 希望 (hope).'),
 ('满意', 'mǎn yì', 'HSK3', 'Satisfied, pleased. 不满意 = dissatisfied. 对…不满意 = not satisfied with … 满 = full; 意 = intention/feeling. Xiaoxue asks her stunned family if they disapprove of her boyfriend. Compare: 满足 (satisfied/content — often internal); 满意 (pleased with something/someone — often evaluative).'),
 ('着急', 'zháo jí', 'HSK3', 'To feel anxious, worried, flustered. 着 is pronounced zháo (2nd tone) in this compound, not the aspect marker zhe. 别着急 = don\'t worry/panic. 一点都不着急 = not the slightest bit anxious. 刘美 coaches 夏东海 to stay calm after the boyfriend reveal; he insists he\'s fine — he\'s just 吓到了.'),
 ('千万', 'qiān wàn', 'HSK4', 'By all means / whatever you do (emphatic warning). 你千万别着急 = whatever you do, don\'t panic. 千万 literally = ten million; used as an intensifier for instructions or warnings. Compare: 一定 (must/certainly — positive); 千万别/不要 (definitely don\'t — negative command).'),
 ('吓到', 'xià dào', 'HSK4+', 'To be scared/shocked (resultative). 吓 = to frighten; 到 = resultative complement (reaching a state). 吓到了 = got frightened/shocked. 夏东海\'s understated confession after insisting he\'s not anxious: he\'s not worried — he\'s just shocked. The comic timing lands on this single line.'),
 ('狂野', 'kuáng yě', 'HSK5+', 'Wild, untamed, uninhibited. 狂 = crazy/mad; 野 = wild/uncultivated. 狂野男孩 (Wild Boy) is Xiaoxue\'s boyfriend\'s name — itself a statement. His fire-and-desert love poem and dramatic delivery leave the blended family completely speechless.'),
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
