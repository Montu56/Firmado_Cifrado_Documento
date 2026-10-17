
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding

# 1. Leer el documento original
with open("documento.txt", "rb") as archivo:
    documento = archivo.read()

# 2. Generar una llave AES de 256 bits
clave_aes = os.urandom(32)

# 3. Generar un IV aleatorio de 128 bits
iv = os.urandom(16)

# 4. Aplicar padding PKCS7
padder = padding.PKCS7(128).padder()
documento_padded = padder.update(documento) + padder.finalize()

# 5. Cifrar el documento con AES-CBC
cipher = Cipher(algorithms.AES(clave_aes), modes.CBC(iv))
encryptor = cipher.encryptor()

documento_cifrado = (
    encryptor.update(documento_padded) + encryptor.finalize()
)

# 6. Guardar IV y documento cifrado
with open("documento_cifrado.bin", "wb") as archivo:
    archivo.write(iv + documento_cifrado)

# 7. Guardar la llave AES localmente (solo para esta demostracion)
with open("clave_aes.key", "xb") as archivo:
    archivo.write(clave_aes)

print("Documento cifrado correctamente con AES-256-CBC.")
print("Archivo generado: documento_cifrado.bin")
print("Llave AES guardada localmente en clave_aes.key")
