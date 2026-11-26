@echo off
REM RAG Chat App - Setup and Run Script for Windows

echo.
echo RAG Chat App - Setup Script for Windows
echo ==========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed. Please install Python 3.8 or higher.
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo Python found:
python --version

REM Create virtual environment if it doesn't exist
if not exist ".venv" (
    echo.
    echo Creating virtual environment...
    python -m venv .venv
)

REM Activate virtual environment
echo.
echo Activating virtual environment...
call .venv\Scripts\activate.bat

REM Install requirements
echo.
echo Installing dependencies...
pip install -r requirements.txt

REM Check for .env file
if not exist ".env" (
    echo.
    echo .env file not found. Creating template...
    (
        echo OPENAI_API_KEY=your_openai_api_key_here
    ) > .env
    echo Please edit .env and add your OpenAI API key
)

REM Run the app
echo.
echo Setup complete!
echo Starting Streamlit app...
echo.
echo The app will open in your browser at http://localhost:8501
echo Press Ctrl+C to stop the app
echo.

streamlit run app.py

pause
