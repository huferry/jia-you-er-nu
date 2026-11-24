# -*- coding: utf-8 -*-
import os, html
from pypinyin import pinyin, Style

TITLE = "家有儿女 S01E02 10:08.68 - 10:52.28"
OUT = "家有儿女S01E02_clip_10-08_lesson"
S = [
 ('10:08.68', '他今天啊', "Today, he —"),
 ('10:09.88', '绝对得受到严厉的惩罚', "absolutely must receive a severe punishment!"),
 ('10:14.12', '那当然了', "Well of course!"),
 ('10:14.92', '把自己的男朋友带回家', "Bringing her own boyfriend home —"),
 ('10:18.56', '太猖狂了', "how outrageous!"),
 ('10:19.76', '不打他不正常', "It'd be weird NOT to beat him."),
 ('10:22.00', '在美国打孩子是犯法的', "In America, hitting children is against the law."),
 ('10:24.76', '在中国也一样犯法', "In China it's exactly the same — it's illegal."),
 ('10:27.56', '在美国挨打的孩子就要打九一一', "In America, a child who gets hit calls 9-1-1."),
 ('10:30.88', '在中国挨打的孩子就要打一一零', "In China, a child who gets hit calls 1-1-0."),
 ('10:36.08', '不过我也没人打过', "But nobody's ever hit me."),
 ('10:40.36', '你想想啊', "Think about it —"),
]
# (sentence_index, char_k_position) -> pinyin override
OVERRIDE = {
 (1, 2): 'děi',   # 得 in 绝对得 → děi (must/have to), not de (structural) or dé (obtain)
 (1, 3): 'shòu',  # 受 in 受到 → shòu
 (1, 4): 'dào',   # 到 → dào
 (1, 5): 'yán',   # 严 in 严厉 → yán
 (1, 8): 'chéng', # 惩 in 惩罚 → chéng (pos 8: 绝对得受到严厉的惩罚)
 (4, 1): 'chāng', # 猖 in 猖狂 → chāng
 (5, 1): 'dǎ',    # 打 in 不打他不正常 → dǎ
 (5, 4): 'zhèng', # 正 in 正常 → zhèng (pos 4: 不打他不正常)
 (6, 3): 'dǎ',    # 打 in 在美国打孩子是犯法的 (pos 3)
 (6, 7): 'fàn',   # 犯 in 犯法 (pos 7)
 (7, 4): 'yī',    # 一 in 一样 → yī (pos 4: 在中国也一样犯法)
 (7, 6): 'fàn',   # 犯 in 犯法 (pos 6)
 (8, 3): 'ái',    # 挨 in 挨打 → ái (pos 3: 在美国挨打的孩子就要打九一一)
 (8, 4): 'dǎ',    # 打 in 挨打 (pos 4)
 (9, 3): 'ái',    # 挨 in 挨打 → ái (pos 3: 在中国挨打的孩子就要打一一零)
 (9, 4): 'dǎ',    # 打 in 挨打 (pos 4)
}
VOCAB = [
 ('绝对得', 'jué duì děi', 'colloquial', '绝对 (absolutely) + 得 (děi = must). Note: 得 here is the modal verb meaning "must/have to" (děi), NOT the structural particle 得 (de) or the verb 得 (dé = obtain). This tone distinction is important: 得 as "must" is always děi in spoken Mandarin.'),
 ('严厉', 'yán lì', 'HSK5', 'Stern, strict, severe. 严厉的惩罚 = severe punishment. Used of discipline, criticism, or consequences. Stronger than 严格 (strict/rigorous, more about rules/standards). 严厉 often implies harshness with an emotional component; 严格 is more neutral/procedural.'),
 ('猖狂', 'chāng kuáng', 'HSK5+', 'Rampant, brazen, wildly arrogant. Usually describes enemies, criminals, or misbehaving people acting without restraint. Here Xiaoyu uses it hyperbolically about his sister bringing a boyfriend home — a child\'s over-the-top moral outrage. Near-synonym: 嚣张 (arrogant/cocky).'),
 ('挨打', 'ái dǎ', 'HSK4+', 'To get beaten/hit; to take a beating. 挨 (ái) = to suffer/endure (always tone 2 when meaning "receive/suffer"). 挨打 is a set collocation. Note 挨 ≠ āi (approach/near). Other 挨 collocations: 挨骂 (get scolded), 挨饿 (suffer hunger). Very colloquial in family/school contexts.'),
 ('犯法', 'fàn fǎ', 'HSK4', 'To break the law; to be illegal. 犯 = to commit (an offense); 法 = law. 犯法 emphasizes the act of violation. Near-synonyms: 违法 (violate the law, more formal/official); 违规 (violate rules, not necessarily criminal). The scene satirizes Chinese parents who threaten to hit kids.'),
 ('打110', 'dǎ yāo yāo líng', 'colloquial', 'To call 110 — China\'s police/emergency number (equivalent to 911 in the US). 打 here means "dial/call" (打电话 = make a phone call). The humor: calling the police on your own parents is ironic since after the police leave, you\'re alone with the same parents again.'),
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
