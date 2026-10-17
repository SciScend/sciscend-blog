#!/usr/bin/env python3
"""Генерира SVG диаграмите за серията за System One моделите и Jev.

Всяка диаграма отива в public/images/<slug>/ на поста, който я ползва (виж SLUG):
jev-model-koyto-reshava, blog-kategorizator-na-balgarski, laya-sreshtu-jev-na-balgarski.

Цветовете са токените на sciscend-blog (src/styles/global.css), светла и тъмна
тема през prefers-color-scheme - точно както сайта. Пусни отново след промяна:
    python3 scripts/make_diagrams.py            # пише в public/images/<slug>/
    python3 scripts/make_diagrams.py /tmp/out   # пише в /tmp/out/<slug>/ (за diff)

ВНИМАНИЕ: някои SVG в public/images/ са редактирани на ръка след генерирането.
Не пускай скрипта направо върху тях - генерирай в друга папка и сравни:
  - 01-sistema-1-i-2.svg: "System One/Two" вместо "Система 1/2", без реда
    "В софтуера: ...", лентата за време е преместена надолу.
  - 04-trite-primitiva.svg: скалата на Score е "0: cosmetic / 1: workaround /
    2: blocking" (mono) вместо българския текст на два реда.
  - 06-tri-zoni.svg, 07-klasicheski-vs-zero-shot.svg, 09-kaskada.svg,
    11-blog-kategorizator.svg: само "->" вместо "-&gt;" в текста (същото като SVG).
d8 (08-etapi-na-obuchenie.svg) не се ползва в никой пост и не се пуска;
последният му изход е в SystemOneModels/archive/blog-post/.
"""

import sys
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent.parent / "public" / "images"
W = 760

# Which post (public/images/<slug>/) each diagram belongs to.
SLUG = {
    "01-sistema-1-i-2.svg": "jev-model-koyto-reshava",
    "02-token-po-token-vs-edin-prohod.svg": "jev-model-koyto-reshava",
    "03-anatomiya-na-zayavka.svg": "jev-model-koyto-reshava",
    "04-trite-primitiva.svg": "jev-model-koyto-reshava",
    "05-veroyatnost-uverenost.svg": "jev-model-koyto-reshava",
    "06-tri-zoni.svg": "jev-model-koyto-reshava",
    "09-kaskada.svg": "jev-model-koyto-reshava",
    "10-benchmark.svg": "jev-model-koyto-reshava",
    "11-blog-kategorizator.svg": "blog-kategorizator-na-balgarski",
    "07-klasicheski-vs-zero-shot.svg": "laya-sreshtu-jev-na-balgarski",
    "14-laya-sreshtu-jev.svg": "laya-sreshtu-jev-na-balgarski",
}

STYLE = """
<style>
  text { font-family: system-ui, -apple-system, 'Segoe UI', Roboto, 'Noto Sans', Arial, sans-serif; fill: #353535; }
  .soft { fill: #5c5f63; } .faint { fill: #7a7e83; }
  .mono { font-family: ui-monospace, 'JetBrains Mono', Menlo, Consolas, monospace; }
  .panel { fill: #f4f7f8; stroke: #e3e8ea; }
  .card { fill: #ffffff; stroke: #d5dcdf; }
  .line { stroke: #9aa0a5; fill: none; }
  .ah { fill: #9aa0a5; }
  .grid { stroke: #e3e8ea; }
  .track { fill: #e3e8ea; }
  .jev { fill: #0b6f68; } .jevTint { fill: #e3f6f4; stroke: #13b0a5; } .jevInk { fill: #0b6f68; }
  .llm { fill: #0050a7; } .llmTint { fill: #e6eef8; stroke: #5b8fd0; } .llmInk { fill: #0050a7; }
  .hum { fill: #b86a00; } .humTint { fill: #fbf0e0; stroke: #d99a3e; } .humInk { fill: #8a4f00; }
  .mid { fill: #c9ced2; } .midTint { fill: #eef1f3; stroke: #b7bec3; }
  .bar2 { fill: #b8bdc1; }
  .onDark { fill: #ffffff; }
  @media (prefers-color-scheme: dark) {
    text { fill: #e7e9ea; }
    .soft { fill: #b3b8bc; } .faint { fill: #8b9196; }
    .panel { fill: #1b1f22; stroke: #2a3034; }
    .card { fill: #131618; stroke: #353c41; }
    .line { stroke: #6d7479; } .ah { fill: #6d7479; }
    .grid { stroke: #2a3034; } .track { fill: #2a3034; }
    .jev { fill: #2cc9bd; } .jevTint { fill: #15302e; stroke: #2cc9bd; } .jevInk { fill: #7fe3da; }
    .llm { fill: #6fb0ff; } .llmTint { fill: #16253a; stroke: #4d7fbf; } .llmInk { fill: #9cc8ff; }
    .hum { fill: #f0b050; } .humTint { fill: #35270f; stroke: #b8862e; } .humInk { fill: #f5c77a; }
    .mid { fill: #4a5156; } .midTint { fill: #22272b; stroke: #454c51; }
    .bar2 { fill: #5c6166; }
    .onDark { fill: #131618; }
  }
</style>
<defs>
  <marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
    <path d="M0,0 L10,5 L0,10 z" class="ah"/>
  </marker>
</defs>
"""


def svg(name: str, h: int, body: list[str], title: str) -> None:
    content = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {h}" width="{W}" height="{h}" '
               f'role="img" aria-label="{escape(title)}">\n<title>{escape(title)}</title>{STYLE}\n'
               + "\n".join(body) + "\n</svg>\n")
    folder = OUT / SLUG.get(name, "")
    folder.mkdir(parents=True, exist_ok=True)
    (folder / name).write_text(content, encoding="utf-8")


def rect(x, y, w, h, cls="panel", rx=10):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" class="{cls}"/>'


def t(x, y, s, size=14, cls="", weight=400, anchor="start"):
    c = f' class="{cls}"' if cls else ""
    return (f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" '
            f'text-anchor="{anchor}"{c}>{escape(s)}</text>')


def lines(x, y, rows, size=14, cls="", weight=400, anchor="start", lh=None):
    lh = lh or round(size * 1.4)
    return [t(x, y + i * lh, r, size, cls, weight, anchor) for i, r in enumerate(rows)]


def arrow(x1, y1, x2, y2, dashed=False):
    d = ' stroke-dasharray="5 4"' if dashed else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="line" stroke-width="1.6"{d} marker-end="url(#ah)"/>'


def path_arrow(d, dashed=False):
    da = ' stroke-dasharray="5 4"' if dashed else ""
    return f'<path d="{d}" class="line" stroke-width="1.6"{da} marker-end="url(#ah)"/>'


def hbar(x, y, w, h, cls):
    """Хоризонтален стълб, закръглен само в края с данните."""
    if w <= 0:
        return ""
    r = min(4, w, h / 2)
    return (f'<path d="M{x},{y} H{x + w - r} Q{x + w},{y} {x + w},{y + r} V{y + h - r} '
            f'Q{x + w},{y + h} {x + w - r},{y + h} H{x} Z" class="{cls}"/>')


def vbar(x, y_base, w, h, cls):
    """Вертикален стълб от базовата линия нагоре, закръглен само отгоре."""
    if h <= 0:
        return ""
    r = min(4, h, w / 2)
    top = y_base - h
    return (f'<path d="M{x},{y_base} V{top + r} Q{x},{top} {x + r},{top} H{x + w - r} '
            f'Q{x + w},{top} {x + w},{top + r} V{y_base} Z" class="{cls}"/>')


def pill(x, y, s, cls="card", tcls="soft", size=12):
    w = round(len(s) * size * 0.58) + 18
    return [rect(x, y, w, 22, cls, 11), t(x + w / 2, y + 15, s, size, tcls, anchor="middle")], w


# 1 - Система 1 и Система 2 ----------------------------------------------------------
def d1():
    b = []
    for x, tint, ink, head, sub in [
        (20, "jevTint", "jevInk", "Система 1", "бързо | интуитивно | без усилие"),
        (395, "llmTint", "llmInk", "Система 2", "бавно | последователно | с усилие"),
    ]:
        b += [rect(x, 20, 345, 290, tint, 14),
              t(x + 22, 54, head, 22, ink, 700),
              t(x + 22, 78, sub, 13, "soft")]
    # пример Система 1
    b += [t(42, 124, "'Този имейл е спам.'", 20, weight=600),
          t(42, 150, "частица от секундата, без да мислиш как", 13, "soft"),
          hbar(42, 166, 26, 10, "jev"), t(76, 175, "< 1 s", 12, "faint"),
          t(42, 206, "В софтуера: спам ли е? спешно ли е?", 13, "soft"),
          t(42, 224, "в коя папка отива?", 13, "soft")]
    # пример Система 2
    b += [t(417, 124, "17 x 24 = ?", 20, weight=600)]
    for i, s in enumerate(["17 x 20 = 340", "17 x 4 = 68", "340 + 68 = 408"]):
        b.append(t(432, 150 + i * 20, f"{i + 1}.  {s}", 13, "soft mono"))
    b += [hbar(417, 206, 150, 10, "llm"), t(575, 215, "стъпка по стъпка", 12, "faint")]
    # разделител и ИИ аналог
    for x, ink, what, tags in [
        (20, "jevInk", "System One модел (Jev)", ["избор", "вероятност", "70-500 ms"]),
        (395, "llmInk", "LLM с reasoning (Claude, GPT...)", ["текст", "обяснение", "секунди"]),
    ]:
        b += [f'<line x1="{x + 22}" y1="236" x2="{x + 323}" y2="236" class="grid" stroke-width="1"/>',
              t(x + 22, 258, "В ИИ:", 12, "faint"),
              t(x + 64, 258, what, 14, ink, 700)]
        px = x + 22
        for s in tags:
            p, w = pill(px, 272, s)
            b += p
            px += w + 8
    svg("01-sistema-1-i-2.svg", 330, b, "Система 1 и Система 2: бързото решение срещу бавното разсъждение")


# 2 - токен по токен срещу едно изчисление ------------------------------------------------
def d2():
    b = [rect(20, 16, 720, 150, "llmTint", 14),
         t(40, 46, "LLM: авторегресивно, токен по токен", 16, "llmInk", 700),
         t(40, 68, "всеки следващ токен зависи от предишните -> толкова изчисления, колкото токена", 12, "soft")]
    toks = ["Отделът", "е", "'tech", "nical'", "."]
    x = 40
    for i, s in enumerate(toks):
        w = max(52, round(len(s) * 9) + 22)
        b += [rect(x, 88, w, 34, "card", 7), t(x + w / 2, 110, s, 14, "mono", anchor="middle"),
              t(x + w / 2, 142, f"стъпка {i + 1}", 11, "faint", anchor="middle")]
        if i < len(toks) - 1:
            b.append(arrow(x + w + 2, 105, x + w + 20, 105))
        x += w + 24
    b += lines(560, 100, ["5 токена = 5 изчисления", "изходът се плаща", "форматът може да се счупи"], 12, "soft", lh=18)

    b += [rect(20, 184, 720, 196, "jevTint", 14),
          t(40, 214, "System One модел: едно паралелно изчисление", 16, "jevInk", 700),
          t(40, 236, "моделът оценява всички твои опции наведнъж и връща вероятности", 12, "soft")]
    b += [rect(40, 262, 150, 86, "card", 8)]
    b += lines(56, 288, ["state:", "'Бутонът за", "експорт не работи...'"], 12, "soft", lh=18)
    b += [rect(230, 280, 90, 50, "jev", 10), t(275, 311, "Jev", 17, "onDark", 700, "middle"),
          arrow(192, 305, 226, 305)]
    opts = [("billing", 0.15), ("technical", 0.85), ("sales", 0.00)]
    for i, (lab, p) in enumerate(opts):
        y = 262 + i * 34
        b += [path_arrow(f"M322,305 C350,305 350,{y + 11} 372,{y + 11}"),
              t(380, y + 16, lab, 13, "mono"),
              rect(462, y + 3, 150, 16, "track", 4), hbar(462, y + 3, round(150 * p), 16, "jev"),
              t(620, y + 16, f"{p:.2f}", 13, "soft")]
    b += [t(40, 372, "1 изчисление -> всички опции наведнъж | изходът е безплатен | само опции от твоя списък", 12, "faint")]
    svg("02-token-po-token-vs-edin-prohod.svg", 396, b, "LLM генерира токен по токен, System One моделът оценява всички опции с едно изчисление")


# 3 - анатомия на заявката ------------------------------------------------------------
def d3():
    b = [rect(20, 20, 330, 102, "card", 10), t(36, 44, "state", 13, "mono faint", 600)]
    b += lines(36, 68, ["'Бутонът за експорт не работи от вчера,", "а отчетът ми е за след два часа!'"], 14, lh=22)
    b += [rect(20, 138, 330, 150, "card", 10), t(36, 162, "questions", 13, "mono faint", 600)]
    qs = [("urgent", "Noul", "'Съобщението е спешно'"),
          ("department", "Choice", "billing | technical | sales"),
          ("severity", "Score", "козметично ... блокиращо")]
    for i, (k, typ, d) in enumerate(qs):
        y = 190 + i * 34
        b += [t(36, y, k, 13, "mono"), t(130, y, typ, 13, "jevInk", 700), t(130, y + 16, d, 12, "soft")]
    b += [path_arrow("M352,71 C380,71 380,150 400,150"), path_arrow("M352,213 C380,213 380,165 400,165"),
          rect(404, 110, 132, 96, "jev", 12), t(470, 150, "Jev", 20, "onDark", 700, "middle"),
          t(470, 172, "едно изчисление", 12, "onDark", anchor="middle"),
          t(470, 188, "70-500 ms", 12, "onDark", anchor="middle"),
          arrow(538, 158, 566, 158)]
    b += lines(470, 232, ["чете state веднъж,", "отговаря на всички", "въпроси паралелно"], 12, "faint", anchor="middle", lh=17)
    b += [rect(570, 40, 170, 236, "jevTint", 10), t(586, 64, "answers", 13, "mono jevInk", 600)]
    ans = [("urgent", "0.97", "вероятност за 'да'"),
           ("department", "technical", "confidence 0.78"),
           ("severity", "1.4", "между 1 и 2")]
    for i, (k, v, n) in enumerate(ans):
        y = 100 + i * 60
        b += [t(586, y, k, 12, "mono faint"), t(586, y + 22, v, 18, weight=700), t(586, y + 40, n, 11, "soft")]
    svg("03-anatomiya-na-zayavka.svg", 308, b, "Една заявка: state и въпроси влизат, типизирани отговори излизат")


# 4 - трите примитива -----------------------------------------------------------------
def d4():
    b = []
    cards = [(20, "Noul", "да / не"), (265, "Choice", "една от няколко опции"), (510, "Score", "позиция по скала")]
    for x, name, sub in cards:
        b += [rect(x, 20, 230, 250, "panel", 12), t(x + 18, 52, name, 20, "jevInk", 700), t(x + 18, 74, sub, 13, "soft")]
    # Noul
    b += [t(38, 110, "'Съобщението е спешно'", 13, "soft"),
          rect(38, 132, 194, 18, "track", 5), hbar(38, 132, round(194 * 0.97), 18, "jev"),
          t(38, 170, "0", 11, "faint"), t(232, 170, "1", 11, "faint", anchor="end"),
          t(38, 206, "noul = 0.97", 18, "mono", 700),
          t(38, 250, "-> една вероятност, че е 'да'", 12, "faint")]
    # Choice
    for i, (lab, p) in enumerate([("technical", 0.85), ("billing", 0.15), ("sales", 0.00)]):
        y = 100 + i * 30
        b += [t(283, y + 13, lab, 12, "mono"), rect(358, y + 1, 96, 14, "track", 4),
              hbar(358, y + 1, round(96 * p), 14, "jev" if i == 0 else "bar2"), t(460, y + 13, f"{p:.2f}", 11, "soft")]
    b += [t(283, 206, "choice = technical", 15, "mono", 700), t(283, 226, "confidence = 0.78", 13, "mono soft"),
          t(283, 250, "-> избор + разпределение", 12, "faint")]
    # Score
    x0, x1, y = 540, 710, 140
    b += [f'<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" class="line" stroke-width="3"/>']
    for i in range(3):
        xx = x0 + i * (x1 - x0) / 2
        b += [f'<circle cx="{xx}" cy="{y}" r="5" class="mid"/>', t(xx, y + 24, str(i), 12, "faint", anchor="middle")]
    mx = x0 + 1.4 * (x1 - x0) / 2
    b += [f'<circle cx="{mx}" cy="{y}" r="8" class="jev"/>', t(mx, y - 16, "1.4", 13, "jevInk", 700, "middle"),
          t(528, 190, "0 козметично | 1 има", 11, "soft"), t(528, 205, "заобикаляне | 2 блокиращо", 11, "soft"),
          t(528, 232, "score = 1.4", 15, "mono", 700),
          t(528, 250, "-> позиция, може да е дробна", 12, "faint")]
    svg("04-trite-primitiva.svg", 290, b, "Трите примитива: Noul, Choice и Score и какво връща всеки")


# 5 - вероятност срещу увереност ------------------------------------------------------
def d5():
    b = []
    sets = [(20, "висока увереност", [0.90, 0.06, 0.04], "jevInk"),
            (395, "ниска увереност", [0.40, 0.33, 0.27], "humInk")]
    for x, head, ps, ink in sets:
        base, hmax = 220, 140
        b += [rect(x, 20, 345, 262, "panel", 12),
              t(x + 20, 50, "choice = A", 15, "mono", 700), t(x + 20, 72, head, 14, ink, 700)]
        b.append(f'<line x1="{x + 40}" y1="{base}" x2="{x + 305}" y2="{base}" class="line" stroke-width="1"/>')
        for i, (lab, p) in enumerate(zip("ABC", ps)):
            bx = x + 60 + i * 85
            b += [vbar(bx, base, 50, round(hmax * p), "jev" if i == 0 else "bar2"),
                  t(bx + 25, base - round(hmax * p) - 8, f"{p:.2f}", 13, "soft", anchor="middle"),
                  t(bx + 25, base + 20, lab, 14, weight=600, anchor="middle")]
        note = "всичко е на една опция" if ps[0] > 0.5 else "почти равномерно - А печели на косъм"
        b.append(t(x + 20, 268, note, 12, "faint"))
    svg("05-veroyatnost-uverenost.svg", 300, b, "Един и същ избор с висока и с ниска увереност")


# 6 - три зони на действие ------------------------------------------------------------
def d6():
    x0, x1 = 60, 720
    sx = lambda c: x0 + (x1 - x0) * c
    b = []
    rows = [(50, "Ниско-рисково действие: 'покажи баланса' | праг 0.5",
             [(0, 0.5, "humTint", "humInk", "не действай -> човек"), (0.5, 1, "jevTint", "jevInk", "действай")]),
            (150, "Рисково действие: 'преведи парите' | праг 0.9",
             [(0, 0.5, "humTint", "humInk", "не действай -> човек"),
              (0.5, 0.9, "midTint", "soft", "поискай потвърждение"), (0.9, 1, "jevTint", "jevInk", "действай")])]
    for y, head, segs in rows:
        b.append(t(x0, y - 12, head, 14, weight=600))
        for a, c, cls, ink, lab in segs:
            b += [rect(sx(a) + 1, y, sx(c) - sx(a) - 2, 44, cls, 6)]
            size = 13 if c - a > 0.2 else 11
            b.append(t((sx(a) + sx(c)) / 2, y + 27, lab, size, ink, 600, "middle"))
    ay = 222
    b.append(f'<line x1="{x0}" y1="{ay}" x2="{x1}" y2="{ay}" class="line" stroke-width="1"/>')
    for c in (0, 0.5, 0.9, 1.0):
        b += [f'<line x1="{sx(c)}" y1="{ay}" x2="{sx(c)}" y2="{ay + 6}" class="line" stroke-width="1"/>',
              t(sx(c), ay + 22, f"{c:g}", 12, "faint", anchor="middle")]
    b.append(t((x0 + x1) / 2, ay + 44, "confidence", 12, "faint mono", anchor="middle"))
    svg("06-tri-zoni.svg", 280, b, "Три зони за действие според увереността; прагът расте с риска")


# 7 - класически срещу zero-shot класификатор -----------------------------------------
def d7():
    b = [rect(20, 20, 280, 300, "panel", 12),
         t(40, 50, "Класически класификатор", 15, weight=700),
         t(40, 70, "класовете са вградени в модела", 12, "soft"),
         rect(40, 150, 60, 40, "card", 8), t(70, 175, "текст", 13, anchor="middle"),
         arrow(102, 170, 118, 170), rect(122, 130, 60, 80, "mid", 10), t(152, 175, "модел", 12, anchor="middle")]
    for i, lab in enumerate(["billing", "technical", "sales"]):
        cy = 125 + i * 45
        b += [path_arrow(f"M184,170 C194,170 194,{cy} 202,{cy}"),
              f'<circle cx="214" cy="{cy}" r="9" class="midTint" stroke-width="1.5"/>',
              t(229, cy + 4, lab, 11, "mono soft")]
    b += lines(40, 278, ["нов клас -> нови етикетирани", "примери и ново обучение"], 12, "humInk", 600, lh=17)

    b += [rect(316, 20, 424, 300, "jevTint", 12),
          t(336, 50, "Zero-shot класификатор", 15, "jevInk", 700),
          t(336, 70, "класовете са част от входа: f(текст, описание) -> число", 12, "soft")]
    rows = [("Payment, invoice...", "2.1", "0.10"), ("Bugs, errors...", "4.3", "0.89"), ("Pricing, seats...", "0.2", "0.01")]
    for i, (d, s, p) in enumerate(rows):
        y = 96 + i * 56
        b += [rect(336, y, 168, 40, "card", 8), t(346, y + 17, "текст +", 11, "faint"),
              t(346, y + 32, d, 12, "mono"), arrow(506, y + 20, 524, y + 20),
              rect(528, y + 5, 34, 30, "jev", 7), t(545, y + 25, "f", 14, "onDark", 700, "middle"),
              arrow(564, y + 20, 582, y + 20), t(588, y + 25, s, 13, "mono")]
    b += [rect(622, 96, 30, 152, "card", 7),
          f'<text x="641" y="172" font-size="12" text-anchor="middle" transform="rotate(-90 641 172)" class="soft">softmax</text>']
    for i, (_, _, p) in enumerate(rows):
        y = 96 + i * 56
        b += [arrow(654, y + 20, 672, y + 20),
              t(678, y + 25, p, 14, "jevInk" if i == 1 else "soft", 700 if i == 1 else 400)]
    b += lines(336, 278, ["етикетът няма собствен неврон - моделът чете описанието;",
                          "опциите може да са различни при всяко извикване"], 12, "jevInk", 600, lh=17)
    svg("07-klasicheski-vs-zero-shot.svg", 340, b, "Класически класификатор с вградени класове срещу zero-shot класификатор с класове във входа")


# 8 - етапи на обучение ---------------------------------------------------------------
def d8():
    b = []
    stages = [("1", "Pretraining", ["огромно количество текст", "без етикети", "-> разбиране на езика"]),
              ("2", "Multi-task fine-tuning", ["хиляди различни задачи:", "текст + въпрос + опции", "-> верен отговор"]),
              ("3", "Калибриране", ["наказание, когато е", "уверен и греши", "(при Jev: RLCD)"])]
    for i, (n, name, rows) in enumerate(stages):
        x = 20 + i * 245
        b += [rect(x, 20, 225, 190, "jevTint" if i == 2 else "panel", 12),
              f'<circle cx="{x + 30}" cy="50" r="14" class="jev"/>', t(x + 30, 55, n, 14, "onDark", 700, "middle"),
              t(x + 54, 56, name, 15, weight=700)]
        b += lines(x + 20, 92, rows, 13, "soft", lh=20)
        if i < 2:
            b.append(arrow(x + 227, 115, x + 243, 115))
    px = 285
    for s in ["спам", "тема", "тон", "спешност", "език", "..."]:
        p, w = pill(px, 164, s, size=11)
        if px + w > 470:
            break
        b += p
        px += w + 5
    b += [rect(20, 226, 715, 44, "jevTint", 10),
          t(378, 254, "Обобщаването идва от разнообразието на задачите: 10 000 вида въпроси -> справя се и с 10 001-вия", 13, "jevInk", 600, "middle")]
    svg("08-etapi-na-obuchenie.svg", 286, b, "Трите етапа на обучение на zero-shot класификатор")


# 9 - каскада -------------------------------------------------------------------------
def d9():
    b = [rect(20, 118, 100, 44, "card", 10), t(70, 145, "заявка", 14, anchor="middle"),
         arrow(122, 140, 158, 140),
         rect(162, 88, 190, 104, "jev", 12), t(257, 118, "Jev", 20, "onDark", 700, "middle"),
         t(257, 142, "тип? сложност?", 12, "onDark", anchor="middle"),
         t(257, 158, "увереност?", 12, "onDark", anchor="middle"),
         t(257, 178, "~100 ms | части от цент", 11, "onDark", anchor="middle")]
    outs = [(30, "jevTint", "jevInk", "просто и сигурно", "обикновен код / шаблон"),
            (118, "llmTint", "llmInk", "средно", "LLM специалист пише отговора"),
            (206, "humTint", "humInk", "ниска увереност / рисково", "човек")]
    for y, cls, ink, cond, dest in outs:
        b += [path_arrow(f"M354,140 C390,140 390,{y + 30} 424,{y + 30}"),
              rect(428, y, 310, 60, cls, 10), t(446, y + 25, cond, 12, "soft"), t(446, y + 46, "-> " + dest, 15, ink, 700)]
    b += [t(380, 296, "Jev решава накъде. LLM прави генеративната работа. Кодът държи контрола.", 13, "faint", 600, "middle")]
    svg("09-kaskada.svg", 310, b, "Каскада: Jev маршрутизира към код, LLM или човек")


# 10 - независимият benchmark ---------------------------------------------------------
def d10():
    data = [("Jev 1.13", "API", 96.5, "~330 ms"), ("GLiNER2 large", "локално", 69.7, "73 ms"),
            ("von 1.0.1", "локално", 68.7, "55 ms"), ("Laya (английски)", "локално", 58.7, "46 ms")]
    x0, x1 = 190, 600
    sx = lambda v: x0 + (x1 - x0) * v / 100
    b = [t(690, 30, "латентност", 11, "faint")]
    for g in (0, 25, 50, 75, 100):
        b += [f'<line x1="{sx(g)}" y1="42" x2="{sx(g)}" y2="222" class="grid" stroke-width="1"/>',
              t(sx(g), 240, f"{g}%", 11, "faint", anchor="middle")]
    for i, (name, where, v, lat) in enumerate(data):
        y = 52 + i * 42
        b += [t(20, y + 15, name, 14, weight=700 if i == 0 else 400), t(20, y + 31, where, 11, "faint"),
              hbar(x0, y + 2, round(sx(v) - x0), 26, "jev" if i == 0 else "bar2"),
              t(sx(v) + 8, y + 20, f"{v:.1f}%".replace(".", ","), 13, weight=700 if i == 0 else 400),
              t(690, y + 20, lat, 12, "soft")]
    b += [t(20, 272, "Точност (micro) | jabr/classifier-benchmark: 947 синтетични случая, 57 задачи, само английски, предварителен", 11, "faint")]
    svg("10-benchmark.svg", 288, b, "Независим benchmark: Jev 96,5%, GLiNER2 69,7%, von 68,7%, Laya 58,7%")


# 11 - категоризаторът на блог постове ------------------------------------------------
def d11():
    b = [rect(20, 40, 130, 76, "card", 10), t(85, 70, "нов пост", 14, weight=700, anchor="middle"),
         t(85, 90, "заглавие + текст", 11, "soft", anchor="middle"),
         arrow(152, 78, 180, 78),
         rect(184, 20, 250, 136, "jev", 12), t(200, 46, "1 | Laya или Jev", 15, "onDark", 700),
         t(200, 66, "Choice | Laya на CPU ~0,2 s | Jev ~0,4 s", 12, "onDark")]
    cats = ["Програмиране", "Пътувания", "Готвене", "Лични финанси", "друга тема"]
    px, py = 200, 80
    for c in cats:
        w = round(len(c) * 6.4) + 14
        if px + w > 424:
            px, py = 200, py + 24
        b += [rect(px, py, w, 20, "card", 10), t(px + w / 2, py + 14, c, 11, "soft", anchor="middle")]
        px += w + 5
    # разклонение
    b += [path_arrow("M436,60 C470,60 470,50 494,50"), path_arrow("M436,110 C470,110 470,200 494,200"),
          rect(498, 20, 240, 68, "jevTint", 10), t(514, 44, "съществуваща категория", 12, "soft"),
          t(514, 66, "предложение + втора възможност", 12, "jevInk", 700),
          rect(498, 158, 240, 90, "llmTint", 10), t(514, 182, "'друга тема'", 12, "soft"),
          t(514, 204, "2 | BgGPT 3.0 4B (Ollama)", 14, "llmInk", 700),
          t(514, 224, "име на български + описание", 12, "soft"), t(514, 240, "на английски, ~6 s", 12, "soft")]
    # човекът
    b += [path_arrow("M510,90 C490,180 460,230 420,268"), path_arrow("M600,250 C600,290 520,300 474,300"),
          rect(214, 272, 256, 56, "humTint", 10), t(230, 296, "човек: приема или поправя", 14, "humInk", 700),
          t(230, 316, "с едно щракване | conf < 0,5 -> 'Несигурно'", 11, "soft")]
    # новата категория се връща в списъка
    b += [path_arrow("M212,272 C120,262 110,190 230,158", dashed=True),
          *lines(30, 190, ["новата категория", "влиза в списъка"], 11, "faint", lh=15)]
    svg("11-blog-kategorizator.svg", 344, b, "Категоризатор на блог постове: Laya или Jev избира, BgGPT измисля име, човекът решава")


# 14 - Laya срещу Jev върху 50-те тестови поста ---------------------------------------
def d14():
    groups = [("всички", 50, 48, 36), ("съществуваща категория", 28, 28, 24), ("нова тема", 22, 20, 12)]
    x0, x1 = 230, 640
    sx = lambda v: x0 + (x1 - x0) * v / 100
    b = [rect(x0, 14, 12, 12, "jev", 3), t(x0 + 18, 25, "Jev (API)", 12, "soft"),
         rect(x0 + 110, 14, 12, 12, "bar2", 3), t(x0 + 128, 25, "Laya multilingual (локално)", 12, "soft")]
    for g in (0, 25, 50, 75, 100):
        b += [f'<line x1="{sx(g)}" y1="40" x2="{sx(g)}" y2="262" class="grid" stroke-width="1"/>',
              t(sx(g), 280, f"{g}%", 11, "faint", anchor="middle")]
    for i, (name, n, jev, laya) in enumerate(groups):
        y = 50 + i * 72
        b += [t(20, y + 22, name, 14, weight=700 if i == 0 else 400), t(20, y + 40, f"{n} поста", 11, "faint")]
        for j, (v, cls) in enumerate([(jev, "jev"), (laya, "bar2")]):
            pct = 100 * v / n
            yy = y + 4 + j * 28
            b += [hbar(x0, yy, round(sx(pct) - x0), 24, cls),
                  t(sx(pct) + 8, yy + 17, f"{v}/{n}", 13, weight=700 if j == 0 else 400)]
    b += [t(20, 306, "Вярно предложение при 4 начални категории | при нова тема се мери само 'друга тема', не името", 11, "faint")]
    svg("14-laya-sreshtu-jev.svg", 318, b, "Laya срещу Jev върху 50 поста на български: 36/50 срещу 48/50")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        OUT = Path(sys.argv[1]).resolve()
    # d8 (08-etapi-na-obuchenie.svg) is not used in any post, so it is not run.
    for f in (d1, d2, d3, d4, d5, d6, d7, d9, d10, d11, d14):
        f()
    print("done:", sorted(str(p.relative_to(OUT)) for p in OUT.glob("*/*.svg")))
