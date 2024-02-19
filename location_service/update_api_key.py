import os
import requests
from pathlib import Path
import environ


def update_api_key():
    BASE_DIR = Path(__file__).resolve().parent.parent
    environ.Env.read_env(os.path.join(BASE_DIR, '.env'))
    env = os.path.join(BASE_DIR, '.env')

    url = "https://www.onemap.gov.sg/api/auth/post/getToken"

    payload = {
        "email": environ.Env()('ONEMAP_API_EMAIL'),
        "password": environ.Env()('ONEMAP_API_PASSWORD')
    }

    response = requests.request("POST", url, json=payload)
    if response.status_code != 200:
        print("Error:", response.json())
        return

    # update the token in .env file
    with open(env, 'r') as file:
        data = file.readlines()
        # find the line with ONE_MAP_TOKEN
        for i in range(len(data)):
            if data[i].startswith("ONEMAP_API_KEY"):
                data[i] = "ONEMAP_API_KEY=" + response.json()['access_token'] + "\n"
                break

        # if the line is not found, add it to the end of the file
        data.append("\nONEMAP_API_KEY=" + response.json()['access_token'] + "\n")

    with open(env, 'w') as file:
        file.writelines(data)

    print("Token updated successfully!")


if __name__ == '__main__':
    update_api_key()
