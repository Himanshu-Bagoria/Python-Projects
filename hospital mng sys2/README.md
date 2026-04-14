# 🏥 Smart Hospital System

A comprehensive, futuristic hospital management system built with Streamlit featuring 15 advanced modules with animated UI elements, biometric authentication, AI-powered diagnostics, and multilingual support.

## ✨ Features

### 🔐 1. Biometric Patient Check-In
- Fingerprint and face recognition simulation
- Auto-fetch patient history and appointments
- Animated login panel with glowing effects

### 🤖 2. AI Symptom Analyzer
- ML-powered symptom analysis
- Interactive body map for symptom selection
- Hindi/English toggle with voice narration
- Disease image integration via URLs

### 📅 3. Smart Appointment Scheduler
- AI-optimized time slot prediction
- Voice-controlled booking system
- Animated calendar with QR confirmation

### 📊 4. Real-Time Health Dashboard
- Live vital signs simulation
- Interactive charts and alerts
- Modular patient monitoring panels

### 💊 5. Digital Prescription & QR Pharmacy
- QR-coded prescriptions
- Automated pharmacy integration
- Dosage reminders and refill alerts
- Medicine image display via URLs

### 📈 6. AI Diagnosis History Tracker
- Timeline visualization of medical history
- Predictive health analytics
- Exportable visual reports

### 🧠 7. Mental Wellness Companion
- Daily mood tracking via webcam/voice
- Meditation and wellness recommendations
- Animated progress journal

### 🔬 8. Lab Report Visualizer
- Automated lab result analysis
- Trend visualization and anomaly detection
- Voice assistant for result explanation

### 🗺️ 9. Smart Navigation System
- Interactive hospital maps
- QR-based wayfinding
- Multi-language voice guidance

### 🚨 10. Emergency Alert System
- One-tap SOS functionality
- Real-time emergency response dashboard
- Location and vital sign transmission

### 📚 11. Health Education Hub
- Personalized educational content
- Animated condition explainers
- Hindi/English video library

### 💳 12. Insurance & Billing Assistant
- Automated bill calculation
- Insurance claim suggestions
- QR payment integration

### 👨‍⚕️ 13. AI Doctor Recommendation Engine
- Symptom-based doctor matching
- Rating and availability display
- Voice-guided selection

### 🏥 14. Smart Ward Monitoring
- Real-time sensor simulation
- Anomaly detection and alerts
- Staff control panel

### ⚙️ 15. Modular Admin Dashboard
- Comprehensive system management
- Role-based access control
- Analytics and reporting

## 🚀 Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd hospital-mng-sys2
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run main.py
```

## 🎨 UI Features

- **Futuristic Design**: Glowing buttons, smooth transitions, and animated elements
- **Theme Switcher**: Toggle between light and dark modes
- **Multilingual Support**: Hindi and English interface
- **Voice Integration**: Speech recognition and text-to-speech
- **Image Integration**: Support for custom URLs for disease visuals and medicine photos
- **Responsive Layout**: Optimized for various screen sizes

## 🛠️ Technical Stack

- **Frontend**: Streamlit with custom HTML/CSS
- **Computer Vision**: OpenCV for biometric features
- **AI/ML**: Scikit-learn for symptom analysis
- **Data Visualization**: Plotly, Matplotlib
- **Voice Processing**: SpeechRecognition, pyttsx3
- **QR Codes**: qrcode library
- **Image Processing**: PIL/Pillow

## 📁 Project Structure

```
hospital-mng-sys2/
├── main.py                 # Main application entry point
├── requirements.txt        # Python dependencies
├── README.md              # Project documentation
├── modules/               # Individual feature modules
│   ├── biometric_checkin.py
│   ├── symptom_analyzer.py
│   ├── appointment_scheduler.py
│   ├── health_dashboard.py
│   ├── prescription_system.py
│   ├── diagnosis_tracker.py
│   ├── wellness_companion.py
│   ├── lab_visualizer.py
│   ├── navigation_system.py
│   ├── emergency_alert.py
│   ├── education_hub.py
│   ├── billing_assistant.py
│   ├── doctor_recommendation.py
│   ├── ward_monitoring.py
│   └── admin_dashboard.py
├── utils/                 # Utility functions
│   ├── __init__.py
│   ├── auth.py
│   ├── database.py
│   ├── voice_utils.py
│   ├── image_utils.py
│   └── ui_components.py
├── data/                  # Sample data and configurations
│   ├── patients.json
│   ├── doctors.json
│   ├── symptoms.json
│   └── diseases.json
├── assets/               # Static assets
│   ├── css/
│   ├── images/
│   └── icons/
└── config/              # Configuration files
    ├── settings.py
    └── themes.py
```

## 🎯 Usage

1. **Start the Application**: Run `streamlit run main.py`
2. **Select Module**: Choose from the 15 available modules
3. **Authentication**: Use biometric or traditional login
4. **Interact**: Utilize voice commands, upload images, and explore features
5. **Customize**: Add custom image URLs for disease visuals and medicine photos

## 🔧 Configuration

- Modify `config/settings.py` for system-wide settings
- Update `config/themes.py` for custom UI themes
- Add custom image URLs in respective modules for disease and medicine visuals

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions, please open an issue in the repository or contact the development team.

---

**Built with ❤️ for modern healthcare management**
