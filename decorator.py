class my_decorator(object):
    def __init__(self,flag):
        self.flag = flag
    def __call__(self, original_func):
        decorator_self = self
        def wrappee( *args, **kwargs):
            decorator_self.flag()
            z = original_func(*args,**kwargs)
            return z
        return wrappee



def for_all_methods(decorator):
    def decorate(cls):
        for attr in cls.__dict__: # there's propably a better way to do this
            if callable(getattr(cls, attr)):
                setattr(cls, attr, decorator(getattr(cls, attr)))
        return cls
    return decorate

import time

def time_wrapper(func):
    def wrapee(*args,**kwargs):
        epoch = time.time()
        obj = func(*args,**kwargs)
        print('Time delta: %f'%(time.time()-epoch,))
        return obj
    return wrapee

