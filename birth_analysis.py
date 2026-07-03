import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


def run_analysis(
    input_file: Path,
    output_clean_csv: Path,
    output_plot_png: Path,
) -> pd.DataFrame:
    """Load KOSIS excel, clean data, analyze, and save outputs."""

    raw = pd.read_excel(input_file, sheet_name=0)

    # Keep columns that look like year columns and normalize year value.
    year_cols = [c for c in raw.columns[1:] if any(ch.isdigit() for ch in str(c))]
    year_map = {}
    for c in year_cols:
        digits = "".join(ch for ch in str(c) if ch.isdigit())
        if len(digits) >= 4:
            year_map[c] = int(digits[:4])

    # In this KOSIS table layout: row 0 = births, row 4 = total fertility rate.
    births_row = raw.iloc[0, 1:]
    tfr_row = raw.iloc[4, 1:]

    records = []
    for c in year_cols:
        if c not in year_map:
            continue
        records.append(
            {
                "year": year_map[c],
                "births": births_row.get(c, np.nan),
                "total_fertility_rate": tfr_row.get(c, np.nan),
                "is_provisional": "p" in str(c).lower(),
            }
        )

    clean = (
        pd.DataFrame(records)
        .sort_values("year")
        .drop_duplicates("year", keep="last")
        .reset_index(drop=True)
    )

    clean["births"] = pd.to_numeric(clean["births"], errors="coerce")
    clean["total_fertility_rate"] = pd.to_numeric(
        clean["total_fertility_rate"], errors="coerce"
    )
    clean = clean.dropna(subset=["year", "births", "total_fertility_rate"]).reset_index(
        drop=True
    )

    # Derived metrics for multi-angle analysis.
    clean["births_yoy_change"] = clean["births"].diff()
    clean["births_yoy_pct"] = clean["births"].pct_change() * 100
    clean["tfr_yoy_change"] = clean["total_fertility_rate"].diff()

    clean.to_csv(output_clean_csv, index=False, encoding="utf-8-sig")

    plt.figure(figsize=(11, 5.5), dpi=130)
    plt.plot(clean["year"], clean["births"], marker="o", linewidth=2)
    plt.title("Korea Births by Year (1970-2025)")
    plt.xlabel("Year")
    plt.ylabel("Births (persons)")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_plot_png)
    plt.close()

    return clean


def print_summary(clean: pd.DataFrame) -> None:
    valid = clean.copy()

    summary = {
        "n_years": int(valid.shape[0]),
        "year_min": int(valid["year"].min()),
        "year_max": int(valid["year"].max()),
        "births_max_year": int(valid.loc[valid["births"].idxmax(), "year"]),
        "births_max_value": float(valid["births"].max()),
        "births_min_year": int(valid.loc[valid["births"].idxmin(), "year"]),
        "births_min_value": float(valid["births"].min()),
        "tfr_max_year": int(valid.loc[valid["total_fertility_rate"].idxmax(), "year"]),
        "tfr_max_value": float(valid["total_fertility_rate"].max()),
        "tfr_min_year": int(valid.loc[valid["total_fertility_rate"].idxmin(), "year"]),
        "tfr_min_value": float(valid["total_fertility_rate"].min()),
        "corr_births_tfr": float(valid["births"].corr(valid["total_fertility_rate"])),
    }

    dec = (
        valid.assign(decade=(valid["year"] // 10) * 10)
        .groupby("decade", as_index=False)[["births", "total_fertility_rate"]]
        .mean()
    )

    first = valid.iloc[0]
    last = valid.iloc[-1]
    years_span = int(last["year"] - first["year"])
    cagr = (last["births"] / first["births"]) ** (1 / years_span) - 1

    yoy = valid.dropna(subset=["births_yoy_change"])
    max_rise = yoy.loc[yoy["births_yoy_change"].idxmax(), ["year", "births_yoy_change"]]
    max_fall = yoy.loc[yoy["births_yoy_change"].idxmin(), ["year", "births_yoy_change"]]

    print("[Summary]")
    for k, v in summary.items():
        print(f"{k}: {v}")

    print("\n[Long-term]")
    print("first_year_births:", int(first["year"]), float(first["births"]))
    print(
        "last_year_births:",
        int(last["year"]),
        float(last["births"]),
        "provisional=",
        bool(last["is_provisional"]),
    )
    print("births_change_abs:", float(last["births"] - first["births"]))
    print("births_change_pct:", float((last["births"] / first["births"] - 1) * 100))
    print("births_cagr_pct:", float(cagr * 100))

    print("\n[Decade means]")
    print(dec.to_string(index=False))

    print("\n[Largest YoY rise/fall in births]")
    print("max_rise_year:", int(max_rise["year"]), "change:", float(max_rise["births_yoy_change"]))
    print("max_fall_year:", int(max_fall["year"]), "change:", float(max_fall["births_yoy_change"]))

    print("\n[Recent 10 years]")
    print(
        valid.tail(10)[["year", "births", "total_fertility_rate", "births_yoy_pct"]].to_string(
            index=False
        )
    )


if __name__ == "__main__":
    input_file = Path(r"c:\work\출생아수__합계출산율__자연증가_등_20260703152912.xlsx")
    output_clean_csv = Path(r"c:\work\birth_rate_cleaned.csv")
    output_plot_png = Path(r"c:\work\births_by_year_line.png")

    cleaned_df = run_analysis(input_file, output_clean_csv, output_plot_png)

    print("CLEAN_FILE:", output_clean_csv)
    print("PLOT_FILE:", output_plot_png)
    print_summary(cleaned_df)
