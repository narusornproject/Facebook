from Driver import Account
import json
from Link import Links
from Responses import Response
from Infomation import Info
from Page import Pages
import Scroll
import time
typepage = ['all']
facebook = ''
# config
base = 'members'
user_col = 'Users_info'
like_col = 'Likes_info'
page_col = 'Pages'


def createlist(listitem):
    item = {}
    for key, value in listitem.items():
        # print(value)
        item.update({key: value})
    return item


class Main:
    # runs = 300
    print('Creating robo browser...')
    # account = Account('narusorn.r@hotmail.com', 'narusorn28041997')
    # account = Account('biw_chotzii@hotmail.com', 'pp0740994')
    account = Account('', '')
    account.getaccount()
    account = Account('bdprtoject002@gmail.com', '@Bigdata001')

    facebook = account.connect()

    print('Starting get information...')

    # get list
    col = Response.members(user_col, base)
    json_data = col.find({})
    #########

    for data in json_data:
        link = Links('', '', '', '')
        info = Info('', '', '', '', '', '')
        page = Pages('', '', '', '', '', '', '', '', '')
        # Profile

        # check url correct

        # check name from database
        ck_name = Response.DB_name(user_col, data['name'], base)
        if ck_name:
            ck = Account.geturl(facebook, data['url'])
            currenturl = data['url']
            if ck:
                html = facebook.page_source
                if not ('ถูกบล็อกชั่วคราว' in html):
                    item = Links.getlink(html)
                    link.createinstance(item)
                    # ----------

                    # Link about
                    Account.geturl(facebook, link.about)
                    currenturl = link.about
                    Scroll.scroll(facebook)
                    html = facebook.page_source
                    like = Pages.getpage(html)
                    page.createinstance(like)
                    item = Info.getinfo(html)
                    info.createinstance(item)
                    # ----------

                    # Infomation
                    Account.geturl(facebook, info.nav_contact_basic)
                    # currenturl = info.nav_contact_basic
                    html = facebook.page_source
                    besic = Info.getbesic(html)

                    Account.geturl(facebook, info.nav_places)
                    # currenturl = info.nav_places
                    html = facebook.page_source
                    places = Info.getplaces(html)

                    img = Info.getimg(html)
                    # ----------

                    # write data
                    Profile = {
                        'ชื่อ-สกุล': data['name'],
                        'ลิ้ง': data['url'],
                        'รูปภาพ': img
                        # 'from': from
                    }
                    # ----------

                    # page like
                    for x in typepage:
                        if (x == 'all') and not (page.all == ''):
                            Account.geturl(facebook, page.all)
                            currenturl = page.all
                            Scroll.scroll(facebook)
                            html = facebook.page_source

                            item = page.get_user_like(html)
                            listitem = page.get_pagelink(html)
                            # All Pages
                            Response.writepagelink(listitem, base, page_col)
                            # User_likes
                            Response.writelistpage(Profile, item, x, base, like_col)

                    # ----------

                    # Convert list to json
                    Infomation_besic = createlist(besic)
                    Infomation_places = createlist(places)
                    # ----------
                    if not (len(Infomation_besic)) == 0 and not (len(Infomation_places) == 0):
                        Response.writeinfo(Profile, Infomation_besic, Infomation_places, base, user_col)
                    else:
                        time.sleep(100)
                else:
                    account.updateaccount()
                    facebook.close()
                    account.getaccount()
                    facebook = account.connect()
