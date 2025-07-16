import streamlit as st
import pandas as pd
from recommender import recommend_movies_for_user
from auth import auth
from profile_manager import profile_manager
import os

st.set_page_config(
    page_title="Movie Recommender System",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'theme' not in st.session_state:
    st.session_state.theme = "light"

def load_css_and_theme():
    if os.path.exists('static/custom.css'):
        with open('static/custom.css') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    
    if st.session_state.theme == "dark":
        st.markdown("""
        <style>
        .stApp { background-color: #262730 !important; color: #ffffff !important; }
        .stSidebar { background-color: #1e1e1e !important; }
        .stSidebar .stMarkdown { color: #ffffff !important; }
        .stSidebar .stMarkdown p { color: #ffffff !important; }
        .stSidebar .stSelectbox label { color: #ffffff !important; }
        .stSidebar .stSlider label { color: #ffffff !important; }
        .stSidebar .stMultiselect label { color: #ffffff !important; }
        .stSidebar .stCheckbox label { color: #ffffff !important; }
        .stSidebar .stTextInput label { color: #ffffff !important; }
        div[data-testid="metric-container"] { background-color: #404040 !important; border: 1px solid #555 !important; padding: 1rem !important; border-radius: 0.5rem !important; color: #ffffff !important; }
        div[data-testid="metric-container"] > div { color: #ffffff !important; }
        .stMarkdown { color: #ffffff !important; }
        .stMarkdown p { color: #ffffff !important; }
        .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4 { color: #ffffff !important; }
        .stTextInput input { background-color: #404040 !important; color: #ffffff !important; border-color: #555 !important; }
        .stSelectbox select { background-color: #404040 !important; color: #ffffff !important; border-color: #555 !important; }
        .stTextArea textarea { background-color: #404040 !important; color: #ffffff !important; border-color: #555 !important; }
        .stNumberInput input { background-color: #404040 !important; color: #ffffff !important; border-color: #555 !important; }
        div[data-testid="stExpander"] { background-color: #404040 !important; border-color: #555 !important; }
        div[data-testid="stExpander"] .streamlit-expanderHeader { color: #ffffff !important; }
        .stTabs [data-baseweb="tab-list"] { background-color: #404040 !important; }
        .stTabs [data-baseweb="tab"] { color: #ffffff !important; }
        .stAlert { color: #000000 !important; }
        </style>
        """, unsafe_allow_html=True)

def show_login_signup():
    st.title("🎬 Movie Recommender System")
    st.markdown("### Welcome! Please login or create an account to continue.")
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        tab1, tab2 = st.tabs(["Login", "Sign Up"])
        
        with tab1:
            st.subheader("Login to your account")
            with st.form("login_form", clear_on_submit=False):
                username = st.text_input("Username", placeholder="Enter your username")
                password = st.text_input("Password", type="password", placeholder="Enter your password")
                submit_login = st.form_submit_button("Login", type="primary", use_container_width=True)
                
                if submit_login:
                    if not username or not password:
                        st.error("Please fill in both username and password!")
                    elif auth.authenticate_user(username, password):
                        st.session_state.logged_in = True
                        st.session_state.username = username
                        user_info = auth.get_user_info(username)
                        if user_info:
                            st.session_state.theme = user_info.get('theme_preference', 'light')
                        st.success("Logged in successfully!")
                        st.rerun()
                    else:
                        st.error("Invalid username or password!")
        
        with tab2:
            st.subheader("Create a new account")
            with st.form("signup_form", clear_on_submit=True):
                new_username = st.text_input("Username", placeholder="Choose a username", key="signup_username")
                new_email = st.text_input("Email", placeholder="Enter your email", key="signup_email")
                new_password = st.text_input("Password", type="password", placeholder="Choose a password", key="signup_password")
                confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password", key="confirm_password")
                
                st.markdown("**Optional Information:**")
                full_name = st.text_input("Full Name", placeholder="Your full name (optional)", key="signup_fullname")
                age = st.number_input("Age", min_value=13, max_value=120, value=None, key="signup_age")
                
                submit_signup = st.form_submit_button("Create Account", type="primary", use_container_width=True)
                
                if submit_signup:
                    if not new_username or not new_email or not new_password:
                        st.error("Please fill in all required fields!")
                    elif new_password != confirm_password:
                        st.error("Passwords don't match!")
                    elif len(new_password) < 6:
                        st.error("Password must be at least 6 characters long!")
                    elif "@" not in new_email:
                        st.error("Please enter a valid email address!")
                    else:
                        success, message = auth.create_user(new_username, new_email, new_password, full_name, age)
                        if success:
                            st.success(f"{message}")
                            st.info("Please switch to the Login tab to access your account!")
                        else:
                            st.error(f"{message}")

def main_app():
    load_css_and_theme()
    
    try:
        users = pd.read_csv("data/users.csv", sep="|", encoding="latin1",
                           names=["user_id", "age", "gender", "occupation", "zip_code"])
        movies = pd.read_csv("data/movies.csv", sep="|", encoding="latin1",
                            names=["movie_id", "title", "release_date", "video_release_date", "imdb_url"] + 
                                  [f"genre_{i}" for i in range(19)])
        ratings = pd.read_csv("data/ratings.csv", sep="\t", encoding="latin1",
                             names=["user_id", "movie_id", "rating", "timestamp"])
    except FileNotFoundError as e:
        st.error(f"Data file not found: {e}")
        st.info("Please make sure the data files are in the 'data' directory.")
        st.stop()

    genre_names = ["Action", "Adventure", "Animation", "Children's", "Comedy", "Crime",
                   "Documentary", "Drama", "Fantasy", "Film-Noir", "Horror", "Musical",
                   "Mystery", "Romance", "Sci-Fi", "Thriller", "War", "Western", "Unknown"]

    st.title("🎬 Movie Recommender System")
    st.markdown(f"### Welcome back, **{st.session_state.username}**!")
    
    profile_manager.render_profile_icon()
    profile_manager.render_profile_dropdown()
    
    st.markdown("---")

    st.sidebar.title("Recommendation Filters")
    
    st.sidebar.subheader("Movie Search")
    movie_search = st.sidebar.text_input("Search Movies by Title:", placeholder="Enter movie title...")
    if movie_search:
        movie_results = movies[movies['title'].str.contains(movie_search, case=False, na=False)]
        if not movie_results.empty:
            st.sidebar.success(f"Found {len(movie_results)} movies matching '{movie_search}'")
            with st.expander(f"Movies matching '{movie_search}' ({len(movie_results)} found)"):
                st.dataframe(movie_results[['movie_id', 'title']], use_container_width=True)
        else:
            st.sidebar.warning(f"No movies found matching '{movie_search}'")
    
    st.sidebar.markdown("---")
    
    user_options = ["None (All Users)"] + sorted(users['user_id'].unique().tolist())
    user_selection = st.sidebar.selectbox("Select a User ID:", user_options, 
                                         help="Choose a user ID to get personalized recommendations, or None for general recommendations")
    user_id = None if user_selection == "None (All Users)" else user_selection
    
    min_rating = st.sidebar.slider("Minimum Rating:", 1, 5, 4, 
                                  help="Only recommend movies with ratings above this threshold")
    top_n = st.sidebar.slider("Number of Recommendations:", 1, 20, 5,
                             help="How many movie recommendations to show")
    genres_list = st.sidebar.multiselect("Filter by Genres:", genre_names,
                                        help="Select specific genres to filter recommendations")

    st.sidebar.markdown("---")
    if user_id and st.sidebar.checkbox("Show Selected User Profile"):
        user_info = users[users['user_id'] == user_id]
        if not user_info.empty:
            st.sidebar.markdown("**User Profile:**")
            st.sidebar.info(f"**Age:** {user_info['age'].values[0]}")
            st.sidebar.info(f"**Gender:** {user_info['gender'].values[0]}")
            st.sidebar.info(f"**Occupation:** {user_info['occupation'].values[0]}")
            st.sidebar.info(f"**Zip Code:** {user_info['zip_code'].values[0]}")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("Get Personalized Recommendations")
        if user_id:
            st.markdown(f"Getting recommendations for **User {user_id}** with minimum rating of **{min_rating}** stars")
        else:
            st.markdown(f"Getting general recommendations with minimum rating of **{min_rating}** stars")
        
        if st.button("Get Recommendations", type="primary", use_container_width=True):
            with st.spinner("Finding the best movies for you..."):
                try:
                    if user_id:
                        recommendations = recommend_movies_for_user(user_id, min_rating=min_rating, top_n=top_n)
                    else:
                        general_recs = ratings[ratings['rating'] >= min_rating].groupby('movie_id').agg({
                            'rating': ['mean', 'count']
                        }).reset_index()
                        general_recs.columns = ['movie_id', 'avg_rating', 'rating_count']
                        general_recs = general_recs[general_recs['rating_count'] >= 10]
                        general_recs = general_recs.sort_values('avg_rating', ascending=False).head(top_n)
                        general_recs['title'] = general_recs['movie_id'].apply(
                            lambda x: movies[movies['movie_id'] == x]['title'].values[0] if len(movies[movies['movie_id'] == x]) > 0 else "Unknown"
                        )
                        general_recs.rename(columns={'avg_rating': 'predicted_rating'}, inplace=True)
                        recommendations = general_recs[['movie_id', 'title', 'predicted_rating', 'rating_count']]
                    
                    if not recommendations.empty:
                        recommendations['movie_id'] = recommendations['movie_id'].astype(int)
                        recommendations['IMDb Link'] = recommendations['movie_id'].apply(
                            lambda x: movies[movies['movie_id'] == x]['imdb_url'].values[0] if len(movies[movies['movie_id'] == x]['imdb_url'].values) > 0 else ""
                        )
                        recommendations['IMDb Link'] = recommendations['IMDb Link'].apply(
                            lambda url: f'<a href="{url}" target="_blank">IMDb</a>' if url else "N/A"
                        )

                        if user_id:
                            st.success(f"Top {len(recommendations)} movie recommendations for User {user_id}:")
                        else:
                            st.success(f"Top {len(recommendations)} highly rated movies:")
                        
                        for idx, row in recommendations.iterrows():
                            with st.container():
                                col_a, col_b, col_c = st.columns([3, 1, 1])
                                with col_a:
                                    st.markdown(f"**{row['title']}**")
                                with col_b:
                                    st.markdown(f"⭐ {row['predicted_rating']:.1f}")
                                with col_c:
                                    if row['IMDb Link'] != "N/A":
                                        st.markdown(row['IMDb Link'], unsafe_allow_html=True)
                                st.markdown("---")
                        
                    else:
                        st.warning("No recommendations found based on your filters. Try adjusting the minimum rating or selecting a different user.")
                        st.info("**Tip:** Try lowering the minimum rating or selecting a user with more rating history.")
                
                except Exception as e:
                    st.error(f"Error getting recommendations: {str(e)}")
                    st.info("Please try again or contact support if the problem persists.")

    with col2:
        st.subheader("Dataset Insights")
        
        st.markdown("#### Statistics")
        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("Total Movies", f"{len(movies):,}")
            st.metric("Total Users", f"{len(users):,}")
        with col_b:
            st.metric("Total Ratings", f"{len(ratings):,}")
            avg_rating = ratings['rating'].mean()
            st.metric("Avg Rating", f"{avg_rating:.1f}")
        
        st.markdown("#### Popular Genres")
        genre_data = pd.DataFrame({
            'Genre': genre_names,
            'Count': [movies[f'genre_{i}'].sum() for i in range(len(genre_names))]
        })
        genre_data = genre_data.sort_values('Count', ascending=False).head(10)
        st.bar_chart(genre_data.set_index('Genre'))
        
        st.markdown("#### User Demographics")
        age_dist = users['age'].value_counts().head(10)
        st.bar_chart(age_dist)

if __name__ == "__main__":
    if not st.session_state.logged_in:
        show_login_signup()
    else:
        main_app()
