import json
import os
from datetime import datetime, date
from pathlib import Path
import streamlit as st

class DataManager:
    def __init__(self):
        self.data_dir = Path("data")
        self.data_dir.mkdir(exist_ok=True)
        
    def save_data(self, data_type, data):
        """Save data to JSON file"""
        file_path = self.data_dir / f"{data_type}.json"
        
        # Load existing data
        existing_data = self.load_data(data_type)
        if not existing_data:
            existing_data = []
        
        # Add timestamp and ensure required fields
        data['timestamp'] = datetime.now().isoformat()
        data['id'] = len(existing_data) + 1
        
        # Ensure patient_name exists
        if 'patient_name' not in data or not data['patient_name']:
            data['patient_name'] = "Unknown Patient"
        
        # Append new data
        existing_data.append(data)
        
        # Save to file
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(existing_data, f, indent=2, ensure_ascii=False)
        
        return data['id']
    
    def load_data(self, data_type):
        """Load data from JSON file with error handling"""
        file_path = self.data_dir / f"{data_type}.json"
        
        if not file_path.exists():
            return []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # Validate and clean data
            if not isinstance(data, list):
                return []
                
            cleaned_data = []
            for item in data:
                if isinstance(item, dict):
                    # Ensure required fields exist
                    if 'patient_name' not in item or not item['patient_name']:
                        item['patient_name'] = "Unknown Patient"
                    if 'id' not in item:
                        item['id'] = len(cleaned_data) + 1
                    if 'timestamp' not in item:
                        item['timestamp'] = datetime.now().isoformat()
                    cleaned_data.append(item)
                    
            return cleaned_data
        except Exception as e:
            st.error(f"Error loading {data_type} data: {e}")
            return []
    
    def delete_data(self, data_type, data_id):
        """Delete specific data entry"""
        data = self.load_data(data_type)
        data = [item for item in data if item.get('id') != data_id]
        
        file_path = self.data_dir / f"{data_type}.json"
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def clear_all_data(self):
        """Clear all data files"""
        for file_path in self.data_dir.glob("*.json"):
            try:
                file_path.unlink()
            except:
                pass

# Global data manager instance
data_manager = DataManager()
