# -*- coding: utf-8 -*-
import os, html
from pypinyin import pinyin, Style

TITLE = "家有儿女 19:59.00 - 20:35.00"
OUT = "家有儿女S01E01_clip_19-59_lesson"
S = [
 ('19:59.00', '为什么', "Why?"),
 ('20:11.00', '好了 我们家到了', "Alright, we're home."),
 ('20:13.00', '把帽子摘下来', "Take your hat off."),
 ('20:15.00', '现在就摘啊', "Take it off right now?"),
 ('20:17.00', '第四十八页', "Page forty-eight."),
 ('20:18.00', '三到十六行', "Lines three to sixteen."),
 ('20:23.00', '在明天上学之前洗得掉吗', "Can it be washed off before school tomorrow?"),
 ('20:26.00', '洗不掉', "It won't wash off."),
 ('20:27.00', '我再帮你染成黑色的嘛', "Then I'll help you dye it back to black."),
 ('20:31.00', '你干嘛呀', "What are you doing?!"),
 ('20:32.00', '我干嘛呀 我干嘛呀', "What am I doing? What am I doing?!"),
 ('20:34.00', '非去不可啊', "You absolutely have to go, huh?"),
]
OVERRIDE = {
 # 得 in potential complement 洗得掉: should be neutral tone 'de', not dé
 # 在(0)明(1)天(2)上(3)学(4)之(5)前(6)洗(7)得(8)掉(9)吗(10)
 (6, 8): 'de',
}
VOCAB = [
 ('第…页', 'dì … yè', 'HSK3', 'Page number. 第四十八页 = page 48. 第 marks ordinal numbers; 页 = page. Dad assigns 刘星 lines 3-16 of page 48 as punishment — the same love poem Xiaoxue\'s boyfriend 狂野男孩 recites later (and again at the S01E02 opening).'),
 ('摘', 'zhāi', 'HSK4', 'To remove, take off (hat, glasses, fruit). 把帽子摘下来 = take your hat off. 摘 implies detaching something that was attached or worn. Compare: 脱 (take off clothing — 脱衣服, 脱鞋); 摘 is for smaller accessories and picking fruit. 摘眼镜 = take off glasses.'),
 ('染', 'rǎn', 'HSK5', 'To dye; to tint; to infect. 染成黑色 = dye it black. 染 + 成 + color = dye into a color. 染发 = dye one\'s hair. The scene: 刘星 has dyed or bleached his hair, which won\'t wash out before school — Dad panics.'),
 ('干嘛', 'gàn má', 'colloquial', 'What are you doing? / Why are you doing that? Colloquial form of 干什么. 你干嘛呀 = what do you think you\'re doing?! The repeated 我干嘛呀 我干嘛呀 is 刘星 mimicking/mocking Dad\'s question back at him — a classic kid deflection tactic.'),
 ('非…不可', 'fēi … bù kě', 'HSK5', 'Must/have to (emphatic). 非去不可 = absolutely must go / have no choice but to go. Double negative construction: 非 (not) + V + 不可 (not allowed) = insisting on the action. Stronger than 一定要. Compare: 非做不可 (must do it no matter what).'),
 ('洗得掉 / 洗不掉', 'xǐ de diào / xǐ bù diào', 'grammar', 'Potential complement: can/cannot wash off. 得 (de) = potential marker (can); 不 = cannot. Pattern: V + 得/不 + result complement. 洗掉 = wash off (result); 洗得掉 = can be washed off; 洗不掉 = cannot be washed off. Same pattern: 拿得动/拿不动 (can/cannot carry).'),
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
