from xmlserializer import XMLSerializerMixin
from testpkg.subpkg.code import PackagedClass

MODULE_NAME = __name__

class Foo(XMLSerializerMixin):
    x = 1
    def __init__(self, y):
        self.y = y
        
foo_xml = ('<Foo module="{0}">'
          +  '<y>'
          +    '<int module="__builtin__">2</int>'
          +  '</y>'
          +'</Foo>').format(MODULE_NAME)
          

class Bar(XMLSerializerMixin):
    def __init__(self, myfoo, x, s):
        self.myfoo = myfoo
        self.x = x
        self.s = s
        
bar_xml = ('<Bar module="{0}">'
          +  '<x>'
          +    '<int module="__builtin__">1</int>'
          +  '</x>'
          +  '<s>'
          +    '<str module="__builtin__">hola</str>'
          +  '</s>'
          +  '<myfoo>'
          +    '<Foo module="{0}">'
          +      '<y>'
          +        '<int module="__builtin__">2</int>'
          +      '</y>'
          +    '</Foo>'
          +  '</myfoo>'
          +'</Bar>').format(MODULE_NAME)
          
        
class Dic(XMLSerializerMixin):
    def __init__(self, d):
        self.mydict = d
        
dic_xml = ('<Dic module="{0}">'
          +  '<mydict>'
          +    '<dict module="__builtin__">'
          +      '<entry>'
          +        '<key>'
          +          '<int module="__builtin__">1</int>'
          +        '</key>'
          +        '<value>'
          +          '<str module="__builtin__">hola</str>'
          +        '</value>'
          +      '</entry>'
          +      '<entry>'
          +        '<key>'
          +          '<int module="__builtin__">2</int>'
          +        '</key>'
          +        '<value>'
          +          '<str module="__builtin__">adios</str>'
          +        '</value>'
          +      '</entry>'
          +    '</dict>'
          +  '</mydict>'
          +'</Dic>').format(MODULE_NAME)
          
        
class Lst(XMLSerializerMixin):
    def __init__(self, l):
        self.mylist = l
        
lst_xml = ('<Lst module="{0}">'
          +  '<mylist>'
          +    '<list module="__builtin__">'
          +      '<element>'
          +        '<int module="__builtin__">1</int>'
          +      '</element>'
          +      '<element>'
          +        '<str module="__builtin__">hola</str>'
          +      '</element>'
          +    '</list>'
          +  '</mylist>'
          +'</Lst>').format(MODULE_NAME)
          
        
class Tup(XMLSerializerMixin):
    def __init__(self, t):
        self.mytuple = t
        
tup_xml = ('<Tup module="{0}">'
          +  '<mytuple>'
          +    '<tuple module="__builtin__">'
          +      '<element>'
          +        '<int module="__builtin__">1</int>'
          +      '</element>'
          +      '<element>'
          +        '<str module="__builtin__">hola</str>'
          +      '</element>'
          +    '</tuple>'
          +  '</mytuple>'
          +'</Tup>').format(MODULE_NAME)

class RandomClass(object):
    def __init__(self, x):
        self.x = x

class NestedWithRandomClass(XMLSerializerMixin):
    def __init__(self):
        self.rc = RandomClass(1)
        
rand_xml = ('<NestedWithRandomClass module="{0}">'
           +  '<rc>'
           +    '<RandomClass module="{0}">'
           +      '<x>'
           +        '<int module="__builtin__">1</int>'
           +      '</x>'
           +    '</RandomClass>'
           +  '</rc>'
           +'</NestedWithRandomClass>').format(MODULE_NAME)
           
class Packaged(XMLSerializerMixin):
    def __init__(self):
        self.pkgd = PackagedClass(1)
           
pkgd_cls_xml = ('<Packaged module="{0}">'
               +  '<pkgd>'
               +    '<PackagedClass module="testpkg.subpkg.code">'
               +      '<x>'
               +        '<int module="__builtin__">1</int>'
               +      '</x>'
               +    '</PackagedClass>'
               +  '</pkgd>'
               +'</Packaged>').format(MODULE_NAME)
               
class NestedDictionaryListAndTuple(XMLSerializerMixin):
    def __init__(self):
        self.dic = {Foo(2):RandomClass(1)}
        self.lst = [Bar(Foo(2), 1, 'hola')]
        self.tup = (NestedWithRandomClass(), Packaged())
        
nested_dic_lst_tup_xml = ('<NestedDictionaryListAndTuple module="{0}">'
                         +  '<tup>'
                         +    '<tuple module="__builtin__">'
                         +      '<element>'
                         +        rand_xml
                         +      '</element>'
                         +      '<element>'
                         +        pkgd_cls_xml
                         +      '</element>'
                         +    '</tuple>'
                         +  '</tup>'
                         +  '<lst>'
                         +    '<list module="__builtin__">'
                         +      '<element>'
                         +        bar_xml
                         +      '</element>'
                         +    '</list>'
                         +  '</lst>'
                         +  '<dic>'
                         +    '<dict module="__builtin__">'
                         +      '<entry>'
                         +        '<key>'
                         +          foo_xml
                         +        '</key>'
                         +        '<value>'
                         +          '<RandomClass module="{0}">'
                         +            '<x>'
                         +              '<int module="__builtin__">1</int>'
                         +            '</x>'
                         +        '</RandomClass>'
                         +        '</value>'
                         +      '</entry>'
                         +    '</dict>'
                         +  '</dic>'
                         +'</NestedDictionaryListAndTuple>').format(MODULE_NAME)