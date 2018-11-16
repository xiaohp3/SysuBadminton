from utility import *

def ok(s):
    return s != "ERROR"

login()

resetDate(2018, 11, 19)

for court in range(2, 11):
    for time in range(19, 21):
        print(check(time, court))

for court in range(2, 11):
    res1 = check(19, court)
    res2 = check(20, court)
    if ok(res1) and ok(res2):
        print(book(19, court))
        print(book(20, court))
        break

# 执行结束后，在体育场馆管理与预订系统
# 的“我的订单”中就可以看到，某个场的
# 连续的两个小时已经被预订，状态显示着
# “未支付”，只需点进订单里支付即可。
