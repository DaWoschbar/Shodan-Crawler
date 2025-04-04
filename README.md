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


# ToDo's

- [x] Make the requests async to guarantee better performance
- [ ] Check for SSL issues (and ignore them)
- [ ] Pretty output
- [ ] Save all the data in a meaningful output such as a JSON 
- [x] Make automated screenshots using something like selenium
- [ ] Refactor Code