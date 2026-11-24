# -*- coding: utf-8 -*-
import os, html
from pypinyin import pinyin, Style

TITLE = "家有儿女 S01E02 08:38.72 - 09:04.80"
OUT = "家有儿女S01E02_clip_08-38_lesson"
S = [
 ('08:38.72', '那她花了多少钱雇你', "So how much money did she pay to hire you?"),
 ('08:40.64', '别那么庸俗好不好', "Don't be so vulgar, would you?"),
 ('08:42.00', '这不是金钱交易', "This is not a financial transaction."),
 ('08:43.40', '是第四十八页三道十六行', "It's page 48, problem 3, line 16."),
 ('08:45.60', '那是什么东西', "What on earth is that?"),
 ('08:47.84', '一道经典理科试题', "A classic science exam problem."),
 ('08:49.80', '我们班只有她学会', "In our class, only she has mastered it."),
 ('08:53.92', '她是让你帮助她', "She asked you to help her,"),
 ('08:55.96', '然后她才来帮助你', "and only then would she help you in return."),
 ('08:57.64', '对 但是她没有帮助我', "Right — but she hasn't helped me yet."),
 ('08:59.36', '她说除了我演得特别像', "She said that unless I act really convincingly,"),
 ('09:01.08', '她才肯跟我讲题', "she won't agree to explain the problem to me."),
]
# (sentence_index, char_k_position) -> pinyin override
OVERRIDE = {
 (0, 2): 'huā',   # 花 in 花钱 → huā (spend), not huā (flower)
 (0, 5): 'qián',  # 钱 → qián
 (0, 6): 'gù',    # 雇 → gù (hire)
 (1, 2): 'yōng',  # 庸 in 庸俗 → yōng
 (2, 2): 'jīn',   # 金 in 金钱 → jīn
 (2, 3): 'qián',  # 钱 → qián
 (2, 4): 'jiāo',  # 交 in 交易 → jiāo
 (5, 1): 'diào',  # 道 in 一道 → dào (measure word for problems)
 (6, 5): 'zhǐ',   # 只 in 只有 → zhǐ (only)
 (9, 2): 'dàn',   # 但 in 但是 → dàn
 (10, 2): 'chú',  # 除 in 除了 → chú
 (10, 7): 'tè',   # 特 in 特别 → tè
 (11, 2): 'kěn',  # 肯 in 才肯 → kěn (willing/consent)
}
VOCAB = [
 ('庸俗', 'yōng sú', 'HSK5', 'Vulgar, philistine, lowbrow — lacking refinement or idealism. 庸俗 implies a crass, money-minded mentality. The boy rejects the assumption that money is the motive; the transaction is an intellectual exchange. Near-synonym: 粗俗 (crude/coarse, more about manners); 低俗 (lowbrow, often about content).'),
 ('金钱交易', 'jīn qián jiāo yì', 'HSK4+', 'A financial transaction; a cash deal. 交易 alone = transaction/trade (commercial). The phrase 这不是金钱交易 dismisses the mercenary interpretation. 交易 also appears in stock market context: 证券交易所. Here used somewhat dramatically to elevate what is just tutoring barter.'),
 ('理科', 'lǐ kē', 'HSK5', 'Science subjects (maths, physics, chemistry, biology) — as opposed to 文科 (humanities/arts subjects). The Chinese high-school track system divides students into 理科生 and 文科生. The problem referenced (page 48, problem 3, line 16) is a science problem Xia Xue can solve.'),
 ('除了…才', 'chú le…cái', 'grammar', '"Only if… then…" — a conditional construction expressing a prerequisite. 除了我演得特别像，她才肯… = "Only if I perform convincingly will she agree to…" Note: 才 here means "only then" (not "just/only" in terms of quantity). Compare: 只有…才 (only by… can…), which is more formal.'),
 ('肯', 'kěn', 'HSK4', 'To be willing to; to consent to do something (usually a positive willingness). 她才肯跟我讲题 = only then will she be willing to explain the problem. Near-synonym: 愿意 (want/willing, more about desire); 肯 implies deliberate agreement, often after some condition is met.'),
 ('学会', 'xué huì', 'HSK3', 'To learn how to do something; to master a skill. 只有她学会 = only she has mastered it. The resultative complement 会 (can/know how to) added to 学 shows successful completion of learning. Compare: 学了 (studied it, completed action but result unclear); 学会了 (fully learned/mastered).'),
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
