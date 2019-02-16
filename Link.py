from scrapy.selector import Selector


class Links:

    def __init__(self, timeline, about, friends, photos):
        self.timeline = timeline
        self.about = about
        self.friends = friends
        self.photos = photos

    def createinstance(self, item):
        for i in item:
            # create object
            if i['type'] == 'photos':
                self.photos = i['link']
            if i['type'] == 'timeline':
                self.timeline = i['link']
            if i['type'] == 'about':
                self.about = i['link']
            if i['type'] == 'friends':
                self.friends = i['link']

    @staticmethod
    def getlink(html):
        item = []
        response = Selector(text=html).xpath('//*[@id="fbTimelineHeadline"]')
        for scl in response.css('ul[class]'):
            for s in scl.css('li'):
                # if s.css('a::attr(href)').extract_first() != "#":
                item.append({
                        'type': s.css('a::attr(data-tab-key)').extract_first(),
                        'link': s.css('a::attr(href)').extract_first()
                    })
        return item
