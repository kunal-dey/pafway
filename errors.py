FAILED__MAIL_SERVER_CONNECT = "Failed to connect the MAIL server."
INTERNAL_SERVER_ERROR = "An error occured from our side"
MISSING_PARAMETER_ERROR = "{} is missing"
TYPE_ERROR = "The type of the parameter is not of type {}"


class MailException(Exception):
    def __init__(self, message:str = FAILED__MAIL_SERVER_CONNECT):
        super().__init__(message)

class DBConnectionException(Exception):
    def __init__(self, message:str = INTERNAL_SERVER_ERROR):
        self.message = message
        super().__init__(message)

class MissingParameterException(Exception):
    def __init__(self, parameter:str):
        self.message = MISSING_PARAMETER_ERROR.format(parameter)
        super().__init__()

class TypeException(Exception):
    def __init__(self, type:str):
        self.message = TYPE_ERROR.format(type)
        super().__init__(TYPE_ERROR.format(type))