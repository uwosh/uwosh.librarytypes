from zope.interface import Interface,Attribute

class IMemoizeHook(Interface):
    """
    Hook interface.  Makes sure you are properly implementing 
    the function cache_timeout() below.
    """
    seconds_to_cache = Attribute("""How many seconds to cache""")



def cache_timeout(class_type):
    """
    This is function hook, to allow manipulation of the cache
    """
    return int(class_type.seconds_to_cache)
        
