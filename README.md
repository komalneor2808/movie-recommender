# Movie Recommender System
This is personalized movie recommendation system that is built using Streamlit. It includes user authentication, profile management menu, and collaborative filtering to suggest movies according to user preferences. It also has filters to make the results more specific. I have used collaborative filtering to find users with similar taste in movie, and suggests movies liked by those users. 


## Features
=: User authentication with both sign in and sign up options
=: Profile management menu for updating user info , password and preferences
=: In prefrences, user can choose between light and dark theme 
=: Personalized movie recommendations using collaborative filtering
=: Filters and search bar to make recommendations more specific
=: bar graphs to show basic dataset insights 


## Files in this project
=: `app.py` - Main application file 
=: `auth.py` - File to handle user login, signup, password 
=: `profile_manager.py` - File to manage user profiles and settings
=: `recommender.py` - File with recommendation algorithm
=: `data_exploration.ipynb` - File of my data analysis work of 3 weeks
=: `requirements.txt` - File with required Python packages
=: `data/` - Folder with Movie dataset files from MovieLens
=: `static/custom.css` - File that contains styling for the app



## Live Demo
https://movie-recommender-67grbyc7jy6vvda5k62yph.streamlit.app/



## Requirements
=: Python 3.7+
=: Streamlit
=: Pandas
=: NumPy
=: Scikit-surprise
=: BCrypt
 


## Installation of project
1. Clone the repository:
    - git clone https://github.com/komalneor2808/movie-recommender.git
    - cd movie-recommender

2. Install the dependencies: pip install -r requirements.txt
    - python -m venv venv

    - source venv/bin/activate     // On macOS/Linux
    - venv\Scripts\activate        // On Windows

    - pip install -r requirements.txt       //install from the given file
    - pip install streamlit pandas numpy scikit-surprise bcrypt     //Or, install individually

3. To run the system: streamlit run app.py

4. In the brower, go to: http://localhost:8501
  


## Project Structure
=: app.py                 # Main application
=: auth.py                # Authentication logic
=: profile_manager.py     # User profile handling
=: recommender.py         # Recommendation system logic
=: data_exploration.ipynb # Jupyter notebook with data analysis
=: requirements.txt       # Dependencies
=: users.db               # Local user database
=: data/                  # Movie dataset
        =: movies.csv
        =: ratings.csv
=: static/                # CSS styling
        =: custom.css



## Data Analysis
=: MovieLens 100k dataset is used for movies which has:
    =: 100,000 ratings from 943 users on 1682 movies
    =: Sparsity of 93.7% 
    =: Average rating of 3.53 and rating 4 is the most frequent one
    =: Users rate between 20 and 737 movies 
=: Link to the dataset: https://grouplens.org/datasets/movielens/100k/
=: `data_exploration.ipynb` file explores all the data very well in its code. 



## Usage
1. Sign up by filling the neccessary details
2. Log in to the system
3. Get movie recommendations based on your preferences using the button(middle of the screen)
4. Use filetrs on the left of the screen to make recomemndations more specific
5. Edit your profile to update your info and movie interests
5. Use the search feature to find movies by title or genre


