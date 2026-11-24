# -*- coding: utf-8 -*-
import os, html
from pypinyin import pinyin, Style

TITLE = "家有儿女 11:05.00 - 11:38.00"
OUT = "家有儿女S01E01_clip_11-05_lesson"
S = [
 ('11:05.00', '在这个家里受尊重吗', "Are you respected in this family?"),
 ('11:07.00', '有人身自由吗', "Do you have personal freedom?"),
 ('11:11.00', '反正晚上不洗脚', "Anyway, if you don't wash your feet at night —"),
 ('11:13.00', '绝对绝对不能上床的', "you absolutely, absolutely cannot go to bed."),
 ('11:18.00', '还有那个叫刘星的那孩子', "And that kid they call Liu Xing —"),
 ('11:20.00', '他欺负过你吗', "Has he ever bullied you?"),
 ('11:26.00', '你放心', "Don't worry."),
 ('11:27.00', '我是不会欺负你的', "I am not going to bully you."),
 ('11:29.00', '这一点我可以向你保证', "This I can guarantee you."),
 ('11:32.00', '原来我在这个家的定位', "So my place in this family —"),
 ('11:35.00', '就是不受别人欺负呀', "is simply: don't get bullied by anyone."),
 ('11:38.00', '那这个生存起点也太低了吧', "Well, that's a pretty low bar to start from."),
]
# (sentence_index, char_k_position) -> pinyin override
OVERRIDE = {
 # 重 in 尊重: zhòng (weight/important) vs zhóng (hit target) — here 尊重 = zūn zhòng, pypinyin handles correctly
 # 的 at end of sentences: neutral tone, pypinyin handles
 # 过 in 欺负过你: aspect marker, should be guo (neutral)
 (5, 3): 'guo',   # 欺负过你 — 过 as aspect particle (experiential): guò → guo
}
VOCAB = [
 ('尊重', 'zūn zhòng', 'HSK4', 'To respect; respect (noun). 受尊重 = to be respected (受 = to receive/suffer). Collocations: 互相尊重 (mutual respect), 尊重别人 (respect others), 受到尊重 (receive respect). Contrast: 看不起 (look down on), 歧视 (discriminate against). Key word for understanding Chinese family/social dynamics.'),
 ('人身自由', 'rén shēn zì yóu', 'formal/legal', 'Personal freedom, freedom of the person. 人身 = one\'s person/body; 自由 = freedom. A formal legal/political term that Xiaoxue applies comically to household rules. 有人身自由吗 = do you have personal liberty? Note: 自由 alone = freedom (broader); 人身自由 specifically refers to freedom of movement/personal autonomy.'),
 ('反正', 'fǎn zhèng', 'HSK4', 'Anyway, in any case, regardless. Used to introduce a conclusion or state something that holds true no matter what. 反正…就… = no matter what…, (the result is)…. Compare: 总之 zǒng zhī (in a word, in short — more formal); 不管怎样 (no matter how). Very common in spoken Chinese. Here: Xiaoyu\'s deadpan answer reveals the household rule: no feet-washing = no bed.'),
 ('绝对', 'jué duì', 'HSK4', 'Absolutely, definitely; absolute. Used as an intensifier. 绝对不能 = absolutely cannot. Doubled for emphasis: 绝对绝对不能 = absolutely 100% cannot. Compare: 肯定 kěn dìng (definitely/certainly — more about speaker\'s confidence); 一定 yī dìng (must/certainly — often about obligation or prediction). 绝对 often carries a more emphatic, final tone.'),
 ('欺负', 'qī fu', 'HSK4', 'To bully, to pick on, to take advantage of. 欺负过你吗 = has (he) ever bullied you? (过 = experiential aspect). 受欺负/被欺负 = to be bullied. Near-synonym: 欺压 qī yā (oppress, stronger); 欺骗 qī piàn (deceive). Common in colloquial speech about children and workplace dynamics.'),
 ('定位', 'dìng wèi', 'HSK5', 'Positioning, role, place (in a system). Originally from navigation (determine position). Now widely used: 我在这个家的定位 = my positioning/role in this family. 品牌定位 (brand positioning), 职业定位 (career positioning). Xiaoxue uses it sarcastically: her entire "role" in the family is apparently just not to be bullied — a wryly low definition.'),
 ('生存起点', 'shēng cún qǐ diǎn', 'colloquial', 'Starting point for survival; baseline for existence. 生存 = survival; 起点 = starting point. 也太低了吧 = it\'s just too low, isn\'t it (也 intensifies; 吧 seeks agreement or expresses mild exasperation). The rhetorical structure 也太…了吧 is a very useful spoken pattern for expressing "that\'s a bit much / that\'s going too far."'),
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
