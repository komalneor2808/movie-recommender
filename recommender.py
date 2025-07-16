# This file contains the movie recommendation logic
# It uses collaborative filtering - basically finds users with similar taste and recommends movies they liked

import pandas as pd

# Load the movie data files
# These are the MovieLens dataset files with movie info and ratings
ratings_data = pd.read_csv("data/ratings.csv", sep="\t", header=None, encoding="latin1")
movies_data = pd.read_csv("data/movies.csv", sep="|", header=None, encoding="latin1")
users_data = pd.read_csv("data/users.csv", sep="|", header=None, encoding="latin1")

# Give proper names to the columns so we can work with them easily
ratings_data.columns = ["user_id", "movie_id", "rating", "timestamp"]
movies_data.columns = ["movie_id", "title", "release_date", "video_release_date", "imdb_url"] + [f"genre_{i}" for i in range(19)]
users_data.columns = ["user_id", "age", "gender", "occupation", "zip_code"]

# Remove columns we don't need
movies_data = movies_data.drop(['release_date', 'video_release_date'], axis=1, errors='ignore')

def recommend_movies_for_user(user_id, min_rating=4, top_n=5, min_similar_ratings=10):
    """
    This function recommends movies for a specific user
    It works by finding other users who liked similar movies, then suggests movies those users also liked
    """
    try:
        # Step 1: Find movies this user rated highly
        user_ratings = ratings_data[ratings_data['user_id'] == user_id]
        liked_movies = user_ratings[user_ratings['rating'] >= min_rating]['movie_id']

        if liked_movies.empty:
            # User hasn't rated any movies highly
            return pd.DataFrame()

        # Step 2: Find other users who also liked these movies
        similar_users = ratings_data[
            (ratings_data['movie_id'].isin(liked_movies)) &
            (ratings_data['rating'] >= min_rating) &
            (ratings_data['user_id'] != user_id)  # Don't include the user themselves
        ]

        if similar_users.empty:
            # No similar users found
            return pd.DataFrame()

        # Step 3: Calculate how similar each user is (based on number of common liked movies)
        user_similarity_scores = similar_users.groupby('user_id').size() / len(liked_movies)

        # Step 4: Find movies that similar users liked, but our user hasn't seen yet
        potential_recommendations = ratings_data[
            (ratings_data['user_id'].isin(user_similarity_scores.index)) &
            (~ratings_data['movie_id'].isin(liked_movies)) &  # Movies user hasn't seen
            (ratings_data['rating'] >= min_rating)
        ]
        
        if potential_recommendations.empty:
            return pd.DataFrame()

        # Step 5: Weight the ratings by user similarity
        potential_recommendations = potential_recommendations.merge(
            user_similarity_scores.reset_index(), on='user_id', how='left'
        )
        potential_recommendations['weighted_rating'] = potential_recommendations['rating'] * potential_recommendations[0]

        # Step 6: Group by movie and calculate average weighted rating
        movie_scores = potential_recommendations.groupby('movie_id').agg({
            'weighted_rating': 'mean',
            'rating': ['count', 'mean']
        })
        movie_scores.columns = ['predicted_rating', 'rating_count', 'avg_rating']
        
        # Only recommend movies that have enough ratings to be reliable
        movie_scores = movie_scores[movie_scores['rating_count'] >= min_similar_ratings]
        
        # Sort by predicted rating and get top N
        top_recommendations = movie_scores.sort_values(by='predicted_rating', ascending=False).head(top_n)

        if top_recommendations.empty:
            return pd.DataFrame()

        # Step 7: Add movie titles to the recommendations
        top_recommendations['title'] = top_recommendations.index.map(
            lambda x: movies_data.loc[movies_data['movie_id'] == x, 'title'].values[0]
        )
        
        # Clean up the result
        final_recommendations = top_recommendations[['title', 'predicted_rating', 'rating_count', 'avg_rating']].copy()
        final_recommendations.reset_index(inplace=True)

        return final_recommendations

    except Exception as e:
        print("Something went wrong:", e)
        return pd.DataFrame()
