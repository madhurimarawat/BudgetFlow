# 🎉 Event Expense Tracking

This section explains how to handle **large, one-time events** (like Weddings, Birthdays, Trips, etc.) without cluttering your main monthly files.

---

## 🧩 The Idea

Regular monthly files are great for day-to-day tracking, but events like:

* 💍 Marriage
* 🎂 Birthday
* ✈️ Trip / Function

often include **many categories and subcategories**:

* Decoration 🎀
* Food 🍽️
* Venue 🏛️
* Gifts 🎁
* Travel 🚗

👉 Putting all of this directly into the monthly file can make it messy and hard to analyze.

---

## 📁 Solution: Separate Event File

For each event, create a **dedicated file** using this format:

```
MM_Month_YYYY_EventName.csv
```

### ✅ Examples:

```
01_January_2026_marriage.csv
03_March_2026_birthday.csv
```

---

## 🧠 How It Works

### 1️⃣ Track Everything in Detail (Event File)

Inside the event file, you can freely add:

* Multiple categories
* Multiple subcategories
* Detailed notes

👉 This file acts as a **deep breakdown** of the event expenses.

---

### 2️⃣ Calculate Total Expense

Once the event is completed:

* Calculate the **total amount spent** from the event file

---

### 3️⃣ Add Summary to Monthly File

Now, in your main monthly file:

```
01_January_2026.csv
```

Add **one single entry**:

```
Category: Event 🎉
Subcategory: Marriage
Amount: <total event cost>
```

---

## 🎯 Why This Approach Is Powerful

### ✔ Clean Monthly Data

Monthly file stays simple and readable
(no 50+ rows from one event)

---

### ✔ Detailed Tracking

Event file keeps **full breakdown** for analysis

---

### ✔ Best of Both Worlds

* Summary in dashboard 📊
* Details when needed 🔍

---

## 📂 Final Structure Example

```
data/
├── 2026/
│   ├── 01_January_2026.csv
│   ├── 01_January_2026_Marriage.csv
│   ├── 02_February_2026.csv
```

---

> [!TIP]
> Use clear event names like:
>
> * `Marriage`
> * `Birthday`
> * `Trip_goa`
>   This makes files easy to identify later.

---

> [!NOTE]
> Event files are **not required to follow strict category rules**.
> You can customize them freely based on the event.

---

> [!IMPORTANT]
> Always ensure the **total from the event file is added to the monthly file**.
> Otherwise, your overall budget summary will be incorrect.

---

> [!WARNING]
> Do NOT mix event entries directly into the monthly file in bulk.
> This defeats the purpose and makes analysis harder.

---

## 🧾 Final Takeaway

This system gives you:

* 📊 Clean dashboards
* 🧾 Detailed records
* ⚡ Scalable structure

👉 Track **big events separately**, then summarize them into your main monthly flow.

Perfect balance between **clarity and control**.