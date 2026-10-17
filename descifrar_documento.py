from getpass import getpass

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives import padding as sym_padding
from cryptography.hazmat.primitives.asymmetric import padding as asym_padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

# 1. Cargar la clave privada RSA
with open("rsa_privada.pem", "rb") as archivo:
    clave_privada_rsa = serialization.load_pem_private_key(
        archivo.read(),
        password=getpass("Ingresa la contraseña de RSA: ").encode("utf-8")
    )

# 2. Leer la llave AES protegida
with open("clave_aes_envuelta.bin", "rb") as archivo:
    clave_aes_envuelta = archivo.read()

# 3. Recuperar la llave AES mediante RSA-OAEP
clave_aes = clave_privada_rsa.decrypt(
    clave_aes_envuelta,
    asym_padding.OAEP(
        mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

print("Llave AES recuperada correctamente.")

# 4. Leer el documento cifrado
with open("documento_cifrado.bin", "rb") as archivo:
    datos = archivo.read()

# Los primeros 16 bytes corresponden al IV
iv = datos[:16]
documento_cifrado = datos[16:]

# 5. Descifrar mediante AES-256-CBC
cipher = Cipher(
    algorithms.AES(clave_aes),
    modes.CBC(iv)
)

decryptor = cipher.decryptor()

documento_padded = (
    decryptor.update(documento_cifrado)
    + decryptor.finalize()
)

# 6. Eliminar el padding PKCS7
unpadder = sym_padding.PKCS7(128).unpadder()

documento_original = (
    unpadder.update(documento_padded)
    + unpadder.finalize()
)

# 7. Guardar el documento recuperado
with open("documento_descifrado.txt", "wb") as archivo:
    archivo.write(documento_original)

print("Documento descifrado correctamente con AES-256-CBC.")
print("Archivo generado: documento_descifrado.txt")