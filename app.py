import streamlit as st
import pandas as pd
import ast
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def load_data():
    movies = pd.read_csv("tmdb_5000_movies.csv")
    credits = pd.read_csv("tmdb_5000_credits.csv")
    # Merging data based on title
    movies = movies.merge(credits, on='title')
    
    def convert(val):
        try:
            return [i['name'] for i in ast.literal_eval(val)]
        except:
            return []
    
    movies['genres'] = movies['genres'].apply(convert)
    movies['keywords'] = movies['keywords'].apply(convert)
    
    def get_main_cast(val):
        try:
            return [i['name'] for i in ast.literal_eval(val)[:3]] 
        except:
            return []
    
    movies['cast'] = movies['cast'].apply(get_main_cast)
    
    def get_director(val):
        try:
            for i in ast.literal_eval(val):
                if i['job'] == 'Director':
                    return i['name']
        except:
            return ''
        return ''
    
    movies['crew'] = movies['crew'].apply(get_director) 
    movies['tags'] = movies['overview'] + movies['genres'].astype(str) + movies['keywords'].astype(str) + movies['cast'].astype(str) + movies['crew']
    movies.dropna(subset=['tags'], inplace=True)
    movies['tags'] = movies['tags'].str.lower()
    #term frquency 
    tfidf = TfidfVectorizer(max_features=5000, stop_words='english')
    tfidf_matrix = tfidf.fit_transform(movies['tags'])
    # applying Cosine Similarity
    similarity = cosine_similarity(tfidf_matrix)
    return movies, similarity
#to add traliers
from youtubesearchpython import VideosSearch

def get_trailer(movie_name):
    try:
        search = VideosSearch(f"{movie_name} trailer", limit=1)
        return search.result()['result'][0]['link']
    except:
        return "Trailer not found"
def recommend_by_movie(movie):
    movie = movie.lower()
    if movie not in movies['title'].str.lower().values:
        return "Sorry, movie not found."
    
    index = movies[movies['title'].str.lower() == movie].index[0]
    distances = list(enumerate(similarity[index]))
    
    sorted_movies = sorted(distances, key=lambda x: x[1], reverse=True)[1:11]

    recommendations = []
    for i in sorted_movies:
        title = movies.iloc[i[0]].title
        trailer_link = get_trailer(title)  
        recommendations.append(f"{title} 🎬: {trailer_link}")
    return recommendations

def recommend_by_genre(genre):
    genre = genre.lower()
    genre_series = movies['genres'].fillna('').astype(str).str.lower()
    genre_movies = movies[genre_series.str.contains(genre)]
    if genre_movies.empty:
        return "Sorry, Try another genre."
    #getting row number of the movie for the given genre
    genre_indices = genre_movies.index.tolist() 
    #finding the avg similarity score for the genre and adding it next to movie index
    mean_similarity = sum(similarity[i] for i in genre_indices) / len(genre_indices)
    distances = list(enumerate(mean_similarity))
    
    sorted_movies = sorted(distances, key=lambda x: x[1], reverse=True)[1:11] 

    recommendations = []
    for i in sorted_movies:
        title = movies.iloc[i[0]].title
        trailer_link = get_trailer(title)  
        recommendations.append(f"{title} 🎬: {trailer_link}")

    return recommendations

movies, similarity = load_data()

# Streamlit

st.title("🎬 Movie Recommender with Trailers")
st.markdown("""
    <style>
    body {
        background-color: #000000;
        color: #ffffff;
    }
    .stApp {
        background-color: #141414;
    }
    h1 {
        color: #e50914;
        font-family: 'Graphique';
        font-size: 60px;
        text-align: center;
    }
    .css-1cpxqw2, .stRadio > div {
        color: white;
    }
    .stTextInput > div > input {
        background-color: #333333;
        color: white;
    }
    .stButton>button {
        background-color: #e50914;
        color: white;
        font-weight: bold;
        border-radius: 5px;
    }
    </style>
""", unsafe_allow_html=True)
mode = st.radio("Select Recommendation Mode", ['By Movie Title', 'By Genre'])

if mode == 'By Movie Title':
    movie_name = st.text_input("Enter a Movie Title:")
    if st.button("Recommend by Movie"):
        results = recommend_by_movie(movie_name)
        for r in results:
            st.markdown(r)

if mode == 'By Genre':
    genre = st.text_input("Enter Genre (e.g., Action, Comedy):")
    if st.button("Recommend by Genre"):
        results = recommend_by_genre(genre)
        for r in results:
            st.markdown(r)
