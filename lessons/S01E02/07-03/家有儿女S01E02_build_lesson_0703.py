# -*- coding: utf-8 -*-
import os, html
from pypinyin import pinyin, Style

TITLE = "家有儿女 S01E02 07:03.80 - 07:37.12"
OUT = "家有儿女S01E02_clip_07-03_lesson"
S = [
 ('07:03.80', '你怎么能叫狂野男孩啊', "How can you go by the name 'Wild Boy'?"),
 ('07:06.20', '我看你应该叫', "I think you should be called"),
 ('07:07.96', '文弱小书生才对啊', "a timid little bookworm — that fits you much better!"),
 ('07:11.00', '这是夏雪给我取的', "Xia Xue is the one who gave me that name."),
 ('07:21.32', '什么什么', "What? What?"),
 ('07:23.56', '其实啊我们呀', "Actually, the thing is, we…"),
 ('07:25.00', '都是为你们着急', "…are both worried about you two."),
 ('07:26.36', '为你们负责', "We're being responsible for you."),
 ('07:27.76', '高中正是人生很重要的一个积累知识的阶段', "High school is a critically important phase in life for building up knowledge."),
 ('07:32.48', '你们应该把精力放在学习上啊', "You should be putting your energy into your studies!"),
 ('07:34.76', '谈恋爱那都是大人的事', "Dating — that's all grown-up stuff."),
 ('07:37.12', '你们不应该', "You two shouldn't be doing that."),
]
# (sentence_index, char_k_position) -> pinyin override
OVERRIDE = {
 (2, 0): 'wén',   # 文 in 文弱 → wén (literary/gentle), tone 2
 (5, 2): 'a',     # 啊 after vowel in 其实啊 → a (neutral exclamation)
 (8, 2): 'zhèng', # 正 in 正是 → zhèng (precisely/right), not zhēng
 (8, 10): 'zhòng', # 重 in 重要 → zhòng (important), not chóng
 (9, 6): 'fàng',  # 放 in 放在 → fàng (place/put), not fāng
}
VOCAB = [
 ('文弱书生', 'wén ruò shū shēng', 'idiom', 'A pale, frail scholar; a bookish young man with no physical prowess. The stereotype of someone who reads all day but can\'t fight. Opposite of 武将 (warrior). Used here to mock the boy: how can a "文弱书生" call himself "Wild Boy"?'),
 ('为…着急', 'wèi…zháojí', 'HSK4+', 'To worry about / be anxious for someone. 着急 = to feel anxious/rushed. The 为 marks the person you worry *for* (不为自己着急 = not worried about oneself). Compare: 担心 (concerned), 焦虑 (anxious/nervous, more formal).'),
 ('负责', 'fù zé', 'HSK4', 'To be responsible for; to take responsibility. 为你们负责 = acting responsibly on your behalf. Can precede 任 for extra formality: 负责任. Contrast: 不负责任 (irresponsible) — appears later in the episode.'),
 ('积累', 'jī lěi', 'HSK5', 'To accumulate, build up gradually. 积累知识 = accumulate knowledge. Implies a slow, sustained process. Collocations: 积累经验 (gain experience), 积累财富 (build wealth). Near-synonym 积攒 emphasizes saving up, more colloquial.'),
 ('把精力放在…上', 'bǎ jīnglì fàng zài…shàng', 'grammar', '"Put one\'s energy/attention into…" The 把-construction moves the object (精力) before the verb for emphasis. 精力 = mental and physical energy. Collocation: 把时间放在…上 (spend time on). Common in exhortations about study or work.'),
 ('谈恋爱', 'tán liàn\'ài', 'HSK4', 'To date someone; to be in a romantic relationship. 谈 here means "to engage in." Note: 谈恋爱 is the process (dating), while 恋爱 alone is the state/feeling (love/romance). 早恋 (premature romance) = dating while underage — a key word in this episode.'),
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
