import requests
from decouple import config

def translate(q):
    google_key = config("GOOGLE_API_KEY")

    api_url = "https://translation.googleapis.com/language/translate/v2"

    data = {
        'q': q,
        'source': 'ko',
        'target': 'en'
    }

    response = requests.post(f'{api_url}?key={google_key}', data)
    return response.json()['data']['translations'][0]['translatedText']