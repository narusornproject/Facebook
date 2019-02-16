import json
import pymongo


class Response:

    # User Infomation
    @staticmethod
    def writeinfo(profile, profile_infomation, profile_places, base, collection):
        json_data = json.dumps({'โปรไฟล์': profile,
                                'ข้อมูลพื้นฐาน': profile_infomation,
                                'สถานที่ที่เคยอาศัยอยู่': profile_places}, ensure_ascii=False)
        load_data = json.loads(json_data)
        Response.conectDB(load_data, collection, base)

    # User like
    @staticmethod
    def writelistpage(profile, like, typepage, base, collection):
        json_data = json.dumps({'โปรไฟล์': profile,
                                'หมวดหมู่': typepage,
                                'รายการ': like}, ensure_ascii=False)
        load_data = json.loads(json_data)
        Response.conectDB(load_data, collection, base)

    # infomation page
    @staticmethod
    def writepagelink(listitem, base, collection):
        print(listitem)
        json_data = json.dumps(listitem, ensure_ascii=False)
        load_data = json.loads(json_data)

        # Response.conectDB(load_data, 'Pages')

        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client[base]
        col = db[collection]
        for x in load_data:
            cursor = col.find({'ชื่อเพจ': x['ชื่อเพจ']}).limit(1)
            if cursor.count() == 0:
                Response.conectDB(x, collection, base)

    # mongoDB
    @staticmethod
    def conectDB(loads, collection, base):
        # insert
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client[base]
        col = db[collection]
        col.insert(loads, check_keys=False)
        client.close()

    @staticmethod
    def DB_name(collection, name, base):
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client[base]
        col = db[collection]
        cursor = col.find({'โปรไฟล์.ชื่อ-สกุล': name}).limit(1)
        client.close()

        if cursor.count() >= 1:
            return False
        else:
            return True

    @staticmethod
    def members(collection, base):
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client[base]
        col = db[collection]
        return col