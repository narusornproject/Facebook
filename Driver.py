from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import datetime
import pymongo


class Account:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def connect(self):
        driver = webdriver.Firefox(executable_path='D:/Project_Social (64 bit)/driver/geckodriver.exe')
        driver.get('https://www.facebook.com')
        driver.find_element_by_id('email').send_keys(self.username)
        driver.find_element_by_id('pass').send_keys(self.password + Keys.ENTER)
        time.sleep(10)
        return driver

    @staticmethod
    def geturl(driver, url):
        try:
            driver.get(url)
            time.sleep(20)
            return True
        except Exception as e:
            print('Error!' + str(e))
            text_file = open("LogError.txt", "a+")
            text_file.write(str(url) + ' :  ' + str(datetime.datetime.now()) + ' ' + str(e))
            text_file.close()
            # html = driver.page_source
            # response = Selector(text=html).xpath('//*[@id="globalContainer"]').css('h2::text').extract_first()
            return False

    def getaccount(self):
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client['account']
        col = db['facebook']
        scl = col.find({'status': 0}).limit(1)
        self.username = scl[0]['username']
        self.password = scl[0]['password']
        col.find_one_and_update({'username': scl[0]['username']}, {'$set': {'status': 1}})
        client.close()

    def updateaccount(self):
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client['account']
        col = db['facebook']
        col.find_one_and_update({'username': self.username}, {'$set': {'status': 2}})
