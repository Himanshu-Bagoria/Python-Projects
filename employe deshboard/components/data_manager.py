import pandas as pd
import numpy as np
import os
from datetime import datetime
import streamlit as st

class DataManager:
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        self.employees_file = os.path.join(data_dir, "employees.csv")
        self.attendance_file = os.path.join(data_dir, "attendance.csv")
        self.performance_file = os.path.join(data_dir, "performance.csv")
        
        # Create data directory if it doesn't exist
        os.makedirs(data_dir, exist_ok=True)
        os.makedirs(os.path.join(data_dir, "faces"), exist_ok=True)
        
        # Initialize CSV files if they don't exist
        self._initialize_data_files()
    
    def _initialize_data_files(self):
        """Initialize CSV files with headers if they don't exist"""
        if not os.path.exists(self.employees_file):
            employees_df = pd.DataFrame(columns=[
                'employee_id', 'name', 'email', 'department', 'role', 
                'hire_date', 'salary', 'phone', 'address'
            ])
            employees_df.to_csv(self.employees_file, index=False)
        
        if not os.path.exists(self.attendance_file):
            attendance_df = pd.DataFrame(columns=[
                'employee_id', 'date', 'time_in', 'time_out', 'status'
            ])
            attendance_df.to_csv(self.attendance_file, index=False)
        
        if not os.path.exists(self.performance_file):
            performance_df = pd.DataFrame(columns=[
                'employee_id', 'date', 'tasks_completed', 'quality_score', 
                'productivity_score', 'comments'
            ])
            performance_df.to_csv(self.performance_file, index=False)
    
    def load_employees(self):
        """Load employees data"""
        try:
            return pd.read_csv(self.employees_file)
        except Exception as e:
            st.error(f"Error loading employees data: {e}")
            return pd.DataFrame()
    
    def load_attendance(self):
        """Load attendance data"""
        try:
            return pd.read_csv(self.attendance_file)
        except Exception as e:
            st.error(f"Error loading attendance data: {e}")
            return pd.DataFrame()
    
    def load_performance(self):
        """Load performance data"""
        try:
            return pd.read_csv(self.performance_file)
        except Exception as e:
            st.error(f"Error loading performance data: {e}")
            return pd.DataFrame()
    
    def save_employees(self, df):
        """Save employees data"""
        try:
            df.to_csv(self.employees_file, index=False)
            return True
        except Exception as e:
            st.error(f"Error saving employees data: {e}")
            return False
    
    def save_attendance(self, df):
        """Save attendance data"""
        try:
            df.to_csv(self.attendance_file, index=False)
            return True
        except Exception as e:
            st.error(f"Error saving attendance data: {e}")
            return False
    
    def save_performance(self, df):
        """Save performance data"""
        try:
            df.to_csv(self.performance_file, index=False)
            return True
        except Exception as e:
            st.error(f"Error saving performance data: {e}")
            return False
    
    def add_employee(self, employee_data):
        """Add new employee"""
        employees_df = self.load_employees()
        
        # Check if employee ID already exists
        if employee_data['employee_id'] in employees_df['employee_id'].values:
            return False, "Employee ID already exists"
        
        # Add new employee
        new_employee = pd.DataFrame([employee_data])
        employees_df = pd.concat([employees_df, new_employee], ignore_index=True)
        
        if self.save_employees(employees_df):
            return True, "Employee added successfully"
        return False, "Error saving employee data"
    
    def update_employee(self, employee_id, employee_data):
        """Update existing employee"""
        employees_df = self.load_employees()
        
        # Find employee index
        employee_index = employees_df[employees_df['employee_id'] == employee_id].index
        
        if len(employee_index) == 0:
            return False, "Employee not found"
        
        # Update employee data
        for key, value in employee_data.items():
            if key in employees_df.columns:
                employees_df.loc[employee_index[0], key] = value
        
        if self.save_employees(employees_df):
            return True, "Employee updated successfully"
        return False, "Error updating employee data"
    
    def delete_employee(self, employee_id):
        """Delete employee"""
        employees_df = self.load_employees()
        
        # Remove employee
        employees_df = employees_df[employees_df['employee_id'] != employee_id]
        
        if self.save_employees(employees_df):
            return True, "Employee deleted successfully"
        return False, "Error deleting employee data"
    
    def log_attendance(self, employee_id, status="Present", time_in=None, time_out=None):
        """Log attendance for an employee"""
        attendance_df = self.load_attendance()
        
        # Check if attendance already logged for today
        today = datetime.now().strftime('%Y-%m-%d')
        existing_record = attendance_df[
            (attendance_df['employee_id'] == employee_id) & 
            (attendance_df['date'] == today)
        ]
        
        if not existing_record.empty:
            return False, "Attendance already logged for today"
        
        # Create attendance record
        attendance_record = {
            'employee_id': employee_id,
            'date': today,
            'time_in': time_in or datetime.now().strftime('%H:%M:%S'),
            'time_out': time_out,
            'status': status
        }
        
        new_attendance = pd.DataFrame([attendance_record])
        attendance_df = pd.concat([attendance_df, new_attendance], ignore_index=True)
        
        if self.save_attendance(attendance_df):
            return True, "Attendance logged successfully"
        return False, "Error logging attendance"
    
    def add_performance_record(self, performance_data):
        """Add performance record"""
        performance_df = self.load_performance()
        
        # Check if record already exists for this employee and date
        existing_record = performance_df[
            (performance_df['employee_id'] == performance_data['employee_id']) & 
            (performance_df['date'] == performance_data['date'])
        ]
        
        if not existing_record.empty:
            return False, "Performance record already exists for this date"
        
        new_record = pd.DataFrame([performance_data])
        performance_df = pd.concat([performance_df, new_record], ignore_index=True)
        
        if self.save_performance(performance_df):
            return True, "Performance record added successfully"
        return False, "Error saving performance record"
    
    def get_employee_stats(self, employee_id, start_date=None, end_date=None):
        """Get statistics for a specific employee"""
        attendance_df = self.load_attendance()
        performance_df = self.load_performance()
        
        # Filter by employee
        emp_attendance = attendance_df[attendance_df['employee_id'] == employee_id]
        emp_performance = performance_df[performance_df['employee_id'] == employee_id]
        
        # Apply date filters if provided
        if start_date:
            emp_attendance = emp_attendance[emp_attendance['date'] >= start_date]
            emp_performance = emp_performance[emp_performance['date'] >= start_date]
        if end_date:
            emp_attendance = emp_attendance[emp_attendance['date'] <= end_date]
            emp_performance = emp_performance[emp_performance['date'] <= end_date]
        
        # Calculate statistics
        stats = {
            'total_days': len(emp_attendance),
            'present_days': len(emp_attendance[emp_attendance['status'] == 'Present']),
            'absent_days': len(emp_attendance[emp_attendance['status'] == 'Absent']),
            'attendance_rate': 0,
            'avg_tasks_completed': emp_performance['tasks_completed'].mean() if not emp_performance.empty else 0,
            'avg_quality_score': emp_performance['quality_score'].mean() if not emp_performance.empty else 0,
            'avg_productivity_score': emp_performance['productivity_score'].mean() if not emp_performance.empty else 0
        }
        
        if stats['total_days'] > 0:
            stats['attendance_rate'] = (stats['present_days'] / stats['total_days']) * 100
        
        return stats
    
    def get_department_stats(self):
        """Get statistics by department"""
        employees_df = self.load_employees()
        attendance_df = self.load_attendance()
        performance_df = self.load_performance()
        
        # Merge data
        merged_df = employees_df.merge(attendance_df, on='employee_id', how='left')
        merged_df = merged_df.merge(performance_df, on=['employee_id', 'date'], how='left')
        
        # Group by department
        dept_stats = merged_df.groupby('department').agg({
            'employee_id': 'count',
            'status': lambda x: (x == 'Present').sum() / len(x) * 100 if len(x) > 0 else 0,
            'tasks_completed': 'mean',
            'quality_score': 'mean',
            'productivity_score': 'mean'
        }).reset_index()
        
        dept_stats.columns = ['department', 'employee_count', 'attendance_rate', 
                             'avg_tasks', 'avg_quality', 'avg_productivity']
        
        return dept_stats