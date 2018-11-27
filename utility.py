import time
from autobadminton import login, bkd, ckd
import autobadminton
import code

# pre-defined parameters
weekday_map = [-1 for i in range(30)]
for i in range(4):
    weekday_map[18 + i] = i
weekday_map = tuple(weekday_map)

weekend_map = [-1 for i in range(30)]
for i in range(3):
    weekend_map[9 + i] = i
for i in range(8):
    weekend_map[14 + i] = 3 + i
weekend_map = tuple(weekend_map)

seconds_in_day = 86400
first_sdid = 0
is_weekday = False

def isWeekday(y = 0, m = 0, d = 0):
    if y == 0 and m == 0 and d == 0:
        t = time.localtime()
        return t.tm_wday < 5
    t = (y, m, d, 0, 0, 0, 0, 0, 0)
    secs = time.mktime(t)
    t = time.localtime(secs)
    return t.tm_wday < 5


def date2stamp(y = 0, m = 0, d = 0):
    if y == 0 and m == 0 and d == 0:
        t = time.time()
        return int(t)
    t = (y, m, d, 0, 0, 0, 0, 0, 0)
    stmp = time.mktime(t)
    return int(stmp)

# pre-defined parameters
std_weekday_stamp = date2stamp(2018, 11, 12)
std_weekday_sdid  = 334210
std_weekday_stock = 44270
std_weekend_stamp = date2stamp(2018, 11, 17)
std_weekend_sdid  = 348250
std_weekend_stock = 45206

def countWeekdays(y, m, d):
    t = (y, m, d, 0, 0, 0, 0, 0, 0)
    stmp = time.mktime(t)
    days = (stmp - std_weekday_stamp) / seconds_in_day
    days = round(days)
    quo = days // 7
    rem = days % 7
    if rem < 4:
        return quo * 5 + rem
    else:
        return quo * 5 + 4

def countWeekends(y, m, d):
    t = (y, m, d, 0, 0, 0, 0, 0, 0)
    stmp = time.mktime(t)
    days = (stmp - std_weekend_stamp) / seconds_in_day
    days = round(days)
    quo = days // 7
    rem = days % 7
    if rem == 0:
        return quo * 2
    else:
        return quo * 2 + 1


stock = 44270
t = time.localtime(int(time.time()))
y = t.tm_year
m = t.tm_mon
d = t.tm_mday
t = (y, m, d, 0, 0, 0, 0, 0, 0)
stmp = time.mktime(t)
stmp += seconds_in_day
t = time.localtime(stmp)
if isWeekday(t.tm_year, t.tm_mon, t.tm_mday):
    stock = std_weekday_stock + countWeekdays(t.tm_year, t.tm_mon, t.tm_mday) * 4
else:
    stock = std_weekend_stock + countWeekends(t.tm_year, t.tm_mon, t.tm_mday) * 11


def resetDate(y, m = -1, d = -1):
    global first_sdid
    global is_weekday
    if m == -1 and d == -1:
        ima = int(time.time())
        t = time.localtime(ima + seconds_in_day * y)
        y = t.tm_year
        m = t.tm_mon
        d = t.tm_mday

    if isWeekday(y, m, d):
        days = countWeekdays(y, m, d)
        first_sdid = std_weekday_sdid + days * 60
        is_weekday = True
    else:
        days = countWeekends(y, m, d)
        first_sdid = std_weekend_sdid + days * 165
        is_weekday = False

def getDetail(time, court):
    if court < 1 or court > 15:
        return -1
    if time < 0 or time >= 24:
        return -1
    if is_weekday:
        if weekday_map[time] == -1:
            return -1
        return first_sdid + weekday_map[time] * autobadminton.nCourts + court - 1
    else:
        if weekend_map[time] == -1:
            return -1
        return first_sdid + weekend_map[time] * autobadminton.nCourts + court - 1

def check(time, court):
    detail = getDetail(time, court)
    if detail == -1:
        return "Invalid parameters"
    return ckd(stock, detail)

def book(time, court):
    detail = getDetail(time, court)
    if detail == -1:
        return "Invalid parameters"
    return bkd(stock, detail)

def lst(start, end = -1):
    if end == -1:
        end = start + 1
    
    mp = ()
    if is_weekday:
        mp = weekday_map
    else:
        mp = weekend_map
    if start >= end:
        print("Invalid parameters")
        return

    for i in range(autobadminton.nCourts):
        print("\t" + str(i + 1), end = "")
    print("")
    for time in range(start, end):
        if mp[time] == -1:
            continue
        print(str(time), end = "")
        for court in range(1, autobadminton.nCourts + 1):
            print("\t", end = "")
            if check(time, court) != "ERROR":
                print("o", end = "")
        print("")


resetDate(2)

if __name__ == '__main__':
    interp = code.InteractiveConsole(globals())
    interp.interact("Enter interactive mode.")
