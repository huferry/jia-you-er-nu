# -*- coding: utf-8 -*-
import os, html
from pypinyin import pinyin, Style

TITLE = "家有儿女 18:30.00 - 19:14.00"
OUT = "家有儿女S01E01_clip_18-30_lesson"
S = [
 ('18:30.00', '你们难道', "Don't you guys—"),
 ('18:31.00', '不想问点什么吗', "—not want to ask me anything?"),
 ('18:34.00', '我刚才干嘛去了', "What I was just doing out there?"),
 ('18:37.00', '你确实应该熟悉熟悉', "You really should get familiar—"),
 ('18:39.00', '这新家的周边环境', "—with the surroundings of this new home."),
 ('18:42.00', '回来的那么早', "You came back so early."),
 ('18:43.00', '也没走多远', "Didn't go very far either."),
 ('18:46.00', '咱们那小区后面有个花园', "There's a garden behind our compound."),
 ('18:48.00', '回头让两个弟弟带你去', "Next time have the two brothers take you there."),
 ('18:51.00', '我现在不想去', "I don't want to go right now."),
 ('18:59.00', '我们以后也能享受 这种待遇吗', "Will we ever get to enjoy this kind of treatment?"),
 ('19:13.00', '耐心 耐心 宽大为怀', "Patience, patience — be magnanimous."),
]
# (sentence_index, char_k_position) -> pinyin override
OVERRIDE = {
 # 干 in "我刚才干嘛去了": 干 = gàn (干嘛 = what for/doing what), not gān (dry)
 # 我(0)刚(1)才(2)干(3)嘛(4)去(5)了(6)
 (2, 3): 'gàn',
 # 为 in "耐心 耐心 宽大为怀": 为 = wéi (to be), not wèi (for)
 # non-space chars: 耐(0)心(1)耐(2)心(3)宽(4)大(5)为(6)怀(7)
 (11, 6): 'wéi',
}
VOCAB = [
 ('难道', 'nán dào', 'HSK4', 'Don\'t tell me…; could it be that…; is it really the case that…? Rhetorical question marker — the speaker expects the answer to be "no." 你们难道不想问点什么吗 = don\'t you guys even want to ask me anything? Signals mild indignation or disbelief. Compare 莫非 (more literary), 该不会 (more tentative).'),
 ('熟悉', 'shú xi', 'HSK4', 'To be familiar with; to get to know. 熟悉熟悉 = get (yourself) familiar (reduplication softens and casualizes). 你应该熟悉熟悉这新家的周边环境 = you should get to know the area around your new home. As an adjective: 我对这里很熟悉 = I\'m very familiar with this place. The reduplication V一V or VV implies a light, brief action.'),
 ('周边环境', 'zhōu biān huán jìng', 'HSK5', 'Surrounding environment, the area around (a place). 周边 = surrounding, peripheral; 环境 = environment, surroundings. Used here about the neighborhood around the new home. Common collocations: 周边设施 (nearby facilities), 生态环境 (ecological environment), 学习环境 (learning environment).'),
 ('小区', 'xiǎo qū', 'colloquial', 'Residential compound, housing estate. The standard word for a gated or semi-gated apartment/housing community in Chinese cities. 咱们那小区 = our compound / our estate. Common in everyday speech: 小区里面 (inside the compound), 小区门口 (at the compound gate). Not to be confused with 社区 (community — broader term).'),
 ('待遇', 'dài yù', 'HSK5', 'Treatment, benefits, perks. 这种待遇 = this kind of treatment. Here the boys are jealously noting that Xiaoxue is being handled with kid gloves. 待遇 also refers to salary/compensation in work contexts: 薪资待遇 (salary and benefits). The irony in this scene: the boys want the VIP treatment, but dad\'s response is just 耐心 宽大为怀.'),
 ('享受', 'xiǎng shòu', 'HSK4', 'To enjoy; to have the benefit of. 享受这种待遇 = enjoy this kind of treatment/perk. As a noun: 这是一种享受 = this is a pleasure/luxury. Common collocations: 享受生活 (enjoy life), 享受权利 (enjoy rights/privileges). Slightly ironic here — the boys use an elevated word to mock-protest the unequal treatment.'),
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
