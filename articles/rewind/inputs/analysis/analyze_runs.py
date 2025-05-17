"""
analyze_runs.py

Purpose:
---------
Compares aggregate CSV outputs from two different runs (e.g., generated using two AI models) 
to identify numeric differences in content retention and transformation metrics.

Outputs:
---------
- Delta CSV: Highlights numeric differences in retention metrics between model outputs.
- Merged CSV: Combines both sets of results side-by-side for comparative inspection.
- Summary stats (numeric deltas) to support model comparison.

Limitations (Not Covered):
---------
- Does NOT analyze semantic meaning or content quality.
- Does NOT provide recommendations or interpretive judgments about which model performed better.
- Assumes structural consistency in input CSVs.

License:
---------
MIT License
"""

#!/usr/bin/env python3
"""
analyze_runs.py  – compare BASE and optional HIGH aggregate CSVs.

Usage examples
--------------
# base-only
python analyze_runs.py --base  articles/foo/base_agg.csv

# base + high
python analyze_runs.py --base  articles/foo/base_agg.csv \
                       --high  articles/foo/high_agg.csv \
                       --output-prefix articles/foo/comparison
"""

import argparse
import pandas as pd
import numpy as np

# ---------- helpers --------------------------------------------------
def compute_delta(base_df, high_df):
    """Return numeric deltas (high − base) for all numeric cols."""
    delta = high_df.copy()
    for col in base_df.columns:
        if pd.api.types.is_numeric_dtype(base_df[col]):
            delta[col] = high_df[col] - base_df[col]
    return delta

def stage_aggregate(retention):
    """Draft→Final etc.  Return % retained per stage."""
    contrib = {
        'Draft→Final':   np.prod([ retention[('Draft','Refined')],
                                   retention[('Refined','Edited')],
                                   retention[('Edited','Final')] ]),
        'Refined→Final': retention[('Refined','Edited')] *
                          retention[('Edited','Final')],
        'Edited→Final':  retention[('Edited','Final')]
    }
    df = (
        pd.DataFrame.from_dict(contrib, orient='index',
                               columns=['Stage Aggregate Retention (%)'])
          .mul(100).round(2)
          .reset_index()
          .rename(columns={'index':'Transition'})
    )
    return df

def compute_retention(retention, metrics):
    """Cumulative % each version’s words survive to Final."""
    steps = ['Draft', 'Refined', 'Edited', 'Final']
    cumulative = {
        'Draft→Final'  : retention[(steps[0], steps[1])]
                       * retention[(steps[1], steps[2])]
                       * retention[(steps[2], steps[3])] * 100,
        'Refined→Final': retention[(steps[1], steps[2])]
                       * retention[(steps[2], steps[3])] * 100,
        'Edited→Final' : retention[(steps[2], steps[3])] * 100,
    }
    return pd.DataFrame.from_dict(
        cumulative, orient='index', columns=metrics
    ).round(4)

def merge_stage_and_retention(stage_df, retention_df):
    ret = retention_df.reset_index().rename(columns={'index':'Transition'})
    merged = pd.merge(stage_df, ret, on='Transition', how='inner')
    return merged.rename(columns={'Transition':'Comparison'})

# ---------- main -----------------------------------------------------
def parse_args():
    p = argparse.ArgumentParser(
        description="Compare base and (optional) high model outputs"
    )
    p.add_argument("--base",  required=True,  help="Path to base_agg.csv")
    p.add_argument("--high",  required=False, help="Path to high_agg.csv")
    p.add_argument("--output-prefix", default="comparison",
                   help="Prefix (and path) for output files")
    return p.parse_args()

def main():
    args = parse_args()

    # --- load BASE ---
    base_df = pd.read_csv(args.base)

    # If HIGH supplied, run full comparison
    if args.high:
        print("High file supplied – running delta comparison")
        high_df = pd.read_csv(args.high)

        # 1. delta CSV
        delta = compute_delta(base_df, high_df)
        delta.to_csv(f"{args.output_prefix}_delta.csv", index=False)
        print(f"Wrote delta CSV: {args.output_prefix}_delta.csv")

        # 2. retention metrics (built from high_df)
        metrics_cols = [c for c in high_df.columns if c.endswith('Retention (%)')]
        retention = {
            (row['Previous Version'], row['Current Version']): row[metrics_cols].values/100.0
            for _, row in high_df.iterrows()
        }

    else:
        print("No --high supplied – skipping delta comparison")
        # Build retention dict from *base* so downstream code still works
        metrics_cols = [c for c in base_df.columns if c.endswith('Retention (%)')]
        retention = {
            (row['Previous Version'], row['Current Version']): row[metrics_cols].values/100.0
            for _, row in base_df.iterrows()
        }

    # 3. stage aggregates & cumulative retention
    stage_df     = stage_aggregate(retention)
    retention_df = compute_retention(retention, metrics_cols)

    # 4. final-% breakdown
    word_ret = retention_df['Word Retention (%)']
    R_df, R_rf, R_ed = word_ret.loc[['Draft→Final','Refined→Final','Edited→Final']]
    final_pct_df = pd.Series({
        'Draft→Final':   R_df,
        'Refined→Final': R_rf - R_df,
        'Edited→Final':  R_ed - R_rf,
    }, name='Final %').reset_index().rename(columns={'index':'Comparison'})

    # 5. merge & write aggregate CSV
    merged = merge_stage_and_retention(stage_df, retention_df).merge(final_pct_df)
    merged.to_csv(f"{args.output_prefix}_agg.csv", index=False)
    print(f"Wrote merged CSV: {args.output_prefix}_agg.csv")

if __name__ == "__main__":
    main()