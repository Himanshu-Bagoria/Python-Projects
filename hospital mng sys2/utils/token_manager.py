import json
import random
import string
from datetime import datetime, timedelta
from pathlib import Path
import streamlit as st

class TokenManager:
    def __init__(self):
        self.data_dir = Path("data")
        self.data_dir.mkdir(exist_ok=True)
        self.token_file = self.data_dir / "tokens.json"
        
    def generate_token(self, patient_name, department, priority="Normal"):
        """Generate a unique waiting token"""
        # Generate token number
        token_number = self._get_next_token_number()
        
        # Generate unique token ID
        token_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        
        # Calculate estimated wait time based on priority
        wait_times = {
            "Emergency": 5,
            "High": 15,
            "Normal": 30,
            "Low": 45
        }
        estimated_wait = wait_times.get(priority, 30)
        
        token_data = {
            "token_id": token_id,
            "token_number": token_number,
            "patient_name": patient_name,
            "department": department,
            "priority": priority,
            "status": "Waiting",
            "created_at": datetime.now().isoformat(),
            "estimated_wait_minutes": estimated_wait,
            "called_at": None,
            "completed_at": None
        }
        
        # Save token
        self._save_token(token_data)
        return token_data
    
    def _get_next_token_number(self):
        """Get the next available token number"""
        tokens = self._load_tokens()
        if not tokens:
            return 1
        return max(token.get('token_number', 0) for token in tokens) + 1
    
    def _save_token(self, token_data):
        """Save token to file"""
        tokens = self._load_tokens()
        tokens.append(token_data)
        
        with open(self.token_file, 'w', encoding='utf-8') as f:
            json.dump(tokens, f, indent=2, ensure_ascii=False)
    
    def _load_tokens(self):
        """Load all tokens from file"""
        if not self.token_file.exists():
            return []
        
        try:
            with open(self.token_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    
    def get_waiting_tokens(self, department=None):
        """Get all waiting tokens, optionally filtered by department"""
        tokens = self._load_tokens()
        waiting_tokens = [t for t in tokens if t.get('status') == 'Waiting']
        
        if department:
            waiting_tokens = [t for t in waiting_tokens if t.get('department') == department]
        
        # Sort by priority and creation time
        priority_order = {"Emergency": 0, "High": 1, "Normal": 2, "Low": 3}
        waiting_tokens.sort(key=lambda x: (priority_order.get(x.get('priority', 'Normal'), 2), x.get('created_at', '')))
        
        return waiting_tokens
    
    def call_token(self, token_id):
        """Call a token (mark as called)"""
        tokens = self._load_tokens()
        for token in tokens:
            if token.get('token_id') == token_id:
                token['status'] = 'Called'
                token['called_at'] = datetime.now().isoformat()
                break
        
        with open(self.token_file, 'w', encoding='utf-8') as f:
            json.dump(tokens, f, indent=2, ensure_ascii=False)
    
    def complete_token(self, token_id):
        """Mark token as completed"""
        tokens = self._load_tokens()
        for token in tokens:
            if token.get('token_id') == token_id:
                token['status'] = 'Completed'
                token['completed_at'] = datetime.now().isoformat()
                break
        
        with open(self.token_file, 'w', encoding='utf-8') as f:
            json.dump(tokens, f, indent=2, ensure_ascii=False)
    
    def get_token_stats(self):
        """Get token statistics"""
        tokens = self._load_tokens()
        
        stats = {
            "total_tokens": len(tokens),
            "waiting": len([t for t in tokens if t.get('status') == 'Waiting']),
            "called": len([t for t in tokens if t.get('status') == 'Called']),
            "completed": len([t for t in tokens if t.get('status') == 'Completed']),
            "departments": {},
            "avg_wait_time": 0
        }
        
        # Calculate department stats
        for token in tokens:
            dept = token.get('department', 'Unknown')
            if dept not in stats['departments']:
                stats['departments'][dept] = {
                    "waiting": 0,
                    "called": 0,
                    "completed": 0
                }
            
            status = token.get('status', 'Waiting')
            if status in stats['departments'][dept]:
                stats['departments'][dept][status] += 1
        
        return stats

# Global token manager instance
token_manager = TokenManager()
