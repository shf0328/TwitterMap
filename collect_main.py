from collect.get_from_twitter_api import start_stream, load_key_words
from collect import elastic_search
import time

if __name__ == '__main__':
    # elastic_search.delete_index()
    # elastic_search.create_index()
    sleep_time = 1
    while True:
        r = start_stream(load_key_words(), elastic_search.upload_to_es)
        if r != "":
            sleep_time *= 2
            if sleep_time > 70:
                sleep_time = 70
        time.sleep(sleep_time)

