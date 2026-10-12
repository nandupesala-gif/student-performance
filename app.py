import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION & STYLING
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Student Performance & Analytics Portal",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for UI Enhancement
st.markdown("""
<style>
    /* Main Background */
    .main {
        background-color: #0f172a;
        color: #f8fafc;
    }
    
    /* Card Container Styling */
    .metric-card {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 1px solid #334155;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
        text-align: center;
    }
    
    .metric-card h3 {
        color: #94a3b8;
        font-size: 0.9rem;
        margin-bottom: 5px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .metric-card h2 {
        color: #38bdf8;
        font-size: 1.8rem;
        font-weight: 700;
        margin: 0;
    }

    /* Section Headers */
    .section-title {
        font-size: 1.4rem;
        font-weight: 600;
        color: #f1f5f9;
        margin-top: 25px;
        margin-bottom: 15px;
        border-left: 4px solid #38bdf8;
        padding-left: 10px;
    }

    /* Custom Badges */
    .badge-pass {
        background-color: #059669;
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: bold;
    }
    
    .badge-fail {
        background-color: #dc2626;
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. SAMPLE DATASET GENERATOR
# -----------------------------------------------------------------------------
@st.cache_data
def load_student_data():
    return pd.DataFrame({
        "Student ID": [101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112],
        "Name": ["Rahul Kumar", "Priya Sharma", "Anil Verma", "Sita Lakshmi", 
                 "Kiran Reddy", "Kavya Rao", "Suresh Naik", "Divya Teja",
                 "Vikram Singh", "Ananya Das", "Rohan Mehta", "Pooja Hegde"],
        "Department": ["CSE", "ECE", "CSE", "EEE", "ECE", "CSE", "EEE", "CSE", "ECE", "CSE", "EEE", "ECE"],
        "Semester": ["Sem 1", "Sem 1", "Sem 2", "Sem 1", "Sem 2", "Sem 1", "Sem 2", "Sem 2", "Sem 1", "Sem 2", "Sem 1", "Sem 2"],
        "Python": [85, 92, 45, 78, 88, 35, 65, 95, 55, 90, 42, 81],
        "Java": [78, 88, 50, 82, 75, 40, 70, 90, 60, 94, 38, 85],
        "AI": [90, 95, 38, 70, 80, 42, 60, 92, 58, 96, 40, 89],
        "Data Structures": [82, 90, 48, 75, 84, 38, 68, 91, 52, 92, 45, 80],
        "Attendance (%)": [90, 95, 65, 85, 88, 60, 75, 98, 70, 96, 58, 89]
    })

# -----------------------------------------------------------------------------
# 3. SIDEBAR & DATA LOADING
# -----------------------------------------------------------------------------
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=80)
st.sidebar.title("Navigation & Filters")

uploaded_file = st.sidebar.file_uploader("📂 Upload Custom Dataset (CSV)", type=["csv"])

if uploaded_file is not None:
    raw_df = pd.read_csv(uploaded_file)
else:
    raw_df = load_student_data()

# Data Processing
df = raw_df.copy()
df["Total Marks"] = df["Python"] + df["Java"] + df["AI"] + df["Data Structures"]
df["Average Score"] = (df["Total Marks"] / 4).round(2)
df["Status"] = df["Average Score"].apply(lambda x: "Pass" if x >= 40 else "Fail")

# Grade Allocation
def get_grade(score):
    if score >= 90: return "A+"
    elif score >= 80: return "A"
    elif score >= 70: return "B"
    elif score >= 60: return "C"
    elif score >= 40: return "D"
    else: return "F"

df["Grade"] = df["Average Score"].apply(get_grade)

# Sidebar Filters
st.sidebar.markdown("---")
selected_dept = st.sidebar.multiselect(
    "Select Department:",
    options=df["Department"].unique(),
    default=df["Department"].unique()
)

selected_sem = st.sidebar.multiselect(
    "Select Semester:",
    options=df["Semester"].unique(),
    default=df["Semester"].unique()
)

filtered_df = df[(df["Department"].isin(selected_dept)) & (df["Semester"].isin(selected_sem))]

# -----------------------------------------------------------------------------
# 4. DASHBOARD HEADER & KPI CARDS
# -----------------------------------------------------------------------------
st.title("🎓 Student Performance & Analytics Portal")
st.markdown("Real-time academic performance, attendance tracking, and student insights dashboard.")
st.markdown("---")

col1, col2, col3, col4, col5 = st.columns(5)

total_students = len(filtered_df)
avg_class_score = filtered_df["Average Score"].mean() if total_students > 0 else 0
pass_count = len(filtered_df[filtered_df["Status"] == "Pass"])
pass_percentage = (pass_count / total_students * 100) if total_students > 0 else 0
avg_attendance = filtered_df["Attendance (%)"].mean() if total_students > 0 else 0
top_performer = filtered_df.loc[filtered_df["Average Score"].idxmax()]["Name"] if total_students > 0 else "N/A"

with col1:
    st.markdown(f'<div class="metric-card"><h3>Total Students</h3><h2>{total_students}</h2></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="metric-card"><h3>Class Average</h3><h2>{avg_class_score:.1f}%</h2></div>', unsafe_allow_html=True)
with col3:
    st.markdown(f'<div class="metric-card"><h3>Pass Rate</h3><h2>{pass_percentage:.1f}%</h2></div>', unsafe_allow_html=True)
with col4:
    st.markdown(f'<div class="metric-card"><h3>Avg Attendance</h3><h2>{avg_attendance:.1f}%</h2></div>', unsafe_allow_html=True)
with col5:
    st.markdown(f'<div class="metric-card"><h3>Top Scorer</h3><h2 style="font-size:1.2rem; margin-top:8px; color:#f59e0b;">{top_performer}</h2></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 5. CHARTS SECTION - ROW 1
# -----------------------------------------------------------------------------
st.markdown('<div class="section-title">📊 Overall Academic Performance</div>', unsafe_allow_html=True)

chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    # Bar Chart: Subject Averages
    subject_cols = ["Python", "Java", "AI", "Data Structures"]
    avg_subject_scores = filtered_df[subject_cols].mean().reset_index()
    avg_subject_scores.columns = ["Subject", "Average Score"]
    
    fig_subjects = px.bar(
        avg_subject_scores,
        x="Subject",
        y="Average Score",
        color="Subject",
        text_auto=".1f",
        title="Subject-wise Class Average Marks",
        template="plotly_dark",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig_subjects.update_layout(yaxis=dict(range=[0, 100]), showlegend=False)
    st.plotly_chart(fig_subjects, use_container_width=True)

with chart_col2:
    # Donut Chart: Pass vs Fail Ratio
    status_df = filtered_df["Status"].value_counts().reset_index()
    status_df.columns = ["Status", "Count"]
    
    fig_pass_fail = px.pie(
        status_df,
        names="Status",
        values="Count",
        hole=0.5,
        title="Pass vs Fail Distribution",
        template="plotly_dark",
        color="Status",
        color_discrete_map={"Pass": "#10b981", "Fail": "#ef4444"}
    )
    st.plotly_chart(fig_pass_fail, use_container_width=True)

# -----------------------------------------------------------------------------
# 6. CHARTS SECTION - ROW 2
# -----------------------------------------------------------------------------
chart_col3, chart_col4 = st.columns(2)

with chart_col3:
    # Scatter Plot: Attendance vs Marks
    fig_scatter = px.scatter(
        filtered_df,
        x="Attendance (%)",
        y="Average Score",
        color="Status",
        size="Total Marks",
        hover_name="Name",
        hover_data=["Department", "Grade"],
        title="Attendance (%) vs Average Marks",
        template="plotly_dark",
        color_discrete_map={"Pass": "#38bdf8", "Fail": "#f43f5e"}
    )
    fig_scatter.update_layout(yaxis=dict(range=[0, 100]), xaxis=dict(range=[40, 100]))
    st.plotly_chart(fig_scatter, use_container_width=True)

with chart_col4:
    # Box Plot: Subject Score Range Distribution
    melted_df = filtered_df.melt(
        id_vars=["Name", "Department"],
        value_vars=subject_cols,
        var_name="Subject",
        value_name="Score"
    )
    fig_box = px.box(
        melted_df,
        x="Subject",
        y="Score",
        color="Subject",
        title="Marks Distribution & Outliers per Subject",
        template="plotly_dark"
    )
    fig_box.update_layout(yaxis=dict(range=[0, 100]), showlegend=False)
    st.plotly_chart(fig_box, use_container_width=True)

# -----------------------------------------------------------------------------
# 7. INDIVIDUAL STUDENT DEEP DIVE
# -----------------------------------------------------------------------------
st.markdown("---")
st.markdown('<div class="section-title">🔍 Individual Student Deep-Dive Analysis</div>', unsafe_allow_html=True)

if not filtered_df.empty:
    selected_student_name = st.selectbox("Select a Student to View Detailed Report Card:", filtered_df["Name"].unique())
    student_info = filtered_df[filtered_df["Name"] == selected_student_name].iloc[0]
    
    st_col1, st_col2 = st.columns([1, 2])
    
    with st_col1:
        st.subheader(f"👤 {student_info['Name']}")
        st.write(f"**Student ID:** {student_info['Student ID']}")
        st.write(f"**Department:** {student_info['Department']}")
        st.write(f"**Semester:** {student_info['Semester']}")
        st.write(f"**Overall Grade:** `{student_info['Grade']}`")
        st.write(f"**Attendance:** {student_info['Attendance (%)']}%")
        
        status_color = "badge-pass" if student_info['Status'] == "Pass" else "badge-fail"
        st.markdown(f'**Result Status:** <span class="{status_color}">{student_info["Status"]}</span>', unsafe_allow_html=True)
    
    with st_col2:
        student_marks_df = pd.DataFrame({
            "Subject": subject_cols,
            "Marks": [student_info["Python"], student_info["Java"], student_info["AI"], student_info["Data Structures"]]
        })
        
        fig_student_bar = px.bar(
            student_marks_df,
            x="Subject",
            y="Marks",
            text="Marks",
            color="Subject",
            title=f"Subject Score Breakdown for {student_info['Name']}",
            template="plotly_dark"
        )
        # Fixed Y-Axis to 100
        fig_student_bar.update_layout(yaxis=dict(range=[0, 100]), showlegend=False)
        st.plotly_chart(fig_student_bar, use_container_width=True)

# -----------------------------------------------------------------------------
# 8. DATA TABLE & EXPORT
# -----------------------------------------------------------------------------
st.markdown("---")
st.markdown('<div class="section-title">📑 Complete Student Data Records</div>', unsafe_allow_html=True)

st.dataframe(
    filtered_df.style.highlight_max(axis=0, subset=subject_cols, color="#065f46")
                     .highlight_min(axis=0, subset=subject_cols, color="#991b1b"),
    use_container_width=True
)

# Download CSV Feature
csv_data = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Download Filtered Report as CSV",
    data=csv_data,
    file_name="student_performance_report.csv",
    mime="text/csv"
)

# Footer
st.markdown("---")
st.caption("Student Analytics Dashboard | Built with Python, Streamlit & Plotly")