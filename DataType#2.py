def MyFunc(n):
    return lambda(n):n*n

List=(1,2,3,4,5)
for i in range(0,3):
    print MyFunc(i)

x= MyFunc(2)
print x(-4)
