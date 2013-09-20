from importlib import import_module
from xml.etree.ElementTree import Element, tostring, XML


class XMLSerializerMixin(object):

    """
    Provide serialize to xml functionality to inheriting classes.
    
    Functions:
    to_xml -- Dumps an object to its xml representation.
    from_xml (static) -- Returns an object from the xml representation.
    
    Private Functions:
    _to_xml -- Does the `to_xml`'s actual job.
    _to_xml_int
    _to_xml_str
    _to_xml_dict
    _to_xml_list
    _to_xml_tuple
    
    _from_xml (static) -- Does the `from_xml`'s actual job.
    _from_xml_int (static)
    _from_xml_str (static)
    _from_xml_dict (static)
    _from_xml_list (static)
    _from_xml_tuple (static)
    """
    
    def to_xml(self):
        """
        Return the xml representation of the object as string.
        """
        return tostring(self._to_xml(self))
    
    def _to_xml(self, obj):
        """
        Return the xml representation of any object as Element
        
        Args:
        obj -- the actual object to work with (can be an XMLSerializerMixin
               or any class)
        """
        xml = Element(obj.__class__.__name__)
        xml.attrib['module'] = obj.__class__.__module__
        
        for key in obj.__dict__:
            value = obj.__dict__[key]
            child = Element(key)
            func = self._serializer_function(value)
            child.append(func(value))
            child[0].attrib['module'] = value.__class__.__module__
            xml.append(child)
            
        return xml
        
    def _to_xml_int_and_str(self, obj):
        """
        Return the xml Element of an int or a str.
        
        Args:
        obj -- the int or str to work with
        """
        xml = Element(obj.__class__.__name__)
        xml.attrib['module'] = obj.__class__.__module__
        xml.text = str(obj)
        return xml
    
    _to_xml_int = _to_xml_str = _to_xml_int_and_str
    
    def _to_xml_dict(self, obj):
        """
        Return the xml Element of a dict.
        
        Args:
        obj -- the dictionary to work with
        """
        xml = Element(obj.__class__.__name__)
        xml.attrib['module'] = obj.__class__.__module__
        
        for key in obj:
            xml.append(Element('entry'))
            child = xml[-1]
            
            child.append(Element('key'))
            func_key = self._serializer_function(key)
            child[0].append(func_key(key))
            
            child.append(Element('value'))
            func_value = self._serializer_function(obj[key])
            child[1].append(func_value(obj[key]))
            
        return xml
        
    def _to_xml_iterable(self, obj):
        """
        Return the xml Element of a list or tuple.
        
        Args:
        obj -- the list or tuple to work with
        """
        xml = Element(obj.__class__.__name__)
        xml.attrib['module'] = obj.__class__.__module__
        
        for elem in obj:
            xml.append(Element('element'))
            child = xml[-1]
            func = self._serializer_function(elem)
            child.append(func(elem))
            
        return xml
        
    _to_xml_list = _to_xml_tuple = _to_xml_iterable

    def _serializer_function(self, obj):
        """
        Return the function used for serializing the object
        
        This method returns the method used to serialize the object
        according to the object's class' name. If the method doesn't
        exists, it returns the default `_to_xml` method.
        
        Args:
        obj -- the object that needs to be serialied
        """
        try:
            func = getattr(self, '_to_xml_' + obj.__class__.__name__)
        except AttributeError:
            func = self._to_xml
            
        return func
        
    
    @staticmethod
    def from_xml(xml):
        """
        Return the Python object retrieved from the xml.
        
        Args:
        xml -- the xml string to work with.
        """
        return XMLSerializerMixin._from_xml(XML(xml))
    
    @staticmethod
    def _from_xml(parsed):
        """
        Return the Python object retrieved from the parsed xml.
        
        Args:
        parsed -- the parsed xml received from `from_xml` function.
        """
        module = import_module(parsed.attrib['module'])
        cls = getattr(module, parsed.tag)
        # Instantiate the class without calling it's constructor
        obj = cls.__new__(cls)
        
        for child in parsed:
            try:
                func = getattr(XMLSerializerMixin, '_from_xml_' + child[0].tag)
            except AttributeError:
                func = XMLSerializerMixin._from_xml
                
            obj.__dict__[child.tag] = func(child[0])
            
        return obj
            
    @staticmethod
    def _from_xml_int_and_str(parsed):
        """
        Return the builtin `int` or `str` type from the xml.
        
        Args:
        parsed -- the parsed xml.
        """
        module_name = parsed.attrib['module']
        module = import_module(module_name)
        cls = getattr(module, parsed.tag)
        obj = cls(parsed.text)
        return obj
        
    _from_xml_int = _from_xml_str = _from_xml_int_and_str
    
    @staticmethod
    def _from_xml_dict(parsed):
        """
        Return the builtin `dict` type from the xml.
        
        Args:
        parsed -- the parsed xml.
        """
        module_name = parsed.attrib['module']
        module = import_module(module_name)
        cls = getattr(module, parsed.tag)
        obj = {}
        
        for child in parsed:
            key = child.find('key')
            func_key = XMLSerializerMixin._deserializer_function(key[0].tag)
            
            value = child.find('value')
            func_value = XMLSerializerMixin._deserializer_function(value[0].tag)
            
            obj[func_key(key[0])] = func_value(value[0])
            
        return obj
    
    @staticmethod
    def _from_xml_iterable(parsed):
        """
        Return the builtin `list` or `tuple` type from the xml.
        
        Args:
        parsed -- the parsed xml.
        """
        module_name = parsed.attrib['module']
        module = import_module(module_name)
        cls = getattr(module, parsed.tag)
        obj = []

        for child in parsed:
            func = XMLSerializerMixin._deserializer_function(child[0].tag)
            obj.append(func(child[0]))
            
        return obj

    
    _from_xml_list = _from_xml_iterable
    _from_xml_tuple = staticmethod(
            lambda parsed : tuple(XMLSerializerMixin._from_xml_iterable(parsed))
    )
    _from_xml_set = _from_xml_iterable
        
    @staticmethod
    def _deserializer_function(tag):
        """
        Return the function used for de-serializing the xml element
        
        This method returns the function used to de-serialize the xml 
        element according to its tag. If the function doesn't
        exists, it returns the default `_from_xml` function.
        
        Args:
        obj -- the element's tag that needs to be de-serialied
        """
        try:
            func = getattr(XMLSerializerMixin,
                           '_from_xml_' + tag)
        except AttributeError:
            func = XMLSerializerMixin._from_xml
            
        return func