import pandas as pd
import matplotlib.pyplot as plt


def load_titanic_data() -> pd.DataFrame:
    """Load Titanic dataset from a public URL."""
    urls = [
        "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv",
        "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/titanic.csv",
    ]

    last_error = None
    for url in urls:
        try:
            df = pd.read_csv(url)
            # Normalize schema when seaborn dataset is loaded
            if "survived" in df.columns and "sex" in df.columns:
                return df
            if "Survived" in df.columns and "Sex" in df.columns:
                return df
        except Exception as exc:  # noqa: BLE001
            last_error = exc

    raise RuntimeError(f"Failed to download Titanic dataset: {last_error}")


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Convert columns to lowercase and normalize key names."""
    out = df.copy()
    out.columns = [c.strip().lower() for c in out.columns]

    # Some datasets use 'class' instead of 'pclass'.
    if "class" in out.columns and "pclass" not in out.columns:
        class_map = {"First": 1, "Second": 2, "Third": 3}
        out["pclass"] = out["class"].map(class_map)

    return out


def clean_titanic(df: pd.DataFrame) -> pd.DataFrame:
    """Data cleansing pipeline."""
    out = normalize_columns(df)

    if "survived" not in out.columns:
        raise ValueError("Dataset must contain a 'survived' column.")
    if "sex" not in out.columns:
        raise ValueError("Dataset must contain a 'sex' column.")

    # Keep a stable subset of columns if available across versions.
    preferred_columns = [
        "survived",
        "pclass",
        "sex",
        "age",
        "sibsp",
        "parch",
        "fare",
        "embarked",
        "cabin",
    ]
    existing_columns = [c for c in preferred_columns if c in out.columns]
    out = out[existing_columns].copy()

    out = out.drop_duplicates().reset_index(drop=True)

    if "embarked" in out.columns:
        out["embarked"] = out["embarked"].fillna(out["embarked"].mode().iloc[0])

    if "fare" in out.columns:
        if "pclass" in out.columns:
            out["fare"] = out["fare"].fillna(out.groupby("pclass")["fare"].transform("median"))
        out["fare"] = out["fare"].fillna(out["fare"].median())

    if "age" in out.columns:
        if "pclass" in out.columns:
            out["age"] = out["age"].fillna(
                out.groupby(["sex", "pclass"])["age"].transform("median")
            )
        out["age"] = out["age"].fillna(out["age"].median())

    # Drop cabin when missing ratio is too high.
    if "cabin" in out.columns:
        missing_ratio = out["cabin"].isna().mean()
        if missing_ratio > 0.6:
            out = out.drop(columns=["cabin"])

    if {"sibsp", "parch"}.issubset(out.columns):
        out["family_size"] = out["sibsp"] + out["parch"] + 1
        out["is_alone"] = (out["family_size"] == 1).astype(int)

    if "age" in out.columns:
        out["age_group"] = pd.cut(
            out["age"],
            bins=[0, 12, 18, 35, 60, 120],
            labels=["Child", "Teen", "YoungAdult", "Adult", "Senior"],
            include_lowest=True,
        )

    return out


def print_analysis(df: pd.DataFrame) -> None:
    """Print multi-angle analysis to console."""
    overall_survival = df["survived"].mean() * 100
    print(f"[Overall] Survival rate: {overall_survival:.2f}%")

    sex_survival = (df.groupby("sex")["survived"].mean() * 100).sort_values(ascending=False)
    print("\n[By Sex] Survival rate (%)")
    print(sex_survival.round(2))

    if "pclass" in df.columns:
        class_survival = (df.groupby("pclass")["survived"].mean() * 100).sort_index()
        print("\n[By Passenger Class] Survival rate (%)")
        print(class_survival.round(2))

    if "embarked" in df.columns:
        embarked_survival = (df.groupby("embarked")["survived"].mean() * 100).sort_values(ascending=False)
        print("\n[By Embark Port] Survival rate (%)")
        print(embarked_survival.round(2))

    if "age_group" in df.columns:
        age_survival = (df.groupby("age_group", observed=False)["survived"].mean() * 100)
        print("\n[By Age Group] Survival rate (%)")
        print(age_survival.round(2))


def plot_analysis(df: pd.DataFrame) -> None:
    """Create visualization with matplotlib."""
    plt.rcParams["font.family"] = "Malgun Gothic"
    plt.rcParams["axes.unicode_minus"] = False

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # 1) Required chart: male vs female survival rate
    sex_survival = (df.groupby("sex")["survived"].mean() * 100).sort_values(ascending=False)
    axes[0, 0].bar(sex_survival.index, sex_survival.values, color=["#4F81BD", "#C0504D"])
    axes[0, 0].set_title("남성/여성 생존율")
    axes[0, 0].set_ylabel("생존율(%)")
    for idx, val in enumerate(sex_survival.values):
        axes[0, 0].text(idx, val + 1, f"{val:.1f}%", ha="center")

    # 2) Survival by class
    if "pclass" in df.columns:
        class_survival = (df.groupby("pclass")["survived"].mean() * 100).sort_index()
        axes[0, 1].bar(class_survival.index.astype(str), class_survival.values, color="#9BBB59")
        axes[0, 1].set_title("객실 등급별 생존율")
        axes[0, 1].set_ylabel("생존율(%)")

    # 3) Survival by age group
    if "age_group" in df.columns:
        age_survival = (df.groupby("age_group", observed=False)["survived"].mean() * 100)
        axes[1, 0].plot(age_survival.index.astype(str), age_survival.values, marker="o", color="#8064A2")
        axes[1, 0].set_title("연령대별 생존율")
        axes[1, 0].set_ylabel("생존율(%)")
        axes[1, 0].tick_params(axis="x", rotation=15)

    # 4) Survival by embarked port
    if "embarked" in df.columns:
        embarked_survival = (df.groupby("embarked")["survived"].mean() * 100).sort_values(ascending=False)
        axes[1, 1].bar(embarked_survival.index, embarked_survival.values, color="#F79646")
        axes[1, 1].set_title("승선 항구별 생존율")
        axes[1, 1].set_ylabel("생존율(%)")

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    raw_df = load_titanic_data()
    cleaned_df = clean_titanic(raw_df)

    print("=== Cleaned Data Preview ===")
    print(cleaned_df.head())
    print("\n=== Missing Values After Cleansing ===")
    print(cleaned_df.isna().sum())

    cleaned_df.to_csv("titanic_cleaned.csv", index=False, encoding="utf-8-sig")
    print("\nSaved cleaned dataset: titanic_cleaned.csv")

    print_analysis(cleaned_df)
    plot_analysis(cleaned_df)
