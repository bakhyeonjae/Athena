import re
import datetime
import threading

class Aspecter(type):
    aspect_rules = []
    LOG_TAG = 'SHERLOCK/PROFILING/BEHAVIOUR'

    def __new__(cls,name,bases,dict):
        module_name = dict['__module__']
        for key, value in dict.items():
            if hasattr(value,"__call__") and key != "__metaclass__":
                dict[key] = Aspecter.wrap_method(value,module_name)
        return type.__new__(cls,name,bases,dict)

    @classmethod
    def register(cls,name_pattern = "", in_objects=(), out_objects=()):
        rules = {"name_pattern": name_pattern, "in_objects": in_objects, "out_objects": out_objects}
        cls.aspect_rules.append(rule)

    @classmethod
    def wrap_method(cls,method,moduleName):
        def call(*args, **kw):
            day = datetime.date.today()
            t = datetime.datetime.now().time()
            arg_str = '[args]' if len(args) > 1 else None
            for idx in range(1,len(args)):
                arg_str += str(args[idx]) + ',,'
            #print("%s %s %s %d [entry] void %s.%s() %s" % (cls.LOG_TAG, day.isoformat(), t.isoformat(), threading.get_ident(), moduleName, method.__name__, arg_str))
            print("%s %s %s %d [entry] void %s.%s()" % (cls.LOG_TAG, day.isoformat(), t.isoformat(), threading.get_ident(), moduleName, method.__name__))
            results = method(*args, **kw)
            print("%s %s %s %d [exit] void %s.%s()" % (cls.LOG_TAG, day.isoformat(), t.isoformat(), threading.get_ident(), moduleName, method.__name__))
            return results
        return call

