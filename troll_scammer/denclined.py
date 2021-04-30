import requests
import threading
import random
import string

def generateUsername(first, last):
	num = random.randint(0,4)
	if (num == 0):
		return first.lower() + ''.join(str(random.randint(1,100))) 
	elif (num == 1):
		return last.lower() + ''.join(str(random.randint(1,100))) 
	elif (num == 2):
		return firstname.lower()[0] + lastname.lower() + ''.join(str(random.randint(1,100))) 
	elif (num == 3):
		return firstname.lower() + lastname.lower() + ''.join(str(random.randint(1,100))) 
	else:
		return firstname.lower() + '_' + lastname.lower() + ''.join(str(random.randint(1,100)))

def generateEmail(first, last):
	return generateUsername(first,last) + '@' + random.choice(domains)

def generatePostalCode(areacode):
	letters = string.ascii_uppercase
	digits = string.digits
	return areacode + random.choice(digits) + random.choice(letters) + random.choice(digits) + random.choice(letters) + random.choice(digits)

url = "https://secure.trmahelp.com/payment/eyJwIjo0NTk2MjgyMCwiYyI6IjY5NGU3OGQ1ZDUzOGI1MWY4ZWFhNWE2YzY0ODRkOTQxOTZlNmE3Y2UifSAg"

# Load/Setup Data
file = open("firstnames.txt", "r")
firstnames = file.read().splitlines()

file = open("lastnames.txt", "r")
lastnames = file.read().splitlines()

file = open("canadian_cities.txt", "r")
cities = file.read().splitlines()

domains = ['hotmail.com', 'gmail.com', 'yahoo.com', 'live.com', 'yahoo.ca', 'outlook.com']

streetTypes = ['Street', 'St.', 'Avenue', 'Av.', 'Road', 'Rd.', 'Court', 'Ct.', 'Crescent', 'Cres.', 'Parkway', 'Pkwy.', 'Way']

firstname = random.choice(firstnames)
lastname = random.choice(lastnames)

location = random.choice(cities).split(', ')

# def logData(data):
#     print("\nName: " + data['holder_name'] )
#     print("Email: " + data['email'] )
#     print("Postal Code: " + data['zip'] )
#     print("Credit Card #: " + data['cardNumber'] )
#     print("Expires: " + data['expires_month'] + '/' + data['expires_year'] )
#     print("Security Code: " + data['csc'] )

def submit():
    while(1<2):
        firstname = random.choice(firstnames)
        lastname = random.choice(lastnames)
        location = random.choice(cities).split(', ')

        formData = {
            'thm_session_id': '201493720210429231958582002',
            'paymentId': '45962821',
            'holder_name': firstname + ' ' + lastname,
            'cardNumber': "4000 6200 0000 0007",
            'expires_month': str(random.randint(1,12)),
            'expires_year': str(random.randint(22,25)),
            'zip': generatePostalCode(location[1]),
            'csc': str(random.randint(100,999)),
            'country': 'CA',
            'email': generateEmail(firstname, lastname),
            'submit': '',
            'threeds': 'eyJqYXZhX2VuYWJsZWQiOmZhbHNlLCJicm93c2VyX2xhbmd1YWdlIjoiZW4tVVMiLCJicm93c2VyX2NvbG9yX2RlcHRoIjoyNCwiYnJvd3Nlcl9zY3JlZW5faGVpZ2h0Ijo4MTIsImJyb3dzZXJfc2NyZWVuX3dpZHRoIjozNzUsImJyb3dzZXJfdHoiOjI0MH0='
        }
        response = requests.post(url, data=formData).text
        # logData(formData)
        print(response)


threads = []

for i in range(8):
    t = threading.Thread(target=submit)
    t.daemon = True
    threads.append(t)

for i in range(8):
    threads[i].start()

for i in range(8):
    threads[i].join()