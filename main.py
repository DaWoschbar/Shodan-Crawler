from dotenv import load_dotenv
import shodan
import os
import requests

# load the secrets from the .env file
load_dotenv()
api_key = os.getenv("API_KEY")
countries = 'DE' # 'at,de,ch'
products = 'tasmota'

found_ips = []

dbg_count = 0

try:
    api = shodan.Shodan(api_key)
    query = f'country:{countries} {products}'

    print(f'[DBG] Currently searching for: {query}')
    results = api.search(query, 5)

    for service in results['matches']:
        if (dbg_count > 5):
            break
        else:
            dbg_count += 1

        found_ips.append(service['ip_str'])

        try:
            r = requests.get(f'http://{service['ip_str']}:{service['port']}', timeout=10)
            print(r)
        except requests.exceptions.Timeout:
            print(f"Timeout reached - skipped for {service['ip_str']}:{service['port']}")


except Exception as e:
    print("Something unexepected happend!")
    print(e)
