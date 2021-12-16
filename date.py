import random
import time
from datetime import datetime


def str_time_prop(start, end, time_format, prop):
    stime = time.mktime(time.strptime(start, time_format))
    etime = time.mktime(time.strptime(end, time_format))

    ptime = stime + prop * (etime - stime)

    return time.strftime(time_format, time.localtime(ptime))


def random_date(day):
    year = time.strftime("%Y", time.localtime())
    month = datetime.now().month

    clock = f"{year}-{month}-{day}"
    return str_time_prop(f"{clock} 00:00:00", f"{clock} 23:59:59", '%Y-%m-%d %H:%M:%S', random.random())


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
