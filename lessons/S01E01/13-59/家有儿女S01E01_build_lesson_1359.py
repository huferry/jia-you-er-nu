# -*- coding: utf-8 -*-
import os, html
from pypinyin import pinyin, Style

TITLE = "家有儿女 13:59.00 - 14:36.00"
OUT = "家有儿女S01E01_clip_13-59_lesson"
S = [
 ('13:59.00', '进我的房间', "To enter my room,"),
 ('14:00.00', '必须先敲门', "you must knock first."),
 ('14:01.00', '我不说请进', "If I don't say 'come in,'"),
 ('14:02.00', '就不能进来', "you cannot come in."),
 ('14:09.00', '我有权决定', "I have the right to decide"),
 ('14:10.00', '自己干什么不干什么', "what I do and don't do for myself."),
 ('14:12.00', '有权不回答问题', "I have the right not to answer questions."),
 ('14:14.00', '在我保持沉默的时候', "When I am maintaining silence,"),
 ('14:16.00', '请勿打扰', "please do not disturb me."),
 ('14:33.00', '我听你爸爸说', "I heard from your dad that"),
 ('14:34.00', '你从小就特别爱吃这个', "you've loved eating this since you were little —"),
 ('14:36.00', '西红柿鸡蛋汤', "tomato and egg soup."),
]
OVERRIDE = {
 # 干 in 自己干什么不干什么: gàn (to do), pypinyin may give gān (dry) as default
 (5, 2): 'gàn',
 (5, 5): 'gàn',
}
VOCAB = [
 ('敲门', 'qiāo mén', 'HSK4+', 'To knock on a door. 敲 = to knock/tap. A key social courtesy in Chinese homes — Xiaoxue is insisting on this as a formal rule, which is unusual in a traditional Chinese family context where parents often enter children\'s rooms freely. The comedy is in codifying normal Western-style privacy norms as a binding legal declaration.'),
 ('保持沉默', 'bǎo chí chén mò', 'HSK4+', 'To maintain silence / to remain silent. 保持 = maintain (HSK4); 沉默 = silence, taciturn (HSK4). The phrase echoes Miranda rights ("you have the right to remain silent") — deliberate humor. 沉默是金 = silence is golden (proverb). Compare: 安静 (quiet — describes the environment); 沉默 (silence — describes a person\'s choice not to speak).'),
 ('请勿打扰', 'qǐng wù dǎ rǎo', 'formal', 'Please do not disturb. 请 = please; 勿 = do not (classical/formal negative, more emphatic than 不要); 打扰 = to disturb, to bother (HSK4). The same phrase is on hotel door signs. Its use in a family dinner speech is comically formal. 打扰一下 = excuse me (polite way to interrupt someone).'),
 ('有权', 'yǒu quán', 'HSK4+', 'To have the right to (do something). Pattern: 有权 + V. 我有权不回答 = I have the right not to answer. Compare: 权利 (quánlì, right/entitlement as a noun); 权力 (quánlì, power/authority). 有权 is the verb phrase used in legal and rights discourse — Xiaoxue is parodying a legal rights declaration throughout her speech.'),
 ('西红柿', 'xī hóng shì', 'HSK3+', 'Tomato. Northern Chinese term (common in Mandarin). Southern Chinese often say 番茄 (fān qié). 西红柿鸡蛋汤 = tomato and egg soup — a quintessential Chinese home-cooking dish. Its appearance here is emotionally significant: it was Xiaoxue\'s favorite as a child, and 刘美 (the stepmother) made it to welcome her, an act of kindness Xiaoxue cannot quite ignore.'),
 ('从小', 'cóng xiǎo', 'HSK3', 'Since childhood, from a young age. Fixed adverbial phrase. 从小就 + V = has [done X] since childhood. Compare: 小时候 (when [I] was little — a time noun used as a topic or adverbial); 从小 is more naturally adverbial. 你从小就特别爱吃这个 = you\'ve loved this ever since you were little.'),
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
