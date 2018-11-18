# **Quick start for court booking script in SYSU (East)**

## What can it do?

- Use python to book badminton courts in your own logic
- Book the courts which are not shown in your browser

## Required third-party libraries

- beautifulsoup4
- requests

## Quick start

The last 2 items in config.json are the NetID and password in SYSU.

The login captcha is saved as a picture, which is in the same path as the script.

function check(time, court) checks the info of a court. The return value is a string, indicating the court info. It can also be the string "Error". In this case, it means that your given court has already been booked. (Yes you're right, the booked courts cannot be checked). Of course, it also probably means the existence of bugs. Please open a issue, thank you :)

book(time, court) is used to book a court. Its return value is a string. If the string is "未支付", then you have booked a court successfully. What you should do next is to use your browser to view the order page and pay the money.

resetDate(y, m, d) can reset the date on which you want to book a court to the given date. The initial date is the day after tomorrow. If only one parameter is used, say resetDate(x), then it means reset the date to x days later.

lst(start_time, end_time) will print a table on the console. The content is: in the time range [start_time, end_time), which court is available at which time.

The module autobadminton deals with the server, and the module utility provides many convenient functions for programmers. Like example.py, programmers can first import utility in their .py source files and then write codes. Programmers can also run utility.py directly to enter interactive mode.

## Examples

![test-0](images/test-1.png)

![test-1](images/test-3.png)

<br/>

Many bugs still exist.
