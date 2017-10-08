from collect.get_from_twitter_api import start_stream, load_key_words
from collect import elastic_search


if __name__ == '__main__':
    elastic_search.delete_index()
    elastic_search.create_index()
    start_stream(load_key_words(), elastic_search.upload_to_es)

