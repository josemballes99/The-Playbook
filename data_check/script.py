import requests, json

# Local
url = 'http://api.openweathermap.org/data/2.5/weather?q=Toronto&appid=APIKEY'
body = {
            'test': '',
            'test':''
        }

response = json.loads(requests.get(url).text)
js = json.dumps(response, indent=4)

file = open("Local/CallA.json", "w")
file.write(js)
file.close()

# QA
url = 'http://api.openweathermap.org/data/2.5/weather?q=Miami&appid=APIKEY'
body = {
            'test': '',
            'test':''
        }

response = json.loads(requests.get(url).text)
js = json.dumps(response, indent=4)

file = open("QA/CallA.json", "w")
file.write(js)
file.close()