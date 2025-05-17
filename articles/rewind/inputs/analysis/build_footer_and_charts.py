#!/usr/bin/env python3
"""
build_footer_and_charts.py
———————————————
Create article footer + Matplotlib charts from metrics CSV.

Usage (run inside article folder):
    python ../../resources/build_footer_and_charts.py \
        --metrics base_agg.csv \
        --out footer.md
"""

import argparse
import json
import textwrap
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

# ── 1  CLI  ──────────────────────────────────────────────────────────
ap = argparse.ArgumentParser()
ap.add_argument("--metrics", required=True, help="Path to metrics CSV (base_agg.csv)")
ap.add_argument("--out", default="footer.md", help="Markdown footer to write")
args = ap.parse_args()
folder = Path(args.metrics).parent

# ── 2  Read data  ─────────────────────────────────────────────────────
df = pd.read_csv(args.metrics)

# ── 3  JSON spec (inline for now)  ────────────────────────────────────
chart_spec_json = rchart_spec_json = r"""
{
  "chart_instructions": [
    {
      "name": "word_vs_sentence_retention",
      "type": "grouped_bar",
      "library": "matplotlib",
      "data_fields": {
        "x": "Current Version",
        "series": [
          { "y": "Word Retention (%)",      "label": "Word Retention (%)" },
          { "y": "Sentence Retention (%)",  "label": "Sentence Retention (%)" }
        ]
      },
      "layout": {
        "figsize": [8, 5],
        "dpi": 100,
        "title": "Word vs. Sentence Retention by Current Version",
        "x_axis": { "field": "Current Version", "type": "category", "label": "Current Version", "rotation": 0 },
        "y_axis": { "label": "Retention (%)", "limit": [0, 100] },
        "legend": { "loc": "upper right" },
        "grid": { "which": "major", "linestyle": "--", "alpha": 0.3 }
      },
      "style": {
        "bar_width": 0.35,
        "colors": {
          "Word Retention (%)": "#1f77b4",
          "Sentence Retention (%)": "#ff7f0e"
        }
      }
    },
    {
      "name": "char_vs_paragraph_retention",
      "type": "grouped_bar",
      "library": "matplotlib",
      "data_fields": {
        "x": "Current Version",
        "series": [
          { "y": "Char Retention (%)",       "label": "Char Retention (%)" },
          { "y": "Paragraph Retention (%)",  "label": "Paragraph Retention (%)" }
        ]
      },
      "layout": {
        "figsize": [8, 5],
        "dpi": 100,
        "title": "Character vs. Paragraph Retention by Current Version",
        "x_axis": { "field": "Current Version", "type": "category", "label": "Current Version", "rotation": 0 },
        "y_axis": { "label": "Retention (%)", "limit": [0, 100] },
        "legend": { "loc": "upper right" },
        "grid": { "which": "major", "linestyle": "--", "alpha": 0.3 }
      },
      "style": {
        "bar_width": 0.35,
        "colors": {
          "Char Retention (%)":      "#9467bd",
          "Paragraph Retention (%)": "#2ca02c"
        }
      }
    },
    {
      "name": "retention_breakdown",
      "type": "stacked_bar_with_lines",
      "library": "matplotlib",
      "data_fields": {
        "x": "Current Version",
        "stacked_bars": [
          { "y": "Word Retention (%)",      "label": "Word Retention (%)" },
          { "y": "Sentence Retention (%)",  "label": "Sentence Retention (%)" },
          { "y": "Paragraph Retention (%)", "label": "Paragraph Retention (%)" }
        ],
        "lines": []
      },
      "layout": {
        "figsize": [8, 5],
        "dpi": 100,
        "title": "Retention Breakdown by Current Version",
        "x_axis": { "field": "Current Version", "type": "category", "label": "Current Version", "rotation": 0 },
        "y_axis_left":  { "label": "Retention (%)", "limit": [0, 100] },
        "y_axis_right": { "label": "—",           "limit": [0, 100] },
        "legend": { "loc": "upper right" },
        "grid": { "which": "major", "linestyle": "--", "alpha": 0.3 }
      },
      "style": {
        "bar_width": 0.6,
        "marker": "o",
        "colors": {
          "Word Retention (%)":      "#1f77b4",
          "Sentence Retention (%)":  "#ff7f0e",
          "Paragraph Retention (%)": "#2ca02c"
        }
      }
    }
  ]
}

"""
SPEC = json.loads(chart_spec_json)["chart_instructions"]

# ── 4  Helper functions  ──────────────────────────────────────────────
def stacked_bar_with_lines(ax, data, spec):
    # Bars
    x = data[spec["data_fields"]["x"]]
    bar_width = spec["style"]["bar_width"]
    bottoms = pd.Series([0] * len(data))
    for stack in spec["data_fields"]["stacked_bars"]:
        y = data[stack["y"]]
        ax.bar(
            x,
            y,
            bar_width,
            bottom=bottoms,
            label=stack["label"],
            color=spec["style"]["colors"][stack["label"]],
        )
        bottoms += y
    # Lines (second y-axis)
    ax2 = ax.twinx()
    for line in spec["data_fields"]["lines"]:
        ax2.plot(
            x,
            data[line["y"]],
            marker=spec["style"]["marker"],
            label=line["label"],
            color=spec["style"]["colors"][line["label"]],
        )
    # Axis limits & labels
    ax.set_ylim(*spec["layout"]["y_axis_left"]["limit"])
    ax2.set_ylim(*spec["layout"]["y_axis_right"]["limit"])
    ax.set_ylabel(spec["layout"]["y_axis_left"]["label"])
    ax2.set_ylabel(spec["layout"]["y_axis_right"]["label"])
    # Legends
    h1, l1 = ax.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax2.legend(h1 + h2, l1 + l2, loc=spec["layout"]["legend"]["loc"])
    return ax, ax2


def grouped_bar(ax, data, spec):
    x = data[spec["data_fields"]["x"]]
    bar_width = spec["style"]["bar_width"]
    indices = range(len(x))
    for i, series in enumerate(spec["data_fields"]["series"]):
        offset = (i - 0.5) * bar_width
        ax.bar(
            [idx + offset for idx in indices],
            data[series["y"]],
            bar_width,
            label=series["label"],
            color=spec["style"]["colors"][series["label"]],
        )
    ax.set_xticks(indices)
    ax.set_xticklabels(x, rotation=spec["layout"]["x_axis"]["rotation"])
    ax.set_ylabel(spec["layout"]["y_axis"]["label"])
    ax.set_ylim(*spec["layout"]["y_axis"]["limit"])
    ax.legend(loc=spec["layout"]["legend"]["loc"])
    return ax


# ── 5  Generate charts  ───────────────────────────────────────────────
out_images = []
for instr in SPEC:
    fig = plt.figure(figsize=instr["layout"]["figsize"], dpi=instr["layout"]["dpi"])
    ax = fig.add_subplot(111)
    if instr["type"] == "grouped_bar":
        grouped_bar(ax, df, instr)
    elif instr["type"] == "stacked_bar_with_lines":
        stacked_bar_with_lines(ax, df, instr)
    else:
        raise ValueError(f"Unknown chart type: {instr['type']}")
    ax.set_title(instr["layout"]["title"])
    ax.grid(**instr["layout"]["grid"])
    filename = folder / f"{instr['name']}.png"
    plt.tight_layout()
    plt.savefig(filename, transparent=False)
    plt.close(fig)
    out_images.append(filename.name)
    print("✓ Saved", filename)

# ── 6  Build footer text  ─────────────────────────────────────────────
if "content_stats.retention.pct_words_retained" in df.columns:
    overall_ret = df["content_stats.retention.pct_words_retained"].mean()
elif "Word Retention (%)" in df.columns:
    overall_ret = df["Word Retention (%)"].mean()
else:
    # last-resort default so the script never crashes
    overall_ret = 0.0
footer_md = textwrap.dedent(
    f"""
    > _AI Use & Methodology_  
    > Drafted with Claude 3.7 Sonnet → human-edited in Type.ai.  
    > **{overall_ret:.0f}%** of the original draft’s words were retained after AI iterations.  
    > Full details in [AI Use Policy](/ai-use.md)  

    **Charts:** `ai_assisted_rewrites_and_revision_depth.png`, `draft_vs_ai_word_counts.png`, `authorship_proportions_with_retention.png`
    """
).strip()

with open(folder / args.out, "w") as f:
    f.write(footer_md)

print("✓ Wrote footer", args.out)