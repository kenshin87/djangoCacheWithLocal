
class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class LocalCacheOperator(object):

    __metaclass__ = Singleton
    _cache = None        
    
    
    def initializeCache(self):
        if self._cache is None:
            self._cache = {}


    def __init__(self):
        self.initializeCache()


    def set(self, name, value, time=None):
        self._cache[name] = value
 
    def get(self, name):
        try:
            return self._cache[name]
        except:
            raise AttributeError


    def __getitem__(self, keyPara):

        return self.getVarFromCache(keyPara)

    def __setitem__(self, keyPara, valuePara):

        self.setVarToCache(keyPara, valuePara)






#from common.djangoapps.general_utils.cache_utils import CacheOperator

def getDjangoCache():
    try:
        import django
        from django.core.exceptions import ImproperlyConfigured
    except ImportError:
        raise ImportError, "please install django to use cache"
    try:
        from django.core.cache import cache
        return cache
    except ImproperlyConfigured:
        return LocalCacheOperator()


class CacheOperator(object):

    __metaclass__ = Singleton
    _cache = None

    def __getattr__(self, keyPara):

        return self.__getitem__(keyPara)

    def __getitem__(self, keyPara):

        return self.getVarFromCache(keyPara)

    def __setitem__(self, keyPara, valuePara):

        self.setVarToCache(keyPara, valuePara)

    def __setattr__(self, keyPara, valuePara):

        self.setVarToCache(keyPara, valuePara)

    def __init__(self):
        pass
        self.initializeCache()

    """
    下面定义的辅助函数，被上面的操作符重载函数调用。
    """
    def initializeCache(self):
        if CacheOperator._cache is None:
            CacheOperator._cache = getDjangoCache()

    def getCache(self):
        return CacheOperator._cache

    def setVarToCache(self, keyPara, valuePara):
        self.getCache().set(keyPara, valuePara, DEFAULT_TIME)

    def appendVarToCacheDict(self, keyPara, valuePara):
        # TODO
        pass

    def getVarFromCache(self, keyPara):
        returnedVal = self.getCache().get(keyPara)
        if returnedVal is None:
            raise AttributeError
        return returnedVal

