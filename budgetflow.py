# Importing Dependencies
import streamlit as st
import pandas as pd
import os
from datetime import datetime
import random
import matplotlib.pyplot as plt

BASE_FOLDER = "data"

# 🎨 Default Category Colors
CATEGORY_COLORS = {
    "Salary 💼": "#27ae60",  # nice green
    "Entertainment 🎬": "#9b59b6",
    "Groceries 🛒": "#2ecc71",
    "Clothes 👕": "#e84393",
    "Rent 🏠": "#e67e22",
    "Bills 💡": "#f1c40f",
    "Food 🍔": "#e74c3c",
    "Study 📚": "#3498db",
}

CATEGORIES = {
    "Salary 💼": ["Salary"],
    "Entertainment 🎬": ["Movies"],
    "Groceries 🛒": ["Dmart", "Local Shop"],
    "Clothes 👕": ["Readymade", "Stitched"],
    "Rent 🏠": ["Home Rent", "Vehicle Rent"],
    "Bills 💡": ["Mobile", "Electricity"],
    "Food 🍔": ["Outside", "Snacks"],
    "Study 📚": ["Books", "Courses"],
}

QUOTES = [
    "💡 Control money or it will control you.",
    "📈 Small savings today = big freedom tomorrow.",
    "🔥 Discipline > Motivation in finance.",
    "💸 Spend wisely, live freely.",
    "📊 What gets tracked gets improved.",
]


# 📁 File path
def get_file_path():
    now = datetime.now()
    year = str(now.year)
    month = now.strftime("%B").lower()

    folder_path = os.path.join(BASE_FOLDER, year)
    os.makedirs(folder_path, exist_ok=True)

    return os.path.join(folder_path, f"{month}_{year}.csv")


# 📥 Load data
def load_data(path):
    if os.path.exists(path):
        return pd.read_csv(path)
    else:
        return pd.DataFrame(
            columns=[
                "Date",
                "Type",
                "Category",
                "Subcategory",
                "Amount",
                "Notes",
            ]
        )


# 💾 Save data
def save_data(df, path):
    df.to_csv(path, index=False)


# 🌟 UI START
st.set_page_config(page_title="BudgetFlow", layout="wide")
st.title("💸 BudgetFlow Dashboard")


def get_available_files():
    files = []
    if not os.path.exists(BASE_FOLDER):
        return files

    for year in os.listdir(BASE_FOLDER):
        year_path = os.path.join(BASE_FOLDER, year)
        if os.path.isdir(year_path):
            for file in os.listdir(year_path):
                if file.endswith(".csv"):
                    files.append(
                        (file.replace(".csv", ""), os.path.join(year_path, file))
                    )

    return sorted(files, reverse=True)


st.sidebar.header("📂 View Data")

files = get_available_files()

file_names = [f[0] for f in files]

selected_file_name = st.sidebar.selectbox("Select Month", file_names)

# Get selected file path
selected_file_path = dict(files)[selected_file_name]

st.sidebar.header("➕ Add Entry Month")

selected_month = st.sidebar.selectbox(
    "Month",
    [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    ],
)

selected_year = st.sidebar.number_input(
    "Year", min_value=2000, max_value=2100, value=datetime.now().year
)

# Create path based on selection
folder_path = os.path.join(BASE_FOLDER, str(selected_year))
os.makedirs(folder_path, exist_ok=True)

file_path = os.path.join(folder_path, f"{selected_month.lower()}_{selected_year}.csv")

st.info(random.choice(QUOTES))

df = load_data(selected_file_path)

# ================================
# ➕ ADD ENTRY SECTION
# ================================
st.sidebar.header("➕ Add Entry")

entry_type = st.sidebar.selectbox("Type", ["Income 💰", "Expense 💸"])

# 🧠 Merge default + existing categories
existing_categories = df["Category"].dropna().unique().tolist()
all_categories = list(set(existing_categories + list(CATEGORIES.keys())))

category = st.sidebar.selectbox("Category", sorted(all_categories))


# 🔁 Subcategory logic (default + existing)
default_subs = CATEGORIES.get(category, [])
existing_subs = df[df["Category"] == category]["Subcategory"].dropna().unique().tolist()

all_subs = list(set(default_subs + existing_subs))

subcategory = st.sidebar.selectbox("Subcategory", sorted(all_subs + ["➕ Add New"]))

# ➕ Add new subcategory
if subcategory == "➕ Add New":
    subcategory = st.sidebar.text_input("New Subcategory")

if subcategory == "➕ Add New":
    subcategory = st.sidebar.text_input("New Subcategory")

# 💸 FLOAT INPUT
amount_input = st.sidebar.text_input("Amount (₹)")

# Convert to number safely
try:
    amount = int(amount_input) if amount_input else 0
except ValueError:
    st.sidebar.error("⚠️ Enter a valid number")
    amount = 0

notes = st.sidebar.text_input("Notes")

if st.sidebar.button("Add Entry"):
    new_row = {
        "Date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "Type": "Income" if "Income" in entry_type else "Expense",
        "Category": category,
        "Subcategory": subcategory,
        "Amount": amount,
        "Notes": notes,
    }

    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    save_data(df, file_path)

    st.sidebar.success("✅ Entry Added!")
    st.rerun()


# ================================
# 📊 MAIN DASHBOARD
# ================================

if df.empty:
    st.warning("⚠️ No data yet.")
else:
    df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")

    income = df[df["Type"] == "Income"]["Amount"].sum()
    expense = df[df["Type"] == "Expense"]["Amount"].sum()
    balance = income - expense

    col1, col2, col3 = st.columns(3)

    col1.metric("💰 Income", f"₹{income:.2f}")
    col2.metric("💸 Expense", f"₹{expense:.2f}")

    if balance >= 0:
        col3.markdown(
            f"<h3 style='color:green;'>💚 Leftover: ₹{balance:.2f}</h3>",
            unsafe_allow_html=True,
        )
    else:
        col3.markdown(
            f"<h3 style='color:red;'>🔴 Debt: ₹{abs(balance):.2f}</h3>",
            unsafe_allow_html=True,
        )

    st.divider()

    # ================================
    # 📊 CATEGORY BREAKDOWN
    # ================================
    st.subheader("📊 Category Breakdown")

    df_no_salary = df[df["Category"] != "Salary 💼"]

    summary = (
        df_no_salary.groupby("Category")["Amount"].sum().sort_values(ascending=False)
    )

    for cat, value in summary.items():
        color = CATEGORY_COLORS.get(cat, "#95a5a6")
        st.markdown(
            f"""
            <div style='background-color:{color};
                        padding:10px;
                        border-radius:10px;
                        margin-bottom:8px;
                        color:white;
                        font-weight:bold;'>
                {cat}: ₹{value:.2f}
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.divider()

    # ================================
    # 📈 CHARTS
    # ================================
    st.subheader("📈 Visual Insights")

    col1, col2 = st.columns(2)

    with col1:

        fig, ax = plt.subplots()

        colors = [CATEGORY_COLORS.get(cat, "#95a5a6") for cat in summary.index]

        ax.bar(summary.index, summary.values, color=colors)

        ax.set_title("Expenses by Category")
        ax.set_ylabel("Amount (₹)")
        ax.set_xticklabels(summary.index, rotation=45, ha="right")

        st.pyplot(fig)

    with col2:

        fig, ax = plt.subplots()

        colors = [CATEGORY_COLORS.get(cat, "#95a5a6") for cat in summary.index]

        ax.pie(
            summary.values,
            labels=summary.index,
            autopct="%1.1f%%",
            colors=colors,
            startangle=90,
        )

        ax.set_title("Expense Distribution")

        st.pyplot(fig)

    st.divider()

    # ================================
    # 📋 DATA TABLE
    # ================================
    st.subheader("📋 All Transactions")
    st.dataframe(df, use_container_width=True)

st.success(f"📊 Viewing: {selected_file_name}")
st.info(f"✍️ Adding entries to: {selected_month} {selected_year}")
