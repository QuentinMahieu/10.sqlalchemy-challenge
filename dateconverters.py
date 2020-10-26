def converter(date):
    from datetime import datetime as dt
    date = date.replace('/','-')
    date = date.replace(" ","")
    try:
        date = dt.strptime(date, '%d-%m-%Y')
        date = dt.strftime(date,'%Y-%m-%d')
    except:
        pass
    try:
        date = dt.strptime(date, '%d-%m-%y')
        date = dt.strftime(date,'%Y-%m-%d')
    except:
        pass
    try:
        date = dt.strptime(date,'%Y-%m-%d')
        date = dt.strftime(date,'%Y-%m-%d')
    except:
        pass
    return date

def converter2(date):
    from datetime import datetime as dt
    date = date.replace('/','-')
    date = date.replace(" ","")
    try:
        date = dt.strptime(date, '%d-%m-%Y')
        date = dt.strftime(date,'%m-%d')
    except:
        pass
    try:
        date = dt.strptime(date, '%d-%m-%y')
        date = dt.strftime(date,'%m-%d')
    except:
        pass
    try:
        date = dt.strptime(date,'%m-%d')
        date = dt.strftime(date,'%m-%d')
    except:
        pass
    return date