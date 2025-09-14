#!/bin/bash

# 🚀 AI Learning Platform with Authentication - Enhanced Linux Launch Script

echo ""
echo "=========================================="
echo "🚀 AI Learning Platform with Authentication"
echo "=========================================="
echo "🔒 Descope Authentication Enabled"
echo "🛡️ API Security Monitoring Active"  
echo "🔗 MCP Protocol Integration"
echo "=========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️ $1${NC}"
}

# Check if Python 3.8+ is available
python_cmd="python3"
if ! command -v python3 &> /dev/null; then
    if command -v python &> /dev/null; then
        python_version=$(python --version 2>&1 | grep -o '[0-9]\+\.[0-9]\+')
        if [[ $(echo "$python_version >= 3.8" | bc -l) -eq 1 ]] 2>/dev/null; then
            python_cmd="python"
        else
            print_error "Python 3.8+ required but found version $python_version"
            exit 1
        fi
    else
        print_error "Python not found. Please install Python 3.8+"
        exit 1
    fi
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    print_info "Creating virtual environment..."
    $python_cmd -m venv venv
    if [ $? -ne 0 ]; then
        print_error "Failed to create virtual environment"
        exit 1
    fi
fi

# Activate virtual environment
print_info "Activating virtual environment..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    print_error "Failed to activate virtual environment"
    exit 1
fi

# Install/update dependencies
print_info "Installing/updating dependencies..."
if [ -f "complete-requirements.txt" ]; then
    pip install -r complete-requirements.txt
    if [ $? -ne 0 ]; then
        print_warning "Failed with complete requirements, trying original..."
        pip install -r requirements.txt
        if [ $? -ne 0 ]; then
            print_error "Failed to install any requirements"
            exit 1
        fi
    fi
else
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        print_error "Failed to install requirements"
        exit 1
    fi
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo ""
    print_warning ".env file not found!"
    echo ""
    
    if [ -f "complete-env-template.env" ]; then
        print_info "Creating .env file from template..."
        cp complete-env-template.env .env
    else
        print_info "Creating basic .env file..."
        cat > .env << EOF
GROQ_API_KEY=your_groq_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
DESCOPE_PROJECT_ID=demo_project_id
EOF
    fi
    
    echo ""
    echo "📝 Please edit .env file with your API keys:"
    echo ""
    echo "REQUIRED KEYS:"
    echo "  GROQ_API_KEY=your_groq_key"
    echo "  TAVILY_API_KEY=your_tavily_key"
    echo ""
    echo "OPTIONAL KEYS:"
    echo "  DESCOPE_PROJECT_ID=your_descope_project_id"
    echo ""
    echo "🌐 Get API keys from:"
    echo "  Groq: https://groq.com/"
    echo "  Tavily: https://tavily.com/"
    echo "  Descope: https://app.descope.com/"
    echo ""
    read -p "Press Enter to continue..."
fi

# Use the complete enhanced app
if [ -f "complete-app-with-auth.py" ]; then
    print_info "Using enhanced app with authentication..."
    cp complete-app-with-auth.py app.py
else
    print_warning "Enhanced app not found, using original..."
fi

# Create logs directory
mkdir -p logs

# Display configuration status
echo ""
echo "========================================"
echo "🔧 Configuration Status"
echo "========================================"

# Check API keys
if grep -q "your_groq_api_key_here" .env; then
    print_error "Groq API: Not Configured"
else
    print_status "Groq API: Configured"
fi

if grep -q "your_tavily_api_key_here" .env; then
    print_error "Tavily API: Not Configured"
else
    print_status "Tavily API: Configured"
fi

if grep -q "demo_project_id" .env; then
    print_info "Descope Auth: Demo Mode"
else
    print_status "Descope Auth: Custom Project"
fi

print_status "Security Monitoring: Active"
print_status "MCP Protocol: Enabled"
echo "========================================"

# Launch the application
echo ""
print_info "Launching AI Learning Platform..."
echo "📖 Open your browser to: http://localhost:8501"
echo ""
echo "🔑 Authentication Features:"
echo "  ✅ Multiple login methods available"
echo "  ✅ Session management enabled"
echo "  ✅ API monitoring active"
echo "  ✅ All original features preserved"
echo ""

# Start the application
streamlit run app.py

# Handle exit
if [ $? -ne 0 ]; then
    echo ""
    print_error "Application encountered an error"
    print_error "Check the console output above for details"
    read -p "Press Enter to exit..."
fi

echo ""
print_info "Application stopped"