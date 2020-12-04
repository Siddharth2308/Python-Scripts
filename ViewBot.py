from selenium import webdriver
import time
link = 'https://www.youtube.com/watch?v=Ho00ahnJ3TM'
views = int(input('Number of Views: '))
view_time = int(input('View Time: '))

browser = webdriver.Firefox()

for i in range(views):
    browser.get(link)
    time.sleep(view_time)

browser.close()