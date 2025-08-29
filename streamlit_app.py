import streamlit as st
import os
import subprocess

st.set_page_config(page_title="Resume Wale Projects Dashboard", layout="wide")
st.title("Resume Wale Projects Dashboard")

# Auto-start all BAT files on application startup
bat_files = [
    "system_monitor.bat",
    "live_monitor.bat",
    "check_status.bat",
    "restart_system.bat",
    "start_all.bat"
]

# Run all BAT files at startup
for bat_file in bat_files:
    try:
        subprocess.Popen(bat_file, shell=True)
        st.sidebar.success(f"Started {bat_file}")
    except Exception as e:
        st.sidebar.error(f"Failed to start {bat_file}: {e}")

st.markdown("""
This dashboard provides access to various scripts and monitoring tools for the Resume Wale Projects suite. Use the buttons below to launch additional modules.
""")

# Define available scripts
scripts = {
    "Admin Panel": "admin_panel.py",
    "Dashboard": "dashboard.py",
    "Control Center": "control_center.py",
    "Realtime Tracker Dashboard": "realtime_tracker_dashboard.py",
    "User Panel": "user_panel.py",
}

col1, col2 = st.columns(2)

with col1:
    for name, script in list(scripts.items())[:len(scripts)//2+1]:
        if st.button(f"Run {name}"):
            if script.endswith('.py'):
                os.system(f'start cmd /k "e:/resume wale projects1/resume wale projects/.conda/python.exe {script}"')
            else:
                os.system(f'start cmd /k "{script}"')

with col2:
    for name, script in list(scripts.items())[len(scripts)//2+1:]:
        if st.button(f"Run {name}"):
            if script.endswith('.py'):
                os.system(f'start cmd /k "e:/resume wale projects1/resume wale projects/.conda/python.exe {script}"')
            else:
                os.system(f'start cmd /k "{script}"')

st.markdown("---")
st.subheader("Quick Links")
st.markdown("""
- [README](README.md)
- [Quick Start Guide](QUICK_START.md)
""")
