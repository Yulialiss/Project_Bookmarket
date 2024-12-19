from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from datetime import datetime, timedelta

# Генерація RSA ключа
key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)

# Збереження приватного ключа
with open("django.key", "wb") as key_file:
    key_file.write(
        key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption(),
        )
    )

# Генерація самопідписаного сертифіката
subject = issuer = x509.Name([
    x509.NameAttribute(NameOID.COUNTRY_NAME, u"UA"),
    x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"Kyiv"),
    x509.NameAttribute(NameOID.LOCALITY_NAME, u"Kyiv"),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"My Organization"),
    x509.NameAttribute(NameOID.COMMON_NAME, u"localhost"),
])
cert = x509.CertificateBuilder().subject_name(
    subject
).issuer_name(
    issuer
).public_key(
    key.public_key()
).serial_number(
    x509.random_serial_number()
).not_valid_before(
    datetime.utcnow()
).not_valid_after(
    datetime.utcnow() + timedelta(days=365)
).sign(key, hashes.SHA256())

# Збереження сертифіката
with open("django.crt", "wb") as cert_file:
    cert_file.write(cert.public_bytes(serialization.Encoding.PEM))
