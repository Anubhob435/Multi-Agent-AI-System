import requests

url = ('https://newsapi.org/v2/everything?'
       'q=Apple&'
       'from=2025-06-14&'
       'sortBy=popularity&'
       'apiKey=get_from_env("NEWS_API_KEY")')

response = requests.get(url)

print (response.json)