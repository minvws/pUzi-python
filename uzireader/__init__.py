#!/usr/bin/python3
__author__ = 'Jan Klopper <jan@underdark.nl>'

from cryptography import x509


class UziPassUser(dict):
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

    OID_IA5STRING = "2.5.5.5"  # see https://oidref.com/2.5.5.5

    def __init__(self, verify="failed", cert=None):
        """Sets up an UziPassUser object

        Expects the following vars from the webserver env
        -  SSL_CLIENT_VERIFY
        -  SSL_CLIENT_CERT
        """
        if verify != "SUCCESS":
            raise UziExceptionServerConfigError(
                "Webserver client cert check not passed"
            )
        if not cert:
            raise UziExceptionClientCertError("No client certificate presented")
        self.cert = x509.load_pem_x509_certificate(bytes(cert.encode("ascii")))
        self.update(self._getData())

    def _getName(self, rdnSequence):
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

    def _getData(self):
        """Attemps to parse the presented certificate and extract the user info
        from it"""
        if not self.cert.subject:
            raise UziException("No subject rdnSequence")

        givenName, surName = self._getName(self.cert.subject.rdns)

        for extension in self.cert.extensions:
            if extension.oid._name != "subjectAltName":
                continue

            for value in extension.value:
                if (
                    type(value) != x509.general_name.OtherName
                    or value.type_id.dotted_string != self.OID_IA5STRING
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
                    raise UziException("Incorrect SAN found")
                data[0] = data[0].split("?", 1)[1]

                return {
                    "givenName": givenName,
                    "surName": surName,
                    "OidCa": data[0],
                    "UziVersion": data[1],
                    "UziNumber": data[2],
                    "CardType": data[3],
                    "SubscriberNumber": data[4],
                    "Role": data[5],
                    "AgbCode": data[6],
                }
        raise UziException("No valid UZI data found")


class UziException(Exception):
    """Base Exception for all Uzi Exceptions"""


class UziExceptionServerConfigError(UziException):
    """Your webserver Did not pass the correct env"""


class UziExceptionClientCertError(UziException):
    """The client did not present a certificate"""
