# -*- coding: utf-8 -*-
import os, html
from pypinyin import pinyin, Style

TITLE = "家有儿女 S01E02 19:00.24 - 19:50.24"
OUT = "家有儿女S01E02_clip_19-00_lesson"
S = [
 ('19:01.24', '你再重复一遍', "Say it again — repeat it once more."),
 ('19:02.24', '她当时是如何对你讲的', "What exactly did she say to you at the time?"),
 ('19:06.24', '她让我长大以后', "She told me that when I grow up,"),
 ('19:08.24', '用这鸡毛换钻石戒指', "I should use this chicken feather to exchange for a diamond ring."),
 ('19:11.24', '你们都听到了吧', "You all heard that, right?"),
 ('19:12.24', '小孩子的话 您不能当真', "You can't take a child's words seriously."),
 ('19:14.24', '我是当时喜欢多多的', "I genuinely liked Duoduo at the time."),
 ('19:18.24', '这个小花花公子', "This little playboy!"),
 ('19:19.24', '你们到底是管还是不管', "Are you going to do something about this or not?"),
 ('19:22.24', '您听我解释', "Please let me explain."),
 ('19:25.24', '不是您想象的那样', "It's not what you're imagining."),
 ('19:28.24', '这个事情难道是我自己想象出来', "Are you saying I made this whole thing up?"),
]
# (sentence_index, char_k_position) -> pinyin override
OVERRIDE = {
 (0, 1): 'zài',   # 再 → zài (again)
 (0, 2): 'chóng', # 重 in 重复 → chóng (repeat), not zhòng
 (1, 2): 'rú',    # 如 in 如何 → rú
 (2, 3): 'zhǎng', # 长 in 长大 → zhǎng (grow), not cháng
 (3, 1): 'zhè',   # 这 → zhè
 (3, 2): 'jī',    # 鸡 → jī
 (5, 4): 'nín',   # 您 → nín
 (5, 5): 'néng',  # 能 → néng
 (5, 6): 'dàng',  # 当 in 当真 → dàng (treat as), not dāng
 (6, 1): 'shì',   # 是 → shì
 (6, 2): 'dāng',  # 当 in 当时 → dāng (at that time)
 (8, 3): 'dǐ',    # 底 in 到底 → dǐ
 (11, 3): 'nán',  # 难 in 难道 → nán
}
VOCAB = [
 ('重复', 'chóng fù', 'HSK3', 'To repeat, say/do again. 重 here is chóng (again/re-), NOT zhòng (heavy/important). Contrast: 重要 (zhòng yào, important), 重复 (chóng fù, repeat). Very common: 重复一遍 = "say it one more time."'),
 ('鸡毛换钻石戒指', 'jī máo huàn zuàn shí jiè zhi', 'phrase', 'Exchange a chicken feather for a diamond ring. This absurd promise is 小雨\'s childish romantic gesture — giving 多多 a chicken feather and vowing to exchange it for a ring when he grows up. 换 = to swap/exchange; 戒指 = ring (finger ring).'),
 ('当真', 'dàng zhēn', 'phrase', 'To take seriously, treat as real. 不能当真 = "you can\'t take it at face value." Note 当 here is dàng (to treat as / regard as), NOT dāng (to be / when). Contrast: 认真 (take seriously, do carefully) — 当真 implies credulity, 认真 implies diligence.'),
 ('小花花公子', 'xiǎo huā huā gōng zǐ', 'colloquial', 'Little playboy / young lothario. 花花公子 (huāhua gōngzǐ) = Playboy — a womanizer, flirt, dandy. Adding 小 makes it contemptuous and comic: "this little two-timing kid." The father uses it to condemn 小雨\'s multiple romantic ventures.'),
 ('到底', 'dào dǐ', 'HSK3', 'On earth, after all, in the end — adds urgency or exasperation to a question. 你到底管还是不管？ = "Are you going to handle this or NOT?" Interchangeable in questions with 究竟 (more literary). Position: before the verb.'),
 ('难道', 'nán dào', 'HSK4', 'Don\'t tell me…? Surely not…? A rhetorical question marker implying the speaker finds the implied answer absurd. 难道是我自己想象出来的？ = "Are you seriously suggesting I made it up?" Always forms a rhetorical question; answer expected: "of course not."'),
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
