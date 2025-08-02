# Movie-Recommender-App
A content-based movie recommender system built with Python, pandas, and scikit-learn, deployed using Streamlit.

## 🚀 Live Demo
Try it here: [movie-recommender-app](https://movie-recommender-app-ecg9fx4szpavuj4uxhrnwg.streamlit.app/#movie-recommender-with-trailers)

## 🔍 Features
- Recommend similar movies based on content (overview, keywords, cast, etc.)
- Uses TF-IDF vectorization and cosine similarity
- User-friendly Streamlit interface
- Clean and simple UI

## 🛠 Built With
- Python 🐍
- pandas
- scikit-learn
- Streamlit

## 📁 Project Structure
movie-recommender-app/
│
├── app.py # Main Streamlit app
├── requirements.txt # Dependencies for deployment
└── README.md 


## 🧠 How It Works
- Loads preprocessed movie and credits datasets
- Merges datasets and extracts key features (overview, cast, crew, etc.)
- Converts text into vectors using `TfidfVectorizer`
- Computes similarity scores with cosine similarity
- Returns top 5 similar movies
