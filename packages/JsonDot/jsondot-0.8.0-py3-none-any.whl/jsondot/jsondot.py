import json
from typing import Optional, Union, Any

class Dot(object):
    
    def __init__(self, file_path: Optional[str] = None) -> None:
        super().__setattr__('file_path', file_path)
        super().__setattr__('translation', {})
        pass

    def __str__(self) -> str:
        return self.__dict__.__str__()
    
    def __setattr__(self, name: str, value: Any) -> None:
        if self.translation and not name in self.translation:
            name = self.format_param(name)
        if isinstance(value, list):
            value = self.process_list(value)
        elif isinstance(value, dict):
            value = self.__load_data(value)
        super().__setattr__(name, value)
        
    def set_file_path(self, path: str):
        self.file_path = path
    
    def loads(self, s: str):
        return JsonDot.loads(s, self.file_path)
        
    def load(self, path):
        return self._load(path)
    
    def _load(self, path):
        d = JsonDot.load(path, self)
        if isinstance(d, Dot):
            self.file_path = path
        return d
        
    def __load_data(self, data: Union[dict,list]):
        return JsonDot.load_data(data, Dot(self.file_path)) 
    
    def format_param(self, param):
        nparam = JsonDot.format_param(param)
        self.translation[nparam] = param
        return nparam 
    
    def process_list(self, l: list):
        return JsonDot.process_list(l, self.file_path)
    
    def process_list_for_load(self, l: list):
        return JsonDot.process_list_for_load(l, self.file_path) 
    
    def process_list_for_dumps(self, l: list):
        return JsonDot.process_list_for_dumps(l) 
    
    def format_json(self, s: str):
        return JsonDot.format_json(s)  
    
    def remove_slash(self, s: str):
        return JsonDot.remove_slash(s)
    
    def load_field(self, name, value):
        name = self.format_param(name)
        setattr(self, name, value)
        return self

    def add_field(self, name, value):
        name = self.format_param(name)
        if isinstance(value, list):
            blist = self.process_list(value)
            setattr(self, name, blist)
        else: 
            setattr(self, name, value)
        return self
    
    def change_field_name(self, name, new_name):
        name = self.format_param(name)
        fnew_name = self.format_param(new_name)
        if hasattr(self, name):
            value = getattr(self, name)
            delattr(self, name)
            setattr(self, new_name, value)
            if self.translation and name in self.translation:
                del self.translation[name]
                self.translation[fnew_name] = new_name
        return self
    
    def dumps(self):
        data = self._dumps()
        fdata = self.format_json(data)
        return fdata

    def _dumps(self):
        items = self.__dict__.items()
        s = ''
        d1 = {}
        for k, v in items:
            if isinstance(v, Dot):
                v1 = v._dumps()
                if self.translation and k in self.translation:
                    k = self.translation[k]
                v2 = self.remove_slash(v1)
                d1[k] = v2
            elif isinstance(v, list):
                blist = list()
                for i, elem in enumerate(v):
                    if isinstance(elem, Dot):
                        v1 = elem._dumps()
                        if self.translation and k in self.translation:
                            k = self.translation[k]
                        v2 = self.remove_slash(v1)
                        blist.append(v2)
                    elif isinstance(elem, list):
                        clist = self.process_list_for_dumps(elem)
                        blist.append(clist)
                    else:
                        blist.append(elem)
                if self.translation and k in self.translation:
                    k = self.translation[k]
                d1[k] = blist
            elif isinstance(v, bool):
                v1 = str(v).lower()
                if self.translation and k in self.translation:
                    k = self.translation[k]
                d1[k] = v1                       
            elif k != 'translation' and k != 'file_path':
                if self.translation and k in self.translation:
                    k = self.translation[k]
                d1[k] = v
        s = d1.__str__()
        return s

    def dump(self, path: Optional[str] = None):
        if self.file_path is not None and path is None:
            path = self.file_path            
        self.file_path = path
        data = self._dumps()
        data = self.format_json(data)
        with open(path, 'w') as file:
            file.write(data)

    def items(self):
        d = self.__dict__.items()
        d1 = self.translate(d, self.translation)
        return d1.items()

    def translate(self, dictionary: dict, translation):
        d1 = {}
        for k, v in dictionary:
            if isinstance(v, Dot):
                bd = {}
                bd[k] = self.translate(v.__dict__.items(), v.translation)
                d1[k] = bd[k]
            elif k != 'translation':
                key = translation[k]
                d1[key] = v
        return d1  

class JsonDot():

    def __init__(self) -> None:
        self.file_path = ""
        self.data = None
        self.dot = None
        pass

    @classmethod
    def loads(cls, s: str, path) -> Dot:
        dot = Dot(path)
        sj = json.loads(s)
        dot = cls.__load_data(sj, dot, path)
        return dot
    
    @classmethod
    def load(cls, path: str, dot:Optional[Dot] = None) -> Dot:
        return cls._load(path, dot)
    
    @classmethod
    def create_dot_from_file(cls, path: str) -> Dot:
        return cls.load(path)
    
    @classmethod
    def _load(cls, path: str, dot: Optional[Dot] = None) -> Dot:
        with open(path, 'r') as f:
            data = json.load(f)
        if dot is not None and isinstance(dot, Dot):
            dot = dot
        else:
            dot = Dot(path)
        dot = cls.__load_data(data, dot, path)       
        return dot
    
    @classmethod
    def load_data(cls, data: Union[dict,list], dot: Union[Dot,list], path: str = None) -> Dot:
        return cls.__load_data(data, dot, path)
    
    @classmethod
    def __load_data(cls, data: Union[dict,list], dot: Union[Dot,list], path: str = None) -> Dot:
        for k, v in data.items():
            if isinstance(v, dict):
                bdot = Dot(path)
                dot.load_field(k, cls.__load_data(v, bdot))
            elif isinstance(v, list):
                blist = cls.process_list_for_load(v, path)
                dot.load_field(k, blist)
            elif isinstance(v, str):
                if v.strip().lower() == 'true':
                    dot.load_field(k, True)
                elif v.strip().lower() == 'false':
                    dot.load_field(k, False)
                else:
                    dot.load_field(k, v)
            else:
                dot.load_field(k, v)
        return dot
    
    @staticmethod
    def format_param(param):
        new_param = ""
        for char in param:
            if char == "-" or char == " ":
                new_param += "_"
            else:
                new_param += char
        new_param = new_param.lower()
        return new_param
    
    @staticmethod            
    def format_json(s: str):
        output = ''
        for char in s:
            if char == "'":
                output += '"'
            elif char == '"':
                output += " "
            else:
                output += char
        return output
    
    @staticmethod            
    def remove_slash(s: str):
        output = ''
        for char in s:
            if char == "\\":
                output += ""
            elif char == '"':
                output += ""
            else:
                output += char
        return output
    
    @classmethod       
    def process_list_for_load(cls, l: list, path: str = None) -> list:
        return cls.process_list(l, path)
    
    @staticmethod
    def process_list_static(l: list, file_path: Optional[str] = None):
        return JsonDot.__shared_process_list(l, file_path)
    
    @classmethod
    def process_list(cls, l: list, path: str = None) -> list:
        return cls.__shared_process_list(l, path)
    
    @classmethod
    def __shared_process_list(cls, l: list, file_path: Optional[str]):
        blist = []
        for elem in l:            
            if isinstance(elem, dict):
                bdot = Dot(file_path)
                d = cls.__load_data(elem, bdot)
            elif isinstance(elem, list):
                d = cls.__shared_process_list(elem, file_path)
            else:
                d = elem
            blist.append(d)
        return blist
    
    @classmethod
    def process_list_for_dumps(cls, l: list):
        blist = []
        e = None
        d = None
        for elem in l:            
            if isinstance(elem, Dot):
                e = elem
                d = elem._dumps()               
            elif isinstance(elem, list):
                e = elem
                d = cls.process_list_for_dumps(e)
            else:
                d = elem
            blist.append(d)
        return blist
    
