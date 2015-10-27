from pwn import *
import urllib2
from Convention import *

def passive(url):
	log.info("Trying to get WordPress Version")
	c = Convention()
	url+="readme.html"
	version = False
	html = ""
	try:
		response = urllib2.urlopen(url)
		html = response.read()
		html = html.split('\n')
	except:
		pass
	for line in html:
		p = line.find('<br /> Version')
		if p != -1:
			versionLine = line.split('\x20')
			version = versionLine[len(versionLine)-1]
	if not version:
		log.failure("Wasn't able to read "+url)
	return [(c.WP_Version,version)]
    
def active(url):
	return passive(url)

