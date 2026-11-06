#!/usr/bin/env python3
"""README visuals for dsh-railway-window — derived from the plugin's real pipeline.

Two figures, both read off the shipped code and rule pack:

  hero 1440×576 (Pillow, 4 files: zh/en × light/dark)
      The material itself: the quickstart register row (#1, V 类, 09:00–11:00,
      0.0833 days, 120 applied / 120 approved) and a work-window track whose
      09:00–11:00 possession block carries the arithmetic (2 h = 0.0833 d,
      tolerance 0.01). Under it sit the two outcomes the quickstart actually
      produces: the RW-001 finding (workContent + permitNo blank) and the
      RW-005 skip (values ships empty), then the report line — 1 difference,
      1 check not executed, the verdict left to the reviewer.

  flow 1100×660 (hand-written SVG, 2 files: light/dark)
      A three-bay check bench, not a row of five boxes:
        A  material gate — the two entry channels (file / material) and the
           reader's hard requirement (at least one of windowNo / startAt /
           endAt / workContent, otherwise it errors instead of returning an
           empty report);
        B  the rule pack — load-time validation (evidence caps severity,
           excerpt must be verbatim) and the seven checks in pack order, each
           with the fields it reads and the check kind that implements it
           (RW-005 ships an empty vocabulary and skips by default);
        C  the two channels that reach the report — issues[] located by row and
           column, skipped[] with a rule id and a reason — then the merge line,
           the report card and the reviewer, with the "a clean check leaves no
           entry" rule stated under the bench.
      A fork on the bench's right edge splits the seven checks into the two
      channels; a full-width footer carries the evidence and config facts.

Numbers come from the repository, not from imagination:
  samples/quickstart/input/RW-001-unsafe.json   (09:00–11:00, 0.0833 d,
      120 applied / 120 approved, blank workContent + permitNo)
  samples/quickstart/expected/result.json        (1 issue, 1 skipped)
  rules/railway-window.yaml                      (RW-001..RW-007, check kinds,
      severities, values: [])
  src/index.ts, src/model.ts, src/view.ts, src/shared/{ruleset,rows}.ts

The older docs/assets/dsh-railway-window-flow.svg and -flow-{light,dark}.svg are
left untouched on purpose — external links may still point at them — but every
README now uses the hero pair and the -flow-v5 pair written here.

Run once:  python scripts/gen-readme-assets.py
Requires:  Pillow + Windows fonts msyh.ttc / msyhbd.ttc / consola.ttf.
"""
from __future__ import annotations

import os
from html import escape

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "docs", "assets")

FONT_CJK = r"C:\Windows\Fonts\msyh.ttc"
FONT_CJK_BOLD = r"C:\Windows\Fonts\msyhbd.ttc"
FONT_MONO = r"C:\Windows\Fonts\consola.ttf"
FONT_MONO_BOLD = r"C:\Windows\Fonts\consolab.ttf"
for _p in (FONT_CJK, FONT_CJK_BOLD, FONT_MONO, FONT_MONO_BOLD):
    if not os.path.exists(_p):
        raise SystemExit(f"FATAL: font missing: {_p}")

RADIUS = 20
FONT_FILES = {"cjk": FONT_CJK, "cjk_bold": FONT_CJK_BOLD,
              "mono": FONT_MONO, "mono_bold": FONT_MONO_BOLD}

SKIN = {
    "light": dict(
        bg_from="#f9f6fd", bg_to="#e4eaf8",
        card="#ffffff", card_edge="#e6e2ef",
        text="#141419", sub="#4d5261", faint="#8f94a4",
        accent="#4B67B4", accent2="#16a34a",
        pill="#ece7f9", band="#f5f2fb", grid="#e7e4f0",
        mark="#b45309", mark_bg="#fdf3e9",
        rail_soft="#e8ecf8", rail_tie="#c3cdea", rail="#c9cfdd",
        shadow=(32, 26, 64), shadow_a=52, glow2="#7a68c9",
    ),
    "dark": dict(
        bg_from="#131a2a", bg_to="#0c1016",
        card="#1b2231", card_edge="#2e374b",
        text="#f0f3f9", sub="#a8b1c4", faint="#737b8d",
        accent="#8496f5", accent2="#3fb950",
        pill="#242d42", band="#202839", grid="#262f42",
        mark="#d9a441", mark_bg="#2a2216",
        rail_soft="#27304a", rail_tie="#3c4a72", rail="#37415a",
        shadow=(0, 0, 0), shadow_a=120, glow2="#8496f5",
    ),
}


def font(size: int, kind: str = "cjk_bold") -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_FILES[kind], size)


def hx(s: str) -> tuple[int, int, int]:
    s = s.lstrip("#")
    return tuple(int(s[i:i + 2], 16) for i in (0, 2, 4))


def gradient(w: int, h: int, c1: str, c2: str) -> Image.Image:
    """A soft diagonal wash in the family's light/dark background colours."""
    sw, sh = 96, 48
    small = Image.new("RGB", (sw, sh))
    px = small.load()
    a, b = hx(c1), hx(c2)
    for y in range(sh):
        for x in range(sw):
            t = (0.58 * x / (sw - 1) + 0.42 * y / (sh - 1)) ** 1.05
            px[x, y] = tuple(int(p + (q - p) * t) for p, q in zip(a, b))
    return small.resize((w, h), Image.BICUBIC)


def glow(img: Image.Image, cx: int, cy: int, r: int, color: tuple,
         alpha: int) -> Image.Image:
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color + (alpha,))
    layer = layer.filter(ImageFilter.GaussianBlur(r * 0.42))
    return Image.alpha_composite(img.convert("RGBA"), layer).convert("RGB")


def card(img: Image.Image, box: tuple, s: dict, radius: int = RADIUS,
         shadow: int = 22, fill: str | None = None,
         outline: str | None = None, width: int = 2) -> Image.Image:
    """A soft-shadowed rounded card on the gradient background."""
    x0, y0, x1, y1 = box
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    ld.rounded_rectangle([x0, y0 + shadow * 0.35, x1, y1 + shadow * 0.6],
                         radius=radius, fill=s["shadow"] + (s["shadow_a"],))
    layer = layer.filter(ImageFilter.GaussianBlur(shadow * 0.62))
    base = Image.alpha_composite(img.convert("RGBA"), layer)
    d = ImageDraw.Draw(base)
    d.rounded_rectangle(box, radius=radius, fill=hx(fill or s["card"]),
                        outline=hx(outline or s["card_edge"]), width=width)
    return base.convert("RGB")


_SCRATCH = ImageDraw.Draw(Image.new("RGB", (8, 8)))


def measure(text: str, size: int, kind: str) -> float:
    return _SCRATCH.textlength(text, font=font(size, kind))


def measure_svg(text: str, size: int, kind: str) -> float:
    """Browser-like advance width for SVG layout.

    Pillow rounds hinted advances to whole pixels, so a 15px Consolas run
    measures 112px here while a browser lays it out at 115.5px. Measuring at
    4× and dividing recovers the fractional advance; CJK advances are already
    integral and are left untouched.
    """
    if kind.startswith("mono"):
        return _SCRATCH.textlength(text, font=font(size * 4, kind)) / 4.0
    return measure(text, size, kind)


def require_w(text: str, size: int, kind: str, max_w: float, what: str) -> None:
    """Fail loudly instead of shipping a clipped label."""
    w = measure(text, size, kind)
    if w > max_w + 0.4:
        raise SystemExit(f"FATAL: {what} overflows: {text!r} needs {w:.1f}px > {max_w}px")


def fit(text: str, kind: str, max_w: float, start: int, minimum: int) -> int:
    size = start
    while size > minimum:
        if measure(text, size, kind) <= max_w:
            return size
        size -= 1
    raise SystemExit(f"FATAL: text does not fit {max_w}px at >= {minimum}px: {text!r}")


def fit_lines(lines: list[str], kind: str, max_w: float, start: int,
              minimum: int) -> int:
    return min(fit(t, kind, max_w, start, minimum) for t in lines)


def pill(img: Image.Image, xy: tuple[int, int], text: str, s: dict,
         size: int = 16, fg: str | None = None, bg: str | None = None,
         kind: str = "cjk_bold") -> tuple[int, int]:
    d = ImageDraw.Draw(img)
    f = font(size, kind)
    w = d.textlength(text, font=f)
    x, y = xy
    h = size + 20
    d.rounded_rectangle([x, y, x + w + 30, y + h], radius=h // 2,
                        fill=hx(bg or s["pill"]))
    d.text((x + 15, y + h / 2), text, font=f, fill=hx(fg or s["accent"]),
           anchor="lm")
    return int(x + w + 30), int(y + h)


def badge(img: Image.Image, xy: tuple[int, int], text: str, fg: str, bg: str,
          size: int = 11, kind: str = "cjk_bold", pad: int = 8,
          height: int = 20) -> int:
    """A small pill anchored on its left edge; returns its width."""
    d = ImageDraw.Draw(img)
    f = font(size, kind)
    w = d.textlength(text, font=f)
    x, y = xy
    d.rounded_rectangle([x, y, x + w + pad * 2, y + height],
                        radius=height // 2, fill=hx(bg))
    d.text((x + pad, y + height / 2), text, font=f, fill=hx(fg), anchor="lm")
    return int(w + pad * 2)


def dash_rect(d: ImageDraw.ImageDraw, box: tuple, color: str, width: int = 2,
              dash: int = 7, gap: int = 5) -> None:
    x0, y0, x1, y1 = box
    for a, b in (((x0, y0), (x1, y0)), ((x0, y1), (x1, y1)),
                 ((x0, y0), (x0, y1)), ((x1, y0), (x1, y1))):
        length = ((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2) ** 0.5
        if length == 0:
            continue
        steps = int(length // (dash + gap)) + 1
        for i in range(steps):
            t0 = i * (dash + gap) / length
            t1 = min((i * (dash + gap) + dash) / length, 1.0)
            if t0 >= 1:
                break
            d.line([(a[0] + (b[0] - a[0]) * t0, a[1] + (b[1] - a[1]) * t0),
                    (a[0] + (b[0] - a[0]) * t1, a[1] + (b[1] - a[1]) * t1)],
                   fill=hx(color), width=width)


def text_at(img: Image.Image, x: int, y: int, text: str, size: int,
            kind: str, fill: str, anchor: str = "ls") -> None:
    """Baseline-anchored text; layout coordinates stay predictable."""
    ImageDraw.Draw(img).text((x, y), text, font=font(size, kind),
                             fill=hx(fill), anchor=anchor)


# --------------------------------------------------------------------------- hero
# Every value below is an excerpt of this repository's own fixtures / rule pack;
# see the module docstring for the mapping.
HERO = {
    "zh": dict(
        kicker="DeepSeek Harness 插件 · 铁路天窗台账核对",
        title="dsh-railway-window",
        value=["七条规则，逐行逐栏核对", "差异落到行号与栏名"],
        sub=["只核对台账自身的时间与算术：起止、时长、",
             "批准与申请、编号唯一——不判合规、不认定责任。"],
        meta="RW-001..RW-007 · 规则包即数据 · skipped 逐条说明",
        foot="Apache-2.0 · PerryLink DSH plugin family",
        reg_title="天窗台账 · rows[]",
        reg_chip="只读原件",
        reg_meta="2026-03-10 · 某某铁路局集团公司 · 规则包 7 条在册",
        headers=["编号", "类型", "起止时间", "时长(天)", "申请/批准"],
        widths=[64, 78, 208, 112, 178],
        row=["1", "V 类", "09:00–11:00", "0.0833", "120 / 120"],
        reg_note="列名忽略大小写与空格；原件只读，不回写",
        win_title="天窗时间窗 · 09:00 → 11:00",
        win_chip="RW-003 · 容差 0.01 天",
        hours=["08:00", "09:00", "10:00", "11:00", "12:00"],
        win_calc="2 h = 0.0833 天（容差 0.01）",
        issue=dict(rule="RW-001", sev="warn",
                   locator="第 1 行 · workContent / permitNo",
                   found="found：都为空", expected="expected：至少填一项",
                   fix="fix：补填作业内容 / 施工命令号"),
        skip=dict(rule="RW-005", sev="info",
                  locator="windowType · values 未配置",
                  l1="本条进 skipped，写明原因", l2="不猜各局的分类口径",
                  l3="skipped[] 与 issues[] 一起读"),
        strip=("issues[] 1 条差异 · skipped[] 1 条未执行", "结论留给审核人"),
    ),
    "en": dict(
        kicker="DeepSeek Harness plugin · work-window register",
        title="dsh-railway-window",
        value=["Seven rules, row by row", "each finding keeps its cell"],
        sub=["Time and arithmetic self-consistency only —",
             "no compliance verdict; the reviewer decides."],
        meta="RW-001..RW-007 · rules are data · every skip explained",
        foot="Apache-2.0 · PerryLink DSH plugin family",
        reg_title="Work-window register · rows[]",
        reg_chip="read-only",
        reg_meta="2026-03-10 · some railway bureau · 7 rules in the pack",
        headers=["No.", "Type", "Window", "Days", "Applied / approved"],
        widths=[64, 78, 208, 112, 178],
        row=["1", "Class V", "09:00–11:00", "0.0833", "120 / 120"],
        reg_note="Column names ignore case and spaces; the original is never written back",
        win_title="Work window · 09:00 → 11:00",
        win_chip="RW-003 · tolerance 0.01 d",
        hours=["08:00", "09:00", "10:00", "11:00", "12:00"],
        win_calc="2 h = 0.0833 d (tolerance 0.01)",
        issue=dict(rule="RW-001", sev="warn",
                   locator="Row 1 · workContent / permitNo",
                   found="found: both blank", expected="expected: at least one",
                   fix="fix: fill work content / order no."),
        skip=dict(rule="RW-005", sev="info",
                  locator="windowType · values not configured",
                  l1="reported in skipped, with a reason", l2="no vocabulary is guessed",
                  l3="read skipped[] with issues[]"),
        strip=("issues[] 1 difference · skipped[] 1 not executed", "verdict stays human"),
    ),
}


def hero(lang: str, skin: str) -> None:
    s = SKIN[skin]
    H = HERO[lang]
    W, HT = 1440, 576
    img = gradient(W, HT, s["bg_from"], s["bg_to"])
    img = glow(img, 1180, 30, 430, hx(s["accent"]),
               26 if skin == "light" else 38)
    img = glow(img, 70, 600, 320, hx(s["glow2"]),
               10 if skin == "light" else 16)

    d = ImageDraw.Draw(img)
    m = 64
    col_w = 596

    # ---- left column: kicker / title / value / sub / meta / footer -----------
    pill(img, (m, 56), H["kicker"], s, size=17)
    d = ImageDraw.Draw(img)

    title_size = fit(H["title"], "mono_bold", col_w, 58, 48)
    text_at(img, m - 2, 186, H["title"], title_size, "mono_bold", s["text"])

    vf = fit_lines(H["value"], "cjk_bold", col_w, 44, 36)
    for i, line in enumerate(H["value"]):
        text_at(img, m, 260 + i * 52, line, vf, "cjk_bold", s["text"])

    for i, line in enumerate(H["sub"]):
        require_w(line, 22, "cjk", col_w, "hero sub")
        text_at(img, m + 1, 366 + i * 30, line, 22, "cjk", s["sub"])

    require_w(H["meta"], 19, "cjk", col_w, "hero meta")
    require_w(H["foot"], 16, "cjk", col_w, "hero footer")
    text_at(img, m + 1, 448, H["meta"], 19, "cjk", s["faint"])
    d = ImageDraw.Draw(img)
    d.line([m + 1, 478, m + col_w - 4, 478], fill=hx(s["grid"]), width=2)
    text_at(img, m + 1, 508, H["foot"], 16, "cjk", s["faint"])

    # ---- right: the register card -------------------------------------------
    img = card(img, (668, 34, 1376, 232), s, radius=RADIUS, shadow=24)
    text_at(img, 692, 72, H["reg_title"], 17, "cjk_bold", s["accent"])
    cw = measure(H["reg_chip"], 11, "cjk")
    badge(img, (1352 - int(cw) - 18, 54), H["reg_chip"], s["accent"], s["pill"],
          size=11, height=20)
    text_at(img, 692, 96, H["reg_meta"], 13, "cjk", s["sub"])
    require_w(H["reg_meta"], 13, "cjk", 640, "register meta")

    x0, top = 700, 104
    xs, acc = [], x0
    for w in H["widths"]:
        xs.append(acc)
        acc += w
    x_end = acc
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([x0 - 8, top, x_end + 8, top + 26], radius=9,
                        fill=hx(s["band"]))
    for i, head in enumerate(H["headers"]):
        require_w(head, 12, "cjk_bold", H["widths"][i] - 16, "table header")
        text_at(img, xs[i] + 10, top + 18, head, 12, "cjk_bold", s["sub"])
    row_top = top + 26
    for i, value in enumerate(H["row"]):
        is_token = value.startswith(("09:", "0.0", "120"))
        kind = "mono" if is_token else "cjk"
        require_w(value, 15, kind, H["widths"][i] - 18, "table cell")
        text_at(img, xs[i] + 10, row_top + 32, value, 15, kind, s["text"])
    d = ImageDraw.Draw(img)
    d.line([x0, row_top + 54, x_end, row_top + 54], fill=hx(s["grid"]), width=1)
    require_w(H["reg_note"], 12, "cjk", 644, "register note")
    text_at(img, 692, 210, H["reg_note"], 12, "cjk", s["faint"])

    # ---- right: the work-window track ---------------------------------------
    img = card(img, (668, 242, 1376, 392), s, radius=RADIUS, shadow=24)
    text_at(img, 692, 266, H["win_title"], 14, "cjk_bold", s["accent"])
    chip_w = measure(H["win_chip"], 11, "cjk")
    badge(img, (1352 - int(chip_w) - 18, 250), H["win_chip"], s["sub"], s["band"],
          size=11, height=20)

    axis_y = 322
    ax0, ax1 = 716, 1332
    d = ImageDraw.Draw(img)
    d.line([ax0, axis_y, ax1, axis_y], fill=hx(s["rail"]), width=2)
    ticks = [716, 870, 1024, 1178, 1332]
    for i, tx in enumerate(ticks):
        d.line([tx, axis_y - 4, tx, axis_y + 4], fill=hx(s["rail"]), width=2)
        is_edge = i in (1, 3)
        text_at(img, tx, 300, H["hours"][i], 11,
                "cjk_bold" if is_edge else "cjk",
                s["accent"] if is_edge else s["faint"], anchor="ms")

    # the possession block: two rails with ties, bounded by stop marks
    bx0, bx1, by0, by1 = 870, 1178, 306, 346
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([bx0, by0, bx1, by1], radius=10,
                        fill=hx(s["rail_soft"]), outline=hx(s["accent"]),
                        width=2)
    for ry in (by0 + 9, by0 + 23):
        d.line([bx0 + 8, ry, bx1 - 8, ry], fill=hx(s["accent"]), width=2)
    for tx in range(bx0 + 14, bx1 - 8, 22):
        d.line([tx, by0 + 9, tx, by0 + 23], fill=hx(s["rail_tie"]), width=2)
    d.line([bx0, by0 - 4, bx0, by1 + 4], fill=hx(s["accent"]), width=3)
    d.line([bx1, by0 - 4, bx1, by1 + 4], fill=hx(s["accent"]), width=3)

    d.line([bx0, 358, bx1, 358], fill=hx(s["sub"]), width=2)
    for tx in (bx0, bx1):
        d.line([tx, 354, tx, 362], fill=hx(s["sub"]), width=2)
    require_w(H["win_calc"], 12, "cjk", 360, "window arithmetic")
    text_at(img, (bx0 + bx1) // 2, 380, H["win_calc"], 12, "cjk", s["accent"],
            anchor="ms")

    # ---- right: finding card + skip card ------------------------------------
    img = card(img, (668, 402, 1012, 516), s, radius=18, shadow=20)
    A = H["issue"]
    text_at(img, 686, 426, A["rule"], 13, "mono_bold", s["accent"])
    badge(img, (686 + int(measure(A["rule"], 13, "mono_bold")) + 8, 414),
          A["sev"], s["accent"], s["pill"], size=11, height=19)
    text_at(img, 686, 450, A["locator"], 12, "cjk", s["sub"])
    text_at(img, 686, 472, A["found"], 12, "cjk", s["text"])
    text_at(img, 686, 490, A["expected"], 11, "cjk", s["sub"])
    text_at(img, 686, 508, A["fix"], 11, "cjk", s["faint"])
    for key, size in (("locator", 12), ("found", 12), ("expected", 11),
                      ("fix", 11)):
        require_w(A[key], size, "cjk", 308, f"issue {key}")

    img = card(img, (1028, 402, 1376, 516), s, radius=18, shadow=20)
    B = H["skip"]
    text_at(img, 1046, 426, B["rule"], 13, "mono_bold", s["sub"])
    badge(img, (1046 + int(measure(B["rule"], 13, "mono_bold")) + 8, 414),
          B["sev"], s["sub"], s["band"], size=11, height=19)
    text_at(img, 1046, 450, B["locator"], 12, "cjk", s["sub"])
    text_at(img, 1046, 472, B["l1"], 12, "cjk", s["text"])
    text_at(img, 1046, 490, B["l2"], 11, "cjk", s["sub"])
    text_at(img, 1046, 508, B["l3"], 11, "cjk", s["faint"])
    for key, size in (("locator", 12), ("l1", 12), ("l2", 11), ("l3", 11)):
        require_w(B[key], size, "cjk", 312, f"skip {key}")

    # ---- right: the report line ---------------------------------------------
    img = card(img, (668, 526, 1376, 564), s, radius=18, shadow=16)
    left, right = H["strip"]
    text_at(img, 686, 548, left, 13, "cjk", s["text"])
    rw = measure(right, 13, "cjk_bold")
    text_at(img, 1352 - rw, 548, right, 13, "cjk_bold", s["accent2"])
    if measure(left, 13, "cjk") + rw + 44 > 640:
        raise SystemExit("FATAL: hero report strip overflows")

    name = f"dsh-railway-window-hero-{lang}-{skin}.webp"
    img.save(os.path.join(OUT, name), "WEBP", quality=92, method=6)
    print(f"wrote {name} ({W}×{HT})")


# --------------------------------------------------------------------------- flow
FLOW = {
    "light": dict(
        bg_from="#f9f6fd", bg_to="#e4eaf8",
        panel="#ffffff", edge="#e6e2ef", band="#f5f2fb", band_alt="#faf8fe",
        text="#141419", sub="#4d5261", faint="#8f94a4",
        accent="#4B67B4", accent2="#16a34a", mark="#b45309",
        mark_bg="#fdf3e9", rule="#dcd8ea", card="#ffffff", shadow="0.10",
        glow="0.16",
    ),
    "dark": dict(
        bg_from="#131a2a", bg_to="#0c1016",
        panel="#1b2231", edge="#2e374b", band="#202839", band_alt="#1e2534",
        text="#f0f3f9", sub="#a8b1c4", faint="#737b8d",
        accent="#8496f5", accent2="#3fb950", mark="#d9a441",
        mark_bg="#2a2216", rule="#2b3348", card="#1b2231", shadow="0.45",
        glow="0.22",
    ),
}

FONT_CSS_CJK = ("'Microsoft YaHei','PingFang SC','Noto Sans CJK SC',"
                "'Source Han Sans SC',sans-serif")
FONT_CSS_MONO = "'Consolas','SFMono-Regular','Menlo',ui-monospace,monospace"

# id, severity cap, one-line job, engine check kind, fields read, default-skip
RULES = [
    ("RW-001", "warn", "作业内容或命令号至少一项", "presenceAny",
     " · workContent | permitNo", False),
    ("RW-002", "warn", "起止时间可解析且先后成立", "date",
     " · startAt ≤ endAt", False),
    ("RW-003", "warn", "时长等于起止之差（按天）", "derivedDays",
     " · durationMin ≈ end−start · 容差 0.01", False),
    ("RW-004", "info", "批准时长不超过申请时长", "fieldComparison",
     " · approvedMin ≤ appliedMin", False),
    ("RW-005", "info", "类型取自你配置的取值", "enum",
     " · windowType ∈ values · 出厂为空 → skipped", True),
    ("RW-006", "warn", "天窗编号在台账内唯一", "unique",
     " · windowNo · 忽略空白", False),
    ("RW-007", "warn", "表头声明日期与铁路局", "headerPresence",
     " · 表头 date · bureau", False),
]


class Svg:
    """Tiny SVG writer that measures every label before it is emitted."""

    def __init__(self) -> None:
        self.parts: list[str] = []
        self.overflows: list[str] = []

    def add(self, markup: str) -> None:
        self.parts.append(markup)

    def text(self, x: float, y: float, content: str, size: int, fill: str, *,
             anchor: str = "start", weight: int | None = None,
             mono: bool = False, max_w: float | None = None,
             opacity: float | None = None) -> None:
        kind = ("mono" if mono else "cjk") + ("_bold" if weight else "")
        if max_w is not None:
            w = measure_svg(content, size, kind)
            if w > max_w + 0.4:
                self.overflows.append(
                    f"{content!r} needs {w:.1f}px > {max_w}px")
        family = FONT_CSS_MONO if mono else FONT_CSS_CJK
        attrs = [f'x="{x}"', f'y="{y}"', f'fill="{fill}"',
                 f'font-family="{family}"', f'font-size="{size}"',
                 'xml:space="preserve"']
        if anchor != "start":
            attrs.append(f'text-anchor="{anchor}"')
        if weight:
            attrs.append(f'font-weight="{weight}"')
        if opacity is not None:
            attrs.append(f'opacity="{opacity}"')
        self.add(f'<text {" ".join(attrs)}>{escape(content)}</text>')

    def mixed(self, x: float, y: float, parts: list[tuple[str, bool]],
              size: int, fill: str, *, max_w: float | None = None,
              weight: int | None = None) -> None:
        """Draw runs of mono and CJK text on one baseline.

        Boundary spaces are positioned by hand instead of being written into
        the text node: SVG trims leading and trailing whitespace, which would
        glue a mono token to the CJK run that follows it.
        """
        def kind_of(mono: bool) -> str:
            return ("mono" if mono else "cjk") + ("_bold" if weight else "")

        runs: list[tuple[str, int, int, str]] = []
        total = 0.0
        for txt, mono in parts:
            kind = kind_of(mono)
            lead = len(txt) - len(txt.lstrip(" "))
            trail = len(txt) - len(txt.rstrip(" "))
            core = txt.strip(" ")
            space = measure_svg(" ", size, kind)
            pad = 2.0 if lead else 0.0
            total += (lead + trail) * space + pad + measure_svg(core, size, kind)
            runs.append((core, lead, trail, kind))
        if max_w is not None and total > max_w + 0.4:
            self.overflows.append(
                f"{''.join(p[0] for p in parts)!r} needs {total:.1f}px > {max_w}px")
        cx = x
        for core, lead, trail, kind in runs:
            space = measure_svg(" ", size, kind)
            pad = 2.0 if lead else 0.0
            if core:
                self.text(cx + lead * space + pad, y, core, size, fill,
                          mono=kind.startswith("mono"),
                          weight=weight)
            cx += lead * space + pad + measure_svg(core, size, kind) + trail * space

    def rect(self, x: float, y: float, w: float, h: float, *, fill: str,
             rx: float = 0, stroke: str | None = None, sw: float = 1.5,
             shadow: bool = False, dash: str | None = None,
             opacity: float | None = None) -> None:
        attrs = [f'x="{x}"', f'y="{y}"', f'width="{w}"', f'height="{h}"']
        if rx:
            attrs.append(f'rx="{rx}"')
        attrs.append(f'fill="{fill}"')
        if stroke:
            attrs.append(f'stroke="{stroke}"')
            attrs.append(f'stroke-width="{sw}"')
        if dash:
            attrs.append(f'stroke-dasharray="{dash}"')
        if opacity is not None:
            attrs.append(f'opacity="{opacity}"')
        if shadow:
            attrs.append('filter="url(#soft)"')
        self.add(f'<rect {" ".join(attrs)}/>')

    def line(self, x1: float, y1: float, x2: float, y2: float, *, stroke: str,
             sw: float = 1.5, dash: str | None = None,
             marker: str | None = None, opacity: float | None = None) -> None:
        attrs = [f'x1="{x1}"', f'y1="{y1}"', f'x2="{x2}"', f'y2="{y2}"',
                 f'stroke="{stroke}"', f'stroke-width="{sw}"']
        if dash:
            attrs.append(f'stroke-dasharray="{dash}"')
        if marker:
            attrs.append(f'marker-end="url(#{marker})"')
        if opacity is not None:
            attrs.append(f'opacity="{opacity}"')
        self.add(f'<line {" ".join(attrs)}/>')

    def path(self, d: str, *, stroke: str, sw: float = 1.5,
             marker: str | None = None, dash: str | None = None,
             fill: str = "none") -> None:
        attrs = [f'd="{d}"', f'fill="{fill}"', f'stroke="{stroke}"',
                 f'stroke-width="{sw}"', 'stroke-linecap="round"',
                 'stroke-linejoin="round"']
        if dash:
            attrs.append(f'stroke-dasharray="{dash}"')
        if marker:
            attrs.append(f'marker-end="url(#{marker})"')
        self.add(f'<path {" ".join(attrs)}/>')

    def badge(self, x: float, y: float, label: str, fg: str, bg: str,
              *, size: int = 11, pad: float = 8, height: float = 18,
              mono: bool = False, weight: int = 700) -> float:
        """A pill anchored on its left edge; returns its right edge."""
        kind = ("mono" if mono else "cjk") + "_bold"
        w = measure_svg(label, size, kind) + pad * 2
        self.rect(x, y, w, height, fill=bg, rx=height / 2)
        self.text(x + pad, y + height / 2 + size * 0.34, label, size, fg,
                  weight=weight, mono=mono)
        return x + w

    def chip(self, x_right: float, y: float, label: str, fg: str, bg: str,
             *, size: int = 11, pad: float = 9, height: float = 20,
             mono: bool = False, weight: int = 700) -> float:
        """A pill anchored on its right edge; returns its left edge."""
        kind = ("mono" if mono else "cjk") + "_bold"
        w = measure_svg(label, size, kind) + pad * 2
        x = x_right - w
        self.rect(x, y, w, height, fill=bg, rx=height / 2)
        self.text(x + pad, y + height / 2 + size * 0.34, label, size, fg,
                  weight=weight, mono=mono)
        return x

    def svg(self, w: int, h: int, label: str) -> str:
        from html import escape
        head = ('<?xml version="1.0" encoding="UTF-8"?>\n'
                f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" '
                f'height="{h}" viewBox="0 0 {w} {h}" role="img" '
                f'aria-label="{escape(label)}">')
        return "\n".join([head, *self.parts, "</svg>"]) + "\n"


def flow_svg(skin: str) -> str:
    s = FLOW[skin]
    W, H = 1100, 660
    v = Svg()

    v.add("<defs>")
    v.add(f'<linearGradient id="bg" x1="0" y1="0" x2="0.35" y2="1">'
          f'<stop offset="0" stop-color="{s["bg_from"]}"/>'
          f'<stop offset="1" stop-color="{s["bg_to"]}"/></linearGradient>')
    v.add(f'<radialGradient id="glow" cx="0.5" cy="0.5" r="0.5">'
          f'<stop offset="0" stop-color="{s["accent"]}" stop-opacity="{s["glow"]}"/>'
          f'<stop offset="1" stop-color="{s["accent"]}" stop-opacity="0"/>'
          f'</radialGradient>')
    v.add(f'<filter id="soft" x="-30%" y="-30%" width="160%" height="170%">'
          f'<feDropShadow dx="0" dy="7" stdDeviation="9" '
          f'flood-color="#16122c" flood-opacity="{s["shadow"]}"/></filter>')
    v.add('<marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" '
          'markerWidth="6.4" markerHeight="6.4" orient="auto-start-reverse">'
          f'<path d="M0 0 L10 5 L0 10 z" fill="{s["accent"]}"/></marker>')
    v.add('<marker id="arr2" viewBox="0 0 10 10" refX="9" refY="5" '
          'markerWidth="6.4" markerHeight="6.4" orient="auto-start-reverse">'
          f'<path d="M0 0 L10 5 L0 10 z" fill="{s["mark"]}"/></marker>')
    v.add("</defs>")
    v.add(f'<rect width="{W}" height="{H}" fill="url(#bg)"/>')
    v.add(f'<ellipse cx="990" cy="26" rx="380" ry="230" fill="url(#glow)"/>')

    # ---- header -------------------------------------------------------------
    v.text(44, 58, "dsh-railway-window", 28, s["text"], weight=700, mono=True,
           max_w=620)
    v.mixed(44, 86, [("railway_window", True),
                     (" 读一份天窗台账：七条规则只看台账自身，差异回到行号与栏名，"
                      "跑不了的逐条说明。", False)],
            15, s["sub"], max_w=790)
    v.chip(1056, 36, "规则包 v2026.1 · 7 条", s["accent"], s["band"],
           size=12, pad=12, height=26)

    # ---- column headings ----------------------------------------------------
    columns = [
        (44, 232, "① 材料入口", "file 或 material"),
        (316, 384, "② 规则包 → 七条检查", "数据与代码分离"),
        (740, 316, "③ 两条通道 → 报告", "空 ≠ 无问题"),
    ]
    for x, w, label, hint in columns:
        v.rect(x, 109, 4, 14, fill=s["accent"], rx=2)
        v.text(x + 10, 123, label, 14, s["text"], weight=700, max_w=w - 110)
        v.text(x + w, 123, hint, 11, s["faint"], anchor="end", max_w=110)

    # ---- A: material gate ---------------------------------------------------
    v.rect(44, 136, 232, 400, fill=s["panel"], rx=20, stroke=s["edge"],
           sw=1.5, shadow=True)

    v.rect(56, 152, 208, 50, fill=s["band"], rx=12, stroke=s["edge"], sw=1.2)
    v.text(68, 172, "file", 13, s["accent"], weight=700, mono=True)
    v.text(68, 191, "绝对路径 · JSON / YAML", 11, s["sub"], max_w=188)

    v.text(160, 214, "或", 11, s["faint"], anchor="middle")

    v.rect(56, 218, 208, 50, fill=s["band"], rx=12, stroke=s["edge"], sw=1.2)
    v.text(68, 238, "material", 13, s["accent"], weight=700, mono=True)
    v.text(68, 257, "内联文本 · JSON / YAML", 11, s["sub"], max_w=188)

    v.line(160, 270, 160, 280, stroke=s["accent"], sw=1.8, marker="arr")

    v.rect(56, 282, 208, 110, fill=s["card"], rx=12, stroke=s["accent"], sw=1.4)
    v.mixed(68, 302, [("读取层 ", False), ("parseMaterial", True)], 13,
            s["text"], max_w=190)
    v.text(68, 324, "至少携带一项，否则报错：", 11, s["sub"], max_w=190)
    v.text(68, 342, "windowNo · startAt", 11, s["text"], mono=True, max_w=190)
    v.text(68, 358, "endAt · workContent", 11, s["text"], mono=True, max_w=190)
    v.text(68, 378, "列名归一，保留原栏名", 11, s["faint"], max_w=190)

    v.rect(56, 400, 208, 48, fill=s["mark_bg"], rx=12, stroke=s["mark"],
           sw=1.4, dash="6 4")
    v.text(68, 418, "缺这四项 → 直接报错，", 11, s["mark"], max_w=190)
    v.text(68, 436, "不产出空报告", 11, s["mark"], weight=700, max_w=190)

    v.text(56, 466, "材料 = 表头 + 每条天窗一行", 11, s["faint"], max_w=212)
    v.text(56, 484, "读一层只归一，不改原件", 11, s["faint"], max_w=212)
    v.text(56, 502, "表头 date · bureau 也读", 11, s["faint"], max_w=212)

    # ---- B: rule pack + seven checks ---------------------------------------
    v.rect(316, 136, 384, 400, fill=s["panel"], rx=20, stroke=s["edge"],
           sw=1.5, shadow=True)
    v.rect(328, 150, 360, 60, fill=s["band"], rx=12)
    v.text(342, 168, "规则包加载期校验：不通过就整体失败", 13, s["accent"],
           weight=700, max_w=332)
    v.text(342, 186, "依据封顶：原则推导 ≤ warn · 本机构 ≤ info", 11,
           s["sub"], max_w=332)
    v.text(342, 202, "excerpt 逐字；取不到就写明，不伪造引文", 11,
           s["faint"], max_w=332)

    for k, (rid, sev, title, kind, rest, skips) in enumerate(RULES):
        ry = 218 + k * 40
        if k % 2 == 0:
            v.rect(328, ry, 360, 40, fill=s["band_alt"])
        if k < len(RULES) - 1:
            v.line(328, ry + 40, 688, ry + 40, stroke=s["rule"], sw=1)
        v.text(334, ry + 17, rid, 13, s["text"], weight=700, mono=True)
        chip_fg = s["accent"] if sev == "warn" else s["sub"]
        right = v.badge(334 + 57, ry + 4, sev, chip_fg, s["band"],
                        size=11, pad=7, height=18, mono=True)
        v.text(right + 9, ry + 17, title, 13, s["text"],
               max_w=688 - right - 12)
        v.mixed(334, ry + 34, [(kind, True), (rest, False)], 11,
                s["mark"] if skips else s["sub"], max_w=354)

    v.text(334, 514, "每条规则只走一条：有差异 → issues[]；", 11, s["sub"],
           max_w=354)
    v.text(334, 530, "跑不了 → skipped[]；跑通无差异 → 不出条目。", 11,
           s["sub"], max_w=354)

    # ---- C: the two channels, report, reviewer ------------------------------
    v.rect(740, 136, 316, 400, fill=s["panel"], rx=20, stroke=s["edge"],
           sw=1.5, shadow=True)

    v.rect(752, 152, 292, 130, fill=s["card"], rx=18, stroke=s["accent"],
           sw=1.6, shadow=True)
    v.text(768, 180, "issues[]", 15, s["accent"], weight=700, mono=True)
    v.chip(1028, 164, "1 条", s["accent"], s["band"], size=11, height=20)
    tag = v.badge(768, 192, "第 1 行", s["accent"], s["band"], size=11,
                  height=20)
    v.badge(tag + 8, 192, "workContent / permitNo", s["sub"], s["band"],
            size=11, height=20, mono=True)
    v.text(768, 242, "都为空 → 应至少填一项", 13, s["text"], max_w=262)
    v.text(768, 260, "每条都带 found · expected · fix", 11, s["faint"],
           max_w=262)
    v.text(768, 274, "定位 = 行号 + 栏名，可自己重算", 11, s["faint"],
           max_w=262)

    v.rect(752, 290, 292, 112, fill=s["card"], rx=18, stroke=s["edge"],
           sw=1.5, shadow=True)
    v.text(768, 318, "skipped[]", 15, s["sub"], weight=700, mono=True)
    v.chip(1028, 302, "1 条", s["sub"], s["band"], size=11, height=20)
    v.mixed(768, 348, [("RW-005", True), (" · values 未配置", False)], 13,
            s["text"], max_w=262)
    v.text(768, 370, "规则 id 与原因一起进报告", 11, s["faint"], max_w=262)
    v.text(768, 390, "空 issues ≠ 没问题；两条一起读", 11, s["accent"],
           max_w=262)

    # merge line between the two channels and the report card
    v.line(752, 415, 820, 415, stroke=s["rule"], sw=1)
    v.line(976, 415, 1044, 415, stroke=s["rule"], sw=1)
    v.text(898, 419, "两条通道 → 同一份报告", 11, s["faint"], anchor="middle",
           max_w=150)

    v.rect(752, 428, 292, 104, fill=s["card"], rx=18, stroke=s["accent2"],
           sw=1.6, shadow=True)
    v.mixed(768, 452, [("报告 · ", False), ("buildView", True)], 13,
            s["text"], max_w=262)
    v.text(768, 474, "summary{error, warn, info}", 11, s["sub"], mono=True,
           max_w=262)
    v.text(768, 488, "issueCount · skippedCount", 11, s["sub"], mono=True,
           max_w=262)
    v.mixed(768, 502, [("checkedAt · rulesetVersion · ", True),
                       ("免责声明", False)], 11, s["faint"], max_w=262)
    v.line(768, 512, 1028, 512, stroke=s["rule"], sw=1)
    v.text(768, 526, "审核人：结论不在报告里", 12, s["accent2"], weight=700,
           max_w=262)

    # ---- connectors ---------------------------------------------------------
    v.line(266, 330, 312, 330, stroke=s["accent"], sw=1.8, marker="arr")
    v.path("M700 292 H718", stroke=s["accent"], sw=1.8)
    v.path("M718 216 V346", stroke=s["accent"], sw=1.8)
    v.line(718, 216, 748, 216, stroke=s["accent"], sw=1.8, marker="arr")
    v.line(718, 346, 748, 346, stroke=s["mark"], sw=1.8, marker="arr2")

    # ---- footer -------------------------------------------------------------
    v.line(44, 556, 1056, 556, stroke=s["rule"], sw=1)
    v.text(44, 580,
           "严重级跟着证据走：原则推导 ≤ warn · 本机构配置 ≤ info；"
           "excerpt 必须逐字，取不到就写明，不伪造引文。",
           12, s["sub"], max_w=1012)
    v.text(44, 606,
           "config：rulesFile · disabledRules · onlyRules · skipNotes · timeoutMs"
           " ｜ 只读材料 · 无网络 · 不调用模型 · 不写回原件",
           11, s["faint"], max_w=1012)

    if v.overflows:
        raise SystemExit("FATAL: SVG label overflow:\n  " +
                         "\n  ".join(v.overflows))
    return v.svg(W, H,
                 "dsh-railway-window 结构图：材料入口（file 或 material，读取层要求 "
                 "windowNo/startAt/endAt/workContent 至少一项）→ 规则包加载期校验后的 "
                 "RW-001..RW-007 → issues[] 与 skipped[] 两条通道汇入报告，结论交给审核人")


def main() -> None:
    os.makedirs(OUT, exist_ok=True)
    for skin in ("light", "dark"):
        for lang in ("zh", "en"):
            hero(lang, skin)
        name = f"dsh-railway-window-flow-v5-{skin}.svg"
        with open(os.path.join(OUT, name), "w", encoding="utf-8",
                  newline="\n") as fh:
            fh.write(flow_svg(skin))
        print(f"wrote {name} (1100×660)")


if __name__ == "__main__":
    main()
