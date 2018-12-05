from utility import *

login()

with open("send_back_to_me.txt", "w") as f:
    f.write("stock: " + str(stock) + "\n")
    for i in range(-30, 30):
        f.write(str(stock + i) + " " + str(bkd(stock + i, 335050)) + "\n")

print("Now please copy the content of send_back_to.me.txt and send to me. 3Q :)")


