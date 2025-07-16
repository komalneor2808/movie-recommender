# Main application file for Movie Recommendation System
# This is where everything comes together - login, recommendations, UI, etc.

import streamlit as st
import pandas as pd
from recommender import recommend_movies_for_user
from auth import auth
from profile_manager import profile_manager
import os

# Set up the page configuration
st.set_page_config(
    page_title="Movie Recommendation System",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state variables (these keep track of user login status, etc.)
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'theme' not in st.session_state:
    st.session_state.theme = "light"
if 'show_profile_dropdown' not in st.session_state:
    st.session_state.show_profile_dropdown = False
if 'profile_tab' not in st.session_state:
    st.session_state.profile_tab = "profile"

def load_styling():
    # Load custom CSS for better appearance
    if os.path.exists('static/custom.css'):
        with open('static/custom.css') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    
    # Apply dark theme if user selected it
    if st.session_state.theme == "dark":
        st.markdown("""
        <style>
        .stApp { background-color: #262730 !important; color: #ffffff !important; }
        .stSidebar { background-color: #1e1e1e !important; }
        .stMarkdown { color: #ffffff !important; }
        .stTextInput input { background-color: #404040 !important; color: #ffffff !important; }
        .stSelectbox select { background-color: #404040 !important; color: #ffffff !important; }
        </style>
        """, unsafe_allow_html=True)

def show_login_page():
    # This function shows the login and signup page
    st.title("🎬 Movie Recommendation System")
    st.markdown("Please sign in or create a new account to continue.")
    st.markdown("---")
    
    # Center the login form
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Create tabs for login and signup
        login_tab, signup_tab = st.tabs(["Sign In", "Create Account"])
        
        # Login tab
        with login_tab:
            st.subheader("Sign in to your account")
            with st.form("login_form"):
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                login_button = st.form_submit_button("Sign In", type="primary", use_container_width=True)
                
                if login_button:
                    if not username or not password:
                        st.error("Please enter both username and password!")
                    elif auth.authenticate_user(username, password):
                        # Login successful
                        st.session_state.logged_in = True
                        st.session_state.username = username
                        # Get user's theme preference
                        user_info = auth.get_user_info(username)
                        if user_info:
                            st.session_state.theme = user_info.get('theme_preference', 'light')
                        st.success("Welcome back!")
                        st.rerun()
                    else:
                        st.error("Wrong username or password!")
        
        # Signup tab
        with signup_tab:
            st.subheader("Create a new account")
            with st.form("signup_form"):
                new_username = st.text_input("Choose Username", key="new_user")
                new_email = st.text_input("Email Address", key="new_email")
                new_password = st.text_input("Password", type="password", key="new_pass")
                confirm_password = st.text_input("Confirm Password", type="password", key="confirm_pass")
                
                st.markdown("**Optional Info:**")
                full_name = st.text_input("Full Name (optional)", key="full_name")
                age = st.number_input("Age (optional)", min_value=13, max_value=120, value=None, key="age")
                
                signup_button = st.form_submit_button("Create Account", type="primary", use_container_width=True)
                
                if signup_button:
                    # Validate the signup form
                    if not new_username or not new_email or not new_password:
                        st.error("Please fill in all required fields!")
                    elif new_password != confirm_password:
                        st.error("Passwords don't match!")
                    elif len(new_password) < 6:
                        st.error("Password should be at least 6 characters!")
                    elif "@" not in new_email:
                        st.error("Please enter a valid email!")
                    else:
                        # Try to create the account
                        success, message = auth.create_user(new_username, new_email, new_password, full_name, age)
                        if success:
                            st.success(message)
                            st.info("Now you can sign in with your new account!")
                        else:
                            st.error(message)

def main_application():
    # This is the main app that shows after user logs in
    load_styling()
    
    # Load the movie datasets
    try:
        users = pd.read_csv("data/users.csv", sep="|", encoding="latin1",
                           names=["user_id", "age", "gender", "occupation", "zip_code"])
        movies = pd.read_csv("data/movies.csv", sep="|", encoding="latin1",
                            names=["movie_id", "title", "release_date", "video_release_date", "imdb_url"] + 
                                  [f"genre_{i}" for i in range(19)])
        ratings = pd.read_csv("data/ratings.csv", sep="\t", encoding="latin1",
                             names=["user_id", "movie_id", "rating", "timestamp"])
    except FileNotFoundError as e:
        st.error(f"Can't find data files: {e}")
        st.info("Make sure the data files are in the 'data' folder.")
        st.stop()

    # List of movie genres
    genre_names = ["Action", "Adventure", "Animation", "Children's", "Comedy", "Crime",
                   "Documentary", "Drama", "Fantasy", "Film-Noir", "Horror", "Musical",
                   "Mystery", "Romance", "Sci-Fi", "Thriller", "War", "Western", "Unknown"]

    # Main page header
    st.title("🎬 Movie Recommendation System")
    st.markdown(f"### Hi there, **{st.session_state.username}**!")
    
    # Show profile button and dropdown
    profile_manager.show_profile_button()
    profile_manager.show_profile_menu()
    
    st.markdown("---")

    # Sidebar with filters and options
    st.sidebar.title("Options")
    
    # Movie search feature
    st.sidebar.subheader("Search Movies")
    movie_search = st.sidebar.text_input("Type movie name:")
    if movie_search:
        # Search for movies containing the search term
        search_results = movies[movies['title'].str.contains(movie_search, case=False, na=False)]
        if not search_results.empty:
            st.sidebar.success(f"Found {len(search_results)} movies!")
            with st.expander(f"Movies with '{movie_search}' ({len(search_results)} found)"):
                st.dataframe(search_results[['movie_id', 'title']], use_container_width=True)
        else:
            st.sidebar.warning(f"No movies found with '{movie_search}'")
    
    st.sidebar.markdown("---")
    
    # User selection for recommendations
    user_options = ["None (Popular Movies)"] + sorted(users['user_id'].unique().tolist())
    selected_user = st.sidebar.selectbox("Pick a User ID:", user_options)
    user_id = None if selected_user == "None (Popular Movies)" else selected_user
    
    # Rating and recommendation filters
    min_rating = st.sidebar.slider("Minimum Rating:", 1, 5, 4)
    num_recommendations = st.sidebar.slider("How many recommendations:", 1, 20, 5)
    selected_genres = st.sidebar.multiselect("Pick genres:", genre_names)

    # Show user profile if selected
    st.sidebar.markdown("---")
    if user_id and st.sidebar.checkbox("Show User Info"):
        user_data = users[users['user_id'] == user_id]
        if not user_data.empty:
            st.sidebar.markdown("**User Details:**")
            st.sidebar.info(f"Age: {user_data['age'].values[0]}")
            st.sidebar.info(f"Gender: {user_data['gender'].values[0]}")
            st.sidebar.info(f"Job: {user_data['occupation'].values[0]}")

    # Main content area
    left_col, right_col = st.columns([2, 1])

    with left_col:
        st.subheader("Get Movie Recommendations")
        if user_id:
            st.markdown(f"Finding movies for **User {user_id}** (minimum {min_rating} stars)")
        else:
            st.markdown(f"Finding popular movies (minimum {min_rating} stars)")
        
        # Recommendation button
        if st.button("Find Movies for Me!", type="primary", use_container_width=True):
            with st.spinner("Looking for great movies..."):
                try:
                    if user_id:
                        # Get personalized recommendations
                        recommendations = recommend_movies_for_user(user_id, min_rating=min_rating, top_n=num_recommendations)
                    else:
                        # Get popular movies instead
                        popular_movies = ratings[ratings['rating'] >= min_rating].groupby('movie_id').agg({
                            'rating': ['mean', 'count']
                        }).reset_index()
                        popular_movies.columns = ['movie_id', 'avg_rating', 'rating_count']
                        popular_movies = popular_movies[popular_movies['rating_count'] >= 10]
                        popular_movies = popular_movies.sort_values('avg_rating', ascending=False).head(num_recommendations)
                        popular_movies['title'] = popular_movies['movie_id'].apply(
                            lambda x: movies[movies['movie_id'] == x]['title'].values[0] if len(movies[movies['movie_id'] == x]) > 0 else "Unknown"
                        )
                        popular_movies.rename(columns={'avg_rating': 'predicted_rating'}, inplace=True)
                        recommendations = popular_movies[['movie_id', 'title', 'predicted_rating', 'rating_count']]
                    
                    # Show the recommendations
                    if not recommendations.empty:
                        recommendations['movie_id'] = recommendations['movie_id'].astype(int)
                        
                        # Add IMDb links
                        recommendations['IMDb Link'] = recommendations['movie_id'].apply(
                            lambda x: movies[movies['movie_id'] == x]['imdb_url'].values[0] if len(movies[movies['movie_id'] == x]['imdb_url'].values) > 0 else ""
                        )
                        recommendations['IMDb Link'] = recommendations['IMDb Link'].apply(
                            lambda url: f'<a href="{url}" target="_blank">View on IMDb</a>' if url else "No link"
                        )

                        if user_id:
                            st.success(f"Here are {len(recommendations)} movies you might like:")
                        else:
                            st.success(f"Here are {len(recommendations)} popular movies:")
                        
                        # Display each recommendation
                        for idx, row in recommendations.iterrows():
                            with st.container():
                                movie_col, rating_col, link_col = st.columns([3, 1, 1])
                                with movie_col:
                                    st.markdown(f"**{row['title']}**")
                                with rating_col:
                                    st.markdown(f"⭐ {row['predicted_rating']:.1f}")
                                with link_col:
                                    if row['IMDb Link'] != "No link":
                                        st.markdown(row['IMDb Link'], unsafe_allow_html=True)
                                st.markdown("---")
                        
                    else:
                        st.warning("Sorry, couldn't find any recommendations with these filters.")
                        st.info("Try changing the minimum rating or user selection.")
                
                except Exception as e:
                    st.error(f"Something went wrong: {str(e)}")
                    st.info("Please try again or change your filters.")

    with right_col:
        st.subheader("Dataset Info")
        
        # Show basic statistics
        st.markdown("#### Quick Stats")
        stats_col1, stats_col2 = st.columns(2)
        with stats_col1:
            st.metric("Movies", f"{len(movies):,}")
            st.metric("Users", f"{len(users):,}")
        with stats_col2:
            st.metric("Ratings", f"{len(ratings):,}")
            avg_rating = ratings['rating'].mean()
            st.metric("Avg Rating", f"{avg_rating:.1f}")
        
        # Show popular genres
        st.markdown("#### Popular Genres")
        genre_data = pd.DataFrame({
            'Genre': genre_names,
            'Count': [movies[f'genre_{i}'].sum() for i in range(len(genre_names))]
        })
        genre_data = genre_data.sort_values('Count', ascending=False).head(10)
        st.bar_chart(genre_data.set_index('Genre'))
        
        # Show user age distribution
        st.markdown("#### User Ages")
        age_distribution = users['age'].value_counts().head(10)
        st.bar_chart(age_distribution)

# Main app logic - decide whether to show login or main app
if __name__ == "__main__":
    if not st.session_state.logged_in:
        show_login_page()
    else:
        main_application()
