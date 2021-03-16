#!/usr/bin/python3
__author__ = "Rafael Dulfer <rafael.dulfer@gmail.com>"

import os
import unittest
import uzireader.exceptions as exceptions
from uzireader.uzipassuser import UziPassUser


class TestUziReader(unittest.TestCase):
    def setUp(self):
        self.succ = "SUCCESS"
        self.dir = os.path.dirname(__file__)

    def readCert(self, path):
        f = open(self.dir + "/certs/" + path, "r")
        cert = f.read()
        f.close()
        return cert

    def checkCert(self, path, message=None):
        cert = self.readCert(path)
        with self.assertRaises(exceptions.UziException, msg=message):
            UziPassUser(self.succ, cert)

    def test_check_request_has_no_cert(self):
        with self.assertRaises(exceptions.UziExceptionServerConfigError):
            UziPassUser()

    def test_check_ssl_client_failed(self):
        with self.assertRaises(exceptions.UziExceptionServerConfigError):
            UziPassUser()

    def test_check_no_client_cert(self):
        with self.assertRaises(exceptions.UziExceptionClientCertError):
            UziPassUser(self.succ)

    def test_check_cert_without_valid_data(self):
        self.checkCert("mock-001-no-valid-uzi-data.cert", "No valid UZI data found")

    def test_check_cert_with_invalid_san(self):
        self.checkCert("mock-002-invalid-san.cert", "No valid UZI data found")

    def test_check_cert_with_invalid_other_name(self):
        self.checkCert("mock-003-invalid-othername.cert", "No valid UZI data found")

    def test_check_cert_without_ia5_string(self):
        self.checkCert("mock-004-othername-without-ia5string.cert")

    def test_check_cert_incorrect_san_data(self):
        self.checkCert("mock-005-incorrect-san-data.cert", "Incorrect SAN found")

    def test_check_cert_incorrect_san_data_2(self):
        self.checkCert("mock-006-incorrect-san-data.cert", "Incorrect SAN found")

    def test_check_valid_cert(self):
        cert = self.readCert("mock-011-correct.cert")
        data = UziPassUser(self.succ, cert)

        self.assertEqual("00000000", data["AgbCode"])
        self.assertEqual("N", data["CardType"])
        self.assertEqual("john", data["givenName"])
        self.assertEqual("2.16.528.1.1003.1.3.5.5.2", data["OidCa"])
        self.assertEqual("30.015", data["Role"])
        self.assertEqual("90000111", data["SubscriberNumber"])
        self.assertEqual("doe-12345678", data["surName"])
        self.assertEqual("12345678", data["UziNumber"])
        self.assertEqual("1", data["UziVersion"])

    def test_check_valid_admin_cert(self):
        cert = self.readCert("mock-012-correct-admin.cert")
        data = UziPassUser(self.succ, cert)

        self.assertEqual("00000000", data["AgbCode"])
        self.assertEqual("N", data["CardType"])
        self.assertEqual("john", data["givenName"])
        self.assertEqual("2.16.528.1.1003.1.3.5.5.2", data["OidCa"])
        self.assertEqual("01.015", data["Role"])
        self.assertEqual("90000111", data["SubscriberNumber"])
        self.assertEqual("doe-11111111", data["surName"])
        self.assertEqual("11111111", data["UziNumber"])
        self.assertEqual("1", data["UziVersion"])
