import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression
import streamlit as st

class ProductivityAnalyzer:
    def __init__(self, data_manager):
        self.data_manager = data_manager
    
    def calculate_productivity_score(self, tasks_completed, quality_score, time_efficiency=1.0):
        """Calculate productivity score based on multiple factors"""
        # Weighted scoring system
        task_weight = 0.4
        quality_weight = 0.4
        efficiency_weight = 0.2
        
        # Normalize scores (assuming 0-10 scale)
        normalized_tasks = min(tasks_completed / 10, 1.0)  # Cap at 1.0
        normalized_quality = quality_score / 10
        normalized_efficiency = min(time_efficiency, 1.0)
        
        productivity_score = (
            normalized_tasks * task_weight +
            normalized_quality * quality_weight +
            normalized_efficiency * efficiency_weight
        ) * 10  # Scale back to 0-10
        
        return round(productivity_score, 2)
    
    def analyze_productivity_trends(self, employee_id=None, days=30):
        """Analyze productivity trends over time"""
        performance_df = self.data_manager.load_performance()
        
        if performance_df.empty:
            return None, "No performance data available"
        
        # Filter data
        if employee_id:
            performance_df = performance_df[performance_df['employee_id'] == employee_id]
        
        # Filter by date range
        if days:
            cutoff_date = datetime.now() - timedelta(days=days)
            performance_df = performance_df[
                pd.to_datetime(performance_df['date']) >= cutoff_date
            ]
        
        if performance_df.empty:
            return None, "No data for specified period"
        
        # Calculate productivity scores
        performance_df['productivity_score'] = performance_df.apply(
            lambda row: self.calculate_productivity_score(
                row['tasks_completed'], 
                row['quality_score']
            ), axis=1
        )
        
        # Group by date for trend analysis
        daily_trends = performance_df.groupby('date').agg({
            'productivity_score': 'mean',
            'tasks_completed': 'mean',
            'quality_score': 'mean'
        }).reset_index()
        
        daily_trends['date'] = pd.to_datetime(daily_trends['date'])
        daily_trends = daily_trends.sort_values('date')
        
        # Calculate trend indicators
        if len(daily_trends) > 1:
            # Linear regression for trend
            X = np.arange(len(daily_trends)).reshape(-1, 1)
            y = daily_trends['productivity_score'].values
            
            model = LinearRegression()
            model.fit(X, y)
            
            trend_slope = model.coef_[0]
            trend_direction = "Improving" if trend_slope > 0 else "Declining" if trend_slope < 0 else "Stable"
            
            # Calculate statistics
            stats = {
                'average_productivity': daily_trends['productivity_score'].mean(),
                'highest_productivity': daily_trends['productivity_score'].max(),
                'lowest_productivity': daily_trends['productivity_score'].min(),
                'trend_slope': trend_slope,
                'trend_direction': trend_direction,
                'total_days': len(daily_trends)
            }
        else:
            stats = {
                'average_productivity': daily_trends['productivity_score'].iloc[0] if not daily_trends.empty else 0,
                'highest_productivity': daily_trends['productivity_score'].iloc[0] if not daily_trends.empty else 0,
                'lowest_productivity': daily_trends['productivity_score'].iloc[0] if not daily_trends.empty else 0,
                'trend_slope': 0,
                'trend_direction': 'Insufficient data',
                'total_days': len(daily_trends)
            }
        
        return {
            'trends': daily_trends,
            'statistics': stats
        }, "Trend analysis completed"
    
    def compare_productivity(self, employee_id, department=None, role=None):
        """Compare employee productivity with peers"""
        performance_df = self.data_manager.load_performance()
        employees_df = self.data_manager.load_employees()
        
        if performance_df.empty or employees_df.empty:
            return None, "Insufficient data for comparison"
        
        # Merge performance with employee data
        merged_df = performance_df.merge(employees_df[['employee_id', 'department', 'role']], 
                                       on='employee_id', how='left')
        
        # Get target employee data
        employee_data = merged_df[merged_df['employee_id'] == employee_id]
        
        if employee_data.empty:
            return None, "Employee data not found"
        
        # Filter comparison group
        if department:
            comparison_group = merged_df[merged_df['department'] == department]
        elif role:
            comparison_group = merged_df[merged_df['role'] == role]
        else:
            comparison_group = merged_df
        
        # Calculate average productivity scores
        comparison_group['productivity_score'] = comparison_group.apply(
            lambda row: self.calculate_productivity_score(
                row['tasks_completed'], 
                row['quality_score']
            ), axis=1
        )
        
        # Group by employee
        employee_averages = comparison_group.groupby('employee_id').agg({
            'productivity_score': 'mean',
            'tasks_completed': 'mean',
            'quality_score': 'mean'
        }).reset_index()
        
        # Get target employee score
        target_score = employee_averages[employee_averages['employee_id'] == employee_id]
        target_score_value = target_score['productivity_score'].iloc[0] if not target_score.empty else 0
        
        # Calculate percentiles
        all_scores = employee_averages['productivity_score'].values
        percentile = (np.sum(all_scores < target_score_value) / len(all_scores)) * 100
        
        # Ranking
        employee_averages = employee_averages.sort_values('productivity_score', ascending=False)
        employee_averages['rank'] = range(1, len(employee_averages) + 1)
        target_rank = employee_averages[employee_averages['employee_id'] == employee_id]['rank'].iloc[0] if not target_score.empty else 0
        
        comparison_result = {
            'employee_id': employee_id,
            'employee_score': target_score_value,
            'percentile': round(percentile, 1),
            'rank': target_rank,
            'total_employees': len(employee_averages),
            'average_score': employee_averages['productivity_score'].mean(),
            'comparison_data': employee_averages.head(10)  # Top 10 for display
        }
        
        return comparison_result, "Comparison completed"
    
    def identify_productivity_patterns(self, days=90):
        """Identify productivity patterns and insights"""
        performance_df = self.data_manager.load_performance()
        
        if performance_df.empty:
            return None, "No performance data available"
        
        # Filter by date range
        if days:
            cutoff_date = datetime.now() - timedelta(days=days)
            performance_df = performance_df[
                pd.to_datetime(performance_df['date']) >= cutoff_date
            ]
        
        # Calculate productivity scores
        performance_df['productivity_score'] = performance_df.apply(
            lambda row: self.calculate_productivity_score(
                row['tasks_completed'], 
                row['quality_score']
            ), axis=1
        )
        
        # Add day of week and month
        performance_df['date'] = pd.to_datetime(performance_df['date'])
        performance_df['day_of_week'] = performance_df['date'].dt.day_name()
        performance_df['month'] = performance_df['date'].dt.month_name()
        
        # Analyze by day of week
        day_analysis = performance_df.groupby('day_of_week').agg({
            'productivity_score': ['mean', 'std'],
            'tasks_completed': 'mean',
            'quality_score': 'mean'
        }).round(2)
        
        # Analyze by month
        month_analysis = performance_df.groupby('month').agg({
            'productivity_score': ['mean', 'std'],
            'tasks_completed': 'mean',
            'quality_score': 'mean'
        }).round(2)
        
        # Identify high/low performing periods
        overall_avg = performance_df['productivity_score'].mean()
        high_performance_days = day_analysis[day_analysis[('productivity_score', 'mean')] > overall_avg]
        low_performance_days = day_analysis[day_analysis[('productivity_score', 'mean')] < overall_avg]
        
        patterns = {
            'day_analysis': day_analysis,
            'month_analysis': month_analysis,
            'high_performance_days': high_performance_days.index.tolist(),
            'low_performance_days': low_performance_days.index.tolist(),
            'overall_average': round(overall_avg, 2)
        }
        
        return patterns, "Pattern analysis completed"
    
    def generate_productivity_recommendations(self, employee_id):
        """Generate productivity improvement recommendations"""
        # Get employee performance data
        performance_data, _ = self.analyze_productivity_trends(employee_id, days=30)
        comparison_data, _ = self.compare_productivity(employee_id)
        
        if not performance_data or not comparison_data:
            return ["Insufficient data for recommendations"]
        
        recommendations = []
        stats = performance_data['statistics']
        comparison = comparison_data
        
        # Analyze trend
        if stats['trend_direction'] == "Declining":
            recommendations.append("⚠️ Productivity trend is declining. Focus on time management and task prioritization.")
        elif stats['trend_direction'] == "Stable":
            recommendations.append("📊 Productivity is stable. Look for opportunities to improve quality scores.")
        
        # Compare with peers
        if comparison['percentile'] < 50:
            recommendations.append("👥 Below 50th percentile compared to peers. Consider seeking mentorship or additional training.")
        elif comparison['percentile'] > 80:
            recommendations.append("🏆 Above 80th percentile! Consider mentoring other team members.")
        
        # Analyze individual metrics
        if stats['average_productivity'] < 7:
            recommendations.append("📈 Overall productivity below 7. Focus on completing more tasks while maintaining quality.")
        
        # Add general recommendations
        recommendations.extend([
            "📝 Set daily goals and track progress",
            "⏱️ Use time-tracking tools to identify inefficiencies",
            "📚 Invest in skill development for your role",
            "👥 Regular check-ins with supervisor for feedback"
        ])
        
        return recommendations