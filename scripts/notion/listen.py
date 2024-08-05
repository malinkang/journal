import json
from listennotes import podcast_api


client = podcast_api.Client(api_key='b3f373f4ec7b49b9ab96226d9d1effe6')
response = client.search(
  q='42章经',
  sort_by_date=0,
  type='episode',
  offset=0,
  len_min=10,
  len_max=30,
  genre_ids='68,82',
  published_before=1580172454000,
  published_after=0,
  only_in='title,description',
  language='English',
  safe_mode=0,
  unique_podcasts=0,
  interviews_only=0,
  sponsored_only=0,
  page_size=10,
)
print(json.dumps(response.json()))