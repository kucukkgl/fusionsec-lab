#!/bin/bash

echo "=== FusionSec Lab Setup + Start (macOS/Linux) ==="

# Ensure python3 exists
if ! command -v python3 &> /dev/null
then
    echo "[ERROR] python3 not found. Install Python 3 first."
    exit 1
fi

# Ensure pip3 exists
if ! command -v pip3 &> /dev/null
then
    echo "[ERROR] pip3 not found. Install pip for Python 3."
    exit 1
fi

# Create venv if missing
if [ ! -d "venv" ]; then
    echo "[+] Creating virtual environment with python3..."
    python3 -m venv venv
else
    echo "[*] venv already exists"
fi

# Activate venv
echo "[+] Activating virtual environment..."
source venv/bin/activate

# Install requirements using pip3
echo "[+] Installing requirements with pip3..."
pip3 install -r requirements.txt

# Create runtime directories
echo "[+] Creating runtime directories..."
mkdir -p logs
mkdir -p dfir_artifacts
mkdir -p fim/created fim/modified fim/deleted fim/uploaded fim/beacon

echo "[+] Environment ready."
echo "[+] Starting FusionSec Lab..."

# Start the app with python3
python3 app.py
