from flask import Flask, request, jsonify
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend-backend communication

# Load datasets
movies_file = "movies.csv"
ratings_file = "ratings.csv"

movies_df = pd.read_csv(movies_file)
ratings_df = pd.read_csv(ratings_file)

# Preprocess movie genres (replace '|' with spaces for better similarity matching)
movies_df['genres'] = movies_df['genres'].fillna('')

# TF-IDF Vectorizer to convert genres into numerical features
vectorizer = TfidfVectorizer(stop_words="english")
tfidf_matrix = vectorizer.fit_transform(movies_df['genres'])

@app.route("/recommend", methods=["POST"])
def recommend():
    data = request.json
    movie_name = data.get("movie", "").lower()
    
    if not movie_name:
        return jsonify({"error": "Movie name is required"}), 400
    
    # Find movie index
    movie_idx = movies_df[movies_df['title'].str.lower().str.contains(movie_name)].index
    if movie_idx.empty:
        return jsonify({"recommendations": ["Movie not found in dataset"]})

    # Compute similarity
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    similar_movies = cosine_sim[movie_idx[0]]

    # Get top 5 similar movies
    recommended_indices = similar_movies.argsort()[-6:-1][::-1]
    recommendations = movies_df.iloc[recommended_indices]['title'].tolist()

    return jsonify({"recommendations": recommendations})

if __name__ == "__main__":
    app.run(debug=True, port=5000)