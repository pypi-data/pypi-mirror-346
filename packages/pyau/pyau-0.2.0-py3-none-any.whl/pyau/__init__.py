import time
import math as pymath
import random as pyrandom

# --- tables ---
class table:
    @staticmethod
    def insert(tbl, value):
        tbl.append(value)

    @staticmethod
    def remove(tbl, index=None):
        if index is None:
            return tbl.pop()
        else:
            return tbl.pop(index - 1)

    @staticmethod
    def foreach(tbl, func):
        for i, v in enumerate(tbl, 1):
            func(i, v)

# --- functions ---
def print_(*args):
    print(*args)

def typeof(value):
    return type(value).__name__

def ipairs(tbl):
    for i, v in enumerate(tbl, 1):
        yield i, v

def pairs(tbl):
    if isinstance(tbl, dict):
        return tbl.items()
    else:
        return enumerate(tbl, 1)

def wait(seconds):
    time.sleep(seconds)

# --- events ---
class EventConnection:
    def __init__(self, callback):
        self.callback = callback
        self.connected = True

    def Disconnect(self):
        self.connected = False

class Event:
    def __init__(self):
        self.connections = []

    def Connect(self, callback):
        conn = EventConnection(callback)
        self.connections.append(conn)
        return conn

    def Fire(self, *args, **kwargs):
        for conn in self.connections:
            if conn.connected:
                conn.callback(*args, **kwargs)

    def DisconnectAll(self):
        self.connections.clear()

# --- metatables ---
class Metatable:
    def __init__(self, obj):
        self.obj = obj
        self.metatable = {}

    def setmetatable(self, mt):
        self.metatable = mt

    def __getattr__(self, name):
        if name in self.metatable.get('__index', {}):
            return self.metatable['__index'][name]
        return getattr(self.obj, name)

    def __setattr__(self, name, value):
        if name in ('obj', 'metatable'):
            object.__setattr__(self, name, value)
        elif '__newindex' in self.metatable:
            self.metatable['__newindex'](self.obj, name, value)
        else:
            setattr(self.obj, name, value)

# --- coroutines ---
class Coroutine:
    def __init__(self, generator_func):
        self.gen = generator_func()
        self.finished = False

def create(func):
    return Coroutine(func)

def resume(coroutine, *args):
    try:
        result = coroutine.gen.send(*args) if args else next(coroutine.gen)
        return True, result
    except StopIteration:
        coroutine.finished = True
        return False, None

def yield_():
    return (yield)

def status(coroutine):
    if coroutine.finished:
        return "dead"
    else:
        return "suspended"

# --- math ---
class math:
    @staticmethod
    def clamp(val, min_val, max_val):
        return max(min(val, max_val), min_val)

    @staticmethod
    def max(a, b):
        return max(a, b)

    @staticmethod
    def min(a, b):
        return min(a, b)

    @staticmethod
    def abs(val):
        return abs(val)

    @staticmethod
    def floor(val):
        return pymath.floor(val)

    @staticmethod
    def ceil(val):
        return pymath.ceil(val)

    @staticmethod
    def random(min_val=0, max_val=1):
        return pyrandom.uniform(min_val, max_val)

# --- string ---
class string:
    @staticmethod
    def len(s):
        return len(s)

    @staticmethod
    def upper(s):
        return s.upper()

    @staticmethod
    def lower(s):
        return s.lower()

    @staticmethod
    def find(s, sub):
        return (s.find(sub) + 1) if sub in s else None

    @staticmethod
    def sub(s, start, end=None):
        if end is None:
            return s[start-1:]
        return s[start-1:end]
