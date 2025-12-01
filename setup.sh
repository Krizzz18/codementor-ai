#!/bin/bash
# Setup script for CodeMentor AI
# Mac/Linux bash script

echo "=========================================="
echo " CodeMentor AI - Setup Script"
echo "=========================================="
echo

# Check Python installation
echo "[1/5] Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.9+ from python.org"
    exit 1
fi
echo "Python found!"
echo

# Create virtual environment
echo "[2/5] Creating virtual environment..."
if [ -d "venv" ]; then
    echo "Virtual environment already exists, skipping..."
else
    python3 -m venv venv
    echo "Virtual environment created!"
fi
echo

# Activate virtual environment
echo "[3/5] Activating virtual environment..."
source venv/bin/activate
echo

# Install dependencies
echo "[4/5] Installing dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi
echo "Dependencies installed successfully!"
echo

# Check for .env file
echo "[5/5] Checking API key configuration..."
if [ -f ".env" ]; then
    echo ".env file found!"
else
    echo "WARNING: .env file not found!"
    echo "Creating .env from template..."
    cp .env.example .env
    echo
    echo "IMPORTANT: Please edit .env file and add your Google Gemini API key"
    echo "Get your API key from: https://aistudio.google.com/app/apikey"
    echo
    echo "Opening .env file..."
    ${EDITOR:-nano} .env
fi
echo

echo "=========================================="
echo " Setup Complete!"
echo "=========================================="
echo
echo "Next steps:"
echo "1. Make sure your Google Gemini API key is in .env file"
echo "2. Run the demo: python demo/demo_script.py"
echo "3. Launch the app: streamlit run app.py"
echo
echo "To activate virtual environment later, run:"
echo "   source venv/bin/activate"
echo
