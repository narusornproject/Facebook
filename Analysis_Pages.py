import time
import pymongo
from scrapy.selector import Selector
import Driver
import math


database = 'members_1503827623035837'


class Page:
    def __init__(self, average, freq, reviews, info, av_like, verify, reply, size):
        self.average = average
        self.freq = freq
        self.reviews = reviews
        self.info = info
        self.like = av_like
        self.verify = verify
        self.reply = reply
        self.size = size
        self.listname = []

    @staticmethod
    def conPage(base):
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client[base]
        col = db['Pages']
        return col

    @staticmethod
    def geturl(url):
        urlpage = ''
        for y in url:
            if y == '?':
                break
            urlpage += y
        return urlpage

    @staticmethod
    def createlist(listitem):
        item = {}
        for key, value in listitem.items():
            # print(value)
            item.update({key: value})
        return item

    # like follow
    def getlike(self, source):
        info = {}
        countlike = '0'
        scl = Selector(text=source).xpath('//*[@id="pages_side_column"]').css('div::text').extract()
        # print(scl)
        for y in scl:
            item = y.split(' ')
            if len(item) == 2:
                try:
                    if item[1] == 'คนถูกใจสิ่งนี้':
                        info.update({item[1]: str(item[0]).replace(',', '')})
                        countlike = item[0]
                    if item[1] == 'คนติดตามเพจนี้':
                        info.update({item[1]: item[0]})
                except:
                    return ''
                    pass
        info = Page.createlist(info)
        self.info = info
        return countlike

    def getsize(self):
        if int(self.info['คนถูกใจสิ่งนี้']) < 10000:
            self.size = 's'
        if (int(self.info['คนถูกใจสิ่งนี้']) < 100000) and (int(self.info['คนถูกใจสิ่งนี้']) >= 10000):
            self.size = 'm'
        if (int(self.info['คนถูกใจสิ่งนี้']) < 1000000) and (int(self.info['คนถูกใจสิ่งนี้']) >= 100000):
            self.size = 'l'
        if int(self.info['คนถูกใจสิ่งนี้']) > 1000000:
            self.size = 'xl'

    # ans
    def getpostlike(self, source, result):

        scl = Selector(text=source).xpath('//*[@id="pagelet_timeline_main_column"]').css("a::attr(aria-label)").extract()
        # print(scl)
        totallike = 0
        countlike = 0
        for y in scl:
            item = y.split(' ')
            try:
                if item[0] == 'ถูกใจ':
                    countlike += 1
                    totallike += int(item[1])
            except:
                pass
        # print('เฉลี่ยคนที่ถูกใจต่อ Post: '+str(totallike/countlike))
        result = result.replace(",", "")
        try:
            average = (totallike / countlike) / float(result)
        except:
            average = 0
        # print('ค่าเฉลี่ยของการกดไลค์ต่อจำนวนคน: ' + str(anslike))
        try:
            self.like = round((totallike / countlike), 10)
        except:
            self.like = 0
        self.average = average
        return average

    # frq
    def activity(self, source):
        frq = 0
        lasted = 30
        scl = Selector(text=source).xpath('//*[@id="pagelet_timeline_main_column"]').css(
            'abbr::attr(data-utime)').extract()
        for y in scl:
            try:
                date = time.time() - float(y)
                datetime = math.ceil((float(date) / 86400))
                if datetime <= 7:
                    frq += 1
                if datetime < lasted:
                    lasted = datetime
                # print(x['ชื่อเพจ'] + '  โพสต์ล่าสุด: ' + str(datetime))
            except:
                pass
                # print(x['ชื่อเพจ'] + '  โพสต์ล่าสุด: ไม่ทราบ')
        if lasted >= 7:
            self.freq = 0
            # print('Dont Active')
        else:
            self.freq = frq
            # print('โพสต์ล่าสุด: ' + str(lasted))

    def getreviews(self, source):
        review = 0
        num = Selector(text=source).xpath('//*[@id="content_container"]').css('div::text').extract_first()
        try:
            review = float(num)
        except:
            pass
        self.reviews = review

    def getuseractivity(self, source, driver):
        itemurl = []
        scl = Selector(text=source).xpath('//*[@id="pagelet_timeline_main_column"]').css('a')
        for li in scl.css('a::attr(href)').extract():
            try:
                itemurl.index(li)
            except:
                itemurl.append(li)
                if 'ufi/reaction' in li:
                    print(li)
                    driver.get('https://www.facebook.com' + li)
                    time.sleep(10)
                    try:
                        while True:
                            button = driver.find_element_by_link_text('ดูเพิ่มเติม')
                            print(len(button))
                            button.click()
                            time.sleep(3)
                    except:
                        _html = driver.page_source
                        scl = Selector(text=_html).xpath('//*[@id="content"]')
                        for y in scl.css('li'):
                            name = y.css('a::text').extract_first()
                            self.listname.append(name)

    def getverify(self, source):
        reply = ['ปกติแล้วตอบกลับภายในหนึ่งวัน',
                 'ปกติแล้วตอบกลับภายในไม่กี่ชั่วโมง',
                 'ปกติแล้วตอบกลับภายในไม่กี่นาที',
                 'ปกติแล้วตอบกลับภายในหนึ่งชั่วโมง',
                 'ปกติแล้วตอบกลับโดยทันที',
                 'ปกติแล้วตอบกลับไวมาก']

        for y in reply:
            if y in str(source):
                if reply.index(y) == 2 or reply.index(y) == 3:
                    self.reply = 0.3
                    break
                else:
                    self.reply = (reply.index(y) + 1) / 10
                    break
            else:
                self.reply = 0

        scl = Selector(text=source).xpath('//*[@id="entity_sidebar"]').extract()
        if 'เพจที่ตรวจสอบยืนยันแล้วFacebook' in str(scl):
            self.verify = 1
        else:
            self.verify = 0


db = Page.conPage(database)
acc1 = Driver.Account('', '')
acc1.getaccount()
facebook = acc1.connect()
while True:
    html = facebook.page_source
    if not ('ถูกบล็อกชั่วคราว' in html) and not ('บัญชีผู้ใช้ของคุณถูกระงับการใช้งาน' in html):
        while True:
            col = db.find({'status': None}).limit(30)
            for x in col:
                page = Page('', '', '', '', '', '', '', '')
                link = Page.geturl(x['ลิ้ง'])

                facebook.get(link + 'posts')
                time.sleep(5)

                html = facebook.page_source
                if not ('ถูกบล็อกชั่วคราว' in html) or not ('บัญชีผู้ใช้ของคุณถูกระงับการใช้งาน' in html):
                    page.activity(html)

                    facebook.get(link)
                    html = facebook.page_source

                    like = page.getlike(html)
                    page.getverify(html)

                    if page.freq > 0:
                        facebook.get(link + 'posts')
                        time.sleep(3)
                        html = facebook.page_source
                        page.getpostlike(html, like)
                        page.getuseractivity(html, facebook)

                        facebook.get(link + 'reviews')
                        time.sleep(3)
                        html = facebook.page_source
                        page.getreviews(html)

                        page.getsize()
                        col = db.find_one_and_update({'ชื่อเพจ': x['ชื่อเพจ']},
                                                     {'$set': {
                                                         'av_people': page.average,
                                                         'reviews': page.reviews,
                                                         'listactivity': page.listname,
                                                         # cluster
                                                         'info': page.info,
                                                         'size': page.size,
                                                         # ---
                                                         'av_like': page.like,
                                                         'frequency': page.freq,
                                                         'verify': page.verify,
                                                         'reply': page.reply,
                                                         'status': 1}})

                    else:
                        col = db.find_one_and_update({'ชื่อเพจ': x['ชื่อเพจ']},
                                                     {'$set': {'status': 0}})
                else:
                    acc1.updateaccount()
                    facebook.close()
                    acc1.getaccount()
                    facebook = acc1.connect()
    else:
        acc1.updateaccount()
        facebook.close()
        acc1.getaccount()
        facebook = acc1.connect()
