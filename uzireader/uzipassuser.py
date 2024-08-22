#!/usr/bin/python3
from cryptography import x509
from uzireader.exceptions import (
    UziException,
    UziExceptionServerConfigError,
    UziExceptionClientCertError,
    UziCertificateException,
    UziCertificateNotUziException,
)
from uzireader.consts import OID_IA5STRING
from uzireader.uzi import Uzi


class UziPassUser(Uzi):
    """UziPassUser dict like object with the following keys:

    givenName: givenName,
    surName: surName,
    OidCa: OID CA,
    UziVersion: UZI Version,
    UziNumber: UZI Number,
    CardType: Card Type,
    SubscriberNumber: Subscriber number,
    Role: Role (reference page 89),
    AgbCode: ABG Code,

    For reference please read
    https://www.zorgcsp.nl/documents/RK1%20CPS%20UZI-register%20V10.2%20ENG.pdf
    """

    def __init__(self, verify="failed", cert=None):
        """Sets up an UziPassUser object

        Expects the following vars from the webserver env
        -  SSL_CLIENT_VERIFY
        -  SSL_CLIENT_CERT
        """
        super().__init__(verify, cert)
        if self.get('CardType') not in ["Z", "N", "M"]:
            raise UziCertificateException("Uzi CardType is not User (Z/N/M)")

        givenName, surName, commonName = None, None, None
        try:
            givenName, surName = self._getUserNames(self.cert.subject.rdns)
        except ValueError:
            # fallback to commonName
            commonName = self["commonName"]

        self["givenName"] = givenName
        self["surName"] = surName
        self["commonName"] = commonName

    def _getUserNames(self, rdnSequence):
        """Finds and returns the surName, and givenName"""
        givenName = None
        surName = None
        for sequence in rdnSequence:
            for attribute in sequence:
                if attribute.oid._name == "surname":
                    surName = attribute.value

                if attribute.oid._name == "givenName":
                    givenName = attribute.value

                if givenName and surName:
                    return (givenName, surName)
        raise UziException("No surname / givenName found.")
