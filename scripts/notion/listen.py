import json
from listennotes import podcast_api


client = podcast_api.Client(api_key='b3f373f4ec7b49b9ab96226d9d1effe6')
response = client.search(
  q='42章经',
  sort_by_date=0,
  type='podcast',
  offset=0,
  page_size=10,
)
print(json.dumps(response.json()))