from dotenv import load_dotenv
from selenium import webdriver
from datetime import datetime
import shodan
import os
import httpx
import asyncio
import json

# load the secrets from the .env file
load_dotenv()
api_key = os.getenv("API_KEY")

# saving paths for data collection
screenshotPath = './screenshots/'
datePath = f'{screenshotPath}{datetime.today().strftime("%Y%m%d")}' 
vendorPath = ''
countries = 'DE' # 'AT,DE,CH'
vendors = ['tasmota', 'openhab', 'shelly'] 
debug = 0

targets = []
targetsAll = []

def createFolderStructure(vendor):

    global vendorPath
    vendorPath = f'{datePath}/{vendor}'

    if not os.path.exists(screenshotPath):
        os.makedirs(screenshotPath)
    
    if not os.path.exists(datePath):
        os.makedirs(datePath)
    
    if not os.path.exists(vendorPath):
        os.makedirs(vendorPath)

def queryShodanDevices(vendor):
        # Connecting to shodan using the API-Key
        api = shodan.Shodan(api_key)
        # Query shodan for the given country and product
        query = f'country:{countries} {vendor}'

        print(f'[i] Currently searching for: {query}')
        # Limit search results to 1 pages - currently only for developing purposes
        results = api.search(query, 1)

        # Clearing the targets list in order to have a clean list per vendor
        targets.clear
        targetsAll.append(results)

        # go through the matches and save the ip + port for later asynchronmotor requests
        for service in results['matches']:
            targets.append(f"{service['ip_str']}:{service['port']}")

async def queryRequests():
    try:
        # Creating async-client to to through the found ip + port with limited connections
        async with httpx.AsyncClient(limits=httpx.Limits(max_connections=10)) as client:
            tasks = [fetchDevice(client, target) for target in targets]
            results = await asyncio.gather(*tasks)
            
            print(f'[i] Devices without result: {results.count(None)}')


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

            # Once we have a successful hit, we should be able to take a screenshot
            await takeScreenshot(target)
        return response.status_code

    except Exception as e:
        # The crawl can fail for various reasons such as timeout, unavailability, read errors, etc.
        if debug:    
            print(f'Error fetching {url} - {e}')

async def takeScreenshot(target):
    # starting firefox in headless mode so we're not stuck with a browser window
    options = webdriver.FirefoxOptions()
    options.add_argument('-headless')

    # TO BE TESTED - Ignore all cert issues, as most devices only have self signed certificates 
    # options.accept_insecure_certs = True
    try:
        # starting the headless browser to take a screenshot of the websites root page
        driver = webdriver.Firefox(options)
        driver.get(f'http://{target}')

        # save the screenshot - for now it's sufficent to just save it with the ip + port
        path = f'{vendorPath}/{target}.png'
        driver.save_screenshot(path)
        driver.quit
    except Exception as e:
        print(f'Failed to take screenshot - {e}')

def saveDataToJSON():
    # saving all the collected data from each vendor in the json file just to have the data
    path = f'{datePath}/data.json'
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(targetsAll, f, ensure_ascii=False, indent=4)

async def main():
    debug = 1

    for vendor in vendors:
        createFolderStructure(vendor)
        queryShodanDevices(vendor)
        await queryRequests()
    saveDataToJSON()
asyncio.run(main())