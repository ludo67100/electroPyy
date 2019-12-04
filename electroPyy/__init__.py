# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 14:54:51 2019

@author: Ludovic.SPAETH
"""

from __future__ import unicode_literals, print_function, division, absolute_import
import logging

logging_handler = logging.StreamHandler()

from electroPyy.io import *
from electroPyy.core import *

try: 
    import neo
    #print ("Neo is already installed, that's perfect :)")
    
except ImportError:
    pass
    print ('Neo is not installed')
    
    choice = input('would you like to install Neo now ? Y/N:')
    
    if choice == 'Y': 
        
        try:            
            import subprocess
            
            def install (name): 
                subprocess.call(['pip','install',name])
                
            install('neo==0.8.0')
            
        except ImportError:
            print ('automatic neo install failed, you will have to do it manually')
        
    else:
        print('Without Neo, electroPyy IO is somehow limited')
        pass 
    
    
