
import streamlit as st
import pandas as pd
import plotly.express as px
import io

# ----------------------------------
# PAGE CONFIGURATION
# ----------------------------------

st.set_page_config(
    page_title="Smart Data Cleaner",
    page_icon="🧹",
    layout="wide"
)

# ----------------------------------
# CUSTOM TITLE
# ----------------------------------

st.title("🧹 Smart Data Cleaner 3.0")

st.markdown(
    "Upload, Analyze, Visualize and Clean Your Dataset."
)

st.divider()

# ----------------------------------
# FILE UPLOAD
# ----------------------------------

uploaded_file = st.file_uploader(
    "📂 Upload CSV or Excel File",
    type=["csv", "xlsx"]
)

if uploaded_file is not None:

    try:

        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)

        else:
            df = pd.read_excel(uploaded_file)

        # Reset cleaning results when a new file is uploaded
        file_signature = (
            uploaded_file.name,
            uploaded_file.size
        )

        if st.session_state.get("file_signature") != file_signature:

            st.session_state.file_signature = file_signature
            st.session_state.cleaned_df = None
            st.session_state.cleaning_report = None

        st.success("Dataset Uploaded Successfully!")

        # ----------------------------------
        # DATASET OVERVIEW
        # ----------------------------------

        st.header("📊 Dataset Overview")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Total Rows", df.shape[0])

        with col2:
            st.metric("Total Columns", df.shape[1])

        with col3:
            st.metric(
                "Missing Values",
                int(df.isnull().sum().sum())
            )

        with col4:
            st.metric(
                "Duplicate Records",
                int(df.duplicated().sum())
            )

        # ----------------------------------
        # DATASET PREVIEW
        # ----------------------------------

        st.header("📋 Dataset Preview")

        st.dataframe(
            df.head(10),
            width="stretch"
        )

        # ----------------------------------
        # DATA INFORMATION
        # ----------------------------------

        st.header("🔍 Dataset Information")

        info_df = pd.DataFrame({
            "Column": df.columns,
            "Data Type": df.dtypes.astype(str).values,
            "Missing Values": df.isnull().sum().values,
            "Unique Values": df.nunique().values
        })

        st.dataframe(
            info_df,
            width="stretch"
        )

        # ----------------------------------
        # MISSING VALUES REPORT
        # ----------------------------------

        st.header("⚠️ Missing Values Report")

        missing_df = pd.DataFrame({
            "Column": df.columns,
            "Missing Values": df.isnull().sum().values,
            "Missing Percentage": (
                df.isnull().mean().values * 100
            ).round(2)
        })

        st.dataframe(
            missing_df,
            width="stretch"
        )

        # ----------------------------------
        # DUPLICATE RECORDS
        # ----------------------------------

        st.header("🔁 Duplicate Records")

        duplicates = int(df.duplicated().sum())

        st.metric(
            "Total Duplicate Records",
            duplicates
        )

        # ----------------------------------
        # DATA VISUALIZATION
        # ----------------------------------

        st.divider()

        st.header("📊 Data Visualization Dashboard")

        numeric_cols = df.select_dtypes(
            include="number"
        ).columns.tolist()

        categorical_cols = df.select_dtypes(
            include=["object", "category", "bool"]
        ).columns.tolist()

        # HISTOGRAM

        st.subheader("📈 Histogram Analysis")

        if numeric_cols:

            selected_numeric = st.selectbox(
                "Select Numerical Column",
                numeric_cols,
                key="histogram_column"
            )

            fig_hist = px.histogram(
                df,
                x=selected_numeric,
                title=f"Distribution of {selected_numeric}",
                marginal="box"
            )

            st.plotly_chart(
                fig_hist,
                width="stretch"
            )

        else:
            st.info("No numerical columns available.")

        # PIE CHART

        st.subheader("🥧 Pie Chart Analysis")

        if categorical_cols:

            selected_pie = st.selectbox(
                "Select Category for Pie Chart",
                categorical_cols,
                key="pie_column"
            )

            pie_data = (
                df[selected_pie]
                .fillna("Missing")
                .astype(str)
                .value_counts()
                .head(10)
                .reset_index()
            )

            pie_data.columns = [
                "Category",
                "Count"
            ]

            fig_pie = px.pie(
                pie_data,
                names="Category",
                values="Count",
                title=f"{selected_pie} Distribution",
                hole=0.35
            )

            st.plotly_chart(
                fig_pie,
                width="stretch"
            )

        # BAR CHART

        st.subheader("📊 Bar Chart Analysis")

        if categorical_cols:

            selected_bar = st.selectbox(
                "Select Category for Bar Chart",
                categorical_cols,
                key="bar_column"
            )

            bar_data = (
                df[selected_bar]
                .fillna("Missing")
                .astype(str)
                .value_counts()
                .head(10)
                .reset_index()
            )

            bar_data.columns = [
                "Category",
                "Count"
            ]

            fig_bar = px.bar(
                bar_data,
                x="Category",
                y="Count",
                title=f"{selected_bar} Comparison",
                text="Count"
            )

            st.plotly_chart(
                fig_bar,
                width="stretch"
            )

        # CORRELATION HEATMAP

        st.subheader("🔥 Correlation Heatmap")

        if len(numeric_cols) >= 2:

            correlation = df[numeric_cols].corr()

            fig_heatmap = px.imshow(
                correlation,
                text_auto=".2f",
                aspect="auto",
                color_continuous_scale="RdBu_r",
                title="Feature Correlation"
            )

            st.plotly_chart(
                fig_heatmap,
                width="stretch"
            )

        else:
            st.info(
                "At least two numerical columns are required."
            )

        # ----------------------------------
        # DATA CLEANING
        # ----------------------------------

        st.divider()

        st.header("🧹 Data Cleaning")

        st.write(
            "Click below to handle missing values "
            "and remove duplicate records."
        )

        if st.button(
            "🚀 Clean Dataset",
            type="primary"
        ):

            cleaned_df = df.copy()

            missing_before = int(
                cleaned_df.isnull().sum().sum()
            )

            duplicates_before = int(
                cleaned_df.duplicated().sum()
            )

            rows_before = len(cleaned_df)

            # Numerical Missing Values

            for col in cleaned_df.select_dtypes(
                include="number"
            ).columns:

                median_value = cleaned_df[col].median()

                if pd.notna(median_value):

                    cleaned_df[col] = cleaned_df[col].fillna(
                        median_value
                    )

            # Categorical Missing Values

            for col in cleaned_df.select_dtypes(
                include=["object", "category"]
            ).columns:

                mode_values = cleaned_df[col].mode()

                if not mode_values.empty:

                    cleaned_df[col] = cleaned_df[col].fillna(
                        mode_values[0]
                    )

            # Boolean Missing Values

            for col in cleaned_df.select_dtypes(
                include="bool"
            ).columns:

                mode_values = cleaned_df[col].mode()

                if not mode_values.empty:

                    cleaned_df[col] = cleaned_df[col].fillna(
                        mode_values[0]
                    )

            # Remove Duplicates

            cleaned_df = cleaned_df.drop_duplicates()

            missing_after = int(
                cleaned_df.isnull().sum().sum()
            )

            rows_after = len(cleaned_df)

            duplicates_removed = (
                rows_before - rows_after
            )

            # Store Results

            st.session_state.cleaned_df = cleaned_df

            st.session_state.cleaning_report = {
                "Rows Before": rows_before,
                "Rows After": rows_after,
                "Duplicates Removed": duplicates_removed,
                "Missing Values Before": missing_before,
                "Missing Values After": missing_after
            }

        # ----------------------------------
        # CLEANING RESULTS
        # ----------------------------------

        if st.session_state.get("cleaned_df") is not None:

            cleaned_df = st.session_state.cleaned_df

            report = st.session_state.cleaning_report

            st.success(
                "✅ Dataset Cleaning Completed Successfully!"
            )

            # BEFORE VS AFTER

            st.header("🔄 Before vs After Comparison")

            c1, c2, c3 = st.columns(3)

            c1.metric(
                "Before Cleaning",
                report["Rows Before"]
            )

            c2.metric(
                "After Cleaning",
                report["Rows After"],
                delta=report["Rows After"] - report["Rows Before"]
            )

            c3.metric(
                "Duplicates Removed",
                report["Duplicates Removed"]
            )

            # CLEANING REPORT

            st.header("📋 Cleaning Report")

            report_df = pd.DataFrame({
                "Metric": report.keys(),
                "Value": report.values()
            })

            st.dataframe(
                report_df,
                width="stretch"
            )

            # CLEANED PREVIEW

            st.header("✨ Cleaned Dataset Preview")

            st.dataframe(
                cleaned_df.head(10),
                width="stretch"
            )

            # CSV DOWNLOAD

            st.subheader("📥 Download Cleaned Dataset")

            csv_data = cleaned_df.to_csv(
                index=False
            ).encode("utf-8")

            st.download_button(
                label="📄 Download Cleaned CSV",
                data=csv_data,
                file_name="cleaned_dataset.csv",
                mime="text/csv"
            )

            # EXCEL DOWNLOAD

            excel_buffer = io.BytesIO()

            with pd.ExcelWriter(
                excel_buffer,
                engine="openpyxl"
            ) as writer:

                cleaned_df.to_excel(
                    writer,
                    index=False,
                    sheet_name="Cleaned Data"
                )

                report_df.to_excel(
                    writer,
                    index=False,
                    sheet_name="Cleaning Report"
                )

            st.download_button(
                label="📊 Download Cleaned Excel",
                data=excel_buffer.getvalue(),
                file_name="cleaned_dataset.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

    except Exception as e:

        st.error(f"Error: {e}")

else:

    st.info(
        "👆 Please upload a CSV or Excel dataset to get started."
    )

    st.markdown("""
    ### Features Available

    - Dataset Analysis
    - Missing Values Detection
    - Duplicate Records Detection
    - Histogram
    - Pie Chart
    - Bar Chart
    - Correlation Heatmap
    - Automatic Data Cleaning
    - CSV and Excel Download
    """)
