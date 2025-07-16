#!/bin/bash

# Movie Recommender System Setup Script
echo "🎬 Setting up Movie Recommender System..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create users database
echo "🗄️ Initializing user database..."
python3 -c "from auth import auth; print('✅ User database initialized!')"

echo "🎉 Setup complete!"
echo ""
echo "To run the application:"
echo "1. Activate the virtual environment: source venv/bin/activate"
echo "2. Run the app: streamlit run app.py"
echo ""
echo "The application will open in your web browser at http://localhost:8501"
