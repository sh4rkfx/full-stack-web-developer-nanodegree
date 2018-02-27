import json
import media
import fresh_tomatoes

# defining an empty list which will be automatically filled later
movies_list = []

# reading from the JSON file, which contains all movie data
with open("movies.json") as data:
    movies = json.load(data)

# create instances for movies from 0 to 14
for movie_obj in range(0, 14):  # TODO iterate over all elements in JSON file
    movie_obj = media.Movie(movies[movie_obj]["movie_title"],
                            movies[movie_obj]["poster_image_url"],
                            movies[movie_obj]["trailer_youtube_url"],
                            movies[movie_obj]["movie_year"])
    movies_list.append(movie_obj)

# passing list of movies to the given function and create HTML page
fresh_tomatoes.open_movies_page(movies_list)
