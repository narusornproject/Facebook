from scrapy.selector import Selector


class Info:
    def __init__(self, nav_edu_work, nav_places, nav_contact_basic, nav_all_relationships, nav_about, nav_year_overviews):
        self.nav_edu_work = nav_edu_work
        self.nav_places = nav_places
        self.nav_contact_basic = nav_contact_basic
        self.nav_all_relationships = nav_all_relationships
        self.nav_about = nav_about
        self.nav_year_overviews = nav_year_overviews

    def createinstance(self, item):
        for i in item:
            # create object
            if i['title'] == 'nav_edu_work':
                self.nav_edu_work = i['link']
            if i['title'] == 'nav_places':
                self.nav_places = i['link']
            if i['title'] == 'nav_contact_basic':
                self.nav_contact_basic = i['link']
            if i['title'] == 'nav_all_relationships':
                self.nav_all_relationships = i['link']
            if i['title'] == 'nav_about':
                self.nav_about = i['link']
            if i['title'] == 'nav_year_overviews':
                self.nav_year_overviews = i['link']

    @staticmethod
    def getinfo(html):
        item = []
        response = Selector(text=html).xpath('//*[@id="pagelet_timeline_medley_about"]')
        for scl in response.css('ul[class]'):
            for s in scl.css('li'):
                # if s.css('a::attr(href)').extract_first() != "#":
                item.append(
                    {
                        'title': s.css('a::attr(data-testid)').extract_first(),
                        'link': s.css('a::attr(href)').extract_first()
                    })
        return item

    @staticmethod
    def getbesic(html):
        item = {}
        response = Selector(text=html).xpath('//*[@id="pagelet_basic"]')
        for scl in response.css('li[class]'):
            info = scl.css('span[class="_50f4 _5kx5"]').css('span::text').extract_first()
            if info == 'ภาษา' or info == 'ศาสนาที่นับถือ':
                value = scl.css('span[class="_2iem"]').css('a::text').extract()
            else:
                value = scl.css('span[class="_2iem"]').css('span::text').extract_first()
            item.update({info: value})
        response = Selector(text=html).xpath('//*[@id="pagelet_contact"]')
        for scl in response.css('li[class]'):
            if scl.css('span::text').extract_first() != 'ไม่มีข้อมูลการติดต่อให้แสดง':
                value = scl.css('span[class="_2iem"]').css('a::attr(href)').extract_first()
                info = scl.css('span[class="_50f4 _5kx5"]').css('span::text').extract_first()
                item.update({info: value})
        return item

    @staticmethod
    def getplaces(html):
        item = {}
        response = Selector(text=html).xpath('//*[@id="pagelet_hometown"]')
        for scl in response.css('li[class]'):
            info = scl.css('div::text').extract_first()
            value = scl.css('a::text').extract_first()
            item.update({info: value})
        return item

    @staticmethod
    def getimg(html):
        response = Selector(text=html).xpath('//*[@id="fbTimelineHeadline"]')
        img = response.css('img::attr(src)').extract_first()
        return img
