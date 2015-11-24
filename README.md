# WPwner
WPwner is a WordPress exploitation tool written in Python. It is really loud and usually doesn't check if a plugin version is vulnerable before trying to exploit it. It should be used as a last resort.

There's only 4 buggy modules for now. This is still a POC. If you want a real scanner, clone wpscan and leave me alone.

# Usage
```
$ ./WPwner.py --help
Usage: ./WPwner.py <options> -u url

Options:
  -h, --help  show this help message and exit
  -u URL      The target's URL
  -m METHOD   The method used -> active || passive
  -l          List modules and description
```
# How it works
WPwner works as a module launcher. Each module was written to exploit a specific vulnerability and implements two functions, `active` and `passive`. Both return a tupple list [(description,value)]

A behavior is considered *passive* when the module visits a page and parses it.

A behavior is considered *active* when the module uploads a shell or bruteforces access.

Once again, WPwner doesn't select which modules to used based on version recon. It activates *all* of them. This may change in the future, but right now, it's the module's job to decide if it should try exploitation
