Function1

class Function1:
    value1=100

    def function1(self):
        print "Function1"
        value =5
        print value
        global List1
        List1= [1,2,4,5,6]
        print List1

if __name__ =="__main__":
    #Function1()
    print Function1.value1
    x= Function1().function1()
    #print x.value
    #print x.List1
    #print Function1.function1().List1

Function2
class Function2:
    value2=15

    def function2(self,value):
        print "Function2"
        print value


if __name__ =="__main__":
    #Function2()
    print Function2.value2
    f2= Function2().function2(10)
    print type(f2)
    print f2

Function3

class Function3:
    value3=150

    def function3(self,value):
        print "Function3"
        print value

    def function32(self):
        print "Function32"

if __name__ =="__main__":
    #Function2()
    print Function3.value3
    f3= Function3().function3(10)
    f31=Function3().function32()


Main
from Function1 import Function1
from Function2 import Function2
from Function3 import *

def Start():
    #print Function1.List1
    x= Function1().function1()
    y= Function2().function2(10)
    '''
    print y.value2
    print y.value
    '''
    #print x.value1
    #print x.function1.value
    #print x.function1.List1
    z1= Function3().function3(100)
    z2= Function3()
    print z2.value3
    z2= Function3().function32()

if __name__ =="__main__":
    Start()
