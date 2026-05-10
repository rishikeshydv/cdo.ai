import pandas as pd
import numpy as np
from pathlib import Path
from scipy import stats

PAIRWISE_FOLDER = "./pairwise_csvs"
H4_FOLDER = "./h4_csvs"

DISTINCTNESS_THRESHOLD = 7

def load_csv_folder(folder_path):
    folder = Path(folder_path)

    csv_files = list(folder.glob("*.csv"))

    if len(csv_files) == 0:
        raise ValueError(f"No CSV files found in: {folder_path}")

    dfs = []

    for file in csv_files:
        print(f"Loading: {file.name}")
        df = pd.read_csv(file)
        dfs.append(df)

    return pd.concat(dfs, ignore_index=True)

pairwise_df = load_csv_folder(PAIRWISE_FOLDER)
h4_df = load_csv_folder(H4_FOLDER)

print("\n==================================================")
print("DATASET SUMMARY")
print("==================================================")

print(f"Pairwise rows: {len(pairwise_df)}")
print(f"H4 rows: {len(h4_df)}")


print("\n==================================================")
print("H1 — Preference Outcomes")
print("==================================================")

comparison_groups = pairwise_df.groupby("comparison_type")

h1_results = []

for comparison_name, group in comparison_groups:

    wins = (group["preferred_output"] == "A").sum()
    ties = (group["preferred_output"] == "Tie").sum()
    losses = (group["preferred_output"] == "B").sum()

    total = len(group)

    preference_rate = wins / total * 100

    # confidence interval
    ci_low, ci_high = stats.binomtest(
        wins,
        total
    ).proportion_ci(confidence_level=0.95)

    h1_results.append({
        "Comparison": comparison_name,
        "Wins": wins,
        "Ties": ties,
        "Losses": losses,
        "Preference Rate (%)": round(preference_rate, 2),
        "95% CI Low": round(ci_low * 100, 2),
        "95% CI High": round(ci_high * 100, 2)
    })

h1_df = pd.DataFrame(h1_results)

print(h1_df)


print("\n==================================================")
print("H2 — Business Alignment")
print("==================================================")

business_wins = (
    pairwise_df["business_alignment_A"]
    >
    pairwise_df["business_alignment_B"]
).sum()

business_total = len(pairwise_df)

business_rate = business_wins / business_total * 100

mean_a = pairwise_df["business_alignment_A"].mean()
mean_b = pairwise_df["business_alignment_B"].mean()

print(f"Business Alignment Win Rate: {business_rate:.2f}%")
print(f"Mean Alignment A: {mean_a:.2f}")
print(f"Mean Alignment B: {mean_b:.2f}")


print("\n==================================================")
print("H3 — Distinctness")
print("==================================================")

distinct_pass = (
    pairwise_df["distinctness_A"]
    >= DISTINCTNESS_THRESHOLD
).sum()

distinct_total = len(pairwise_df)

distinct_rate = distinct_pass / distinct_total * 100

distinct_mean = pairwise_df["distinctness_A"].mean()

print(f"Distinctness Threshold: {DISTINCTNESS_THRESHOLD}")
print(f"Pass Rate: {distinct_rate:.2f}%")
print(f"Mean Distinctness: {distinct_mean:.2f}")


print("\n==================================================")
print("H4 — Confidence & Collaboration")
print("==================================================")

h4_df["combined_on"] = (
    h4_df["confidence_rationale_on"]
    +
    h4_df["collaboration_rationale_on"]
) / 2

h4_df["combined_off"] = (
    h4_df["confidence_rationale_off"]
    +
    h4_df["collaboration_rationale_off"]
) / 2

mean_on = h4_df["combined_on"].mean()
mean_off = h4_df["combined_off"].mean()

relative_improvement = (
    (mean_on - mean_off)
    / mean_off
) * 100

paired_t = stats.ttest_rel(
    h4_df["combined_on"],
    h4_df["combined_off"]
)

print(f"Mean ON: {mean_on:.2f}")
print(f"Mean OFF: {mean_off:.2f}")
print(f"Relative Improvement: {relative_improvement:.2f}%")

print(f"T-statistic: {paired_t.statistic:.4f}")
print(f"P-value: {paired_t.pvalue:.6f}")


print("\n==================================================")
print("H5 — Time to Acceptable Output")
print("==================================================")

mean_time_a = pairwise_df[
    "time_to_acceptable_A_min"
].mean()

mean_time_b = pairwise_df[
    "time_to_acceptable_B_min"
].mean()

time_reduction = (
    (mean_time_b - mean_time_a)
    / mean_time_b
) * 100

print(f"Mean Time A: {mean_time_a:.2f} min")
print(f"Mean Time B: {mean_time_b:.2f} min")
print(f"Reduction: {time_reduction:.2f}%")


print("\n==================================================")
print("EXPORTING RESULTS")
print("==================================================")

h1_df.to_csv("h1_results.csv", index=False)

summary = pd.DataFrame([
    {
        "H2 Business Alignment Win Rate": round(business_rate, 2),
        "H3 Distinctness Pass Rate": round(distinct_rate, 2),
        "H4 Relative Improvement": round(relative_improvement, 2),
        "H5 Time Reduction": round(time_reduction, 2)
    }
])

summary.to_csv("summary_results.csv", index=False)

print("Saved:")
print("- h1_results.csv")
print("- summary_results.csv")

print("\nDONE.")