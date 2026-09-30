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
TIMEOUT = 10  # segundos máximos de espera por cada llamada a la API

if not API_KEY:
    print("AVISO: no se encontró TMDB_API_KEY. Crea un archivo .env con tu llave (ver README).")

# Diccionario de géneros para el Sidebar
IMPORTANT_GENRES = {
    "Acción": 28, "Aventura": 12, "Animación": 16, "Comedia": 35,
    "Crimen": 80, "Drama": 18, "Fantasía": 14, "Terror": 27,
    "Romance": 10749, "Ciencia ficción": 878, "Suspenso": 53
}

# --- FUNCIONES DE APOYO ---

def tmdb_get(path, **params):
    """
    Única función que consulta la API de TMDB.
    - Agrega la API key y el idioma.
    - Codifica los parámetros de forma segura (búsquedas con &, acentos, etc.).
    - Usa timeout y devuelve {} si algo falla, para que la app no se caiga.
    """
    params.update({"api_key": API_KEY, "language": LANG})
    try:
        response = requests.get(f"{BASE_URL}{path}", params=params, timeout=TIMEOUT)
        response.raise_for_status()
        return response.json()
    except (requests.RequestException, ValueError) as error:
        # Solo registramos el tipo de error: el mensaje completo incluye la URL con la API key.
        app.logger.warning("Falló la consulta a TMDB (%s): %s", path, type(error).__name__)
        return {}

def get_genres():
    """Retorna la lista de géneros para el sidebar"""
    return [{"id": v, "name": k} for k, v in IMPORTANT_GENRES.items()]

def get_popular():
    """Obtiene películas populares y tendencia para el inicio"""
    tendencia = tmdb_get("/trending/movie/week").get("results", [])
    populares = tmdb_get("/movie/popular").get("results", [])
    return tendencia + populares

def search_movies(query):
    """Busca películas por texto"""
    return tmdb_get("/search/movie", query=query).get("results", [])

def get_recommendations(movie_id):
    """
    Recomendaciones generadas por TMDB (similitud de contenido y
    comportamiento de usuarios). La app las consulta y las muestra.
    """
    return tmdb_get(f"/movie/{movie_id}/recommendations").get("results", [])

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
    query = (request.args.get("q") or "").strip()
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
    movies = tmdb_get("/discover/movie", with_genres=genre_id).get("results", [])
    genre_name = next((name for name, id in IMPORTANT_GENRES.items() if id == genre_id), "Género")

    return render_template(
        "index.html",
        genres=get_genres(),
        movies=movies,
        title=f"Género: {genre_name}"
    )

@app.route("/movie/<int:movie_id>")
def movie(movie_id):
    movie_data = tmdb_get(f"/movie/{movie_id}")
    if not movie_data:
        return (
            "<p>No pudimos cargar esta película en este momento. Intenta de nuevo más tarde.</p>"
            "<p><a href='/'>Volver al inicio</a></p>",
            503
        )

    similar_movies = get_recommendations(movie_id)

    return render_template(
        "movie.html",
        movie=movie_data,
        similar=similar_movies[:10],
        genres=get_genres()
    )

if __name__ == "__main__":
    app.run(debug=True)