from functools import cache

class TypeHelper :
    @property
    def function (self) :
        return type(lambda: 1)

    @property
    def property (self) :
        return type(TypeHelper.function)

      
def construct_node_json (title, ext, src, links, data) :
    return {
        "title" : title,
        "type" : ext,
        "source" : src,
        "links" : links,
        "data" : data
    }


TYPE = TypeHelper()

class FileHelper :
    def __init__ (self, path : str, sep : str = ':') :
        self.path = path
        self.sep = sep

    def __str__ (self) : return self.path

    @property
    @cache
    def ext (self) -> str : 
        return self.path.split('.')[-1]

    @property
    @cache
    def file (self) -> 'FileHelper' :
        return FileHelper(self.path.split('/')[-1], self.sep)

    @property
    @cache
    def filename (self) -> str :
        return str(self.file).split('.')[0]

    @property
    @cache
    def dirs (self) -> list[str] :
        return self.path.split('/')[:-1]

    @property
    @cache
    def dir (self) -> 'FileHelper' :
        return FileHelper('/'.join(self.dirs) + '/', self.sep)

    @property
    @cache
    def filename_sect (self) -> list[str] :
        return self.filename.split(self.sep)

    def prepend (self, target : str, sep : str = None) -> 'FileHelper' :
        return FileHelper(f"{self.dir}{target}{self.sep}{self.file}", self.sep)

    def chext (self, new_ext : str) -> 'FileHelper' :
        return FileHelper(f"{self.dir}{self.filename}.{new_ext}", self.sep)


def get_defining_class (obj : type, method : str) :
    return getattr(obj, method).__code__.co_qualname.split('.')[0]

def is_defined_in_lowest_subclass (obj : type, method : str) :
    return get_defining_class(obj, method) == obj.__name__

def _get_content (obj : type) :
    return [i for i in obj.__dict__.keys() if not (i.startswith('__') and i.endswith('__'))]

def get_methods (obj : type) :
    return [i for i in _get_content(obj) if isinstance(type(getattr(obj, i)), TYPE.function)]

def get_properties (obj : type) :
    return [i for i in _get_content(obj) if isinstance(type(getattr(obj, i)), TYPE.property)]

def default (func) :
    func.__isdefaultmethod__ = True
    return func
   
def implements_interface_semantics (cls : type, subclass : type) -> bool :
    # cls is the interface
    # subclass is the subclass
    try: 
        return all([
            hasattr(subclass, i) and 
            callable(getattr(subclass, i)) and 
            (get_defining_class(subclass, i) != cls.__name__ or getattr(cls, i).__isdefaultmethod__) and
            (getattr(subclass, i).__annotations__ == getattr(cls, i).__annotations__)
        for i in get_methods(cls)]) and \
                all([
            hasattr(subclass, i) and
            get_defining_class(subclass, i) != cls.__name__
        for i in get_properties(cls)])
    except AttributeError :
        return False

def implement (target_interface : type) :
    def implements_decorator (cls) :
        if not implements_interface_semantics(target_interface, cls) :
            raise SyntaxError("Interface Not Implemented Properly")
        return cls
    return implements_decorator

class Interface (type) :
    """
    Interface Metaclass. All methods defined in the interface must be overridden
    in subclasses or isinstance and issubclass return false.

    Demands that: 
    - All implementing classes have all methods defined in the Interface
    - All such methods are callable
    - All such methods have the same annotations as the parent class (expect the same types, return 
        the same types)
    - All such methods are not defined in the Interface that is currently being checked isinstance
    - All implementing classes have all properties defined in the interface
    - All such methods are not defined in the Interface that is currently being checked isinstance

    Limitations: 
    - Interfaces must not inherit from any classes. 
    - @default decorator MUST be the top decorator or else there can be undefined behavior

    @todo implement @default decorator for default methods
    """
    def __instancecheck__ (cls, instance) :
        return issubclass(cls, type(instance))

    def __subclasscheck__ (cls, subclass) :
        return implements_interface_semantics(cls, subclass)

class TypeCollisionError (BaseException) :
    pass
