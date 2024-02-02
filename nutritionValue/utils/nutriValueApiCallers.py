import requests

def get_nutrition_info(query):
    api_url = 'https://api.calorieninjas.com/v1/nutrition?query='
    api_key = 'Lmaxuo3f+uwsJogaJdwx8g==YNuJfB0IsSWqpsC6'

    response = requests.get(api_url + query, headers={'X-Api-Key': api_key})

    if response.status_code == requests.codes.ok:
        return response.text
    else:
        return f"Error: {response.status_code}, {response.text}"


def analyze_image(path_to_file):
    api_key = 'kHJzFX3T.LNXwgqLRrSsU4As5gIFNPoBhtEf7pQez'
    url = "https://vision.foodvisor.io/api/1.0/en/analysis/"
    headers = {"Authorization": f"Api-Key {api_key}"}

    with open(path_to_file, "rb") as image:
        response = requests.post(url, headers=headers, files={"image": image})
        response.raise_for_status()

    return response.json()