"""
Google Forms Integration Helper
This file shows how to connect your Google Forms to the Streamlit Dashboard
"""

import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import json

# Required Google Sheets API scopes
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

def setup_google_sheets_connection():
    """
    Setup Google Sheets connection using service account credentials
    
    Steps to set up:
    1. Go to Google Cloud Console
    2. Create a new project or select existing
    3. Enable Google Sheets API and Google Drive API
    4. Create service account credentials
    5. Download the JSON key file
    6. Share your Google Sheets with the service account email
    """
    
    # Replace with your service account credentials file path
    SERVICE_ACCOUNT_FILE = 'path/to/your/service-account-key.json'
    
    try:
        credentials = Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, 
            scopes=SCOPES
        )
        
        client = gspread.authorize(credentials)
        return client
        
    except Exception as e:
        print(f"Error connecting to Google Sheets: {e}")
        return None

def read_daily_checkins(client, spreadsheet_id, worksheet_name="Daily Check-ins"):
    """
    Read daily check-in data from Google Sheets
    
    Expected columns in your Google Form responses:
    - Timestamp
    - رقم الموظف (Employee ID)
    - الاسم (Name)
    - القسم (Department)
    - موقع العمل (Work Location)
    - وقت بدء العمل (Start Time)
    - المهام المخطط لها اليوم (Today's Planned Tasks)
    - حالة مهام الأمس (Yesterday's Task Status)
    - التحديات والعوائق (Challenges/Blockers)
    - نسبة الإنجاز المتوقعة (Expected Completion %)
    """
    
    try:
        spreadsheet = client.open_by_key(spreadsheet_id)
        worksheet = spreadsheet.worksheet(worksheet_name)
        
        # Get all records
        records = worksheet.get_all_records()
        
        # Convert to DataFrame
        df = pd.DataFrame(records)
        
        # Clean and standardize column names
        column_mapping = {
            'Timestamp': 'timestamp',
            'رقم الموظف': 'employee_id',
            'الاسم': 'name',
            'القسم': 'department',
            'موقع العمل': 'work_location',
            'وقت بدء العمل': 'start_time',
            'المهام المخطط لها اليوم': 'planned_tasks',
            'حالة مهام الأمس': 'yesterday_status',
            'التحديات والعوائق': 'challenges',
            'نسبة الإنجاز المتوقعة': 'completion_percentage'
        }
        
        # Rename columns if they exist
        for old_name, new_name in column_mapping.items():
            if old_name in df.columns:
                df = df.rename(columns={old_name: new_name})
        
        # Convert timestamp to datetime
        if 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Convert completion percentage to numeric
        if 'completion_percentage' in df.columns:
            df['completion_percentage'] = pd.to_numeric(df['completion_percentage'], errors='coerce')
        
        return df
        
    except Exception as e:
        print(f"Error reading daily check-ins: {e}")
        return pd.DataFrame()

def read_weekly_progress(client, spreadsheet_id, worksheet_name="Weekly Progress"):
    """
    Read weekly progress data from Google Sheets
    
    Expected columns:
    - Timestamp
    - الأسبوع (Week of)
    - رقم الموظف (Employee ID)
    - الاسم (Name)
    - المشاريع النشطة (Active Projects)
    - المهام المكتملة (Completed Tasks)
    - المهام قيد التنفيذ (In Progress Tasks)
    - المهام المتأخرة (Delayed Tasks)
    - أهداف الأسبوع القادم (Next Week Goals)
    """
    
    try:
        spreadsheet = client.open_by_key(spreadsheet_id)
        worksheet = spreadsheet.worksheet(worksheet_name)
        
        records = worksheet.get_all_records()
        df = pd.DataFrame(records)
        
        column_mapping = {
            'Timestamp': 'timestamp',
            'الأسبوع': 'week_of',
            'رقم الموظف': 'employee_id',
            'الاسم': 'name',
            'المشاريع النشطة': 'active_projects',
            'المهام المكتملة': 'completed_tasks',
            'المهام قيد التنفيذ': 'in_progress_tasks',
            'المهام المتأخرة': 'delayed_tasks',
            'أهداف الأسبوع القادم': 'next_week_goals'
        }
        
        for old_name, new_name in column_mapping.items():
            if old_name in df.columns:
                df = df.rename(columns={old_name: new_name})
        
        # Convert numeric columns
        numeric_columns = ['active_projects', 'completed_tasks', 'in_progress_tasks', 'delayed_tasks']
        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        return df
        
    except Exception as e:
        print(f"Error reading weekly progress: {e}")
        return pd.DataFrame()

def send_notification_to_employee(client, spreadsheet_id, employee_id, message):
    """
    Send notification to employee by adding to notifications sheet
    """
    
    try:
        spreadsheet = client.open_by_key(spreadsheet_id)
        
        # Try to get notifications worksheet, create if doesn't exist
        try:
            notifications_sheet = spreadsheet.worksheet("Notifications")
        except:
            notifications_sheet = spreadsheet.add_worksheet(title="Notifications", rows="1000", cols="10")
            # Add headers
            notifications_sheet.append_row([
                "Timestamp", "Employee ID", "Message", "Status", "Priority"
            ])
        
        # Add notification
        notifications_sheet.append_row([
            pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S'),
            employee_id,
            message,
            "Pending",
            "Normal"
        ])
        
        return True
        
    except Exception as e:
        print(f"Error sending notification: {e}")
        return False

# Example usage and configuration
GOOGLE_FORMS_SETUP = {
    "daily_form_url": "https://forms.gle/your-daily-form-id",
    "weekly_form_url": "https://forms.gle/your-weekly-form-id",
    "spreadsheet_id": "your-google-sheets-id-here",
    "service_account_email": "your-service-account@project.iam.gserviceaccount.com"
}

# Sample Google Form Questions in Arabic
DAILY_FORM_QUESTIONS = {
    "ar": [
        "التاريخ (Date)",
        "رقم الموظف (Employee ID)",
        "الاسم (Name)",
        "القسم (Department)",
        "موقع العمل (Work Location) - مكتب/منزل/ميداني",
        "وقت بدء العمل (Start Time)",
        "المهام المخطط لها اليوم (Today's Planned Tasks)",
        "حالة مهام الأمس (Yesterday's Task Status) - مكتمل/قيد التنفيذ/متأخر",
        "التحديات والعوائق (Challenges/Blockers)",
        "نسبة الإنجاز المتوقعة (Expected Completion %) - 0-100"
    ]
}

WEEKLY_FORM_QUESTIONS = {
    "ar": [
        "الأسبوع (Week of)",
        "رقم الموظف (Employee ID)",
        "الاسم (Name)",
        "المشاريع النشطة (Active Projects) - عدد",
        "المهام المكتملة (Completed Tasks) - عدد",
        "المهام قيد التنفيذ (In Progress Tasks) - عدد",
        "المهام المتأخرة (Delayed Tasks) - عدد",
        "أهداف الأسبوع القادم (Next Week Goals)"
    ]
}

def print_setup_instructions():
    """Print setup instructions for Google Forms integration"""
    
    print("""
    🔧 إعداد تكامل Google Forms مع لوحة التحكم
    
    الخطوات المطلوبة:
    
    1️⃣ إنشاء Google Forms:
    - إنشاء نموذج للتسجيل اليومي
    - إنشاء نموذج للتقرير الأسبوعي
    - ربط النماذج بـ Google Sheets
    
    2️⃣ إعداد Google Cloud API:
    - فتح Google Cloud Console
    - تفعيل Google Sheets API و Google Drive API
    - إنشاء Service Account
    - تحميل ملف المفاتيح JSON
    
    3️⃣ مشاركة Google Sheets:
    - مشاركة الجداول مع إيميل Service Account
    - إعطاء صلاحية التحرير
    
    4️⃣ تحديث الكود:
    - إضافة مسار ملف المفاتيح
    - إضافة ID الجداول
    - تشغيل لوحة التحكم
    
    📧 للمساعدة التقنية: تواصل مع فريق تقنية المعلومات
    """)

if __name__ == "__main__":
    print_setup_instructions() 