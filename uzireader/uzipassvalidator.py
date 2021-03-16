__author__ = "Rafael Dulfer <rafael.dulfer@gmail.com>"

from uzireader.consts import OID_CA_CARE_PROVIDER, OID_CA_NAMED_EMPLOYEE
from uzireader.exceptions import UziException
from uzireader.uzipassuser import UziPassUser


class UziPassValidator:
    def __init__(self, strict_ca: bool, allowed_types: list, allowed_roles: list):
        self.strict_ca = strict_ca
        self.allowed_types = allowed_types
        self.allowed_roles = allowed_roles

    def is_valid(self, user: UziPassUser):
        try:
            self.validate(user)
        except UziException:
            return False
        return True

    def validate(self, user: UziPassUser):
        if user is None:
            raise UziException("Empty User Provided")
        oidca = user["OidCa"]
        if (
            self.strict_ca
            and oidca != OID_CA_CARE_PROVIDER
            and oidca != OID_CA_NAMED_EMPLOYEE
        ):
            raise UziException(
                "CA OID not UZI register Care Provider or named employee"
            )
        if user["UziVersion"] != "1":
            raise UziException("UZI version not 1")
        if user["CardType"] not in self.allowed_types:
            raise UziException("UZI card type not allowed")
        if user["Role"][:3] not in self.allowed_roles:
            raise UziException("UZI card role not allowed")
