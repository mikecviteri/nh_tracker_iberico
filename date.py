import random
import time
from datetime import datetime


def str_time_prop(start, end, time_format, prop):
    """Get a time at a proportion of a range of two formatted times.

    start and end should be strings specifying times formatted in the
    given format (strftime-style), giving an interval [start, end].
    prop specifies how a proportion of the interval to be taken after
    start.  The returned time will be in the specified format.
    """

    stime = time.mktime(time.strptime(start, time_format))
    etime = time.mktime(time.strptime(end, time_format))

    ptime = stime + prop * (etime - stime)

    return time.strftime(time_format, time.localtime(ptime))


def random_date(day):
    year = time.strftime("%y", time.localtime())
    month = datetime.now().month

    clock = f"{day}/{month}/{year}"
    return str_time_prop(f"{clock} 12:00:00 AM", f"{clock} 11:59:59 PM", '%d/%m/%y %I:%M:%S %p', random.random())


def day_checker():
    while True:
        try:
            day = int(input("Ingresa el día de delivery"))
            if type(day) == int:
                try:
                    random_date(day)
                    break
                except ValueError:
                    print(f"{day} no es un día válido para este mes")
        except ValueError:
            print("No es un número")
            continue
    return day
