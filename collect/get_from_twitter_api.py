import requests
from requests_oauthlib import OAuth1
import json
import pprint


def load_key_words():
    with open('collect/key_words.json') as fp:
        keywords = json.load(fp)['key_words']
    return keywords


def match_key_word(string, keywords):
    for keyword in keywords:
        if keyword in string:
            return keyword
    return ''


def clean_up_one_tweet(one_tweet, keywords):
    cleaned_tweet = {}
    try:
        # extract location information
        cleaned_tweet['location'] = one_tweet['coordinates']['coordinates']
        # extract text information
        cleaned_tweet['text'] = one_tweet['text']
        # extract time information
        cleaned_tweet['created_at'] = one_tweet['created_at']
        # extract keyword information
        keyword = match_key_word(cleaned_tweet['text'], keywords)
        if keyword != '':
            cleaned_tweet['keyword'] = keyword
        else:
            return None
        # extract author information
        cleaned_tweet['author'] = one_tweet['user']['name']
        # extract author information
        cleaned_tweet['headicon_url'] = one_tweet['user']['profile_image_url_https']
        return cleaned_tweet
    except Exception as e:
        return None


def start_stream(keywords, callback):
    twitter_auth = OAuth1(
        client_key='EqOgAHclBjORupyhHQj71YfTU',
        client_secret='K3YKC3HmWU7XIerp44vqyYzNpQ1dh3HJmdusDf0NZlN5gPAmKR',
        resource_owner_key='783860454225391616-aptFykzX1X4isOcBvZTFYBiETNvCiS5',
        resource_owner_secret='ALfBmHMr1PsnawPEaYW1cW2IBp9SSloCQWQwYf0eEEb8H'
    )

    res = requests.get('https://stream.twitter.com/1.1/statuses/filter.json',
                       stream=True,
                       auth=twitter_auth,
                       params={'track': ','.join(keywords)}
                       )

    for line in res.iter_lines():
        try:
            if line:
                one_tweet = json.loads(line)
                cleaned_tweet = clean_up_one_tweet(one_tweet, keywords)
                if cleaned_tweet:
                    callback(cleaned_tweet)
        except Exception as e:
            print("ERROR!")
            print(str(e))
            return str(e)
    return ""


if __name__ == '__main__':
    with open('key_words.json') as fp:
        local_kws = json.load(fp)['key_words']
    start_stream(local_kws, pprint.pprint)
