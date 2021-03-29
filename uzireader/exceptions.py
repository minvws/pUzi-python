__author__ = "Jan Klopper <jan@underdark.nl>"


class UziException(Exception):
    """Base Exception for all Uzi Exceptions"""


class UziExceptionServerConfigError(UziException):
    """Your webserver Did not pass the correct env"""


class UziExceptionClientCertError(UziException):
    """The client did not present a certificate"""


class UziAllowedRoleException(UziException):
    """The client card role is not allowed"""


class UziAllowedTypeException(UziException):
    """The client card type is not allowed"""


class UziVersionException(UziException):
    """The client card version is wrong"""


class UziCaException(UziException):
    """The client CA is invalid"""
