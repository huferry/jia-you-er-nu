# -*- coding: utf-8 -*-
import os, html
from pypinyin import pinyin, Style

TITLE = "家有儿女 12:10.00 - 12:49.00"
OUT = "家有儿女S01E01_clip_12-10_lesson"
S = [
 ('12:10.00', '这可是妈妈', "This — this is from Mom."),
 ('12:11.00', '为迎接你专门做的', "She made it specially to welcome you."),
 ('12:13.00', '是刘星的妈妈', "It's Liu Xing's mom."),
 ('12:16.00', '来 尝尝我做的茄子', "Here — try the eggplant I made."),
 ('12:19.00', '我不习惯', "I'm not used to it —"),
 ('12:20.00', '在别人的帮助下吃饭', "eating with other people's help."),
 ('12:25.00', '我太爱吃你做的茄子了', "I absolutely love the eggplant you make!"),
 ('12:34.00', '那恐怕得你们习惯我了', "Well then, I'm afraid you'll all have to get used to me."),
 ('12:36.00', '反正我是不会习惯别人的', "Anyway, I'm not going to get used to anyone else."),
 ('12:44.00', '妈 那个八条腿', "Mom, that thing with eight legs —"),
 ('12:46.00', '横着走那个熟了没', "the one that walks sideways — is it cooked yet?"),
 ('12:49.00', '螃蟹呀', "You mean crab!"),
]
# (sentence_index, char_k_position) -> pinyin override
OVERRIDE = {
 # 得 in 得你们习惯我了: modal/obligatory 得 = děi (must/have to), not 得 de (complement marker) or dé (obtain)
 (7, 2): 'děi',   # 恐怕得你们习惯我了 — 得 = děi (have to)
 # 着 in 横着走: manner complement marker = zhe (neutral tone), not zhāo/zháo/zhè
 (10, 1): 'zhe',  # 横着走 — 着 = zhe (manner: walking sideways)
}
VOCAB = [
 ('专门', 'zhuān mén', 'HSK4', 'Specially, specifically, exclusively. 专门做的 = made especially (for you). Compare: 特意 tè yì (deliberately, on purpose — implies effort made); 特别 tè bié (especially — more adjectival). 专门 often modifies the purpose: 专门为你 (specifically for you), 专门学习中文 (study Chinese exclusively/dedicatedly). Very common collocate: 专门来/去 (come/go specifically to).'),
 ('习惯', 'xí guàn', 'HSK3', 'To be used to / accustomed to (verb); a habit (noun). 习惯 + V = be used to doing. 不习惯 = not used to. 习惯别人 = get used to other people. This scene is a wordplay on the word: 多吃点 → rebuttal → 大家互相慢慢习惯 → 那恐怕得你们习惯我了 → 反正我是不会习惯别人的. The repetition builds Xiaoxue\'s character. Compare: 适应 shì yìng (to adapt — more effortful, deliberate change).'),
 ('恐怕', 'kǒng pà', 'HSK4', 'I\'m afraid, probably, I suspect (hedging adverb). 恐怕得你们习惯我了 = I\'m afraid you\'ll have to get used to me. Signals that something is undesirable or unexpected but likely. Compare: 也许 yě xǔ (maybe — neutral); 大概 dà gài (probably — more neutral estimation); 恐怕 implies the speaker foresees something the listener may not want to hear.'),
 ('反正', 'fǎn zhèng', 'HSK4', 'Anyway, regardless, in any case. 反正我是不会习惯别人的 = I\'m not going to adapt to anyone else, period. 反正 dismisses alternatives and states a fixed conclusion. Useful spoken pattern: 反正…就… (whatever the case, the outcome is…). Xiaoxue uses it twice in the episode (also at 11:11), marking her as stubborn and self-certain. Very colloquial; too casual for formal writing.'),
 ('横着走', 'héng zhe zǒu', 'colloquial', 'To walk sideways. 横 = horizontal/sideways; 着 (zhe) = manner complement marker (ongoing state). 横着走 = walking in a horizontal/sideways manner — Xiaoyu\'s charming indirect description of a crab without knowing the word. 着 (zhe) attaches to verbs to indicate manner or ongoing state: 躺着看书 (read lying down), 站着等 (wait standing up). Distinguish from 着 zhāo (move in chess/strategy).'),
 ('八条腿', 'bā tiáo tuǐ', 'everyday', 'Eight legs. 条 is the measure word for long, strip-like things — legs, rivers, roads, fish, trousers. 八条腿横着走那个 = that thing with eight legs that walks sideways. Xiaoyu doesn\'t know the word 螃蟹 (crab) so he describes it. This is a great example of circumlocution (迂回表达) — a useful survival strategy when you don\'t know a word.'),
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
