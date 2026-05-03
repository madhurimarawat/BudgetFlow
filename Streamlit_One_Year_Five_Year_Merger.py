import os
import pandas as pd
import streamlit as st

# -----------------------------
# Helper Functions
# -----------------------------


def get_year_folders(base_path):
    return sorted(
        [f for f in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, f))]
    )


def read_year_data(base_path, year):
    year_path = os.path.join(base_path, year)
    all_data = []

    for file in sorted(os.listdir(year_path)):
        file_path = os.path.join(year_path, file)
        if file.endswith(".csv"):
            try:
                df = pd.read_csv(file_path)
                df["source_file"] = file
                df["year"] = year
                all_data.append(df)
            except Exception as e:
                st.warning(f"Error reading {file}: {e}")

    if all_data:
        return pd.concat(all_data, ignore_index=True)
    return pd.DataFrame()


def merge_5_years(data_dict):
    merged = []
    years = sorted(data_dict.keys())

    for i in range(len(years)):
        chunk = years[i : i + 5]
        if len(chunk) == 5:
            dfs = [data_dict[y] for y in chunk if not data_dict[y].empty]
            if dfs:
                merged_df = pd.concat(dfs, ignore_index=True)
                merged.append(("-".join(chunk), merged_df))

    return merged


# -----------------------------
# Streamlit UI
# -----------------------------

st.set_page_config(page_title="Data Merger", layout="wide")
st.title("📊 Yearly & 5-Year Data Merger")

base_path = st.text_input("Enter Data Folder Path", value="data")

if os.path.exists(base_path):
    years = get_year_folders(base_path)

    if years:
        st.success(f"Found {len(years)} year folders")

        selected_years = st.multiselect("Select Years", years, default=years)

        data_dict = {}

        if st.button("🔄 Load & Merge Yearly Data"):
            with st.spinner("Processing..."):
                for year in selected_years:
                    df = read_year_data(base_path, year)
                    data_dict[year] = df

                st.session_state["data_dict"] = data_dict

        if "data_dict" in st.session_state:
            data_dict = st.session_state["data_dict"]

            st.subheader("📅 Yearly Merged Data")
            for year, df in data_dict.items():
                if not df.empty:
                    st.write(f"### {year}")
                    st.dataframe(df.head())
                    st.download_button(
                        label=f"Download {year}",
                        data=df.to_csv(index=False),
                        file_name=f"merged_{year}.csv",
                        mime="text/csv",
                    )

            st.subheader("🧩 5-Year Merged Data")
            merged_5y = merge_5_years(data_dict)

            for label, df in merged_5y:
                st.write(f"### {label}")
                st.dataframe(df.head())
                st.download_button(
                    label=f"Download {label}",
                    data=df.to_csv(index=False),
                    file_name=f"merged_{label}.csv",
                    mime="text/csv",
                )
    else:
        st.warning("No year folders found.")
else:
    st.error("Invalid folder path.")


# -----------------------------
# Notes:
# -----------------------------
# Folder Structure Expected:
# data/
#   ├── 2022/
#   │     ├── 01_January_2022.csv
#   │     ├── 02_February_2022.csv
#   ├── 2023/
#   ├── 2024/
#
# Run using:
# streamlit run app.py
