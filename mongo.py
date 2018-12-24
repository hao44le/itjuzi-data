import pymongo
import json

def read_mongodb_cre():
    sec = open('.secret')
    data = json.load(sec)['mongodb']
    sec.close()
    return data

def get_companies_connections():
    mongodb_uri = read_mongodb_cre()
    client = pymongo.MongoClient(mongodb_uri)
    db = client.itjuzi.companies
    return db

def query(db, json):
    return db.find(json)

def is_query_exist(db, json):
    return db.find(json).count() > 0

def check_company_id_exist_or_not(db, company_id):
    return is_query_exist(db, {'company_id': company_id})

def inserts(db, jsons):
    return db.insert_many(jsons)

if __name__ == '__main__':
    db = get_companies_connections()
    result = check_company_id_exist_or_not(db, "1")
    print(result)
    # obj = query(db, {"username":"abc", "company":"abc","keyword":"abc"})
    # print(obj)
