import streamlit as st
import json
import time
from datetime import datetime, timedelta
import uuid
from typing import List, Dict, Any
import pandas as pd

class NotificationSystem:
    """Advanced real-time notification system for hospital management"""
    
    def __init__(self):
        if 'notifications' not in st.session_state:
            st.session_state['notifications'] = []
        if 'notification_settings' not in st.session_state:
            st.session_state['notification_settings'] = {
                'enable_sound': True,
                'enable_popup': True,
                'auto_dismiss': True,
                'dismiss_time': 5000,  # milliseconds
                'notification_types': {
                    'emergency': True,
                    'appointment': True,
                    'system': True,
                    'reminder': True
                }
            }
    
    def add_notification(self, title: str, message: str, type: str = "info", 
                        priority: str = "normal", action_url: str = None,
                        auto_dismiss: bool = True, user_id: str = None):
        """Add a new notification to the system"""
        notification = {
            'id': str(uuid.uuid4()),
            'title': title,
            'message': message,
            'type': type,  # success, error, warning, info, emergency
            'priority': priority,  # low, normal, high, urgent
            'timestamp': datetime.now().isoformat(),
            'read': False,
            'dismissed': False,
            'action_url': action_url,
            'auto_dismiss': auto_dismiss,
            'user_id': user_id
        }
        
        st.session_state['notifications'].insert(0, notification)
        
        # Keep only last 100 notifications
        if len(st.session_state['notifications']) > 100:
            st.session_state['notifications'] = st.session_state['notifications'][:100]
        
        return notification['id']
    
    def get_notifications(self, user_id: str = None, unread_only: bool = False,
                         limit: int = None) -> List[Dict[Any, Any]]:
        """Get notifications with optional filtering"""
        notifications = st.session_state['notifications']
        
        # Filter by user
        if user_id:
            notifications = [n for n in notifications if n.get('user_id') == user_id or n.get('user_id') is None]
        
        # Filter unread only
        if unread_only:
            notifications = [n for n in notifications if not n['read']]
        
        # Apply limit
        if limit:
            notifications = notifications[:limit]
        
        return notifications
    
    def mark_as_read(self, notification_id: str):
        """Mark notification as read"""
        for notification in st.session_state['notifications']:
            if notification['id'] == notification_id:
                notification['read'] = True
                break
    
    def dismiss_notification(self, notification_id: str):
        """Dismiss a notification"""
        for notification in st.session_state['notifications']:
            if notification['id'] == notification_id:
                notification['dismissed'] = True
                break
    
    def clear_all_notifications(self, user_id: str = None):
        """Clear all notifications"""
        if user_id:
            st.session_state['notifications'] = [
                n for n in st.session_state['notifications'] 
                if n.get('user_id') != user_id and n.get('user_id') is not None
            ]
        else:
            st.session_state['notifications'] = []
    
    def display_notification_center(self):
        """Display the notification center widget"""
        notifications = self.get_notifications(limit=10)
        unread_count = len([n for n in notifications if not n['read']])
        
        # Notification header
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.subheader(f"🔔 Notifications ({unread_count} unread)")
        
        with col2:
            if st.button("Mark All Read", key="mark_all_read"):
                for notification in notifications:
                    notification['read'] = True
                st.rerun()
        
        with col3:
            if st.button("Clear All", key="clear_all"):
                self.clear_all_notifications()
                st.rerun()
        
        # Display notifications
        if notifications:
            for notification in notifications:
                self._render_notification_item(notification)
        else:
            st.info("No notifications to display")
    
    def _render_notification_item(self, notification: Dict[Any, Any]):
        """Render individual notification item"""
        if notification['dismissed']:
            return
        
        # Determine notification style based on type and priority
        type_config = {
            'emergency': {'color': '#ff4757', 'icon': '🚨'},
            'error': {'color': '#ff6b6b', 'icon': '❌'},
            'warning': {'color': '#ffa502', 'icon': '⚠️'},
            'success': {'color': '#2ed573', 'icon': '✅'},
            'info': {'color': '#5352ed', 'icon': 'ℹ️'}
        }
        
        config = type_config.get(notification['type'], type_config['info'])
        read_style = "opacity: 0.6;" if notification['read'] else ""
        
        # Format timestamp
        timestamp = datetime.fromisoformat(notification['timestamp'])
        time_ago = self._format_time_ago(timestamp)
        
        # Render notification
        st.markdown(f"""
        <div style="
            border-left: 4px solid {config['color']};
            background: white;
            padding: 15px;
            margin: 10px 0;
            border-radius: 0 8px 8px 0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            {read_style}
        ">
            <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                <div style="flex: 1;">
                    <div style="display: flex; align-items: center; margin-bottom: 5px;">
                        <span style="font-size: 18px; margin-right: 8px;">{config['icon']}</span>
                        <strong style="color: {config['color']};">{notification['title']}</strong>
                        {f'<span style="background: {config["color"]}; color: white; padding: 2px 6px; border-radius: 10px; font-size: 10px; margin-left: 8px;">{notification["priority"].upper()}</span>' if notification['priority'] != 'normal' else ''}
                    </div>
                    <div style="color: #333; margin-bottom: 8px;">{notification['message']}</div>
                    <div style="color: #666; font-size: 12px;">{time_ago}</div>
                </div>
                <div style="margin-left: 15px;">
                    <button onclick="markAsRead('{notification['id']}')" 
                            style="background: none; border: none; cursor: pointer; font-size: 16px;"
                            title="Mark as read">👁️</button>
                    <button onclick="dismissNotification('{notification['id']}')" 
                            style="background: none; border: none; cursor: pointer; font-size: 14px;"
                            title="Dismiss">✖️</button>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Action button if provided
        if notification.get('action_url'):
            if st.button(f"Take Action", key=f"action_{notification['id']}"):
                st.info(f"Action triggered for: {notification['title']}")
    
    def _format_time_ago(self, timestamp: datetime) -> str:
        """Format timestamp as time ago"""
        now = datetime.now()
        diff = now - timestamp
        
        if diff.seconds < 60:
            return "Just now"
        elif diff.seconds < 3600:
            minutes = diff.seconds // 60
            return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
        elif diff.seconds < 86400:
            hours = diff.seconds // 3600
            return f"{hours} hour{'s' if hours != 1 else ''} ago"
        else:
            days = diff.days
            return f"{days} day{'s' if days != 1 else ''} ago"
    
    def display_notification_settings(self):
        """Display notification settings panel"""
        st.subheader("🔧 Notification Settings")
        
        settings = st.session_state['notification_settings']
        
        # General settings
        col1, col2 = st.columns(2)
        
        with col1:
            settings['enable_sound'] = st.checkbox("Enable Sound", value=settings['enable_sound'])
            settings['enable_popup'] = st.checkbox("Enable Popup Notifications", value=settings['enable_popup'])
        
        with col2:
            settings['auto_dismiss'] = st.checkbox("Auto Dismiss", value=settings['auto_dismiss'])
            if settings['auto_dismiss']:
                settings['dismiss_time'] = st.slider("Dismiss Time (seconds)", 1, 30, settings['dismiss_time']//1000) * 1000
        
        # Notification types
        st.subheader("Notification Types")
        
        for ntype, enabled in settings['notification_types'].items():
            settings['notification_types'][ntype] = st.checkbox(
                f"Enable {ntype.title()} Notifications", 
                value=enabled,
                key=f"notif_type_{ntype}"
            )
        
        if st.button("Save Settings"):
            st.session_state['notification_settings'] = settings
            st.success("Notification settings saved!")
    
    def send_realtime_notifications(self):
        """Send sample real-time notifications for demonstration"""
        sample_notifications = [
            {
                'title': 'New Patient Check-in',
                'message': 'John Doe has checked in for appointment',
                'type': 'info',
                'priority': 'normal'
            },
            {
                'title': 'Emergency Alert',
                'message': 'Emergency patient in Room 105 requires immediate attention',
                'type': 'emergency',
                'priority': 'urgent'
            },
            {
                'title': 'Appointment Reminder',
                'message': 'Patient Jane Smith has appointment in 15 minutes',
                'type': 'warning',
                'priority': 'high'
            },
            {
                'title': 'Lab Results Ready',
                'message': 'Blood test results for Patient PT003 are ready for review',
                'type': 'success',
                'priority': 'normal'
            },
            {
                'title': 'System Update',
                'message': 'Hospital management system will undergo maintenance at 2 AM',
                'type': 'info',
                'priority': 'low'
            }
        ]
        
        import random
        notification = random.choice(sample_notifications)
        
        return self.add_notification(
            title=notification['title'],
            message=notification['message'],
            type=notification['type'],
            priority=notification['priority']
        )

# Global notification system instance
notification_system = NotificationSystem()

def display_realtime_notifications():
    """Display real-time notifications widget in sidebar"""
    with st.sidebar:
        st.markdown("---")
        
        # Quick notification controls
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔔", help="Show notifications"):
                st.session_state['show_notifications'] = True
        
        with col2:
            unread_count = len([n for n in notification_system.get_notifications() if not n['read']])
            if unread_count > 0:
                st.markdown(f"**{unread_count}** unread")
        
        # Auto-generate sample notifications every 30 seconds
        if st.button("📢 Generate Sample Alert"):
            notification_system.send_realtime_notifications()
            st.success("Sample notification sent!")

def show_notification_panel():
    """Show full notification panel"""
    st.title("🔔 Notification Center")
    
    tab1, tab2 = st.tabs(["📋 Notifications", "⚙️ Settings"])
    
    with tab1:
        notification_system.display_notification_center()
    
    with tab2:
        notification_system.display_notification_settings()