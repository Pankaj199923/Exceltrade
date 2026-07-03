# Live Excel Dashboard — Setup Guide

Ye system 3 parts me kaam karta hai:

```
[Excel file on your laptop] --> [excel_watcher.py] --> [server.py on internet] --> [dashboard.html in any browser]
```

Excel save karo → watcher detect karega → server ko bhejega → sab open browsers me turant update ho jaayega.

---

## Step 1: Server ko internet par deploy karo

Server (`server.py` + `templates/dashboard.html`) ko kisi free hosting par daalna hoga taaki
"internet par instantly update" ho sake. Sabse aasaan options:

### Option A — Render.com (recommended, free tier)
1. Is poore `excel-live-dashboard` folder ko GitHub repo me push karo
2. Render.com par "New Web Service" banao, apna GitHub repo connect karo
3. Build command: `pip install -r requirements.txt`
4. Start command: `python server.py`
5. Environment variable add karo: `EXCEL_DASHBOARD_KEY = <apni-strong-secret-key>`
6. Deploy hone ke baad tumhe URL milega jaise: `https://your-app.onrender.com`

### Option B — Railway.app
Same process — repo connect karo, ye auto-detect kar lega Python app.

### Option C — Quick test (bina deploy kiye, sirf demo ke liye)
Apne laptop par hi `python server.py` chalao, phir `ngrok` se public URL banao:
```
ngrok http 5000
```
(Ye temporary hai, laptop band hote hi link expire ho jaayega — production ke liye Option A/B use karo)

---

## Step 2: Apne laptop par watcher setup karo

```bash
pip install -r requirements.txt
```

`excel_watcher.py` file kholo aur CONFIG section me ye values badlo:

```python
EXCEL_FILE_PATH = r"C:\Users\YourName\Documents\MySheet.xlsx"   # apni file ka path
SERVER_URL = "https://your-app.onrender.com/update"              # Step 1 wala URL
API_KEY = "<apni-strong-secret-key>"                              # server wali key se match ho
```

Phir chalao:
```bash
python excel_watcher.py
```

Ye background me chalti rahegi. Jab bhi Excel save karoge, terminal me
`[OK] Sent X rows to server` dikhega.

**Hamesha chalte rehne ke liye (laptop restart ke baad bhi):**
- Windows: Task Scheduler me is script ko "on startup" add kar do
- Ya `pythonw excel_watcher.py` se bina console window ke background me chalao

---

## Step 3: Dashboard dekho

Server ka URL kisi bhi browser me kholo:
```
https://your-app.onrender.com
```

Bas — ab jahan se bhi ye link khologe, Excel update hote hi wahan live dikhega.
Koi bhi jisko ye link doge, unko bhi real-time updates milenge (koi refresh nahi chahiye).

---

## Important notes

- **Security**: `API_KEY` / `EXCEL_DASHBOARD_KEY` ko strong random string rakho, kisi ko mat batao —
  ye endpoint ko sirf tumhare watcher se update hone deta hai.
- **Formulas**: `data_only=True` set hai, isliye formula ka calculated result bhejega (raw formula nahi) —
  isliye Excel me file open karke ek baar save zaroor karo taaki formulas calculate ho chuke hon.
- **Large sheets**: Agar sheet bahut badi hai (10,000+ rows), to socket payload bada ho sakta hai —
  zaroorat pade to sirf top N rows ya specific range bhejne ka logic add kar sakte hain.
- **Multiple sheets**: Abhi ek sheet track hoti hai. `SHEET_NAME` set karke specific sheet choose kar sakte ho.
