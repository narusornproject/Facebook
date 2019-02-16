# -*- coding: utf-8-sig -*-
from flask import Flask, request
from flask import json
import pymongo
from bson import json_util

app = Flask(__name__)


class member:

    # cluster fetch
    @staticmethod
    @app.route('/members', methods=['GET'])
    def cluster_members():
        # level = request.args.get('level', default='', type=str)
        type = request.args.get('type', default='*', type=str)
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client['members_1503827623035837']
        temp = db['temp_copy']
        scl = list(temp.find({'interes': type}))
        client.close()
        response = app.response_class(
            response=json.dumps(scl, ensure_ascii=False, default=json_util.default),
            status=200,
            mimetype='application/json',
            headers={"Content-Type": "application/json; charset=utf-8"}
        )
        return response, 200

    @staticmethod
    @app.route('/members/live', methods=['GET'])
    def fetch_live():
        pipline = [
            {"$group": {"_id": '$live', 'count': {"$sum": 1}}},
            {"$match":  {"count": {"$gt": 20}}}
        ]
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client['members_1503827623035837']
        temp = db['temp_copy']
        scl = list(temp.aggregate(pipline))
        client.close()

        response = app.response_class(
            response=json.dumps(scl, ensure_ascii=False),
            status=200,
            mimetype='application/json',
            headers={"Content-Type": "application/json; charset=utf-8"}
        )
        return response, 200

    @staticmethod
    @app.route('/members/<name>', methods=['GET'])
    def fetch_members(name):
        item = []
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client['members_1503827623035837']
        col = db['Users_info']
        user = col.find({'โปรไฟล์.ชื่อ-สกุล': name})
        client.close()
        for detail in user:
            item.append(detail['โปรไฟล์'])
            item.append(detail['ข้อมูลพื้นฐาน'])
            item.append(detail['สถานที่ที่เคยอาศัยอยู่'])
        response = app.response_class(
            response=json.dumps(item, ensure_ascii=False),
            status=200,
            mimetype='application/json',
            headers={"Content-Type": "application/json; charset=utf-8"}
        )
        return response, 200

    # cluster
    # # response temp
    # @staticmethod
    # @app.route('/members/behavior/<name>', methods=['GET'])
    # def behavior_members(name):
    #     item = {}
    #     type = []
    #     col = conPageLike('members_1503827623035837')
    #     colpage = conPage('members_1503827623035837')
    #     user = col.find({'โปรไฟล์.ชื่อ-สกุล': name})
    #     total = 0
    #     for x in user[0]['รายการ']:
    #         total += 1
    #         page = colpage.find({'ชื่อเพจ': x}).limit(1)
    #         activity = colpage.find({'ชื่อเพจ': x,'listactivity':name}).count()
    #         try:
    #             item[page[0]['ประเภท']]['count'] += 1
    #             item[page[0]['ประเภท']]['list'].append(x)
    #         except:
    #             type.append(page[0]['ประเภท'])
    #             item[page[0]['ประเภท']] = {'type': page[0]['ประเภท'], 'count': 1, 'list': [x]}
    #     # print(item)
    #     result = []
    #     for x in item.values():
    #         if x['count'] > 20:
    #             result.append({'type': x['type'], 'count': str(x['count']), 'list': x['list']})
    #
    #     response = app.response_class(
    #         response=json.dumps(result, ensure_ascii=False),
    #         status=200,
    #         mimetype='application/json',
    #         headers={"Content-Type": "application/json; charset=utf-8"}
    #     )
    #     return response, 200

    # don't use at web
    @staticmethod
    @app.route('/members/info/<name>', methods=['GET'])
    def process(name):
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client['members_1503827623035837']
        coltemp = db['temp_copy']
        col = db['Likes_info']
        pa = db['Pages']
        info = db['Users_info']

        searchinfo = info.find({'โปรไฟล์.ชื่อ-สกุล': name})
        search = col.find({'โปรไฟล์.ชื่อ-สกุล': name})
        item = {}
        maxscorce, maxactivity, maxcount = [0, 0, 0]
        for x in search[0]['รายการ']:
            infopage = pa.find({'ชื่อเพจ': x})
            activity = pa.find({'ชื่อเพจ': x, 'listactivity': name, 'status': 1}).count()
            try:
                if infopage[0]['status'] == 1:
                    try:
                        item[infopage[0]['ประเภท']].update({'count': item[infopage[0]['ประเภท']]['count'] + 1})
                        item[infopage[0]['ประเภท']].update(
                            {'activity': item[infopage[0]['ประเภท']]['activity'] + activity})
                        item[infopage[0]['ประเภท']].update(
                            {'scorce': item[infopage[0]['ประเภท']]['scorce'] + infopage[0]['scorce']})
                        item[infopage[0]['ประเภท']]['list'].append(x)
                    # scroll
                    except:
                        item[infopage[0]['ประเภท']] = {'activity': 0, 'count': 1, 'scorce': float(infopage[0]['scorce']), 'list': [x]}

                    if maxscorce < item[infopage[0]['ประเภท']]['scorce']:
                        maxscorce = item[infopage[0]['ประเภท']]['scorce']

                    if maxactivity < item[infopage[0]['ประเภท']]['activity']:
                        maxactivity = item[infopage[0]['ประเภท']]['activity']

                    if maxcount < item[infopage[0]['ประเภท']]['count']:
                        maxcount = item[infopage[0]['ประเภท']]['count']
            except:
                pass
        ans = []
        max = 0
        # print(str(maxscorce)+' '+str(maxactivity)+' '+str(maxcount))
        try:
            day, month, space, year = str(searchinfo[0]['ข้อมูลพื้นฐาน']['วันเกิด']).split(' ')
            if int(year) < 2016:
                bod = 2018 - int(year)
            else:
                bod = 2561 - int(year)
        except:
            bod = ''
        try: live = searchinfo[0]['สถานที่ที่เคยอาศัยอยู่']['เมืองปัจจุบัน']
        except:
            try:
                live = searchinfo[0]['สถานที่ที่เคยอาศัยอยู่']['เมืองเกิด']
            except:
                live = ''

        for x in item:
            if item[x]['activity'] != 0:
                activity = (item[x]['activity'] * 2.5) / maxactivity
            else:
                activity = 0
            count = (item[x]['count'] * 1) / maxcount
            scorce = (item[x]['scorce'] * 1.5) / maxscorce

            result = activity + count + scorce
            if result > max:
                max = result
                ans = ({'name': name,
                        'bod': bod,
                        'gender': searchinfo[0]['ข้อมูลพื้นฐาน']['เพศ'],
                        'live': live,
                        'interes': x,
                        'result': result,
                        'count': item[x]['count'],
                        'scorce': item[x]['scorce']})

            item[x].update({'result': result})
        # sorted(item.items(), key=lambda kv: kv[1])
        # insert db
        coltemp.insert(ans)

        response = app.response_class(
            response=json.dumps(item, ensure_ascii=False),
            status=200,
            mimetype='application/json',
            headers={"Content-Type": "application/json; charset=utf-8"}
        )
        client.close()
        return response, 200


class Page:

    # @staticmethod
    # @app.route('/page/<name>', methods=['GET'])
    # def fetch_page(name):
    #     item = []
    #     db = conPage('members_1503827623035837')
    #     page = db.find({'ชื่อเพจ': name})
    #     for x in page:
    #         item.append({
    #             'ชื่อเพจ': x['ชื่อเพจ'],
    #             'ลิ้ง': x['ลิ้ง'],
    #             'ประเภท': x['ประเภท'],
    #             'คะเเนน': x['คะเเนน']
    #         })
    #     response = app.response_class(
    #         response=json.dumps(item, ensure_ascii=False),
    #         status=200,
    #         mimetype='application/json',
    #         headers={"Content-Type": "application/json; charset=utf-8"}
    #     )
    #     return response, 200

    @staticmethod
    @app.route('/page/type', methods=['GET'])
    def fetch_type():
        pipline = [
            {"$group": {"_id": '$interes', 'count': {"$sum": 1}}},
            {"$match": {'count': {"$gt": 50}}}
        ]
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client['members_1503827623035837']
        temp = db['temp_copy']
        scl = list(temp.aggregate(pipline))
        response = app.response_class(
            response=json.dumps(scl, ensure_ascii=False),
            status=200,
            mimetype='application/json',
            headers={"Content-Type": "application/json; charset=utf-8"}
        )
        client.close()
        return response, 200

    @staticmethod
    @app.route('/page/alltype', methods=['GET'])
    def typepage():
        pipline = [
            {"$group": {"_id": '$ประเภท', 'count': {"$sum": 1}}},
            {"$match": {'count': {"$gt": 1}}}
        ]

        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client['members_1503827623035837']
        temp = db['Pages']
        result = []
        scl = list(temp.aggregate(pipline))
        response = app.response_class(
            response=json.dumps(scl, ensure_ascii=False),
            status=200,
            mimetype='application/json',
            headers={"Content-Type": "application/json; charset=utf-8"}
        )
        client.close()
        return response, 200


if __name__ == '__main__':
    app.run(debug=True)
