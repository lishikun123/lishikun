import json


def load_json_file(_file_name):
    _lines = open(_file_name).readlines()
    _data = list()
    for _line_index in range(0, len(_lines)):
        _d = json.loads(_lines[_line_index])
        _d.update({"code": _line_index + 1})
        _data.append(_d)
    return _data

if __name__ == "__main__":
    file_name = 'keywords.json'
    data = load_json_file(file_name)
    print(data)