class Movie():
    # defining constructor with common movie attributes
    def __init__(self, movie_title, poster_image_url,
                 trailer_youtube_url, movie_year):
        self.movie_title = movie_title
        self.poster_image_url = poster_image_url
        self.trailer_youtube_url = trailer_youtube_url
        self.movie_year = movie_year
