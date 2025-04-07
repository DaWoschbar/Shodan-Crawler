from dotenv import load_dotenv
from selenium import webdriver
from datetime import datetime
import shodan
import os
import httpx
import asyncio
import json
import requests

# load the secrets from the .env file
load_dotenv()
api_key = os.getenv("API_KEY")
debug = 0

# saving paths for data collection
screenshotPath = './screenshots/'
datePath = f'{screenshotPath}{datetime.today().strftime("%Y%m%d")}' 
vendorPath = ''
countries = 'DE' # 'AT,DE,CH'
vendors = ['tasmota']#, 'openhab']#, 'openhab', 'shelly'] 

def createFolderStructure(vendor):
    # defining a global var to save the path for each vendor
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
        result = api.search(query, 1)
        return result['matches']

async def queryRequests(matches):

    try:
        # Creating async-client to to through the found ip + port with limited connections
        targets = []
        successfulTargets = []

        # create a list for asyncClient to go through all the gathered hosts
        # in the format ip + port
        for match in matches:
            targets.append(f'{match['ip_str']}:{match['port']}')

        try:
            # execute async function to fetch the client
            async with httpx.AsyncClient(limits=httpx.Limits(max_connections=10)) as client:
                tasks = [fetchTarget(client, target) for target in targets]
                # all successfully connected targets are returned here
                connectedTarget = await asyncio.gather(*tasks)
        
        except Exception as e:
            print(f'An error occured while connecting {e}')

        # Go through all matches and compare them with the successful targets
        # if any match, save them including all of their fields in a new list
        for match in matches:
            if match['ip_str'] in connectedTarget:
                successfulTargets.append(match) 

        return successfulTargets

    except Exception as e:
        if debug:
            print(f'Something unexepected happend! \n {e}')

async def fetchTarget (client, target):
    try:
        # trying to fetch found target
        url = f'http://{target}'

        response = await client.get(url, timeout=10)
        if response.status_code == 200:
            print(f'Success for: {url}')

            # Once we have a successful hit, we should be able to take a screenshot
            takeScreenshot(target)
            
            # split the target so that we can create a list of just the successful ip adresses
            ip = target.split(':')[0]
            return ip

    except Exception as e:
        # The crawl can fail for various reasons such as timeout, unavailability, read errors, etc.
        if debug:    
            print(f'Error fetching {url} - {e}')

def takeScreenshot(target):
    # starting firefox in headless mode so we're not stuck with a browser window
    options = webdriver.FirefoxOptions()
    options.add_argument('-headless')
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

def saveDataToJSON(successfulTargets):
    # saving all the collected data in a json file just to have the data for later analysis
    path = f'{datePath}/data.json'
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(successfulTargets, f, ensure_ascii=False, indent=4)

async def main():
    debug = 1
    successfulTargets = []

    for vendor in vendors:
        createFolderStructure(vendor)
        matches = queryShodanDevices(vendor)
        successfulTargets.append(await queryRequests(matches))

    saveDataToJSON(successfulTargets)
asyncio.run(main())
