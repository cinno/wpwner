#!/usr/bin/env python
from pwn import *
import sys
import optparse
from Target import Target
#from modules import *
import modules

def main():
	parser = optparse.OptionParser("Usage: "+sys.argv[0]+" <options> -u url")
	parser.add_option('-u',dest='url',type='string',help="The target's URL")
	parser.add_option('-m',dest='method', type='string', help="The method used -> active || passive")
	(options, args) = parser.parse_args()
	if options.url:
		domain = options.url
		if options.method:
			if options.method != "passive" and options.method != "active":
				print parser.usage
				return 0
			else:
				method = options.method
		else:
			method = "passive"	
		pwner = WPwner(domain,method)
	else:
		print parser.usage
	return 0

class WPwner(object):
	def __init__(self,url,method):
		log.info('WPwner')
		self.target = Target(url)
		log.info('Starting attack on '+self.target.url)
		self.passiveAttack()
	def passiveAttack(self):
    		for module_name in modules.__all__:
			module = __import__ ("modules."+module_name, fromlist=[module_name])
        		if hasattr(module, 'passive'):
				module.passive(self.target.url)
			else:
				print module_name+" no passive"
if __name__ == "__main__":
	main()
