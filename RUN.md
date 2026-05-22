# How to Run Alpha

This document explains how to run the Alpha incident investigation agent from both **Ubuntu/WSL** and **Windows PowerShell**.

---

## Files in this project

- `alpha.py` - CLI version of the agent
- `app.py` - Web UI for entering an incident number
- `requirements.txt` - Python dependencies
- `README.md` - Architecture and design notes

---

## Supported mock incident numbers

The current version uses mocked incident data. Use one of these values:

- `INC1001`
- `INC1002`
- `INC1003`

---

# Run from Ubuntu / WSL

## 1. Go to the project folder

If the code is on your Windows drive, use the Linux path:

```bash
cd "/mnt/c/Users/sindhuRambala/OneDrive - IBM/AI stuff/something"
```

> Do **not** use a Windows path like `C:\Users\...` inside Ubuntu.

---

## 2. Check Python

```bash
python3 --version
```

If Python is missing, install it:

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip
```

---

## 3. Create a virtual environment

Run this once:

```bash
python3 -m venv .venv
```

If this fails, install venv first:

```bash
sudo apt update
sudo apt install -y python3-venv
```

---

## 4. Activate the virtual environment

```bash
source .venv/bin/activate
```

You should now see something like:

```bash
(.venv) sindhurambala@IBM-BPMMC64:...
```

---

## 5. Install dependencies

```bash
pip install -r requirements.txt
```

If you see `externally-managed-environment`, that means you forgot to activate the virtual environment.

Activate it again:

```bash
source .venv/bin/activate
```

Then rerun:

```bash
pip install -r requirements.txt
```

---

## 6. Run the web UI

```bash
python app.py
```

Open this in your browser:

```text
http://127.0.0.1:5000
```

Enter one of:

- `INC1001`
- `INC1002`
- `INC1003`

---

## 7. Run the CLI version

```bash
python alpha.py INC1002
```

You can replace `INC1002` with any supported mock incident number.

---

## 8. Next time you open Ubuntu

You do **not** need to recreate the virtual environment every time.

Just do:

```bash
cd "/mnt/c/Users/sindhuRambala/OneDrive - IBM/AI stuff/something"
source .venv/bin/activate
python app.py
```

For CLI:

```bash
cd "/mnt/c/Users/sindhuRambala/OneDrive - IBM/AI stuff/something"
source .venv/bin/activate
python alpha.py INC1002
```

---

# Run from Windows PowerShell

## 1. Go to the project folder

```powershell
cd "C:\Users\sindhuRambala\OneDrive - IBM\AI stuff\something"
```

---

## 2. Check Python

```powershell
python --version
```

If `python` does not work, try:

```powershell
py --version
```

---

## 3. Create a virtual environment

```powershell
python -m venv .venv
```

If needed, use:

```powershell
py -m venv .venv
```

---

## 4. Activate the virtual environment

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

---

## 5. Install dependencies

```powershell
pip install -r requirements.txt
```

If needed:

```powershell
python -m pip install -r requirements.txt
```

---

## 6. Run the web UI

```powershell
python app.py
```

Then open:

```text
http://127.0.0.1:5000
```

---

## 7. Run the CLI version

```powershell
python alpha.py INC1002
```

---

## 8. Next time on Windows

```powershell
cd "C:\Users\sindhuRambala\OneDrive - IBM\AI stuff\something"
.\.venv\Scripts\Activate.ps1
python app.py
```

---

# Common Issues

## `python: command not found` in Ubuntu

Use:

```bash
python3
```

Instead of:

```bash
python
```

---

## `No module named pip`

Install pip:

```bash
sudo apt update
sudo apt install -y python3-pip
```

---

## `externally-managed-environment`

Do not install globally. Use a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## `sudo apt update` fails

Possible reasons:

- wrong Ubuntu password
- user not in sudoers
- keyboard layout issue
- using Windows password instead of Ubuntu password

Check:

```bash
whoami
groups
sudo -l
```

---

## Flask import error in editor

Install dependencies:

```bash
pip install -r requirements.txt
```

or on Windows:

```powershell
python -m pip install -r requirements.txt
```

---

# What the app currently does

This is a prototype with mocked data.

It can:
- accept an incident number
- classify incident type
- route to a playbook
- generate:
  - engineer report
  - manager summary
  - Slack/email notification
  - probable P1 escalation message

It does **not** yet connect to:
- real ServiceNow
- real OpenShift
- real CI/CD pipeline tools
- real IBM Cloud APIs

---

# Quick Start

## Ubuntu / WSL

```bash
cd "/mnt/c/Users/sindhuRambala/OneDrive - IBM/AI stuff/something"
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

## Windows PowerShell

```powershell
cd "C:\Users\sindhuRambala\OneDrive - IBM\AI stuff\something"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py