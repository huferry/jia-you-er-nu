# -*- coding: utf-8 -*-
import os, html
from pypinyin import pinyin, Style

TITLE = "家有儿女 S01E02 21:18.24 - 22:16.24"
OUT = "家有儿女S01E02_clip_21-29_lesson"
S = [
 ('21:18.24', '我只是行使一下当姐姐的责任', "I was just exercising my responsibility as a big sister."),
 ('21:20.24', '他们却给我捣蛋', "But they just made trouble for me!"),
 ('21:26.24', '只许州官放火', "Officials may set fires,"),
 ('21:27.24', '不许百姓点灯', "but commoners may not light a lamp!"),
 ('21:29.24', '可是咱们家没有州官', "But our family has no officials —"),
 ('21:31.24', '只有姐姐', "only a big sister!"),
 ('21:36.24', '不听爸爸妈妈的话', "You don't listen to your parents,"),
 ('21:38.24', '你一进门就给我们俩下马威', "the moment you walked in you tried to intimidate us,"),
 ('21:43.24', '还把男朋友带家来', "and you even brought your boyfriend home!"),
 ('21:53.24', '送小妹妹一根鸡毛 算得了什么呀', "Giving little sister a chicken feather — that's nothing!"),
 ('22:03.24', '我们才是好孩子', "We're the real good kids here!"),
 ('22:05.24', '我要跟你们两个小坏蛋决斗了', "I'm going to have a showdown with you two little troublemakers!"),
]
# (sentence_index, char_k_position) -> pinyin override
OVERRIDE = {
 (0, 1): 'zhǐ',   # 只 in 只是 → zhǐ (only)
 (0, 2): 'shì',   # 是 → shì
 (0, 4): 'xíng',  # 行 in 行使 → xíng (exercise/use), not háng
 (0, 7): 'zé',    # 责 in 责任 → zé
 (2, 1): 'xǔ',    # 许 in 只许 → xǔ
 (2, 2): 'zhōu',  # 州 → zhōu
 (3, 1): 'xǔ',    # 许 in 不许 → xǔ
 (7, 3): 'mén',   # 门 → mén
 (7, 7): 'liǎ',   # 俩 → liǎ (the two of us)
 (7, 8): 'xià',   # 下 in 下马威 → xià
 (7, 9): 'mǎ',    # 马 in 马威 → mǎ
 (11, 5): 'huài', # 坏 in 坏蛋 → huài
 (11, 7): 'jué',  # 决 in 决斗 → jué
}
VOCAB = [
 ('行使', 'xíng shǐ', 'HSK5', 'To exercise (a right, power, or responsibility). 行使责任 = "exercise one\'s responsibility." Note 行 is xíng (to do/carry out) here, NOT háng (row/line). Common with legal/formal nouns: 行使权力 (exercise power), 行使职能 (perform a function).'),
 ('捣蛋', 'dǎo dàn', 'colloquial', 'To make trouble, act up, play pranks. Literally "smash an egg." 给我捣蛋 = "made trouble for me / got in my way." A casual, slightly playful term — not as serious as 闹事 (cause a scene/disturbance). Often used for mischievous children: 小捣蛋 (little troublemaker).'),
 ('下马威', 'xià mǎ wēi', 'idiom', 'To intimidate from the outset, give someone an initial show of force. 一进门就给我们下马威 = "the moment she walked in she tried to cow us." From 马 (horse) — originally the display of authority when dismounting. Used for anyone who makes an aggressive first impression.'),
 ('任人宰割', 'rèn rén zǎi gē', 'idiom', 'To be at someone\'s mercy; to allow oneself to be slaughtered. Literally "let people butcher you." An earlier scene establishes 小雪\'s position: she is NOT a 任人宰割的小绵羊 (meek little lamb), but a 小刺猬 (little hedgehog/porcupine full of spines). This idiom frames the whole episode\'s theme.'),
 ('坏蛋', 'huài dàn', 'colloquial', 'Rascal, bad egg, troublemaker. Affectionate-contemptuous; often used for naughty children. 两个小坏蛋 = "you two little rascals." 小坏蛋 is playful; serious: 坏人 (bad person), 坏份子 (bad element). The tone here is mock-outrage: 夏东海 is challenging the kids to a "duel."'),
 ('决斗', 'jué dòu', 'HSK5+', 'A duel, decisive confrontation. 我要跟你们决斗了 = "I\'m going to have it out with you!" The word echoes the very first lesson (S01E02, 00:30) where the boys recite a love vow about dueling for 小雪. Here it circles back as 夏东海\'s comic threat to his own children.'),
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
