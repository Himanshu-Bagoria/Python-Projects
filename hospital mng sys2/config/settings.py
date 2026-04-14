# System settings for Smart Hospital System

import os
from datetime import datetime

# Application settings
APP_NAME = "Smart Hospital System"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "Advanced Healthcare Management Platform"
APP_AUTHOR = "Smart Hospital Team"

# Database settings
DATABASE_DIR = "data"
CACHE_DIR = "assets/images/cache"
LOG_DIR = "logs"

# Authentication settings
SESSION_TIMEOUT = 3600  # 1 hour
MAX_LOGIN_ATTEMPTS = 3
PASSWORD_MIN_LENGTH = 8

# Voice settings
VOICE_TIMEOUT = 5  # seconds
VOICE_LANGUAGE_DEFAULT = "en-US"
VOICE_VOLUME = 0.9
VOICE_RATE = 150

# Image settings
IMAGE_MAX_SIZE = (800, 600)
IMAGE_CACHE_ENABLED = True
IMAGE_WATERMARK_ENABLED = True
IMAGE_WATERMARK_TEXT = "Smart Hospital System"

# AI/ML settings
SYMPTOM_ANALYSIS_CONFIDENCE_THRESHOLD = 0.7
DISEASE_PREDICTION_TOP_K = 5
MEDICATION_RECOMMENDATION_TOP_K = 3

# Emergency settings
EMERGENCY_RESPONSE_TIMEOUT = 30  # seconds
EMERGENCY_ALERT_RETENTION_DAYS = 30
EMERGENCY_CONTACT_NUMBER = "+1-800-HOSPITAL"

# Appointment settings
APPOINTMENT_SLOT_DURATION = 30  # minutes
APPOINTMENT_ADVANCE_BOOKING_DAYS = 30
APPOINTMENT_CANCELLATION_HOURS = 24

# Vital signs settings
VITAL_SIGNS_UPDATE_INTERVAL = 60  # seconds
VITAL_SIGNS_ALERT_THRESHOLDS = {
    "heart_rate": {"min": 60, "max": 100},
    "blood_pressure_systolic": {"min": 90, "max": 140},
    "blood_pressure_diastolic": {"min": 60, "max": 90},
    "temperature": {"min": 36.0, "max": 37.5},
    "oxygen_saturation": {"min": 95, "max": 100},
    "respiratory_rate": {"min": 12, "max": 20}
}

# Ward monitoring settings
WARD_TEMPERATURE_RANGE = {"min": 20, "max": 25}  # Celsius
WARD_NOISE_LEVEL_THRESHOLD = 60  # dB
WARD_OCCUPANCY_ALERT_THRESHOLD = 0.9  # 90%

# Notification settings
NOTIFICATION_ENABLED = True
NOTIFICATION_TYPES = ["email", "sms", "push"]
NOTIFICATION_RETRY_ATTEMPTS = 3

# Export settings
EXPORT_FORMATS = ["pdf", "csv", "json"]
EXPORT_MAX_RECORDS = 10000

# Security settings
ENCRYPTION_ENABLED = True
ENCRYPTION_ALGORITHM = "AES-256"
SESSION_ENCRYPTION = True

# Logging settings
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_FILE = f"logs/hospital_system_{datetime.now().strftime('%Y%m%d')}.log"

# Performance settings
CACHE_ENABLED = True
CACHE_TTL = 3600  # 1 hour
MAX_CONCURRENT_REQUESTS = 100
REQUEST_TIMEOUT = 30  # seconds

# Multilingual settings
SUPPORTED_LANGUAGES = ["en", "hi"]
DEFAULT_LANGUAGE = "en"
LANGUAGE_FALLBACK = "en"

# Theme settings
DEFAULT_THEME = "light"
AVAILABLE_THEMES = ["light", "dark", "futuristic", "medical"]

# Feature flags
FEATURES = {
    "biometric_auth": True,
    "voice_commands": True,
    "ai_diagnosis": True,
    "real_time_monitoring": True,
    "emergency_alerts": True,
    "multilingual": True,
    "image_integration": True,
    "qr_codes": True,
    "voice_navigation": True,
    "mood_tracking": True,
    "meditation_guide": True,
    "health_education": True,
    "insurance_billing": True,
    "doctor_recommendation": True,
    "ward_monitoring": True,
    "admin_dashboard": True
}

# API settings
API_VERSION = "v1"
API_RATE_LIMIT = 1000  # requests per hour
API_TIMEOUT = 30  # seconds

# External service settings
EXTERNAL_SERVICES = {
    "weather_api": {
        "enabled": True,
        "url": "https://api.openweathermap.org/data/2.5/weather",
        "timeout": 10
    },
    "maps_api": {
        "enabled": True,
        "url": "https://maps.googleapis.com/maps/api",
        "timeout": 10
    },
    "translation_api": {
        "enabled": True,
        "url": "https://translation.googleapis.com/language/translate/v2",
        "timeout": 10
    }
}

# Backup settings
BACKUP_ENABLED = True
BACKUP_FREQUENCY = "daily"  # daily, weekly, monthly
BACKUP_RETENTION_DAYS = 30
BACKUP_COMPRESSION = True

# Monitoring settings
MONITORING_ENABLED = True
METRICS_COLLECTION_INTERVAL = 60  # seconds
ALERT_EMAILS = ["admin@hospital.com", "support@hospital.com"]

# Development settings
DEBUG_MODE = False
TESTING_MODE = False
MOCK_DATA_ENABLED = True

# Get setting value
def get_setting(key, default=None):
    """Get setting value by key"""
    return globals().get(key, default)

# Set setting value
def set_setting(key, value):
    """Set setting value by key"""
    globals()[key] = value

# Check if feature is enabled
def is_feature_enabled(feature_name):
    """Check if a feature is enabled"""
    return FEATURES.get(feature_name, False)

# Get vital signs threshold
def get_vital_signs_threshold(metric):
    """Get vital signs threshold for a metric"""
    return VITAL_SIGNS_ALERT_THRESHOLDS.get(metric, {})

# Validate vital signs
def validate_vital_signs(metric, value):
    """Validate vital signs value against thresholds"""
    thresholds = get_vital_signs_threshold(metric)
    if not thresholds:
        return True
    
    min_val = thresholds.get("min")
    max_val = thresholds.get("max")
    
    if min_val is not None and value < min_val:
        return False, f"Value {value} is below minimum {min_val}"
    
    if max_val is not None and value > max_val:
        return False, f"Value {value} is above maximum {max_val}"
    
    return True, "Value is within normal range"

# Create directories
def create_directories():
    """Create necessary directories"""
    directories = [DATABASE_DIR, CACHE_DIR, LOG_DIR]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

# Initialize settings
def initialize_settings():
    """Initialize system settings"""
    create_directories()
    
    # Set environment variables
    os.environ.setdefault('HOSPITAL_SYSTEM_ENV', 'development')
    os.environ.setdefault('HOSPITAL_SYSTEM_DEBUG', str(DEBUG_MODE))
    
    return True
