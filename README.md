# AI_Document_Workflow_Project

## 📌 Project Overview
This project is an AI-powered document analysis and fraud detection system built using FastAPI. It uses OCR to extract text from uploaded documents/images and applies both rule-based logic and Machine Learning models to detect fraud and generate a risk score.

The system also includes a workflow automation approach where different components (OCR, keyword detection, ML prediction, risk scoring, and reporting) work together like an intelligent multi-agent pipeline.

---

## ⚙️ Tech Stack
- Python
- FastAPI
- Tesseract OCR
- Machine Learning (Joblib model / Scikit-learn)
- SQLAlchemy (Database)
- HTML, CSS (Jinja2 Templates)
- PIL (Image Processing)
- ReportLab (PDF Generation)

---

## 🚀 Features
- Upload image or document for analysis  
- OCR-based text extraction using Tesseract  
- Fraud keyword detection with similarity matching  
- ML-based fraud prediction model  
- Hybrid risk scoring system (Rule-based + AI)  
- Risk classification: Safe / Suspicious / High Risk  
- Dashboard with analytics  
- Scan history tracking  
- Downloadable PDF fraud report  

---

## 🧠 System Workflow
1. User uploads document/image  
2. OCR extracts text from file  
3. Text is cleaned and processed  
4. Fraud keywords are detected  
5. ML model predicts fraud probability  
6. Hybrid logic generates final risk level  
7. Result is displayed and stored in database  
8. User can download report or view analytics  

---

## 🛠️ How to Run

## 1. Clone the repository
```bash
git clone https://github.com/tahirsavanur19-dev/AI_document_workflow_project.git
```

## 2. Move into project folder
```bash
cd Multi-Agent_Workflow_Automation_System_Using_AI
```

## 3. Install dependencies
```bash
pip install -r requirements.txt
```

## 4. Run FastAPI server
```bash
uvicorn main:app --reload
```

## 5. Open in browser
http://127.0.0.1:8000

---

📂 Project Structure

project/
│── main.py
│── database.py
│── fraud_model.pkl
│── uploads/
│── templates/
│    ├── login.html
│    ├── dashboard.html
│    ├── upload.html
│    ├── result.html
│    ├── history.html
│    ├── analytics.html
│── static/
│── requirements.txt

---

## 📊 Risk Levels

🟢 Safe Document
🟠 Suspicious Document
🔴 High Risk Fraud

---

## 🔮 Future Improvements
Deep Learning-based fraud detection
API-based real-time scanning
Cloud deployment (AWS / Render)
User authentication system
Improved OCR accuracy

---

## Screenshots

## LOGIN PAGE
![LOGIN](https://github.com/user-attachments/assets/51c1745e-bfc6-4514-98d0-a3a7d9edf9f6)

## DASHBOARD PAGE
![DASHBOARD](https://github.com/user-attachments/assets/80f57d84-06a2-44a1-93c3-99249f43586c)

## UPLOAD PAGE 
![UPLOAD](https://github.com/user-attachments/assets/f01fa2d1-d2c5-4e04-9ffb-116c004847b8)

## RESULT PAGE
![RESULT](https://github.com/user-attachments/assets/43255d0e-4ce9-46b8-a3b5-4f67c456301a)

## FRAUD ANALYTICS PAGE
![ANALYTICS](https://github.com/user-attachments/assets/9da44b74-4186-4810-a395-a6165c0fac40)

---
## 📌 Note
This project is for educational purposes and demonstrates AI + OCR + Machine Learning based workflow automation for document fraud detection.

 ---
 
## 👨‍💻 Author
Tahirhussain Mahabub Savanur
