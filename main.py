from dotenv import load_dotenv
import shodan
import os

# load the secrets from the .env file
load_dotenv()
api_key = os.getenv("API_KEY")
countries = 'de' # 'at,de,ch'
products = 'tasmota'


try:
    api = shodan.Shodan(api_key)

    print(f'[i] Currently searching for: country:{countries} product:{products}')

    results = api.search(f'country:{countries} product:{products}', 5)
    print(results)

except Exception as e:
    print("Something unexepected happend:" + e)