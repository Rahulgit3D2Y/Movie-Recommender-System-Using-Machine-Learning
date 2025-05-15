
import pickle
import streamlit as st
import requests

def fetch_poster_and_link(movie_id):
    try:
        api_key = "8265bd1679663a7ea12ac168da84d2e8"
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        poster_path = data.get('poster_path')
        poster_url = f"https://image.tmdb.org/t/p/w500/{poster_path}" if poster_path else "https://via.placeholder.com/500x750?text=No+Image"
        movie_url = f"https://www.themoviedb.org/movie/{movie_id}"
        return poster_url, movie_url
    except Exception as e:
        print("API error:", e)
        return "https://via.placeholder.com/500x750?text=No+Image", "#"


def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    names, posters, links = [], [], []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        poster_url, movie_url = fetch_poster_and_link(movie_id)
        names.append(movies.iloc[i[0]].title)
        posters.append(poster_url)
        links.append(movie_url)
    return names, posters, links


st.header('Movie Recommender System Using Machine Learning')
movies = pickle.load(open('artifacts/movie_list.pkl','rb'))
similarity = pickle.load(open('artifacts/similarity.pkl','rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    names, posters, links = recommend(selected_movie)
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.markdown(f"**{names[i]}**", unsafe_allow_html=True)
            st.markdown(
                f"<a href='{links[i]}' target='_blank'><img src='{posters[i]}' width='100%' style='border-radius:10px;'/></a>",
                unsafe_allow_html=True
            )

