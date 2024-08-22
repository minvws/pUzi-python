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


class UziServer(Uzi):
    """Uzi dict like object with the following keys:

    commonName: The certificate common name
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
        """Sets up an UziServer object

        Expects the following vars from the webserver env
        -  SSL_CLIENT_VERIFY
        -  SSL_CLIENT_CERT
        """
        super().__init__(verify, cert)

        if self.get('CardType') != 'S':
            raise UziCertificateException("Uzi CardType is not S (Server)")
