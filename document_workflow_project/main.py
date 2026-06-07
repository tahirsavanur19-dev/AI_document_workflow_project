import os
import shutil
import re
import joblib

from fastapi import FastAPI, Request, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from reportlab.lib.pagesizes import letter
from fastapi.responses import FileResponse
from reportlab.pdfgen import canvas
from database import SessionLocal, ScanResult
import datetime
from fastapi.responses import RedirectResponse

from PIL import Image
import pytesseract
from difflib import SequenceMatcher

# ✅ Database imports
from database import SessionLocal, ScanResult

# -----------------------------
# App Setup
# -----------------------------

pytesseract.pytesseract.tesseract_cmd = r"C:\Users\Tahir savanur\tesseract.exe"

app = FastAPI()

ml_model = joblib.load("fraud_model.pkl")

os.makedirs("uploads", exist_ok=True)

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/logout")
def logout():
    return RedirectResponse(url="/")

# -----------------------------
# Fraud Keywords
# -----------------------------

fraud_keywords = [
    "lottery", "win", "urgent", "bank",
    "account", "transfer", "prize",
    "claim", "free", "investment",
    "cash", "scratch"
]

# -----------------------------
# Routes
# -----------------------------

@app.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):

    db = SessionLocal()

    scans = db.query(ScanResult).all()

    fraud_count = db.query(ScanResult).filter(
        ScanResult.risk_level.contains("High")
    ).count()

    suspicious_count = db.query(ScanResult).filter(
        ScanResult.risk_level.contains("Suspicious")
    ).count()

    safe_count = db.query(ScanResult).filter(
        ScanResult.risk_level.contains("Safe")
    ).count()

    db.close()

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "fraud_count": fraud_count,
            "suspicious_count": suspicious_count,
            "safe_count": safe_count
        }
    )

@app.get("/analytics", response_class=HTMLResponse)
async def analytics_page(request: Request):

    db = SessionLocal()

    scans = db.query(ScanResult).all()

    fraud_count = 0
    suspicious_count = 0
    safe_count = 0

    keyword_counts = {}

    for scan in scans:

        if "High" in scan.risk_level:
            fraud_count += 1

        elif "Suspicious" in scan.risk_level:
            suspicious_count += 1

        else:
            safe_count += 1

        if scan.matched_keywords:
            keywords = scan.matched_keywords.split(",")

            for k in keywords:
                k = k.strip()

                if k not in keyword_counts:
                    keyword_counts[k] = 1
                else:
                    keyword_counts[k] += 1

    db.close()

    keyword_labels = list(keyword_counts.keys())
    keyword_values = list(keyword_counts.values())

    return templates.TemplateResponse(
        "analytics.html",
        {
            "request": request,
            "fraud_count": fraud_count,
            "suspicious_count": suspicious_count,
            "safe_count": safe_count,
            "keyword_labels": keyword_labels,
            "keyword_values": keyword_values
        }
    )

@app.get("/history", response_class=HTMLResponse)
async def history(request: Request):

    db = SessionLocal()
    scans = db.query(ScanResult).order_by(ScanResult.id.desc()).all()
    db.close()

    return templates.TemplateResponse(
        "history.html",
        {
            "request": request,
            "scans": scans
        }
    )

@app.get("/download_report")
def download_report():

    db = SessionLocal()

    # Last scan result
    last_scan = db.query(ScanResult).order_by(ScanResult.id.desc()).first()

    db.close()

    file_path = "fraud_report.pdf"

    c = canvas.Canvas(file_path)

    c.setFont("Helvetica-Bold", 16)
    c.drawString(150, 800, "AI Document Workflow System")

    c.setFont("Helvetica", 14)
    c.drawString(170, 770, "Fraud Detection Report")

    c.setFont("Helvetica", 12)

    y = 720

    c.drawString(50, y, f"Report Date: {datetime.datetime.now()}")
    y -= 40

    c.drawString(50, y, f"Scan ID: {last_scan.id}")
    y -= 30

    c.drawString(50, y, f"Risk Level: {last_scan.risk_level}")
    y -= 30

    c.drawString(50, y, f"Risk Score: {last_scan.risk_score}")
    y -= 30

    c.drawString(50, y, f"ML Prediction: {last_scan.ml_prediction}")
    y -= 30

    c.drawString(50, y, f"Confidence: {last_scan.ml_confidence}%")
    y -= 30

    c.drawString(50, y, f"Detected Keywords: {last_scan.matched_keywords}")
    y -= 40

    c.drawString(50, y, "Extracted Text:")
    y -= 20

    text = c.beginText(50, y)
    text.setFont("Helvetica", 11)

    for line in last_scan.extracted_text.split():
        text.textLine(line)

    c.drawText(text)

    c.save()

    return FileResponse(file_path, filename="fraud_report.pdf")

@app.get("/upload", response_class=HTMLResponse)
async def upload_page(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})


# -----------------------------
# Upload + Detection
# -----------------------------

@app.post("/upload", response_class=HTMLResponse)
async def upload_file(request: Request, file: UploadFile = File(...)):

    file_location = f"uploads/{file.filename}"

    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    extracted_text = ""
    highlighted_text = ""
    risk_level = ""
    risk_color = ""
    risk_score = 0
    matched_keywords = []

    ml_prediction = "N/A"
    ml_probability = 0

    try:
        image = Image.open(file_location)

        custom_config = r'--oem 3 --psm 6'
        extracted_text = pytesseract.image_to_string(image, config=custom_config)

        # ---------------------------
        # Clean text
        # ---------------------------
        extracted_text = re.sub(r'[^A-Za-z0-9\s]', ' ', extracted_text)
        extracted_text = re.sub(r'\s+', ' ', extracted_text)
        extracted_text = extracted_text.strip()

        # ---------------------------
        # Rule-Based Detection
        # ---------------------------
        text_words = extracted_text.lower().split()

        for keyword in fraud_keywords:
            for word in text_words:
                similarity = SequenceMatcher(None, keyword, word).ratio()

                if keyword in word or similarity > 0.75:
                    if keyword not in matched_keywords:
                        matched_keywords.append(keyword)
                        risk_score += 1
                    break

        # ---------------------------
        # Highlight Keywords
        # ---------------------------
        highlighted_text = extracted_text
        for keyword in matched_keywords:
            highlighted_text = re.sub(
                f"(?i){keyword}",
                f"<span style='color:red;font-weight:bold'>{keyword.upper()}</span>",
                highlighted_text
            )

        # ---------------------------
        # ML Prediction
        # ---------------------------
        if extracted_text.strip() != "":
            prediction = ml_model.predict([extracted_text])[0]
            probabilities = ml_model.predict_proba([extracted_text])[0]

            ml_prediction = prediction
            ml_probability = round(max(probabilities) * 100, 2)

        # ---------------------------
        # HYBRID FINAL DECISION LOGIC
        # ---------------------------
        if ml_prediction == "fraud" and ml_probability > 75:
            risk_level = "High Risk Fraud (ML Confirmed)"
            risk_color = "red"

        elif risk_score >= 3:
            risk_level = "High Risk Fraud (Keyword Heavy)"
            risk_color = "red"

        elif risk_score >= 1 or ml_probability > 60:
            risk_level = "Suspicious Document"
            risk_color = "orange"

        else:
            risk_level = "Safe Document"
            risk_color = "green"

        # ---------------------------
        # Save to Database
        # ---------------------------
        db = SessionLocal()

        new_scan = ScanResult(
            extracted_text=extracted_text,
            risk_level=risk_level,
            risk_score=risk_score,
            ml_prediction=ml_prediction,
            ml_confidence=ml_probability,
            matched_keywords=", ".join(matched_keywords)
        )

        db.add(new_scan)
        db.commit()
        db.close()

    except Exception as e:
        extracted_text = f"OCR failed: {str(e)}"
        highlighted_text = extracted_text
        risk_level = "OCR Error"
        risk_color = "red"

    return templates.TemplateResponse(
        "result.html",
        {
            "request": request,
            "extracted_text": highlighted_text,
            "risk_level": risk_level,
            "risk_score": risk_score,
            "total_keywords": len(fraud_keywords),
            "risk_color": risk_color,
            "matched_keywords": matched_keywords,
            "ml_prediction": ml_prediction,
            "ml_probability": ml_probability
        }
    )