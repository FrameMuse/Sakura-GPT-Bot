import json

class Serializable:
    def __init__(self, fields_map: dict):
        self.__fields_map = fields_map
        self._fields = fields_map.keys()
    
    # def represents(self):
    #     return self

    def _toJSON(self):
        def filter_fields(cls):          
            fields = {}
            for key in self._fields:
                fields[key] = str(cls.__dict__.get(key, ""))
            return fields
        
        return json.dumps(self, default=filter_fields, indent=4, ensure_ascii=False)

    def _assign(self, fields: dict):
        for key, value in fields.items():
            self.__dict__[key] = self.__fields_map[key](value)

    def _assign_fromJSON(self, string: str):
        json_content = json.loads(string)
        return self._assign(json_content)
