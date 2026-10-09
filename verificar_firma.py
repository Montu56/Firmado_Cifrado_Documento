
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.exceptions import InvalidSignature

# Leer el documento original
with open("documento.txt", "rb") as archivo:
    documento = archivo.read()

# Leer la firma digital
with open("firma_documento.bin", "rb") as archivo:
    firma = archivo.read()

# Cargar la clave publica ECDSA
with open("clave_publica.pem", "rb") as archivo:
    clave_publica = serialization.load_pem_public_key(
        archivo.read()
    )

# Verificar la firma digital
try:
    clave_publica.verify(
        firma,
        documento,
        ec.ECDSA(hashes.SHA256())
    )
    print("Firma valida: el documento no fue alterado.")
except InvalidSignature:
    print("Firma INVALIDA: el documento o la firma fueron modificados.")
