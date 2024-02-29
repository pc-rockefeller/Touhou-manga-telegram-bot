from parsers import *

if __name__ == '__main__':
    parsers = []
    globalObjs = list(globals().items())

    for name, obj in globalObjs:
        print(name, obj)
        if obj is not BaseParser and isinstance(obj, type) and issubclass(obj, BaseParser):
            parsers.append(obj())
    
    print(parsers[0].parseElementsCount('touhou project'))
    print(parsers[0].parseElement('touhou project', 22))
    print(parsers[0].parseElement('touhou project', 23))
