# CineBot - Recomendador de Películas

Aplicación web hecha con **Python y Flask** que consume la API de [TMDB (The Movie Database)](https://www.themoviedb.org/) para buscar películas, explorarlas por género y mostrar recomendaciones similares. Proyecto académico desarrollado para la clase de **Inteligencia Artificial** (Tecmilenio).

## Qué permite hacer

- Ver las películas **en tendencia y populares** de la semana en la página de inicio.
- **Buscar una película por nombre** y ver recomendaciones basadas en ella (hasta 10).
- **Explorar por género** desde el menú lateral: Acción, Aventura, Animación, Comedia, Crimen, Drama, Fantasía, Terror, Romance, Ciencia ficción y Suspenso.
- Abrir la **página de detalle** de una película y ver títulos similares.
- Contenido en español de México (`es-MX`).

## Cómo funcionan las recomendaciones

Las recomendaciones las genera el servicio de TMDB a través de su endpoint `/movie/{id}/recommendations`. La aplicación se encarga de enviar las consultas, procesar las respuestas y mostrarlas en la interfaz. **No incluye un modelo de recomendación propio.**

## Tecnologías

Python · Flask · API REST (TMDB) · Requests · python-dotenv · HTML/Jinja · CSS

## Requisito: API Key de TMDB

Por seguridad, este repositorio **no incluye** la llave de acceso. Para que el proyecto funcione necesitas una propia:

1. Regístrate en [The Movie Database (TMDB)](https://www.themoviedb.org/).
2. Ve a tu perfil > Configuración > API y genera una **API Key (v3 auth)**.

## Instalación y ejecución

**1. Clona el repositorio**

```bash
git clone https://github.com/aramrdz06/Proyecto-de-recomendaciones
cd Proyecto-de-recomendaciones
```

**2. (Opcional) Crea un entorno virtual**

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
```

**3. Instala las dependencias**

```bash
pip install -r requirements.txt
```

**4. Crea el archivo `.env`** en la carpeta del proyecto con tu llave:

```
TMDB_API_KEY=tu_api_key_aqui
```

El archivo `.env` está en `.gitignore`, así que no se sube al repositorio.

**5. Ejecuta la aplicación**

```bash
python app.py
```

Abre en tu navegador la dirección que aparece en la terminal (normalmente `http://127.0.0.1:5000`).

## Estructura del proyecto

```
├── app.py              # Rutas de Flask y consumo de la API de TMDB
├── templates/          # Páginas HTML (index.html, movie.html)
├── static/             # Estilos (style.css)
├── requirements.txt    # Dependencias
├── .gitignore
└── README.md
```

## Créditos

Este producto usa la API de TMDB, pero no está avalado ni certificado por TMDB.

## Autor

Francisco Aram Rodríguez García · [GitHub](https://github.com/aramrdz06)