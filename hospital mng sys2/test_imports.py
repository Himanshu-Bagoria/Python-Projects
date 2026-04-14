#!/usr/bin/env python3
"""
Test script to verify all imports work correctly
"""

import sys
import os
from pathlib import Path

# Add modules to path
sys.path.append(str(Path(__file__).parent / "modules"))
sys.path.append(str(Path(__file__).parent / "utils"))

def test_imports():
    """Test all module imports"""
    print("Testing imports...")
    
    # Test utility imports
    try:
        from utils.ui_components import *
        print("✅ UI components imported successfully")
    except Exception as e:
        print(f"❌ UI components import failed: {e}")
    
    try:
        from utils.auth import *
        print("✅ Auth module imported successfully")
    except Exception as e:
        print(f"❌ Auth module import failed: {e}")
    
    try:
        from utils.database import *
        print("✅ Database module imported successfully")
    except Exception as e:
        print(f"❌ Database module import failed: {e}")
    
    try:
        from utils.voice_utils import *
        print("✅ Voice utils imported successfully")
    except Exception as e:
        print(f"❌ Voice utils import failed: {e}")
    
    try:
        from utils.image_utils import *
        print("✅ Image utils imported successfully")
    except Exception as e:
        print(f"❌ Image utils import failed: {e}")
    
    try:
        from config.themes import *
        print("✅ Themes module imported successfully")
    except Exception as e:
        print(f"❌ Themes module import failed: {e}")
    
    # Test module imports
    modules = [
        "biometric_checkin",
        "symptom_analyzer", 
        "appointment_scheduler",
        "health_dashboard",
        "prescription_system",
        "diagnosis_history",
        "mental_wellness",
        "lab_visualizer",
        "navigation_system",
        "emergency_alert",
        "health_education",
        "insurance_billing",
        "doctor_recommendation",
        "ward_monitoring",
        "admin_dashboard"
    ]
    
    for module_name in modules:
        try:
            module = __import__(f"modules.{module_name}", fromlist=['main'])
            print(f"✅ {module_name} module imported successfully")
        except Exception as e:
            print(f"❌ {module_name} module import failed: {e}")
    
    print("\n🎉 Import test completed!")

if __name__ == "__main__":
    test_imports()
