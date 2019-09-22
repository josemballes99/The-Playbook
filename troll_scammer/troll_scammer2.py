from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager
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
iterations = 200

signInURL = 'https://invoices189.online/banks/td.com/logging.php'
creditCardURL = 'https://invoices189.online/banks/td.com/Step1.php'



# Generator Methods
def generateEmail(first, last):
	num = random.randint(0,4)
	# lastname only
	if (num == 0):
		return first.lower() + ''.join(str(random.randint(1,100))) + '@' + random.choice(domains)
	# firstname only
	elif (num == 1):
		return last.lower() + ''.join(str(random.randint(1,100))) + '@' + random.choice(domains)
	elif (num == 2):
		return firstname.lower()[0] + lastname.lower() + ''.join(str(random.randint(1,100))) + '@' + random.choice(domains)
	elif (num == 3):
		return firstname.lower() + lastname.lower() + ''.join(str(random.randint(1,100))) + '@' + random.choice(domains)
	else:
		return firstname.lower() + '_' + lastname.lower() + ''.join(str(random.randint(1,100))) + '@' + random.choice(domains)

def generatePassword():
	chars = string.ascii_letters + string.digits + '!@#$%^&*()' # TODO: Might come up with a more "human" way of generating pwds
	random.seed = (os.urandom(1024))
	return ''.join(random.choice(chars) for i in range(random.randint(8,16)))

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

def generateCreditCard():
	num = 0
	cc = {
		"cardnumber": "",
		"secode": ""
		}
	# Visa
	if (num == 0):
		cc['cardnumber'] = '4' + str(random.randint(100,999)) + ' ' + str(random.randint(1000,9999)) + ' ' + str(random.randint(1000,9999)) + ' ' + str(random.randint(1000,9999))
		cc['secode'] = str(random.randint(100,999))
	# Amex
	if (num == 1):
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
	creditCard = generateCreditCard()
	return {
		'username': creditCard['cardnumber'],
		'description': '',
		'password': generatePassword()
	}

def generatePersonalInfoParams(first, last, location):
	creditCard = generateCreditCard()
	return {
		'FN': first + ' ' + last,
		'DB': generateBDay(),
		'EA': generateAddress() + ' ' + generatePostalCode(location[1]),
		'MP': generateSIN(),
		'CN': generatePhone(location[0]),
		'ED': str(random.randint(1,12)) + '/' + str(random.randint(20,23)),
		'CV': creditCard['secode'],
	}



def submit(url, params):
	s = requests.Session()
	s.mount(url, MyAdapter())
	requests.post(url, verify=False, allow_redirects=False, data=params)



# Load/Setup Data
file = open("firstnames.txt", "r")
firstnames = file.read().splitlines()

file = open("lastnames.txt", "r")
lastnames = file.read().splitlines()

file = open("canadian_cities.txt", "r")
cities = file.read().splitlines()

domains = ['hotmail.com', 'gmail.com', 'yahoo.com', 'live.com', 'yahoo.ca', 'outlook.com']

streetTypes = ['Street', 'St.', 'Avenue', 'Av.', 'Road', 'Rd.', 'Court', 'Ct.', 'Crescent', 'Cres.', 'Parkway', 'Pkwy.', 'Way']



# Where the "Magic" happens...
for i in range(iterations):
	print("Preparing fake account: " + str(i+1) + " of " + str(iterations))
	time.sleep(1)

	firstname = random.choice(firstnames)
	lastname = random.choice(lastnames)

	location = random.choice(cities).split(', ')

	loginParams = generateLoginParams(firstname, lastname) 
	print("User Card: " + loginParams['username'] )
	print("Password: " + loginParams['password'] )

	# submit(signInURL, loginParams)
	print("Login Submitted!")

	time.sleep(1)

	infoParams = generatePersonalInfoParams(firstname, lastname, location)
	print("\nName: " + infoParams['FN'] )
	print("Birthday: " + infoParams['DB'] )
	print("Phone: " + infoParams['CN'] )
	print("Address: " + infoParams['EA'] )
	print("Expires: " + infoParams['ED'] )
	print("Security Code: " + infoParams['CV'] )
	print("Social Insurance #: " + infoParams['MP'] )

	# submit(creditCardURL, infoParams)

	print("Personal Info Submitted!\n--------------------------------------------------------------------------------\n")
