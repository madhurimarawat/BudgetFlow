# 🎉 Event Expense Manager

# Importing Dependencies
import streamlit as st
import pandas as pd
import os
from datetime import datetime

BASE_FOLDER = "data"

# -----------------------------
# 📁 Helpers
# -----------------------------


def get_event_file_path(year, month, event_name):
    folder_path = os.path.join(BASE_FOLDER, str(year))
    os.makedirs(folder_path, exist_ok=True)

    return os.path.join(folder_path, f"{month}_{year}_{event_name}.csv")


def get_month_file_path(year, month):
    folder_path = os.path.join(BASE_FOLDER, str(year))
    os.makedirs(folder_path, exist_ok=True)

    return os.path.join(folder_path, f"{month}_{year}.csv")


def load_data(path):
    if os.path.exists(path):
        return pd.read_csv(path)
    else:
        return pd.DataFrame(
            columns=["Date", "Category", "Subcategory", "Amount", "Notes"]
        )


def save_data(df, path):
    df.to_csv(path, index=False)


# -----------------------------
# 🎨 UI
# -----------------------------

st.set_page_config(page_title="Event Expense Manager", layout="wide")
st.title("🎉 Event Expense Manager")

# -----------------------------
# 📌 Event Setup
# -----------------------------

st.sidebar.header("📌 Event Setup")

month = st.sidebar.selectbox(
    "Month",
    [
        "01_January",
        "02_February",
        "03_March",
        "04_April",
        "05_May",
        "06_June",
        "07_July",
        "08_August",
        "09_September",
        "10_October",
        "11_November",
        "12_December",
    ],
)

year = st.sidebar.number_input(
    "Year", min_value=2000, max_value=2100, value=datetime.now().year
)

event_name = st.sidebar.text_input("Event Name (e.g., Marriage, Birthday)")

if not event_name:
    st.warning("⚠️ Enter an event name to continue.")
    st.stop()

event_name = event_name.replace(" ", "_")

event_file_path = get_event_file_path(year, month, event_name)
month_file_path = get_month_file_path(year, month)

df = load_data(event_file_path)

# -----------------------------
# ➕ Add Entry
# -----------------------------

st.sidebar.header("➕ Add Event Expense")

category = st.sidebar.text_input("Category (e.g., Decoration, Food)")
subcategory = st.sidebar.text_input("Subcategory (optional)")
amount_input = st.sidebar.text_input("Amount (₹)")
notes = st.sidebar.text_input("Notes")

try:
    amount = int(amount_input) if amount_input else 0
except:
    st.sidebar.error("⚠️ Enter valid amount")
    amount = 0

if st.sidebar.button("Add Expense"):
    new_row = {
        "Date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "Category": category,
        "Subcategory": subcategory,
        "Amount": amount,
        "Notes": notes,
    }

    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    save_data(df, event_file_path)

    st.sidebar.success("✅ Expense Added!")
    st.rerun()

# -----------------------------
# 📊 Event Summary
# -----------------------------

st.subheader(f"📊 Event: {event_name}")

if df.empty:
    st.warning("⚠️ No event data yet.")
else:
    df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")

    total = df["Amount"].sum()

    st.metric("💸 Total Event Expense", f"₹{total:.2f}")

    st.dataframe(df, use_container_width=True)

    # -----------------------------
    # 📤 Push to Monthly File
    # -----------------------------

    st.divider()
    st.subheader("📤 Add to Monthly Summary")

    if st.button("Add Total to Monthly File"):
        month_df = load_data(month_file_path)

        new_row = {
            "Date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "Type": "Expense",
            "Category": "Event 🎉",
            "Subcategory": event_name.capitalize(),
            "Amount": total,
            "Notes": f"{event_name} total expense",
        }

        month_df = pd.concat([month_df, pd.DataFrame([new_row])], ignore_index=True)
        save_data(month_df, month_file_path)

        st.success("✅ Added to monthly file!")

        # Optional safety warning
        st.warning("⚠️ Make sure you don't add this twice.")

# -----------------------------
# 📁 Info
# -----------------------------

st.info(f"📁 Event File: {event_file_path}")
st.info(f"📁 Monthly File: {month_file_path}")
