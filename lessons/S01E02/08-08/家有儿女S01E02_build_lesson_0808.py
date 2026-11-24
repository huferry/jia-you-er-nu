# -*- coding: utf-8 -*-
import os, html
from pypinyin import pinyin, Style

TITLE = "家有儿女 S01E02 08:08.84 - 08:35.80"
OUT = "家有儿女S01E02_clip_08-08_lesson"
S = [
 ('08:08.84', '其实我不是小雪的男朋友', "Actually, I'm not Xia Xue's boyfriend."),
 ('08:10.00', '是她过来的一个托儿', "I'm a decoy she brought in."),
 ('08:11.16', '什么', "What?!"),
 ('08:14.52', '小雪让我假冒她男朋友', "Xia Xue asked me to impersonate her boyfriend"),
 ('08:16.12', '是为了演给你们俩看', "just to put on a show for the two of you."),
 ('08:17.88', '她说爸爸娶了后妈', "She said her dad married a stepmom,"),
 ('08:20.04', '她怕受后妈的气', "and she was afraid of being pushed around by the stepmom."),
 ('08:21.72', '失去自由和快乐', "She was afraid of losing her freedom and happiness."),
 ('08:22.96', '所以拿这事给你们叫板', "So she used this whole thing to call your bluff."),
 ('08:29.96', '她是想表明', "She wanted to make it clear"),
 ('08:31.44', '她不是一个任人宰割的小绵羊', "that she's not a helpless little lamb who lets anyone do as they please,"),
 ('08:33.96', '而是长满了刺的小刺猬', "but a little hedgehog covered in spines."),
]
# (sentence_index, char_k_position) -> pinyin override
OVERRIDE = {
 (1, 2): 'guò',   # 过 in 过来 → guòlái (come over), not guò as verbal aspect
 (3, 2): 'ràng',  # 让 → ràng
 (3, 4): 'jiǎ',   # 假 in 假冒 → jiǎ (fake/pretend), not jià
 (5, 2): 'qǔ',    # 娶 → qǔ (marry, of man taking wife)
 (5, 3): 'le',    # 了 → le (completion)
 (6, 2): 'pà',    # 怕 → pà
 (6, 4): 'hòu',   # 后 in 后妈 → hòu
 (8, 1): 'yǐ',    # 以 in... actually 拿 nà
 (8, 4): 'gěi',   # 给 → gěi
 (8, 5): 'nǐ',    # 你 → nǐ
 (10, 4): 'rèn',  # 任 in 任人 → rèn (let/allow)
 (10, 5): 'rén',  # 人 → rén
 (10, 6): 'zǎi',  # 宰 → zǎi (slaughter)
 (11, 2): 'zhǎng', # 长 in 长满 → zhǎng (grow), not cháng
}
VOCAB = [
 ('托儿', 'tuō r', 'colloquial', 'A plant; a decoy or shill — someone secretly recruited to play a role and fool others. 托 means "to entrust/commission." 托儿 is Beijing slang; in standard Mandarin 托 alone is used. Here: Xia Xue hired a classmate to play fake boyfriend to alarm her parents.'),
 ('假冒', 'jiǎ mào', 'HSK5', 'To impersonate, pass off as; to counterfeit. 假 (fake) + 冒 (pass off as). Common in: 假冒伪劣 (counterfeit and substandard goods). Here used humorously — impersonating a boyfriend, not a criminal act, though treated as one by the father.'),
 ('叫板', 'jiào bǎn', 'colloquial', 'To challenge someone; to call someone\'s bluff; to pick a fight with. Originally from Peking opera (calling out the beat to the orchestra to start a fight scene). 拿这事给你们叫板 = use this situation to challenge/provoke you. Very colloquial, combative register.'),
 ('任人宰割', 'rèn rén zǎi gē', 'idiom', 'To be at others\' mercy; to let people do as they please with you. Literally: "let people slaughter (you) at will." A vivid image of powerlessness. The opposite of 长满刺的小刺猬 (a hedgehog covered in spines) — the contrast the boy draws to describe Xia Xue\'s true character.'),
 ('后妈', 'hòu mā', 'colloquial', 'Stepmother. More colloquial than 继母 (formal). In Chinese cultural discourse, 后妈 carries the fairy-tale stereotype of the cruel stepmother — Xia Xue fears her new stepmother will oppress her, which is the emotional root of her scheme.'),
 ('失去', 'shī qù', 'HSK4', 'To lose (something one previously had). 失去 is permanent or serious loss; contrast with 丢 (to misplace/drop). 失去自由和快乐 = lose freedom and happiness. Collocations: 失去机会 (miss/lose an opportunity), 失去信心 (lose confidence).'),
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
