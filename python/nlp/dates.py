# import datetime
from datetime import datetime


def economic(date_str):
    dt_object = datetime.strptime(date_str, "%b %d, %Y, %I.%M %p IST")
    return(printDate(dt_object))


def moneyctl2(date_str):
    dt_object = datetime.strptime(date_str, "%b %d, %Y %I:%M %p IST")
    return(printDate(dt_object))


def moneyctl(date_str):
    dt_object = datetime.strptime(date_str, "%B %d, %Y %I:%M %p IST")
    return(printDate(dt_object))


def deccan(date_str):
    dt_object = datetime.strptime(date_str, "%b %d %Y, %H:%M ist")
    return(printDate(dt_object))


def economic2(date_str):
    dt_object = datetime.strptime(date_str, "%d %b, %Y")
    return(printDate(dt_object))


def firstpost(date_str):
    dt_object = datetime.strptime(date_str, "%b %d, %Y")
    return(printDate(dt_object))


def firstpost2(date_str):
    dt_object = datetime.strptime(date_str, "%b %d, %Y %H:%M:%S IST")
    return(printDate(dt_object))


def printDate(dt_object):
    timestamp = datetime.timestamp(dt_object)
    date_time = datetime.fromtimestamp(timestamp)
    d = date_time.strftime("%Y-%m-%d")
    D = date_time.strftime("%x %X")
    # return(d+","+D)
    sep = "\n-------\n"
    return(sep+d+sep+D)

    # economic("Mar 24, 2020, 04:37 PM IST")
moneyctl("March 24, 2020 02:28 PM IST")

# dt_string = "12/11/2018 09:15:32"
# dt_object1 = datetime.strptime(dt_string, "%d/%m/%Y %H:%M:%S")

# dt_string = "Mar 24, 2020, 04:37 PM IST"

# dt_object1 = datetime.strptime(dt_string, "%b %d, %Y, %H:%M %p IST")
# print("dt_object1:", dt_object1)
