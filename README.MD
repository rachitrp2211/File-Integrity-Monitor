# File Integrity Monitor (FIM)

**Real-time file monitoring system that detects unauthorized changes in critical system folders and sends alerts.**

---

## Table of Contents

1. [Project Overview](#project-overview)  
2. [Features](#features)  
3. [Technologies](#technologies)  
4. [Architecture & Design](#architecture--design)  
5. [Setup Instructions](#setup-instructions)  
6. [Configuration](#configuration)  
7. [Usage](#usage)  
8. [Impact & Applications](#impact--applications)  
9. [Future Enhancements](#future-enhancements)  
10. [License](#license)

---

## Project Overview

The **File Integrity Monitor (FIM)** is a Python-based system designed to track changes in critical files and directories. It monitors file creation, modification, and deletion events in real-time, logs the activity, and sends email alerts to administrators.  

FIM ensures **system security** by detecting unauthorized tampering and maintaining a secure baseline of monitored files. It mimics a lightweight **SOC (Security Operations Center)** functionality.

---

## Features

- Real-time monitoring of multiple folders  
- Detect file **creation**, **modification**, and **deletion**  
- Maintain a **baseline** hash of monitored files (SHA256)  
- Automatic **baseline updates** for new or modified files  
- Exclude specific files or directories (e.g., logs, `__pycache__`)  
- **Email alerts** for immediate notifications  
- **Daily digest** of all file events with HTML formatting and attachments  
- Detailed logging of all events  
- Configurable via a YAML file  

---

## Technologies

- **Python 3.10+**  
- **watchdog** – Real-time filesystem monitoring  
- **hashlib** – File hash computation (SHA256)  
- **PyYAML** – Configuration management  
- **smtplib / email.message** – Email notifications  
- **logging** – Event and error logging  
- **threading / scheduler** – Daily digest email  

---

## Architecture & Design

### 1. File Monitoring
- Uses `watchdog` to monitor folders in real-time.  
- Detects file creation, modification, and deletion.  

### 2. Baseline Management
- Baseline of all monitored files stored in `baseline.json`.  
- Baseline updated automatically whenever a file is created or modified.  
- Deleted files are removed from the baseline.  

### 3. Email Alerts
- Immediate alerts for file events.  
- Daily digest emails summarize all events of the day.  

### 4. Logging
- All events and errors logged in `fim.log`.  
- Facilitates auditing and incident tracking.  

---

## Setup Instructions

1. **Clone the repository**  
```bash
git clone https://github.com/rachitrp2211/File-Integrity-Monitor.git
cd File-Integrity-Monitor
```
2. **Create a virtual environment (recommended)**  
```bash
python -m venv .venv
source .venv/Scripts/activate  # Windows
```
3. **Install dependencies** 
```bash
pip install -r requirements.txt
```

4. **Prepare monitored folders**  

Create a test folder or choose existing folders to monitor.


