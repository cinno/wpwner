#!/usr/bin/env python
import pwn
import sys
from Target import Target
from modules import *

def main():
	target = Target(domain)
	return 0

def help():
	print "You are doing it wrong"
if __name__ == "__main__":
	if len(sys.argv) < 2:
		help()
	else:
		domain = sys.argv[0]
		main()
