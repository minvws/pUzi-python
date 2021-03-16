#!/usr/bin/python3
__author__ = "Rafael Dulfer <rafael.dulfer@gmail.com>"

import unittest
import os

import uzireader.exceptions as exceptions
from uzireader.uzipassuser import UziPassUser
from uzireader.uzipassvalidator import UziPassValidator
from uzireader.consts import UZI_TYPE_CARE_PROVIDER, UZI_ROLE_NURSE, UZI_ROLE_DENTIST


class TestUziValidator(unittest.TestCase):
    def setUp(self):
        self.succ = "SUCCESS"
        self.dir = os.path.dirname(__file__)

    def readCert(self, path):
        f = open(self.dir + "/certs/" + path, "r")
        cert = f.read()
        f.close()
        return cert

    def checkUser(self, path, message=None, types=[], roles=[]):
        cert = self.readCert(path)
        user = UziPassUser(self.succ, cert)
        with self.assertRaises(exceptions.UziException, msg=message):
            validator = UziPassValidator(True, types, roles)
            validator.validate(user)

    def test_empty_user(self):
        validator = UziPassValidator(True, [], [])
        with self.assertRaises(exceptions.UziException, msg="Empty User Provided"):
            validator.validate(None)

    def test_validate_incorrect_oid(self):
        cert = self.readCert("mock-011-correct.cert")
        user = UziPassUser(self.succ, cert)
        validator = UziPassValidator(True, [], [])
        user["OidCa"] = "1.2.3.4"
        with self.assertRaises(exceptions.UziException, msg="Empty User Provided"):
            validator.validate(user)

    def test_strict_ca(self):
        self.checkUser(
            "mock-007-strict-ca-check.cert",
            "CA OID not UZI register Care Provider or named employee",
        )

    def test_incorrect_version(self):
        self.checkUser("mock-008-invalid-version.cert", "UZI version not 1")

    def test_not_allowed_type(self):
        self.checkUser(
            "mock-009-invalid-types.cert",
            "UZI card type not allowed",
            [UZI_TYPE_CARE_PROVIDER],
        )

    def test_not_allowed_role(self):
        self.checkUser(
            "mock-010-invalid-roles.cert",
            "UZI card role not allowed",
            [UZI_TYPE_CARE_PROVIDER],
            [UZI_ROLE_NURSE],
        )

    def test_is_valid(self):
        cert = self.readCert("mock-011-correct.cert")
        user = UziPassUser(self.succ, cert)
        user["CardType"] = UZI_TYPE_CARE_PROVIDER
        user["Role"] = UZI_ROLE_DENTIST
        validator = UziPassValidator(True, [UZI_TYPE_CARE_PROVIDER], [UZI_ROLE_DENTIST])
        self.assertTrue(validator.is_valid(user))
        user["Role"] = UZI_ROLE_NURSE
        self.assertFalse(validator.is_valid(user))
