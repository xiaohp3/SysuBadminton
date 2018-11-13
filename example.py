from autobadminton import *

Login()

while True:
    s = input("Intput time and number of court: ")
    s = s.split()
    time = int(s[0])
    court = int(s[1])
    if len(s) == 2:
        res = Book(time, court)
        print(res)
    else:
        print("Invalid")
