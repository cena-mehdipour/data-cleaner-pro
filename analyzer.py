import pandas as pd


def analyze_data(df):
    return {
        "rows": len(df),
        "columns": len(df.columns),
        "duplicates": int(df.duplicated().sum()),
        "missing_values": int(df.isnull().sum().sum())
    }


def get_numeric_summary(df):
    numeric_df = df.select_dtypes(include="number")

    if numeric_df.empty:
        return pd.DataFrame()

    summary = numeric_df.describe().T

    summary = summary.rename(
        columns={
            "count": "Count",
            "mean": "Mean",
            "std": "Std Dev",
            "min": "Min",
            "25%": "25%",
            "50%": "Median",
            "75%": "75%",
            "max": "Max"
        }
    )

    return summary.round(2)


def get_missing_summary(df):
    missing_values = df.isnull().sum()

    if len(df) > 0:
        missing_percent = (
            missing_values / len(df) * 100
        ).round(2)
    else:
        missing_percent = missing_values * 0

    summary = pd.DataFrame(
        {
            "Missing Values": missing_values,
            "Missing %": missing_percent
        }
    )

    return summary[
        summary["Missing Values"] > 0
    ]


def get_column_types(df):
    results = []

    for column in df.columns:
        dtype = df[column].dtype

        if pd.api.types.is_bool_dtype(dtype):
            detected_type = "Boolean"

        elif pd.api.types.is_numeric_dtype(dtype):
            detected_type = "Numeric"

        elif pd.api.types.is_datetime64_any_dtype(dtype):
            detected_type = "Date / Time"

        else:
            detected_type = "Text / Categorical"

        results.append(
            {
                "Column": column,
                "Type": detected_type,
                "Data Type": str(dtype),
                "Unique Values": int(df[column].nunique()),
                "Missing Values": int(
                    df[column].isnull().sum()
                )
            }
        )

    return pd.DataFrame(results)


def get_correlation_matrix(df):
    numeric_df = df.select_dtypes(include="number")

    if len(numeric_df.columns) < 2:
        return pd.DataFrame()

    return numeric_df.corr().round(2)


def get_outlier_summary(df):
    numeric_df = df.select_dtypes(include="number")

    results = []

    for column in numeric_df.columns:
        values = numeric_df[column].dropna()

        if values.empty:
            continue

        q1 = values.quantile(0.25)
        q3 = values.quantile(0.75)

        iqr = q3 - q1

        lower_bound = q1 - (1.5 * iqr)
        upper_bound = q3 + (1.5 * iqr)

        outliers = values[
            (values < lower_bound)
            | (values > upper_bound)
        ]

        percentage = (
            len(outliers) / len(values) * 100
            if len(values) > 0
            else 0
        )

        results.append(
            {
                "Column": column,
                "Outliers": int(len(outliers)),
                "Outlier %": round(percentage, 2),
                "Lower Bound": round(lower_bound, 2),
                "Upper Bound": round(upper_bound, 2)
            }
        )

    return pd.DataFrame(results)


def calculate_quality_score(df):
    if df.empty:
        return 0

    total_cells = df.shape[0] * df.shape[1]

    if total_cells == 0:
        return 0

    missing_ratio = (
        df.isnull().sum().sum()
        / total_cells
    )

    duplicate_ratio = (
        df.duplicated().sum()
        / len(df)
    )

    outlier_summary = get_outlier_summary(df)

    numeric_df = df.select_dtypes(
        include="number"
    )

    if (
        not outlier_summary.empty
        and not numeric_df.empty
    ):
        total_outliers = int(
            outlier_summary["Outliers"].sum()
        )

        numeric_cells = (
            len(df)
            * len(numeric_df.columns)
        )

        outlier_ratio = (
            total_outliers / numeric_cells
            if numeric_cells > 0
            else 0
        )

    else:
        outlier_ratio = 0

    missing_penalty = missing_ratio * 40
    duplicate_penalty = duplicate_ratio * 30
    outlier_penalty = outlier_ratio * 30

    score = (
        100
        - missing_penalty
        - duplicate_penalty
        - outlier_penalty
    )

    score = max(
        0,
        min(100, score)
    )

    return round(score, 1)