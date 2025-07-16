# Movie Recommendation System

This is my school project for building a movie recommendation system. I used Python and Streamlit to make a web app that suggests movies to users based on what other similar users liked.

## What it does

- Users can sign up and login
- Get personalized movie recommendations 
- Search for movies by title
- Change profile settings and password
- Switch between light and dark themes
- View movie statistics and popular genres

## How the recommendation works

I used collaborative filtering - basically the app finds users who liked similar movies as you, then suggests other movies those users also enjoyed. It's like asking friends with similar taste for movie recommendations!

## Files in this project

- `app.py` - Main application file with all the UI
- `auth.py` - Handles user login, signup, password stuff
- `profile_manager.py` - Manages user profiles and settings
- `recommender.py` - The recommendation algorithm 
- `data_exploration.ipynb` - My data analysis work (3 weeks of progress)
- `requirements.txt` - Python packages needed
- `data/` - Movie dataset files from MovieLens
- `static/custom.css` - Some basic styling to make it look nicer

## How to run it

1. Install Python packages:
```bash
pip install -r requirements.txt
```

2. Run the app:
```bash
streamlit run app.py
```

3. Open your browser to `http://localhost:8501`

## Dataset info

I used the MovieLens 100K dataset which has:
- 100,000 movie ratings
- 1,682 movies  
- 943 users
- 19 different genres

The data is pretty sparse (93.7% empty) which made the recommendation algorithm challenging but interesting to work with.

## What I learned

- How to build web apps with Streamlit
- User authentication and database management
- Collaborative filtering for recommendations
- Data analysis and visualization
- CSS styling for better UI
- Git version control

## Future improvements

- Add more recommendation algorithms
- Include movie posters and descriptions
- Better mobile responsive design
- Movie rating and review features
- Social features like friend recommendations

This was a fun project that taught me a lot about data science and web development!
