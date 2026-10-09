from getpass import getpass
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec

# 1. Leer el documento original
with open("documento.txt", "rb") as archivo:
    documento = archivo.read()

# 2. Cargar la clave privada ECDSA
password = getpass("Contraseña de la clave privada: ")



with open("clave_privada.pem", "rb") as archivo:
    clave_privada = serialization.load_pem_private_key(
        archivo.read(),
        password=password.encode("utf-8")
    )

# 3. Firmar el documento con ECDSA y SHA-256
firma = clave_privada.sign(
    documento,
    ec.ECDSA(hashes.SHA256())
)

# 4. Guardar la firma digital
with open("firma_documento.bin", "wb") as archivo:
    archivo.write(firma)

print("Documento firmado correctamente con ECDSA.")
print("Firma guardada en firma_documento.bin")
