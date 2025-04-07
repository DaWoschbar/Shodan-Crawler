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
As for now, even though the webdriver manger should handle all of the geckodriver dependencies, the script still requires a locally installed firefox instance. It's a known issue, the current workaround is to install firefox via the package manager of your choice like apt
```
sudo apt install firefox
```

As well as some dependencies to allow firefix to run in headless mode
```
sudo apt-get install libgtk-3-0 libdbus-glib-1-2 libx11-xcb1 libasound2 libatk1.0-0 libcairo2
```

# ToDo's

- [] Make the requests async to guarantee better performance
- [x] Check for SSL issues (and ignore them)
- [ ] Pretty output
- [x] Save all the data in a meaningful output such as a JSON 
- [x] Make automated screenshots using something like selenium
- [ ] Refactor Code
