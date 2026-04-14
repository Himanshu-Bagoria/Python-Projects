# Intelligent Face Recognition Attendance System

A professional, high‑accuracy attendance management system using advanced face recognition technology. This system automates employee entry/exit tracking, enforces smart attendance rules, and provides a modern, recruiter‑ready interface.

## 🚀 Core Features
- **Face Recognition**: Powered by DeepFace (FaceNet) with anti‑spoofing placeholders.
- **Smart Entry/Exit Rules**:
  - ✅ **Full Day Exit**: Allowed only after completing the full workday.
  - ✅ **Half Day Exit**: Allowed only 5 times per month (auto‑tracked).
  - ✅ **Emergency Exit**: Allowed only after 1 hour of entry.
- **Analytics Dashboard**: Real‑time tracking with Plotly charts and monthly usage analytics.
- **Security & Reliability**: AES‑encrypted face embeddings, role‑based access (Admin/Employee), and event logging.
- **Professional UI**: Modern glassmorphic design, colorful layout, and responsive top-right navigation.

## 🛠 Tech Stack
- **Python 3.13+** (Core Logic)
- **OpenCV + DeepFace/FaceNet** (Biometrics)
- **Streamlit** (User Interface)
- **SQLite** (Database)
- **Plotly** (Visualizations)
- **Cryptography (AES)** (Secure Storage)

## 📦 Project Structure
```
📦 FaceRecognitionAttendanceSystem
 ┣ 📂 app/           # Core logic (DB, Auth, AI, Engine)
 ┣ 📂 data/          # Face database & Logs
 ┣ 📂 models/        # Pre-trained models (Downloadable)
 ┣ 📂 reports/       # Exported attendance reports
 ┣ 📜 requirements.txt
 ┣ 📜 README.md
 ┗ 📜 app.py         # Main entry point
```

## ⚙️ Installation & Setup
1. **Clone the repository**:
   ```bash
   git clone https://github.com/username/FaceRecognitionAttendanceSystem.git
   cd FaceRecognitionAttendanceSystem
   ```
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the application**:
   ```bash
   streamlit run app.py
   ```

## 📊 Dashboard Highlights
- Real‑time IN/OUT tracking with high-precision timestamps.
- Monthly attendance trends and half‑day budget tracking.
- Secure, exportable reports (CSV/Excel).

## 🔮 Future Improvements
- Mobile application integration (Android/iOS).
- Advanced liveness detection (blink & texture analysis).
- Hybrid Cloud deployment with PostgreSQL/AWS S3.
- Automated HR alerts via email/Slack.
