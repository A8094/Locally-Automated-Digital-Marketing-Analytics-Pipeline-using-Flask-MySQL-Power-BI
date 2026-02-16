

################ ‼️ Before running the code follow the given steps ‼️ #######################

### step1️⃣:
##               🌟🌟🌟🌟🌟 DOWNLOAD THE GIVEN CSV FILE AND STORE THE FILES IN BELOW MENTIONED RESPECTIVE PATH👇🏻👇🏻👇🏻👇🏻👇🏻👇🏻

#📂C:\
# └── MarketingDat\
 #    └── DIGITAL_MARKETING_AD_PERFORMANCE_DATA.csv -------- DOWNLOADED CSV FILE

#📂C:\
# └── Users\
#    └── <your-username>\
#         └── OneDrive\
#            └── Documents\
#               └── digitalmarketing dataset\
#                   └── powerbi_digital_marketing_data.csv ----------- DOWNLOADED CSV FILE
#


### STEP 2️⃣:
###                                           🌟🌟🌟MY SQL DATABASE AND TABLE SETUP🌟🌟🌟🌟🌟

####### FOR DATABASE : CREATE DATABASE digital_marketing;
#                      USE digital_marketing;

#### FOR TABLE : IMPORT CSV FILE FROM 📂C:\
#                                           └── MarketingDat\
 #                                                          └── DIGITAL_MARKETING_AD_PERFORMANCE_DATA.csv -------- DOWNLOADED CSV FILE
 
 
 
 
 #STEP 3️⃣:👇🏻👇🏻👇🏻👇🏻👇🏻👇🏻👇🏻👇🏻👇🏻👇🏻👇🏻👇🏻👇🏻
 # 🌟🌟🌟🌟🌟INSTALL the  flask  AND pymysql in terminal





## STEP 4️⃣:
###                                  🌟🌟🌟🌟🌟 COPY PASTE THE GIVEN VS CODE AND SAVE THE FILE IN MENTIONED WAY 👇🏻👇🏻👇🏻

#   PASTE THE MAIN CODE AND SAVE  IN GIVEN DIRECTORY: 📂📂 "C:\Users\YOUR-USER_NAME\OneDrive\Documents\digital_marketing analysis\combined_form.py" 

# PASTE THE HTML CODE FOR DATA ENTRY AND SAVE  IN GIVEN DIRECTORY:📂📂 "C:\Users\YOUR-USER_NAME\OneDrive\Documents\digital_marketing analysis\templates\form.html"

# PASTE THE HTML CODE FOR CONFIRMATION PAGE AND SAVE  IN GIVEN DIRECTORY:📂📂 "C:\Users\YOUR-USER_NAME\OneDrive\Documents\digital_marketing analysis\templates\filled_form.html"



### step 5️⃣ :
#                                                 🌟🌟🌟🌟🌟  Update the code 🌟🌟🌟🌟🌟
 

# # in ====================== MYSQL CONNECTION ======================
# #       db = pymysql.connect(
#            host="localhost",
#            user="root",
#  📝📝     password="YOUR_MYSQL_PASSWORD", ‼️‼️‼️‼️‼️‼️
#           database="digital_marketing",
#             autocommit=False
#             )
#            cursor = db.cursor()

# in # ====================== FILE PATHS ======================
 
# CSV_FILE = r"C:\MarketingDat\DIGITAL_MARKETING_AD_PERFORMANCE_DATA.csv"           
# 📝📝 📝📝 📝📝 ONEDRIVE_CSV = r"c:\users\‼️‼️‼️‼️‼️‼️your user filename ‼️‼️‼️‼️‼️‼️ \onedrive\documents\digitalmarketing dataset\powerbi_digital_marketing_data.csv"    
# queue = Queue()
# lock = Lock()


 #step 6️⃣ :
 # then run combined.form and give ctrl click to open browser (eg:https://127.0.0.1.5000) which will be in terminal  to fill the form 
 
 
 








from flask import Flask, render_template, request, redirect, url_for
from queue import Queue
from threading import Thread, Lock
import csv, os, time, shutil
from datetime import datetime
import pymysql

app = Flask(__name__)

# ====================== FILE PATHS ======================
CSV_FILE = r"C:\MarketingDat\DIGITAL_MARKETING_AD_PERFORMANCE_DATA.csv"
ONEDRIVE_CSV = r"c:\users\ajeetha\onedrive\documents\digitalmarketing dataset\powerbi_digital_marketing_data.csv"

queue = Queue()
lock = Lock()

# ====================== METRIC CALCULATIONS ======================
def calculate_metrics(impressions, clicks, conversions, ad_spend):
    impressions = float(impressions)
    clicks = float(clicks)
    conversions = float(conversions)
    ad_spend = float(ad_spend)

    cpc = ad_spend / clicks if clicks > 0 else 0
    cpm = (ad_spend / impressions) * 1000 if impressions > 0 else 0
    ctr = clicks / impressions if impressions > 0 else 0
    cr = conversions / clicks if clicks > 0 else 0
    cpc_eff = ctr / cpc if cpc > 0 else 0
    roi = conversions / ad_spend if ad_spend > 0 else 0
    click_ratio = clicks / conversions if conversions > 0 else 0
    qs = (ctr + cr) * 10
    eng_ratio = clicks / ad_spend if ad_spend > 0 else 0
    cost_eff = ad_spend / conversions if conversions > 0 else 0

    return (
        round(ad_spend, 2), round(cpc, 2), round(cpm, 2),
        round(ctr, 4), round(cr, 4), round(cpc_eff, 4),
        round(roi, 4), round(click_ratio, 4), round(qs, 2),
        round(eng_ratio, 4), round(cost_eff, 2)
    )

# ====================== CSV WRITER ======================
def get_next_campaign_id():
    if not os.path.exists(CSV_FILE):
        return 1
    with open(CSV_FILE, "r", encoding="latin-1") as f:
        rows = list(csv.reader(f))
        return 1 if len(rows) <= 1 else int(rows[-1][0]) + 1

def csv_worker():
    while True:
        row = queue.get()
        while True:
            try:
                with lock:
                    with open(CSV_FILE, "a", newline="", encoding="latin-1") as f:
                        csv.writer(f).writerow(row)
                print("CSV UPDATED:", row[0])
                break
            except PermissionError:
                print("Excel open — retrying...")
                time.sleep(1)
        queue.task_done()

Thread(target=csv_worker, daemon=True).start()

# ====================== MYSQL CONNECTION ======================
db = pymysql.connect(
    host="localhost",
    user="root",
    password="Ajeetha_rengasamy@2001",
    database="digital_marketing",
    autocommit=False
)
cursor = db.cursor()

# ====================== NORMALIZATION ======================
def normalize_csv_row(r):
    return (
        int(r[0]), r[1].strip(), r[2].strip(), r[3].strip(), r[4].strip(),
        r[5].strip(), r[6].strip(), int(r[7]), int(r[8]), int(r[9]),
        float(r[10]), r[11].strip(), r[12].strip(), r[13].strip(),
        float(r[14]), float(r[15]), float(r[16]), float(r[17]),
        float(r[18]), float(r[19]), float(r[20]), float(r[21]),
        float(r[22]), float(r[23]), int(r[24]), int(r[25])
    )

# ====================== SYNC CSV → ONEDRIVE ======================
def sync_csv_to_onedrive():
    for _ in range(3):
        try:
            shutil.copyfile(CSV_FILE, ONEDRIVE_CSV)
            print("POWER BI CSV UPDATED")
            return
        except PermissionError:
            time.sleep(1)

# ====================== AUTO SYNC (FIXED) ======================
def auto_sync():
    print("SQL + POWER BI SYNC THREAD RUNNING")
    last_campaign_id = None

    while True:
        try:
            if not os.path.exists(CSV_FILE):
                time.sleep(0.3)
                continue

            with open(CSV_FILE, "r", encoding="latin-1") as f:
                rows = list(csv.reader(f))[1:]

            if not rows:
                time.sleep(0.3)
                continue

            r = rows[-1]
            cid = int(r[0])

            # 🔒 CRITICAL FIX — prevent double insert
            if cid == last_campaign_id:
                time.sleep(0.3)
                continue

            last_campaign_id = cid
            csv_norm = normalize_csv_row(r)

            db.ping(reconnect=True)

            cursor.execute(
                "SELECT campaign_id FROM digital_marketing_ad_performance_data WHERE campaign_id=%s",
                (cid,)
            )

            if not cursor.fetchone():
                cursor.execute("""
                    INSERT INTO digital_marketing_ad_performance_data VALUES (
                        %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                        %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s
                    )
                """, csv_norm)
                db.commit()
                print("SQL INSERT:", cid)
            else:
                print("SQL ROW EXISTS:", cid)

            sync_csv_to_onedrive()

        except Exception as e:
            print("AUTO SYNC ERROR:", e)

        time.sleep(0.3)

Thread(target=auto_sync, daemon=True).start()

# ====================== FORM ROUTE ======================
@app.route("/", methods=["GET", "POST"])
def form_page():

    campaign_companies = [
        "Adidas","Ajio","Alibaba","AliExpress","Amazon","Apple","BigBasket","Blinkit",
        "Dell","eBay","Etsy","Flipkart","Gap","H&M","HP","Lenovo","Levis","Loreal",
        "MAC Cosmetics","Marks & Spencer","Maybelline","Meesho","Meesho App","Myntra",
        "Nike","Nykaa","Ola","OnePlus","Paytm","PhonePe","Puma","Rakuten","Realme",
        "Samsung","Sephora","Shopee","Sony","Spotify","Swiggy","Target","Tata Cliq",
        "The Body Shop","Uber","Uniqlo","Vivo","Walmart","Xiaomi","Zara","Zomato"
    ]

    campaign_names = [
        "App Install","App Install Drive","Back to School Promo","Black Friday",
        "Black Friday Campaign","Brand Awareness Push","Cyber Monday Deals",
        "Diwali Mega Offers","End of Season Sale","Festival Discount Drive",
        "Flash Sale Weekend","Holiday Sale Blast","Lead Generation Boost",
        "New Product Launch","Spring Collection Launch","Summer Clearance","Winter Deals"
    ]

    campaign_types = [
        "App Installs","Awareness","Brand Building","Conversions","Engagement",
        "Leads","New Product Launch","Remarketing","Sales","Traffic"
    ]

    marketing_channels = ["Facebook", "Google", "Instagram", "LinkedIn", "Pinterest", "YouTube"]
    ad_formats = ["Carousel", "Image", "Story", "Text", "Video"]
    device_types = ["Desktop", "Mobile", "Tablet"]
    countries = ["Australia", "Canada", "Germany", "India", "UK", "USA"]
    audience_segments = ["Cold Audience", "High Intent", "Lookalike Audience", "New Users", "Returning Users"]

    # ================= POST =================
    if request.method == "POST":
        data = request.form  # ✅ defined ONLY for POST

        next_id = get_next_campaign_id()

        d = datetime.strptime(data["date"], "%Y-%m-%d")
        week = d.strftime("%U")
        month = d.month

        (spend, cpc, cpm, ctr, cr, ceff, roi,
         click_ratio, qs, eng_ratio, cost_eff) = calculate_metrics(
            data["impressions"],
            data["clicks"],
            data["conversions"],
            data["ad_spend"]
        )

        row = [
            next_id,
            data["campaign_company"],
            data["campaign_name"],
            data["campaign_type"],
            data["marketing_channel"],
            data["ad_format"],
            data["date"],
            data["impressions"],
            data["clicks"],
            data["conversions"],
            spend,
            data["device_type"],
            data["country"],
            data["audience_segment"],
            cpc, cpm, ctr, cr, ceff, roi, click_ratio,
            qs, eng_ratio, cost_eff,
            week, month
        ]

        queue.put(row)

        # ✅ SHOW FILLED FORM PAGE
        return render_template("filled_form.html", data=data)

    # ================= GET =================
    return render_template(
        "form.html",
        campaign_companies=campaign_companies,
        campaign_names=campaign_names,
        campaign_types=campaign_types,
        marketing_channels=marketing_channels,
        ad_formats=ad_formats,
        device_types=device_types,
        countries=countries,
        audience_segments=audience_segments
    )


# ====================== RUN APP ======================
if __name__ == "__main__":
    app.run(debug=False, threaded=True, use_reloader=False)
