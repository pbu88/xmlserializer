import unittest
from xmlserializer import XMLSerializerMixin
from testdata import *


class TestSerializerFlat(unittest.TestCase):
    
    def setUp(self):
        self.foo = Foo(2)
    
    def test_to_xml_flat(self):        
        self.failUnless(self.foo.to_xml() == foo_xml)
        
    def test_from_xml_flat(self):
        obj = Foo.from_xml(foo_xml)
        self.failUnless(self.foo.y == obj.y)
        
        
class TestSerializerNested(unittest.TestCase):

    def setUp(self):
        self.bar = Bar(Foo(2), 1, 'hola')

    def test_to_xml_nested(self):
        self.failUnless(self.bar.to_xml() == bar_xml)

    def test_from_xml_nested(self):
        obj = Bar.from_xml(bar_xml)
        self.failUnless(
            self.bar.x == obj.x
            and self.bar.s == obj.s
            and self.bar.myfoo.y == obj.myfoo.y
        )
        
        
class TestSerializerWithDataStructures(unittest.TestCase):
    def setUp(self):
        self.dic = Dic({1:'hola', 2:'adios'})
        self.lst = Lst([1,'hola'])
        self.tup = Tup((1,'hola'))
        self.rand = NestedWithRandomClass()
        
    def test_to_xml_dict(self):
        self.failUnless(self.dic.to_xml() == dic_xml)
        
    def test_from_xml_dict(self):
        obj = XMLSerializerMixin.from_xml(dic_xml)
        self.failUnless(obj.mydict[1] == 'hola' and
                        obj.mydict[2]=='adios')
        
    def test_to_xml_list(self):
        self.failUnless(self.lst.to_xml() == lst_xml)
        
    def test_from_xml_list(self):
        obj = XMLSerializerMixin.from_xml(lst_xml)
        self.failUnless(obj.mylist[0] == 1 and
                        obj.mylist[1] == 'hola')
        
    def test_to_xml_tuple(self):
        self.failUnless(self.tup.to_xml() == tup_xml)
        
    def test_from_xml_tuple(self):
        obj = XMLSerializerMixin.from_xml(tup_xml)
        self.failUnless(obj.mytuple[0] == 1 and
                        obj.mytuple[1] == 'hola')
        
    def test_to_xml_random_class(self):
        self.failUnless(self.rand.to_xml() == rand_xml)
        
    def test_from_xml_random_class(self):
        obj = XMLSerializerMixin.from_xml(rand_xml)
        self.failUnless(self.rand.rc.x == obj.rc.x)
        
        
class TestSerializerWithClassInSubPackages(unittest.TestCase):
    
    def setUp(self):
        self.pkgd = Packaged()
        
    def test_to_xml_class_in_nested_package(self):
        self.failUnless(self.pkgd.to_xml() == pkgd_cls_xml)
        
    def test_from_xml_class_in_nested_package(self):
        obj = XMLSerializerMixin.from_xml(pkgd_cls_xml)
        self.failUnless(obj.pkgd.x == self.pkgd.pkgd.x)
        
        
class TestSerializerOnLongDeepStructure(unittest.TestCase):
    
    def setUp(self):
        self.nested = NestedDictionaryListAndTuple()
        
    def test_to_xml_nested_deep_structure(self):
        self.failUnless(self.nested.to_xml() == nested_dic_lst_tup_xml)
        
    def test_from_xml_nested_deep_structure(self):
        obj = XMLSerializerMixin.from_xml(nested_dic_lst_tup_xml)
        self.failUnless(
            self.nested.lst[0].myfoo.y == obj.lst[0].myfoo.y
            and self.nested.lst[0].s == obj.lst[0].s
            and self.nested.lst[0].x == obj.lst[0].x
            and self.nested.tup[0].rc.x == obj.tup[0].rc.x
            and self.nested.tup[1].pkgd.x == obj.tup[1].pkgd.x
            and self.nested.dic.keys()[0].y == obj.dic.keys()[0].y
            and self.nested.dic.values()[0].x == obj.dic.values()[0].x
            )
        

def main():
    unittest.main()

    
if __name__ == '__main__':
    main()