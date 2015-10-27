from pwn import *
from Convention import Convention
import urllib2

def passive(url):
	c = Convention()
	retValue = []
	url += "/wp-includes/rss-functions.php"
	html = ""
	try:
		response = urllib2.urlopen(url)
		html = response.read()
		log.info('May have found Full Path Disclosure')
		html = html.split('\n')
		for line in html:
			if line.find('() in <b>') != -1:
				beg = line.find('() in <b>')+9
				end = line.find("wp-includes")
				retValue.append((c.Full_Path,line[beg:end]))
	except:
		pass
	if len(retValue) == 0:
		retValue = [('none',False)]
	return retValue

def active(url):
	return passive(url)
