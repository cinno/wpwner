#!/usr/bin/env python
from pwn import *
import sys
import optparse
from core.Target import Target
from core.Convention import Convention
import modules.info

def main():
	parser = optparse.OptionParser("Usage: "+sys.argv[0]+" <options> -u url")
	parser.add_option('-u',dest='url',type='string',help="The target's URL")
	parser.add_option('-m',dest='method', type='string', help="The method used -> active || passive")
	parser.add_option('-l',action="store_true",dest='listModules', help="List modules and description")
	(options, args) = parser.parse_args()
	if options.listModules:
		listModules()
		return 0
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

def listModules():
	for module_name in modules.info__all__:
		module = __import__ ("modules.info."+module_name, fromlist=[module_name])
		if hasattr(module,"description"):
			print '\n'
			d = module.description()
			print module_name+'\x20'*(20-len(module_name))+d
	return 0
class WPwner(object):
	def __init__(self,url,method):
		log.info('Preparing WPwner.......')
		self.c = Convention()
		self.target = Target(url)
		self.method = method
		log.info('Starting information gathering on '+self.target.url)
		if self.hostUp():
			self.info()
	def hostUp(self):
		# Verify host is online
		return True
	def info(self):
    		for module_name in modules.info.__all__:
			module = __import__ ("modules.info."+module_name, fromlist=[module_name])
        		if hasattr(module, self.method):
				(attribute,value) = ("",False)
				if self.method == "passive":
					tupList = module.passive(self.target)
				elif self.method == "active":
					tupList = module.active(self.target)
				for attribute,value in tupList:
					if value and attribute != self.c.Service_User:
						log.success("Adding '"+value+"' to target's "+attribute)
						if hasattr(self.target, attribute):
							orig = getattr(self.target,attribute)
							if value not in orig:
								orig.append(value)
								setattr(self.target,attribute,orig)
						else:
							setattr(self.target,attribute,[value])
			else:
				log.failure('Problem with Module '+module_name)
if __name__ == "__main__":
	main()
