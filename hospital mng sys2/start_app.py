#!/usr/bin/env python3
"""
Startup script for Smart Hospital System
"""

import subprocess
import sys
import os
from pathlib import Path

def main():
    """Start the Smart Hospital System"""
    print("🏥 Starting Smart Hospital System...")
    print("=" * 50)
    
    # Check if required files exist
    if not Path("main.py").exists():
        print("❌ Error: main.py not found!")
        return
    
    if not Path("requirements.txt").exists():
        print("❌ Error: requirements.txt not found!")
        return
    
    # Install dependencies if needed
    print("📦 Checking dependencies...")
    try:
        import streamlit
        print("✅ Streamlit is installed")
    except ImportError:
        print("📦 Installing dependencies...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    
    # Start the application
    print("🚀 Launching Smart Hospital System...")
    print("🌐 The application will open in your browser at: http://localhost:8501")
    print("📱 You can also access it at: http://localhost:8502")
    print("=" * 50)
    
    try:
        # Start the application
        subprocess.run([sys.executable, "-m", "streamlit", "run", "main.py", "--server.port", "8501"])
    except KeyboardInterrupt:
        print("\n🛑 Application stopped by user")
    except Exception as e:
        print(f"❌ Error starting application: {e}")

if __name__ == "__main__":
    main()
