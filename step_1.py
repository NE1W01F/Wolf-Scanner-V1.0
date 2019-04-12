import urllib
import sqlite3
from multiprocessing import Process
import re
import sys

colur_red = '\033[31m'
colur_end = '\033[0m'
color_green = '\033[32m'

def findurl(text):
    if str(text).find("http") == 0:
        return True
    elif str(text).find("ftp") == 0:
        return True
    elif str(text).find("https") == 0:
        return True
    else:
        return False

def openurl(url):
    urls = []
    try:
        html = urllib.urlopen(url).read()
        getlinks = re.findall(r"""<\s*a\s*href=["']([^=]+)["']""", html)
        for link in getlinks:
            a = findurl(link)
            if a == True:
                urls.append(link)

        return urls
    except:
        print(colur_red + "[-] Error Loading {}".format(str(url)) + colur_end)
        return ''

exitvalue = 0

def main(site):
    print(color_green + "[+] Starting Scan on {}".format(site) + colur_end)
    links = openurl(site)
    while True:
        for url in links:
            print url
            if len(url) == 0:
                print(colur_red + "[-] No URLs Found" + colur_end)
                break
            else:
                print(color_green + "[+] Found URl and adding it to database" + colur_end)
                hostname = str(url).replace(':/', '').split('/')[1]
                db = sqlite3.connect('database.db')
                cursor = db.cursor()
                cursor.execute('''INSERT INTO data_1(urls, hostname)VALUES(?,?)''', (url, hostname))
                db.commit()
                db.close()
                for i in openurl(url):
                    links.append(i)

def meun(url):
    with open('art.txt', 'r') as art:
        print color_green + art.read() + colur_end
        print("\nEnter q and then press enter to scan {} and do the same again to stop scan".format(str(url)))
        if sys.stdin.read(1) != '':
            process = Process(target=main, args=(starturl,))
            process.start()
            while True:
                if sys.stdin.read(1) == 'q':
                    process.terminate()
                    break

command = sys.argv
length = len(command)
num = 0
if len(command) == 1:
    print('please use -u <url>')
else:
    for i in command:
        if i == "-u":
            num = num + 1
            starturl = command[num]
            meun(starturl)
        else:
            num = num + 1