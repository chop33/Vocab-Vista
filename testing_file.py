import requests

search_url = f'https://openlibrary.org/search.json?q=bible&has_fulltext=true&format=Epub&fields=key,title,author_name,editions&limit=1'

response = requests.get(search_url)
print(response.text)
# response = response.json()
# key = response["docs"][0]["key"]
# key = key.split("/")[-1]
# print(key)

# response = requests.get(f'https://openlibrary.org/download/{key}/epub')
# print(response.text)