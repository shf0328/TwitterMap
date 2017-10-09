import pprint
from elasticsearch import Elasticsearch
from datetime import datetime

es = Elasticsearch('https://search-my-es-for-cc-x4kz3eyvmftufvm6lqh43sepf4.us-east-2.es.amazonaws.com')
index = 'my_twitter_index'
doc_type = 'tweet'


def convert(original_time):
    original_time="2017-10-08T12:30"
    timestamp = datetime.strptime(original_time, '%Y-%m-%dT%H:%M')
    return timestamp.strftime('%a %b %d %H:%M:%S +0000 %Y')


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
    # other()
    # print(es.count(
    #     index='my_twitter_index',
    #     doc_type='tweet',))
    print(search_area(10, -73.99, 40))