import pandas as pd


def remove_iqr_outliers(
    df,
    columns
):
    cleaned_df = df.copy()

    for column in columns:

        if column not in cleaned_df.columns:
            continue

        if not pd.api.types.is_numeric_dtype(
            cleaned_df[column]
        ):
            continue

        values = cleaned_df[column].dropna()

        if values.empty:
            continue

        q1 = values.quantile(0.25)
        q3 = values.quantile(0.75)

        iqr = q3 - q1

        lower_bound = q1 - (1.5 * iqr)
        upper_bound = q3 + (1.5 * iqr)

        mask = (
            cleaned_df[column].isna()
            |
            cleaned_df[column].between(
                lower_bound,
                upper_bound
            )
        )

        cleaned_df = cleaned_df[mask]

    return cleaned_df


def clean_data(
    df,
    remove_duplicates=True,
    trim_text=True,
    missing_strategy="Median / Mode",
    columns_to_remove=None,
    remove_outliers=False,
    outlier_columns=None
):
    cleaned_df = df.copy()

    if columns_to_remove:
        cleaned_df = cleaned_df.drop(
            columns=columns_to_remove,
            errors="ignore"
        )

    if trim_text:
        text_columns = (
            cleaned_df
            .select_dtypes(
                include="object"
            )
            .columns
        )

        for column in text_columns:

            cleaned_df[column] = (
                cleaned_df[column]
                .apply(
                    lambda value:
                    value.strip()
                    if isinstance(
                        value,
                        str
                    )
                    else value
                )
            )

            cleaned_df[column] = (
                cleaned_df[column]
                .replace(
                    "",
                    pd.NA
                )
            )

    if remove_duplicates:
        cleaned_df = (
            cleaned_df
            .drop_duplicates()
        )

    if missing_strategy == "Drop rows":

        cleaned_df = (
            cleaned_df
            .dropna()
        )

    elif missing_strategy == "Median / Mode":

        numeric_columns = (
            cleaned_df
            .select_dtypes(
                include="number"
            )
            .columns
        )

        for column in numeric_columns:

            if (
                cleaned_df[column]
                .isnull()
                .any()
            ):
                median_value = (
                    cleaned_df[column]
                    .median()
                )

                cleaned_df[column] = (
                    cleaned_df[column]
                    .fillna(
                        median_value
                    )
                )

        text_columns = (
            cleaned_df
            .select_dtypes(
                include="object"
            )
            .columns
        )

        for column in text_columns:

            if (
                cleaned_df[column]
                .isnull()
                .any()
            ):
                mode_value = (
                    cleaned_df[column]
                    .mode()
                )

                if not mode_value.empty:

                    cleaned_df[column] = (
                        cleaned_df[column]
                        .fillna(
                            mode_value[0]
                        )
                    )

                else:

                    cleaned_df[column] = (
                        cleaned_df[column]
                        .fillna(
                            "Unknown"
                        )
                    )

    elif missing_strategy == "Mean / Mode":

        numeric_columns = (
            cleaned_df
            .select_dtypes(
                include="number"
            )
            .columns
        )

        for column in numeric_columns:

            if (
                cleaned_df[column]
                .isnull()
                .any()
            ):
                mean_value = (
                    cleaned_df[column]
                    .mean()
                )

                cleaned_df[column] = (
                    cleaned_df[column]
                    .fillna(
                        mean_value
                    )
                )

        text_columns = (
            cleaned_df
            .select_dtypes(
                include="object"
            )
            .columns
        )

        for column in text_columns:

            if (
                cleaned_df[column]
                .isnull()
                .any()
            ):
                mode_value = (
                    cleaned_df[column]
                    .mode()
                )

                if not mode_value.empty:

                    cleaned_df[column] = (
                        cleaned_df[column]
                        .fillna(
                            mode_value[0]
                        )
                    )

                else:

                    cleaned_df[column] = (
                        cleaned_df[column]
                        .fillna(
                            "Unknown"
                        )
                    )

    elif missing_strategy == "Keep missing values":
        pass

    if (
        remove_outliers
        and outlier_columns
    ):
        cleaned_df = remove_iqr_outliers(
            cleaned_df,
            outlier_columns
        )

    cleaned_df = (
        cleaned_df
        .reset_index(
            drop=True
        )
    )

    return cleaned_df