# Shodan-Crawler
Simple Shodan Crawler Proof of Concept for my Bachelor Thesis 

# Setup
Prepare the virtual environment
```
python3 -m venv .
source /bin/activate
```

And install the requirements
```
pip3 install -r requirements.txt
```

Do not forget to add your shodan API-Key 
```
echo 'API_KEY=XXX' > .env
```

## Sidenote
As for now, even though the webdriver manger should handle all of the geckodriver dependencies, the script still requires a locally installede firefox instance. It's a known issue, the current workaround is to install firefox
```
sudo apt install firefox
```

# ToDo's

- [x] Make the requests async to guarantee better performance
- [ ] Check for SSL issues (and ignore them)
- [ ] Pretty output
- [ ] Save all the data in a meaningful output such as a JSON 
- [x] Make automated screenshots using something like selenium
- [ ] Refactor Code
