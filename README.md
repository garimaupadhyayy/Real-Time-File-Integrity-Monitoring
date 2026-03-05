Real-Time File Integrity Monitoring & Alert System (FIM)
A Python-based Real-Time File Integrity Monitoring (FIM) system with GUI interface and Email Alert functionality. This project monitors selected directories for file changes (Addition, Deletion, Modification) using SHA-256 hashing and generates real-time alerts.
Designed as a cybersecurity-focused integrity monitoring solution.

Project Overview
File Integrity Monitoring (FIM) is a core security control used in:

- SOC environments
- Threat detection systems
- Malware detection
- Compliance frameworks (ISO 27001, PCI-DSS)
- Incident response workflows
This system creates a baseline of file hashes and continuously scans the directory to detect integrity violations.

Features
- SHA-256 file hashing
- Directory monitoring (every 10 seconds)
- Detects file addition
- Detects file modification
- Detects file deletion
- Email alert notifications
- GUI built with Tkinter
- Multi-threaded execution
- Logging system (`alerts.log`)
- Baseline stored in JSON format
- Secure credential handling using `.env`

Tech Stack
- Python
- Tkinter (GUI)
- Hashlib
- JSON
- Logging
- SMTP (Email Alerts)
- OS module
- Multithreading
- python-dotenv

Project Structure
Real-Time-File-Integrity-Monitoring/
│
├── file_integrity_monitor_system.py   # Core monitoring logic
├── gui_monitor.py                     # GUI Interface
├── .gitignore
├── README.md
└── baseline_*.json                    # Auto-generated baseline files

How It Works
1. User selects a directory using GUI.
2. System scans and generates SHA-256 hashes for all files.
3. Baseline file is created.
4. Every 10 seconds:
   - New hashes are generated
   - Compared with baseline
   - Changes detected
   - Alerts generated
5. Email notification sent (if configured).

Installation & Setup

1️⃣ Clone the Repository
bash
git clone https://github.com/garimaupadhyayy/Real-Time-File-Integrity-Monitoring.git
cd Real-Time-File-Integrity-Monitoring

2️⃣ Install Dependencies
bash
pip install python-dotenv

4️⃣ Run the Application
bash
python gui_monitor.py
- Select folder
- Click "Start Monitoring"
- Modify/Add/Delete files
- View alerts in GUI and Email

Security Considerations
- No hardcoded credentials
- Environment variable-based authentication
- Email app password required
- Runtime data excluded using `.gitignore`
- Hash-based change detection

Academic & Practical Relevance
This project demonstrates:
- File Integrity Monitoring principles
- Hash-based verification
- Secure configuration management
- Logging and alerting systems
- Multi-threaded application design
- GUI-based security tools

Future Enhancements
- Real-time event-based monitoring using Watchdog
- Stop Monitoring button
- Threat severity classification
- PDF report generation
- Web-based dashboard
- Multi-directory monitoring
- SIEM integration

Author
Garima Upadhyay 
B.Tech CSE (Cyber Security)  
Passionate about Security Operations & Threat Detection  
