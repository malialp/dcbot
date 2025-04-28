import re

def validate_film_url(url: str):
    patterns = [
        r"^https:\/\/(?:www\.)?imdb\.com\/title\/tt\d+\/?(\?[^\/\s]+)?$",  # IMDB
        r"^https:\/\/letterboxd\.com\/film\/[a-z0-9-]+\/?(\?[^\/\s]+)?$",  # Letterboxd
        r"^https:\/\/boxd\.it\/[a-z0-9]+\/?(\?[^\/\s]+)?$"  # Boxd.it
    ]
    
    for pattern in patterns:
        if re.match(pattern, url):
            return True
    return False

def validate_spotify_url(link):
    pattern = r'^https://open\.spotify\.com/[^/]+/track/[A-Za-z0-9]+(?:\?.*)?$'
    return bool(re.match(pattern, link))