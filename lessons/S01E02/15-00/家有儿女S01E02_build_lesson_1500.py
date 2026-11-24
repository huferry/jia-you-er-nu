# -*- coding: utf-8 -*-
import os, html
from pypinyin import pinyin, Style

TITLE = "家有儿女 S01E02 15:00.24 - 15:49.24"
OUT = "家有儿女S01E02_clip_15-00_lesson"
S = [
 ('15:00.24', '睡吧', "Let's sleep."),
 ('15:02.24', '我的爱情 好像一把火', "My love is like a blazing fire,"),
 ('15:06.24', '染上了整个沙漠', "spreading across the whole desert."),
 ('15:08.24', '这女儿刚安静下来', "Just as the daughter finally quieted down,"),
 ('15:09.24', '是她儿子又闹上来', "it's her son making noise again."),
 ('15:22.24', '停', "Stop!"),
 ('15:23.24', '干什么呢你们大半夜的', "What are you doing in the middle of the night?"),
 ('15:34.24', '妈我跟您商量件事', "Mom, I want to discuss something with you."),
 ('15:36.24', '您给点资金成吗', "Can you give me some funding?"),
 ('15:38.24', '我想把这玩意染成绿的', "I want to dye this thing green."),
 ('15:45.24', '让刘欣把话说完吧', "Let Liu Xing finish speaking."),
 ('15:47.24', '你还想要干什么呀', "What else do you want to do?"),
]
# (sentence_index, char_k_position) -> pinyin override
OVERRIDE = {
 (6, 3): 'gàn',    # 干 in 干什么 → gàn (do), not gān (dry)
 (11, 4): 'gàn',   # 干 in 想干什么 → gàn
}
VOCAB = [
 ('大半夜', 'dà bàn yè', 'colloquial', 'The middle of the night, deep in the night. A spoken intensifier: 大 amplifies 半夜 (midnight). "What are you doing 大半夜?" implies it\'s outrageous to be this loud this late. Compare: 深夜 (deep night, more literary/formal), 半夜三更 (the dead of night, 4-character set phrase). Common in scolding.'),
 ('商量', 'shāng liáng', 'HSK3', 'To discuss, consult. 跟…商量件事 = discuss something with someone. Implies a two-way conversation seeking agreement, softer than 要求 (demand) or 通知 (notify). Note: 商量 requires a person object (跟你商量), unlike 讨论 which can take a topic (讨论这个问题). Here Liu Xing uses it strategically to soften an outrageous request.'),
 ('资金', 'zī jīn', 'HSK5', 'Funds, capital. A formal/business word — hilariously misused by the boy to ask his mom for pocket money to dye his hair. The register gap (formal financial term for a child\'s whim) is the joke. Normal spoken alternative: 钱 (money) or 零用钱 (pocket money). Collocations: 资金不足 (insufficient funds), 筹集资金 (raise funds).'),
 ('染', 'rǎn', 'HSK5', 'To dye, to color; also to infect/taint. 染成绿的 = dye it green. 染头发 = dye hair. The same character appears earlier in 染上了整个沙漠 (spread across the desert) — a clever echo: the song\'s "love spreading like fire" and the boy\'s literal request to "dye" something both use 染.'),
 ('玩意', 'wán yì', 'colloquial', 'Thing, stuff, gadget — informal and slightly dismissive. 这玩意 = this thing. Used here by Liu Xing about his hair (!) — calling his own hair "this thing" shows casual self-mockery. Compare: 东西 (thing, neutral), 玩意儿 (more Beijing-accented, with 儿化). Avoid in formal writing.'),
 ('闹', 'nào', 'HSK3', 'To make noise, cause trouble, kick up a fuss. 又闹上来 = started making a ruckus again. 上来 as directional complement here means the noise/trouble has resumed/risen. Collocations: 闹笑话 (make a laughingstock of oneself), 闹情绪 (throw a tantrum), 闹钟 (alarm clock — the clock that "makes noise"). Very expressive verb.'),
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
