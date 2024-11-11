import os 

# assets and cache by default
assets_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "assets")
cache_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "cache")

class Color:
    BLACK = (0,0,0)
    