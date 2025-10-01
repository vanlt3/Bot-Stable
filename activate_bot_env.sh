#!/bin/bash
# Activation script for the fixed trading bot environment

echo "🚀 Activating trading bot environment with numpy compatibility fix..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Creating one..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install/upgrade key packages if needed
echo "📦 Ensuring compatible packages are installed..."
pip install --upgrade pip
pip install numpy==1.26.4 stable-baselines3==2.7.0

echo "✅ Environment activated successfully!"
echo "   You can now run your trading bot without numpy._core.numeric errors."
echo ""
echo "To run your bot:"
echo "   python3 'Bot-Trading_Swing (1).py'"
