# -*- coding: utf-8 -*-
import os, html
from pypinyin import pinyin, Style

TITLE = "家有儿女 S01E02 15:57.24 - 16:19.24"
OUT = "家有儿女S01E02_clip_15-57_lesson"
S = [
 ('15:57.24', '小雪都能和自己的狂野男孩约会', "Xiaoxue can even go on dates with her own Wild Boy —"),
 ('16:00.24', '我怎么就不能见见自己的野蛮女友啊', "so why can't I meet my own Savage Girlfriend?"),
 ('16:03.24', '我告诉你', "Let me tell you something."),
 ('16:05.24', '你要是敢有野蛮女友', "If you dare to have a Savage Girlfriend,"),
 ('16:07.24', '你就会突然发现', "you'll suddenly discover"),
 ('16:09.24', '你有一个 野蛮又狂野的母亲', "that you have a savage and wild mother!"),
 ('16:12.24', '不公平', "That's not fair!"),
 ('16:13.24', '不公平', "Not fair!"),
 ('16:14.24', '小雨快开门', "Xiaoyu, open the door quickly!"),
 ('16:16.24', '干嘛', "What for?"),
 ('16:17.24', '不公平', "Not fair!"),
 ('16:18.24', '我跟她闭嘴', "I need to shut her up."),
]
# (sentence_index, char_k_position) -> pinyin override
OVERRIDE = {
 (9, 0): 'gàn',    # 干 in 干嘛 → gàn (do), not gān
}
VOCAB = [
 ('约会', 'yuē huì', 'HSK4', 'To go on a date; a date, an appointment. 约会 implies a romantic or social meeting arranged in advance. Here used by Liu Xing to argue for equal treatment: if his sister can date, why can\'t he? Collocations: 约会对象 (date/partner), 赴约 (keep an appointment). Note: 约 alone can mean "arrange to meet" in a broader sense.'),
 ('野蛮', 'yě mán', 'HSK5', 'Savage, barbaric, rough. Originally: uncivilized/primitive (野蛮人 = savage). Here used as a playful label for a rough-and-tumble girlfriend — a pop-culture reference to the 2001 Korean film 엽기적인 그녀 (野蛮女友 in Chinese). The word has been domesticated into affectionate slang for a feisty girl. Contrast: 文明 (civilized).'),
 ('突然', 'tū rán', 'HSK3', 'Suddenly, all of a sudden. 会突然发现 = will suddenly find out. 突然 as an adverb precedes the verb. As an adjective: 突然的变化 (sudden change). Compare: 忽然 (suddenly — more literary and for internal/mental shifts), 猛然 (suddenly — more physical/violent). 突然 is the most common spoken form.'),
 ('不公平', 'bù gōng píng', 'HSK3', 'Unfair, unjust. 公平 = fair, equal. Liu Xing\'s repeated cry of 不公平 is both his genuine complaint and a comic refrain. Note 不 sandhi: before 公 (1st tone) it stays bù. Collocations: 对…不公平 (unfair to...), 不公平竞争 (unfair competition). The double standard — one rule for sister, another for brother — is the episode\'s central theme.'),
 ('要是…就…', 'yào shì…jiù…', 'grammar', 'Conditional pattern: "If… then…". 要是 is a spoken variant of 如果/假如. 你要是敢有野蛮女友，你就会突然发现… = "If you dare to have a Savage Girlfriend, then you\'ll suddenly discover…" The 就 in the result clause is mandatory in this pattern. Very common in conversational threats, warnings, and bargains.'),
 ('闭嘴', 'bì zuǐ', 'colloquial', 'Shut up! Close one\'s mouth. 闭 = close, 嘴 = mouth. Direct and rude when aimed at someone; here Liu Xing says "我跟她闭嘴" meaning he needs to make his mom stop talking — using it about a third person is slightly softer. Collocations: 叫他闭嘴 (tell him to shut up). Compare: 别说了 (stop talking, softer).'),
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
