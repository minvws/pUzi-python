#!/usr/bin/python3
import os
import unittest
from uzireader.exceptions import (
    UziCertificateException,
)
from uzireader.uzi import Uzi
from uzireader.uziserver import UziServer


class TestUzi(unittest.TestCase):
    def setUp(self):
        self.succ = "SUCCESS"
        self.dir = os.path.dirname(__file__)

    def readCert(self, path):
        f = open(self.dir + "/certs/" + path, "r")
        cert = f.read()
        f.close()
        return cert

    def test_check_valid_cert_022(self):
        cert = self.readCert("mock-022-correct-server-cert.cert")
        data = Uzi(self.succ, cert)

        self.assertEqual("00000000", data["AgbCode"])
        self.assertEqual("S", data["CardType"])
        self.assertEqual("2.16.528.1.1003.1.3.5.5.2", data["OidCa"])
        self.assertEqual("00.000", data["Role"])
        self.assertEqual("90000123", data["SubscriberNumber"])
        self.assertEqual("12345678", data["UziNumber"])
        self.assertEqual("1", data["UziVersion"])
        self.assertEqual("test.example.org", data["commonName"])

    def test_check_valid_cert_011(self):
        cert = self.readCert("mock-011-correct.cert")
        data = Uzi(self.succ, cert)

        self.assertEqual("00000000", data["AgbCode"])
        self.assertEqual("N", data["CardType"])
        self.assertEqual("2.16.528.1.1003.1.3.5.5.2", data["OidCa"])
        self.assertEqual("30.015", data["Role"])
        self.assertEqual("90000111", data["SubscriberNumber"])
        self.assertEqual("12345678", data["UziNumber"])
        self.assertEqual("1", data["UziVersion"])
        self.assertEqual("john doe-12345678", data["commonName"])

    def test_check_valid_server_cert(self):
        cert = self.readCert("mock-022-correct-server-cert.cert")
        data = UziServer(self.succ, cert)

        self.assertEqual("00000000", data["AgbCode"])
        self.assertEqual("S", data["CardType"])
        self.assertEqual("2.16.528.1.1003.1.3.5.5.2", data["OidCa"])
        self.assertEqual("00.000", data["Role"])
        self.assertEqual("90000123", data["SubscriberNumber"])
        self.assertEqual("12345678", data["UziNumber"])
        self.assertEqual("1", data["UziVersion"])
        self.assertEqual("test.example.org", data["commonName"])

    def test_check_invalid_server_cert(self):
        cert = self.readCert("mock-011-correct.cert")
        with self.assertRaises(UziCertificateException):
            data = UziServer(self.succ, cert)
