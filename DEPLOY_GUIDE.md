# 🚀 Deploy Guide — AI Prompt Playbook lên Streamlit Cloud

Thời gian ước tính: **20–30 phút** (lần đầu), 5 phút cho lần sau.

---

## Cấu trúc file cần có

```
ai-prompt-playbook/          ← tên repo GitHub
├── app.py                   ← Streamlit app chính
├── cheatsheet.html          ← HTML cheatsheet (giữ nguyên)
├── requirements.txt         ← dependencies
├── .gitignore               ← exclude secrets
└── .streamlit/
    └── secrets.toml         ← KHÔNG commit, chỉ add trên Streamlit Cloud
```

---

## BƯỚC 1 — Tạo Google Sheet để nhận feedback

1. Vào [sheets.google.com](https://sheets.google.com) → **New spreadsheet**
2. Đặt tên: `AI Prompt Feedback`
3. **Tạo header ở Row 1** (gõ chính xác vào các ô A1→G1):

   | A | B | C | D | E | F | G |
   |---|---|---|---|---|---|---|
   | Timestamp | Submitter | Template | Platform | Rating | Useful | Improve |

4. Copy **Sheet ID** từ URL:
   `docs.google.com/spreadsheets/d/`**`1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgVE2upms`**`/edit`
   → Lưu lại, dùng ở Bước 3.

---

## BƯỚC 2 — Tạo Google Cloud Service Account

> Service Account là "bot account" để app đọc/ghi Google Sheet mà không cần login.

### 2a. Tạo project trên Google Cloud

1. Vào [console.cloud.google.com](https://console.cloud.google.com)
2. Click **Select a project** → **New Project**
3. Đặt tên: `ai-prompt-playbook` → **Create**

### 2b. Bật Google Sheets API

1. Menu trái → **APIs & Services** → **Library**
2. Search: `Google Sheets API` → Click → **Enable**
3. Search: `Google Drive API` → Click → **Enable**

### 2c. Tạo Service Account

1. Menu trái → **IAM & Admin** → **Service Accounts**
2. **+ Create Service Account**
3. Name: `streamlit-sheets-writer` → **Create and Continue** → **Done**

### 2d. Tạo JSON key

1. Click vào service account vừa tạo
2. Tab **Keys** → **Add Key** → **Create new key** → **JSON** → **Create**
3. File JSON tự download về máy — **giữ file này an toàn, không share**

### 2e. Share Google Sheet cho Service Account

1. Mở file JSON vừa download, copy giá trị `client_email`
   (dạng: `streamlit-sheets-writer@your-project.iam.gserviceaccount.com`)
2. Vào Google Sheet → **Share** → paste email → Role: **Editor** → **Send**

---

## BƯỚC 3 — Push code lên GitHub

### 3a. Tạo GitHub repo

1. Vào [github.com](https://github.com) → **New repository**
2. Name: `ai-prompt-playbook`
3. **Private** (khuyến nghị cho nội bộ) → **Create repository**

### 3b. Upload files

Cách đơn giản nhất (không cần git command):

1. Trên trang repo → **uploading an existing file**
2. Upload tất cả các file:
   - `app.py`
   - `cheatsheet.html`
   - `requirements.txt`
   - `.gitignore`
   
   > ⚠️ **KHÔNG upload** file `secrets.toml` — sẽ config trực tiếp trên Streamlit Cloud

3. Commit message: `Initial deploy` → **Commit changes**

---

## BƯỚC 4 — Deploy lên Streamlit Community Cloud

1. Vào [share.streamlit.io](https://share.streamlit.io) → **Sign in with GitHub**
2. **New app**
3. Điền thông tin:
   - **Repository**: `your-username/ai-prompt-playbook`
   - **Branch**: `main`
   - **Main file path**: `app.py`
4. Click **Advanced settings** → tab **Secrets**
5. Paste nội dung sau (thay bằng giá trị thật của bạn):

```toml
google_sheet_id = "PASTE_SHEET_ID_TỪ_BƯỚC_1"

[gcp_service_account]
type = "service_account"
project_id = "your-project-id"
private_key_id = "abc123..."
private_key = "-----BEGIN RSA PRIVATE KEY-----\nMIIEo...\n-----END RSA PRIVATE KEY-----\n"
client_email = "streamlit-sheets-writer@your-project.iam.gserviceaccount.com"
client_id = "123456789"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/streamlit-sheets-writer%40your-project.iam.gserviceaccount.com"
```

> Tất cả giá trị lấy từ file JSON download ở Bước 2d.
> `private_key`: copy nguyên, giữ `\n` trong chuỗi.

6. **Save** → **Deploy!**
7. Chờ ~1-2 phút → app live tại URL dạng:
   `https://your-username-ai-prompt-playbook-app-xxxx.streamlit.app`

---

## BƯỚC 5 — Share với team

Copy URL và gửi cho team. Không cần account để xem.

Nếu muốn **giới hạn chỉ team xem** (optional):
- Streamlit Cloud → App → **Settings** → **Sharing**
- Chọn **"Only specific people"** → Add email của từng thành viên

---

## Troubleshooting

| Lỗi | Nguyên nhân | Fix |
|-----|------------|-----|
| `ModuleNotFoundError: gspread` | requirements.txt chưa đúng | Check file, redeploy |
| `google.auth.exceptions.DefaultCredentialsError` | Secrets chưa đúng format | Check `private_key` có `\n` không |
| `gspread.exceptions.SpreadsheetNotFound` | Sheet chưa share cho service account | Bước 2e: share email SA |
| Cheatsheet không load | `cheatsheet.html` chưa upload | Upload file lên GitHub |
| Feedback ghi nhưng không thấy trong Sheet | Header row sai | Check Bước 1: phải có đúng 7 cột header |

---

## Update app sau này

Mỗi khi cần update (thêm template, sửa prompt):
1. Chỉnh sửa `cheatsheet.html` hoặc `app.py` locally
2. Upload file mới lên GitHub (replace file cũ)
3. Streamlit Cloud tự động redeploy trong ~1 phút

---

## Cấu trúc feedback trong Google Sheet

Sau khi có feedback, Sheet sẽ có dạng:

| Timestamp | Submitter | Template | Platform | Rating | Useful | Improve |
|-----------|-----------|----------|----------|--------|--------|---------|
| 2025-01-15 09:30:00 | Nguyen Van A | 1 — Risk Report | Claude | 5 | System prompt chính xác | Thêm template DCF |
| 2025-01-16 14:00:00 | DA Team | 5 — EDA | ChatGPT | 4 | User prompts hay | Thiếu anomaly viz |
