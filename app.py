import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_posters(movie_id):
    response = requests.get("https://api.themoviedb.org/3/movie/{}?api_key=7d40312e8cb61fc1c6c675fa49bcf1e0&language=en-US".format(
        movie_id))
    data = response.json()
    if 'poster_path' in data:
        return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    else:
        return None

def recommend(movie_title):
    movie_index = movies[movies['title'] == movie_title].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    recommended_movies_poster =[]
    for i in movies_list:
        movie_id = movies.iloc[i[0]]['movie_id']
        poster_url = fetch_posters(movie_id)
        if poster_url:
            recommended_movies_poster.append(poster_url)
            recommended_movies.append(movies.iloc[i[0]]['title'])
    return recommended_movies, recommended_movies_poster

movies_dict = pickle.load(open('movies_dict1.pkl','rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl','rb'))

st.title('Movie Recommender System')
selected_movie_title = st.selectbox(
    'Select a movie',
    movies['title'].values
)


if st.button('Show Recommendations'):
    names, poster = recommend(selected_movie_title)
    num_recommendations = len(names)
    with st.container():
        st.markdown("<div style='display: flex;'>", unsafe_allow_html=True)
        for name, poster_url in zip(names, poster):
            st.markdown(f"<div style='margin-right: 20px;'><h2>{name}</h2><img src='{poster_url}' style='width: 200px;'></div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)