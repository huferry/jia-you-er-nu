# -*- coding: utf-8 -*-
import os, html
from pypinyin import pinyin, Style

TITLE = "家有儿女 S01E02 10:41.76 - 11:03.64"
OUT = "家有儿女S01E02_clip_10-41_lesson"
S = [
 ('10:41.76', '警察要是一走', "The moment the police leave,"),
 ('10:43.52', '孩子又要落到家长的手掌里了', "the child falls right back into the parents' hands again."),
 ('10:48.80', '不行', "That won't work."),
 ('10:50.76', '你说得这没有', "Now you've left me speechless."),
 ('10:54.32', '把嘴给堵上了', "My mouth is completely blocked up!"),
 ('10:55.80', '就像这样', "Just like this."),
 ('11:02.28', '小雪 你不要紧张', "Xia Xue, don't be nervous."),
 ('11:06.76', '我们找你来就是想彼此沟通一下', "We asked you here because we just want to have a talk with each other."),
 ('11:09.92', '对', "Right."),
 ('11:11.04', '如果要是为了狂野男孩的事就算了', "If this is about the Wild Boy thing — let's just forget about it."),
 ('11:14.64', '因为我不想和别人讨论我的男朋友', "Because I don't want to discuss my boyfriend with anyone."),
 ('11:18.28', '关于你的男朋友', "As for your boyfriend —"),
]
# (sentence_index, char_k_position) -> pinyin override
OVERRIDE = {
 (0, 0): 'jǐng', # 警 in 警察 → jǐng
 (0, 3): 'yī',   # 一 in 一走 → yī
 (1, 2): 'yòu',  # 又 → yòu
 (1, 3): 'yào',  # 要 → yào
 (1, 4): 'luò',  # 落 in 落到 → luò (fall/land), not lào
 (1, 7): 'zhǎng', # 掌 in 手掌 → zhǎng
 (3, 2): 'zhè',  # 这 → zhè
 (5, 1): 'xiàng', # 像 in 就像 → xiàng
 (7, 5): 'bǐ',   # 彼 in 彼此 → bǐ
 (7, 6): 'cǐ',   # 此 in 彼此 → cǐ
 (7, 7): 'gōu',  # 沟 in 沟通 → gōu
 (10, 2): 'bù',  # 不 → bù
 (10, 5): 'tǎo', # 讨 in 讨论 → tǎo
 (10, 6): 'lùn', # 论 in 讨论 → lùn
}
VOCAB = [
 ('落到…手掌里', 'luò dào…shǒu zhǎng lǐ', 'idiom', 'To fall into someone\'s clutches/hands. 手掌 = palm. The image is of a child falling back into the grip of the parents after the police leave. The logic: calling 110 is pointless since the police leave and you\'re still at home. A dark but funny observation on the limits of child protection.'),
 ('堵上', 'dǔ shàng', 'HSK4+', 'To block up, plug up, stop up. 把嘴给堵上了 = "mouth has been completely blocked up" — i.e., left with nothing to say. The 把-construction + 给 (adds emphasis/adversarial nuance). 堵 also used for traffic: 堵车 (traffic jam). Here: an argument so good it silences you.'),
 ('彼此', 'bǐ cǐ', 'HSK5', 'Each other; mutually (between both parties). 彼此沟通 = communicate with each other. More formal/literary than 互相. Used in formal speech or writing. Can stand alone as "you and me both" in colloquial responses: 彼此彼此 = "same to you!" (mutually).'),
 ('沟通', 'gōu tōng', 'HSK4', 'To communicate; communication. 想沟通一下 = want to have a communication/chat. 沟通 implies a productive exchange — not just talking (说话) but achieving mutual understanding. Very common in modern Chinese: 沟通能力 (communication skills), 沟通不畅 (poor communication).'),
 ('就算了', 'jiù suàn le', 'colloquial', 'Let\'s just forget about it; let that go; that settles it. 为了狂野男孩的事就算了 = regarding the Wild Boy business, let\'s just drop it. 算了 alone = forget it / never mind. 就 adds finality: "then we\'ll count it as resolved." Very common for dismissing sensitive topics.'),
 ('讨论', 'tǎo lùn', 'HSK3', 'To discuss; discussion. 不想讨论我的男朋友 = don\'t want to discuss my boyfriend. More neutral than 争论 (argue/dispute) or 辩论 (debate, formal). 讨论 implies two-way exchange of views. Collocation: 讨论会 (discussion forum), 课堂讨论 (classroom discussion).'),
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
