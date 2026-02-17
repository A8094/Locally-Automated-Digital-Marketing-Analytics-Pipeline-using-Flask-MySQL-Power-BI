# Locally-Automated-Digital-Marketing-Analytics-Pipeline-using-Flask-MySQL-Power-BI
## 🏗️ Project Architecture & Workflow

This project follows a **local end-to-end data automation pipeline**, where digital marketing data flows from a web form to analytics dashboards **without using any cloud services** ☁️❌.

---

## 🔁 Step-by-Step Workflow 🚀

### 1️⃣ User Interaction (Flask Web Form) 🧑‍💻
- User accesses the application via a **local Flask server** 🌐  
- A structured form collects:
  - Campaign details 📋  
  - Marketing channel information 📣  
  - Performance inputs (impressions, clicks, conversions, ad spend) 📊  

---

### 2️⃣ Backend Processing (Flask Logic) ⚙️
- On form submission:
  - Flask captures the input data 🧠  
  - Key marketing metrics are calculated automatically:
    - CPC, CPM, CTR 💰  
    - Conversion Rate & ROI 📈  
    - Engagement Ratio & Cost Efficiency 🔍  
  - Date-based fields like **week number and month** are derived 🗓️  

---

### 3️⃣ Thread-Safe CSV Automation 📄🔒
- Processed data is pushed into a **queue system** 📥  
- A background worker thread:
  - Writes data safely to the CSV file ✍️  
  - Handles Excel file-lock issues gracefully 🛑  
- This CSV acts as the **primary analytics data source** 📊  

---

### 4️⃣ MySQL Database Synchronization 🗄️
- A separate background thread monitors the CSV continuously 👀  
- For every new campaign record:
  - Data is normalized 🔄  
  - Inserted into the **MySQL database**  
  - Duplicate inserts are prevented using campaign ID validation ✅  
- Enables **SQL-based analysis and reporting** 🔍  

---

### 5️⃣ Power BI Integration (CSV Sync) 📊
- The updated CSV is automatically synced to a **OneDrive folder** ☁️  
- Power BI connects to this CSV as a data source 🔗  
- On refresh, dashboards update with the latest campaign data 🔄  

---

## 🔐 Key Design Features ⭐
- ✔ Fully local execution 🖥️  
- ✔ Thread-safe file handling 🔒  
- ✔ Duplicate SQL insert prevention 🚫  
- ✔ Automatic metric computation 🤖  
- ✔ Power BI–ready data structure 📊  
- ✔ Real-world analytics simulation 🧪  

### 🔗 Data Flow Architecture

```

                 CSV (MySQL Load) 📄 → MySQL 🗄️
              ⭧
Local Flask 🖥️
              🡖
                CSV (Power BI Source) 📄 → Power BI 📊

```
---


### ‼️ Before Running the Code – Follow the Given Steps ‼️ 

### Step 1️⃣:
**🌟🌟🌟🌟🌟 DOWNLOAD THE GIVEN CSV FILES AND STORE THEM IN THE BELOW MENTIONED PATHS 👇🏻👇🏻👇🏻👇🏻👇🏻👇🏻**
```
📂 C:\
 └── MarketingDat\
     └── DIGITAL_MARKETING_AD_PERFORMANCE_DATA.csv
         -------- DOWNLOADED CSV FILE

📂 C:\
 └── Users\
     └── <your-username>\
         └── OneDrive\
             └── Documents\
                 └── digitalmarketing dataset\
                     └── powerbi_digital_marketing_data.csv
                         -------- DOWNLOADED CSV FILE

```
### Step 2️⃣:
**🌟🌟🌟 MY SQL DATABASE AND TABLE SETUP 🌟🌟🌟🌟🌟**

FOR DATABASE:
```
CREATE DATABASE digital_marketing;
USE digital_marketing;
```
FOR TABLE:
```
IMPORT CSV FILE FROM:
📂 C:\
 └── MarketingDat\
     └── DIGITAL_MARKETING_AD_PERFORMANCE_DATA.csv -------- DOWNLOADED CSV FILE
```

### Step 3️⃣:
**🌟🌟🌟🌟🌟 INSTALL FLASK AND PYMYSQL IN TERMINAL🌟🌟🌟🌟🌟**
```
pip install flask pymysql
```
----
### Step 4️⃣:
**🌟🌟🌟🌟🌟 COPY & PASTE THE GIVEN CODE AND SAVE FILES AS SHOWN BELOW 👇🏻👇🏻👇🏻🌟🌟🌟🌟🌟**

**I.PASTE THE MAIN CODE AND SAVE IN:**

```
📂 C:\Users\YOUR-USERNAME\OneDrive\Documents\digital_marketing analysis\
 └── combined_form.py
```

**II.PASTE THE HTML CODE FOR DATA ENTRY AND SAVE IN:**

```
📂 C:\Users\YOUR-USERNAME\OneDrive\Documents\digital_marketing analysis\templates\
 └── form.html
```

**III.PASTE THE HTML CODE FOR CONFIRMATION PAGE AND SAVE IN:**

```
📂 C:\Users\YOUR-USERNAME\OneDrive\Documents\digital_marketing analysis\templates\
 └── filled_form.html
```

### Step 5️⃣:

🌟🌟🌟🌟🌟Updating CSV Path in Power BI (One-Time Setup)🌟🌟🌟🌟🌟

1. Open the `.pbix` file in Power BI Desktop
2. Go to **Home → Transform data → Data source settings**
3. Select the CSV source and click **Change Source**
4. Browse and select:
   `powerbi_digital_marketing_data.csv`
5. Click **OK → Close & Apply**
6. Click **Refresh**


### Step 6️⃣:
🌟🌟🌟🌟🌟 UPDATE THE CODE 🌟🌟🌟🌟🌟

**I.IN MYSQL CONNECTION SECTION:**
```
db = pymysql.connect(
    host="localhost",
    user="root",
  ‼️password="YOUR_MYSQL_PASSWORD",   ‼️ UPDATE THIS LINE‼️
    database="digital_marketing",
    autocommit=False
)
cursor = db.cursor()
```
**II.IN FILE PATHS SECTION:**
```
   CSV_FILE = r"C:\MarketingDat\DIGITAL_MARKETING_AD_PERFORMANCE_DATA.csv"
‼️ ONEDRIVE_CSV = r"C:\Users\‼️YOUR-USERNAME‼️\OneDrive\Documents\digitalmarketing dataset\powerbi_digital_marketing_data.csv" ‼️ UPDATE THIS LINE‼️
   queue = Queue()
   lock = Lock()
```

### Step 7️⃣:

```
RUN THE PYTHON FILE-python combined_form.py

A LOCAL URL WILL APPEAR IN TERMINAL (Example:
http://127.0.0.1:5000)

PRESS CTRL + CLICK ON THE LINK TO OPEN THE BROWSER
AND START FILLING THE FORM
```

**################ ✅ IMPORTANT NOTES ################**

- This project runs ONLY on a local system
- Flask must be running to access the application
- One Local Flask application writes to TWO CSV files
- One CSV is loaded into MySQL for SQL analysis
- One CSV is used as the data source for Power BI
