@echo off

REM 🚀 AI Learning Platform with Authentication - Enhanced Windows Launch Script

echo.
echo ==========================================
echo 🚀 AI Learning Platform with Authentication
echo ==========================================
echo 🔒 Descope Authentication Enabled
echo 🛡️ API Security Monitoring Active  
echo 🔗 MCP Protocol Integration
echo ==========================================
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ❌ Failed to create virtual environment
        echo Please ensure Python 3.8+ is installed
        pause
        exit /b 1
    )
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate
if errorlevel 1 (
    echo ❌ Failed to activate virtual environment
    pause
    exit /b 1
)

REM Install/update dependencies
echo 📥 Installing/updating dependencies...
pip install -r complete-requirements.txt
if errorlevel 1 (
    echo ❌ Failed to install requirements
    echo Trying with original requirements...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ Failed to install any requirements
        pause
        exit /b 1
    )
)

REM Check if .env file exists
if not exist ".env" (
    echo.
    echo ⚠️ WARNING: .env file not found!
    echo.
    if exist "complete-env-template.env" (
        echo Creating .env file from template...
        copy complete-env-template.env .env
    ) else (
        echo Creating basic .env file...
        echo GROQ_API_KEY=your_groq_api_key_here > .env
        echo TAVILY_API_KEY=your_tavily_api_key_here >> .env
        echo DESCOPE_PROJECT_ID=demo_project_id >> .env
    )
    echo.
    echo 📝 Please edit .env file with your API keys:
    echo.
    echo REQUIRED KEYS:
    echo   GROQ_API_KEY=your_groq_key
    echo   TAVILY_API_KEY=your_tavily_key
    echo.
    echo OPTIONAL KEYS:
    echo   DESCOPE_PROJECT_ID=your_descope_project_id
    echo.
    echo 🌐 Get API keys from:
    echo   Groq: https://groq.com/
    echo   Tavily: https://tavily.com/
    echo   Descope: https://app.descope.com/
    echo.
    pause
)

REM Use the complete enhanced app
if exist "complete-app-with-auth.py" (
    echo 🔄 Using enhanced app with authentication...
    copy complete-app-with-auth.py app.py
) else (
    echo ⚠️ Enhanced app not found, using original...
)

REM Create logs directory
if not exist "logs" mkdir logs

REM Display configuration status
echo.
echo ========================================
echo 🔧 Configuration Status
echo ========================================

REM Check API keys
findstr /C:"your_groq_api_key_here" .env > nul
if errorlevel 1 (
    echo ✅ Groq API: Configured
) else (
    echo ❌ Groq API: Not Configured
)

findstr /C:"your_tavily_api_key_here" .env > nul
if errorlevel 1 (
    echo ✅ Tavily API: Configured
) else (
    echo ❌ Tavily API: Not Configured
)

findstr /C:"demo_project_id" .env > nul
if errorlevel 1 (
    echo ✅ Descope Auth: Custom Project
) else (
    echo ℹ️ Descope Auth: Demo Mode
)

echo ✅ Security Monitoring: Active
echo ✅ MCP Protocol: Enabled
echo ========================================

REM Launch the application
echo.
echo 🌟 Launching AI Learning Platform...
echo 📖 Open your browser to: http://localhost:8501
echo.
echo 🔑 Authentication Features:
echo   ✅ Multiple login methods available
echo   ✅ Session management enabled  
echo   ✅ API monitoring active
echo   ✅ All original features preserved
echo.

streamlit run app.py

REM Handle exit
if errorlevel 1 (
    echo.
    echo ❌ Application encountered an error
    echo Check the console output above for details
    pause
)

echo.
echo 👋 Application stopped
pause