# pUZI python
Proficient UZI pass reader in python, based on work by Anne Jan: https://github.com/minvws/pUZI-php

The UZI card is part of an authentication mechanism for medical staff and doctors working in the Netherlands. The cards are distributed by the CIBG. More information and the relevant client software can be found at www.uziregister.nl (in Dutch).

pUZI is a simple and functional module which allows you to use the UZI cards as authentication mechanism. It consists of:

1. a reader that reads the data on the card and gives an UziUser object in return (this repository).

pUZI is available under the EU PL licence. It was created early 2021 during the COVID19 campaign as part of the vaccination registration project BRBA for the ‘Ministerie van Volksgezondheid, Welzijn & Sport, programma Realisatie Digitale Ondersteuning.’

Questions and contributions are welcome via [GitHub](https://github.com/minvws/pUzi-python/issues).

## Requirements

* python >= 3.6

Apache config (or NginX equivalent):
```apacheconf
SSLEngine on
SSLProtocol -all +TLSv1.3
SSLHonorCipherOrder on
SSLCipherSuite ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-CHACHA20-POLY1305:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384
SSLVerifyClient require
SSLVerifyDepth 3
SSLCACertificateFile /path/to/uziCA.crt
SSLOptions +StdEnvVars +ExportCertData
```

## Installation
```bash
pip install pUzi
```

## Usage

```python3
from uzireader.uzipassuser import UziPassUser
uzipas = UziPassUser(env['SSL_CLIENT_VERIFY'], env['SSL_CLIENT_CERT'])
print(uzipas)
```

```text
{'givenName': 'john', 'surName': 'doe-11111111', 'OidCa': '2.16.528.1.1003.1.3.5.5.2', 'UziVersion': '1', 'UziNumber': '11111111', 'CardType': 'N', 'SubscriberNumber': '90000111', 'Role': '01.015', 'AgbCode': '00000000'}
```

## Uses

[Python cryptography Library](https://cryptography.io/en/)

## Contributing

1. Fork the Project

2. Ensure you have Black installed (pip3 install black)

3. Create a Feature Branch

4. (Recommended) Check whether your code conforms to our Coding Standards by running black on your changed files

5. Send us a Pull Request
