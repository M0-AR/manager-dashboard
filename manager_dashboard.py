import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import gspread
from google.oauth2.service_account import Credentials
import json
import time

# Page configuration
st.set_page_config(
    page_title="لوحة تحكم المدير - Manager Dashboard", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Arabic RTL Support
st.markdown("""
<style>
    .main .block-container {
        direction: rtl;
        text-align: right;
    }
    .stSelectbox label, .stMultiSelect label {
        direction: rtl;
        text-align: right;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
    .alert-card {
        background: #ff6b6b;
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 0.5rem 0;
    }
    .success-card {
        background: #51cf66;
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 0.5rem 0;
    }
    .rtl-text {
        direction: rtl;
        text-align: right;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'last_update' not in st.session_state:
    st.session_state.last_update = datetime.now()

def connect_to_sheets():
    """Connect to Google Sheets using service account"""
    try:
        # You'll need to add your service account credentials here
        # For now, we'll simulate the data
        return None
    except Exception as e:
        st.error(f"Connection error: {e}")
        return None

def load_sample_data():
    """Load sample data for demonstration"""
    # Daily Check-ins Data
    daily_data = pd.DataFrame({
        'timestamp': pd.date_range(start='2024-01-15', periods=50, freq='D'),
        'employee_id': ['EMP001', 'EMP002', 'EMP003', 'EMP004', 'EMP005'] * 10,
        'name': ['أحمد محمد', 'فاطمة علي', 'محمد حسن', 'سارة أحمد', 'علي محمود'] * 10,
        'department': ['تقنية المعلومات', 'الموارد البشرية', 'التسويق', 'المبيعات', 'التمويل'] * 10,
        'work_location': ['مكتب', 'منزل', 'ميداني', 'مكتب', 'منزل'] * 10,
        'start_time': ['09:00', '08:30', '09:15', '08:45', '09:30'] * 10,
        'planned_tasks': [
            'تطوير النظام الجديد',
            'مراجعة السياسات',
            'حملة إعلانية',
            'متابعة العملاء',
            'تحليل الميزانية'
        ] * 10,
        'yesterday_status': ['مكتمل', 'قيد التنفيذ', 'مكتمل', 'متأخر', 'مكتمل'] * 10,
        'completion_percentage': [85, 70, 90, 45, 88] * 10,
        'challenges': [
            'لا توجد',
            'نقص في الموارد',
            'تأخير من العميل',
            'مشاكل تقنية',
            'انتظار موافقات'
        ] * 10
    })
    
    # Weekly Progress Data
    weekly_data = pd.DataFrame({
        'week_of': pd.date_range(start='2024-01-01', periods=20, freq='W'),
        'employee_id': ['EMP001', 'EMP002', 'EMP003', 'EMP004'] * 5,
        'name': ['أحمد محمد', 'فاطمة علي', 'محمد حسن', 'سارة أحمد'] * 5,
        'active_projects': [3, 2, 4, 3] * 5,
        'completed_tasks': [12, 8, 15, 10] * 5,
        'in_progress_tasks': [5, 3, 7, 4] * 5,
        'delayed_tasks': [1, 2, 0, 3] * 5
    })
    
    return daily_data, weekly_data

def create_alert_system(daily_data):
    """Create alert system for tracking issues"""
    alerts = []
    
    # Check for employees with low completion rates
    low_performers = daily_data[daily_data['completion_percentage'] < 60]
    for _, emp in low_performers.iterrows():
        alerts.append({
            'type': 'تحذير',
            'employee': emp['name'],
            'message': f"معدل الإنجاز منخفض: {emp['completion_percentage']}%",
            'priority': 'عالي'
        })
    
    # Check for employees with challenges
    challenged = daily_data[daily_data['challenges'] != 'لا توجد']
    for _, emp in challenged.iterrows():
        alerts.append({
            'type': 'تنبيه',
            'employee': emp['name'],
            'message': f"تحدي: {emp['challenges']}",
            'priority': 'متوسط'
        })
    
    return alerts

def main():
    # Header
    st.title("🏢 لوحة تحكم المدير")
    st.markdown("### نظام متابعة الموظفين والمشاريع")
    
    # Sidebar
    st.sidebar.title("⚙️ الإعدادات")
    
    # Auto-refresh option
    auto_refresh = st.sidebar.checkbox("تحديث تلقائي كل 30 ثانية")
    if auto_refresh:
        time.sleep(30)
        st.rerun()
    
    # Department filter
    departments = ["الكل", "تقنية المعلومات", "الموارد البشرية", "التسويق", "المبيعات", "التمويل"]
    selected_dept = st.sidebar.selectbox("اختر القسم:", departments)
    
    # Date range filter
    date_range = st.sidebar.date_input(
        "نطاق التاريخ:",
        value=[datetime.now() - timedelta(days=7), datetime.now()],
        max_value=datetime.now()
    )
    
    # Load data
    daily_data, weekly_data = load_sample_data()
    
    # Filter data based on selection
    if selected_dept != "الكل":
        daily_data = daily_data[daily_data['department'] == selected_dept]
        weekly_data = weekly_data[weekly_data['name'].isin(daily_data['name'].unique())]
    
    # Main dashboard
    col1, col2, col3, col4 = st.columns(4)
    
    # KPI Cards
    with col1:
        st.markdown('<div class="metric-card rtl-text">', unsafe_allow_html=True)
        total_employees = len(daily_data['employee_id'].unique())
        st.metric("إجمالي الموظفين", total_employees)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card rtl-text">', unsafe_allow_html=True)
        avg_completion = daily_data['completion_percentage'].mean()
        st.metric("متوسط الإنجاز", f"{avg_completion:.1f}%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card rtl-text">', unsafe_allow_html=True)
        on_track = len(daily_data[daily_data['completion_percentage'] >= 70])
        st.metric("موظفين على المسار الصحيح", on_track)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-card rtl-text">', unsafe_allow_html=True)
        needs_attention = len(daily_data[daily_data['completion_percentage'] < 60])
        st.metric("يحتاج متابعة", needs_attention, delta=f"-{needs_attention}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Alerts Section
    st.markdown("---")
    st.subheader("🚨 التنبيهات والتحذيرات")
    
    alerts = create_alert_system(daily_data)
    
    if alerts:
        for alert in alerts[:5]:  # Show top 5 alerts
            if alert['priority'] == 'عالي':
                st.markdown(f'<div class="alert-card rtl-text">⚠️ <strong>{alert["type"]}</strong>: {alert["employee"]} - {alert["message"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="success-card rtl-text">ℹ️ <strong>{alert["type"]}</strong>: {alert["employee"]} - {alert["message"]}</div>', unsafe_allow_html=True)
    else:
        st.success("✅ لا توجد تنبيهات - جميع الموظفين يعملون بشكل جيد!")
    
    # Charts Section
    st.markdown("---")
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.subheader("📊 توزيع معدلات الإنجاز")
        fig_completion = px.histogram(
            daily_data, 
            x='completion_percentage',
            title="توزيع معدلات الإنجاز",
            labels={'completion_percentage': 'معدل الإنجاز (%)', 'count': 'عدد الموظفين'},
            color_discrete_sequence=['#667eea']
        )
        fig_completion.update_layout(
            font=dict(family="Arial", size=12),
            title_x=0.5
        )
        st.plotly_chart(fig_completion, use_container_width=True)
    
    with col_chart2:
        st.subheader("🏢 الموظفين حسب موقع العمل")
        location_counts = daily_data['work_location'].value_counts()
        fig_location = px.pie(
            values=location_counts.values,
            names=location_counts.index,
            title="توزيع مواقع العمل",
            color_discrete_sequence=['#667eea', '#764ba2', '#f093fb']
        )
        fig_location.update_layout(
            font=dict(family="Arial", size=12),
            title_x=0.5
        )
        st.plotly_chart(fig_location, use_container_width=True)
    
    # Detailed Employee Status
    st.markdown("---")
    st.subheader("👥 حالة الموظفين التفصيلية")
    
    # Create employee status dataframe
    employee_status = daily_data.groupby(['employee_id', 'name', 'department']).agg({
        'completion_percentage': 'mean',
        'challenges': lambda x: 'نعم' if any(x != 'لا توجد') else 'لا',
        'work_location': 'last'
    }).round(1)
    
    employee_status['الحالة'] = employee_status['completion_percentage'].apply(
        lambda x: '🟢 ممتاز' if x >= 80 else '🟡 جيد' if x >= 60 else '🔴 يحتاج متابعة'
    )
    
    # Rename columns for display
    employee_status.columns = ['معدل الإنجاز', 'توجد تحديات', 'موقع العمل', 'الحالة']
    employee_status = employee_status.reset_index()
    employee_status.columns = ['رقم الموظف', 'الاسم', 'القسم', 'معدل الإنجاز', 'توجد تحديات', 'موقع العمل', 'الحالة']
    
    st.dataframe(employee_status, use_container_width=True)
    
    # Weekly Progress Chart
    st.markdown("---")
    st.subheader("📈 التقدم الأسبوعي للمشاريع")
    
    fig_weekly = go.Figure()
    
    # Add completed tasks
    fig_weekly.add_trace(go.Scatter(
        x=weekly_data['week_of'],
        y=weekly_data['completed_tasks'],
        mode='lines+markers',
        name='المهام المكتملة',
        line=dict(color='#51cf66', width=3)
    ))
    
    # Add in-progress tasks
    fig_weekly.add_trace(go.Scatter(
        x=weekly_data['week_of'],
        y=weekly_data['in_progress_tasks'],
        mode='lines+markers',
        name='المهام قيد التنفيذ',
        line=dict(color='#ffd43b', width=3)
    ))
    
    # Add delayed tasks
    fig_weekly.add_trace(go.Scatter(
        x=weekly_data['week_of'],
        y=weekly_data['delayed_tasks'],
        mode='lines+markers',
        name='المهام المتأخرة',
        line=dict(color='#ff6b6b', width=3)
    ))
    
    fig_weekly.update_layout(
        title="تتبع المهام الأسبوعي",
        xaxis_title="الأسبوع",
        yaxis_title="عدد المهام",
        font=dict(family="Arial", size=12),
        hovermode='x unified'
    )
    
    st.plotly_chart(fig_weekly, use_container_width=True)
    
    # Action Center
    st.markdown("---")
    st.subheader("⚡ مركز الإجراءات")
    
    action_col1, action_col2, action_col3 = st.columns(3)
    
    with action_col1:
        if st.button("📧 إرسال تذكير جماعي", use_container_width=True):
            st.success("تم إرسال التذكير لجميع الموظفين!")
    
    with action_col2:
        if st.button("📊 تصدير التقرير", use_container_width=True):
            st.success("تم تصدير التقرير بصيغة Excel!")
    
    with action_col3:
        if st.button("🔄 تحديث البيانات", use_container_width=True):
            st.success("تم تحديث البيانات!")
    
    # Footer
    st.markdown("---")
    st.markdown(f"آخر تحديث: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main() 