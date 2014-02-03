# -*- coding: utf-8 -*-
"""""
Logging Modul zum einfachen Loggen auf Stdout.

"""
import logging
import sys
    
root = logging.getLogger()
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
formatter = logging.Formatter('%(message)s')
ch.setFormatter(formatter)
root.addHandler(ch)
root.setLevel(logging.DEBUG)
  

def log(msg):
    """Gibt msg auf Konsole aus, sind keine Ausgaben erwuenscht pass einkommentieren"""
#     pass
    root.info(msg)

if __name__ == '__main__':
    log('glgls')