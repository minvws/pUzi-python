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


class Uzi(dict):
    """UziPass dict like object with the following keys:

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
        """Sets up an Uzi object

        Expects the following vars from the webserver env
        -  SSL_CLIENT_VERIFY
        -  SSL_CLIENT_CERT
        """
        super().__init__()
        if verify != "SUCCESS":
            raise UziExceptionServerConfigError(
                "Webserver client cert check not passed"
            )
        if not cert:
            raise UziExceptionClientCertError("No client certificate presented")
        self.cert = x509.load_pem_x509_certificate(bytes(cert.encode("ascii")))
        self.update(self._getData())


    def _getCommonName(self, rdnSequence):
        """Finds and returns the commonName"""
        for sequence in rdnSequence:
            for attribute in sequence:
                if attribute.oid._name == "commonName":
                    return attribute.value
        raise UziException("No commonName found.")


    def _getData(self):
        """Attemps to parse the presented certificate and extract the user info
        from it"""
        if not self.cert.subject:
            raise UziCertificateException("No subject rdnSequence")

        commonName = self._getCommonName(self.cert.subject.rdns)

        for extension in self.cert.extensions:
            if extension.oid._name != "subjectAltName":
                continue

            for value in extension.value:
                if (
                    type(value) != x509.general_name.OtherName
                    or value.type_id.dotted_string != OID_IA5STRING
                ):
                    continue

                subjectAltName = value.value.decode("ascii")

                # Reference page 60
                #
                # [0] OID CA
                # [1] UZI Version
                # [2] UZI number
                # [3] Card type
                # [4] Subscriber number
                # [5] Role (reference page 89)
                # [6] AGB code

                data = subjectAltName.split("-")
                if len(data) < 6:
                    raise UziCertificateException("Incorrect SAN found")

                if '=' in data[0]:
                    # To remove the \x16= prefix from the OidCa, for example \x16=2.16.528.1.1007.99.217
                    data[0] = data[0].split("=", 1)[1]
                elif '?' in data[0]:
                    data[0] = data[0].split("?", 1)[1]

                return {
                    "commonName": commonName,
                    "OidCa": data[0],
                    "UziVersion": data[1],
                    "UziNumber": data[2],
                    "CardType": data[3],
                    "SubscriberNumber": data[4],
                    "Role": data[5],
                    "AgbCode": data[6],
                }
        raise UziCertificateNotUziException("No valid UZI data found")
