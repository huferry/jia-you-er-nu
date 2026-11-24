# -*- coding: utf-8 -*-
import os, html
from pypinyin import pinyin, Style

TITLE = "家有儿女 S01E02 04:58.44 - 05:54.92"
OUT = "家有儿女S01E02_clip_04-58_lesson"
S = [
 ('04:58.44', '稀里糊涂的就闪电式跟他结婚了', "In a muddle-headed daze, I went and married him in a flash."),
 ('05:02.36', '嫁错人了吧', "Married the wrong person, didn't you?"),
 ('05:03.68', '虽然我现在及时地改正了错误', "Although I've now corrected my mistake in time —"),
 ('05:07.04', '毕竟有一个共同的孩子啊', "— we do still share a child together, after all."),
 ('05:08.84', '他什么时候心血来潮想来看孩子', "Whenever he gets a sudden urge to come see the kid —"),
 ('05:11.00', '我也不能把他轰出去啊', "— I can't just chase him out the door."),
 ('05:23.20', '你别非得跟他发生正面冲突啊', "Don't go and have a head-on clash with him."),
 ('05:37.60', '你不是我的智囊团吗 小哥', "Aren't you my think tank, little brother?"),
 ('05:42.16', '我现在就从狂野男孩那下手', "I'm going to start by dealing with Wild Boy right now."),
 ('05:46.28', '干嘛呀 你要打人家', "What are you doing — you want to hit him?"),
 ('05:49.48', '他还用我亲自动手', "Does he even need me to do it myself?"),
 ('05:53.16', '你要雇人打他', "You're going to hire someone to beat him up?"),
]
# (sentence_index, char_k_position) -> pinyin override
OVERRIDE = {
 (0, 0): 'xī',   # 稀 — default ok
 (4, 4): 'cháo', # 潮 in 心血来潮 → cháo (tide/trend), default ok
 (6, 2): 'fēi',  # 非 in 非得 → fēi (must/have to), not fēi (fly)
 (6, 3): 'děi',  # 得 in 非得 → děi (must), not de/dé
 (6, 7): 'zhèng', # 正 in 正面 → zhèng (front/positive), not zhēng
 (9, 1): 'ma',   # 嘛 neutral — default ok
 (9, 3): 'gàn',  # 干 in 干嘛 → gàn, not gān
}
VOCAB = [
 ('稀里糊涂', 'xī li hú tu', 'colloquial', 'In a muddled, confused, half-aware state. A four-character colloquial phrase (not a 成语 but fixed expression). 稀里糊涂的就… = "in a daze, just went and…" Conveys acting without thinking clearly. Compare: 糊里糊涂 (same meaning), 迷迷糊糊 (half-asleep/dazed).'),
 ('心血来潮', 'xīn xuè lái cháo', 'idiom', 'On a sudden whim, struck by an impulse. Lit. "blood rushes to the heart." 成语. 什么时候心血来潮 = "whenever he gets a sudden whim." Usually mildly pejorative — implies impulsive, unplanned action. Compare: 一时兴起 (moment of excitement), 临时起意 (a sudden idea).'),
 ('轰出去', 'hōng chū qù', 'colloquial', 'To drive/chase someone out loudly; to boot someone out. 轰 = to shout/drive away (like shooing animals). 把他轰出去 = boot him out. More forceful and rude than 请他走 (ask him to leave) or 叫他出去. Implies rudeness not acceptable in the situation.'),
 ('正面冲突', 'zhèng miàn chōng tū', 'HSK5+', 'Head-on confrontation, direct clash. 正面 = frontal, direct; 冲突 = conflict. 发生正面冲突 = to have a direct confrontation. Formal-sounding phrase used in contexts from family drama to international relations. Compare: 闹翻 (fall out badly), 吵架 (quarrel).'),
 ('智囊团', 'zhì náng tuán', 'colloquial', 'Think tank; brain trust. Lit. "wisdom sack group." 智囊 = advisor/brains (single person), 团 = group. Here used humorously — the stepmother is calling her new husband her personal think tank. Compare: 参谋 (advisor), 出谋划策 (to devise strategies).'),
 ('非得…不可', 'fēi děi…bù kě', 'grammar', 'Must absolutely, have to without exception. 非 (fēi) + 得 (děi) = must/have to (emphatic). 你别非得跟他发生冲突 = "Don\'t insist on having a clash with him." 非得 alone already means "must"; 不可 at the end makes it complete. Compare: 一定要 (must), 必须 (must, formal).'),
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
