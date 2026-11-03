import streamlit as st
import pandas as pd
import numpy as np

from io import BytesIO

from analyzer import (
    analyze_data,
    get_numeric_summary,
    get_missing_summary,
    get_column_types,
    get_correlation_matrix,
    get_outlier_summary,
    calculate_quality_score
)

from cleaner import clean_data


st.set_page_config(
    page_title="Data Cleaner Pro",
    page_icon="🧹",
    layout="wide"
)


st.title("🧹 Data Cleaner Pro")

st.caption(
    "Analyze, visualize, clean and export CSV or Excel datasets."
)


uploaded_file = st.file_uploader(
    "Upload a CSV or Excel file",
    type=[
        "csv",
        "xlsx"
    ]
)


if uploaded_file is not None:

    file_key = (
        uploaded_file.name,
        uploaded_file.size
    )

    if (
        "current_file"
        not in st.session_state
        or
        st.session_state.current_file
        != file_key
    ):
        st.session_state.current_file = (
            file_key
        )

        st.session_state.pop(
            "cleaned_df",
            None
        )

        st.session_state.pop(
            "cleaning_options",
            None
        )


    try:

        if (
            uploaded_file.name
            .lower()
            .endswith(".csv")
        ):
            df = pd.read_csv(
                uploaded_file
            )

        else:
            df = pd.read_excel(
                uploaded_file
            )

    except Exception as error:

        st.error(
            f"Could not read the file: {error}"
        )

        st.stop()


    analysis = analyze_data(df)

    quality_score = (
        calculate_quality_score(df)
    )

    numeric_columns = list(
        df.select_dtypes(
            include="number"
        ).columns
    )


    # Sidebar
    with st.sidebar:

        st.header(
            "Cleaning Settings"
        )

        remove_duplicates = (
            st.checkbox(
                "Remove duplicates",
                value=True
            )
        )

        trim_text = (
            st.checkbox(
                "Trim text values",
                value=True
            )
        )

        missing_strategy = (
            st.selectbox(
                "Missing values",
                [
                    "Median / Mode",
                    "Mean / Mode",
                    "Drop rows",
                    "Keep missing values"
                ]
            )
        )

        columns_to_remove = (
            st.multiselect(
                "Remove columns",
                options=list(
                    df.columns
                )
            )
        )

        st.divider()

        remove_outliers = (
            st.checkbox(
                "Remove outliers",
                value=False
            )
        )

        outlier_columns = []

        if remove_outliers:

            outlier_columns = (
                st.multiselect(
                    "Outlier columns",
                    options=numeric_columns
                )
            )

            st.caption(
                "Outliers are detected using the IQR method."
            )


    overview_tab, analysis_tab, cleaning_tab = (
        st.tabs(
            [
                "Overview",
                "Analysis",
                "Clean & Export"
            ]
        )
    )


    # Overview Tab
    with overview_tab:

        st.subheader(
            "Dataset Overview"
        )

        col1, col2, col3, col4 = (
            st.columns(4)
        )

        col1.metric(
            "Rows",
            analysis["rows"]
        )

        col2.metric(
            "Columns",
            analysis["columns"]
        )

        col3.metric(
            "Duplicates",
            analysis["duplicates"]
        )

        col4.metric(
            "Missing Values",
            analysis["missing_values"]
        )


        st.subheader(
            "Data Quality Score"
        )

        score_col1, score_col2 = (
            st.columns(
                [
                    1,
                    3
                ]
            )
        )

        with score_col1:

            st.metric(
                "Score",
                f"{quality_score} / 100"
            )

        with score_col2:

            st.progress(
                int(
                    quality_score
                )
            )

            if quality_score >= 90:

                st.success(
                    "Excellent data quality"
                )

            elif quality_score >= 75:

                st.info(
                    "Good data quality"
                )

            elif quality_score >= 50:

                st.warning(
                    "Data needs cleaning"
                )

            else:

                st.error(
                    "Poor data quality"
                )


        st.subheader(
            "Data Preview"
        )

        st.dataframe(
            df,
            use_container_width=True
        )


        st.subheader(
            "Column Information"
        )

        column_types = (
            get_column_types(df)
        )

        st.dataframe(
            column_types,
            use_container_width=True,
            hide_index=True
        )


    # Analysis Tab
    with analysis_tab:

        st.subheader(
            "Missing Values"
        )

        missing_summary = (
            get_missing_summary(df)
        )

        if missing_summary.empty:

            st.success(
                "No missing values found."
            )

        else:

            missing_left, missing_right = (
                st.columns(2)
            )

            with missing_left:

                st.dataframe(
                    missing_summary,
                    use_container_width=True
                )

            with missing_right:

                st.bar_chart(
                    missing_summary[
                        "Missing Values"
                    ]
                )


        st.subheader(
            "Numeric Statistics"
        )

        numeric_summary = (
            get_numeric_summary(df)
        )

        if numeric_summary.empty:

            st.info(
                "No numeric columns found."
            )

        else:

            st.dataframe(
                numeric_summary,
                use_container_width=True
            )


        st.subheader(
            "Correlation Analysis"
        )

        correlation_matrix = (
            get_correlation_matrix(
                df
            )
        )

        if correlation_matrix.empty:

            st.info(
                "At least two numeric columns are required."
            )

        else:

            st.dataframe(
                correlation_matrix,
                use_container_width=True
            )


        st.subheader(
            "Outlier Detection"
        )

        outlier_summary = (
            get_outlier_summary(df)
        )

        if outlier_summary.empty:

            st.info(
                "No numeric columns available."
            )

        else:

            st.dataframe(
                outlier_summary,
                use_container_width=True,
                hide_index=True
            )

            total_outliers = int(
                outlier_summary[
                    "Outliers"
                ].sum()
            )

            if total_outliers == 0:

                st.success(
                    "No potential outliers detected."
                )

            else:

                st.warning(
                    f"{total_outliers} potential outliers detected."
                )


        st.subheader(
            "Chart Builder"
        )

        chart_type = (
            st.selectbox(
                "Chart type",
                [
                    "Histogram",
                    "Bar Chart",
                    "Line Chart",
                    "Scatter Plot"
                ]
            )
        )


        if chart_type == "Histogram":

            if numeric_columns:

                selected_column = (
                    st.selectbox(
                        "Numeric column",
                        numeric_columns,
                        key="hist_column"
                    )
                )

                values = (
                    df[selected_column]
                    .dropna()
                )

                if not values.empty:

                    counts, bins = (
                        np.histogram(
                            values,
                            bins=10
                        )
                    )

                    labels = []

                    for i in range(
                        len(bins) - 1
                    ):

                        labels.append(
                            f"{bins[i]:.2f} - "
                            f"{bins[i + 1]:.2f}"
                        )

                    histogram_df = (
                        pd.DataFrame(
                            {
                                "Range":
                                    labels,

                                "Count":
                                    counts
                            }
                        )
                    )

                    histogram_df = (
                        histogram_df
                        .set_index(
                            "Range"
                        )
                    )

                    st.bar_chart(
                        histogram_df
                    )

            else:

                st.info(
                    "No numeric columns available."
                )


        elif chart_type == "Bar Chart":

            selected_column = (
                st.selectbox(
                    "Column",
                    list(
                        df.columns
                    ),
                    key="bar_column"
                )
            )

            values = (
                df[selected_column]
                .fillna(
                    "Missing"
                )
                .astype(str)
                .value_counts()
                .head(20)
            )

            st.bar_chart(
                values
            )


        elif chart_type == "Line Chart":

            if numeric_columns:

                selected_column = (
                    st.selectbox(
                        "Numeric column",
                        numeric_columns,
                        key="line_column"
                    )
                )

                st.line_chart(
                    df[
                        selected_column
                    ]
                )

            else:

                st.info(
                    "No numeric columns available."
                )


        elif chart_type == "Scatter Plot":

            if len(
                numeric_columns
            ) >= 2:

                x_column = (
                    st.selectbox(
                        "X axis",
                        numeric_columns,
                        key="scatter_x"
                    )
                )

                y_options = [
                    column
                    for column
                    in numeric_columns
                    if column
                    != x_column
                ]

                y_column = (
                    st.selectbox(
                        "Y axis",
                        y_options,
                        key="scatter_y"
                    )
                )

                st.scatter_chart(
                    df,
                    x=x_column,
                    y=y_column
                )

            else:

                st.info(
                    "At least two numeric columns are required."
                )


    # Cleaning Tab
    with cleaning_tab:

        st.subheader(
            "Cleaning Configuration"
        )

        st.write(
            "Use the sidebar to configure the cleaning process."
        )

        options1, options2 = (
            st.columns(2)
        )

        with options1:

            st.write(
                f"Remove duplicates: {remove_duplicates}"
            )

            st.write(
                f"Trim text: {trim_text}"
            )

            st.write(
                f"Missing strategy: {missing_strategy}"
            )

        with options2:

            st.write(
                f"Remove outliers: {remove_outliers}"
            )

            st.write(
                "Removed columns:",
                columns_to_remove
                if columns_to_remove
                else "None"
            )

            st.write(
                "Outlier columns:",
                outlier_columns
                if outlier_columns
                else "None"
            )


        if st.button(
            "Clean Data",
            type="primary",
            use_container_width=True
        ):

            cleaned_df = clean_data(
                df,
                remove_duplicates=remove_duplicates,
                trim_text=trim_text,
                missing_strategy=missing_strategy,
                columns_to_remove=columns_to_remove,
                remove_outliers=remove_outliers,
                outlier_columns=outlier_columns
            )


            st.session_state[
                "cleaned_df"
            ] = cleaned_df


            st.session_state[
                "cleaning_options"
            ] = {
                "missing_strategy":
                    missing_strategy,

                "remove_duplicates":
                    remove_duplicates,

                "trim_text":
                    trim_text,

                "remove_outliers":
                    remove_outliers,

                "columns_to_remove":
                    columns_to_remove,

                "outlier_columns":
                    outlier_columns
            }


        if (
            "cleaned_df"
            in st.session_state
        ):

            cleaned_df = (
                st.session_state[
                    "cleaned_df"
                ]
            )

            cleaned_analysis = (
                analyze_data(
                    cleaned_df
                )
            )

            cleaned_quality_score = (
                calculate_quality_score(
                    cleaned_df
                )
            )


            rows_removed = (
                analysis["rows"]
                - cleaned_analysis[
                    "rows"
                ]
            )


            columns_removed = (
                analysis["columns"]
                - cleaned_analysis[
                    "columns"
                ]
            )


            duplicates_removed = (
                max(
                    0,
                    analysis[
                        "duplicates"
                    ]
                    -
                    cleaned_analysis[
                        "duplicates"
                    ]
                )
            )


            missing_fixed = (
                max(
                    0,
                    analysis[
                        "missing_values"
                    ]
                    -
                    cleaned_analysis[
                        "missing_values"
                    ]
                )
            )


            st.success(
                "Data cleaned successfully."
            )


            st.subheader(
                "Cleaning Results"
            )

            result1, result2, result3, result4 = (
                st.columns(4)
            )

            result1.metric(
                "Rows Removed",
                rows_removed
            )

            result2.metric(
                "Columns Removed",
                columns_removed
            )

            result3.metric(
                "Duplicates Removed",
                duplicates_removed
            )

            result4.metric(
                "Missing Values Handled",
                missing_fixed
            )


            st.subheader(
                "Quality Improvement"
            )

            quality1, quality2 = (
                st.columns(2)
            )

            quality1.metric(
                "Before",
                f"{quality_score} / 100"
            )

            quality2.metric(
                "After",
                f"{cleaned_quality_score} / 100",
                delta=round(
                    cleaned_quality_score
                    - quality_score,
                    1
                )
            )


            st.subheader(
                "Before vs After"
            )

            before_col, after_col = (
                st.columns(2)
            )

            with before_col:

                st.markdown(
                    "### Before"
                )

                st.metric(
                    "Rows",
                    analysis["rows"]
                )

                st.metric(
                    "Columns",
                    analysis["columns"]
                )

                st.metric(
                    "Duplicates",
                    analysis[
                        "duplicates"
                    ]
                )
                st.metric(
                    "Missing Values",
                    analysis[
                        "missing_values"
                    ]
                )
            with after_col:
                st.markdown(
                    "### After"
                )
                st.metric(
                    "Rows",
                    cleaned_analysis[
                        "rows"
                    ]
                )
                st.metric(
                    "Columns",
                    cleaned_analysis[
                        "columns"
                    ]
                )
                st.metric(
                    "Duplicates",
                    cleaned_analysis[
                        "duplicates"
                    ]
                )
                st.metric(
                    "Missing Values",
                    cleaned_analysis[
                        "missing_values"
                    ]
                )
            st.subheader(
                "Cleaned Data"
            )
            st.dataframe(
                cleaned_df,
                use_container_width=True
            )
            st.subheader(
                "Download Results"
            )
            csv_data = (
                cleaned_df
                .to_csv(
                    index=False
                )
                .encode(
                    "utf-8"
                )
            )
            excel_buffer = (
                BytesIO()
            )
            with pd.ExcelWriter(
                excel_buffer,
                engine="openpyxl"
            ) as writer:
                cleaned_df.to_excel(
                    writer,
                    index=False,
                    sheet_name="Cleaned Data"
                )
            excel_data = (
                excel_buffer
                .getvalue()
            )
            report = f"""
DATA CLEANER PRO - CLEANING REPORT
Original rows: {analysis["rows"]}
Final rows: {cleaned_analysis["rows"]}
Rows removed: {rows_removed}
Original columns: {analysis["columns"]}
Final columns: {cleaned_analysis["columns"]}
Columns removed: {columns_removed}
Duplicates before: {analysis["duplicates"]}
Duplicates after: {cleaned_analysis["duplicates"]}
Duplicates removed: {duplicates_removed}
Missing values before: {analysis["missing_values"]}
Missing values after: {cleaned_analysis["missing_values"]}
Missing values handled: {missing_fixed}
Quality score before: {quality_score}
Quality score after: {cleaned_quality_score}
Missing strategy: {missing_strategy}
Trim text: {trim_text}
Remove duplicates: {remove_duplicates}
Remove outliers: {remove_outliers}
Removed columns:
{", ".join(columns_to_remove) if columns_to_remove else "None"}
Outlier columns:
{", ".join(outlier_columns) if outlier_columns else "None"}
"""
            download1, download2, download3 = (
                st.columns(3)
            )
            with download1:
                st.download_button(
                    "Download CSV",
                    data=csv_data,
                    file_name="cleaned_data.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            with download2:
                st.download_button(
                    "Download Excel",
                    data=excel_data,
                    file_name="cleaned_data.xlsx",
                    mime=(
                        "application/vnd.openxmlformats-officedocument."
                        "spreadsheetml.sheet"
                    ),
                    use_container_width=True
                )
            with download3:
                st.download_button(
                    "Download Report",
                    data=report,
                    file_name="cleaning_report.txt",
                    mime="text/plain",
                    use_container_width=True
                )