"""
🎁 Gift Tracker - Streamlit App

📌 Purpose:
Track gifts received during events with approximate price ranges,
so you can analyze and plan return gifts in a structured way.

✨ Features:
- Event-based gift tracking
- Price-based categorization
- Total value calculation
- Category-wise breakdown
- Clean CSV-based storage (no database needed)

👩‍💻 Author: Madhurima Rawat
"""

# -----------------------------
# 📦 Imports
# -----------------------------
import streamlit as st  # 🎨 UI framework
import pandas as pd  # 📊 Data handling
import os  # 📁 File management
from datetime import datetime  # ⏱ Timestamping

# 📁 Base folder where all data will be stored
BASE_FOLDER = "data"


# -----------------------------
# 📁 Helper Functions
# -----------------------------


def get_gift_file_path(year, month, event_name):
    """
    📌 Generates file path for storing gift data.

    Ensures:
    - Year-wise folder structure
    - Consistent file naming

    📂 Example:
    data/2026/05_May_2026_Wedding_Gift_Tracking.csv
    """
    folder_path = os.path.join(BASE_FOLDER, str(year))

    # 🛠 Create folder if it doesn't exist
    os.makedirs(folder_path, exist_ok=True)

    # 📄 Return full file path
    return os.path.join(folder_path, f"{month}_{year}_{event_name}_Gift_Tracking.csv")


def load_data(path):
    """
    📥 Loads existing CSV data.

    If file doesn't exist:
    → returns empty DataFrame with predefined columns
    """
    if os.path.exists(path):
        return pd.read_csv(path)
    else:
        # 🆕 Empty structure for first-time use
        return pd.DataFrame(
            columns=["Date", "Gift Name", "Given By", "Category", "Approx Price"]
        )


def save_data(df, path):
    """
    💾 Saves DataFrame to CSV.

    index=False → cleaner file without row numbers
    """
    df.to_csv(path, index=False)


# -----------------------------
# 🎨 UI Setup
# -----------------------------

# ⚙️ Page configuration
st.set_page_config(page_title="Gift Tracker", layout="wide")

# 🏷 Main title
st.title("🎁 Gift Tracker")


# -----------------------------
# 📌 Event Setup (Sidebar)
# -----------------------------

st.sidebar.header("📌 Event Setup")

# 📅 Month selection (prefixed for sorting consistency)
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

# 📆 Year input
year = st.sidebar.number_input(
    "Year",
    min_value=2000,
    max_value=2100,
    value=datetime.now().year,  # ⏳ Default = current year
)

# 🎉 Event name input
event_name = st.sidebar.text_input("Event Name")

# ⚠️ Stop execution if no event name
if not event_name:
    st.warning("⚠️ Enter an event name to continue.")
    st.stop()

# 🧼 Clean event name for file safety
event_name = event_name.replace(" ", "_")

# 📄 Generate file path
gift_file_path = get_gift_file_path(year, month, event_name)

# 📊 Load existing data
df = load_data(gift_file_path)


# -----------------------------
# ➕ Add Gift Section
# -----------------------------

st.sidebar.header("➕ Add Gift")

# 🎁 Gift details input
gift_name = st.sidebar.text_input("Gift Name")
given_by = st.sidebar.text_input("Given By")

# 🏷 Category based on price ranges
category = st.sidebar.selectbox(
    "Category (Price Range)",
    [
        "Category 1 (₹100-1000)",
        "Category 2 (₹1000-2000)",
        "Category 3 (₹2000-3000)",
    ],
)

# 💰 Approx price input
price_input = st.sidebar.text_input("Approx Price (₹)")

# 🛡 Validate price input
try:
    price = int(price_input) if price_input else 0
except:
    st.sidebar.error("⚠️ Enter valid price")
    price = 0

# ➕ Add gift button logic
if st.sidebar.button("Add Gift"):

    # 🆕 Create new entry
    new_row = {
        "Date": datetime.now().strftime("%Y-%m-%d %H:%M"),  # ⏱ Timestamp
        "Gift Name": gift_name,
        "Given By": given_by,
        "Category": category,
        "Approx Price": price,
    }

    # 🔗 Append to existing data
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

    # 💾 Save updated data
    save_data(df, gift_file_path)

    # ✅ Feedback
    st.sidebar.success("✅ Gift Added!")

    # 🔄 Refresh UI
    st.rerun()


# -----------------------------
# 📊 Summary Section
# -----------------------------

st.subheader(f"🎁 Gifts for {event_name}")

if df.empty:
    st.warning("⚠️ No gifts recorded yet.")
else:
    # 🔄 Ensure numeric values
    df["Approx Price"] = pd.to_numeric(df["Approx Price"], errors="coerce")

    # 💰 Total value calculation
    total_value = df["Approx Price"].sum()

    # 📌 Display total
    st.metric("💰 Total Gift Value", f"₹{total_value:.2f}")

    # 📋 Display full table
    st.dataframe(df, use_container_width=True)

    # -----------------------------
    # 📊 Category Breakdown
    # -----------------------------

    st.subheader("📊 Category Breakdown")

    # 📊 Group by category
    category_summary = df.groupby("Category")["Approx Price"].sum().reset_index()

    # 📋 Show grouped data
    st.dataframe(category_summary, use_container_width=True)


# -----------------------------
# 📁 File Info
# -----------------------------

# 📂 Show file path for transparency/debugging
st.info(f"📁 Gift File: {gift_file_path}")
