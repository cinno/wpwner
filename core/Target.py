class Target(object):
	def __init__(self,url):
		self.url = self.sanitizeUrl(url)
	def sanitizeUrl(self,url):
		if "://" not in url: 
                        url = "http://"+url
                if url[len(url)-1] != "/":
                        url = url+"/"
		return url
