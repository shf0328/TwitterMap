import json
from elasticsearch import Elasticsearch

es = Elasticsearch('https://search-my-es-for-cc-x4kz3eyvmftufvm6lqh43sepf4.us-east-2.es.amazonaws.com')

# for key in ["google", "apple", "phone", "amazon", "nike", "sports", "music", "movie", "song"]:
returns = es.search(
    index='my_twitter_index',
    doc_type='tweet',
    body={
        "size": 10000,
        "query": {
            "bool": {
                "filter": [
                    {
                        "match": {"keyword": "apple"}
                    },

                ]
            }
        },
        "sort": [
            {"created_at": "asc"}
        ]
    }
)
print(returns)
