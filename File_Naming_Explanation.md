# 📁 File Naming Explanation

This document explains the logic behind the **month-wise file naming system** used in the budget and why it’s designed this way.

---

## 🧩 The Naming Structure

```python
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
```

Each file is named using the format:

```
MM_Month_YYYY.csv
```

### ✅ Example:

```
01_January_2026.csv
02_February_2026.csv
```

---

## 🧠 Why This Format Is Used

### 1️⃣ Ensures Correct Sorting

File systems sort files **alphabetically (lexicographically)**, not chronologically.

Without numbering:

```
April
August
December
February
```

❌ Incorrect order

With numbering:

```
01_January
02_February
03_March
...
12_December
```

✅ Perfect chronological order

---

### 2️⃣ Works Seamlessly with Code

Your merging logic relies on:

```python
for file in sorted(os.listdir(year_path)):
```

Because files are already numbered:

* No need for custom sorting
* No need for date parsing
* Everything stays simple and efficient

---

### 3️⃣ Prevents Data Chaos

Using a consistent naming convention avoids:

* Duplicate month files (`January` vs `01_January`)
* Misplaced data
* Confusing file structures over time

---

## 📂 Folder Structure

```
data/
├── 2026/
│   ├── 01_January_2026.csv
│   ├── 02_February_2026.csv
│   ├── ...
├── 2027/
```

Each year contains all its monthly data, neatly organized.

---

> [!TIP]
> Always use **two-digit numbering (01–12)**.
> Using `1_January` instead of `01_January` will break sorting.

---

> [!NOTE]
> The underscore `_` is used instead of spaces to:
>
> * Avoid file path issues
> * Keep naming consistent across systems

---

> [!IMPORTANT]
> Stick to this format throughout the budget.
> Even small inconsistencies can lead to duplicate files and messy merges later.

---

> [!WARNING]
> Avoid mixing formats like:
>
> ```
> January_2026.csv
> 01-January_2026.csv
> ```
>
> This will break ordering and may split your data unintentionally.

---

## 🧾 Final Takeaway

This naming system is:

* ✔ Simple
* ✔ Scalable
* ✔ Code-friendly
* ✔ Error-resistant

It ensures your data stays **clean, sortable, and reliable** as your budget grows.