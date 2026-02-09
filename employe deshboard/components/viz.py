import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import streamlit as st

class VisualizationManager:
    def __init__(self):
        pass
    
    def create_attendance_chart(self, attendance_df, group_by='department'):
        """Create attendance visualization chart"""
        if attendance_df.empty:
            return None
        
        # Group by specified column and calculate attendance rate
        if group_by in attendance_df.columns:
            grouped = attendance_df.groupby(group_by).agg({
                'status': lambda x: (x == 'Present').sum() / len(x) * 100
            }).reset_index()
            grouped.columns = [group_by, 'attendance_rate']
            
            fig = px.bar(grouped, x=group_by, y='attendance_rate',
                        title=f'Attendance Rate by {group_by.title()}',
                        labels={group_by: group_by.title(), 'attendance_rate': 'Attendance Rate (%)'},
                        color='attendance_rate',
                        color_continuous_scale='viridis')
            
            fig.update_layout(height=400)
            return fig
        return None
    
    def create_performance_scatter(self, performance_df, x_col='tasks_completed', y_col='quality_score'):
        """Create performance scatter plot"""
        if performance_df.empty:
            return None
            
        fig = px.scatter(performance_df, x=x_col, y=y_col, 
                        color='productivity_score',
                        size='productivity_score',
                        hover_data=['employee_id'],
                        title='Performance Scatter Plot',
                        labels={
                            x_col: x_col.replace('_', ' ').title(),
                            y_col: y_col.replace('_', ' ').title(),
                            'productivity_score': 'Productivity Score'
                        })
        
        fig.update_layout(height=400)
        return fig
    
    def create_department_pie_chart(self, dept_stats):
        """Create department distribution pie chart"""
        if dept_stats.empty:
            return None
            
        fig = px.pie(dept_stats, values='employee_count', names='department',
                    title='Employee Distribution by Department',
                    color_discrete_sequence=px.colors.qualitative.Set3)
        
        fig.update_layout(height=400)
        return fig
    
    def create_performance_trend(self, performance_df, employee_id=None):
        """Create performance trend line chart"""
        if performance_df.empty:
            return None
        
        # Filter by employee if specified
        if employee_id:
            performance_df = performance_df[performance_df['employee_id'] == employee_id]
            title = f'Performance Trend for Employee {employee_id}'
        else:
            # Group by date for overall trend
            performance_df = performance_df.groupby('date').agg({
                'tasks_completed': 'mean',
                'quality_score': 'mean',
                'productivity_score': 'mean'
            }).reset_index()
            title = 'Overall Performance Trend'
        
        if performance_df.empty:
            return None
        
        # Convert date to datetime for proper sorting
        performance_df['date'] = pd.to_datetime(performance_df['date'])
        performance_df = performance_df.sort_values('date')
        
        fig = go.Figure()
        
        # Add traces for different metrics
        metrics = ['tasks_completed', 'quality_score', 'productivity_score']
        colors = ['blue', 'green', 'orange']
        names = ['Tasks Completed', 'Quality Score', 'Productivity Score']
        
        for metric, color, name in zip(metrics, colors, names):
            if metric in performance_df.columns:
                fig.add_trace(go.Scatter(
                    x=performance_df['date'],
                    y=performance_df[metric],
                    mode='lines+markers',
                    name=name,
                    line=dict(color=color, width=2),
                    marker=dict(size=6)
                ))
        
        fig.update_layout(
            title=title,
            xaxis_title='Date',
            yaxis_title='Score',
            height=400,
            hovermode='x unified'
        )
        
        return fig
    
    def create_productivity_heatmap(self, performance_df):
        """Create productivity heatmap by day of week and hour"""
        if performance_df.empty:
            return None
        
        # This would require time data - for now create a simple heatmap
        # based on productivity scores by employee and date
        pivot_data = performance_df.pivot_table(
            values='productivity_score',
            index='employee_id',
            columns='date',
            aggfunc='mean'
        )
        
        if pivot_data.empty:
            return None
        
        fig = go.Figure(data=go.Heatmap(
            z=pivot_data.values,
            x=pivot_data.columns,
            y=pivot_data.index,
            colorscale='Viridis',
            hoverongaps=False
        ))
        
        fig.update_layout(
            title='Productivity Heatmap',
            xaxis_title='Date',
            yaxis_title='Employee ID',
            height=400
        )
        
        return fig
    
    def create_leaderboard(self, performance_df, top_n=10):
        """Create top performers leaderboard"""
        if performance_df.empty:
            return None
        
        # Calculate average scores by employee
        leaderboard = performance_df.groupby('employee_id').agg({
            'tasks_completed': 'mean',
            'quality_score': 'mean',
            'productivity_score': 'mean'
        }).reset_index()
        
        # Calculate overall score (weighted average)
        leaderboard['overall_score'] = (
            leaderboard['tasks_completed'] * 0.3 +
            leaderboard['quality_score'] * 0.4 +
            leaderboard['productivity_score'] * 0.3
        )
        
        # Sort and get top performers
        leaderboard = leaderboard.nlargest(top_n, 'overall_score')
        
        fig = px.bar(leaderboard, x='employee_id', y='overall_score',
                    title=f'Top {top_n} Performers Leaderboard',
                    labels={'employee_id': 'Employee ID', 'overall_score': 'Overall Score'},
                    color='overall_score',
                    color_continuous_scale='Bluered')
        
        fig.update_layout(height=400)
        return fig
    
    def create_kpi_dashboard(self, attendance_df, performance_df):
        """Create KPI summary dashboard"""
        if attendance_df.empty and performance_df.empty:
            return None
        
        # Calculate KPIs
        total_employees = len(attendance_df['employee_id'].unique()) if not attendance_df.empty else 0
        total_attendance_records = len(attendance_df) if not attendance_df.empty else 0
        present_records = len(attendance_df[attendance_df['status'] == 'Present']) if not attendance_df.empty else 0
        attendance_rate = (present_records / total_attendance_records * 100) if total_attendance_records > 0 else 0
        
        avg_tasks = performance_df['tasks_completed'].mean() if not performance_df.empty else 0
        avg_quality = performance_df['quality_score'].mean() if not performance_df.empty else 0
        avg_productivity = performance_df['productivity_score'].mean() if not performance_df.empty else 0
        
        # Create indicator charts
        fig = go.Figure()
        
        # Add KPI indicators
        kpis = [
            {'title': 'Total Employees', 'value': total_employees, 'suffix': ''},
            {'title': 'Attendance Rate', 'value': attendance_rate, 'suffix': '%'},
            {'title': 'Avg Tasks Completed', 'value': avg_tasks, 'suffix': ''},
            {'title': 'Avg Quality Score', 'value': avg_quality, 'suffix': ''},
            {'title': 'Avg Productivity', 'value': avg_productivity, 'suffix': ''}
        ]
        
        # Create subplots for KPIs
        fig = make_subplots(
            rows=2, cols=3,
            subplot_titles=[kpi['title'] for kpi in kpis],
            vertical_spacing=0.15,
            horizontal_spacing=0.1
        )
        
        for i, kpi in enumerate(kpis):
            row = (i // 3) + 1
            col = (i % 3) + 1
            
            fig.add_trace(
                go.Indicator(
                    mode="number",
                    value=kpi['value'],
                    number={'suffix': kpi['suffix']},
                    title={'text': kpi['title']},
                ),
                row=row, col=col
            )
        
        fig.update_layout(
            title='Key Performance Indicators',
            height=300,
            showlegend=False
        )
        
        return fig
    
    def create_time_series_analysis(self, df, date_column, value_column, title="Time Series Analysis"):
        """Create time series analysis chart"""
        if df.empty or date_column not in df.columns or value_column not in df.columns:
            return None
        
        # Convert date column to datetime
        df[date_column] = pd.to_datetime(df[date_column])
        df = df.sort_values(date_column)
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=df[date_column],
            y=df[value_column],
            mode='lines+markers',
            name=value_column,
            line=dict(width=2),
            marker=dict(size=4)
        ))
        
        fig.update_layout(
            title=title,
            xaxis_title='Date',
            yaxis_title=value_column.replace('_', ' ').title(),
            height=400
        )
        
        return fig

# Import for make_subplots
from plotly.subplots import make_subplots