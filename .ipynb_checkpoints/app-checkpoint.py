import streamlit as st
import pandas as pd
from recommender import recommend_movies_for_user

# Load the datasets with correct separators and encoding
users = pd.read_csv("data/users.csv", sep="|", encoding="latin1",
                   names=["user_id", "age", "gender", "occupation", "zip_code"])
movies = pd.read_csv("data/movies.csv", sep="|", encoding="latin1",
                    names=["movie_id", "title", "release_date", "video_release_date", "imdb_url"] + 
                          [f"genre_{i}" for i in range(19)])
ratings = pd.read_csv("data/ratings.csv", sep="\t", encoding="latin1",
                     names=["user_id", "movie_id", "rating", "timestamp"])

# Create genres list from movie genre columns
genre_names = ["Action", "Adventure", "Animation", "Children's", "Comedy", "Crime",
               "Documentary", "Drama", "Fantasy", "Film-Noir", "Horror", "Musical",
               "Mystery", "Romance", "Sci-Fi", "Thriller", "War", "Western", "Unknown"]
genres_df = pd.DataFrame({'genre': genre_names})

# Sidebar Filters
st.sidebar.title("Filters")
user_id = st.sidebar.selectbox("Select a User ID:", sorted(users['user_id'].unique()))
min_rating = st.sidebar.slider("Minimum Rating:", 1, 5, 4)
top_n = st.sidebar.slider("Top N Recommendations:", 1, 10, 5)
genres_list = st.sidebar.multiselect("Select Genres:", genre_names)

# User Profile Management
if st.sidebar.checkbox("Show User Profile"):
    user_info = users[users['user_id'] == user_id]
    st.write("User Profile:", user_info)

# Movie Search
movie_search = st.sidebar.text_input("Search Movies by Title:")
if movie_search:
    movie_results = movies[movies['title'].str.contains(movie_search, case=False)]
    st.write(f"Movies matching '{movie_search}':")
    st.dataframe(movie_results[['movie_id', 'title']])


# Recommendations Button
if st.button("Get Recommendations"):
    recommendations = recommend_movies_for_user(user_id, min_rating=min_rating, top_n=top_n)
    
    if not recommendations.empty:
        # Add IMDb links to the table
        recommendations['movie_id'] = recommendations['movie_id'].astype(int)
        recommendations['IMDb Link'] = recommendations['movie_id'].apply(
            lambda x: movies[movies['movie_id'] == x]['imdb_url'].values[0]
        )
        # Make links clickable
        recommendations['IMDb Link'] = recommendations['IMDb Link'].apply(
            lambda url: f'<a href="{url}" target="_blank">IMDb</a>'
        )

        # Optional: Drop movie_id for cleaner table
        display_df = recommendations.drop(columns=['movie_id'])

        st.success(f"Top {top_n} movie recommendations for user {user_id}:")
        st.markdown(display_df.to_html(escape=False, index=False), unsafe_allow_html=True)
        
    else:
        st.warning("No recommendations found based on your filters.")

# Additional visualizations
st.subheader("Popular Genres")
genre_data = pd.DataFrame({
    'Genre': genre_names,
    'Count': [movies[f'genre_{i}'].sum() for i in range(len(genre_names))]
})
st.bar_chart(genre_data.set_index('Genre'))
