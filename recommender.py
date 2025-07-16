import pandas as pd

# Load data (use relative paths if needed)
ratings = pd.read_csv("data/ratings.csv", sep="\t", header=None, encoding="latin1")
movies = pd.read_csv("data/movies.csv", sep="|", header=None, encoding="latin1")
users = pd.read_csv("data/users.csv", sep="|", header=None, encoding="latin1")

# Assign column names
ratings.columns = ["user_id", "movie_id", "rating", "timestamp"]
movies.columns = ["movie_id", "title", "release_date", "video_release_date", "imdb_url"] + [f"genre_{i}" for i in range(19)]
users.columns = ["user_id", "age", "gender", "occupation", "zip_code"]

# Drop unnecessary columns
movies = movies.drop(['release_date', 'video_release_date'], axis=1, errors='ignore')

def recommend_movies_for_user(user_id, min_rating=4, top_n=5, min_similar_ratings=10):
    try:
        user_ratings = ratings[ratings['user_id'] == user_id]
        high_rated = user_ratings[user_ratings['rating'] >= min_rating]['movie_id']

        if high_rated.empty:
            return pd.DataFrame()

        similar_users = ratings[
            (ratings['movie_id'].isin(high_rated)) &
            (ratings['rating'] >= min_rating) &
            (ratings['user_id'] != user_id)
        ]

        if similar_users.empty:
            return pd.DataFrame()

        user_similarity = similar_users.groupby('user_id').size() / len(high_rated)

        recommendations = ratings[
            (ratings['user_id'].isin(user_similarity.index)) &
            (~ratings['movie_id'].isin(high_rated)) &
            (ratings['rating'] >= min_rating)
        ]
        if recommendations.empty:
            return pd.DataFrame()

        recommendations = recommendations.merge(user_similarity.reset_index(), on='user_id', how='left')
        recommendations['weighted_rating'] = recommendations['rating'] * recommendations[0]

        top = recommendations.groupby('movie_id').agg({
            'weighted_rating': 'mean',
            'rating': ['count', 'mean']
        })
        top.columns = ['weighted_avg', 'rating_count', 'avg_rating']
        top = top[top['rating_count'] >= min_similar_ratings]
        top = top.sort_values(by='weighted_avg', ascending=False).head(top_n)

        if top.empty:
            return pd.DataFrame()

        top['title'] = top.index.map(lambda x: movies.loc[movies['movie_id'] == x, 'title'].values[0])
        final_df = top[['title', 'weighted_avg', 'rating_count', 'avg_rating']].copy()
        final_df.reset_index(inplace=True)
        final_df.rename(columns={'weighted_avg': 'predicted_rating'}, inplace=True)

        return final_df

    except Exception as e:
        print("Error:", e)
        return pd.DataFrame()
