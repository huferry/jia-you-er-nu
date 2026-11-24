# -*- coding: utf-8 -*-
import os, html
from pypinyin import pinyin, Style

TITLE = "家有儿女 S01E02 04:06.32 - 04:52.92"
OUT = "家有儿女S01E02_clip_04-06_lesson"
S = [
 ('04:06.32', '她说我结婚离婚又结婚', "She said I married, divorced, then married again."),
 ('04:08.12', '你说这孩子', "What do you make of this kid?"),
 ('04:09.44', '你可不是结婚离婚又结婚嘛', "But you DID marry, divorce, and marry again, didn't you?"),
 ('04:14.04', '这孩子说得也没错啊', "The kid's not wrong, you know."),
 ('04:26.04', '喝口冰水 摆摆火', "Have some ice water — cool yourself down."),
 ('04:33.12', '我摔了它', "I want to smash it."),
 ('04:34.96', '摔吧', "Go ahead, smash it."),
 ('04:36.40', '塑料的', "It's plastic."),
 ('04:37.68', '意味着让你摔的', "Meaning: it was made for you to smash."),
 ('04:41.84', '没玻璃的摔得过瘾', "Nothing beats smashing something without glass — really satisfying."),
 ('04:45.36', '我告诉你啊 夏东海', "Let me tell you, Xia Donghai —"),
 ('04:48.24', '父母越反对孩子也跟你拧着来', "The more parents object, the more kids dig in and push back."),
]
# (sentence_index, char_k_position) -> pinyin override
OVERRIDE = {
 (4, 3): 'bǎi',  # 摆 in 摆火 → bǎi; actually 消气 is the standard; 摆火 = 摆 tone 3 — default ok
 (11, 5): 'nǐng', # 拧 in 拧着来 → nǐng (stubborn, go against), not níng (twist)
 (11, 6): 'zhe',  # 着 as suffix in 拧着来 → zhe (neutral), not zháo
}
VOCAB = [
 ('摔', 'shuāi', 'HSK4', 'To smash/throw/drop (something) down hard. 摔了它 = smash it. 摔 implies a forceful throw downward, often out of anger. Compare: 砸 (smash by striking), 扔 (throw away). The substitution of a plastic glass here is a classic calming gesture.'),
 ('过瘾', 'guò yǐn', 'colloquial', 'Satisfying, to really scratch the itch — to fully indulge a craving or desire. 摔得过瘾 = satisfying to smash. 过 = pass through; 瘾 = addiction/craving. Very colloquial. Compare: 爽 (feels great), 痛快 (exhilarating). Often used for physical satisfaction.'),
 ('拧着来', 'nǐng zhe lái', 'colloquial', 'To stubbornly go against, to do the opposite out of defiance. 拧 (nǐng) = to be contrary/obstinate. 跟你拧着来 = dig in against you. This is a key parenting insight in the scene: opposition breeds rebellion. Compare: 对着干 (deliberately oppose), 较劲 (lock horns).'),
 ('着 (zhe)', 'zhe', 'grammar', '着 as a durative/manner suffix: marks ongoing state or manner. 拧着来 = come at it in a stubborn manner. Distinct from 着 (zháo, to touch/achieve) and 着 (zhāo, a move in chess). In 看着/说着/跟着, 着 = zhe (neutral tone), indicating sustained action.'),
 ('越…也…', 'yuè…yě…', 'grammar', 'The more… the more… (asymmetric variant). Standard pattern: 越…越…; here 越反对…也跟你拧着来 uses 也 instead of the second 越 for a slightly more colloquial feel: "the more [you] oppose, [they] also push back." Compare: 越来越 (more and more over time).'),
 ('消火', 'xiāo huǒ', 'colloquial', 'To cool down anger; lit. extinguish the fire. 摆摆火 (here transcribed) likely = 消消火 = calm the anger a bit. 火 metaphorically = anger (怒火). Related: 发火 (to flare up in anger), 火气 (angry energy), 消气 (let the anger go). Compare: 冷静 (calm down, more neutral).'),
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
