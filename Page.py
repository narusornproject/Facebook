from scrapy.selector import Selector


class Pages:
    def __init__(self, movies, tv_shows, music, books, apps_and_games, sports_teams, sports_athletes,
                 restaurants, all):
        self.movies = movies
        self.tv_shows = tv_shows
        self.music = music
        self.books = books
        self.apps_and_games = apps_and_games
        self.sports_teams = sports_teams
        self.sports_athletes = sports_athletes
        self.restaurants = restaurants
        self.all = all

    def createinstance(self, item):
        for i in item:
            # create object
            if i['type'] == 'ภาพยนตร์':
                self.movies = i['link']
            if i['type'] == 'รายการโทรทัศน์':
                self.tv_shows = i['link']
            if i['type'] == 'เพลง':
                self.music = i['link']
            if i['type'] == 'หนังสือ':
                self.books = i['link']
            if i['type'] == 'แอพและเกม':
                self.apps_and_games = i['link']
            if i['type'] == 'ทีมกีฬา':
                self.sports_teams = i['link']
            if i['type'] == 'นักกีฬา':
                self.sports_athletes = i['link']
            if i['type'] == 'ร้านอาหาร':
                self.restaurants = i['link']
            if i['type'] == 'การถูกใจทั้งหมด':
                self.all = i['link']

    @staticmethod
    def getpage(html):
        item = []
        response = Selector(text=html).xpath('//*[@id="pagelet_timeline_medley_likes"]')
        for scl in response.css('a'):
            obj = scl.css('a::attr(href)').extract_first()
            text = scl.css('a::attr(name)').extract_first()
            item.append({
                'type': text,
                'link': obj
            })
        return item

    @staticmethod
    def get_user_like(html):
        item = []
        response = Selector(text=html).xpath('//*[@id="pagelet_timeline_medley_likes"]')
        for scl in response.css('li'):
            text = scl.css('a::text').extract_first()
            item.append(text)
        return item

    @staticmethod
    def get_pagelink(html):
        item = []
        response = Selector(text=html).xpath('//*[@id="pagelet_timeline_medley_likes"]')
        for scl in response.css('li'):
            link = scl.css('a::attr(href)').extract_first()
            text = scl.css('a::text').extract_first()
            catagory = scl.css('div::text').extract_first()
            item.append({"ชื่อเพจ": text,
                         "ลิ้ง": link,
                         "ประเภท": catagory,
                         "คะเเนน":  0})
        return item
