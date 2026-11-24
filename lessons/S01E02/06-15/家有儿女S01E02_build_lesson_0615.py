# -*- coding: utf-8 -*-
import os, html
from pypinyin import pinyin, Style

TITLE = "家有儿女 S01E02 06:15.96 - 06:57.08"
OUT = "家有儿女S01E02_clip_06-15_lesson"
S = [
 ('06:15.96', '站住', "Stop right there!"),
 ('06:18.80', '很高兴认识你', "Very pleased to meet you."),
 ('06:21.32', '四十八页三道十六行什么意思啊', "Page forty-eight, question three, line sixteen — what does that mean?"),
 ('06:24.60', '是哪本书的', "Which book is it from?"),
 ('06:28.52', '是大众情人', "Is it 'The Crowd's Sweetheart'?"),
 ('06:30.16', '还是恋爱绝招', "Or 'Secret Moves in Love'?"),
 ('06:36.08', '听好了', "Listen up."),
 ('06:37.16', '作为夏雪的父亲', "As Xiaoxue's father,"),
 ('06:38.76', '我是绝不会允许你们这个年龄谈恋爱的', "I absolutely will not allow anyone your age to date."),
 ('06:43.52', '你先等一会啊', "Just wait a moment."),
 ('06:44.44', '你先消消气', "First calm yourself down a bit."),
 ('06:46.20', '他爸脾气不好', "His dad has a bad temper."),
]
# (sentence_index, char_k_position) -> pinyin override
OVERRIDE = {
 (2, 3): 'dào',  # 道 in 三道 → dào (measure word for problems/questions)
 (8, 2): 'jué',  # 绝 in 绝不 → jué (absolutely), default ok
 (10, 2): 'xiāo', # 消 in 消消气 → xiāo (extinguish/dispel), default ok
 (11, 3): 'pí',  # 脾 in 脾气 → pí (spleen/temperament), default ok
}
VOCAB = [
 ('站住', 'zhàn zhù', 'colloquial', 'Stop! Halt! Used as an imperative command to stop someone moving. 住 as a resultative complement = successfully held in place. Compare: 停下 (stop what you\'re doing), 别动 (don\'t move). 站住 is specifically for stopping someone who is walking/leaving.'),
 ('绝不', 'jué bù', 'formal', 'Absolutely not, under no circumstances. 绝 = absolutely/completely. 绝不会允许 = will absolutely not permit. Much stronger than 不会 alone. Used in firm declarations. Compare: 决不 (same meaning, 决 = resolved), 永远不 (never ever). Both 绝不 and 决不 are correct.'),
 ('允许', 'yǔn xǔ', 'HSK4', 'To permit, allow. More formal than 让 (let) or 准 (approve). 我不会允许你们 = "I won\'t allow you." Collocations: 允许…进入 (permit entry), 经…允许 (with permission of). The double 不会允许 + 绝 stresses the absoluteness of the refusal.'),
 ('消气', 'xiāo qì', 'colloquial', 'To let anger go, to calm down. 消 = dispel/extinguish; 气 = anger (breath/energy). 消消气 (reduplicated verb) = calm down a little. Similar: 消火 (extinguish the fire [of anger]), 息怒 (formal: suppress anger). Reduplication softens the command.'),
 ('脾气', 'pí qi', 'HSK3', 'Temper, disposition. 脾气不好 = has a bad temper. 发脾气 = to lose one\'s temper. The 脾 (spleen) in Chinese medicine was associated with emotion regulation — hence this compound. Compare: 性格 (character, more permanent), 情绪 (mood, more temporary).'),
 ('作为…', 'zuò wéi…', 'grammar', 'As / in the capacity of. 作为夏雪的父亲 = "As Xiaoxue\'s father [I…]" Introduces a role or identity that justifies the action following. More formal than 我是夏雪的父亲，所以…. Used in both formal writing and elevated spoken rhetoric. Compare: 以…身份 (in the capacity of).'),
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
