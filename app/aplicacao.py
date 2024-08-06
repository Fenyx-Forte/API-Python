import polars as pl
import requests
from sendgrid_teste import email_sendgrid


def api_fake_store():
    API_URL = "https://fakestoreapi.com/products"

    params = {"limit": 3}

    response = requests.get(API_URL, params=params)

    response_json = response.json()

    print(response_json)


def api_random_user():
    API_URL = "https://randomuser.me/api/"

    response = requests.get(API_URL)

    print(response.status_code)

    print(response.json())


def api_random_user_female():
    API_URL = "https://randomuser.me/api/"

    params = {"gender": "female", "nat": "de"}

    response = requests.get(API_URL, params=params)

    print(response.status_code)

    print(response.json())


def api_cat():
    API_URL = "https://api.thecatapi.com/v1/breeds"

    response = requests.get(API_URL)

    print(response.status_code)

    print(response.json())


def api_dog():
    API_URL = "https://api.thedogapi.com/v1/breeds"

    response = requests.get(API_URL)

    print(response.status_code)

    if response.status_code == 200:
        print(response.json())


def integrar_polars_com_requests():
    API_URL = "https://api.thecatapi.com/v1/breeds"

    response = requests.get(API_URL)

    dados = response.json()

    df = pl.DataFrame(dados)

    print(df)


def testando_sendgrid():
    email_sendgrid.enviar_email_teste()
