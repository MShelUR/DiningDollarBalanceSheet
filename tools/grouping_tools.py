
def by_categories(expenses):
    categories = {}

    for item in expenses:
        timestamp, place, amount = item
        if not categories.get(place):
            categories[place] = 0
        categories[place] += amount

    for cat in categories:
        categories[cat] = round(categories[cat],2)

    return categories, [('service','d$')]+[(key, categories[key]) for key in sorted(categories)]

def by_time_of_day(expenses,hour_interval=1):
    times = {}
    
    for interval in range(0,int(24/hour_interval)+1,1):
        times[interval*hour_interval] = 0

    for item in expenses:
        timestamp, place, amount = item
        date, time = timestamp.split()
        h, m, s = time.split(":")
        used_time = round(round((float(h)+int(m)/60)/hour_interval))*hour_interval
        

        if amount > 0:
            times[used_time] += amount

    for time in times:
        times[time] = round(times[time],0)

    print(times)
    return times, [('time','d$')]+[(key, times[key]) for key in sorted(times)]

def find_income(expenses):
    funds = 0
    
    for item in expenses:
        timestamp, place, amount = item
        if amount < 0: # negative amount means income
            funds -= amount # flip sign for total funds

    return funds