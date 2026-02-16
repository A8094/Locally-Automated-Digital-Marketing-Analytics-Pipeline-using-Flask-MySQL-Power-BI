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

```text

                 CSV (MySQL Load) 📄 → MySQL 🗄️
              ⭧
Local Flask 🖥️
              🡖
                CSV (Power BI Source) 📄 → Power BI 📊
