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
		self.method = method
		log.info('Starting attack on '+self.target.url)
		if self.hostUp():
			self.attack()
	def hostUp(self):
		# Verify host is online
		return True
	def attack(self):
    		for module_name in modules.__all__:
			module = __import__ ("modules."+module_name, fromlist=[module_name])
        		if hasattr(module, self.method):
				(attribute,value) = ("",False)
				if self.method == "passive":
					tupList = module.passive(self.target.url)
				elif self.method == "active":
					tupList = module.active(self.target.url)
				for attribute,value in tupList:
					if value:
						log.info("Adding "+value+" to target's "+attribute)
						if hasattr(self.target, attribute):
							orig = getattr(self.target,attribute)
							orig.append(value)
							setattr(self.target,attribute,orig)
						else:
							setattr(self.target,attribute,[value])
			else:
				log.failure('Problem with Module '+module_name)
if __name__ == "__main__":
	main()
