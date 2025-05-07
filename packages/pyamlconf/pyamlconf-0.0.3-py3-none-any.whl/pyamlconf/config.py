import re
import yaml

# ${var}
mustache_p = re.compile(r"(\{\{ *[a-zA-Z0-9\.\-_]*? *\}\})")


class PyamlConfig:
    config_file: str
    __config: dict

    def __init__(self, config_file: str, encoding: str = 'utf-8'):
        '''
        build a yaml file to pymalconfig object
        :param config_file: a yaml file
        '''
        self.__config = {}
        self.config_file = config_file
        with open(config_file, 'r', encoding=encoding) as f:
            self.__config = yaml.safe_load(f)

    @staticmethod
    def __deep_merge(dict1: dict, dict2: dict, merge: bool):
        result = dict1.copy()
        for key, value in dict2.items():
            if not merge and not result.__contains__(key):
                continue
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = PyamlConfig.__deep_merge(result[key], value, merge)
            else:
                result[key] = value
        return result

    def update(self, config: 'PyamlConfig', merge: bool = False):
        '''
        update with another config
        :param config: PyamlConfig
        :param merge: True: merge all key; False: update exists key
        '''
        self.__config = PyamlConfig.__deep_merge(self.__config, config.__config, merge)

    def get(self, key: str, default_value=None) -> (str | int | float | bool | list | dict):
        '''
        get a value from config
        :param key: get value by this key, like: db.name
        :param default_value: if db.name have no value, then return default_value
        :return: str | int | float | bool | list | dict
        '''
        keys = key.split(".")
        i = 0
        c = self.__config
        while i < len(keys) and c is not None:
            c = c.get(keys[i])
            i += 1

        c = c if c is not None else default_value

        if c is not None and isinstance(c, str):
            ss = mustache_p.findall(c)
            if ss is not None:
                for s in ss:
                    k = s[2:-2].strip()
                    if k.startswith('.'):
                        dot_count = 0
                        while k.startswith('.'):
                            k = k[1:]
                            dot_count += 1
                        if dot_count < len(keys):
                            k = ".".join(keys[:- dot_count]) + "." + k
                    v = self.get(k)
                    c = c.replace(s, "" if v is None else str(v))

        return c

    def get_str(self, key: str, default_value=None) -> str:
        return str(self.get(key, default_value))

    def get_int(self, key: str, default_value: int = None) -> int:
        return int(self.get(key, default_value))

    def get_float(self, key: str, default_value: float = None) -> float:
        return float(self.get(key, default_value))

    def get_bool(self, key: str, default_value: bool = None) -> bool:
        return bool(self.get(key, default_value))

    def get_list(self, key: str, default_value: bool = None) -> list:
        return list(self.get(key, default_value))

    def get_tuple(self, key: str, default_value: bool = None) -> tuple:
        return tuple(self.get(key, default_value))

    def get_set(self, key: str, default_value: bool = None) -> set:
        return set(self.get(key, default_value))
