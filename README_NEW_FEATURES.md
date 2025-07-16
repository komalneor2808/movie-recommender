# 🎬 Movie Recommender System

An enhanced movie recommendation system with user authentication, profile management, and theme customization.

## ✨ New Features

### 🔐 Authentication System
- **User Registration**: Create new accounts with username, email, and password
- **Secure Login**: Password hashing using bcrypt for security
- **Session Management**: Persistent login sessions

### 👤 Profile Management
- **Profile Icon**: Located in the top-left corner for easy access
- **Profile Dropdown**: Expandable menu with multiple tabs:
  - **👤 Profile Tab**: View and edit user information (email, full name, age)
  - **🔒 Password Tab**: Change password with current password verification
  - **⚙️ Preferences Tab**: Toggle between light and dark themes

### 🎨 Theme Support
- **Light Theme**: Clean, bright interface (default)
- **Dark Theme**: Easy on the eyes for low-light environments
- **Persistent Settings**: Theme preference saved to user profile

## 🚀 Getting Started

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. **Clone or navigate to the project directory**:
   ```bash
   cd /Users/kkaur/Documents/AIProject/Code
   ```

2. **Run the setup script**:
   ```bash
   ./setup.sh
   ```

3. **Or install manually**:
   ```bash
   # Create virtual environment
   python3 -m venv venv
   source venv/bin/activate
   
   # Install dependencies
   pip install -r requirements.txt
   ```

### Running the Application

1. **Activate virtual environment** (if not already active):
   ```bash
   source venv/bin/activate
   ```

2. **Start the application**:
   ```bash
   streamlit run app.py
   ```

3. **Open your browser** to `http://localhost:8501`

## 📋 Usage

### First Time Setup
1. **Create Account**: Use the "Sign Up" tab to create a new account
2. **Login**: Switch to "Login" tab and enter your credentials
3. **Explore**: Start getting movie recommendations!

### Profile Management
1. **Click Profile Icon**: Located in the top-left corner (👤)
2. **Navigate Tabs**:
   - **Profile**: Update your personal information
   - **Password**: Change your password securely
   - **Preferences**: Switch between light/dark themes

### Getting Recommendations
1. **Select User ID**: Choose from the dataset users in the sidebar
2. **Set Filters**: Adjust minimum rating and number of recommendations
3. **Optional Filters**: Select specific genres if desired
4. **Get Recommendations**: Click the main recommendation button

## 🛠️ Technical Details

### File Structure
```
Code/
├── app.py                 # Main application
├── auth.py               # Authentication system
├── profile_manager.py    # Profile management
├── recommender.py        # Recommendation engine
├── requirements.txt      # Python dependencies
├── setup.sh             # Setup script
├── static/
│   └── custom.css       # Custom styling
└── data/                # Dataset files
    ├── users.csv
    ├── movies.csv
    └── ratings.csv
```

### Database
- **SQLite**: Local database for user accounts (`users.db`)
- **Automatic Creation**: Database initialized on first run
- **Secure Storage**: Passwords hashed with bcrypt

### Security Features
- **Password Hashing**: bcrypt with salt
- **Session Management**: Streamlit session state
- **Input Validation**: Form validation and sanitization

## 🎯 Features Overview

### Authentication
- ✅ User registration with email validation
- ✅ Secure password hashing
- ✅ Login/logout functionality
- ✅ Session persistence

### Profile Management
- ✅ Profile icon in top-left corner
- ✅ Expandable profile dropdown
- ✅ Three-tab interface (Profile/Password/Preferences)
- ✅ Edit user information
- ✅ Change password with verification
- ✅ Theme selection (light/dark)

### Movie Recommendations
- ✅ Personalized recommendations
- ✅ Filtering options
- ✅ Genre-based filtering
- ✅ Movie search functionality
- ✅ IMDb links
- ✅ User profile insights

### UI/UX Enhancements
- ✅ Modern, responsive design
- ✅ Dark/light theme support
- ✅ Intuitive navigation
- ✅ Visual feedback and notifications
- ✅ Mobile-friendly layout

## 🔧 Customization

### Adding New Themes
Edit `static/custom.css` to add new theme options:
```css
.theme-custom {
    background-color: #your-color !important;
    color: #your-text-color !important;
}
```

### Modifying Profile Fields
Update `auth.py` database schema and `profile_manager.py` forms to add new user fields.

## 🐛 Troubleshooting

### Common Issues
1. **Database Error**: Delete `users.db` and restart the app
2. **Import Error**: Ensure all dependencies are installed
3. **Theme Not Applying**: Refresh the page after changing theme
4. **Profile Not Saving**: Check database permissions

### Support
For issues or questions, check the code comments or create an issue in the project repository.

## 📝 License

This project is for educational purposes. Please respect the MovieLens dataset license terms.

---

**Enjoy your enhanced movie recommendation experience!** 🍿✨
