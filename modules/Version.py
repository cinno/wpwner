from pwn import *
import urllib2

def passive(url):
	log.info("Trying to get WordPress Version")
	url+="readme.html"
	version = False
	html = ""
	try:
		response = urllib2.urlopen(url)
		html = response.read()
		html = html.split('\n')
	except:
		log.failure("Wasn't able to read "+url)
	for line in html:
		p = line.find('<br /> Version')
		if p != -1:
			versionLine = line.split('\x20')
			version = versionLine[len(versionLine)-1]
	return ("version",version)
    
def active(url):
	return passive(url)

