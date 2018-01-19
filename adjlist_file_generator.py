from pymongo import MongoClient
import pymongo
import pickle

__db_server, __db_port, __db_name = '127.0.0.1', 27017, 'WOS'


def duplicate_author():
    _authors = find_all_authors()
    for _author in _authors:
        _client = MongoClient(__db_server, __db_port, maxPoolSize=4000)
        _db = _client[__db_name]
        _da = "duplicate_authors"
        if _da not in _db.collection_names():
            _dac = _db.create_collection(_da)
        else:
            _dac = _db.get_collection(_da)
        _dac.update({
                "author_first_name": _author["author_first_name"],
                "author_last_name": _author["author_last_name"],
                "organization": _author["organization"]
            }, {'$setOnInsert': _author}, upsert=True)
    _client.close()


def encode_author():
    _client = MongoClient(__db_server, __db_port, maxPoolSize=4000)
    _db = _client[__db_name]
    _da = "duplicate_authors"
    _dac = _db.get_collection(_da)
    _cursor = _dac.find()
    _author_order = 1
    for _c in _cursor:
        _c["code"] = _author_order
        _author_order += 1
        _dac.update({"_id": _c["_id"]}, {"$set": _c})
    _client.close()


def find_all_authors():
    _client = MongoClient(__db_server, __db_port, maxPoolSize=400)
    _db = _client[__db_name]
    _collection = _db.get_collection("0301-4215_address_adjust")
    _items = _collection.find()
    _client.close()
    return list(_items)


def find_coauthors_by_article_id(_article_id):
    _client = MongoClient(__db_server, __db_port, maxPoolSize=4000)
    _dac_add_ajs = _client[__db_name]["0301-4215_address_adjust"]
    _dac = _client[__db_name]["duplicate_authors"]
    _authors = list(_dac_add_ajs.find(
        {"article_id": _article_id},
        {"author_first_name": 1, "author_last_name": 1, "organization": 1}))
    _author_codes = list()
    for _author in _authors:
        _result = _dac.find_one({
                    "author_first_name": _author["author_first_name"],
                    "author_last_name": _author["author_last_name"],
                    "organization": _author["organization"]
                })
        _author_codes.append(_result["code"])
    _client.close()
    return _author_codes


def make_adjlist():
    _client = MongoClient(__db_server, __db_port, maxPoolSize=4000)
    _dac = _client[__db_name]["duplicate_authors"]
    _cursor = _dac.find({}).sort([("code", pymongo.ASCENDING)])
    _dac_add_ajs = _client[__db_name]["0301-4215_address_adjust"]
    _coauthor_dict = dict()
    for _c in _cursor:
        _current_author_code = _c["code"]
        _results = _dac_add_ajs.find({
                "author_first_name": _c["author_first_name"],
                "author_last_name": _c["author_last_name"],
                "organization": _c["organization"]
            })
        _coauthors = list()
        for _result in _results:
            _article_id = _result["article_id"]
            _coauthors.extend(find_coauthors_by_article_id(_article_id))

            # print(_authors)
        _coauthors = list(set(_coauthors))
        _coauthors.remove(_current_author_code)
        _coauthor_dict[_current_author_code] = _coauthors
    _pickle_out = open("dict.pickle", "wb")
    pickle.dump(_coauthor_dict, _pickle_out)
    _pickle_out.close()
    _client.close()


def write_ajd_file():
    _pickle_in = open("dict.pickle", "rb")
    _dict = pickle.load(_pickle_in)
    for k, vs in _dict.items():
        if len(vs) != 0:
            for v in vs:
                _dict[v].remove(k)
    _adj_file = open("test.adjlist", "w+")
    _adj_file.write("#\n")
    for k, vs in _dict.items():
        vs = [str(v) for v in vs]
        if len(vs) != 0:
            _line = str(k) + " " + " ".join(vs) + "\n"
            _adj_file.write(_line)

        # 是否写入孤立的节点?
        """
        else:
            _adj_file.write(str(k) + "\n")
        """
    _adj_file.close()
    _pickle_in.close()

if __name__ == "__main__":
    """
    duplicate_author()
    encode_author()
    print("编码完毕")

    make_adjlist()
    """
    write_ajd_file()