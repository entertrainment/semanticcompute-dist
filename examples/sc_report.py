"""
sc_report — turn SemanticCompute parity results into a self-contained HTML verification report.

A *pure renderer*: it takes the JSON the `semanticcompute-parity --json` CLI emits (or the MCP server's
structured output) and returns a standalone HTML string — no subprocess, no network, no third-party deps, and
no SemanticCompute source needed. The result is a shareable audit artifact: open it in any browser, attach it
to a compliance record, hand it to a reviewer. It renders in light and dark.

The input `data` for each case is the parsed `--json` object, e.g.:
    {"compared": 24, "compatible": false, "diverged": 3, "maxAbsoluteError": 0.8,
     "tolerance": "ulp(1)", "mismatches": [{"index": 7, "cause": "signFlip",
     "ulpDistance": 2151677952, "reference": "2.5", "candidate": "-2.5", "explanation": "..."}]}

Usage
-----
    from sc_report import write_html
    write_html("report.html", "softmax kernel", [
        {"label": "v1 — naive (generated)", "data": v1_json},
        {"label": "v2 — max-shift fix",     "data": v2_json},
    ])

Each element is coloured by its *cause*; the authoritative pass/fail (compatible + diverged count + tolerance)
comes straight from the CLI, never re-derived here. Buffers larger than `max_cells` fall back to a cause
histogram + a top-N mismatch table instead of a per-element grid.
"""

from __future__ import annotations

import html
from typing import Any

# cause -> (label, chip fill, chip text, chip border). Light fills + dark text read on either page background;
# unknown causes fall back to neutral grey. Ordering here is the legend/histogram order.
_CAUSE = {
    "ulpDrift": ("ULP drift", "#FAEEDA", "#412402", "#BA7517"),
    "denormalFlush": ("denormal flush", "#E6F1FB", "#042C53", "#185FA5"),
    "signedZero": ("signed zero", "#EEEDFE", "#26215C", "#534AB7"),
    "signFlip": ("sign flip", "#FCEBEB", "#501313", "#A32D2D"),
    "numericDivergence": ("numeric divergence", "#FAECE7", "#4A1B0C", "#993C1D"),
    "nanGeneration": ("NaN generation", "#FCEBEB", "#501313", "#A32D2D"),
    "overflowToPositiveInfinity": ("overflow +∞", "#FBEAF0", "#4B1528", "#993556"),
    "overflowToNegativeInfinity": ("overflow −∞", "#FBEAF0", "#4B1528", "#993556"),
    "infinitySignFlip": ("∞ sign flip", "#FBEAF0", "#4B1528", "#993556"),
    "infinityCollapse": ("∞ collapse", "#FBEAF0", "#4B1528", "#993556"),
}
_FALLBACK = ("divergence", "#F1EFE8", "#2C2C2A", "#B4B2A9")


def _meta(cause: str):
    return _CAUSE.get(cause, _FALLBACK)


def _ulp_label(m: dict) -> str:
    u = m.get("ulpDistance")
    cause = m.get("cause", "")
    if cause == "signFlip":
        return "sign"
    if cause == "denormalFlush":
        return "denorm"
    if cause in ("nanGeneration",):
        return "NaN"
    if u is None:
        return ""
    return f"{u:,} ULP" if u < 100000 else "≫ ULP"


def _tiles(d: dict) -> str:
    compared = d.get("compared", 0)
    mismatches = d.get("mismatches", []) or []
    diverged = d.get("diverged", len(mismatches))
    tol = d.get("tolerance", "—")
    max_abs = d.get("maxAbsoluteError")
    ok = bool(d.get("compatible"))
    max_abs_s = "0" if not max_abs else (f"{max_abs:.3g}")
    cells = [
        ("compared", str(compared), None),
        ("differ from ref", str(len(mismatches)), None),
        ("fail " + str(tol), str(diverged), "danger" if diverged else None),
        ("max abs error", max_abs_s, None),
    ]
    out = ['<div class="tiles">']
    for label, value, tone in cells:
        cls = "tile" + (" danger" if tone == "danger" else "")
        out.append(f'<div class="{cls}"><div class="tl">{html.escape(label)}</div>'
                   f'<div class="tv">{html.escape(value)}</div></div>')
    out.append("</div>")
    return "".join(out)


def _is_truncated(d: dict) -> bool:
    # Every failing element is also a listed mismatch, so fewer mismatches than `diverged` proves the list was
    # capped (CLI --limit). Painting the unlisted remainder as "agree" would hide real divergences — refuse to.
    return len(d.get("mismatches", []) or []) < d.get("diverged", 0)


def _cell_map(d: dict, max_cells: int) -> str:
    compared = d.get("compared", 0)
    mismatches = {m["index"]: m for m in (d.get("mismatches", []) or []) if "index" in m}
    if _is_truncated(d):
        return (f'<p class="note">Per-element grid omitted — the diagnosis list is truncated '
                f'({len(mismatches)} of {d.get("diverged", 0):,} diverged elements returned). Re-run the check '
                f'with a higher limit for the full map; the cause summary and top mismatches are below.</p>')
    if compared > max_cells:
        return (f'<p class="note">{compared:,} elements — too many for a per-element grid; '
                f'see the cause summary and the top mismatches below.</p>')
    out = ['<div class="grid">']
    for i in range(compared):
        m = mismatches.get(i)
        if m is None:
            out.append(f'<div class="cell agree"><span class="ci">{i}</span></div>')
        else:
            label, fill, text, border = _meta(m.get("cause", ""))
            cap = _ulp_label(m)
            title = f'index {i} — {label}'
            cap_html = f'<span class="cc">{html.escape(cap)}</span>' if cap else ""
            out.append(
                f'<div class="cell" title="{html.escape(title)}" '
                f'style="background:{fill};color:{text};border:1.5px solid {border}">'
                f'<span class="ci">{i}</span>{cap_html}</div>')
    out.append("</div>")
    return "".join(out)


def _legend(d: dict) -> str:
    counts: dict[str, int] = {}
    for m in (d.get("mismatches", []) or []):
        c = m.get("cause", "")
        counts[c] = counts.get(c, 0) + 1
    if not counts:
        return '<p class="note">No element diverged from the reference.</p>'
    ordered = [c for c in _CAUSE if c in counts] + [c for c in counts if c not in _CAUSE]
    out = ['<div class="legend">']
    for c in ordered:
        label, fill, text, border = _meta(c)
        out.append(f'<span class="lg"><span class="sw" style="background:{fill};border:1px solid {border}">'
                   f'</span>{html.escape(label)} · {counts[c]}</span>')
    out.append("</div>")
    return "".join(out)


def _mismatch_table(d: dict, top: int = 30) -> str:
    ms = d.get("mismatches", []) or []
    if not ms:
        return ""
    rows = ms[:top]
    out = ['<table class="mm"><thead><tr><th>idx</th><th>reference</th><th>candidate</th>'
           '<th>ULP</th><th>cause</th></tr></thead><tbody>']
    for m in rows:
        u = m.get("ulpDistance")
        us = "—" if u is None else (f"{u:,}")
        label = _meta(m.get("cause", ""))[0]
        out.append(
            f'<tr><td>{html.escape(str(m.get("index","")))}</td>'
            f'<td class="num">{html.escape(str(m.get("reference","")))}</td>'
            f'<td class="num">{html.escape(str(m.get("candidate","")))}</td>'
            f'<td class="num">{html.escape(us)}</td>'
            f'<td>{html.escape(label)}</td></tr>')
    out.append("</tbody></table>")
    if len(ms) > top:
        out.append(f'<p class="note">… and {len(ms) - top:,} more.</p>')
    return "".join(out)


def _case_section(case: dict, max_cells: int) -> str:
    d = case["data"]
    label = case.get("label", "case")
    tol = d.get("tolerance", "")
    ok = bool(d.get("compatible"))
    pill = ('<span class="pill ok">✓ verified</span>' if ok
            else '<span class="pill bad">✗ diverged</span>')
    sub = f'under {html.escape(str(tol))}' if tol else ""
    return (f'<section class="case"><div class="chead"><h2>{html.escape(label)}</h2>{pill}'
            f'<span class="sub">{sub}</span></div>'
            f'{_tiles(d)}{_cell_map(d, max_cells)}{_legend(d)}{_mismatch_table(d)}</section>')


_STYLE = """
:root{--bg:#fbfbf9;--fg:#1a1a19;--muted:#6b6a66;--card:#f6f5f1;--cell:#efeee8;
--celltext:#8a8880;--cborder:#e2e0d9;--danger:#a32d2d}
@media (prefers-color-scheme:dark){:root{--bg:#191817;--fg:#ececec;--muted:#a3a29a;
--card:#232320;--cell:#2a2a27;--celltext:#78766f;--cborder:#33322e;--danger:#e24b4a}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);
font:15px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
padding:2rem 1.25rem}
main{max-width:860px;margin:0 auto}
h1{font-size:22px;font-weight:600;margin:0 0 .25rem}
h2{font-size:17px;font-weight:600;margin:0}
.lead{color:var(--muted);margin:.25rem 0 1.75rem}
.case{border-top:1px solid var(--cborder);padding-top:1.5rem;margin-top:1.75rem}
.chead{display:flex;align-items:center;gap:12px;flex-wrap:wrap;margin-bottom:1rem}
.sub{color:var(--muted);font-size:13px}
.pill{font-size:12px;font-weight:600;padding:3px 10px;border-radius:20px}
.pill.ok{background:#E1F5EE;color:#04342C}.pill.bad{background:#FCEBEB;color:#501313}
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:10px;margin-bottom:1.25rem}
.tile{background:var(--card);border-radius:8px;padding:.7rem .9rem}
.tl{font-size:12px;color:var(--muted)}.tv{font-size:22px;font-weight:600}
.tile.danger .tv{color:var(--danger)}
.grid{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:1rem}
.cell{width:46px;min-height:46px;display:flex;flex-direction:column;align-items:center;justify-content:center;
gap:2px;border-radius:7px;background:var(--cell);color:var(--celltext);border:1px solid var(--cborder)}
.ci{font-size:11px;font-weight:600}.cc{font-size:10px;line-height:1.1;text-align:center;padding:0 2px}
.cell.agree{background:var(--cell);color:var(--celltext);border:1px solid var(--cborder)}
.legend{display:flex;flex-wrap:wrap;gap:14px;font-size:12px;color:var(--muted);margin-bottom:1rem}
.lg{display:flex;align-items:center;gap:6px}
.sw{width:12px;height:12px;border-radius:3px;display:inline-block}
.mm{width:100%;border-collapse:collapse;font-size:12px;margin-top:.5rem}
.mm th{text-align:left;color:var(--muted);font-weight:500;border-bottom:1px solid var(--cborder);padding:5px 8px}
.mm td{border-bottom:1px solid var(--cborder);padding:5px 8px}
.mm .num{font-variant-numeric:tabular-nums;font-family:ui-monospace,Menlo,monospace}
.note{color:var(--muted);font-size:12px;margin:.25rem 0 1rem}
footer{margin-top:2.5rem;border-top:1px solid var(--cborder);padding-top:1rem;color:var(--muted);font-size:12px}
"""


def render_html(title: str, cases: list[dict], *, subtitle: str | None = None, max_cells: int = 256) -> str:
    """Return a complete, self-contained HTML document for one or more verification `cases`."""
    lead = subtitle or ("SemanticCompute compared each candidate against a trusted reference and classified "
                        "every divergence by cause. Provenance-agnostic — the candidate's origin is irrelevant.")
    body = "".join(_case_section(c, max_cells) for c in cases)
    return (
        "<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\">"
        "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">"
        f"<title>{html.escape(title)} — SemanticCompute verification</title>"
        f"<style>{_STYLE}</style></head><body><main>"
        f"<h1>{html.escape(title)}</h1><p class=\"lead\">{html.escape(lead)}</p>"
        f"{body}"
        "<footer>Generated by SemanticCompute — numerical verification for heterogeneous compute. "
        "Cause inference is a heuristic (leads to confirm, not proofs); the pass/fail verdict and tolerance "
        "are authoritative.</footer>"
        "</main></body></html>")


def write_html(path: str, title: str, cases: list[dict], *, subtitle: str | None = None,
               max_cells: int = 256) -> str:
    """Render and write the report to `path`; return the path written."""
    with open(path, "w", encoding="utf-8") as f:
        f.write(render_html(title, cases, subtitle=subtitle, max_cells=max_cells))
    return path


if __name__ == "__main__":
    # Self-test with a fabricated case (no CLI needed): a mixed-cause diverged buffer -> report.html.
    demo = {
        "compared": 12, "compatible": False, "diverged": 3, "maxAbsoluteError": 0.8, "tolerance": "ulp(1)",
        "mismatches": [
            {"index": 3, "cause": "ulpDrift", "ulpDistance": 1, "reference": "0.7548123", "candidate": "0.75481236"},
            {"index": 5, "cause": "signFlip", "ulpDistance": 2151677952, "reference": "2.5", "candidate": "-2.5"},
            {"index": 8, "cause": "numericDivergence", "ulpDistance": 13422, "reference": "0.5", "candidate": "0.5008"},
        ],
    }
    p = write_html("report.html", "self-test", [{"label": "demo buffer", "data": demo}])
    print(f"wrote {p}")
