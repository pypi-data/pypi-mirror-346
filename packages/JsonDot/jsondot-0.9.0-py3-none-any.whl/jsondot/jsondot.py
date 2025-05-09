import json
from typing import Optional, Union, Any

class Dot(object):
    """
    Dot is a class that provides functionality for managing JSON-like data structures 
    with additional features such as dynamic attribute setting, JSON serialization, 
    and field name translation.
    Attributes:
        file_path (Optional[str]): The file path associated with the Dot instance.
        translation (dict): A dictionary used for translating field names.
    Methods:
        __init__(file_path: Optional[str] = None) -> None:
            Initializes a Dot instance with an optional file path.
        __str__() -> str:
            Returns a string representation of the Dot instance.
        __setattr__(name: str, value: Any) -> None:
            Dynamically sets attributes, processing lists and dictionaries as needed.
        set_file_path(path: str):
            Sets the file path for the Dot instance.
        loads(s: str):
            Loads JSON data from a string using the JsonDot utility.
        load(path):
            Loads JSON data from a file.
        _load(path):
            Internal method to load JSON data from a file and update the file path.
        __load_data(data: Union[dict, list]):
            Processes and loads data into a Dot instance.
        format_param(param):
            Formats a parameter name and updates the translation dictionary.
        process_list(l: list):
            Processes a list using the JsonDot utility.
        process_list_for_load(l: list):
            Processes a list for loading using the JsonDot utility.
        process_list_for_dumps(l: list):
            Processes a list for dumping using the JsonDot utility.
        format_json(s: str):
            Formats a JSON string using the JsonDot utility.
        remove_slash(s: str):
            Removes slashes from a string using the JsonDot utility.
        load_field(name, value):
            Loads a field into the Dot instance, formatting the field name.
        add_field(name, value):
            Adds a field to the Dot instance, formatting the field name and processing lists if necessary.
        change_field_name(name, new_name):
            Changes the name of an existing field, updating the translation dictionary.
        dumps():
            Serializes the Dot instance to a JSON string.
        _dumps():
            Internal method to serialize the Dot instance to a JSON-compatible dictionary.
        dump(path: Optional[str] = None):
            Serializes the Dot instance and writes it to a file.
        items():
            Returns the items of the Dot instance, applying field name translations.
        translate(dictionary: dict, translation):
            Translates field names in a dictionary using the provided translation mapping.
    """
    
    def __init__(self, file_path: Optional[str] = None) -> None:
        """
        Initializes a new instance of the class.

        Args:
            file_path (Optional[str]): The path to the file. Defaults to None.
        """
        super().__setattr__('file_path', file_path)
        super().__setattr__('translation', {})
        pass

    def __str__(self) -> str:
        """
        Returns a string representation of the object's dictionary.

        This method is used to provide a human-readable string representation
        of the object by converting its internal `__dict__` attribute, which
        contains all the instance attributes, into a string.

        Returns:
            str: A string representation of the object's dictionary.
        """
        return self.__dict__.__str__()
    
    def __setattr__(self, name: str, value: Any) -> None:
        """
        Overrides the default behavior of setting an attribute on the object.

        If a translation mapping is defined and the attribute name is not in the 
        translation, the name is formatted using the `format_param` method. 
        Additionally, if the value being set is a list or a dictionary, it is 
        processed accordingly before being assigned.

        Args:
            name (str): The name of the attribute to set.
            value (Any): The value to assign to the attribute.

        Raises:
            AttributeError: If the attribute cannot be set.
        """
        if self.translation and not name in self.translation:
            name = self.format_param(name)
        if isinstance(value, list):
            value = self.process_list(value)
        elif isinstance(value, dict):
            value = self.__load_data(value)
        super().__setattr__(name, value)
        
    def set_file_path(self, path: str):
        """
        Sets the file path for the current instance.

        Args:
            path (str): The file path to be set.
        """
        self.file_path = path
    
    def loads(self, s: str):
        """
        Parses a JSON-formatted string and returns a JsonDot object.

        Args:
            s (str): The JSON-formatted string to be parsed.

        Returns:
            JsonDot: An instance of JsonDot initialized with the parsed data.

        Raises:
            ValueError: If the input string is not a valid JSON.
        """
        return JsonDot.loads(s, self.file_path)
        
    def load(self, path):
        """
        Load data from the specified file path.

        Args:
            path (str): The file path to load the data from.

        Returns:
            Any: The data loaded from the file.

        Raises:
            Exception: If there is an error during the loading process.
        """
        return self._load(path)
    
    def _load(self, path):
        """
        Load a JSON file from the specified path and return its contents.

        If the loaded data is an instance of `Dot`, the `file_path` attribute
        of the current object is updated to the provided path.

        Args:
            path (str): The file path to the JSON file to be loaded.

        Returns:
            Any: The contents of the loaded JSON file, which could be any
            valid JSON data type (e.g., dict, list, etc.).
        """
        d = JsonDot.load(path, self)
        if isinstance(d, Dot):
            self.file_path = path
        return d
        
    def __load_data(self, data: Union[dict,list]):
        """
        Loads the provided data into a JsonDot object.

        Args:
            data (Union[dict, list]): The data to be loaded, which can be either a dictionary or a list.

        Returns:
            JsonDot: An instance of JsonDot containing the loaded data.
        """
        return JsonDot.load_data(data, Dot(self.file_path)) 
    
    def format_param(self, param):
        """
        Formats a parameter and updates the translation mapping.

        This method takes a parameter, formats it using the `JsonDot.format_param` 
        method, and stores the mapping between the formatted parameter and the 
        original parameter in the `translation` dictionary.

        Args:
            param (Any): The parameter to be formatted.

        Returns:
            Any: The formatted parameter.
        """
        nparam = JsonDot.format_param(param)
        self.translation[nparam] = param
        return nparam 
    
    def process_list(self, l: list):
        """
        Processes a list using the JsonDot class.

        Args:
            l (list): The list to be processed.

        Returns:
            The result of processing the list using the JsonDot class and the 
            specified file path.
        """
        return JsonDot.process_list(l, self.file_path)
    
    def process_list_for_load(self, l: list):
        """
        Processes a list for loading by delegating to the static method 
        `JsonDot.process_list_for_load`.

        Args:
            l (list): The list to be processed.

        Returns:
            The result of processing the list using `JsonDot.process_list_for_load`.

        """
        return JsonDot.process_list_for_load(l, self.file_path) 
    
    def process_list_for_dumps(self, l: list):
        """
        Processes a list for serialization in the dumps method.

        This method is a wrapper that delegates the processing of the list
        to the `process_list_for_dumps` method of the `JsonDot` class.

        Args:
            l (list): The list to be processed.

        Returns:
            The processed list, formatted for JSON serialization.
        """
        return JsonDot.process_list_for_dumps(l) 
    
    def format_json(self, s: str):
        """
        Formats a JSON string into a more readable format.

        Args:
            s (str): The JSON string to be formatted.

        Returns:
            str: A formatted and indented JSON string.
        """
        return JsonDot.format_json(s)  
    
    def remove_slash(self, s: str):
        """
        Removes slashes from the given string.

        Args:
            s (str): The input string from which slashes should be removed.

        Returns:
            str: A new string with all slashes removed.
        """
        return JsonDot.remove_slash(s)
    
    def load_field(self, name, value):
        """
        Sets an attribute on the current object with the given name and value.

        Args:
            name (str): The name of the attribute to set. It will be formatted
                using the `format_param` method before being set.
            value (Any): The value to assign to the attribute.

        Returns:
            self: The current instance of the object, allowing for method chaining.
        """
        name = self.format_param(name)
        setattr(self, name, value)
        return self

    def add_field(self, name, value):
        """
        Adds a new field to the object with the specified name and value.

        Args:
            name (str): The name of the field to add. It will be formatted using `format_param`.
            value (Any): The value to assign to the field. If the value is a list, it will be
                         processed using `process_list` before being assigned.

        Returns:
            self: The instance of the object, allowing for method chaining.
        """
        name = self.format_param(name)
        if isinstance(value, list):
            blist = self.process_list(value)
            setattr(self, name, blist)
        else: 
            setattr(self, name, value)
        return self
    
    def change_field_name(self, name, new_name):
        """
        Changes the name of an existing field in the object.

        Args:
            name (str): The current name of the field to be changed.
            new_name (str): The new name to assign to the field.

        Returns:
            self: The instance of the object, allowing for method chaining.

        Notes:
            - The method uses `format_param` to process both the current and new field names.
            - If the field exists, its value is preserved under the new name, and the old field is removed.
            - If the object has a `translation` attribute and the old field name exists in it, 
              the translation mapping is updated to reflect the new field name.
        """
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
        """
        Serializes the current object to a formatted JSON string.

        This method first generates a JSON representation of the object
        using the `_dumps` method, and then formats the JSON string
        using the `format_json` method.

        Returns:
            str: A formatted JSON string representation of the object.
        """
        data = self._dumps()
        fdata = self.format_json(data)
        return fdata

    def _dumps(self):
        """
        Serializes the attributes of the current object into a string representation.

        This method iterates through the attributes of the object, processes them based on their type,
        and constructs a dictionary representation of the object. The dictionary is then converted
        to a string and returned.

        Returns:
            str: A string representation of the object's attributes.

        Processing Details:
            - If an attribute is an instance of `Dot`, its `_dumps` method is recursively called.
            - If an attribute is a list, each element is processed:
                - If the element is a `Dot` instance, its `_dumps` method is called.
                - If the element is a nested list, it is processed using `process_list_for_dumps`.
                - Otherwise, the element is added to the list as-is.
            - If an attribute is a boolean, it is converted to a lowercase string.
            - Attributes named 'translation' and 'file_path' are excluded from the output.
            - If a `translation` dictionary is present, attribute keys are translated based on it.
            - Slashes in serialized `Dot` objects are removed using `remove_slash`.

        Note:
            - The method assumes the presence of `translation`, `remove_slash`, and `process_list_for_dumps`
              as part of the object's attributes or methods.
        """
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
        """
        Serializes the current object to a JSON file.

        Args:
            path (Optional[str]): The file path where the JSON data will be written.
                                  If not provided, the instance's `file_path` attribute
                                  will be used.

        Raises:
            ValueError: If no valid file path is provided.

        Notes:
            - If `path` is not specified and `self.file_path` is None, a ValueError
              will be raised.
            - The JSON data is formatted before being written to the file.
        """
        if self.file_path is not None and path is None:
            path = self.file_path            
        self.file_path = path
        data = self._dumps()
        data = self.format_json(data)
        with open(path, 'w') as file:
            file.write(data)

    def items(self):
        """
        Retrieves the items of the object's dictionary, applies a translation
        to the keys or values, and returns the translated items.

        Returns:
            dict_items: A view object that displays a list of the dictionary's 
            key-value pairs after applying the translation.
        """
        d = self.__dict__.items()
        d1 = self.translate(d, self.translation)
        return d1.items()

    def translate(self, dictionary: dict, translation):
        """
        Translates the keys of a dictionary based on a given translation mapping.

        Args:
            dictionary (dict): The input dictionary whose keys need to be translated.
            translation (dict): A mapping dictionary where the keys are the original 
                keys from the input dictionary, and the values are the translated keys.

        Returns:
            dict: A new dictionary with the keys translated based on the provided 
            translation mapping.

        Notes:
            - If a value in the input dictionary is an instance of `Dot`, the method 
              recursively translates its attributes.
            - The key 'translation' is skipped during the translation process.
        """
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
    """
    JsonDot is a utility class for loading, processing, and manipulating JSON data
    with a dot notation interface. It provides methods to load JSON from strings
    or files, process lists, and format JSON strings.
    Methods
    -------
    __init__():
        Initializes an instance of the JsonDot class.
    loads(s: str, path) -> Dot:
        Loads JSON data from a string and returns a Dot object.
    load(path: str, dot: Optional[Dot] = None) -> Dot:
        Loads JSON data from a file and returns a Dot object.
    create_dot_from_file(path: str) -> Dot:
        Creates a Dot object from a JSON file.
    load_data(data: Union[dict, list], dot: Union[Dot, list], path: str = None) -> Dot:
        Loads JSON data into a Dot object or list.
    format_param(param: str) -> str:
        Formats a parameter string by replacing spaces and hyphens with underscores
        and converting it to lowercase.
    format_json(s: str) -> str:
        Formats a JSON string by replacing single quotes with double quotes.
    remove_slash(s: str) -> str:
        Removes backslashes and double quotes from a string.
    process_list_for_load(l: list, path: str = None) -> list:
        Processes a list for loading JSON data.
    process_list_static(l: list, file_path: Optional[str] = None):
        Processes a list statically for JSON data.
    process_list(l: list, path: str = None) -> list:
        Processes a list for JSON data.
    process_list_for_dumps(l: list) -> list:
        Processes a list for dumping JSON data.
    Private Methods
    ---------------
    _load(path: str, dot: Optional[Dot] = None) -> Dot:
        Internal method to load JSON data from a file.
    __load_data(data: Union[dict, list], dot: Union[Dot, list], path: str = None) -> Dot:
        Internal method to recursively load JSON data into a Dot object or list.
    __shared_process_list(l: list, file_path: Optional[str]) -> list:
        Internal method to process lists for JSON data.
    """

    def __init__(self) -> None:
        """
        Initializes an instance of the class.

        Attributes:
            file_path (str): The file path to be used. Defaults to an empty string.
            data (Any): Placeholder for data to be loaded or processed. Defaults to None.
            dot (Any): Placeholder for dot-related data or operations. Defaults to None.
        """
        self.file_path = ""
        self.data = None
        self.dot = None
        pass

    @classmethod
    def loads(cls, s: str, path) -> Dot:
        """
        Deserialize a JSON-formatted string into a Dot object.

        Args:
            s (str): The JSON-formatted string to deserialize.
            path: The path to associate with the Dot object.

        Returns:
            Dot: A Dot object populated with the data from the JSON string.
        """
        dot = Dot(path)
        sj = json.loads(s)
        dot = cls.__load_data(sj, dot, path)
        return dot
    
    @classmethod
    def load(cls, path: str, dot:Optional[Dot] = None) -> Dot:
        """
        Load a JSON file from the specified path and return a Dot object.

        Args:
            path (str): The file path to the JSON file to be loaded.
            dot (Optional[Dot]): An optional Dot object to populate with the loaded data. 
                                 If not provided, a new Dot object will be created.

        Returns:
            Dot: The Dot object containing the data from the loaded JSON file.
        """
        return cls._load(path, dot)
    
    @classmethod
    def create_dot_from_file(cls, path: str) -> Dot:
        """
        Create a Dot object from a JSON file.

        This method loads a JSON file from the specified path and converts it 
        into a Dot object.

        Args:
            path (str): The file path to the JSON file.

        Returns:
            Dot: An instance of the Dot class created from the JSON file.
        """
        return cls.load(path)
    
    @classmethod
    def _load(cls, path: str, dot: Optional[Dot] = None) -> Dot:
        """
        Load data from a JSON file and populate a Dot object.

        Args:
            path (str): The file path to the JSON file to be loaded.
            dot (Optional[Dot], optional): An existing Dot object to populate. 
                If not provided or not an instance of Dot, a new Dot object will be created. Defaults to None.

        Returns:
            Dot: The populated Dot object.
        """
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
        """
        Load data into a Dot object or a list of Dot objects.

        This method processes the given data and populates the provided Dot object(s)
        with the corresponding values. Optionally, a path can be specified to indicate
        the base path for the data.

        Args:
            data (Union[dict, list]): The data to be loaded, either as a dictionary or a list.
            dot (Union[Dot, list]): The target Dot object or a list of Dot objects to populate.
            path (str, optional): The base path for the data. Defaults to None.

        Returns:
            Dot: The populated Dot object.
        """
        return cls.__load_data(data, dot, path)
    
    @classmethod
    def __load_data(cls, data: Union[dict,list], dot: Union[Dot,list], path: str = None) -> Dot:
        """
        Recursively loads data from a dictionary or list into a Dot object.

        Args:
            data (Union[dict, list]): The input data to be loaded, which can be a dictionary or a list.
            dot (Union[Dot, list]): The target Dot object or list where the data will be loaded.
            path (str, optional): The current path in the data hierarchy. Defaults to None.

        Returns:
            Dot: The Dot object populated with the loaded data.

        Notes:
            - If a value in the data is a dictionary, it recursively creates a new Dot object for it.
            - If a value is a list, it processes the list using `process_list_for_load`.
            - String values of "true" and "false" (case-insensitive) are converted to boolean True and False, respectively.
            - Other values are directly loaded into the Dot object.
        """
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
        """
        Formats a given parameter string by replacing hyphens ('-') and spaces (' ') 
        with underscores ('_') and converting all characters to lowercase.

        Args:
            param (str): The input string to be formatted.

        Returns:
            str: The formatted string with hyphens and spaces replaced by underscores 
                 and all characters in lowercase.
        """
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
        """
        Formats a given JSON-like string by replacing single quotes with double quotes
        and replacing double quotes with spaces.

        Args:
            s (str): The input string to be formatted.

        Returns:
            str: The formatted string with single quotes replaced by double quotes
                 and double quotes replaced by spaces.
        """
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
        """
        Removes backslashes and double quotes from the input string.

        Args:
            s (str): The input string to process.

        Returns:
            str: A new string with all backslashes and double quotes removed.
        """
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
        """
        Processes a list for loading by delegating to the `process_list` method.

        Args:
            l (list): The list to be processed.
            path (str, optional): The path associated with the list. Defaults to None.

        Returns:
            list: The processed list.
        """
        return cls.process_list(l, path)
    
    @staticmethod
    def process_list_static(l: list, file_path: Optional[str] = None):
        """
        Processes a list in a static context, optionally using a specified file path.

        Args:
            l (list): The list to be processed.
            file_path (Optional[str], optional): The file path to be used during processing. 
                Defaults to None.

        Returns:
            The result of processing the list using the shared processing logic.
        """
        return JsonDot.__shared_process_list(l, file_path)
    
    @classmethod
    def process_list(cls, l: list, path: str = None) -> list:
        """
        Processes a list and returns the result after applying a shared processing method.

        Args:
            l (list): The list to be processed.
            path (str, optional): An optional path string to be used during processing. Defaults to None.

        Returns:
            list: The processed list.
        """
        return cls.__shared_process_list(l, path)
    
    @classmethod
    def __shared_process_list(cls, l: list, file_path: Optional[str]):
        """
        Processes a list by iterating through its elements and handling each element
        based on its type. If an element is a dictionary, it processes it using the
        `__load_data` method. If an element is a list, it recursively processes it
        using `__shared_process_list`. Otherwise, it appends the element as is.

        Args:
            l (list): The list to be processed.
            file_path (Optional[str]): The file path to be used for creating Dot objects.

        Returns:
            list: A new list with processed elements.
        """
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
        """
        Processes a list for serialization by converting its elements into a format
        suitable for dumping.

        This method iterates through the elements of the input list and processes
        each element based on its type:
        - If the element is an instance of `Dot`, it calls the `_dumps` method of
          the `Dot` instance to serialize it.
        - If the element is a nested list, it recursively processes the nested list
          by calling `process_list_for_dumps`.
        - For all other types, the element is added to the result as is.

        Args:
            cls: The class reference, used for recursive calls.
            l (list): The input list to be processed.

        Returns:
            list: A new list where each element has been processed for serialization.
        """
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
    
