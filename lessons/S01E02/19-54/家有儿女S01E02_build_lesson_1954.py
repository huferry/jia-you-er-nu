# -*- coding: utf-8 -*-
import os, html
from pypinyin import pinyin, Style

TITLE = "家有儿女 S01E02 19:54.24 - 20:32.24"
OUT = "家有儿女S01E02_clip_19-54_lesson"
S = [
 ('19:56.24', '我会尽快让她回归中国国情呗', "I'll get her back in line with Chinese norms as soon as possible."),
 ('19:59.24', '多多 我爱你', "Duoduo, I love you!"),
 ('20:01.24', '这太不像话了', "This is absolutely outrageous!"),
 ('20:05.24', '不得不马上逃离这里', "We have no choice but to flee this place immediately!"),
 ('20:08.24', '希望你对你们家的小孩子', "I hope you will discipline your child"),
 ('20:09.24', '严加管教', "with the strictest supervision."),
 ('20:22.24', '你做的太过分了', "What you did was way too much!"),
 ('20:26.24', '我就是做我喜欢的事', "I was just doing what I like to do —"),
 ('20:28.24', '跟你一样啊', "just like you!"),
 ('20:29.24', '你能跟我比吗你', "Can you even compare yourself to me?"),
 ('20:30.24', '那你等刘星晚上回来', "Then wait until Liu Xing gets home tonight —"),
 ('20:32.24', '你去管他', "you go and deal with him yourself."),
]
# (sentence_index, char_k_position) -> pinyin override
OVERRIDE = {
 (0, 1): 'huì',   # 会 → huì
 (0, 2): 'jǐn',   # 尽 in 尽快 → jǐn (as fast as possible), not jìn (exhausted)
 (0, 7): 'guī',   # 归 in 回归 → guī
 (2, 1): 'tài',   # 太 → tài
 (3, 0): 'bù',    # 不 in 不得不 → bù
 (3, 1): 'dé',    # 得 in 不得不 → děi (must), but here 不得不 = cannot but → de neutral? No: 不得不 = "have no choice but to" → bùdébù, 得 = děi
 (5, 0): 'yán',   # 严 in 严加 → yán
 (6, 2): 'tài',   # 太 → tài
 (6, 3): 'guò',   # 过 in 过分 → guò
 (8, 1): 'gēn',   # 跟 → gēn
 (9, 1): 'néng',  # 能 → néng
 (9, 2): 'gēn',   # 跟 → gēn
}
VOCAB = [
 ('国情', 'guó qíng', 'HSK5', 'National conditions, the state of a country / its social norms and realities. 中国国情 = "the Chinese context/norms." A common phrase in political and social discourse, often used to explain why something that works elsewhere doesn\'t apply to China. Here used humorously.'),
 ('不像话', 'bù xiàng huà', 'colloquial', 'Outrageous, absurd, out of line. Literally "doesn\'t resemble speech/words" → too improper to even describe. 这太不像话了 = "this is simply unacceptable." Colloquial; near-synonym 太过分了 (too much/excessive) is used moments later in the same scene.'),
 ('不得不', 'bù dé bù', 'grammar', '"Have no choice but to…" — a double-negative structure meaning compulsion without alternatives. 不得不 + V = "must V whether one likes it or not." Near-synonym: 只好 (can only…, used resignedly). 不得不 is slightly more formal/dramatic.'),
 ('严加管教', 'yán jiā guǎn jiào', 'formal', 'To discipline strictly, to bring up with rigorous supervision. 严 (strict) + 加 (apply/increase) + 管教 (discipline/raise). A formal phrase used in letters, official complaints, or scoldings. The father uses it here as a parting shot to the family.'),
 ('过分', 'guò fèn', 'HSK4', 'Excessive, going too far, out of line. 太过分了 = "that\'s way too much!" A very common spoken expression of reproach. 过分 can be used as adjective or predicate. Near-synonym: 过头 (gone too far, more colloquial); 不像话 (outrageous, same register).'),
 ('尽快', 'jǐn kuài', 'HSK3', 'As quickly as possible, at the earliest opportunity. Note: 尽 here is jǐn (to the utmost), NOT jìn (to exhaust/finish). Common in instructions and promises: 我会尽快处理 = "I\'ll deal with it ASAP." Near-synonym: 赶快 (hurry up — imperative urging); 尽快 is more polite/formal.'),
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
