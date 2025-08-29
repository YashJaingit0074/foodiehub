## Overview
This dashboard provides a central interface for managing and monitoring all the scripts and processes in the Projects suite. The dashboard automatically starts all BAT files on startup to ensure all systems are operational.

## Features
- Auto-starts all monitoring and system BAT files
- Provides buttons to launch Python modules as needed
- Displays status of running processes
- Links to documentation and quick start guides

## How to Run
1. Make sure all dependencies are installed:
   ```
   pip install -r requirements.txt
   ```

2. Launch the Streamlit app:
   ```
   streamlit run streamlit_app.py
   ```

## Modules
The dashboard provides access to:
- Admin Panel
- Dashboard
- Control Center
- Realtime Tracker Dashboard
- User Panel
- System Monitor (auto-started)
- Live Monitor (auto-started)
- Other system BAT files (auto-started)

## Development
The streamlit_app.py file launches all necessary background processes and provides a web interface to manage the entire system.
