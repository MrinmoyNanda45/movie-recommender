import streamlit as st
import pandas as pd
import pickle
import requests
import os

api_key = os.getenv("TMDB_API_KEY")  # Fetch from Render env

def recommend(movie):
    movie_index = movies[movies['original_title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    return [movies.iloc[i[0]] for i in movies_list]

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}"
    data = requests.get(url).json()
    poster_path = data.get('poster_path', '')
    return f"https://image.tmdb.org/t/p/w185{poster_path}" if poster_path else "https://via.placeholder.com/185x278?text=No+Poster"

# Load data
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame.from_dict(movies_dict, orient='index')
similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movies Recommender System')

selected_movie_name = st.selectbox(
    "Pick a movie to get recommendations",
    movies['original_title'].values
)

if st.button('Recommend'):
    recommendations = recommend(selected_movie_name)
    st.subheader("Top Picks:")
    cols = st.columns(5)
    for i, movie in enumerate(recommendations):
        with cols[i]:
            poster_url = fetch_poster(movie['id'])
            st.image(poster_url, width=100)
            st.write(movie['original_title'])