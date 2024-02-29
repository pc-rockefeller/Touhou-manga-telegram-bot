class ParserException(Exception):
    pass

class ConnectionErrorException(ParserException):
    pass

class BadRequestException(ParserException):
    pass # TODO maybe create another python file with request exceptions