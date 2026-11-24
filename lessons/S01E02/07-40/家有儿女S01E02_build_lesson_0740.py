# -*- coding: utf-8 -*-
import os, html
from pypinyin import pinyin, Style

TITLE = "家有儿女 S01E02 07:40.12 - 08:03.56"
OUT = "家有儿女S01E02_clip_07-40_lesson"
S = [
 ('07:40.12', '如果你不肯放弃这种不负责任的幼稚的感情', "If you refuse to give up this kind of irresponsible, childish so-called romance,"),
 ('07:47.88', '作为小雪的父亲', "then as Xia Xue's father,"),
 ('07:49.00', '我就会马上联络你的父亲', "I will immediately contact your father,"),
 ('07:50.72', '连同校方处理这个问题', "and together with the school deal with this matter,"),
 ('07:52.12', '将反对早恋进行到底', "and take our opposition to early romance all the way to the end!"),
 ('07:55.24', '你把我提醒一下来', "You've reminded me of something —"),
 ('07:56.32', '我根本就管不了', "I actually can't control this at all."),
 ('07:57.80', '请请请', "Please, please, please —"),
 ('07:58.52', '千万别告诉我爸爸好不好', "whatever you do, please don't tell my dad, okay?"),
 ('08:00.48', '那你是不是就能够立刻', "So does that mean you could immediately"),
 ('08:02.00', '从小雪的身边消失', "disappear from Xia Xue's side?"),
 ('08:05.44', '其实', "Actually…"),
]
# (sentence_index, char_k_position) -> pinyin override
OVERRIDE = {
 (0, 3): 'kěn',   # 肯 in 不肯 → kěn (willing), not kèn
 (0, 6): 'zhè',   # 这 → zhè
 (0, 7): 'zhǒng', # 种 in 这种 → zhǒng (type/kind)
 (0, 8): 'bù',    # 不 → standard
 (0, 11): 'rèn',  # 任 in 负责任 → rèn (responsibility)
 (0, 13): 'yòu',  # 幼 in 幼稚 → yòu
 (0, 15): 'suǒ',  # 所 — not in text, skip
 (4, 2): 'fǎn',   # 反 in 反对 → fǎn
 (4, 5): 'zǎo',   # 早 in 早恋 → zǎo
 (4, 6): 'liàn',  # 恋 in 早恋 → liàn
 (4, 8): 'jìn',   # 进 in 进行 → jìn
 (8, 0): 'qiān',  # 千 in 千万 → qiān
 (8, 2): 'bié',   # 别 → bié
 (10, 1): 'xiǎo', # 小 → xiǎo
}
VOCAB = [
 ('不负责任', 'bù fù zé rèn', 'HSK4+', 'Irresponsible; failing to take responsibility. The key word 负责任 (take responsibility) is negated by 不. Very common in moral criticism. Near-synonym: 不靠谱 (unreliable, more colloquial). The charge here is that the boy\'s "romance" at this age is inherently irresponsible.'),
 ('幼稚', 'yòu zhì', 'HSK5', 'Childish, naive, immature. Often used by adults to dismiss young people\'s actions or emotions. Stronger criticism than 天真 (naive/innocent, which can be positive). 幼稚园 = kindergarten. Here paired with 不负责任 as a double dismissal.'),
 ('早恋', 'zǎo liàn', 'HSK5+', 'Underage or premature romance — dating before the socially/educationally approved age (typically before university in Chinese cultural context). A culturally loaded term: parents and teachers treat 早恋 as almost a disciplinary offense. Central concept of this episode.'),
 ('进行到底', 'jìn xíng dào dǐ', 'idiom', 'To carry something through to the very end, to see it through completely. 进行 = carry out/conduct; 到底 = to the end/bottom. Dramatic, official-sounding. The father is ironically using bureaucratic language for a family dispute.'),
 ('千万别', 'qiān wàn bié', 'HSK4', 'Whatever you do, don\'t…; absolutely must not. 千万 intensifies the prohibition. 千万 literally "ten million" — hyperbolic emphasis. Compare: 一定不要 (definitely don\'t), less urgent. Very common in spoken Chinese for strong warnings or pleas.'),
 ('管不了', 'guǎn bu liǎo', 'grammar', 'Cannot control/manage. Potential complement construction: 管 (control) + 不 (negative potential) + 了 (completion marker). Compare: 管得了 (can control). The father\'s threat to "contact your father" backfires — he realizes he has no real authority over the boy.'),
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
