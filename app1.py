import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=80a199e1d8f61b28e49e8c0ee5a08c3f&language=en.US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend_movie(movie_name):
    movie_index = movie[movie['title'] == movie_name].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommend_movie = []
    recommend_movie_poster = []
    for i in movie_list:
        movie_id = movie.iloc[i[0]].movie_id
        recommend_movie.append(movie.iloc[i[0]].title)
        recommend_movie_poster.append(fetch_poster(movie_id))
    return recommend_movie, recommend_movie_poster

movie_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movie = pd.DataFrame(movie_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title("Movie Recommend System")
selected_movie_name = st.selectbox("Select a movie:", movie['title'].values)

if st.button('Recommend'):
    names, posters = recommend_movie(selected_movie_name)
    cols = st.columns(5)
    for i, col in enumerate(cols):
        col.text(names[i])
        col.image(posters[i], use_column_width=True)