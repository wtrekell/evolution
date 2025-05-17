"""
generate_runs.py

Purpose:
---------
Analyzes four content stages (Draft → Refined → Edited → Final) to compute retention metrics 
across character and word levels. Designed to assess how much content persists across each 
transformation stage.

Outputs:
---------
- Per-run CSVs showing character and word-level retention from:
  - Draft → Refined
  - Refined → Edited
  - Edited → Final
  - Each version → Final
- Aggregated metrics across multiple runs if specified.
- Summary outputs with overall content retention statistics.

Limitations (Not Covered):
---------
- Does NOT perform semantic or stylistic analysis.
- Does NOT assess narrative quality, factual consistency, or tone shifts.
- Does NOT differentiate between high-quality vs. low-quality edits.
- No qualitative interpretation of content changes.

License:
---------
MIT License
"""

#!/usr/bin/env python3
"""
generate_runs.py: Multi-run analysis for content retention metrics.
Generates run-level and aggregated CSVs for Draft→Refined, Refined→Edited, Edited→Final, plus version-to-Final comparisons.
Usage:
  python generate_runs.py \
    --draft /mnt/data/draft-markup-guide.md \
    --refined /mnt/data/refined-markup-guide.md \
    --edited /mnt/data/edited-markup-guide.md \
    --final /mnt/data/final-markup-guide.md \
    --output-prefix /mnt/data/base
    [--runs 3]
"""
import difflib
import re
import random
import pandas as pd
import argparse

# --- Retention functions ---
def compute_char_retention(prev_text: str, curr_text: str) -> float:
    matcher = difflib.SequenceMatcher(None, prev_text, curr_text)
    return matcher.ratio() * 100

def compute_word_retention(prev_text: str, curr_text: str) -> float:
    prev_words = set(re.findall(r"\w+", prev_text.lower()))
    curr_words = set(re.findall(r"\w+", curr_text.lower()))
    return len(prev_words & curr_words) / len(prev_words) * 100 if prev_words else 0.0

def split_sentences(text: str) -> list:
    return [s.strip() for s in re.split(r'(?<=[\.!?])\s+', text) if s.strip()]

def compute_sentence_retention(prev_text: str, curr_text: str, threshold: float) -> float:
    prev_sents = split_sentences(prev_text)
    curr_sents = split_sentences(curr_text)
    if not prev_sents:
        return 0.0
    matched = sum(
        1 for sent in prev_sents
        if max((difflib.SequenceMatcher(None, sent, c).ratio() for c in curr_sents), default=0) >= threshold
    )
    return matched / len(prev_sents) * 100

def split_paragraphs(text: str) -> list:
    return [p.strip() for p in re.split(r'\n{2,}', text) if p.strip()]

def compute_paragraph_retention(prev_text: str, curr_text: str, threshold: float) -> float:
    prev_paras = split_paragraphs(prev_text)
    curr_paras = split_paragraphs(curr_text)
    if not prev_paras:
        return 0.0
    matched = sum(
        1 for para in prev_paras
        if max((difflib.SequenceMatcher(None, para, c).ratio() for c in curr_paras), default=0) >= threshold
    )
    return matched / len(prev_paras) * 100

# --- Threshold sampling with minimum separation ---
def sample_thresholds(n: int, low: float, high: float, min_sep: float) -> list:
    """
    Sample `n` values in [low, high] such that each pair is at least `min_sep` apart.
    """
    vals = []
    attempts = 0
    while len(vals) < n:
        if attempts > 1000:
            raise ValueError("Unable to sample thresholds with given separation")
        cand = random.uniform(low, high)
        if all(abs(cand - v) >= min_sep for v in vals):
            vals.append(round(cand, 2))
        attempts += 1
    return vals

# --- Multi-run analysis ---
def multi_run_analysis(paths: dict, n_runs: int = 3,
                       sent_range=(0.70, 0.90), para_range=(0.60, 0.80), min_sep=0.03) -> pd.DataFrame:
    # Load texts
    texts = {name: open(p, 'r', encoding='utf-8').read() for name, p in paths.items()}
    # Sample thresholds
    sent_threshs = sample_thresholds(n_runs, sent_range[0], sent_range[1], min_sep)
    para_threshs = sample_thresholds(n_runs, para_range[0], para_range[1], min_sep)

    comparisons = [
        ('Draft', 'Refined'),
        ('Refined', 'Edited'),
        ('Edited', 'Final'),
        ('Draft', 'Final'),
        ('Refined', 'Final')
    ]

    rows = []
    for run_id, (s_th, p_th) in enumerate(zip(sent_threshs, para_threshs), start=1):
        for prev, curr in comparisons:
            char_ret = compute_char_retention(texts[prev], texts[curr])
            word_ret = compute_word_retention(texts[prev], texts[curr])
            sent_ret = compute_sentence_retention(texts[prev], texts[curr], s_th)
            para_ret = compute_paragraph_retention(texts[prev], texts[curr], p_th)
            rows.append({
                'RunID': run_id,
                'SentenceThreshold': s_th,
                'ParagraphThreshold': p_th,
                'Previous Version': prev,
                'Current Version': curr,
                'Char Retention (%)': round(char_ret, 2),
                'Word Retention (%)': round(word_ret, 2),
                'Sentence Retention (%)': round(sent_ret, 2),
                'Paragraph Retention (%)': round(para_ret, 2)
            })
    return pd.DataFrame(rows)

# --- Main entrypoint ---
def main():
    parser = argparse.ArgumentParser(description="Multi-run retention analysis for content versions.")
    parser.add_argument('--draft', required=True, help="Path to Draft markdown file")
    parser.add_argument('--refined', required=True, help="Path to Refined markdown file")
    parser.add_argument('--edited', required=True, help="Path to Edited markdown file")
    parser.add_argument('--final',   required=True, help="Path to Final markdown file")
    parser.add_argument('--output-prefix', default='base', help="Prefix for output CSV files")
    parser.add_argument('--runs', type=int, default=3, help="Number of randomized runs")
    args = parser.parse_args()

    paths = {
        'Draft': args.draft,
        'Refined': args.refined,
        'Edited': args.edited,
        'Final': args.final
    }
    df_runs = multi_run_analysis(paths, n_runs=args.runs)

    # Write run-level CSV
    run_csv = f"{args.output_prefix}_run_level.csv"
    df_runs.to_csv(run_csv, index=False)
    print(f"Wrote run-level CSV: {run_csv}")

    # Aggregate and write aggregated CSV
    df_agg = df_runs.groupby(['Previous Version','Current Version']).mean().reset_index()
    agg_csv = f"{args.output_prefix}_agg.csv"
    df_agg.to_csv(agg_csv, index=False)
    print(f"Wrote aggregated CSV: {agg_csv}")

if __name__ == '__main__':
    main()
