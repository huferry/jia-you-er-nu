# -*- coding: utf-8 -*-
import os, html
from pypinyin import pinyin, Style

TITLE = "家有儿女 19:19.00 - 19:58.00"
OUT = "家有儿女S01E01_clip_19-19_lesson"
S = [
 ('19:19.00', '我们也能把音响开得这么大吗', "Can we also turn the speakers up this loud?"),
 ('19:23.00', '而且你们还不说我', "And yet you're not scolding me for it."),
 ('19:31.00', '我不喜欢你们给我准备的这套枕巾', "I don't like this set of pillow covers you prepared for me."),
 ('19:34.00', '我要拿它当擦脚布', "I'm going to use them as foot wipes."),
 ('19:36.00', '没问题', "No problem."),
 ('19:37.00', '只要你愿意', "As long as you're willing."),
 ('19:38.00', '你把擦脚布当枕巾都行', "You can even use a foot wipe as a pillow cover — that's fine too."),
 ('19:40.00', '没错', "That's right."),
 ('19:44.00', '我能把枕巾当成擦脚布吗', "Can I use the pillow cover as a foot wipe too?"),
 ('19:47.00', '这样两个脚丫子可以一块擦', "That way both feet can be wiped at the same time."),
 ('19:51.00', '你们俩老在这捣什么乱呢你们', "You two, what are you always stirring up trouble here for?"),
 ('19:53.00', '对于你们俩来讲 擦脚布就是擦脚布 枕巾就是枕巾 不能换', "For you two, a foot wipe is a foot wipe and a pillow cover is a pillow cover — no swapping."),
]
OVERRIDE = {
 # 当 (dāng = serve as) is handled correctly by pypinyin in context; no overrides needed
}
VOCAB = [
 ('枕巾', 'zhěn jīn', 'HSK5+', 'Pillow cover / pillow towel. 枕 = pillow; 巾 = cloth/towel. 枕巾 is a rectangular towel placed over a pillowcase — common in mainland Chinese homes. Xiaoxue objects to the ones prepared for her and threatens to repurpose them.'),
 ('擦脚布', 'cā jiǎo bù', 'colloquial', 'Foot wipe / foot towel. 擦 = to wipe/rub; 脚 = foot; 布 = cloth. Not a standard lexicon item — it is a colloquial compound. The humor: Xiaoxue threatens to demote her 枕巾 to 擦脚布 status; the boys ask if they can do the reverse.'),
 ('把…当…', 'bǎ … dāng …', 'grammar', 'To treat/use X as Y. 把擦脚布当枕巾 = use a foot wipe as a pillow cover. Pattern: 把 + object + 当(成) + role. 当 (dāng) here means "to serve as / to treat as". Distinguish from 当 (dàng) = to regard wrongly (误当). This pattern appears three times in the scene.'),
 ('脚丫子', 'jiǎo yā zi', 'colloquial', 'Feet (informal/affectionate). 脚 = foot; 丫子 is a colloquial suffix that makes it playful/childlike. 两个脚丫子 = both feet. Used by the boys to comic effect as they lobby for equal treatment.'),
 ('捣乱', 'dǎo luàn', 'HSK4+', 'To make trouble, stir things up, cause mischief. 捣 = to pound/stir; 乱 = chaos/disorder. 老在这捣什么乱呢 = what are you always making trouble here for? Often used by adults scolding children. Compare 闹事 (cause a disturbance — more serious).'),
 ('不能换', 'bù néng huàn', 'HSK3', 'Cannot swap / no swapping allowed. 换 = to exchange/swap. Dad\'s ruling: objects have their proper function and cannot be substituted. 换 is versatile: 换衣服 (change clothes), 换钱 (exchange money), 交换 (exchange mutually).'),
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
