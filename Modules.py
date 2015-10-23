'''
Folder Format
'''
"""
init.py 
"""
"""
Format.py 
"""

def Format():
    print "Format"


if __name__ == '__main__':
        Format()
        
'''
Folder Effect
'''
"""
init.py 
"""
"""
Effect.py 
"""

def Effect():
    print "Effect"

if __name__ == '__main__':
        Effect()      
        
from Sound.Format import Format
from Sound.Effect import *

def main():
    pass

if __name__ == '__main__':
    Format()
    Effect()        
