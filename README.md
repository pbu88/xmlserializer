# Python's XMLSerializerMixin

_Another tool for XML serialization in Python._

The `XMLSerializerMixin` is intended to bring a **very** simple way to persist your Python's object to XML. You'll need only two methods to write your objects as XML and read them back. 

It's a very useful way to show your object's XML representation when writing a web service, storing them in the hard drive or passing them as arguments to remote functions for example.

## Show me some code...!

The `XMLSerializerMixin` -- as its name says -- is intended to be used as a `mixin` for your current objects. Say you have an `Dog` object:

	class Dog(object):
	
	    def __init__(self, name, favourite_toy):
	        self.name = name
            self.favourite_toy = favourite_toy

And you want to show its _XML representation_ for some purpose. Then, you can add the `to_xml` functionality to the `Dog` class by simple inheriting from `XMLSerializerMixin`:

    from xmlserializer import XMLSerializerMixin
    class Dog(XMLSerializerMixin):
	
	    def __init__(self, name, favourite_toy):
	        self.name = name
            self.favourite_toy = favourite_toy

    >>>dog = Dog('Gio', 'ball')
    >>>dog.to_xml()
    '<Dog module="__main__"><favourite_toy><str module="__builtin__">ball</str></favourite_toy><name><str module="__builtin__">Gio</str></name></Dog>'

As you can see, it's very easy to get the XML representation of the object. Later on, suppose you have some dog's XML representation. You can turn it into a Python's Dog class by just doing:

    >>>dog_xml = '<Dog module="__main__"><favourite_toy><str module="__builtin__">ball</str></favourite_toy><name><str module="__builtin__">Gio</str></name></Dog>'
    >>>dog = Dog.from_xml(dog_xml)
    >>>dog.name
    'Gio'
    >>>dog.favourite_toy
    'ball'
    
_**Note**: This can cause problems with `IPython` interpreter and other `Python`'s interpreter because dynamically importing `__main__` module. With official Python's interpreter it works well._

As you may see. It almost takes no effort to bring objects back and forth to XML. But now, let's say for example that you don't want your dog to inherit `XMLSerializeMixin` -- you love your dog so much that you want to keep its pedigree intact ;) --. You have several ways to accomplish the task anyways. For example, let's build an XMLDogHouse for it, so we can put it in there as XML and bring it out whenever we want.

    from xmlserializer import XMLSerializerMixin
    class Dog(object):
	
	    def __init__(self, name, favourite_toy):
	        self.name = name
            self.favourite_toy = favourite_toy

    class XMLDogHouse(XMLSerializerMixin):
        
        def __init__(self, dog):
            self.dog = dog

    That's it, now your dog **isn't** and XMLSerializerMixin anymore, but you still can persist it in XML:

    >>>dog = Dog('Gio', 'ball')
    >>>XMLDogHouse(dog).to_xml()
    '<XMLDogHouse module="__main__"><dog><Dog module="__main__"><favourite_toy><str module="__builtin__">ball</str></favourite_toy><name><str module="__builtin__">Gio</str></name></Dog
></dog></XMLDogHouse>'

And to bring it back from its XML house, just need to do:

    >>>dog = XMLDogHouse.from_xml(xml_housed_dog)
    >>>dog.name
    'Gio'

`XMLSerializerMixin` can also play with some `built-in` data types as well, like `list`s. So if you want your dog house to be a little bigger to have `Gio`'s girlfriend `Lassie`, you can do it easily:

    class XMLDogHouse(XMLSerializerMixin):
        
        def __init__(self, dogs):
            self.dogs = dogs

    >>>gio = Dog('Gio', 'ball')
    >>>lassie = Dog('Lassie', 'stick')
    >>>love_nest = XMLDogHouse([gio, lassie])
    >>>love_nest.to_xml()
    '<XMLDogHouse module="__main__"><dogs><list module="__builtin__"><element><Dog module="__main__"><favourite_toy><str module="__builtin__">ball</str></favourite_toy><name><str module="__builtin__">Gio</str></name></Dog></element><element><Dog module="__main__"><favourite_toy><str module="__builtin__">stick</str></favourite_toy><name><str module="__builtin__">Lassie</str></name></Dog></element></list></dogs></XMLDogHouse>'

To retrieve them from their XML honey moon is just the same, `XMLDogHouse.from_xml(honey_moon_xml).dogs` and you'll get the list with `gio` and `lassie`.

## Last words

`XMLSerializerMixin` has the power to convert back and forth to XML Python's basics `built-in` types like `dict, list, tuple, int, str` and also a mechanism to convert a regular class not matter it's type (as long as it has `__dict__` and the module where it's defined is _importable_, this is **very** important).

You don't have to stop there, feel free to extend it to convert whatever type you need to use. For example: a class extending XMLSerializerMixin can add support for serialize Python's `set` elements very easily. Just inherit from it and create the method `_to_xml_set` and `_from_xml_set`. 

`XMLSerializerMixin` dynamically dispatches the functions to serialize/de-serialize their objects according to its class name. If it has defined the `_to_xml_set`, then it when it has a `set` object, it will call `_to_xml_set` to serialize it. If it's not defined, the default function used is the general `_to_xml` (used for Python's generic classes).

This extension would look like this:

    class XMLSerializerMixinWithSetSupport(XMLSerializerMixin):
        
        def _to_xml_set(self, set):
            	return self._to_xml_iterable(set)
        
        @staticmethod
        def _from_xml_set(set):
            lst = XMLSerializerMixinWithSetSupport._from_xml_iterable(parsed)
            return set(lst)

## Contribute!

If you find this class useful in some way, **please!** feel free to contribute :). If you find some bug, have some recommendation, want to rebuild this whole thing, whatever it is, I'll be delighted to hear about it.