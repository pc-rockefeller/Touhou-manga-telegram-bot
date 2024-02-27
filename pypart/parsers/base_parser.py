class BaseParser:
    def getName() -> str:
        """ Gets the name of a parser """
        return 'BaseParser'
    def parseElementsCount(self) -> int:
        """ Parses site to get count of elements (mangas) """
        pass
    def parseElement(self, elementNumber : int) -> str:
        """ Parses site to get an element and returns link """
        pass