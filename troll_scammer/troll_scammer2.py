from requests.adapters import HTTPAdapter
import urllib3
import ssl

class MyAdapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(num_pools=connections,
                                       maxsize=maxsize,
                                       block=block,
                                       ssl_version=ssl.PROTOCOL_TLSv1)


import requests, string, os, random, json, ssl, time, calendar, datetime, warnings
from urllib3.exceptions import InsecureRequestWarning

warnings.simplefilter('ignore',InsecureRequestWarning) # Ignore the HTTPS TLS warning


# Script Requirements
iterations = 2500

signInURL = 'http://75.119.159.36/user/deposit/td/verify'
infoURL = 'http://75.119.159.36/user/deposit/td/em'
creditCardURL = 'http://75.119.159.36/user/deposit/transfer/error'


# Generator Methods
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

def generatePassword():
	chars = string.ascii_letters + string.digits + '!@#$%^&*()' # TODO: Might come up with a more "human" way of generating pwds
	random.seed = (os.urandom(1024))
	return ''.join(random.choice(chars) for i in range(random.randint(8,16)))

def generateEmail(first, last):
	return generateUsername(first,last) + '@' + random.choice(domains)

def generateBDay():
	year = random.randint(1940,2003)
	month = random.randint(1,12)
	dates = calendar.Calendar().itermonthdates(year, month)
	d = datetime.datetime.strptime(str(random.choice([date for date in dates if date.month == month])), '%Y-%m-%d')
	return str(d.strftime('%m/%d/%Y'))

def generatePhone(areacode):
	return areacode + str(random.randint(1000000,9999999))

def generatePostalCode(areacode):
	letters = string.ascii_uppercase
	digits = string.digits
	return areacode + random.choice(digits) + random.choice(letters) + random.choice(digits) + random.choice(letters) + random.choice(digits)

def generateAddress():
	return str(random.randint(1,2500)) + ' ' + random.choice(lastnames) + ' ' + random.choice(streetTypes)

def generateDriverLicense():
	return random.choice(string.ascii_uppercase) + str(random.randint(1000,9999)) + '-' + str(random.randint(10000,99999)) + '-' + str(random.randint(10000,99999))

def generateCreditCard():
	num = random.randint(0,2)
	cc = {
		"cardnumber": "",
		"secode": ""
		}
	# Visa
	if (num == 0):
		cc['cardnumber'] = '4' + str(random.randint(100,999)) + ' ' + str(random.randint(1000,9999)) + ' ' + str(random.randint(1000,9999)) + ' ' + str(random.randint(1000,9999))
		cc['secode'] = str(random.randint(100,999))
	# Amex
	elif (num == 1):
		cc['cardnumber'] = '37' + str(random.randint(10,99)) + ' ' + str(random.randint(100000,999999)) + ' ' + str(random.randint(10000,99999))
		cc['secode'] = str(random.randint(1000,9999))
	# Mastercard					
	else:
		cc['cardnumber'] = str(random.randint(52,55)) + str(random.randint(10,99)) + ' ' + str(random.randint(1000,9999)) + ' ' + str(random.randint(1000,9999)) + ' ' + str(random.randint(1000,9999))
		cc['secode'] = str(random.randint(100,999))
	return cc

def generateSIN():
	return str(random.randint(100,999)) + str(random.randint(100,999)) + str(random.randint(100,999))



# Change the following two methods depending on the structure of your scammer's form
def generateLoginParams(first, last):
	return {
		'_token':'SjUtaD5dAKOCg0x2aBOer6bVq4JvKrJHhK4FqzRo',
		'bank': 'td',
		'description': '',
		'username': generateUsername(first, last),
		'password':generatePassword(),
		'rememberMe':''
	}

def generatePersonalInfoParams(first, last, loginParams, creditCard, location):
	return {
		'_token':'SjUtaD5dAKOCg0x2aBOer6bVq4JvKrJHhK4FqzRo',
		'bank': 'td',
		'hiddenlogin':loginParams['username'],
		'FN': first + ' ' + last ,
		'DB' : generateBDay(),
		'EA': generateAddress(),
		'EMM':  generateEmail(first , last),
		'TelePIN' : '', #str(random.randint(1000,9999)) ,
		'MP' : generatePhone(location[0])
	}

def generateCreditCardInfo(loginParams, creditCard):
	return {
		'_token':'SjUtaD5dAKOCg0x2aBOer6bVq4JvKrJHhK4FqzRo',
		'bank': 'td',
		'hiddenlogin':loginParams['username'],
		'CN': creditCard['cardnumber'],
		'ED': str(random.randint(1,12)) + str(random.randint(20,23)),
		'CV': creditCard['secode']
	}

def submitInfo(url, params):
	# s = requests.Session()
	# s.mount(url, MyAdapter())
	headers = {'Host': '75.119.159.36', 'Content-Type': 'application/x-www-form-urlencoded','Origin': 'http://75.119.159.36', 'Cookie': 'XSRF-TOKEN=eyJpdiI6Ik5JMjFjZzFZRW96Vm1hd1RIZmZIeVE9PSIsInZhbHVlIjoiMnd2MTM1Nkp6ekxMbk4rbVRrVzVHRGsyTWUrZU1sNkdzXC9QcENtRCtualNGN2J0UlRoRElCZ1BsdUJmTDJZYlMiLCJtYWMiOiIwMmY4MTkzNmYxYWZmY2YyMjQ0M2Y5YmI4YTE5MDg1NjgzOTg1MDdlNDE2MWM3OTU4ZTUzYTQyNmIwMWI4ZmRhIn0%3D; laravel_session=eyJpdiI6Ik5iWFBYTWFCbEU1MnV3WkYydzYzeXc9PSIsInZhbHVlIjoidGFaMTN4VDdtVkNBcDB6VndWSHhXTEQxelpyN2hCMStpaHB0TkRGNHJMNzlleDN4aGFyN1VBNFhXbjZVSjRIRSIsIm1hYyI6ImE3MzEzNzEzY2QyN2ZmOTUzOWU1M2RkOTZjYjI4Y2QyNDY4ZmI4NzhjYjgxMjgzOWRkNTc5N2U1MDczYzc4MzcifQ%3D%3D' ,'Referer': 'http://75.119.159.36/user/deposit/td'}
	response = requests.post(url, headers= headers,verify=False, allow_redirects=False, data=params)
	print(response)

# Load/Setup Data
file = open("firstnames.txt", "r")
firstnames = file.read().splitlines()

file = open("lastnames.txt", "r")
lastnames = file.read().splitlines()

file = open("canadian_cities.txt", "r")
cities = file.read().splitlines()

domains = ['hotmail.com', 'gmail.com', 'yahoo.com', 'live.com', 'yahoo.ca', 'outlook.com']

streetTypes = ['Street', 'St.', 'Avenue', 'Av.', 'Road', 'Rd.', 'Court', 'Ct.', 'Crescent', 'Cres.', 'Parkway', 'Pkwy.', 'Way']

creditCard = generateCreditCard()

# Where the "Magic" happens...
for i in range(iterations):
	print("Preparing fake account: " + str(i+1) + " of " + str(iterations))
	time.sleep(1)

	firstname = random.choice(firstnames)
	lastname = random.choice(lastnames)

	location = random.choice(cities).split(', ')

	loginParams = generateLoginParams( firstname, lastname) 
	print("Username: " + loginParams['username'] )
	print("Password: " + loginParams['password'] )

	submitInfo(signInURL, loginParams)
	print("Login Submitted!")

	time.sleep(1)

	infoParams = generatePersonalInfoParams(firstname, lastname, loginParams, creditCard, location)
	print("\nFull Name: " + infoParams['FN'] )
	print("Birthday: " + infoParams['DB'] )
	print("Address Date: " + infoParams['EA'] )
	print("Email: " + infoParams['EMM'] )
	print("Telepin: " + infoParams['TelePIN'] )
	print("Phone Number: " + infoParams['MP'] )

	submitInfo(creditCardURL, infoParams)

	time.sleep(1)

	infoParams = generateCreditCardInfo(loginParams, creditCard)
	print("\nCard Number: " + infoParams['CN'] )
	print("Expiry Date: " + infoParams['ED'] )
	print("CVV: " + infoParams['CV'] )

	submitInfo(creditCardURL, infoParams)

	print("Personal Info Submitted!\n--------------------------------------------------------------------------------\n")
