#!/bin/bash

# RAG Chat App - Setup and Run Script

echo "RAG Chat App - Setup Script"
echo "================================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "Python found: $(python3 --version)"

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Install requirements
echo "Installing dependencies..."
pip install -r requirements.txt

# Apply pydantic_v1 compatibility shim for langchain-core >= 0.3.0
echo "Applying langchain_core.pydantic_v1 compatibility shim..."
LANGCHAIN_CORE_DIR=$(python3 -c "import langchain_core, os; print(os.path.dirname(langchain_core.__file__))")
SHIM_DIR="$LANGCHAIN_CORE_DIR/pydantic_v1"
if [ ! -f "$SHIM_DIR/__init__.py" ]; then
    mkdir -p "$SHIM_DIR"
    cat > "$SHIM_DIR/__init__.py" << 'SHIM'
# Compatibility shim: langchain_core.pydantic_v1 was removed in langchain-core >= 0.3.0
import warnings
warnings.filterwarnings("ignore", message="Core Pydantic V1 functionality", category=UserWarning)
try:
    from pydantic.v1 import *  # noqa: F401, F403
    from pydantic.v1 import (BaseModel, Field, validator, root_validator,
                              ValidationError, Extra, PrivateAttr, SecretStr,
                              AnyUrl, AnyHttpUrl, HttpUrl)
except ImportError:
    from pydantic import *  # noqa: F401, F403
    from pydantic import (BaseModel, Field, ValidationError, PrivateAttr,
                          SecretStr, AnyUrl, AnyHttpUrl, HttpUrl)
SHIM
    echo "Shim created at $SHIM_DIR/__init__.py"
fi

# Check for .env file
if [ ! -f ".env" ]; then
    echo ".env file not found. Creating template..."
    echo "OPENAI_API_KEY=your_openai_api_key_here" > .env
    echo "Please edit .env and add your OpenAI API key"
fi

# Run the app
echo ""
echo "Setup complete!"
echo "Starting Streamlit app..."
echo ""
echo "The app will open in your browser at http://localhost:8501"
echo "Press Ctrl+C to stop the app"
echo ""

streamlit run app.py
