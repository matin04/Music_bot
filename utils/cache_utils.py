import os


def get_cached_song_path(query):
    safe_name = query.replace("/", "_").replace("\\", "_")

    path = f"cache/{safe_name}.mp3"

    if os.path.exists(path):
        return path

    return None


def save_to_cache(original_path, query):

    safe_name = query.replace("/", "_").replace("\\", "_")

    cache_path = f"cache/{safe_name}.mp3"

    if not os.path.exists(cache_path):

        with open(original_path, "rb") as src:
            with open(cache_path, "wb") as dst:
                dst.write(src.read())

    return cache_path