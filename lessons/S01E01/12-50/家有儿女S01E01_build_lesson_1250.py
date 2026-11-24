# -*- coding: utf-8 -*-
import os, html
from pypinyin import pinyin, Style

TITLE = "家有儿女 12:50.00 - 13:13.00"
OUT = "家有儿女S01E01_clip_12-50_lesson"
S = [
 ('12:50.00', '一会儿就熟', "They'll be done in a moment."),
 ('12:52.00', '再等一会儿', "Wait just a little longer."),
 ('12:53.00', '妈妈一早去买的', "Mom went out early this morning to buy them."),
 ('12:54.00', '都是活的', "They were all alive."),
 ('12:55.00', '哪儿产的呀', "Where are they from?"),
 ('12:56.00', '能确定没被污染过吗', "Can you confirm they haven't been contaminated?"),
 ('12:59.00', '螃蟹壳上', "On the crab shell —"),
 ('13:00.00', '有没有防伪标志', "is there an anti-counterfeit label?"),
 ('13:05.00', '我一直以为', "I always thought —"),
 ('13:06.00', '只有正宗的那种大闸蟹', "only authentic hairy crabs"),
 ('13:08.00', '壳上才有标志呢', "would have a label on the shell."),
 ('13:13.00', '您已经没有主见了', "You've already lost your own opinion."),
]
# (sentence_index, char_k_position) -> pinyin override
OVERRIDE = {
 # 熟 shú (cooked/ripe) vs shóu (familiar) — here = cooked: shú; pypinyin may default to shú, check
 # 的 at end of sentences: neutral, fine
 # 污染 wū rǎn: straightforward, no override needed
 # 大闸蟹 dà zhá xiè: 蟹 = xiè; pypinyin handles
 # 正宗 zhèng zōng: standard reading, no override
}
VOCAB = [
 ('一会儿', 'yī huì r', 'HSK3', 'A moment, a little while. 一会儿就熟 = will be cooked in a moment (就 = right away/then). 再等一会儿 = wait a little longer. Can refer to past or future short time: 一会儿我来 (I\'ll come in a bit); 刚才一会儿 (just a moment ago). Note the erhua (儿化) — typical Beijing speech. Compare: 一下 (a moment — often for quick actions: 等一下 = wait a sec).'),
 ('污染', 'wū rǎn', 'HSK5', 'Pollution, contamination; to pollute/contaminate. 被污染过 = has been contaminated (被 = passive marker; 过 = experiential aspect). Environmental concern: 水污染 (water pollution), 空气污染 (air pollution), 污染源 (source of pollution). Xiaoxue applies food-safety anxiety to the crab — a comic character moment. 污染 is now one of the most common news/policy words in modern Chinese.'),
 ('防伪标志', 'fáng wèi biāo zhì', 'HSK5+', 'Anti-counterfeit label/mark. 防 = prevent; 伪 = fake/counterfeit; 标志 = mark/label/sign. In China, premium products (especially 大闸蟹, liquor, medicine) carry holographic or QR anti-fake labels. Xiaoxue asks if the crab has one — played for laughs. 标志 alone = mark, logo, symbol (国家标志 = national emblem). Compare: 防伪 (anti-counterfeiting, as a verb/adj compound).'),
 ('正宗', 'zhèng zōng', 'HSK4+', 'Authentic, genuine, orthodox. 正宗的大闸蟹 = authentic hairy crabs (from Yangcheng Lake). Collocations: 正宗北京烤鸭 (authentic Peking duck), 正宗四川火锅 (genuine Sichuan hotpot). Compare: 地道 dì dao (genuine, authentic — more colloquial, often about accent or food); 真正 zhēn zhèng (truly, genuinely — more about essence/nature). 正宗 is specifically about origin and tradition.'),
 ('大闸蟹', 'dà zhá xiè', 'cultural', 'Shanghai hairy crab; Chinese mitten crab. 大 = big; 闸 = sluice/gate (refers to the lake waterways); 蟹 = crab. The most prized variety comes from Yangcheng Lake (阳澄湖) in Jiangsu. Seasonally eaten in autumn; authentic ones have hologram labels (防伪标志) around their legs. A luxury food item and a byword for food authenticity debates in China.'),
 ('主见', 'zhǔ jiàn', 'HSK5', 'One\'s own opinion/view; independent judgment. 没有主见 = has no mind of one\'s own, easily swayed. 您已经没有主见了 = you\'ve already lost your own opinion (sarcastic: you\'ve been brainwashed into agreeing). Compare: 见解 jiàn jiě (view, perspective — more neutral/intellectual); 意见 yì jiàn (opinion — broader). 有主见 is a compliment (decisive, opinionated); 没主见 is a criticism (spineless, easily led).'),
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
