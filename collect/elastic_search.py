import pprint
import requests
import json
import time
from elasticsearch import Elasticsearch

aws_es = 'https://search-my-es-for-cc-x4kz3eyvmftufvm6lqh43sepf4.us-east-2.es.amazonaws.com'
index = 'my_twitter_index'
doc_type = 'tweet'
es = Elasticsearch(aws_es)


def load_mapping_config():
    with open('collect/mapping.json') as f:
        mapping_config = json.dumps(json.load(f))
        return mapping_config


def get_url():
    return aws_es + '/' + index


def is_exist():
    url = get_url()
    r = requests.get(url)
    if r.status_code == 200:
        return True
    else:
        return False


def delete_index():
    url = get_url()
    if is_exist():
        pprint.pprint(requests.delete(url).json())
    else:
        pprint.pprint({'message': 'no need for delete'})


def create_index():
    url = get_url()
    if not is_exist():
        r = requests.put(url, data=load_mapping_config())
        if r.status_code == 200:
            pprint.pprint(r.json())
        else:
            pprint.pprint(r)
    else:
        pprint.pprint({'message': 'already exist'})


def upload_to_es(twitter):
    es.create(index=index, doc_type=doc_type, id=int(time.time() * 10000) - 15074220541720, body=twitter)
    pass


def search_keyword(size, keyword, datetime):
    returns = es.search(
        index=index, doc_type=doc_type,
        body={
            "size": size,
            "query": {
                "bool": {
                    "filter": [
                        {
                            "match": {"keyword": keyword}
                        },
                        {
                            "range": {
                                "created_at": {
                                    "lte":datetime
                                }
                            }
                        },
                    ]
                }
            },
            "sort": [
                {"created_at": "desc"}
            ]
        }
    )
    return [item['_source'] for item in returns['hits']['hits']]


def search_area(size, lng, lat):
    returns = es.search(
        index=index, doc_type=doc_type,
        body={
            "size": size,
            "query": {
                "bool": {
                    "filter": [
                        {
                            "geo_distance": {
                                "distance": "500km",
                                "location": [lng, lat]
                            }
                        },
                    ]
                }
            },
            "sort": [
                {"created_at": "desc"}
            ]
        }
    )
    return [item['_source'] for item in returns['hits']['hits']]


if __name__ == '__main__':
    is_exist()
