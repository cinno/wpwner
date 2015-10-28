from pwn import *
from Convention import Convention
from Target import Target
import urllib2

def description():
	d = "Tries to access /wp-includes/rss-functions.php to disclose the full installation path"
	return d

def passive(target):
	url = target.url
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

def active(target):
	return passive(target)
