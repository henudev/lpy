import requests

def search_duckduckgo(query):
    url = 'https://api.duckduckgo.com/'
    params = {
        'q': query,
        'format': 'json'
    }
    response = requests.get(url, params=params)
    return response.json()

if __name__ == "__main__":
    query = "Python 中文是什么"
    results = search_duckduckgo(query)
    print(results)