from dotenv import load_dotenv
import shodan
import os
import httpx
import asyncio

# load the secrets from the .env file
load_dotenv()
api_key = os.getenv("API_KEY")
countries = 'DE' # 'AT,DE,CH'
products = 'tasmota'
debug = 0

targets = []

def queryShodanDevices():
        # Connecting to shodan using the API-Key
        api = shodan.Shodan(api_key)
        # Query shodan for the given country and product
        query = f'country:{countries} {products}'

        print(f'[i] Currently searching for: {query}')
        # Limit search results to 5 pages - currently only for developing purposes
        results = api.search(query, 5)

        # go through the matches and save the ip + port for later asynchronmotor requests
        for service in results['matches']:
            targets.append(f"{service['ip_str']}:{service['port']}")

async def queryRequests():
    try:
        # Creating async-client to to through the found ip + port with limited connections
        async with httpx.AsyncClient(limits=httpx.Limits(max_connections=10)) as client:
            tasks = [fetchDevice(client, target) for target in targets]
            results = await asyncio.gather(*tasks)

    except Exception as e:
        if debug:
            print(f'Something unexepected happend! \n {e}')


async def fetchDevice (client, target):
    try:
        # trying to fetch found target
        url = f'http://{target}'
        response = await client.get(url, timeout=10)
        if response.status_code == 200:
            print(f'Success for: {url}')
        return response.status_code

    except Exception as e:
        # The crawl can fail for various reasons such as timeout, unavailability, read errors, etc.
        if debug:    
            print(f'Error fetching {url} - {e}')


async def main():
    debug = 0
    queryShodanDevices()
    await queryRequests()

asyncio.run(main())