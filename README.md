# 🎬 Movie Recommender System

A personalized movie recommendation system built with Streamlit, featuring user authentication, profile management, and collaborative filtering.

## ✨ Features

- **🔐 User Authentication**: Secure login and signup system
- **👤 Profile Management**: Edit user information and preferences
- **🎨 Theme Support**: Light and dark mode themes
- **🎯 Personalized Recommendations**: Get movie suggestions based on user preferences
- **🔍 Movie Search**: Search and filter movies by title and genre
- **📊 Dataset Insights**: View statistics and popular genres

## 🚀 Live Demo

[Deploy your app here - add your deployment URL]

## 📋 Requirements

- Python 3.7+
- Streamlit
- Pandas
- NumPy
- Scikit-surprise
- BCrypt

## 🛠️ Installation

1. Clone the repository:
```bash
git clone https://github.com/komalneor2808/movie-recommender.git
cd movie-recommender
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run app.py
```

4. Open your browser to `http://localhost:8501`

## 📁 Project Structure

```
├── app.py                 # Main Streamlit application
├── auth.py               # User authentication system
├── profile_manager.py    # User profile management
├── recommender.py        # Movie recommendation engine
├── requirements.txt      # Python dependencies
├── users.db             # SQLite user database
├── data/                # Movie dataset files
│   ├── movies.csv
│   ├── ratings.csv
│   └── users.csv
└── static/              # CSS styling files
    └── custom.css
```

## 🎯 Usage

1. **Sign Up**: Create a new account with username, email, and password
2. **Login**: Access your personalized dashboard
3. **Get Recommendations**: Select filters and get movie suggestions
4. **Manage Profile**: Update your information and preferences
5. **Search Movies**: Find specific movies by title or genre

## 🔧 Configuration

The app uses the MovieLens dataset for recommendations. You can customize:
- Minimum rating thresholds
- Number of recommendations
- Genre filters
- User interface themes

## 📊 Dataset

This project uses the MovieLens dataset containing:
- 100,000 ratings
- 1,682 movies
- 943 users
- 19 genres

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🙋‍♀️ Support

If you encounter any issues or have questions, please open an issue on GitHub.
