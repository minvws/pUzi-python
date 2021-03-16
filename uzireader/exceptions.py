__author__ = "Jan Klopper <jan@underdark.nl>"


class UziException(Exception):
    """Base Exception for all Uzi Exceptions"""


class UziExceptionServerConfigError(UziException):
    """Your webserver Did not pass the correct env"""


class UziExceptionClientCertError(UziException):
    """The client did not present a certificate"""
