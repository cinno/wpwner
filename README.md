# WPwner
WPwner is a WordPress exploitation tool written in Python. It is really loud and usually doesn't check if a plugin version is vulnerable before trying to exploit it. It should be used as a last resort.

There's only 4 buggy modules for now. This is still a POC. If you want a real scanner, clone wpscan and leave me alone.

# Method
WPwner works as a module launcher. Each module was written to exploit a specific vulnerability and implements two functions, `active` and `passive`. Both return a tupple list [(description,value)]

A behavior is considered *passive* when the module visits a page and parses it.

A behavior is considered *active* when the module uploads a shell or bruteforces access.
