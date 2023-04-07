import datetime
def getday(day: int, start_day=datetime.datetime.today()):
    days_to_go = (day - start_day.weekday() + 7) % 7
    next_date = start_day + datetime.timedelta(days=days_to_go)

    while next_date.month != start_day.month:
        next_date = next_date.replace(day=1)
        next_date += datetime.timedelta(days=7 - next_date.weekday() + day)

    return next_date
