from pwn import *

def passive(url):
	log.info("Trying to get WordPress Version")
	version = "4.2.3"
	if version:
		return ("version",version)
	else:
		return ("version",False)
    
def active(url):
	return passive(url)

