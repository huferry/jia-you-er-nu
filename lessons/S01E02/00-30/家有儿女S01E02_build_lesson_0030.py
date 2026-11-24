# -*- coding: utf-8 -*-
import os, html
from pypinyin import pinyin, Style

TITLE = "家有儿女 S01E02 00:30.00 - 01:04.00"
OUT = "家有儿女S01E02_clip_00-30_lesson"
S = [
 ('00:30.00', '诶诶诶 狂野男孩', "Hey hey hey, wild boys!"),
 ('00:32.00', '你会为了小雪和她的爸爸决斗吗', "Would you fight a duel for Xiaoxue, against her father?"),
 ('00:35.00', '第四十八页 几行几行什么的', "Page forty-eight, some line or other..."),
 ('00:39.00', '那是什么东西啊', "What on earth is that?"),
 ('00:41.00', '是爱情誓言吧', "It's a love vow, isn't it!"),
 ('00:43.00', '不不不 不是不是', "No no no, it's not, it's not!"),
 ('00:44.00', '我还先到外面待会吧', "I'll head outside for a bit first."),
 ('00:46.00', '哎呦', "Ouch!"),
 ('00:49.00', '别怕 我们会保护你的', "Don't be afraid — we'll protect you!"),
 ('00:55.00', '诶诶 干嘛呢这是', "Hey! What do you think you're doing?"),
 ('00:57.00', '反正这句话我们以后也会对女孩子说的', "Anyway, we'll be saying this kind of thing to girls someday."),
 ('01:02.00', '我们长大了也会狂野', "When we grow up, we'll be wild too!"),
]
# (sentence_index, char_k_position) -> pinyin override
# k counts non-space characters only (spaces in text are skipped)
OVERRIDE = {
 (0, 0): 'ēi', (0, 1): 'ēi', (0, 2): 'ēi',  # 诶诶诶 — ēi (1st, calling attention), not éi/ěi
 (1, 2): 'wèi',   # 为 in 为了 → wèi (for/in order to), not wéi
 (2, 6): 'háng', (2, 8): 'háng',  # 行 as háng (line/row of text), not xíng (OK/walk)
 (6, 6): 'dāi',   # 待 in 待会 → dāi (stay/hang around), not dài (treat)
 (9, 0): 'ēi', (9, 1): 'ēi',  # 诶诶 — same ēi
 (9, 2): 'gàn',   # 干 in 干嘛 → gàn (do), not gān (dry)
 (11, 2): 'zhǎng',  # 长 in 长大 → zhǎng (grow), not cháng (long)
}
VOCAB = [
 ('狂野', 'kuángyě', 'colloquial', 'Wild, feral, unrestrained. Used here by young boys as aspirational cool-speak. Collocation: 狂野的个性 (wild personality), 狂野西部 (Wild West). Softer near-synonym: 野 alone; stronger: 疯狂.'),
 ('决斗', 'jué dòu', 'HSK5+', 'A formal duel; loosely any decisive face-off. 为…决斗 = duel for someone. The classical romance trope — fighting for a girl\'s honor — here used humorously by kids who\'ve been reading too many adventure novels.'),
 ('誓言', 'shì yán', 'HSK5', 'Oath, solemn vow. 爱情誓言 = love pledge. More dramatic/literary than 保证 (guarantee) or 承诺 (promise). The joke: the boys found it in a novel (page 48, some line) and are reciting it like a script.'),
 ('反正', 'fǎn zhèng', 'HSK4', 'Anyway, in any case — dismisses prior objections and asserts a fixed conclusion. 反正…的 = "[it] will… regardless." Compare: 总之 (in short, more formal/written). Very common in spoken argument and confident declarations.'),
 ('保护', 'bǎo hù', 'HSK3', 'To protect, guard. Core HSK3 word. 会保护你的 uses 会…的 for confident reassurance (see below). Collocations: 保护环境, 保护隐私, 保护动物.'),
 ('会…的', 'huì…de', 'grammar', 'Confident future assertion or reassurance. 的 at the end adds certainty: 我们会保护你的 = "We WILL protect you." vs plain 我们会保护你. Reappears in line 11: 我们以后也会对女孩子说的. Very common in comforting, bragging, or determined statements.'),
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
