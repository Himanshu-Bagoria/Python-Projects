# Employee Performance Dashboard

A comprehensive Streamlit-based Employee Performance Dashboard that allows HR managers to track, analyze, and manage employee performance with advanced features including face recognition attendance.

## 🚀 Features

### Core Features
- **Employee Management**: Add, update, and manage employee records
- **Attendance Tracking**: Manual logging and automated face recognition attendance
- **Performance Monitoring**: Track KPIs like tasks completed, quality scores, and productivity metrics
- **Data Visualization**: Interactive charts and graphs using Plotly
- **Reporting**: Generate PDF and CSV reports
- **Alert System**: Automated alerts for low attendance and performance dips

### Unique Features
- **Face Recognition Attendance**: Webcam-based attendance using OpenCV and face_recognition
- **Productivity Trend Analysis**: Visualize performance trends over time
- **Leaderboard**: Top performers ranking system
- **Dark/Light Theme Toggle**: Better UI experience
- **Advanced Analytics**: Department comparisons and productivity insights

## 📋 Requirements

- Python 3.8+
- Webcam (for face recognition feature)
- See `requirements.txt` for detailed dependencies

## 🛠️ Installation

1. **Clone or download the project** to your local machine

2. **Navigate to the project directory**:
   ```bash
   cd "employe deshboard"
   ```

3. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## ▶️ Running the Application

1. **Start the Streamlit app**:
   ```bash
   streamlit run app.py
   ```

2. **Access the dashboard**:
   - The app will automatically open in your default browser
   - Or navigate to: `http://localhost:8501`

## 📊 Usage Guide

### Dashboard Navigation

The dashboard has 8 main sections accessible via the sidebar:

#### 1. **Dashboard**
- Executive overview with key metrics
- Department distribution pie chart
- Daily attendance trend
- Recent activity summary

#### 2. **Employee Management**
- **View Employees**: Filter and search employee records
- **Add Employee**: Add new employees via form
- **Upload Data**: Import employee data from CSV/Excel

#### 3. **Attendance**
- **Log Attendance**: Manual attendance entry
- **View Records**: Filter attendance by date range and department
- **Face Recognition**: Register faces and recognize employees

#### 4. **Performance Tracking**
- **Add Performance Record**: Enter tasks, quality, and productivity scores
- **View Performance**: Filter and view performance records
- **Productivity Analysis**: Trend analysis and recommendations

#### 5. **Face Recognition**
- **Register Face**: Upload employee photos for face recognition
- **Recognize Face**: Use webcam to automatically log attendance

#### 6. **Reports**
- **Generate Report**: Create employee or department PDF reports
- **Export Data**: Download data as CSV

#### 7. **Alerts**
- View automated alerts for performance issues
- Configure alert thresholds

#### 8. **Analytics**
- Department performance comparison
- Top performers leaderboard
- Productivity heatmap visualization

### Getting Started

1. **Initial Setup**:
   - Sample data is included in the `data/` folder
   - Add more employees using the Employee Management section
   - Register employee faces for face recognition

2. **Daily Usage**:
   - Use the attendance section to log employee attendance
   - Add performance records regularly
   - Monitor alerts for any issues
   - Generate reports as needed

## 📁 Project Structure

```
employe deshboard/
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── data/                     # Data storage
│   ├── employees.csv         # Employee records
│   ├── attendance.csv        # Attendance logs
│   ├── performance.csv       # Performance metrics
│   └── faces/                # Employee face images
├── components/               # Core components
│   ├── data_manager.py       # Data handling
│   ├── face_recognition.py   # Face recognition system
│   └── viz.py                # Visualization components
└── utils/                    # Utility modules
    ├── alerts.py             # Alert system
    ├── reports.py            # Report generation
    └── productivity.py       # Productivity analysis
```

## 🔧 Configuration

### Face Recognition Setup
1. Ensure your webcam is properly connected
2. Good lighting conditions improve recognition accuracy
3. Use clear, front-facing photos for face registration
4. Register each employee's face in the Face Recognition section

### Alert Thresholds
Configure alert settings in the Alerts section:
- **Attendance Threshold**: Percentage below which attendance alerts trigger
- **Performance Threshold**: Score below which performance alerts trigger
- **Inactivity Threshold**: Days of inactivity that trigger alerts

## 📱 Features in Detail

### Face Recognition Attendance
- Uses OpenCV and face_recognition library
- Real-time webcam face detection
- Automatic attendance logging when face is recognized
- Confidence-based matching system

### Performance Tracking
- Tasks completed tracking
- Quality score assessment (0-10 scale)
- Productivity score calculation
- Trend analysis over time
- Peer comparison capabilities

### Visualization
- Interactive Plotly charts
- Department performance comparisons
- Productivity trend lines
- Heatmaps for detailed analysis
- Leaderboard rankings

### Reporting
- PDF report generation with FPDF
- CSV export functionality
- Customizable date ranges
- Department and individual employee reports

## ⚠️ Important Notes

### Face Recognition Limitations
- Requires proper lighting
- Works best with clear frontal faces
- May require re-registration if appearance changes significantly
- WebCam access must be granted in browser

### Data Management
- All data stored in local CSV files
- Backup your data directory regularly
- Export data regularly for off-site storage
- Large datasets may affect performance

### Performance
- The dashboard can handle 1000+ employee records
- Face recognition performance depends on system resources
- Close unused tabs in Streamlit for better performance

## 🐛 Troubleshooting

### Common Issues

1. **Module Not Found Errors**
   - Run `pip install -r requirements.txt`

2. **WebCam Access Issues**
   - Ensure webcam permissions are granted
   - Close other applications using the camera
   - Try reconnecting the webcam

3. **Face Recognition Problems**
   - Improve lighting conditions
   - Use higher quality images for registration
   - Ensure face is clearly visible in webcam

4. **Data Loading Issues**
   - Check that CSV files in data/ directory are not corrupted
   - Ensure proper file permissions
   - Restart the Streamlit application

### Performance Optimization
- Limit the date range in filters
- Use specific employee filters when possible
- Close unused browser tabs
- Restart the application periodically

## 📄 License

This project is for internal use. Please contact the development team for licensing information.

## 🆘 Support

For issues, questions, or feature requests:
- Check the troubleshooting section above
- Review the Streamlit documentation
- Contact your system administrator

## 🔄 Updates

The dashboard will be updated regularly with:
- New visualization features
- Performance improvements
- Additional reporting options
- Enhanced face recognition capabilities

---

*Built with Python, Streamlit, Plotly, OpenCV, and face_recognition*