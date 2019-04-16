
import os
import urllib
import threads

def get_threads():
    thread_url = 'http://www.archboston.org/community/printthread.php?t='
    try:
        f = open('data7.txt', 'r')
        last_thread = int(f.readlines()[-1][2:6])
        f.close()
    except FileNotFoundError:
        f = open('data7.txt', 'w')
        f.close()
        last_thread = 999
    for num in range (last_thread+1, 5689):
        f = open('data7.txt', 'a')
        data = threads.get_data(str(num), thread_url + str(num))
        if not os.path.exists(str(num)):
            os.mkdir(str(num))
        if data:
            last = int(data[5])
            for page in range(1,last+1):
                if os.path.exists(str(num)+'/'+str(page)+'.html'):
                    g = open(str(num)+'/'+str(page)+'.html', 'r', encoding="utf-8")
                    print(page)
                    if len(str(g.readlines())) < 20:
                        g.close()
                        g = open(str(num)+'/'+str(page)+'.html', 'w', encoding="utf-8")
                        print(data[4] + r"&pp=20&page=" + str(page))
                        text = threads.get_contents(data[4] + r"&pp=20&page=" + str(page))
                        g.write(text)
                    else:
                        print(str(g.readlines()))
                    g.close()
                else:
                    g = open(str(num)+'/'+str(page)+'.html', 'w', encoding="utf-8")
                    print(data[4] + r"&pp=20&page=" + str(page))
                    text = threads.get_contents(data[4] + r"&pp=20&page=" + str(page))
                    g.write(text)
                    g.close()
        if data:
            f.write(str(data) + '\n')
        f.close()
                
if __name__ == '__main__':
    print(get_threads())
#    print(threads.get_contents("http://www.archboston.org/community/printthread.php?t=1008&page=12"))