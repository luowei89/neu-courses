DELETE /crawler_data

PUT /crawler_data/
{
  "settings": {
    "index": {
      "store": {
        "type": "default"
      },
      "number_of_shards": 1,
      "number_of_replicas": 1
    },
    "analysis": {
      "analyzer": {
        "my_english": { 
          "type": "english",
          "stopwords_path": "stoplist.txt"
        }
      }
    }
  }
}

PUT /crawler_data/document/_mapping
{
  "document": {
    "properties": {
      "id": {
        "type": "string",
        "store": true,
        "index": "not_analyzed"
      },
      "title": {
        "type": "string",
        "store": true,
        "index": "analyzed",
        "analyzer": "my_english"
      },
      "text": {
        "type": "string",
        "store": true,
        "index": "analyzed",
        "term_vector": "with_positions_offsets_payloads",
        "analyzer": "my_english"
      },
      "html": {
        "type": "string",
        "store": true,
        "index": "no"
      },
      "inlinks": {
        "type" : "string", 
        "index" : "no"
      },
      "outlinks": {
        "type" : "string", 
        "index" : "no"
      }
    }
  }
}