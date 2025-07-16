#!/usr/bin/env python3
"""
Demo script to showcase the Movie Recommender System features
"""

import subprocess
import sys
import os

def main():
    print("🎬 Movie Recommender System - Enhanced Version")
    print("=" * 50)
    print()
    
    print("✨ NEW FEATURES ADDED:")
    print("1. 🔐 User Authentication (Login/Signup)")
    print("2. 👤 Profile Management with dropdown menu")
    print("3. 🔒 Secure password change functionality")
    print("4. 🎨 Light/Dark theme support")
    print("5. ⚙️ User preferences management")
    print()
    
    print("📋 PROFILE FEATURES:")
    print("• Profile icon in top-left corner")
    print("• Expandable dropdown with 3 tabs:")
    print("  - 👤 Profile: Edit user information")
    print("  - 🔒 Password: Change password securely")
    print("  - ⚙️ Preferences: Toggle light/dark theme")
    print()
    
    print("🚀 TO RUN THE APPLICATION:")
    print("1. Make sure you're in the project directory")
    print("2. Run: streamlit run app.py")
    print("3. Open browser to: http://localhost:8501")
    print()
    
    # Check if we're in the right directory
    if os.path.exists('app.py') and os.path.exists('auth.py'):
        print("✅ All files found! Ready to run.")
        
        response = input("Would you like to start the application now? (y/n): ")
        if response.lower() in ['y', 'yes']:
            print("🚀 Starting Streamlit application...")
            try:
                subprocess.run(['streamlit', 'run', 'app.py'], check=True)
            except subprocess.CalledProcessError:
                print("❌ Error starting Streamlit. Make sure it's installed:")
                print("pip install streamlit")
            except KeyboardInterrupt:
                print("\n👋 Application stopped by user.")
    else:
        print("❌ Please run this script from the project directory containing app.py")

if __name__ == "__main__":
    main()
