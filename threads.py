

import urllib
from bs4 import BeautifulSoup

def get_contents(url):
    fp = urllib.request.urlopen(url)
    mybytes = fp.read()
    
    mystr = mybytes.decode("latin_1")
    fp.close()
    
    return mystr

def get_thread_num(url):
    return url.rsplit('=', 1)[1]

def get_title(contents):
    name = str(contents.title.string)
    title = name.split('-', 1)[1][2:]
    return title

def get_forum(contents):
    pos = contents.body.find_all('div')
    for x in pos:
        if x.contents:
            if x.contents[0] == '\r\n\t- \xa0 ':
                return x.a.strong.contents[0]

def get_start_time(contents):
    pos = contents.body.find_all('td')
    for x in pos:
        if x.contents:
            if str(x.contents[0])[-1] == 'M':
                return x.contents[0]

def get_last_page(contents):
    pos = contents.body.find_all('td')
    for x in pos:
        if x.tr:
            if x.tr.td:
                if x.tr.td.contents:
                    if str(x.tr.td.contents[0]).startswith("Page"):
                        return x.tr.td.contents[0].rsplit('of ', 1)[1]
    return "1"

def get_last_url(url, last_page):
    return url + r"&pp=20&page=" + last_page
    
def get_last_time(contents):
    pos = contents.body.find_all('td')
    time = None
    for x in pos:
        if x.contents:
            if str(x.contents[0])[-1] == 'AM' or str(x.contents[0])[-1] == 'PM':
                time = x.contents[0]
    return time

def get_data(num, url):
    data = (num,)
    contents = get_contents(url)
    contents = BeautifulSoup(contents)
    try:
        data += (get_title(contents),)
    except:
        return None
    print(data)
    data += (get_forum(contents),)
    data += (get_start_time(contents),)
    data += (url,)
    last_page = get_last_page(contents)
    data += (last_page,)
    if int(last_page) > 1:
        last_url = get_last_url(url, last_page)
        last_contents = get_contents(last_url)
        last_contents = BeautifulSoup(last_contents)
    else:
        last_url = url
        last_contents = contents
    data += (get_last_time(last_contents),)
    data += (last_url,) 
    # (#, forum, start time, url, page count, last pst time, last page url)
    return data

def get_all_data():
    thread_url = 'http://www.archboston.org/community/printthread.php?t='
    f = open('data.txt', 'r')
    last_thread = int(f.readlines()[-1][2:6])
    f.close()
    for num in range (last_thread+1, 5681):
        f = open('data.txt', 'a')
        data = get_data(str(num), thread_url + str(num))
        if data:
            f.write(str(data) + '\n')
        f.close()
                
if __name__ == '__main__':
    print(get_all_data())
#    print(get_data('1000', 'http://www.archboston.org/community/printthread.php?t=1189'))