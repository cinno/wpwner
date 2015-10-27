class Convention(object):
	def __init__(self):

	# WordPress Installation
		# Holds the WordPress Version
		self.WP_Version = "Version"
		# List of WordPress Users
		self.WP_User = "User"
		# Dictionary formatted as {user:password}
		self.WP_Password = "Password"

	# Database Access
		# Database address (usually localhost)
		self.DB_Host = "DB_Host"
		# Database Name
		self.DB_Name = "DB_Name"
		# Database User
		self.DB_User = "DB_User"
		# Database Password
		self.DB_Password = "DB_Password"
		
	# Linux Environnement
		# Server Users with login shell enabled
		self.SSH_User = "SSH_User"
		# Dictionary of {ssh_user:ssh_password}
		self.SSH_Password = "SSH_Password"
		# Service Users (no login shell in /etc/passwd)
		self.Service_User = "Service_User"
		# Full Path
		self.Full_Path = "Full_Path"

	# Unmatched Credentials
		# List of user (in case of reused or unknown purpose)
		self.User = "U_User"
		# List of every passwords
		self.Password = "U_Password"

	# Misc
		# If your module uses other custom attributes, you are free
		# to add them here
