from flask import Flask, render_template, request
import requests
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

app = Flask(__name__)

# Configuración Global segura
API_KEY = os.getenv("TMDB_API_KEY") 
BASE_URL = "https://api.themoviedb.org/3"
LANG = "es-MX"

# Diccionario de géneros para el Sidebar
IMPORTANT_GENRES = {
    "Acción": 28, "Aventura": 12, "Animación": 16, "Comedia": 35,
    "Crimen": 80, "Drama": 18, "Fantasía": 14, "Terror": 27,
    "Romance": 10749, "Ciencia ficción": 878, "Suspenso": 53
}

# --- FUNCIONES DE APOYO ---

def get_genres():
    """Retorna la lista de géneros para el sidebar"""
    return [{"id": v, "name": k} for k, v in IMPORTANT_GENRES.items()]

def get_popular():
    """Obtiene películas populares y tendencia para el inicio"""
    url_t = f"{BASE_URL}/trending/movie/week?api_key={API_KEY}&language={LANG}"
    url_p = f"{BASE_URL}/movie/popular?api_key={API_KEY}&language={LANG}"
    
    try:
        r1 = requests.get(url_t).json().get("results", [])
        r2 = requests.get(url_p).json().get("results", [])
        return r1 + r2
    except:
        return []

def search_movies(query):
    """Busca películas por texto"""
    url = f"{BASE_URL}/search/movie?api_key={API_KEY}&query={query}&language={LANG}"
    return requests.get(url).json().get("results", [])

def get_recommendations(movie_id):
    """
    EL MOTOR DE IA: TMDB usa algoritmos de similitud de contenido 
    y comportamiento de usuarios para estas recomendaciones.
    """
    url = f"{BASE_URL}/movie/{movie_id}/recommendations?api_key={API_KEY}&language={LANG}"
    return requests.get(url).json().get("results", [])

# --- RUTAS DE LA APLICACIÓN ---

@app.route("/")
def home():
    return render_template(
        "index.html",
        genres=get_genres(),
        movies=get_popular(),
        title="Películas Destacadas"
    )

@app.route("/search")
def search():
    query = request.args.get("q")
    movies = search_movies(query) if query else []
    
    recommendations = []
    main_movie = None

    if movies:
        main_movie = movies[0] 
        recommendations = get_recommendations(main_movie['id'])

    return render_template(
        "index.html",
        genres=get_genres(),
        movies=movies,
        recommendations=recommendations[:10],
        main_movie=main_movie,
        query=query
    )

@app.route("/genre/<int:genre_id>")
def genre(genre_id):
    url = f"{BASE_URL}/discover/movie?api_key={API_KEY}&with_genres={genre_id}&language={LANG}"
    movies = requests.get(url).json().get("results", [])
    genre_name = next((name for name, id in IMPORTANT_GENRES.items() if id == genre_id), "Género")
    
    return render_template(
        "index.html",
        genres=get_genres(),
        movies=movies,
        title=f"Género: {genre_name}"
    )

@app.route("/movie/<int:movie_id>")
def movie(movie_id):
    url_m = f"{BASE_URL}/movie/{movie_id}?api_key={API_KEY}&language={LANG}"
    movie_data = requests.get(url_m).json()
    similar_movies = get_recommendations(movie_id)

    return render_template(
        "movie.html",
        movie=movie_data,
        similar=similar_movies[:10],
        genres=get_genres()
    )

if __name__ == "__main__":
    app.run(debug=True)