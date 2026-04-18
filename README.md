# 📘 SQF Active Certified Site Directory & Organizations Scraper

## 🧾 Project Overview

This project extracts, processes, and organizes data from the **SQF Public Directory**.

It focuses on two main datasets:

### 🔹 SQF Certified Site Directory (Active Certifications)

* Audit Name
* Certification Number
* Certification Status
* Expiration Date
* Additional certification details

### 🔹 SQF Organizations Data

* Organization ID
* Organization Name
* Address
* Related organization details

🔗 **Data Source:**
https://sqfi.compliancemetrix.com/rql/g/Public_Directory

---

## ⚙️ Project Structure

```
├── sqfActCer.py         # Extract active certified site directory data
├── sqf_cer.py           # Extract certification-related data
├── generate_excel.py    # Clean data & generate Excel output
├── db_config.py         # Database configuration
├── requirements.txt     # Python dependencies (optional)
└── README.md
```

---

## 🚀 Setup Instructions

### 1️⃣ Clone Repository

```bash
git clone https://github.com/Niraj1321/sqf-public-directory-scraper.git
cd sqf-scraper
```

---

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

If `requirements.txt` is not available, install manually:

```bash
pip install requests pandas mysql-connector-python openpyxl
```

---

### 3️⃣ Database Setup

Create a MySQL database:

```sql
CREATE DATABASE sqf_data;
```

Update your database credentials in:

```python
# db_config.py
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "your_password"
DB_NAME = "sqf_data"
```

---

## 🔐 Handling API Access (Headers & Cookies)

If you encounter a **406 Not Acceptable error**, update request headers.

### Steps:

1. Open the SQF Public Directory website
2. Open **Developer Tools → Network tab**
3. Find API request (e.g., `queue` or `find`)
4. Right-click → **Copy → Copy as cURL**
5. Extract and update:

   * Headers (especially cookies)
   * JSON payload (if required)

⚠️ These values must be updated in your Python scripts.

---

## ▶️ Running the Project

### Step 1: Extract Certification Data

```bash
python sqf_cer.py
```

### Step 2: Extract Active Certified Sites

```bash
python sqfActCer.py
```

---

## 📊 Generate Excel Output

After successful data extraction:

```bash
python generate_excel.py
```

### This script will:

* Read data from SQL tables
* Remove duplicates
* Clean and rename columns
* Export structured Excel files

---

## 📁 Output Files

* 📄 `SQF_Organizations_Data.xlsx`
* 📄 `SQF_Certifications_Data.xlsx`

---

## ⚠️ Important Notes

* Always keep headers and cookies updated
* Run scripts in correct sequence
* Ensure database tables exist before execution
* API behavior may change over time

---

## 🧠 Key Features

* Automated data extraction from API endpoints
* Handles authentication via headers & cookies
* Data cleaning and transformation pipeline
* Structured Excel output generation
* Modular and scalable code design

---

## 🛠️ Tech Stack

* Python
* Requests
* Pandas
* MySQL
* OpenPyXL

---

## 📌 Use Cases

* Certification data analysis
* Compliance tracking
* Market research
* Business intelligence

---

## 🐞 Troubleshooting

### Issue: 406 Error

✔ Update headers and cookies from browser

### Issue: Database Connection Failed

✔ Verify credentials in `db_config.py`

### Issue: Empty Data

✔ Check API response and payload

---

## 🔮 Future Improvements

* Add proxy rotation support
* Automate cookie/session refresh
* Add logging system
* Deploy as scheduled pipeline

---

## 👨‍💻 Author

**Niraj Chauhan**
Web Scraping & Data Automation Specialist

📧 mrchauhan783@gmail.com
📍 Ahmedabad, India

---

