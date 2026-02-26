#!/bin/bash

# ----------------------------------------
# Function to check if a command exists
# ----------------------------------------
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# ----------------------------------------
# Check Python version
# ----------------------------------------
PYTHON_VERSION=$(python3 -c 'import sys; print(sys.version_info[0])' 2>/dev/null || echo 0)

if [ "$PYTHON_VERSION" -ge 3 ]; then
    echo "Python 3 detected."
else
    echo "Python 3 is required. Please install Python 3."
    exit 1
fi

# ----------------------------------------
# Detect OS
# ----------------------------------------
OS_TYPE="$(uname -s)"
echo "Detected OS: $OS_TYPE"

# ----------------------------------------
# Install mpg123 if needed (Linux/macOS)
# ----------------------------------------
if [[ "$OS_TYPE" == "Linux"* ]]; then
    echo "Linux detected"
    if ! command_exists mpg123; then
        echo "Installing mpg123..."
        if command_exists apt; then
            sudo apt update && sudo apt install -y mpg123
        elif command_exists yum; then
            sudo yum install -y mpg123
        else
            echo "Unknown package manager. Please install mpg123 manually."
        fi
    else
        echo "mpg123 already installed"
    fi

elif [[ "$OS_TYPE" == "Darwin"* ]]; then
    echo "macOS detected"
    if ! command_exists brew; then
        echo "Homebrew not found. Installing Homebrew..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    fi
    if ! command_exists mpg123; then
        echo "Installing mpg123 via Homebrew..."
        brew install mpg123
    else
        echo "mpg123 already installed"
    fi

elif [[ "$OS_TYPE" == MINGW* || "$OS_TYPE" == MSYS* || "$OS_TYPE" == CYGWIN* || "$OS_TYPE" == "Windows_NT" ]]; then
    echo "Windows detected"
    echo "No need for mpg123 on Windows. pyttsx3 will be used for TTS."
else
    echo "Unknown OS: $OS_TYPE"
fi

# ----------------------------------------
# Create virtual environment
# ----------------------------------------
VENV_DIR="venv"
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment in $VENV_DIR..."
    python3 -m venv $VENV_DIR
else
    echo "Virtual environment already exists at $VENV_DIR"
fi

# ----------------------------------------
# Activate virtual environment
# ----------------------------------------
echo "Activating virtual environment..."
source "$VENV_DIR/bin/activate" 2>/dev/null || source "$VENV_DIR/Scripts/activate"

# ----------------------------------------
# Upgrade pip
# ----------------------------------------
echo "Upgrading pip..."
python -m pip install --upgrade pip

# ----------------------------------------
# Install requirements
# ----------------------------------------
if [ -f "requirements.txt" ]; then
    echo "Installing packages from requirements.txt..."
    python -m pip install -r requirements.txt
else
    echo "requirements.txt not found! Please create one with your dependencies."
fi

echo "Setup complete! Virtual environment is active."
echo "Use 'deactivate' to exit the environment."