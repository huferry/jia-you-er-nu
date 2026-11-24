# -*- coding: utf-8 -*-
import os, html
from pypinyin import pinyin, Style

TITLE = "家有儿女 S01E02 16:27.24 - 17:00.24"
OUT = "家有儿女S01E02_clip_16-27_lesson"
S = [
 ('16:27.24', '你干什么', "What are you doing?"),
 ('16:28.24', '请看', "Please observe."),
 ('16:31.24', '只许州官放火', "Only officials are allowed to set fires —"),
 ('16:33.24', '不许百姓点灯', "common people are not even allowed to light a lamp."),
 ('16:40.24', '什么意思', "What does that mean?"),
 ('16:41.24', '你什么意思', "What do YOU mean?"),
 ('16:42.24', '我说你放火', "I'm saying YOU are setting fires."),
 ('16:56.24', '什么意思', "What's the meaning of this?"),
 ('16:58.24', '记住这个成语吧', "Remember this idiom."),
 ('16:58.24', '只许州官放火 不许百姓点灯', "Officials may set fires; common folk may not even light lamps."),
 ('17:00.24', '以后在咱们家只能够说', "From now on in our house, you can only say:"),
 ('17:03.24', '只许姐姐放火 不许弟弟点灯', "Sisters may set fires; little brothers may not light lamps."),
]
# (sentence_index, char_k_position) -> pinyin override
OVERRIDE = {
 (0, 1): 'gàn',    # 干 in 干什么 → gàn (do), not gān
 (7, 0): 'shén',   # 什么意思 — 什 is shén in 什么; pypinyin usually handles this
}
OVERRIDE = {
 (0, 1): 'gàn',    # 干 in 干什么 → gàn
}
VOCAB = [
 ('只许州官放火，不许百姓点灯', 'zhǐ xǔ zhōu guān fàng huǒ, bù xǔ bǎi xìng diǎn dēng', 'chengyu', 'Officials may set fires; common people may not even light lamps. A classical idiom (成语) from the Song Dynasty about hypocrisy and double standards in power. Here Liu Xing literally acts it out with a candle to make his point about unfair treatment. The episode then remixes it as: 只许姐姐放火，不许弟弟点灯. Collocations: 这不是只许…不许… (isn\'t this a case of…?).'),
 ('成语', 'chéng yǔ', 'HSK4', 'Four-character set phrase / idiom. 成 = established, 语 = language. Chinese has thousands of these, usually from classical texts or historical anecdotes. They compress a whole story into 4 characters. 记住这个成语 = "remember this idiom." Liu Xing shows off by citing a real 成语 to win an argument — a clever rhetorical move.'),
 ('州官', 'zhōu guān', 'literary', 'A prefectural official (historical). In ancient China, 州 was an administrative region; 官 = official. The idiom contrasts 州官 (privileged authority) with 百姓 (ordinary people). Today used only in this idiom and similar contexts — not an active word. The power hierarchy it encodes remains culturally resonant.'),
 ('百姓', 'bǎi xìng', 'HSK4', 'Common people, ordinary citizens. 百 = hundred (metaphor for "all"), 姓 = surname. Literally "the hundred surnames" — meaning all the common folk. Formal/literary feel; in speech, 老百姓 (old hundred-surnames) is more common and affectionate. Compare: 人民 (the people, political register), 市民 (city residents).'),
 ('只许…不许…', 'zhǐ xǔ…bù xǔ…', 'grammar', 'Allowed only for X but not for Y — a pattern expressing double standards. 只许 = only permit; 不许 = do not permit. The pattern can be extended: 只许你…不许我… (only you are allowed…not me…). Very useful for expressing unfairness or irony. 只 = only (restrictive); compare 仅 (only, more formal/written).'),
 ('放火', 'fàng huǒ', 'HSK4+', 'To set fire, to commit arson. 放 = release/set, 火 = fire. Here used both literally (Liu Xing lights a candle dramatically) and figuratively (Xiaoxue making trouble). Collocations: 放火烧 (set fire to and burn), 放火犯 (arsonist). Contrast: 点灯 (light a lamp) — the two halves of the idiom frame the power imbalance perfectly.'),
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
