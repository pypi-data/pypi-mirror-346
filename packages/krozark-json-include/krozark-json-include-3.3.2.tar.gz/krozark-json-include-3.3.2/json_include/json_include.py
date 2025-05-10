import json
import os
import random
import re
import string
from collections import OrderedDict

OBJECT_TYPES = (dict, list)
INCLUDE_KEYS = ['...', '$ref']
INCLUDE_VALUE_PATTERNS = [
    re.compile(r'^#/(.+)$'),  # simple local definition
    re.compile(r'^include\((.+)\)$'),  # include
    re.compile(r'^file:(.+)?#/(.+)$'),  # remote definition inclusion
    re.compile(r'^file:(.+)$'),  # remote file inclusion
    re.compile(r'^(.+)?#/(.+)$'),  # remote definition inclusion without `file:` pattern
]
INCLUDE_INDEX_LOCAL = [0]
INCLUDE_INDEX_DEFINITION = [2, 4]
INCLUDE_TEXT_PATTERN = re.compile(r'^include_text\((.+)\)$')


class JSONInclude(object):
    def __init__(self):
        self._included_cache = None
        self._original_schemas = None

    def _random_string(self, length=9):
        return ''.join(
            random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(length)
        )

    @staticmethod
    def _read_file(filePath):
        with open(filePath) as f:
            data = f.read()
            return JSONInclude.read_content_without_comments(data)

    @staticmethod
    def read_content_without_comments(file_content):
        useful_lines = []
        for line in file_content.splitlines():
            # Split at the first '//' and trim whitespace
            content = line.split('//', 1)[0].strip()
            if content:  # Add only if the line is not empty
                useful_lines.append(content)
        return "\n".join(useful_lines)

    def _get_include_name(self, value, regex_list):
        if not isinstance(regex_list, list):
            # passing single regex only
            return self._get_include_name([value], regex_list)[0]
        else:
            # passing list of regex`s
            for idx, regex in enumerate(regex_list):
                if isinstance(value, str):
                    rv = regex.search(value)
                    if rv:
                        return rv.groups(), idx
            return None, None

    def _lookup(self, dic, key, *keys):
        if keys:
            return self._lookup(dic.get(key, {}), *keys)
        return dic.get(key)

    def _make_unique(self, obj, key, original=None, replacement=None):
        """
        Walk through the dict and add random string to the value at key
        and all other occurrences of the same value.
        """
        if key in obj and isinstance(obj[key], str):
            original = obj[key]
            replacement = obj[key] + "-" + self._random_string()
            obj[key] = replacement
        for k, v in obj.items():
            if original and v == original:
                obj[k] = replacement
            if isinstance(v, dict):
                self._make_unique(v, key, original, replacement)
        return obj

    def _include_definition(self, include_name, schema):
        attr = include_name.split("/")
        return self._lookup(schema, *attr)

    def _include_remote_file(self, dirpath, include_name):
        _f = os.path.join(dirpath, include_name)
        if include_name not in self._included_cache:
            remote_schema = self._parse_json_include(os.path.dirname(_f), os.path.basename(_f))
            self._cleanup_before_inclusion(remote_schema)
            return remote_schema
        else:
            return self._included_cache[include_name]

    def _cleanup_before_inclusion(self, data):
        if isinstance(data, list):
            for item in data:
                self._cleanup_before_inclusion(item)
            return
        elif isinstance(data, dict):
            data.pop('$schema', None)  # remove $schema property before inclusion

    def _walk_through_to_include(self, o, dirpath):
        if isinstance(o, dict):
            is_include_exp = False
            make_unique_key = o.pop('makeUnique', None)
            # if a key match a INCLUDE_KEYS
            if any(map(lambda x: x in o, INCLUDE_KEYS)):
                include_key = [y for y in map(lambda x: x if x in o else None, INCLUDE_KEYS) if y][0]  # get key that match
                include_info, include_idx = self._get_include_name(o[include_key], INCLUDE_VALUE_PATTERNS)
                if include_info:
                    is_include_exp = True
                    include_name = include_info[0]
                    if include_idx in INCLUDE_INDEX_LOCAL:
                        # include local definitions
                        self._included_cache[include_name] = self._include_definition(
                            include_name,
                            self._original_schemas[-1]
                        )
                    elif include_idx in INCLUDE_INDEX_DEFINITION:
                        # include remote definitions
                        include_name = include_info[1]
                        remote_file_schema = self._include_remote_file(dirpath, include_info[0])
                        self._included_cache[include_name] = self._include_definition(include_name, remote_file_schema)
                    else:
                        # enable relative directory references: `../../`
                        self._included_cache[include_name] = self._include_remote_file(dirpath, include_name)
                    # remove "key : include-pattern" from dict

                    _data = self._included_cache[include_name]
                    o.pop(include_key)
                    # add data under include_key if it is not a dictionary
                    if not isinstance(_data, dict):
                        _data = {include_key: _data}
                    if make_unique_key:
                        o.update(self._make_unique(_data, make_unique_key))
                    else:
                        o.update(_data)

            if is_include_exp:
                # don't recurse
                return

        if isinstance(o, dict):
            for k, v in o.items():
                self._walk_through_to_include(v, dirpath)
        elif isinstance(o, list):
            for i in o:
                self._walk_through_to_include(i, dirpath)

    def _parse_json_include(self, dirpath, filename):
        filepath = os.path.join(dirpath, filename)
        json_str = self._read_file(filepath)
        d = self._resolve_extend_replace(json_str, filepath)

        self._original_schemas.append(d)
        self._walk_through_to_include(d, dirpath)
        self._original_schemas.pop()
        return d

    def build_json_include(self, dirpath, filename=None):
        """Parse a json file and build it by the include expression recursively.

        :param str dirpath: The directory path of source json files.
        :param str filename: The name of the source json file.
        :return: A json string with its include expression replaced by the indicated data.
        :rtype: str
        """
        self._included_cache = {}
        self._original_schemas = []
        return self._parse_json_include(dirpath, filename)

    def parse_vars(self, data, **vars):
        """
        Change the structure of data to select branch to use.

        data = {
            "message": "hello world",
            "CHECK_OS": {
                "linux": {
                    "os": "linux",
                    "console": True,
                },
                "android": {
                    "os": "android",
                    "console": False,
                }
            }
        }
        result = pars_vars(data,CHECK_OS="linux")
        print(result)
        {
            "message: "hello world",
            "os": "linux",
            "console": True,
        }

        the value of all key CHECK_OS are removed, and the sub data corresponding of its value is added in place.

        :param data: the dict to update
        :param vars: the vars to use
        :return: data modified
        """
        if isinstance(data, dict):
            for var_key in list(data.keys()):
                # check if the key is in vars, and get its value
                key_to_use = vars.get(var_key, None)
                if not key_to_use:
                    continue

                # here we have a "switch" to build depending on the value of var_to_use
                value = data.get(var_key)
                if isinstance(value, dict):
                    all_values = data.pop(var_key)
                    value = all_values.get(key_to_use)
                    if not value:
                        continue
                    # add new data
                    data.update(value)

            for key in data:
                data[key] = self.parse_vars(data[key], **vars)
        elif isinstance(data, str):
            data = data.format(**vars)

        return data


    def _resolve_extend_replace(self, str, filepath):
        """
        Resolve the content `$extend` and `$replace` keys:

        {
            "$extend": {
                "name": "parent.json"
            },
            "$replace": [
                {
                    "where": {
                        "key": "units",
                        "idx": 4
                    },
                    "with": "$this.units"
                },


        :param str str: json string with file content
        :param str filepath: path to the file
        :rtype: dict
        """
        obj = json.loads(str, object_pairs_hook=OrderedDict)
        if not isinstance(obj, dict):
            return obj
        extend = obj.get("$extend", {})
        replace = obj.get("$replace", {})
        filename = extend.get("name", None)
        if filename:
            json_string = self._read_file(os.path.join(os.path.dirname(filepath), filename))
            json_data = json.loads(json_string, object_pairs_hook=OrderedDict)
            for entry in replace:
                key = entry["where"]["key"]
                idx = entry["where"].get("idx", None)
                idx_cache = 0
                _with = entry["with"]
                _replacement = obj.get(_with.replace("$this.", "")) if _with and "$this." in _with else _with
                _current_value = json_data[key]
                if (idx or idx == 0) and isinstance(_current_value, list):
                    del _current_value[idx]
                    if isinstance(_replacement, list):
                        for _in, _el in enumerate(_replacement):
                            _current_value.insert(idx + _in, _el)
                            idx_cache += 1
                    else:
                        _current_value.insert(idx, _replacement)
                    _replacement = _current_value
                json_data[key] = _replacement
            obj = json_data
        return obj


def build_json(dirpath, filename=None, **kwargs):
    if filename is None:
        dirpath = os.path.abspath(os.path.join(os.getcwd(), dirpath))
        dirpath, filename = os.path.split(dirpath)

    jsoninc = JSONInclude()
    data = jsoninc.build_json_include(dirpath, filename)
    if kwargs:
        data = jsoninc.parse_vars(data, **kwargs)
    return data


def build_str(dirpath, filename=None, indent=4, **kwargs):
    d = build_json(dirpath, filename=filename, **kwargs)
    return json.dumps(d, indent=indent, separators=(',', ': '))



