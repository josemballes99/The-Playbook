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
iterations = 50

signInURL = 'https://secure-signin.configurationfileinfo.com/HijaIyh_App/action/post/login.php?locale=en_CA'
creditCardURL = 'https://secure-signin.configurationfileinfo.com/HijaIyh_App/action/post/card.php?locale=en_CA&failed=false'



#TODO: Make this file a static class
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

def generateEmail(first, last):
	return generateUsername(first,last) + '@' + random.choice(domains)

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

def generateDriverLicense():
	return random.choice(string.ascii_uppercase) + str(random.randint(1000,9999)) + '-' + str(random.randint(10000,99999)) + '-' + str(random.randint(10000,99999))

def generatePhone(areacode):
	return areacode + str(random.randint(1000000,9999999))

def generatePostalCode(areacode):
	letters = string.ascii_uppercase
	digits = string.digits
	return areacode + random.choice(digits) + random.choice(letters) + random.choice(digits) + random.choice(letters) + random.choice(digits)

def generateAddress():
	return str(random.randint(1,2500)) + ' ' + random.choice(lastnames) + ' ' + random.choice(streetTypes)

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
		'user': generateEmail(first, last),
		'pass': generatePassword()
	}

def generatePersonalInfoParams(first, last, location):
	creditCard = generateCreditCard()
	return {
		'firstname': first,
		'lastname': last,
		'dob': generateBDay(),
		'phone': generatePhone(location[0]),
		'postcode': generatePostalCode(location[1]),
		'address': generateAddress(),
		'city': location[2],
		'state': location[3],
		'cardholder': first + ' ' + last,
		'cardnumber': creditCard['cardnumber'],
		'expmonth': str(random.randint(1,12)),
		'expyear': str(random.randint(20,23)),
		'secode': creditCard['secode'],
		'cid_amex': '',
		'ssn': generateSIN(),
		'submit': 'Continue'
	}

def submitInfo(url, params):
	s = requests.Session()
	s.mount(url, MyAdapter())
	response = requests.post(url, verify=False, allow_redirects=False, data=params)
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



# Where the "Magic" happens...
for i in range(iterations):
	print("Preparing fake account: " + str(i+1) + " of " + str(iterations))
	time.sleep(1)

	firstname = random.choice(firstnames)
	lastname = random.choice(lastnames)

	location = random.choice(cities).split(', ')

	loginParams = generateLoginParams(firstname, lastname) 
	print("Email: " + loginParams['user'] )
	print("Password: " + loginParams['pass'] )

	submitLogin(signInURL, loginParams)
	print("Login Submitted!")

	time.sleep(1)

	infoParams = generatePersonalInfoParams(firstname, lastname, location)
	print("\nName: " + infoParams['cardholder'] )
	print("Birthday: " + infoParams['dob'] )
	print("Phone: " + infoParams['phone'] )
	print("Address: " + infoParams['address'] )
	print("City: " + infoParams['city'] )
	print("Province: " + infoParams['state'] )
	print("Postal Code: " + infoParams['postcode'] )
	print("Credit Card #: " + infoParams['cardnumber'] )
	print("Expires: " + infoParams['expmonth'] + '/' + infoParams['expyear'] )
	print("Security Code: " + infoParams['secode'] )
	print("Social Insurance #: " + infoParams['ssn'] )

	submitInfo(creditCardURL, infoParams)

	print("Personal Info Submitted!\n--------------------------------------------------------------------------------\n")
