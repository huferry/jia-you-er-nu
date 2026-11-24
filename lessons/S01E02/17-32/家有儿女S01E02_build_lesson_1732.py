# -*- coding: utf-8 -*-
import os, html
from pypinyin import pinyin, Style

TITLE = "家有儿女 S01E02 17:32.24 - 18:07.24"
OUT = "家有儿女S01E02_clip_17-32_lesson"
S = [
 ('17:32.24', '刘星怎么还不回来', "How come Liu Xing still isn't back?"),
 ('17:33.24', '都几点了', "Look what time it is already!"),
 ('17:37.24', '肯定忘拿钥匙了', "He must have forgotten his key again."),
 ('17:43.24', '就住在你家楼上', "I live right upstairs from your apartment."),
 ('17:48.24', '我的女儿', "My daughter —"),
 ('17:49.24', '和你家的小儿子', "— and your little son"),
 ('17:51.24', '是同一个班的', "are in the same class."),
 ('17:58.24', '由于事关重大', "Since this matter is of great importance,"),
 ('17:59.24', '我要和你家的男主人对话', "I need to speak with the man of the house."),
 ('18:03.24', '要跟你对话', "He wants to talk to you."),
 ('18:05.24', '男主人在', "The man of the house is here."),
 ('18:10.24', '要不然坐下谈话', "Why don't we sit down and talk?"),
]
# (sentence_index, char_k_position) -> pinyin override
OVERRIDE = {
 (2, 1): 'dìng',  # 肯定 → kěn dìng
 (3, 0): 'jiù',   # 就 → jiù (4th tone)
 (7, 2): 'shì',   # 事 in 事关重大 → shì
 (7, 4): 'zhòng', # 重 in 重大 → zhòng (important/weighty), not chóng
 (8, 6): 'nán',   # 男 in 男主人 → nán
 (9, 1): 'gēn',   # 跟 → gēn
 (10, 0): 'nán',  # 男 in 男主人 → nán
 (11, 3): 'xià',  # 下 → xià (sit down)
}
VOCAB = [
 ('肯定', 'kěn dìng', 'HSK3', 'Certainly, definitely; also "to affirm/confirm." As an adverb: 肯定 + V = "definitely does/did." Here: 肯定忘拿钥匙了 = "He definitely forgot his key." Very common in spoken Chinese for confident inference. Near-synonym: 一定 (more literary/formal); 肯定 is more colloquial.'),
 ('事关重大', 'shì guān zhòng dà', 'idiom', 'The matter is of great importance / the stakes are high. A formal fixed phrase: 事 (matter) + 关 (concerns/involves) + 重大 (significant). Note 重 here is zhòng (weighty), not chóng. Used to justify formal or dramatic behavior — here the neighbor uses it to request the "man of the house."'),
 ('男主人', 'nán zhǔ rén', 'phrase', 'The man of the house, male head of household. The counterpart is 女主人 (mistress of the house). The neighbor\'s insistence on speaking only to the 男主人 is played for comedy — the women are clearly equally (or more) in charge.'),
 ('由于', 'yóu yú', 'HSK4', 'Because of, due to — introduces a cause, more formal than 因为. 由于…, … = "Because of …, [therefore] …." 由于事关重大 = "Given that the matter is serious." Common in written Chinese and formal speech; 因为 is more colloquial.'),
 ('坐下', 'zuò xia', 'HSK2', 'Sit down. 坐下谈话 = "sit down and talk." Directional complement: 坐 (sit) + 下 (down). The polite formula 要不然坐下谈话 softens the confrontation — "why not just sit and talk it over?"'),
 ('楼上', 'lóu shàng', 'HSK3', 'Upstairs; "the floor above." 就住在你家楼上 = "I live just upstairs from you." 就 adds "right/exactly" — the neighbor is a close physical neighbor as well as an intrusive one. Contrast 楼下 (downstairs).'),
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
