# -*- coding: utf-8 -*-
import os, html
from pypinyin import pinyin, Style

TITLE = "家有儿女 S01E02 03:16.44 - 04:05.04"
OUT = "家有儿女S01E02_clip_03-16_lesson"
S = [
 ('03:16.44', '出趟国还把我妈给弄掉了', "You went abroad and even managed to lose my mum."),
 ('03:22.24', '我还没从你的离婚阴影中清醒过来', "I still haven't recovered from the shadow of your divorce."),
 ('03:28.00', '你又给我找了一个好吗', "And now you've gone and found me another one, huh?"),
 ('03:32.60', '这对我的幼小心灵是多么大的伤害啊', "What a huge wound this is to my young, tender heart!"),
 ('03:35.68', '你懂不懂啊', "Do you even get it?"),
 ('03:43.68', '不是不说我吗', "Weren't you NOT going to lecture me?"),
 ('03:45.52', '我是说你', "I'm talking about YOU."),
 ('03:48.40', '你不应该交男朋友', "You shouldn't be dating."),
 ('03:50.72', '我不要你管', "I don't need you telling me what to do."),
 ('03:52.68', '就许你结婚离婚再结婚', "You're allowed to marry, divorce, and marry again —"),
 ('03:55.00', '我交个男朋友都不行啊', "— but I can't even have a boyfriend?"),
 ('04:03.44', '行了行了 干嘛呀', "Alright, alright — what's going on?"),
]
# (sentence_index, char_k_position) -> pinyin override
OVERRIDE = {
 (1, 7): 'yīng',  # 阴 — default ok (yīn)
 (1, 8): 'yǐng', # 影 — default ok
 (4, 0): 'dǒng', # 懂 — default ok
 (11, 2): 'gàn', # 干 in 干嘛 → gàn (do), not gān (dry)
}
VOCAB = [
 ('阴影', 'yīn yǐng', 'HSK5', 'Shadow; psychological shadow/trauma. 离婚阴影 = the psychological shadow of [a parent\'s] divorce. Literal: shadow cast by an object. Figurative: lasting negative psychological impact. Compare: 创伤 (trauma, more clinical), 心理阴影 (psychological shadow, more explicit).'),
 ('清醒', 'qīng xǐng', 'HSK5', 'To be clear-headed, to come to one\'s senses; to recover from a shock. 从…清醒过来 = to snap out of / recover from [something]. Also means to wake up mentally. Compare: 醒来 (to wake up physically), 振作 (to pull oneself together).'),
 ('幼小', 'yòu xiǎo', 'HSK5+', 'Young and tender/small; used of children or immature things. 幼小心灵 (young tender heart/mind) is a set phrase often used semi-dramatically. Collocation: 幼小的孩子, 幼小的心灵. Near-synonym: 年幼 (young in age, more neutral/formal).'),
 ('就许…不许…', 'jiù xǔ…bù xǔ…', 'grammar', 'Double standard construction: "You\'re allowed to… but [I\'m] not allowed to…" 就许你结婚离婚再结婚，不许我交男朋友 = "You can marry/divorce/remarry, but I can\'t even date." 就 emphasizes the unfairness. Related idiom: 只许州官放火，不许百姓点灯.'),
 ('干嘛', 'gàn má', 'colloquial', 'What are you doing? / What\'s the matter? Note 干 = gàn here (4th tone), not gān (dry). 干嘛呀 = casual "what\'s going on?" or mild scolding "what are you doing?!" Very common in Beijing-flavored speech. More casual than 干什么 or 做什么.'),
 ('从…过来', 'cóng…guò lái', 'grammar', '从 [bad situation] 过来 = to come through/recover from something. 从你的离婚阴影中清醒过来 = recover/snap out of the shadow of your divorce. 过来 as a directional complement here means "come through to this side" = fully recover. Compare: 走出来 (walk out of / get over).'),
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
