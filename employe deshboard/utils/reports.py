import pandas as pd
from fpdf import FPDF
from datetime import datetime
import streamlit as st
import io
import base64

class ReportGenerator:
    def __init__(self, data_manager):
        self.data_manager = data_manager
    
    def generate_employee_report(self, employee_id, start_date=None, end_date=None):
        """Generate detailed report for a specific employee"""
        # Get employee data
        employees_df = self.data_manager.load_employees()
        employee = employees_df[employees_df['employee_id'] == employee_id]
        
        if employee.empty:
            return None, "Employee not found"
        
        employee = employee.iloc[0]
        
        # Get statistics
        stats = self.data_manager.get_employee_stats(employee_id, start_date, end_date)
        
        # Get attendance and performance data
        attendance_df = self.data_manager.load_attendance()
        performance_df = self.data_manager.load_performance()
        
        # Filter data
        emp_attendance = attendance_df[attendance_df['employee_id'] == employee_id]
        emp_performance = performance_df[performance_df['employee_id'] == employee_id]
        
        if start_date:
            emp_attendance = emp_attendance[emp_attendance['date'] >= start_date]
            emp_performance = emp_performance[emp_performance['date'] >= start_date]
        if end_date:
            emp_attendance = emp_attendance[emp_attendance['date'] <= end_date]
            emp_performance = emp_performance[emp_performance['date'] <= end_date]
        
        # Create report data
        report_data = {
            'employee_info': {
                'ID': employee_id,
                'Name': employee['name'],
                'Department': employee['department'],
                'Role': employee['role'],
                'Email': employee['email'],
                'Hire Date': employee['hire_date']
            },
            'statistics': stats,
            'attendance_records': emp_attendance,
            'performance_records': emp_performance
        }
        
        return report_data, "Report generated successfully"
    
    def generate_department_report(self, department, start_date=None, end_date=None):
        """Generate report for a department"""
        # Get department data
        employees_df = self.data_manager.load_employees()
        dept_employees = employees_df[employees_df['department'] == department]
        
        if dept_employees.empty:
            return None, "No employees found in department"
        
        # Get department statistics
        dept_stats = self.data_manager.get_department_stats()
        dept_stat = dept_stats[dept_stats['department'] == department]
        
        # Get attendance and performance data for department
        attendance_df = self.data_manager.load_attendance()
        performance_df = self.data_manager.load_performance()
        
        # Filter by department employees
        dept_employee_ids = dept_employees['employee_id'].tolist()
        dept_attendance = attendance_df[attendance_df['employee_id'].isin(dept_employee_ids)]
        dept_performance = performance_df[performance_df['employee_id'].isin(dept_employee_ids)]
        
        # Apply date filters
        if start_date:
            dept_attendance = dept_attendance[dept_attendance['date'] >= start_date]
            dept_performance = dept_performance[dept_performance['date'] >= start_date]
        if end_date:
            dept_attendance = dept_attendance[dept_attendance['date'] <= end_date]
            dept_performance = dept_performance[dept_performance['date'] <= end_date]
        
        report_data = {
            'department': department,
            'employee_count': len(dept_employees),
            'statistics': dept_stat.iloc[0].to_dict() if not dept_stat.empty else {},
            'employees': dept_employees,
            'attendance_records': dept_attendance,
            'performance_records': dept_performance
        }
        
        return report_data, "Department report generated successfully"
    
    def export_to_csv(self, data, filename):
        """Export data to CSV"""
        try:
            # Convert to DataFrame if it's a dictionary
            if isinstance(data, dict):
                if 'attendance_records' in data:
                    df = data['attendance_records']
                elif 'performance_records' in data:
                    df = data['performance_records']
                else:
                    df = pd.DataFrame([data])
            else:
                df = data
            
            csv = df.to_csv(index=False)
            return csv
        except Exception as e:
            st.error(f"Error exporting to CSV: {e}")
            return None
    
    def generate_pdf_report(self, report_data, report_type="employee"):
        """Generate PDF report"""
        try:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            
            # Add title
            pdf.set_font("Arial", 'B', 16)
            if report_type == "employee":
                pdf.cell(200, 10, f"Employee Performance Report", ln=True, align='C')
                pdf.cell(200, 10, f"Employee ID: {report_data['employee_info']['ID']}", ln=True, align='C')
                pdf.cell(200, 10, f"Name: {report_data['employee_info']['Name']}", ln=True, align='C')
            else:
                pdf.cell(200, 10, f"Department Performance Report", ln=True, align='C')
                pdf.cell(200, 10, f"Department: {report_data['department']}", ln=True, align='C')
            
            pdf.ln(10)
            
            # Add report generation date
            pdf.set_font("Arial", size=10)
            pdf.cell(200, 8, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
            pdf.ln(5)
            
            # Add statistics
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(200, 10, "Key Statistics:", ln=True)
            pdf.set_font("Arial", size=10)
            
            if report_type == "employee":
                stats = report_data['statistics']
                pdf.cell(200, 8, f"Attendance Rate: {stats['attendance_rate']:.1f}%", ln=True)
                pdf.cell(200, 8, f"Total Days: {stats['total_days']}", ln=True)
                pdf.cell(200, 8, f"Present Days: {stats['present_days']}", ln=True)
                pdf.cell(200, 8, f"Average Tasks Completed: {stats['avg_tasks_completed']:.1f}", ln=True)
                pdf.cell(200, 8, f"Average Quality Score: {stats['avg_quality_score']:.1f}", ln=True)
                pdf.cell(200, 8, f"Average Productivity Score: {stats['avg_productivity_score']:.1f}", ln=True)
            else:
                stats = report_data['statistics']
                pdf.cell(200, 8, f"Employee Count: {stats.get('employee_count', 0)}", ln=True)
                pdf.cell(200, 8, f"Average Attendance Rate: {stats.get('attendance_rate', 0):.1f}%", ln=True)
                pdf.cell(200, 8, f"Average Tasks: {stats.get('avg_tasks', 0):.1f}", ln=True)
                pdf.cell(200, 8, f"Average Quality: {stats.get('avg_quality', 0):.1f}", ln=True)
                pdf.cell(200, 8, f"Average Productivity: {stats.get('avg_productivity', 0):.1f}", ln=True)
            
            # Save PDF to bytes
            pdf_bytes = pdf.output(dest='S').encode('latin-1')
            return pdf_bytes
            
        except Exception as e:
            st.error(f"Error generating PDF: {e}")
            return None
    
    def create_download_link(self, data, filename, file_type="csv"):
        """Create download link for reports"""
        if file_type == "csv":
            b64 = base64.b64encode(data.encode()).decode()
            href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">Download CSV Report</a>'
        elif file_type == "pdf":
            b64 = base64.b64encode(data).decode()
            href = f'<a href="data:application/pdf;base64,{b64}" download="{filename}">Download PDF Report</a>'
        
        return href