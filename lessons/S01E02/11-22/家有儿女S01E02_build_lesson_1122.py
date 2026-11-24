# -*- coding: utf-8 -*-
import os, html
from pypinyin import pinyin, Style

TITLE = "家有儿女 S01E02 11:22.08 - 11:55.68"
OUT = "家有儿女S01E02_clip_11-22_lesson"
S = [
 ('11:22.08', '我们认为这是你自己的事情', "We think this is entirely your own business."),
 ('11:24.00', '我们不再干涉', "We won't interfere anymore."),
 ('11:28.20', '因为我们认为你的综合素质', "Because we believe your overall qualities"),
 ('11:30.60', '完全可以应付这方面的问题', "are fully capable of handling this."),
 ('11:34.24', '我代表你的妈妈', "On behalf of your mother,"),
 ('11:35.48', '明确表一下态', "I want to clearly state our position:"),
 ('11:37.08', '你在这个家里有完全的自由', "you have complete freedom in this house."),
 ('11:39.88', '只要是你认为正确的事情', "Whatever you consider to be right,"),
 ('11:42.12', '想怎么做就这么做', "do it however you want."),
 ('11:44.24', '我们准备对你实行零限制', "We are prepared to impose zero restrictions on you."),
 ('11:51.80', '你在这个家就是一个自由的小小小小鸟', "In this house you are a free little-little-little bird."),
 ('11:55.68', '想要飞多高就可以飞多高', "Fly as high as you want to fly."),
]
# (sentence_index, char_k_position) -> pinyin override
OVERRIDE = {
 (1, 4): 'gān',  # 干 in 干涉 → gān (interfere), not gàn (do/work)
                 # sentence: 我们不再干涉 → 我(0)们(1)不(2)再(3)干(4)涉(5)
}
VOCAB = [
 ('干涉', 'gān shè', 'HSK4+', 'To interfere, meddle. 不再干涉 = won\'t interfere anymore. Note: 干 here is gān (the intervene/meddle reading), not gàn (do/work). Compare: 干扰 (disrupt/interfere with a signal); 插手 (stick one\'s hand in, informal meddling). 干涉 is more forceful/formal than 插手.'),
 ('综合素质', 'zōng hé sù zhì', 'HSK5+', 'Overall/comprehensive qualities, all-round capability. 综合 = comprehensive, combined; 素质 = innate + cultivated qualities, character, capability. Common in Chinese education/HR/parenting discourse: 综合素质好 = well-rounded. The father is using bureaucratic language to deliver his compliment — comic register mismatch.'),
 ('应付', 'yìng fu', 'HSK4', 'To deal with, cope with, handle. 应付这方面的问题 = handle this kind of issue. Second sense (negative): to do something perfunctorily, just enough to get by (应付了事 = do it in a slapdash way). Context determines which sense is meant.'),
 ('表态', 'biǎo tài', 'HSK5', 'To state/declare one\'s position or stance. 明确表一下态 = clearly declare our position. 表 = express; 态 = attitude/stance. Common in political/official speech but here used by a dad in family negotiations — humorously formal register. Near-synonym: 表明立场 (more wordy).'),
 ('实行', 'shí xíng', 'HSK4', 'To implement, put into practice, carry out (a policy/measure). 实行零限制 = implement/enforce zero restrictions. Compare 实现 (realize/achieve a goal — the outcome); 实行 focuses on putting something into practice/enforcing it (the process).'),
 ('零限制', 'líng xiàn zhì', 'colloquial', 'Zero restrictions. 零 = zero; 限制 = restriction/limit. Comic exaggeration — the parents offer Xiaoxue total freedom as a manipulation tactic, so she\'ll feel grateful and naturally want to please them. The plan immediately backfires: she just leaves.'),
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
